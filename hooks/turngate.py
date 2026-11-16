#!/usr/bin/env python3
"""turngate.py: the turn model and the call classifier behind the turn gates.

Used by turn-gates-pretool.py (the merge gate and the plan-shown advisory), governance-enforce.py (the Stop
gate), governance-trigger.py and govclass.py (the harness-lead test), and by shell hooks through the `span`
command line at the end of this file. Three layers, each usable alone:

  rows   -> events   row_events(rows): what each row of the session record IS (the owner, a wake, a result ...)
  events -> Model    the window of the merge word, the governance turn, the stretch one Stop judges
  call   -> acts     classify_call(name, input, cwd): what a tool call DOES (shell commands are parsed)

The decisions (merge_decision, f1_decision) read only the last two.

Nothing here raises to its caller on bad input, except parse_shell (caught in shell_acts). A row that cannot be
read is kept as BAD and counted. Which way a failure goes is the hooks' business: closed for a merge, open for
everything else.

Every hand-set value is an upper-case name in section 1. No environment variable and no key of a hook's input
switches a rule off: the only lookups in the environment are where state files go and what counts as scratch.

Standard library only; imports nothing from this directory; runs on Python 3.8 and later.
"""
import bisect
import calendar
import hashlib
import json
import os
import re
import shlex
import sys
import time
import unicodedata

# ----------------------------------------------------------------------------------------------------------------
# 1. Hand-set values
# ----------------------------------------------------------------------------------------------------------------
GOVERNORS = ("plan-gate", "adversarial-verify", "scope-fence")
PLAN_GOVERNOR = "plan-gate"                    # must be loaded before an outward action
VERIFY_GOVERNOR = "adversarial-verify"         # must be loaded somewhere in the same governance turn
SKILL_TOOL = "Skill"

# -- rows: who wrote a row of the session record
OWNER_ORIGIN_KINDS = ("human",)                # origin.kind of what the owner typed
SCHEDULED_ORIGIN_KINDS = ("scheduled-trigger",)   # origin kind or subkind of a scheduled delivery, where a row has it
OWNER_MEDIA_BLOCKS = ("image", "document")     # a message with no text and one of these is still the owner's
WAKE_LEADS = ("<task-notification>", "[SYSTEM NOTIFICATION", "<wake ", "<agent-message", "<webhook-payload",
              "<system-notification", "<child-session-event")
ECHO_LEADS = ("<local-command-stdout>", "<local-command-stderr>", "<local-command-caveat>", "<bash-input>",
              "<bash-stdout>", "<bash-stderr>", "<system-reminder>")
LOCAL_ECHO_LEADS = ("<local-command-stdout>", "<local-command-stderr>", "<local-command-caveat>")
COMMAND_LEADS = ("<command-name>", "<command-message>")
COMMAND_NAME = re.compile(r"<command-name>\s*(.*?)\s*</command-name>", re.S)
COMMAND_ARGS = re.compile(r"<command-args>(.*?)</command-args>", re.S)
LOCAL_COMMANDS = ("/model", "/clear", "/compact", "/config", "/cost", "/help", "/status", "/usage", "/mcp", "/login",
                  "/logout", "/exit", "/resume", "/rename", "/context", "/permissions", "/hooks", "/plugin")
LOCAL_COMMAND_REACH = 2                        # rows on either side in which a local-command echo marks a command row
INTERRUPT_LEAD = "[Request interrupted by user"
HOOK_FEEDBACK_LEAD = "Stop hook feedback"
RESTART_LEAD = "This session's worker process was restarted"
OUR_BLOCK_MARK = "GOV-ENFORCE"                 # in every block reason of governance-enforce.py
F1_BLOCK_MARK = "outward action"               # in its outward-action reason only
RECEIPT_BLOCK_MARK = "Receipt law"             # in the receipt gate's reason (counted for it by `span`)
HARNESS_MARKERS = WAKE_LEADS + ECHO_LEADS + COMMAND_LEADS      # the one list of what a harness text starts with

# -- cards and notifications
CARD_TOOL = "AskUserQuestion"
ANSWER_LEADS = ("Your questions have been answered:", "The user answered:")
ANSWER_MARK = '"%s"="'                         # how a result text introduces the answer to one question
ANSWER_END = '"'
ANSWER_JOIN = ","                              # how the labels of a multi-select answer are joined
ANSWER_CHOICE = re.compile(r'="([^"]*)"')
NOTIF_READ_TOOLS = ("ReadNotifications",)
NOTIF_RESULT_LEAD = "[SYSTEM NOTIFICATION - NOT USER INPUT]"
# The label ends at the first " · queued at: " (a tempered run, so a long line cannot make the search slow).
NOTIF_HEADER = re.compile(r"^--- Notification (\d+) of (\d+) · id: \S+ · origin: ((?:(?! · queued at: ).)+)"
                          r" · queued at: .*---[ \t]*$", re.M)
SCHEDULED_ORIGIN_PREFIX = "scheduled trigger"
YES_LABEL = re.compile(r"^\W*(?:yes|yep|yeah|approved?|go ahead|proceed|do it|confirm(?:ed)?|ok|okay)\b")
CARD_ALL_WORD = re.compile(r"\b(?:both|all|every|each|everything)\b")
RECOMMENDED = re.compile(r"\(\s*recommended\s*\)")

# -- the owner's word. Every text is normalised first (normalize): lower case, straight quotes and dashes.
DEFAULT_BRANCHES = ("main", "master")
MERGE_VERB_TEXT = r"(?:(?:auto|squash|rebase)[- ]?)?merge"
PUSH_VERB_TEXT = r"(?:push|merge|commit|land)"
MERGE_VERB = re.compile(r"(?<![\w-])(" + MERGE_VERB_TEXT + r")(?![\w-])")
MERGE_ANY = re.compile(r"(?<![\w])(?:auto-?)?merg(?:e|ed|es|ing)(?![\w])")
MERGE_NOUN_BEFORE = re.compile(r"(?:\b(?:the|a|an|this|that|last|previous|next|my|your|our|its|every|each|any|no)|(?<!\blet)'s)\s+$")
MERGE_NOUN_AFTER = re.compile(r"^[- ](?:conflicts?|commits?|gate|queue|requests?|word|button|base|strategy|tool|route|check)\b")
# The words an order may start with. One separator class, in one place, after each word, and no word that is also
# a part of another ("go ahead" and "and" are two words, not "go ahead and"): a text cannot be read in two ways,
# so a long run of these words cannot make the search slow (A8).
ORDER_LEADIN_WORDS = ("yes", "yep", "yeah", "ok", "okay", "sure", "great", "good", "fine", "perfect", "approved?", "lgtm",
                      "thanks", "thank you", "please", "now", "then", "and", "so", "also", "just", "do", "go ahead",
                      "you (?:can|may)", "feel free to", "let's", "lets", "looks good", "sounds good",
                      "(?:can|could|would|will) you")
LEADIN_SEPARATORS = r"[\s,:;.!-]*"             # what may stand between the lead-in words
ORDER_LEADIN = (LEADIN_SEPARATORS + r"(?:(?:" + "|".join(ORDER_LEADIN_WORDS) + r")\b" + LEADIN_SEPARATORS + r")*")
TYPED_ORDER = re.compile(r"^" + ORDER_LEADIN + r"(" + MERGE_VERB_TEXT + r")(?![\w-])")
PUSH_ORDER = re.compile(r"^" + ORDER_LEADIN + r"(?:force[- ]?)?" + PUSH_VERB_TEXT + r"(?![\w-])")
CARD_ORDER = re.compile(r"^\W*(?:yes\W+)?(" + MERGE_VERB_TEXT + r")(?![\w-])")
CARD_PUSH_ORDER = re.compile(r"^\W*(?:yes\W+)?(?:force[- ]?)?" + PUSH_VERB_TEXT + r"(?![\w-])")
REFUSAL_CUE = re.compile(
    r"(?<![\w-])(?:no|not|never|none|neither|nor|nothing|without|cannot|stop|wait|hold|pause|later|dont|cant|wont|"
    r"shouldnt|isnt|doesnt|didnt|except|excluding|exclude|skip|leave|until|unless|cancel|abort|"
    r"other than|apart from|instead of|rather than|\w+n't)(?![\w-])")
REFUSAL_START = re.compile(r"^\W*(?:no|nope|not|don't|dont|do not|never|wait|later|hold|skip|cancel|stop|neither|none|nothing|"
                           r"keep|leave|defer|postpone|abort|pause)\b")
OPEN_NEGATOR = re.compile(r"(?<![\w-])(?:do not|don't|dont|never|cannot|can't|cant|won't|wont|will not|shouldn't|should not|"
                          r"mustn't|must not)(?![\w-])")
AFFIRMATIVE_PHRASES = ("no objections", "no objection", "no problems", "no problem", "no worries", "no issues", "no issue",
                       "no concerns", "no complaints", "no blockers", "not a problem", "nothing against", "why not",
                       "no need to wait", "no rush", "no hurry", "no pressure", "nothing else", "can't wait", "cannot wait",
                       "don't forget to", "dont forget to", "do not forget to",
                       # M2: a negated hold is a go-ahead
                       "let's not wait", "lets not wait", "don't wait", "dont wait", "do not wait", "don't hold off",
                       "do not hold off", "let's not delay", "don't delay", "do not delay", "without waiting",
                       "no more waiting")
# A2, A5: words that hold the work back. Un-negated when no HALT_NEGATOR word stands before them in their clause.
# They only REVOKE (a typed order grants only when it is plain, D4): revoking too much costs one card.
HALT_WORDS = ("wait", "hold", "stop", "pause", "cancel", "abort", "postpone", "defer", "delay", "not yet", "not now",
              "never mind", "nevermind", "scratch that", "second thought", "second thoughts", "changed my mind",
              "change of plan", "change of plans", "let's not", "lets not", "hang on", "on hold",
              "one sec", "one second", "a sec", "one moment", "a moment", "a minute", "give me", "hold up", "not so fast")
HALT_CUE = re.compile(r"(?<![\w-])(?:" + "|".join(sorted(HALT_WORDS, key=len, reverse=True)) + r")(?![\w-])")
HALT_NEGATOR = re.compile(r"(?<![\w-])(?:no|not|never|without|cannot|dont|cant|wont|\w+n't)(?![\w-])")
# M6: the first word after an order's pull requests that makes the clause a statement about them; a statement that
# also refuses or holds ("Merge #34 can wait.") takes them out of the grant.
STATEMENT_WORDS = ("is", "isn't", "isnt", "was", "wasn't", "are", "aren't", "were", "has", "hasn't", "had", "have", "does",
                   "doesn't", "did", "didn't", "will", "won't", "would", "wouldn't", "should", "shouldn't", "can", "can't",
                   "cannot", "could", "couldn't", "might", "may", "must", "needs", "need", "failed", "fails", "broke",
                   "breaks", "looks", "seems", "appears", "got", "went", "still")
STATEMENT_NEXT = re.compile(r"^\s*([a-z][\w']*)")
# A5: words a refusal may start with; they are dropped before the short-refusal test.
SOFT_LEADIN_WORDS = ("actually", "well", "hmm", "hm", "um", "uh", "oh", "sorry", "please", "ok", "okay", "so", "and", "also",
                     "maybe", "perhaps", "i think", "i guess", "on second thought")
SOFT_LEADIN = re.compile(r"^(?:[\s,:;.!-]*(?:" + "|".join(sorted(SOFT_LEADIN_WORDS, key=len, reverse=True))
                         + r")(?![\w-]))+[\s,:;.!-]*")
QUESTION_LEADIN_WORDS = ORDER_LEADIN_WORDS + ("shall i", "shall we", "should i", "should we", "do you want me to",
                                              "want me to", "would you like me to", "can i", "may i", "do i", "ok to",
                                              "okay to", "is it ok to", "is it okay to")
QUESTION_LEADIN = (LEADIN_SEPARATORS + r"(?:(?:" + "|".join(sorted(QUESTION_LEADIN_WORDS, key=len, reverse=True))
                   + r")\b" + LEADIN_SEPARATORS + r")*")
QUESTION_ORDER = re.compile(r"^" + QUESTION_LEADIN + r"(" + MERGE_VERB_TEXT + r")(?![\w-])")
QUESTION_PUSH = re.compile(r"^" + QUESTION_LEADIN + r"(?:force[- ]?)?(" + PUSH_VERB_TEXT + r")(?![\w-])")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?;])\s+|\n+|\s+\bbut\b\s+|\s+\bhowever\b\s+")
CLAUSE_SPLIT = re.compile(r",\s+|:\s+|\s+-\s+|\s+\bthen\b\s+|\s+\band\b\s+(?=(?:please\s+|just\s+|also\s+|then\s+)?"
                          + MERGE_VERB_TEXT + r"(?![\w-]))")
QUESTION_END = "?"
POLITE_REQUEST = re.compile(r"^[\s,:;.!-]*(?:\w+[\s,]+){0,3}(?:can|could|would|will) you\b")
# -- D4 (the owner's decision of 2026-11-16): a typed message grants only when its LAST sentence is a plain order.
# Every list below lets an order through; none of them is what stops a merge. A wordier order costs one card.
ORDER_MESSAGE_MAX_CHARS = 4000                  # A1: a longer message is not read for an order: it grants nothing
SENTENCE_END_MARKS = (".", "!", "?")            # A1: a line break ends a sentence only after one of these
CLAUSE_END_MARKS = ".!?;"                       # dropped from the end of a clause before it is read
# A2: a sentence after the order made only of these words closes the message; any other sentence there voids it
CLOSING_WORDS = ("thanks", "thank you", "thx", "cheers", "please", "go", "go ahead", "do it", "that's all", "that is all")
CLOSING_SENTENCE = re.compile(r"^\W*(?:(?:" + "|".join(sorted(CLOSING_WORDS, key=len, reverse=True)) + r")(?![\w'-])\W*)+$")
# A3 (1): a clause before the order made only of lead-in words or of one affirmative phrase
LEADIN_CLAUSE = re.compile(r"^" + LEADIN_SEPARATORS + r"(?:(?:" + "|".join(ORDER_LEADIN_WORDS + ("first",))
                           + r")\b" + LEADIN_SEPARATORS + r")+$")
# A3 (3): what may follow an order's pull requests in its own clause; nothing else may
ORDER_TAIL_WORDS = ("now", "right now", "right away", "immediately", "today", "asap", "please", "pls", "thanks", "too",
                    "as well", "first", "squash", "squashed", "yourself", "after all", "with squash", "with rebase",
                    "with a merge commit", "for me", "for us")
ORDER_DESTINATION = (r"(?:into|to|onto)\s+(?:the\s+)?(?:" + "|".join(re.escape(b) for b in DEFAULT_BRANCHES)
                     + r"|default)(?:\s+branch)?")
ORDER_TAIL = re.compile(r"\s*,?\s*(?:(?:" + "|".join(re.escape(w) for w in sorted(ORDER_TAIL_WORDS, key=len, reverse=True))
                        + r"|" + ORDER_DESTINATION + r")(?![\w'-])|\([^()]{0,200}\))")
ORDER_TAIL_END = re.compile(r"\s*[.!?]*\s*$")
# A3 (3), A5: the object of an order that names no number: the card's pull requests (none for a typed message)
ORDER_OBJECT_WORDS = ("it", "this", "that", "them", "this one", "that one", "both", "both of them", "all", "all of them",
                      "everything", "the pr", "the prs", "this pr", "the pull request", "the pull requests")
ORDER_COUNT_WORDS = ("two", "three", "four", "five", "six")    # "merge all three", "merge both PRs" (a card option)
ORDER_OBJECT = re.compile(r"\s*,?\s*(?:" + "|".join(re.escape(w) for w in sorted(ORDER_OBJECT_WORDS, key=len, reverse=True))
                          + r")(?:\s+(?:of\s+)?(?:them|these|those|the))?(?:\s+(?:" + "|".join(ORDER_COUNT_WORDS)
                          + r"))?(?:\s+(?:prs?|pull\s+requests?|ones?))?(?![\w'-])")
# A3 (4): a clause after the order made only of numbers and list words ("34 first", "then #141")
ORDER_LIST_CLAUSE = re.compile(r"^\W*(?:(?:and|&|\+|plus|also|then|both|first|prs?|pull requests?|#?\d+(?!\d))\W*)+$")
# A3 (2, 4): a refusal that names only OTHER pull requests ("not #141", "don't merge #26", "leave 141 alone"): it
# starts with one of REFUSAL_START and holds, besides its numbers, only these words
REFUSAL_OTHER_WORDS = ("no", "not", "nope", "don't", "dont", "do", "never", "leave", "alone", "keep", "open", "hold", "skip",
                       "wait", "for", "my", "word", "on", "merge", "pr", "prs", "pull", "request", "requests", "and", "or",
                       "nor", "neither", "yet", "the", "other", "one", "please", "just", "touch", "that", "those")
REFUSAL_OTHER_WORD = re.compile(r"[a-z][a-z']*")
REFUSAL_OTHER_LEAD = re.compile(r"^(?:(?:then|and|also|but|please|just)\s+)+")    # "then wait for my word on #141"
# A3 (3): the words an order's list may hold besides its numbers, unless the numbers stand in a bracket ("merge
# library only (#34)"); an object word ("it", "both") counts too
ORDER_LIST_WORDS = ("and", "plus", "also", "pr", "prs", "pull", "request", "requests", "the", "both", "all", "of", "them")
ORDER_WORD = re.compile(r"[a-z][\w'-]*")
# The push order (Q2, D4): lead-in words, the push verb, at most OBJECT_FILLER_MAX words of object, the default
# branch as the destination, then only tail words
PUSH_DESTINATION = re.compile(r"\s*(?<![\w/.-])(?:to|into|onto|on)\s+(?:the\s+)?(?:(?:origin|upstream)[/ ])?(?:(?:"
                              + "|".join(re.escape(b) for b in DEFAULT_BRANCHES)
                              + r")(?:\s+branch)?|default\s+branch)(?![\w/-]|\.\w)")
PUSH_OBJECT_WORD = re.compile(r"\s*[\w'/.-]+")
GRANT_OPS = ("grant", "branch")
CODE_FENCE = re.compile(r"```.*?```", re.S)
QUOTE_LEAD = ">"
STANDALONE_REFUSAL_MAX_WORDS = 6
OBJECT_FILLER_MAX = 3
OBJECT_STOP_WORDS = ("after", "before", "when", "once", "if", "then", "that", "which", "so", "because", "while",
                     "to", "into", "onto", "for", "with", "from", "on", "in", "at", "as")
OBJECT_TAIL_WORDS = ("now", "please", "pls", "asap", "today", "too", "thanks", "first", "then", "with", "using", "via",
                     "squash", "squashed")
OBJECT_GAP = re.compile(r"\s*,?\s*")
OBJECT_PAREN = re.compile(r"\([^)]*\)")
# a bracket in an order clause (typed, a card's option or its question) is a label only when every word in it is one of
# these, a pull request reference or number, a repository name (a word that holds "/") or a list mark; any other word
# ("(after the audit)", "(draft)") makes the clause no plain order
BRACKET_LABEL_WORDS = ("library", "lib", "deck", "kit", "docs", "plugin", "core", "the", "recommended", "and")
BRACKET_WORD = re.compile(r"[^\s,&()]+")
OBJECT_LIST_WORD = re.compile(r"(?:and\b|&|\+)")
OBJECT_LIST_MORE = re.compile(r"(?:and\b|&|\+)(?=\s*(?:(?:prs?|pull requests?)\s*)?#?\d)")
OBJECT_NUMBER_END = ",.;!?)("
OBJECT_WORD = re.compile(r"[\w'/-]+")
OBJECT_TAIL = re.compile(r"[a-z]+")
PR_REF = re.compile(r"(?:https?://github\.com/(?P<uo>[\w.-]+)/(?P<ur>[\w.-]+)/pull/(?P<un>\d+)"
                    r"|(?P<ro>[\w.-]+)/(?P<rr>[\w.-]+)#(?P<rn>\d+)"
                    r"|(?:\b(?:prs?|pull requests?|pull)\s*(?:number\s*|no\.?\s*)?#?\s*(?P<pn>\d+))"
                    r"|#(?P<hn>\d+))(?![\w])")
PR_LIST_MORE = re.compile(r"\s*(?:,\s*and|,|and|&|\+)\s*(?:(?:prs?|pull requests?)\s*)?#?(\d+)(?!\w|\.\d)")
BARE_NUMBER = re.compile(r"#?(\d+)(?!\w|\.\d)")
BARE_NUMBERS = re.compile(r"(?<![\w#.])\d+(?![\w.])")

# -- policy switches (the owner's answers of 2026-11-13 and 2026-11-15; one line each)
SCHEDULED_READ_ENDS_WORD = True                # a scheduled notification read mid-turn ends the word given before it
RESTART_ENDS_WORD = True                       # so does the restart notice of the worker process
POLICY_DENY_UNATTENDED = "deny-unattended"
POLICY_DENY = "deny"
POLICY_ALLOW = "allow"
PUSH_UNKNOWN_BRANCH_POLICY = POLICY_DENY_UNATTENDED   # a push whose branch cannot be read: denied where the owner is absent
DELEGATE_MAY_MERGE = True                      # a helper agent may merge what the owner's standing word names
QUEUED_OWNER_ATTENDS_RUN = True                # a message the owner types during a scheduled run makes the rest of it attended
MIDTURN_MESSAGE_ENDS_WORD = True               # D4: a message typed mid-turn that is no plain order ends the word
BARE_NUMBER_ONE_REPOSITORY = True              # a word naming a number without a repository covers it in one repository
F1_MAX_BLOCKS = 2                              # blocks of the outward-action rule in one stretch
PROMPT_CLASS_MAX_BLOCKS = 1                    # blocks of the prompt-class rule in one stretch
WAKE_TURN_INHERITS_LOADS = True                # work woken after a completed stop keeps the turn's governor loads
COMPACTION_VOIDS_LOADS = True                  # an outward action after a compaction needs the governors loaded again
CLASSIFY_CARD_ANSWERS = False                  # a clicked label is not a prompt for the prompt-class rule
# AS-3 (the documents do not decide; default taken without a question): a helper's noted act is charged to the
# stretch in which it happens, also when the helper was started in an earlier turn. False: such an act is charged
# only to a stretch whose main thread started a helper (HELPER_TOOLS) before it.
HELPER_ACT_PLACED_BY_TIME = True
HELPER_TOOLS = ("Agent", "Task")               # the main thread's calls that start a helper agent
MERGE_GATED_KINDS = ("merge", "push_default")
F1_COUNTED_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "file_push", "schedule")
# What the plan-shown advisory treats as a write. A list of its own: the Stop gate's list above is one of the
# owner's switches, and changing it must change neither the advisory nor what the merge gate looks at.
WRITE_KINDS = ("merge", "push_default", "push", "commit", "pr_write", "file_push", "schedule", "write")

# -- what a call does: tools by name. For an `mcp__` name the leaf after the last `__` is matched exactly.
MCP_PREFIX = "mcp__"
MCP_SEPARATOR = "__"
MERGE_TOOL_LEAVES = ("merge_pull_request", "enable_pr_auto_merge")
FILE_PUSH_LEAVES = ("push_files", "create_or_update_file", "delete_file")
PR_WRITE_LEAVES = ("create_pull_request", "update_pull_request", "update_pull_request_branch", "disable_pr_auto_merge",
                   "actions_run_trigger")
SCHEDULE_LEAVES = ("create_trigger", "update_trigger", "delete_trigger", "fire_trigger", "send_later")
SCHEDULE_TOOLS = ("CronCreate", "CronDelete", "ScheduleWakeup")
OTHER_OUTWARD_LEAVES = (
    "create_branch", "create_repository", "fork_repository", "delete_repository", "issue_write", "sub_issue_write",
    "add_issue_comment", "update_issue_comment", "pull_request_review_write", "add_comment_to_pending_review",
    "add_reply_to_pull_request_comment", "request_copilot_review", "resolve_review_thread", "unresolve_review_thread",
    "create_session", "send_message", "reply", "forward", "create_draft", "create_file", "update_file", "share_file",
    "trash_file", "copy_file")
WRITE_TOOLS = ("Edit", "Write", "NotebookEdit")
WRITE_PATH_KEYS = ("file_path", "notebook_path")
SHELL_TOOLS = ("Bash", "Monitor")              # tools whose input.command is a shell command
PR_NUMBER_KEYS = ("pullNumber", "pull_number")
SCRATCH_DIRS = ("/tmp/", "/var/tmp/", "/dev/", "/proc/")
SCRATCH_VARS = ("TMPDIR",)                     # a path that starts with one of these variables (unexpanded) is scratch
HOME_LEAD = "~"

# -- what a call does: git
GIT_COMMAND = "git"
HELP_FLAGS = ("--help", "-h")
END_OF_OPTIONS = "--"
GIT_DIR_FLAG = "-C"
GIT_GLOBAL_WITH_VALUE = ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix",
                         "--config-env", "--attr-source")
GIT_COMMIT_VERBS = ("commit", "revert", "cherry-pick", "am")
GIT_NO_COMMIT_FLAGS = {"commit": ("--dry-run",),
                       "revert": ("--dry-run", "-n", "--no-commit", "--abort", "--quit"),
                       "cherry-pick": ("--dry-run", "-n", "--no-commit", "--abort", "--quit"),
                       "am": ("--dry-run", "--abort", "--quit")}
GIT_PUSH_VERB = "push"
GIT_PUSH_WITH_VALUE = ("--repo", "-o", "--push-option", "--receive-pack", "--exec", "--recurse-submodules")
GIT_PUSH_DRY_RUN = ("--dry-run", "-n")
GIT_PUSH_EVERYTHING = ("--all", "--mirror", "--branches")
GIT_PUSH_TAGS = ("--tags",)
GIT_PUSH_DELETE = ("--delete", "-d")
GIT_HEAD_NAMES = ("HEAD", "@")                 # a refspec side that means "the current branch"
GIT_REFSPEC_WILDCARD = "*"
GIT_BRANCH_PREFIX = "refs/heads/"
GIT_DEFAULT_REMOTE = "origin"
GIT_REMOTE_NAME = re.compile(r"^[\w.-]+$")
GIT_SWITCH_VERBS = {"checkout": ("-b", "-B"), "switch": ("-c", "-C")}    # verb -> the flags that create the branch
GIT_SWITCH_WITH_VALUE = ("-t", "--track", "--orphan", "--conflict", "--pathspec-from-file")
GIT_SWITCH_TRACK = ("-t", "--track")
GIT_SWITCH_ORPHAN = "--orphan"
GIT_SWITCH_DETACH = ("--detach", "-d")
GIT_SWITCH_PREVIOUS = "-"
GIT_SWITCH_MAY_NAME_A_PATH = ("checkout",)       # `git checkout NAME` restores a file when NAME is a path
GIT_WRITE_VERBS = ("add", "rm", "mv", "apply", "stash", "reset", "restore", "merge", "rebase", "tag", "clean")
GIT_HEAD_REF = re.compile(r"ref:\s*refs/heads/(\S+)")
GIT_REMOTE_HEAD_REF = re.compile(r"ref:\s*refs/remotes/[^/\s]+/(\S+)")
GIT_DIR_POINTER = re.compile(r"gitdir:\s*(.+)")
GIT_DIR_NAME = ".git"
GIT_HEAD_FILE = "HEAD"
GIT_COMMON_FILE = "commondir"
GIT_REMOTES_PATH = os.path.join("refs", "remotes")
GIT_SEARCH_DEPTH = 40                          # parent directories searched for the checkout's .git
GIT_FILE_MAX_BYTES = 400                       # of HEAD, a .git file, commondir: all are one short line

# -- what a call does: the GitHub command line and the API
GH_COMMAND = "gh"
GH_GLOBAL_WITH_VALUE = ("-R", "--repo", "--hostname")
GH_REPO_FLAGS = ("-R", "--repo")
GH_API_GROUP = "api"
GH_PR_GROUP = "pr"
GH_MERGE_SUB = "merge"
GH_AUTO_FLAG = "--auto"
GH_DISABLE_AUTO_FLAG = "--disable-auto"
GH_MERGE_WITH_VALUE = ("-b", "--body", "-F", "--body-file", "-t", "--subject", "-A", "--author-email", "--match-head-commit")
GH_PR_WRITE_SUBS = ("create", "edit", "close", "reopen", "ready", "update-branch")
GH_PR_OUTWARD_SUBS = ("comment", "review", "lock", "unlock")
GH_WORKFLOW_RUN = ("workflow", "run")
GH_OUTWARD_GROUPS = ("issue", "release", "repo", "workflow", "run", "label", "secret", "variable", "gist", "ruleset")
GH_READ_SUBS = ("list", "view", "status", "diff", "checks", "checkout", "clone", "download", "watch", "logs", "browse")
GH_API_WITH_VALUE = ("-X", "--method", "-H", "--header", "-f", "--raw-field", "-F", "--field", "--input", "-q", "--jq",
                     "-t", "--template", "--cache", "-p", "--preview", "--hostname")
GH_API_BODY_FLAGS = ("-f", "--raw-field", "-F", "--field")
GH_API_INPUT_FLAG = "--input"
GH_API_FILE_FIELD_FLAGS = ("-F", "--field")      # `-F key=@FILE` reads FILE; `-f` takes "@FILE" as it is
GH_PR_NUMBER = re.compile(r"^#?(\d+)$")
GH_PR_URL = re.compile(r"github\.com/([\w.-]+/[\w.-]+)/pull/(\d+)")
HTTP_COMMANDS = ("curl", "wget", "http", "https")
HTTP_URL = re.compile(r"^https?://")
HTTP_HOST = re.compile(r"^https?://([^/]+)")
HTTP_METHODS = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE")
HTTP_DEFAULT_SCHEME = "https://"
METHOD_OF_NOTHING = "GET"                      # the method of a request that names none and sends no body
METHOD_OF_BODY = "POST"
METHOD_OF_UPLOAD = "PUT"
METHOD_OF_HEAD = "HEAD"
API_METHOD_FLAGS = ("-X", "--method", "--request")
API_READ_METHODS = ("GET", "HEAD")
CURL_WITH_VALUE = ("-X", "--request", "-H", "--header", "-d", "--data", "--data-raw", "--data-binary",
                   "--data-urlencode", "--json", "-F", "--form", "-T", "--upload-file", "-o", "--output", "-u", "--user",
                   "-A", "--user-agent", "-e", "--referer", "-b", "--cookie", "-c", "--cookie-jar", "--url", "-w",
                   "--write-out", "--connect-timeout", "-m", "--max-time", "--retry", "-K", "--config", "--cacert",
                   "--method", "--body-data", "--body-file", "--post-data", "--post-file", "--header")
CURL_DATA_FLAGS = ("-d", "--data", "--data-raw", "--data-binary", "--data-urlencode", "--json", "-F", "--form",
                   "--body-data", "--body-file", "--post-data", "--post-file")
CURL_UPLOAD_FLAGS = ("-T", "--upload-file")
CURL_FILE_DATA_FLAGS = ("-d", "--data", "--data-binary")   # `-d @FILE` sends the text of FILE
BODY_FILE_STDIN = "-"                          # `@-`, `--input -`: the body comes from standard input
CURL_HEAD_FLAGS = ("-I", "--head")
CURL_URL_FLAG = "--url"
GITHUB_API_HOSTS = ("api.github.com", "uploads.github.com")
GITHUB_ENTERPRISE_API = "/api/v3/"
API_HOST_PREFIX = re.compile(r"^https?://[^/]+/")
API_V3_PREFIX = re.compile(r"^api/v3/")
API_REPO_PATH = re.compile(r"repos/([^/]+)/([^/]+)/(.*)$")
API_MERGE_PATH = re.compile(r"pulls/(\d+)/merge$")
API_MERGES_PATH = "merges"
API_REFS_PATH = re.compile(r"git/refs(?:/heads/(.+))?$")
API_CONTENTS_PREFIX = "contents/"
API_PULLS_PATH = re.compile(r"pulls(?:/\d+(?:/update-branch)?)?$")
API_BODY_BRANCH = re.compile(r"""["']?\b(?:branch|base|ref)["']?\s*[=:]\s*["']?(?:refs/heads/)?([\w./-]+)""")
API_FILE_BODY = ("@", "=@")                    # a body that starts with, or holds, one of these comes from a file
GRAPHQL_PATH = "graphql"
GRAPHQL_MERGE = re.compile(r"mergePullRequest|enablePullRequestAutoMerge|enqueuePullRequest")
GRAPHQL_REF = re.compile(r"mergeBranch|createCommitOnBranch|updateRef|createRef|deleteRef")
GRAPHQL_MUTATION = re.compile(r"\bmutation\b")

# -- what a call does: the shell
SHELLS = ("bash", "sh", "zsh", "dash", "ksh")
SHELL_COMMAND_FLAG = "c"                       # `bash -c TEXT`, also inside a cluster such as -lc
SHELL_FLAGS_WITH_VALUE = ("-o", "--rcfile", "--init-file", "-O", "+o", "+O")
SHELL_OPTION_LEADS = ("-", "+")                # B4: `bash +x FILE` runs FILE: a word that starts so is an option
SHELL_STDIN_FLAG = "s"                         # B1: `bash -s ARGS`: the program comes from standard input
SHELL_STDIN_NAMES = ("/dev/stdin", "/dev/fd/0", "/proc/self/fd/0")   # B1: the script named so is standard input
SHELL_STDIN_REDIRECT = "<"                     # B1: `bash < FILE` reads FILE as its program
SHELL_KEYWORDS = ("if", "then", "elif", "else", "fi", "do", "done", "while", "until", "!", "{", "}", "time", "esac")
SHELL_NO_COMMAND = ("for", "select", "case", "function", "[[", "[", "test", "((")
WRAPPERS_WITH_VALUE = {"sudo": ("-u", "-g", "-C", "-h", "-p", "-U", "-r", "-t"), "env": ("-u", "-C", "-S"),
                       "command": (), "builtin": (), "exec": ("-a",), "nohup": (), "time": ("-o", "-f"),
                       "nice": ("-n",), "ionice": ("-c", "-n", "-p"), "setsid": (), "stdbuf": ("-i", "-o", "-e"),
                       "unbuffer": (), "timeout": ("-s", "--signal", "-k", "--kill-after"),
                       "xargs": ("-I", "-n", "-P", "-d", "-L", "-s", "-E", "-a")}
ENV_WRAPPERS = ("env",)                        # wrappers that take NAME=value words before the command
DURATION_WRAPPERS = ("timeout",)               # wrappers whose first plain word is a duration
STDIN_ARG_WRAPPERS = ("xargs",)                # wrappers that add arguments read from standard input
ASSIGN_COMMANDS = ("export", "declare", "local", "readonly", "typeset")
EVAL_COMMANDS = ("eval",)
SOURCE_COMMANDS = ("source", ".")
SCRIPT_SUFFIX = ".sh"
SCRIPT_PATH_MARK = "/"                         # a command word that holds this names a file the command runs (D1)
SCRIPT_SHEBANG = "#!"                          # a first line that names the program that runs the file
SHEBANG_ENV = "env"                            # `#!/usr/bin/env PROGRAM`: the program is the next word
SCRIPT_BINARY_BYTE = b"\x00"                   # a file that holds this byte is a program, not a script: it is not read
SHELL_SYNTAX_FLAG = "n"                        # `bash -n FILE` (also in a cluster): syntax check only, nothing runs (D6)
PWD_VARIABLE = "PWD"                           # B2: `$PWD/x`, `${PWD}/x`, `$(pwd)/x` name x in the command's directory
PWD_COMMANDS = ("pwd", "pwd -L", "pwd -P")     # B2: a substitution of one of these is the command's directory
COPY_COMMANDS = ("cp", "mv")                   # B2: `cp A B`: B then holds the text of A
HTTP_FILE_BODY_FLAGS = ("--post-file", "--body-file")   # B3: wget sends the text of the file these name
UNRESOLVED_READINGS = ("gh", "git")            # a command word that cannot be resolved is judged as each of these (D3)
FIND_COMMANDS = ("find",)
FIND_EXEC_FLAGS = ("-exec", "-execdir", "-ok", "-okdir")   # find runs the words after one of these as a command (D4)
FIND_EXEC_ENDS = (";", "+")
TEE_COMMANDS = ("tee",)
TEE_APPEND_FLAGS = ("-a", "--append")
SHELL_APPEND_REDIRECTS = (">>", "&>>")
HTTP_OUTPUT_FLAGS = ("-o", "--output", "-O", "--output-document")   # where curl and wget write what they fetch
ECHO_ESCAPES = (("\\n", "\n"), ("\\t", "\t"))  # what printf (and echo -e) turn into a new line and a tab
ECHO_ESCAPE_FLAG = "-e"
UNKNOWN_DIR_KEY = "?"                          # the key of a file named relative to a directory the parser does not know
DIR_COMMANDS = ("cd",)
DIR_UNKNOWN_COMMANDS = ("pushd", "popd")
ECHO_COMMANDS = ("echo", "printf")
CAT_COMMANDS = ("cat",)
SHELL_WRITE_COMMANDS = ("cp", "mv", "install", "rsync", "tee", "touch", "mkdir", "rm", "rmdir", "ln", "truncate", "patch")
LAST_TARGET_COMMANDS = ("cp", "mv", "install", "rsync", "ln")      # their target is the last plain word
IN_PLACE_EDITORS = ("sed", "perl")
IN_PLACE_FLAG = re.compile(r"^(?:--in-place(?:=.*)?|-[A-Za-z]*i(?:[^A-Za-z].*)?)$")
MAX_SHELL_DEPTH = 4
SCRIPT_MAX_BYTES = 262144
SHELL_WORD_END = " \t\r\n;|&()<>"
SHELL_BLANKS = " \t\r"
SHELL_COMMAND_START = " \t\n;|&("              # a `#` or a numbered redirection after one of these starts a new word
SHELL_OPERATORS = ("&&", "||", ";;", "|&", ";", "|", "&", "(", ")")
SHELL_GROUP_OPEN = "("
SHELL_GROUP_CLOSE = ")"
SHELL_REDIRECT = re.compile(r"(\d*)(<<<|<<-|<<|<>|>>|>&|<&|>\||&>>|&>|>|<)")
SHELL_HEREDOC_OPS = ("<<", "<<-")
SHELL_HEREDOC_STRIP = "<<-"
SHELL_HERESTRING = "<<<"
SHELL_WRITE_REDIRECTS = (">", ">>", ">|", "&>", "&>>")
SHELL_PROCESS_SUBST = ("<(", ">(")
SHELL_PIPES = ("|", "|&")
SHELL_SEQUENCE = ("&&", ";", "\n")             # after one of these a `cd` holds for what follows
SHELL_AND = "&&"
SHELL_VAR = re.compile(r"\$([A-Za-z_]\w*)")
SHELL_BRACE_VAR = re.compile(r"\$\{([A-Za-z_]\w*)\}$")
SHELL_SPECIAL_VAR = re.compile(r"\$[0-9@*#?$!-]")
SHELL_ASSIGNMENT = re.compile(r"^[A-Za-z_]\w*=")
SHELL_HEREDOC_SUBST = re.compile(r"\$\(((?:[^()]|\([^()]*\))*)\)")

# -- a shell text the parser cannot read: crude screens, scanned word by word (linear in the length of the text)
FALLBACK_SPLIT = re.compile(r"[\n|;&]")        # where one command ends, crudely
FALLBACK_WORD = re.compile(r"\w+")
FALLBACK_MERGE_TEXT = re.compile(r"/pulls/\d+/merge\b|mergePullRequest|enablePullRequestAutoMerge|enqueuePullRequest|"
                                 r"merge_pull_request|enable_pr_auto_merge")
FALLBACK_MERGE_WORDS = (("gh", "pr", "merge"),)                    # the words of one command, in this order
FALLBACK_OUTWARD_WORDS = (("git", "commit"), ("git", "push"), ("gh", "pr", "create"), ("gh", "pr", "merge"),
                          ("gh", "pr", "edit"))
FALLBACK_PUSH_EVERY = ("all", "mirror", "branches")          # `git push --all` and its like: every branch
FALLBACK_PUSH_WORDS = tuple(("git", "push", b) for b in DEFAULT_BRANCHES + FALLBACK_PUSH_EVERY)    # D5
FALLBACK_MERGE_NUMBER = re.compile(r"\bmerge\s+#?(\d+)\b|/pulls/(\d+)/merge")

# -- was the act taken: a call was denied when its result row carries a denial flag, or when its result is an
# error whose text STARTS with one of these leads. What a result that is not an error says decides nothing: a
# successful commit echoes its branch, its subject and its new file paths, which the session chose.
DENIAL_FLAG = "toolDenialKind"                 # the result row's field that names why a call was denied (2.1.325)
DENIAL_WRAPPERS = ("Error: ", "<tool_use_error>")   # dropped from the front of an error text before the leads are read
DENIAL_LEADS = re.compile(
    r"(?:PreToolUse:\S*\s+hook\s+(?:error|denied|blocked)"     # a pre-tool hook's denial (observed 2026-11-16)
    r"|TURN-GATE"                                              # the merge gate's own reason, shown alone
    r"|The user doesn't want to proceed"                       # rejected at the permission prompt
    r"|Permission to use \S+"                                  # denied by a permission rule
    r"|(?:This (?:command|call|tool use) )?requires approval"  # held for an approval that did not come
    r"|Hook (?:denied|blocked))", re.I)

# -- Stop gate, advisory, state
PLAN_MARK = re.compile(r"\bGoal\b")
LEDGER_DIRNAME = "turn-gates"
LEDGER_KEY_CHARS = 20
LEDGER_FILE = "delegate-%s.jsonl"
ADVISORY_FILE = "plan-shown-%s"
SPAN_MARKS = (OUR_BLOCK_MARK, RECEIPT_BLOCK_MARK)   # the Stop hooks whose blocks `span` counts
ISO_STAMP = re.compile(r"^(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d):(\d\d)(\.\d+)?\s*(Z|z|[+-]\d\d:?\d\d)?$")
ISO_UTC = ("Z", "z")
STATE_DIR_ENV = "TURNGATE_STATE_DIR"
TMPDIR_ENV = "TMPDIR"
STATE_DIR_DEFAULT = "/tmp"
MISSING_PLAN = "plan-gate (before the first outward action)"
MISSING_VERIFY = "adversarial-verify"
MISSING_PLAN_RELOAD = "plan-gate (loaded again after the compaction, before the outward action that followed it)"
MISSING_VERIFY_RELOAD = "adversarial-verify (loaded again after the compaction)"
NOTE_BEFORE_RUN = "The miss is in the work done before the scheduled run began."
NOTE_IN_RUN = "The miss is in the scheduled run."

# -- the merge gate's words. Every denial starts with the gate's name and a code in brackets.
DENY_LEAD = "TURN-GATE (merge word) [%s]: "
REASON_NO_RECORD = ("the gate cannot read this session's record (its path is empty or missing, or the file holds no "
                    "readable row), so nothing shows the owner's word, and a merge is not let through without it. "
                    "Tell the owner; they can merge it themselves.")
REASON_BRANCH_UNKNOWN = ("this push does not name its branch, the gate cannot read the checkout it runs in, and the "
                         "owner is not present in this stretch of work. Name the branch in the command (git push "
                         "origin HEAD:BRANCH). A push to a default branch needs the owner's word.")
REASON_SCHEDULED = ("a scheduled run never merges%s and never pushes to a default branch. Record it as an open "
                    "decision in the run's report; the owner merges on their own word.")
REASON_DELEGATE = "a helper agent does not merge. Return the request to the main session."
REASON_NO_OWNER_WORD = ("the owner has said nothing since this stretch of work began (it began at a stop, a wake-up, "
                        "a restart or the start of the record), so nothing here is authorized to merge or to push to "
                        "a default branch. Ask the owner with a card (AskUserQuestion) whose merge option names the "
                        "pull request, and act only on that answer.")
REASON_TARGET_UNKNOWN = ("the gate cannot tell which pull request this call merges (%s). Use the merge tool, or name "
                         "the number in the command, so that it can be matched to the owner's word.")
REASON_MERGE_WORD = ("the owner has not ordered the merge of PR #%d in this turn. Their word is a click on a card "
                     "(AskUserQuestion) that names #%d and whose chosen option says to merge it, or a plain typed order "
                     "as the LAST sentence of their message, for example \"Merge #%d\". A wordier message (a "
                     "condition, a report, a question, more words after the order) and any message typed while you "
                     "work that is not itself such an order do not count. The word covers only the pull requests "
                     "named and ends when you stop. Ask with a card whose merge option names #%d, and merge only on "
                     "that answer.")
REASON_BARE_NUMBER = ("the owner's word for #%d names no repository, and it was already used in this turn for #%d of "
                      "another repository (%s), so it does not cover this call (%s). A word that names only a number is "
                      "good for one repository. Ask the owner with a card that names the repository (owner/repo#%d), "
                      "and merge only on that answer.")
REASON_DEFAULT_BRANCH = ("a direct push to a default branch (%s) needs the owner's word for exactly that: a card that "
                         "asks it and is answered yes, or a typed order such as \"push this to main\". A merge word "
                         "for a pull request does not cover it. Without that word, open a pull request.")
NOTE_NO_NUMBER = "it names no number"
NOTE_STDIN_NUMBER = "the number comes from standard input"
NOTE_GRAPHQL_MERGE = "a GraphQL merge mutation shows no number"
NOTE_GRAPHQL_UNREADABLE = "the GraphQL request body cannot be read"
NOTE_UNPARSED = "the command could not be parsed"
NOTE_UNKNOWN_REPOSITORY = "a repository the gate cannot read"
NOTE_BRANCH_UNKNOWN = "branch-unknown"
NOTE_TAGS = "tags only"
ALL_BRANCHES = "every branch"
SOME_BRANCH = "a branch the call does not name"

_unresolved = "\x00"     # an expansion inside a shell word that this parser cannot resolve
_varmark = "\x01"        # brackets the name of a variable inside a shell word
_ledger_block = 999      # a helper's noted act sorts after the blocks of the row it is placed at
_no_command = ":"        # stands for a redirection that has no command word


# ----------------------------------------------------------------------------------------------------------------
# 2. Loading and text helpers
# ----------------------------------------------------------------------------------------------------------------
def load(path):
    """Rows of a session record. A line that is not a JSON object becomes {"type": "BAD"}, so counts stay honest.
    Any error reading the file gives []."""
    rows = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    d = json.loads(raw)
                except Exception:
                    d = None
                rows.append(d if isinstance(d, dict) else {"type": "BAD"})
    except Exception:
        return []
    return rows


def normalize(text):
    """One normal form for every word test: NFKC, curly quotes and dashes straightened, lower case."""
    t = unicodedata.normalize("NFKC", text or "")
    for a, b in (("’", "'"), ("‘", "'"), ("ʼ", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-"), (" ", " ")):
        t = t.replace(a, b)
    return t.lower()


def _text(msg):
    """The text of a message: its string content, or its text blocks joined; None when it has none."""
    c = msg.get("content") if isinstance(msg, dict) else None
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(str(b.get("text", "")) for b in c if isinstance(b, dict) and b.get("type") == "text") or None
    return None


def _result_text(block):
    cc = block.get("content")
    if isinstance(cc, str):
        return cc
    return "\n".join(str(x.get("text", "")) for x in (cc or []) if isinstance(x, dict))


def was_denied(block, row):
    """The call did not run because it was denied: its result row carries a denial flag, or its result is an
    error whose text starts (leading blanks and one wrapper dropped) with one of DENIAL_LEADS. A result that is not
    an error is never a denial, whatever it says. One test for the Stop gate and the merge gate."""
    if row.get(DENIAL_FLAG):
        return True
    if not block.get("is_error"):
        return False
    text = _result_text(block).lstrip()
    for wrapper in DENIAL_WRAPPERS:
        if text.startswith(wrapper):
            text = text[len(wrapper):].lstrip()
            break
    return bool(DENIAL_LEADS.match(text))


def _content(row):
    m = row.get("message")
    return m.get("content") if isinstance(m, dict) else None


def harness_lead(text):
    """True when a text STARTS with a harness lead (a notification, a wake, a local-command echo, a command tag).
    A text that merely quotes one of these is the owner's."""
    return (text or "").lstrip().startswith(HARNESS_MARKERS)


def command_args(text):
    """The owner's words in a slash-command row: its arguments, or the command's name when it has none."""
    name = COMMAND_NAME.search(text or "")
    args = COMMAND_ARGS.search(text or "")
    a = args.group(1).strip() if args else ""
    return a or (name.group(1).strip() if name else "")


def _command_name(text):
    m = COMMAND_NAME.search(text or "")
    return m.group(1).strip().split()[0] if m and m.group(1).strip() else ""


# ----------------------------------------------------------------------------------------------------------------
# 3. Rows -> events
# ----------------------------------------------------------------------------------------------------------------
class Ev(object):
    """One row of the record as the gates see it. kind is one of:
    OWNER QUEUED_OWNER WAKE QUEUED_WAKE RESULT FEEDBACK INTERRUPT ECHO META SUMMARY STOP_DONE STOP_BLOCKED COMPACT
    ASSISTANT SIDECHAIN OTHER BAD"""
    __slots__ = ("i", "kind", "text", "grantable", "uses", "results", "says", "wake_kind", "scheduled")

    def __init__(self, i, kind, text="", grantable=False):
        self.i, self.kind, self.text, self.grantable = i, kind, text, grantable
        self.uses, self.results, self.says, self.wake_kind, self.scheduled = [], [], [], None, False

    def __repr__(self):
        return "Ev(%d,%s)" % (self.i, self.kind)


def _scheduled_origin(origin):
    return isinstance(origin, dict) and (origin.get("kind") in SCHEDULED_ORIGIN_KINDS
                                         or origin.get("subkind") in SCHEDULED_ORIGIN_KINDS)


def _user_kind(row, text, strict):
    """(kind, may grant) of a `user` row. COMMAND and META_COMMAND are settled by row_events, which sees the
    neighbouring rows."""
    if row.get("isSidechain") is True:
        return "SIDECHAIN", False
    if row.get("isCompactSummary"):
        return "SUMMARY", False
    c = _content(row)
    if isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
        return "RESULT", False
    s = (text or "").lstrip()
    origin = row.get("origin")
    has_origin = isinstance(origin, dict)
    owner_origin = has_origin and origin.get("kind") in OWNER_ORIGIN_KINDS
    if row.get("isMeta"):
        if s.startswith(HOOK_FEEDBACK_LEAD):
            return "FEEDBACK", False
        if s.startswith(RESTART_LEAD):
            return ("WAKE" if RESTART_ENDS_WORD else "META"), False
        if s.startswith(COMMAND_LEADS) and (owner_origin or not has_origin):
            return "META_COMMAND", False
        return ("WAKE" if has_origin else "META"), False
    if has_origin:                                  # who typed a row is in `origin`, whatever its text quotes
        return ("OWNER", True) if owner_origin else ("WAKE", False)
    if s.startswith(INTERRUPT_LEAD):
        return "INTERRUPT", False
    if s.startswith(WAKE_LEADS):
        return "WAKE", False
    if s.startswith(ECHO_LEADS):
        return "ECHO", False
    if s.startswith(COMMAND_LEADS):
        return "COMMAND", False
    media = isinstance(c, list) and any(isinstance(b, dict) and b.get("type") in OWNER_MEDIA_BLOCKS for b in c)
    if not s and not media:
        return "OTHER", False
    return "OWNER", (not strict)   # a row without `origin` grants only in a file whose rows carry none


def _queued_event(i, row, a):
    origin = a.get("origin")
    kind = origin.get("kind") if isinstance(origin, dict) else None
    p = a.get("prompt")
    text = p if isinstance(p, str) else (_text({"content": p}) or "")
    flagged = bool(a.get("isMeta") or a.get("forwardedIntent") or row.get("isMeta"))
    if text.lstrip().startswith(COMMAND_LEADS):
        text = command_args(text)
    if kind in OWNER_ORIGIN_KINDS and not flagged:
        return Ev(i, "QUEUED_OWNER", text, True)
    if origin is None and a.get("commandMode") == "prompt" and not flagged:
        return Ev(i, "QUEUED_OWNER", text, False)          # may refuse, may not grant
    ev = Ev(i, "QUEUED_WAKE", text)
    ev.scheduled = _scheduled_origin(origin)
    return ev


def row_events(rows):
    """One Ev per row, and the pairing of tool calls with their results, by id only.
    -> (events, uses, results, facts)
       uses:    tool_use id -> (row, block index, block, is a helper's)
       results: tool_use id -> (row, result block, result row)
       facts:   strict (some user row carries `origin`), bad (unreadable lines), has_stop_rows"""
    strict = any(r.get("type") == "user" and isinstance(r.get("origin"), dict) for r in rows)
    evs, uses, results = [], {}, {}
    for i, row in enumerate(rows):
        t = row.get("type")
        if t == "user":
            text = _text(row.get("message")) or ""
            kind, grantable = _user_kind(row, text, strict)
            ev = Ev(i, kind, text, grantable)
            if kind == "WAKE":                      # what woke the session: an origin kind, "restart", or "lead"
                origin = row.get("origin")
                restart = bool(row.get("isMeta")) and text.lstrip().startswith(RESTART_LEAD)
                ev.wake_kind = "restart" if restart else origin.get("kind") if isinstance(origin, dict) else "lead"
                ev.scheduled = _scheduled_origin(origin)
            if kind in ("RESULT", "SIDECHAIN"):
                c = _content(row)
                ev.results = [b for b in (c if isinstance(c, list) else [])
                              if isinstance(b, dict) and b.get("type") == "tool_result"]
        elif t == "assistant":
            side = row.get("isSidechain") is True
            ev = Ev(i, "SIDECHAIN" if side else "ASSISTANT")
            c = _content(row)
            for k, b in enumerate(c if isinstance(c, list) else []):
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and str(b.get("text") or "").strip():
                    ev.says.append(str(b["text"]))
                elif b.get("type") == "tool_use":
                    ev.uses.append(b)
                    key = b.get("id")
                    if not isinstance(key, str) or not key or key in uses:
                        key = "row:%d:%d" % (i, k)          # no id of its own: nothing can be paired with it
                    uses[key] = (i, k, b, side)
        elif t == "system":
            sub = row.get("subtype")
            if sub == "stop_hook_summary":
                ev = Ev(i, "STOP_BLOCKED" if row.get("hookErrors") else "STOP_DONE")
            elif sub == "compact_boundary":
                ev = Ev(i, "COMPACT")
            else:
                ev = Ev(i, "OTHER")
        elif t == "attachment":
            a = row.get("attachment") if isinstance(row.get("attachment"), dict) else {}
            if a.get("type") == "queued_command":
                ev = _queued_event(i, row, a)
            elif a.get("type") == "hook_blocking_error" and a.get("hookEvent") == "Stop":
                be = a.get("blockingError")
                if isinstance(be, dict):
                    be = be.get("blockingError")
                ev = Ev(i, "FEEDBACK", be if isinstance(be, str) else json.dumps(be))
            else:
                ev = Ev(i, "OTHER")
        elif t == "BAD":
            ev = Ev(i, "BAD")
        else:
            ev = Ev(i, "OTHER")
        evs.append(ev)
    # Command rows. A local command (/model) is an echo. Any other command row without `origin` is the owner's.
    # One recorded as a harness row is the owner's only where the session was idle: after a completed stop, an
    # interrupt or the start of the file, with no work and no wake row in between.
    idle = True
    for n, ev in enumerate(evs):
        if ev.kind in ("COMMAND", "META_COMMAND"):
            near = evs[max(0, n - LOCAL_COMMAND_REACH):n + LOCAL_COMMAND_REACH + 1]
            local = _command_name(ev.text) in LOCAL_COMMANDS or any(
                e is not ev and e.kind in ("ECHO", "META") and e.text.lstrip().startswith(LOCAL_ECHO_LEADS) for e in near)
            if ev.kind == "COMMAND":
                if local:
                    ev.kind = "ECHO"
                else:
                    ev.kind, ev.grantable, ev.text = "OWNER", (not strict), command_args(ev.text)
            elif idle and not local:
                ev.kind, ev.grantable, ev.text = "OWNER", False, command_args(ev.text)     # never grants
            else:
                ev.kind = "META"
        elif ev.kind == "OWNER" and ev.text.lstrip().startswith(COMMAND_LEADS):
            ev.text = command_args(ev.text)             # typed with `origin`: the owner's words are the arguments
        if ev.kind in ("STOP_DONE", "INTERRUPT"):
            idle = True
        elif ev.kind in ("ASSISTANT", "SIDECHAIN", "RESULT", "WAKE"):
            idle = False
    for ev in evs:
        for b in ev.results:
            tid = b.get("tool_use_id")
            if isinstance(tid, str) and tid in uses and tid not in results and uses[tid][0] < ev.i:
                results[tid] = (ev.i, b, rows[ev.i])
    facts = {"strict": strict, "bad": sum(1 for e in evs if e.kind == "BAD"),
             "has_stop_rows": any(e.kind in ("STOP_DONE", "STOP_BLOCKED") for e in evs)}
    return evs, uses, results, facts


def scheduled_origins(text):
    """The origins of the headers of ONE notification read, in order. A header counts only when its number is the
    next expected one and its total equals the first header's total: a line of the header form anywhere else is
    body text. (Stated limit: a body line that imitates exactly the next expected header takes its place.)"""
    out, expect, total = [], 1, None
    for m in NOTIF_HEADER.finditer(text or ""):
        i, n, origin = int(m.group(1)), int(m.group(2)), m.group(3)
        if total is None:
            if i != 1:
                continue
            total = n
        if i != expect or n != total:
            continue
        out.append(origin)
        expect += 1
    return out


# ----------------------------------------------------------------------------------------------------------------
# 4. The owner's word
# ----------------------------------------------------------------------------------------------------------------
def _ref_of(m):
    g = m.groupdict()
    if g["un"]:
        return (g["uo"] + "/" + g["ur"], int(g["un"]))
    if g["rn"]:
        return (g["ro"] + "/" + g["rr"], int(g["rn"]))
    return (None, int(g["pn"] or g["hn"]))


def pr_refs(text):
    """The pull requests a normalised text names -> set of (repository or None, number). A URL and `owner/repo#n`
    bind the repository; a list goes on with "," / "and" / "&" / "+"."""
    out = set()
    for m in PR_REF.finditer(text or ""):
        out.add(_ref_of(m))
        pos = m.end()
        while True:
            more = PR_LIST_MORE.match(text, pos)
            if not more:
                break
            out.add((None, int(more.group(1))))
            pos = more.end()
    return out


def _bare_numbers(text):
    return set((None, int(n)) for n in BARE_NUMBERS.findall(text or ""))


def _strip_affirmative(clause):
    for phrase in AFFIRMATIVE_PHRASES:              # "no objections", "why not": a "no" that refuses nothing
        clause = clause.replace(phrase, " ")
    return clause


def _is_verb(text, m):
    """The verb at group 1 of `m` is used as a verb: not "the merge", not "merge conflict"."""
    return not MERGE_NOUN_BEFORE.search(text[:m.start(1)]) and not MERGE_NOUN_AFTER.match(text[m.end(1):])


def _object_scan(rest):
    """(the pull requests an order names, where that list ends in `rest`). The list directly follows the verb
    ("merge #34 and #141"), after at most OBJECT_FILLER_MAX filler words ("merge the QA-loop PRs (#34 library,
    #141 deck)", "merge library only (#34)": a bracket that holds numbers before the first one counts); a number
    elsewhere in the clause is not on it ("merge #34 and close #35" names 34; "merge the 3 PRs" names none). With
    no number on it, the list ends where the verb does."""
    out, pos, filler, end = set(), 0, 0, 0
    while pos < len(rest):
        pos = OBJECT_GAP.match(rest, pos).end()
        m = OBJECT_PAREN.match(rest, pos)
        if m and not _bracket_label(m.group(0)):
            break                                   # "#34 (after the audit)": no label, so no plain order
        if m and out:
            pos = end = m.end()                     # "#34 (library) and #141 (deck)"
            continue
        if m and pr_refs(m.group(0)):
            out |= pr_refs(m.group(0))              # "library only (#34)"
            pos = end = m.end()
            filler = 0
            continue
        m = PR_REF.match(rest, pos)
        if m:
            out.add(_ref_of(m))
            pos, filler = m.end(), 0
            end = pos
            continue
        m = BARE_NUMBER.match(rest, pos)
        if m:
            tail = rest[m.end():].lstrip()
            word = OBJECT_TAIL.match(tail)
            if (tail == "" or tail[0] in OBJECT_NUMBER_END or OBJECT_LIST_WORD.match(tail)
                    or (word and word.group(0) in OBJECT_TAIL_WORDS)):
                out.add((None, int(m.group(1))))
                pos, filler = m.end(), 0
                end = pos
                continue
        m = OBJECT_LIST_MORE.match(rest, pos)
        if m and out:
            pos = m.end()
            continue
        m = OBJECT_WORD.match(rest, pos)
        if out or not m or m.group(0) in OBJECT_STOP_WORDS or filler >= OBJECT_FILLER_MAX:
            break
        filler += 1
        pos = m.end()
    return out, end


def _bracket_label(bracket):
    """A bracket that only labels: every word in it is a pull request reference or number, a repository name (a word
    holding "/"), one of BRACKET_LABEL_WORDS or a list mark ("(#34 library, #141 deck)", "(Recommended)")."""
    words = BRACKET_WORD.findall(BARE_NUMBERS.sub(" ", PR_REF.sub(" ", bracket.lower())))
    return all("/" in w or w.lstrip("#").isdigit() or w in BRACKET_LABEL_WORDS for w in words)


def _object_refs(rest):
    """The pull requests an order names (see _object_scan)."""
    return _object_scan(rest)[0]


def _is_statement(rest):
    """M6: the first word after the pull requests an order names is one of STATEMENT_WORDS ("merge #34 can wait",
    "merge #34 is not ready"): the clause says something about them and orders nothing."""
    m = STATEMENT_NEXT.match(rest[_object_scan(rest)[1]:])
    return bool(m and m.group(1) in STATEMENT_WORDS)


def _unnegated(pattern, clause):
    """A match of `pattern` in the clause with no negating word before it in the same clause: "there is no reason
    to hold this" negates the hold; "let's not" and "not yet" are cues of their own."""
    return any(not HALT_NEGATOR.search(clause[:m.start()]) for m in pattern.finditer(clause))


def _statement_revokes(clause, rest):
    """M6: a statement about pull requests that also refuses or holds ("Merge #34 can wait.", "Merge #34 is not
    ready.") takes them out of the grant."""
    if not (REFUSAL_CUE.search(rest) or _unnegated(HALT_CUE, rest)):
        return []
    refs = _object_refs(rest) or pr_refs(clause)
    return [("revoke", refs)] if refs else []


def _short_refusal(clause):
    """A5: a short clause that starts with a refusal ("No, wait.", "stop", "not yet", "nope"), once a leading run of
    soft words ("actually", "hmm", "on second thought") is dropped; the word limit counts what is left."""
    c = SOFT_LEADIN.sub("", clause, count=1)
    return len(c.split()) <= STANDALONE_REFUSAL_MAX_WORDS and bool(REFUSAL_START.match(c))


def _sentences(text):
    """A1: the sentences of a typed text, after `normalize`, with code fences and quoted lines dropped. A line break
    ends a sentence only when the line before it ends with one of SENTENCE_END_MARKS; otherwise the two lines are
    one sentence. Then the sentences are split as SENTENCE_SPLIT says. One pass over the text."""
    t = CODE_FENCE.sub(" ", normalize(text))
    chunks, buf = [], []
    for line in t.split("\n"):
        line = line.strip()
        if not line or line.startswith(QUOTE_LEAD):
            continue
        buf.append(line)
        if line.endswith(SENTENCE_END_MARKS):
            chunks.append(" ".join(buf))
            buf = []
    if buf:
        chunks.append(" ".join(buf))
    out = []
    for chunk in chunks:
        out += [s.strip() for s in SENTENCE_SPLIT.split(chunk) if s and s.strip()]
    return out


def _clauses_of(sentence):
    """The clauses of one sentence, each without the end marks after it. A bracket is not split ("(#34 library,
    #141 deck)")."""
    out, held = [], ""
    for clause in CLAUSE_SPLIT.split(sentence):
        piece = (held + ", " if held else "") + (clause or "").strip()
        if piece.count("(") > piece.count(")"):
            held = piece
            continue
        held = ""
        c = piece.strip().rstrip(CLAUSE_END_MARKS).strip()
        if c:
            out.append(c)
    if held.strip().rstrip(CLAUSE_END_MARKS).strip():
        out.append(held.strip().rstrip(CLAUSE_END_MARKS).strip())
    return out


def _revocations(sentences):
    """What a typed text takes out of the grant, in order: ("revoke", PRs) or ("revoke_all",). A refusal names
    what it refuses ("not #141", "leave 141 alone") or, with a merge word or as a short refusal, everything; a
    clause that holds the work back ("wait", "scratch that") does the same; a negation that comes before its verb
    ("don't, under any circumstances, merge #34") reaches it. Revoking too much costs one card."""
    ops = []
    for sentence in sentences:
        open_neg = False
        for clause in CLAUSE_SPLIT.split(sentence):
            c = _strip_affirmative((clause or "").strip())
            if not c.strip():
                continue
            halt = _unnegated(HALT_CUE, c)
            has_merge = bool(MERGE_ANY.search(c))
            cue_any = REFUSAL_CUE.search(c)
            if open_neg and has_merge:              # "don't, under any circumstances, merge #34"
                refs = pr_refs(c) | _bare_numbers(c)
                ops.append(("revoke", refs) if refs else ("revoke_all",))
                open_neg = False
                continue
            m = TYPED_ORDER.match(c)
            if m and _is_verb(c, m):
                rest = c[m.end(1):]
                if _is_statement(rest):
                    ops += _statement_revokes(c, rest)
                    continue
                cue = REFUSAL_CUE.search(rest)
                if cue:                             # "merge #34, not #141"; "merge everything except #141"
                    excluded = pr_refs(rest[cue.start():]) | _bare_numbers(rest[cue.start():])
                    if excluded:
                        ops.append(("revoke", excluded))
                    elif not _object_refs(rest[:cue.start()]):
                        ops.append(("revoke_all",))                 # "merge nothing"
                continue
            if cue_any:
                refs = pr_refs(c) | _bare_numbers(c[cue_any.end():])
                if refs:
                    ops.append(("revoke", refs))
                elif has_merge or halt or _short_refusal(c):
                    ops.append(("revoke_all",))     # "No, wait."; "Actually no."; "Better to wait for the audit."
                negator = OPEN_NEGATOR.search(c)
                if negator and not MERGE_ANY.search(c[negator.end():]):
                    open_neg = True                 # the verb it negates is still to come in this sentence
            elif halt or _short_refusal(c):         # "Scratch that."; "postpone #34"; "Nope."; "Keep #34 open."
                refs = pr_refs(c) | _bare_numbers(c)
                ops.append(("revoke", refs) if refs else ("revoke_all",))
    return ops


def _tail_only(text):
    """A3 (3): nothing but tail words (ORDER_TAIL_WORDS, the default branch as destination, a bracket) and end
    marks."""
    pos = 0
    while True:
        m = ORDER_TAIL.match(text, pos)
        if not m or m.end() == pos or ("(" in m.group(0) and not _bracket_label(m.group(0))):
            break
        pos = m.end()
    return bool(ORDER_TAIL_END.match(text, pos))


def _order_object(rest, fallback):
    """(the pull requests an order clause names, where its object ends in `rest`), the verb already read. With no
    number, an object word ("it", "both") or nothing, and then `fallback` (a card's pull requests)."""
    refs, end = _object_scan(rest)
    if refs:
        return refs, end
    obj = ORDER_OBJECT.match(rest)
    end = obj.end() if obj else 0
    if len(fallback) > 1 and not (obj and CARD_ALL_WORD.search(obj.group(0))):
        return set(), end                           # several pull requests: only "both" / "all" takes them
    return set(fallback), end


def _merge_clause(c, start, fallback):
    """A3 (3): a plain merge order clause -> the pull requests it names, or None. `start` reads the lead-in words
    and the verb (TYPED_ORDER, QUESTION_ORDER, CARD_ORDER)."""
    m = start.match(c)
    if not m or not _is_verb(c, m):
        return None
    rest = c[m.end(1):]
    refs, end = _order_object(rest, fallback)
    if not refs or not _tail_only(rest[end:]) or REFUSAL_CUE.search(rest[:end]):
        return None                                 # "merge everything except #141" orders nothing
    words = ORDER_WORD.findall(PR_REF.sub(" ", rest[:end]))
    if _object_refs(rest) and not OBJECT_PAREN.search(rest[:end]) and any(w not in ORDER_LIST_WORDS for w in words):
        return None                                 # words before a number count only before a bracket of numbers
    return refs


def _push_clause(c, start):
    """The plain push order: lead-in words and the push verb (`start`), at most OBJECT_FILLER_MAX words of object,
    the default branch as destination, then only tail words. It names no pull request."""
    m = start.match(c)
    if not m or pr_refs(c):
        return False
    pos = m.end()
    for n in range(OBJECT_FILLER_MAX + 1):
        dest = PUSH_DESTINATION.match(c, pos)
        if dest:
            return _tail_only(c[dest.end():])
        word = PUSH_OBJECT_WORD.match(c, pos)
        if not word or n == OBJECT_FILLER_MAX:
            return False
        pos = word.end()
    return False


def _refuses_others(c):
    """A3 (2, 4): the clause refuses pull requests it names ("not #141", "don't merge #26", "leave 141 alone") and
    holds no other word than REFUSAL_OTHER_WORDS -> the pull requests it names, or None."""
    c = REFUSAL_OTHER_LEAD.sub("", c, count=1)
    if not REFUSAL_START.match(c):
        return None
    refs = pr_refs(c) | _bare_numbers(c)
    rest = BARE_NUMBER.sub(" ", PR_REF.sub(" ", c))
    if not refs or any(w not in REFUSAL_OTHER_WORDS for w in REFUSAL_OTHER_WORD.findall(rest)):
        return None
    return refs


def _plain_order(sentence, fallback=(), question=False):
    """A3: the sentence is a plain order -> ("merge", PRs) or ("branch", None); else None. Its clauses, in order:
    lead-in clauses (LEADIN_CLAUSE, AFFIRMATIVE_PHRASES) or refusals of other pull requests; the order clause; then
    only further orders, lists of numbers ("34 first"), tail words, affirmative phrases or refusals of other pull
    requests. With `question` (a card's question), the lead-in words of a question ("shall I") are read and the
    end mark is not looked at; a typed sentence that ends with "?" is an order only in the polite form."""
    if not question and sentence.endswith(QUESTION_END) and not POLITE_REQUEST.match(sentence):
        return None
    merge_start, push_start = (QUESTION_ORDER, QUESTION_PUSH) if question else (TYPED_ORDER, PUSH_ORDER)
    granted, refused, branch, ordered = set(), set(), False, False
    for c in _clauses_of(sentence):
        refs = _merge_clause(c, merge_start, fallback)
        if refs:
            granted |= refs
            ordered = True
            continue
        if not refs and _push_clause(c, push_start):
            branch = ordered = True
            continue
        other = _refuses_others(c)
        if other:
            refused |= other
            continue
        if c in AFFIRMATIVE_PHRASES:
            continue
        if not ordered:
            if LEADIN_CLAUSE.match(c):
                continue
            return None
        if ORDER_LIST_CLAUSE.match(c) and (pr_refs(c) | _bare_numbers(c)) and not branch:
            granted |= pr_refs(c) | _bare_numbers(c)
            continue
        if _tail_only(c):
            continue
        return None
    if not ordered or any(_same_pr(g, r) for g in granted for r in refused):
        return None
    return ("branch", None) if branch and not granted else ("merge", granted)


def _closing(sentence):
    """A2: a sentence after the order that closes the message -> the pull requests it refuses (an empty set for
    closing words alone), or None for any other sentence."""
    if CLOSING_SENTENCE.match(sentence):
        return set()
    refused = set()
    for c in _clauses_of(sentence):
        other = _refuses_others(c)
        if other:
            refused |= other
        elif not (CLOSING_SENTENCE.match(c) or c in AFFIRMATIVE_PHRASES):
            return None
    return refused or None


def typed_ops(text, fallback=()):
    """What a text the owner typed does to the grant, as an ordered list of operations:
    ("grant", PRs)  ("revoke", PRs)  ("revoke_all",)  ("branch",).  What the text revokes comes first, sentence by
    sentence; then, only when its LAST sentence (closing sentences after it aside) is a plain order (A2, A3), what
    that order grants. A text longer than ORDER_MESSAGE_MAX_CHARS is not read at all. `fallback` = the PRs an order
    without a number takes (a card answered in free text)."""
    text = text or ""
    if len(text) > ORDER_MESSAGE_MAX_CHARS:
        return []
    sentences = _sentences(text)
    ops = _revocations(sentences)
    refused, k = set(), len(sentences) - 1
    while k >= 0:
        closing = _closing(sentences[k])
        if closing is None:
            break
        refused |= closing
        k -= 1
    order = _plain_order(sentences[k], fallback) if k >= 0 else None
    if order and order[0] == "branch":
        ops.append(("branch",))
    elif order and not any(_same_pr(g, r) for g in order[1] for r in refused):
        ops.append(("grant", order[1]))
    return ops


def card_answers(use_block, result_block, row):
    """[(question, answer, labels)] for the questions of ONE card that its own result answers. The structured
    answers of the result row when it has them; otherwise the result text, read against the card's own questions.
    An answer to a question the card did not ask is dropped."""
    if result_block.get("is_error"):
        return []
    inp = use_block.get("input")
    qs = inp.get("questions") if isinstance(inp, dict) else None
    known = {}
    for q in (qs if isinstance(qs, list) else []):
        if isinstance(q, dict):
            options = q.get("options")
            known[str(q.get("question") or "")] = [str(o.get("label") or "") for o in
                                                   (options if isinstance(options, list) else []) if isinstance(o, dict)]
    tur = row.get("toolUseResult") if isinstance(row, dict) else None
    answers = tur.get("answers") if isinstance(tur, dict) else None
    pairs = []
    if isinstance(answers, dict) and answers:
        pairs = [(str(k), ANSWER_JOIN.join(str(x) for x in v) if isinstance(v, list) else str(v))
                 for k, v in answers.items()]
    else:
        text = _result_text(result_block).lstrip()
        lead = next((x for x in ANSWER_LEADS if text.startswith(x)), None)
        if lead:
            body = text[len(lead):]
            marks = sorted((body.find(ANSWER_MARK % q), q) for q in known if body.find(ANSWER_MARK % q) >= 0)
            for n, (pos, q) in enumerate(marks):
                seg = body[pos + len(ANSWER_MARK % q):marks[n + 1][0] if n + 1 < len(marks) else len(body)]
                cut = seg.rfind(ANSWER_END)
                pairs.append((q, seg[:cut] if cut >= 0 else seg))
    return [(q, a, known[q]) for q, a in pairs if q in known]


def _split_labels(answer, labels):
    """[(text, is one of the card's labels)]: one label, several joined by "," (a label may itself hold a comma, so
    the longest is tried first), or the whole answer as free text."""
    a = answer or ""
    labels = [x for x in (labels or []) if x]
    if a in labels:
        return [(a, True)]
    out, rest = [], a
    by_length = sorted(labels, key=len, reverse=True)
    while rest:
        hit = next((x for x in by_length if rest == x or rest.startswith(x + ANSWER_JOIN)), None)
        if hit is None:
            return [(a, False)]
        out.append((hit, True))
        rest = rest[len(hit) + len(ANSWER_JOIN):].lstrip()
    return out


def _merge_question(q):
    """The question uses the verb as a verb ("Merge #34?"), not as a noun ("Audit today's merge?")."""
    return any(_is_verb(q, m) for m in MERGE_VERB.finditer(q))


def _asked(q, qrefs):
    """A5: what a yes on this question grants: its LAST sentence is a plain order question (question lead-ins such
    as "shall I", the verb, the list, only tail words) -> ("merge", PRs) | ("branch", None) | None. Sentences before
    it are context ("PR 34 is green. Merge it now?")."""
    sentences = _sentences(q) if len(q) <= ORDER_MESSAGE_MAX_CHARS else []
    return _plain_order(sentences[-1], qrefs, question=True) if sentences else None


def card_ops(question, answer, labels):
    """What one answered question of a card does to the grant (same operations as typed_ops). Only the chosen
    options are read. A chosen option grants only when it is a plain order clause ("Merge #34", "Merge both
    (Recommended)", "Yes, merge #34"); a yes only on a plain order question. An option without a number takes the
    question's pull requests when it names exactly one, or when the option says both / all. Any other option of a
    merge card takes the question's pull requests out of the grant. Text typed into the card is a typed message."""
    ops = []
    q = normalize(question)
    qrefs = pr_refs(q)
    merge_q = _merge_question(q)
    asked = _asked(q, qrefs)
    for raw, is_label in _split_labels(answer, labels):
        if not is_label:                            # free text typed into the card: read as a typed message
            got = [("revoke", set(qrefs)) if (op[0] == "revoke_all" and qrefs) else op
                   for op in typed_ops(raw, fallback=qrefs if merge_q else ())]
            if MIDTURN_MESSAGE_ENDS_WORD and not any(op[0] in GRANT_OPS for op in got):
                got.append(("revoke_all",))         # A4: typed while the assistant works, and no plain order
            ops += got
            continue
        p = RECOMMENDED.sub(" ", normalize(raw)).strip()
        refs = pr_refs(p)
        if REFUSAL_CUE.search(_strip_affirmative(p)):       # "Wait", "Not yet", "Merge neither"
            if refs or qrefs:
                ops.append(("revoke", set(refs or qrefs)))
            elif MERGE_ANY.search(p) or merge_q:
                ops.append(("revoke_all",))
            continue
        target = _merge_clause(p, CARD_ORDER, qrefs)
        yes = YES_LABEL.match(p)
        if target is None and yes and asked and asked[0] == "merge":
            found, end = _order_object(p[yes.end():], asked[1])
            if found and _tail_only(p[yes.end() + end:]):
                target = found
        if target:
            ops.append(("grant", target))
        elif not refs and not qrefs and (_push_clause(p, CARD_PUSH_ORDER) or (
                yes and asked and asked[0] == "branch" and _tail_only(p[yes.end():]))):
            ops.append(("branch",))
        elif (refs or qrefs) and merge_q:
            ops.append(("revoke", set(refs or qrefs)))      # any other option of a merge card; a yes to holding it
    return ops


# ----------------------------------------------------------------------------------------------------------------
# 5. Shell commands: a small lexer and parser. A word in command position is an act; anything else is data.
# ----------------------------------------------------------------------------------------------------------------
class ShellParseError(Exception):
    """The text is not something this parser can read. The text screens decide instead (shell_acts)."""


def _match_paren(s, i):
    depth, j, n = 0, i, len(s)
    while j < n:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "'":
            k = s.find("'", j + 1)
            if k < 0:
                raise ShellParseError("quote")
            j = k + 1
            continue
        if c == '"':
            j += 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            j += 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    raise ShellParseError("paren")


def _read_dollar(s, i):
    """An expansion at s[i] -> (end, the piece it leaves in the word, nested command texts)."""
    n = len(s)
    if s[i] == "`":
        k = i + 1
        while k < n and s[k] != "`":
            k += 2 if s[k] == "\\" else 1
        if k >= n:
            raise ShellParseError("backtick")
        return k + 1, _unresolved, [s[i + 1:k].replace("\\`", "`")]
    if s.startswith("$((", i):
        k = s.find("))", i)
        if k < 0:
            raise ShellParseError("arith")
        return k + 2, _unresolved, []
    if s.startswith("$(", i):
        k = _match_paren(s, i + 1)
        if " ".join(s[i + 2:k].split()) in PWD_COMMANDS:
            return k + 1, _varmark + PWD_VARIABLE + _varmark, [s[i + 2:k]]     # B2: `$(pwd)`, the directory
        return k + 1, _unresolved, [s[i + 2:k]]
    if s.startswith("${", i):
        k = s.find("}", i)
        if k < 0:
            raise ShellParseError("brace")
        m = SHELL_BRACE_VAR.match(s[i:k + 1])
        return k + 1, (_varmark + m.group(1) + _varmark) if m else _unresolved, []
    m = SHELL_VAR.match(s, i)
    if m:
        return m.end(), _varmark + m.group(1) + _varmark, []
    if SHELL_SPECIAL_VAR.match(s, i):
        return i + 2, _unresolved, []
    return i + 1, "$", []


def _read_word(s, i):
    """One shell word at s[i] -> (text, nested command texts, was any of it quoted, end)."""
    out, subs, quoted, n = [], [], False, len(s)
    while i < n:
        c = s[i]
        if c in SHELL_WORD_END:
            break
        if c == "\\":
            if s[i + 1:i + 2] != "\n":
                out.append(s[i + 1:i + 2])
                quoted = True
            i += 2
            continue
        if c == "'":
            k = s.find("'", i + 1)
            if k < 0:
                raise ShellParseError("unterminated '")
            out.append(s[i + 1:k])
            i, quoted = k + 1, True
            continue
        if c == '"':
            quoted, i = True, i + 1
            while True:
                if i >= n:
                    raise ShellParseError('unterminated "')
                d = s[i]
                if d == '"':
                    i += 1
                    break
                if d == "\\" and s[i + 1:i + 2] in ('"', "\\", "$", "`", "\n"):
                    if s[i + 1] != "\n":
                        out.append(s[i + 1])
                    i += 2
                    continue
                if d in "$`":
                    i, piece, sub = _read_dollar(s, i)
                    out.append(piece)
                    subs += sub
                    continue
                out.append(d)
                i += 1
            continue
        if c in "$`":
            if s.startswith("$'", i):
                k, buf = i + 2, []
                while k < n and s[k] != "'":
                    if s[k] == "\\" and k + 1 < n:
                        buf.append(s[k + 1])
                        k += 2
                    else:
                        buf.append(s[k])
                        k += 1
                if k >= n:
                    raise ShellParseError("unterminated $'")
                out.append("".join(buf))
                i, quoted = k + 1, True
                continue
            i, piece, sub = _read_dollar(s, i)
            out.append(piece)
            subs += sub
            continue
        out.append(c)
        i += 1
    return "".join(out), subs, quoted, i


def _lex(s):
    """-> tokens: ("W", text, nested, quoted) | ("OP", operator) | ("R", operator, target, nested, here-document)"""
    toks, i, n, pending = [], 0, len(s), []
    while i < n:
        c = s[i]
        if c == "\\" and s[i + 1:i + 2] == "\n":
            i += 2
            continue
        if c in SHELL_BLANKS:
            i += 1
            continue
        if c == "\n":
            toks.append(("OP", "\n"))
            i += 1
            for h in pending:                       # the bodies of the here-documents opened on this line
                body = []
                while i < n:
                    j = s.find("\n", i)
                    line = s[i:] if j < 0 else s[i:j]
                    i = n if j < 0 else j + 1
                    if (line.lstrip("\t") if h["strip"] else line) == h["delim"]:
                        break
                    body.append(line)
                h["body"] = "\n".join(body)
            pending = []
            continue
        at_start = i == 0 or s[i - 1] in SHELL_COMMAND_START
        if c == "#" and at_start:
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if s.startswith(SHELL_PROCESS_SUBST, i):
            k = _match_paren(s, i + 1)
            toks.append(("W", _unresolved, [s[i + 2:k]], False))
            i = k + 1
            continue
        m = SHELL_REDIRECT.match(s, i)
        if m and (m.group(1) == "" or at_start):
            i = m.end()
            while i < n and s[i] in SHELL_BLANKS:
                i += 1
            target, subs, quoted, i = _read_word(s, i)
            if m.group(2) in SHELL_HEREDOC_OPS:
                h = {"delim": target, "strip": m.group(2) == SHELL_HEREDOC_STRIP, "quoted": quoted, "body": ""}
                pending.append(h)
                toks.append(("R", m.group(2), target, [], h))
            else:
                toks.append(("R", m.group(2), target, subs, None))
            continue
        for op in SHELL_OPERATORS:
            if s.startswith(op, i):
                toks.append(("OP", op))
                i += len(op)
                break
        else:
            text, subs, quoted, j = _read_word(s, i)
            if j == i:
                raise ShellParseError("stuck at %d" % i)
            toks.append(("W", text, subs, quoted))
            i = j
    return toks


class Cmd(object):
    """One simple command: its words, its redirections, the operators around it, and the directory it runs in
    (None when this parser does not know it). `unparsed` holds the text of a script file that could not be read
    as shell."""
    __slots__ = ("argv", "redirs", "before", "after", "via", "heredocs", "stdin_args", "cwd", "unparsed", "known")

    def __init__(self, argv, redirs, before, after, via, cwd):
        self.argv, self.redirs, self.before, self.after, self.via, self.cwd = argv, redirs, before, after, via, cwd
        self.heredocs = [r[4] for r in redirs if r[4] is not None]
        self.stdin_args, self.unparsed, self.known = False, None, {}


def _expand(text, env):
    """Replace the variables an earlier NAME=value of the same text set; any other becomes unresolved."""
    out, parts = [], text.split(_varmark)
    for n, part in enumerate(parts):
        out.append(part if n % 2 == 0 else env.get(part, _unresolved))
    return "".join(out)


def _strip_wrappers(argv):
    """Drop sudo, env, timeout N, xargs and their like, with their own options, from the front of a command."""
    stdin_args = False
    while argv:
        base = os.path.basename(argv[0])
        if base not in WRAPPERS_WITH_VALUE:
            break
        with_value = WRAPPERS_WITH_VALUE[base]
        j = 1
        while j < len(argv):
            a = argv[j]
            if a == END_OF_OPTIONS:
                j += 1
                break
            if a in with_value:
                j += 2
            elif a.startswith("-") and len(a) > 1:
                j += 1
            elif base in ENV_WRAPPERS and SHELL_ASSIGNMENT.match(a):
                j += 1
            else:
                break
        if base in DURATION_WRAPPERS and j < len(argv):
            j += 1
        if base in STDIN_ARG_WRAPPERS:
            stdin_args = True
        argv = argv[j:]
    return argv, stdin_args


def _join_dir(base, target):
    """The directory `target` names, seen from `base`; None when it cannot be known."""
    if not target or _unresolved in target or _varmark in target or target.startswith((HOME_LEAD, "-")):
        return None
    if os.path.isabs(target):
        return os.path.normpath(target)
    return os.path.normpath(os.path.join(base, target)) if base else None


def parse_shell(text, cwd=None, depth=0, via="top", env=None, written=None):
    """Every simple command the text would run, nested ones included: substitutions, `sh -c`, `eval`, a
    here-document fed to a shell, a script file, the command `find -exec` runs. Raises ShellParseError on text
    this parser cannot read. `written` = what the text has written into files so far (D2): {file: its text, or
    None when it was written in a way this parser does not follow}; the nested texts share it."""
    if depth > MAX_SHELL_DEPTH:
        raise ShellParseError("too deep")
    env = {} if env is None else env
    written = {} if written is None else written
    seq, cur, before = [], {"w": [], "r": []}, None
    for tok in _lex(text):
        if tok[0] == "OP":
            if cur["w"] or cur["r"]:
                seq.append(("cmd", cur, before, tok[1]))
            cur, before = {"w": [], "r": []}, tok[1]
            if tok[1] in (SHELL_GROUP_OPEN, SHELL_GROUP_CLOSE):
                seq.append((tok[1],))
        elif tok[0] == "W":
            cur["w"].append(tok)
        else:
            cur["r"].append(tok)
    if cur["w"] or cur["r"]:
        seq.append(("cmd", cur, before, None))
    out, here, saved, upstream = [], cwd, [], None
    for item in seq:
        if item[0] == SHELL_GROUP_OPEN:             # a `cd` inside a subshell ends with it
            saved.append(here)
            continue
        if item[0] == SHELL_GROUP_CLOSE:
            here = saved.pop() if saved else here
            continue
        raw, before, after = item[1], item[2], item[3]
        nested = []
        for w in raw["w"]:
            nested += w[2]
        for r in raw["r"]:
            nested += r[3]
            if r[4] is not None and not r[4]["quoted"]:     # an unquoted here-document still runs its $( )
                nested += SHELL_HEREDOC_SUBST.findall(r[4]["body"])
        for sub in nested:
            out += parse_shell(sub, here, depth + 1, "subst", dict(env), written)
        words = list(raw["w"])
        while words and not words[0][3] and words[0][1] in SHELL_KEYWORDS:
            words.pop(0)
        if words and not words[0][3] and words[0][1] in SHELL_NO_COMMAND:
            upstream = None
            continue
        local = {}
        while words and not words[0][3] and SHELL_ASSIGNMENT.match(words[0][1]):
            name, value = words[0][1].split("=", 1)
            value = _expand(value, env)
            if _unresolved not in value:
                local[name] = value
            words.pop(0)
        seen = env if (PWD_VARIABLE in env or not here) else dict(env, **{PWD_VARIABLE: here})    # B2: $PWD
        argv, stdin_args = _strip_wrappers([_expand(w[1], seen) for w in words])
        if not argv:
            env.update(local)                       # NAME=value alone sets it for what follows
            if raw["r"]:
                out.append(Cmd([_no_command], raw["r"], before, after, via, here))    # a redirection alone
                out[-1].known = dict(written)
                _note_writes(out[-1], here, written)
            upstream = None
            continue
        base = os.path.basename(argv[0])
        if base in ASSIGN_COMMANDS:                 # export NAME=value
            for a in argv[1:]:
                if SHELL_ASSIGNMENT.match(a) and _unresolved not in a:
                    name, value = a.split("=", 1)
                    env[name] = value
            upstream = None
            continue
        c = Cmd(argv, raw["r"], before, after, via, here)
        c.stdin_args, c.known = stdin_args, dict(written)
        out.append(c)
        if base in DIR_COMMANDS:
            if after in SHELL_SEQUENCE:
                here = _join_dir(here, argv[1]) if len(argv) == 2 else None
        elif base in DIR_UNKNOWN_COMMANDS:
            here = None
        elif base in SHELLS:
            program, j, syntax_only = None, 1, False
            while j < len(argv):
                a = argv[j]
                short = a.startswith("-") and not a.startswith("--")
                if short and a not in SHELL_FLAGS_WITH_VALUE and SHELL_SYNTAX_FLAG in a[1:]:
                    syntax_only = True              # `bash -n FILE`: a syntax check, nothing runs (D6)
                if short and SHELL_COMMAND_FLAG in a[1:]:
                    program = argv[j + 1] if j + 1 < len(argv) else ""
                    break
                if a in SHELL_FLAGS_WITH_VALUE:
                    j += 2
                    continue
                if short and SHELL_STDIN_FLAG in a[1:]:
                    break                           # `bash -s ARGS`: the words after it are the program's arguments
                if a.startswith(SHELL_OPTION_LEADS):
                    j += 1
                    continue
                if a in SHELL_STDIN_NAMES:
                    break                           # `bash /dev/stdin < FILE`
                if not syntax_only:
                    out += _run_file(a, here, depth, env, written, text)
                program = ""
                break
            if syntax_only:
                pass
            elif program is None:                   # the shell reads its program from standard input
                for h in c.heredocs:
                    out += parse_shell(h["body"], here, depth + 1, "heredoc", dict(env), written)
                for r in raw["r"]:
                    if r[1] == SHELL_HERESTRING:
                        out += parse_shell(_expand(r[2], env).replace(_unresolved, " "), here, depth + 1,
                                           "herestring", dict(env), written)
                    elif r[1] == SHELL_STDIN_REDIRECT and r[2] and not r[2].isdigit():
                        out += _run_file(r[2], here, depth, env, written, text)      # `bash < FILE` (B1)
                if before in SHELL_PIPES and upstream is not None:
                    feeder = os.path.basename(upstream.argv[0])
                    if feeder in ECHO_COMMANDS:
                        said = " ".join(a for a in upstream.argv[1:] if not a.startswith("-"))
                        out += parse_shell(said.replace(_unresolved, " "), here, depth + 1, "pipe", dict(env), written)
                    elif feeder in CAT_COMMANDS:
                        for h in upstream.heredocs:
                            out += parse_shell(h["body"], here, depth + 1, "pipe", dict(env), written)
                        for name in [a for a in upstream.argv[1:] if not a.startswith("-")]:
                            out += _run_file(name, upstream.cwd, depth, env, written, text)   # `cat FILE | bash` (B1)
            elif program:
                out += parse_shell(program.replace(_unresolved, " "), here, depth + 1, "sh-c", dict(env), written)
        elif base in EVAL_COMMANDS:
            out += parse_shell(" ".join(argv[1:]).replace(_unresolved, " "), here, depth + 1, "eval", dict(env),
                               written)
        elif base in SOURCE_COMMANDS and len(argv) > 1:
            out += _run_file(argv[1], here, depth, env, written, text)
        elif base in FIND_COMMANDS:
            out += _find_commands(argv, here, depth, env, written)
        elif argv[0].endswith(SCRIPT_SUFFIX) or SCRIPT_PATH_MARK in argv[0]:
            out += _run_file(argv[0], here, depth, env, written, text, direct=True)
        _note_writes(c, here, written)
        upstream = c
    return out


def _with_pwd(name, cwd):
    """B2: a name that starts with `$PWD`, `${PWD}` or `$(pwd)` names a file in the command's directory."""
    lead = _varmark + PWD_VARIABLE + _varmark
    if cwd and name and name.startswith(lead):
        return cwd + name[len(lead):]
    return name


def _file_key(cwd, name):
    """How a file the text writes or runs is known: its path, or its name where the directory is not known."""
    name = _with_pwd(name, cwd)
    return _join_dir(cwd, name) or (UNKNOWN_DIR_KEY + (name or ""))


def _known_text(name, cwd, written):
    """B2: the text of a file as this point of the command text leaves it: what the text wrote into it, else the file
    on disk; None when it cannot be known."""
    key = _file_key(cwd, name)
    if key in written:
        return written[key]
    text = _file_text(name, cwd)
    return None if text == _unresolved else text


def _echo_text(argv):
    """What `echo` or `printf` writes: its words, with printf's (and echo -e's) new lines and tabs."""
    words = [a.replace(_unresolved, " ") for a in argv[1:]]
    is_echo = os.path.basename(argv[0]) == ECHO_COMMANDS[0]
    escapes = not is_echo or ECHO_ESCAPE_FLAG in words
    while is_echo and words and words[0].startswith("-") and len(words[0]) > 1:
        words = words[1:]
    text = " ".join(words)
    for a, b in (ECHO_ESCAPES if escapes else ()):
        text = text.replace(a, b)
    return text


def _note_writes(c, cwd, written):
    """D2: what one command writes into files, remembered for a later run of the same file in the same text. A
    here-document or a here-string given to `cat` or `tee`, and the words of `echo` and `printf`, are known; a
    file written any other way (another program's output, a copy, a download, an edit in place) is noted as
    unknown, and running it sends the whole command text to the text screens."""
    argv = c.argv
    base = os.path.basename(argv[0])
    given = None                                    # what the command reads on standard input, when it is known
    for r in c.redirs:
        if r[4] is not None:
            given = r[4]["body"]
        elif r[1] == SHELL_HERESTRING:
            given = r[2].replace(_unresolved, " ")
    plain = [a for a in argv[1:] if not a.startswith("-")]
    if base == _no_command:
        produced = ""                               # `> FILE` alone: an empty file
    elif base in CAT_COMMANDS and len(argv) == 1:
        produced = given
    elif base in CAT_COMMANDS and plain and len(plain) == len(argv) - 1:
        texts = [_known_text(a, cwd, written) for a in plain]      # `cat A > B` (B2)
        produced = None if any(t is None for t in texts) else "".join(texts)
    elif base in ECHO_COMMANDS:
        produced = _echo_text(argv)
    else:
        produced = None
    for r in c.redirs:
        if r[1] in SHELL_WRITE_REDIRECTS and r[2] and not r[2].isdigit():
            key = _file_key(cwd, r[2])
            if r[1] in SHELL_APPEND_REDIRECTS:
                earlier = written.get(key)
                written[key] = earlier + "\n" + produced if isinstance(earlier, str) and produced is not None else None
            else:
                written[key] = produced
    if base in TEE_COMMANDS:
        appending = any(a in TEE_APPEND_FLAGS for a in argv[1:])
        for a in plain:
            written[_file_key(cwd, a)] = None if appending else given
    elif base in COPY_COMMANDS and len(plain) == 2:              # `cp A B`, `mv A B`: B holds A's text (B2)
        target = _with_pwd(plain[1], cwd)
        folder = _join_dir(cwd, target)
        if target.endswith("/") or (folder and os.path.isdir(folder)):
            target = os.path.join(target, os.path.basename(plain[0]))
        written[_file_key(cwd, target)] = _known_text(plain[0], cwd, written)
    elif base in LAST_TARGET_COMMANDS and plain:
        written[_file_key(cwd, plain[-1])] = None
    elif base in IN_PLACE_EDITORS and any(IN_PLACE_FLAG.match(a) for a in argv[1:]):
        for a in plain[1:]:
            written[_file_key(cwd, a)] = None
    elif base in HTTP_COMMANDS:
        for v in _values(_options(argv[1:], CURL_WITH_VALUE + HTTP_OUTPUT_FLAGS)[1], HTTP_OUTPUT_FLAGS):
            written[_file_key(cwd, v)] = None


def _screened(text, cwd):
    """A stand-in command whose text goes to the text screens."""
    c = Cmd([_unresolved], [], None, None, "file", cwd)
    c.unparsed = text
    return c


def _run_file(name, cwd, depth, env, written, text, direct=False):
    """The commands of a file a command runs (`bash FILE`, `source FILE`, `./FILE`): the text this command text
    wrote into it, when it did (D2); the whole command text, for the text screens, when it wrote the file in a way
    this parser does not follow; else the file on disk (_parse_file)."""
    key = _file_key(cwd, name)
    if key in written:
        body = written[key]
        return [_screened(text, cwd)] if body is None else _parse_body(body, cwd, depth, env, written)
    return _parse_file(_with_pwd(name, cwd), cwd, depth, env, written, direct)


def _parse_body(body, cwd, depth, env, written):
    try:
        return parse_shell(body, cwd, depth + 1, "file", dict(env), written)
    except (ShellParseError, RecursionError, IndexError):
        return [_screened(body, cwd)]


def _runs_in_a_shell(body):
    """A file run directly is a shell script unless its first line names another program (`#!/usr/bin/python3`,
    `#!/usr/bin/env node`)."""
    first = body.split("\n", 1)[0]
    if not first.startswith(SCRIPT_SHEBANG):
        return True
    words = first[len(SCRIPT_SHEBANG):].split()
    program = os.path.basename(words[0]) if words else ""
    if program == SHEBANG_ENV:
        rest = [w for w in words[1:] if not w.startswith("-") and not SHELL_ASSIGNMENT.match(w)]
        program = os.path.basename(rest[0]) if rest else ""
    return not words or program in SHELLS


def _parse_file(path, cwd, depth, env, written=None, direct=False):
    """The commands of a script file a command runs. Only a regular file of bounded size is read; one that is
    missing, too large, or named relative to a directory this parser does not know contributes nothing (a stated
    limit). One that cannot be parsed is handed on as text, for the text screens. A file run directly (`./land`,
    D1) is read only when it holds no NUL byte (a program is not a script) and its first line names no program
    other than a shell: a Python or Node file run directly is not read, the same stated limit as `python3 FILE`
    (M1: its text on the screens denied honest runs of a file that only mentions the words)."""
    try:
        path = _join_dir(cwd, path)
        if not path or not os.path.isfile(path) or os.path.getsize(path) > SCRIPT_MAX_BYTES:
            return []
        with open(path, "rb") as fh:
            data = fh.read(SCRIPT_MAX_BYTES + 1)
    except Exception:
        return []
    if direct and SCRIPT_BINARY_BYTE in data:
        return []
    body = data.decode("utf-8", errors="replace")
    if direct and not _runs_in_a_shell(body):
        return []
    return _parse_body(body, cwd, depth, env, {} if written is None else written)


def _find_commands(argv, cwd, depth, env, written):
    """D4: the command `find ... -exec CMD ... ;` runs (also -execdir, -ok, -okdir; ended by `;` or `+`)."""
    out, j = [], 1
    while j < len(argv):
        if argv[j] not in FIND_EXEC_FLAGS:
            j += 1
            continue
        k = j + 1
        while k < len(argv) and argv[k] not in FIND_EXEC_ENDS:
            k += 1
        if k > j + 1:
            out += parse_shell(" ".join(shlex.quote(w) for w in argv[j + 1:k]), cwd, depth + 1, "find", dict(env),
                               written)
        j = k + 1
    return out


# ----------------------------------------------------------------------------------------------------------------
# 6. Calls -> acts
# ----------------------------------------------------------------------------------------------------------------
class Act(object):
    """One thing a call does. kind: merge | push_default | push | commit | pr_write | file_push | schedule |
    outward_other | write. `last_step` marks an act of the last step of an and-chain (Model.outward)."""
    __slots__ = ("kind", "route", "pr", "repo", "branch", "note", "last_step")

    def __init__(self, kind, route, pr=None, repo=None, branch=None, note=""):
        self.kind, self.route, self.pr, self.repo, self.branch, self.note = kind, route, pr, repo, branch, note
        self.last_step = False

    def __repr__(self):
        return "Act(%s,%s,pr=%s,repo=%s,branch=%s,%s)" % (self.kind, self.route, self.pr, self.repo, self.branch, self.note)


def _read_short(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(GIT_FILE_MAX_BYTES)
    except Exception:
        return ""


def _git_dir(folder):
    """The .git directory of the checkout that holds `folder` (a worktree's .git file is followed), or None."""
    if not folder or not os.path.isabs(folder):
        return None
    d = os.path.normpath(folder)
    for _ in range(GIT_SEARCH_DEPTH):
        g = os.path.join(d, GIT_DIR_NAME)
        if os.path.isdir(g):
            return g
        if os.path.isfile(g):
            m = GIT_DIR_POINTER.match(_read_short(g))
            return os.path.normpath(os.path.join(d, m.group(1).strip())) if m else None
        up = os.path.dirname(d)
        if up == d:
            return None
        d = up
    return None


def current_branch(folder):
    """The branch checked out in `folder`, read from the checkout's HEAD file. None when there is no checkout
    there or its HEAD names no branch. No subprocess: two small files are read."""
    g = _git_dir(folder)
    m = GIT_HEAD_REF.match(_read_short(os.path.join(g, GIT_HEAD_FILE))) if g else None
    return m.group(1) if m else None


def default_branches(folder, remote):
    """DEFAULT_BRANCHES, plus the name the checkout records as the default branch of `remote`."""
    names = list(DEFAULT_BRANCHES)
    g = _git_dir(folder)
    if g and GIT_REMOTE_NAME.match(remote or ""):
        common = _read_short(os.path.join(g, GIT_COMMON_FILE)).strip()  # a worktree keeps its refs in the main checkout
        base = os.path.normpath(os.path.join(g, common)) if common else g
        m = GIT_REMOTE_HEAD_REF.match(_read_short(os.path.join(base, GIT_REMOTES_PATH, remote, GIT_HEAD_FILE)))
        if m and m.group(1) not in names:
            names.append(m.group(1))
    return tuple(names)


def _option_at(args, j, with_value):
    """The options the word args[j] holds -> ([(option, value or True)], the index of the next unread word).
    Reads `--name=value`, `--name value`, a cluster of short options (-sX PUT) and a value attached to a short
    option (-XPUT), so that an option's value is never taken for an option or for a plain word."""
    a = args[j]
    following = args[j + 1] if j + 1 < len(args) else ""
    if a.startswith("--"):
        if "=" in a:
            return [tuple(a.split("=", 1))], j + 1
        if a in with_value:
            return [(a, following)], j + 2
        return [(a, True)], j + 1
    opts = []
    for k in range(1, len(a)):
        opt = "-" + a[k]
        if opt in with_value:                       # the rest of the cluster, or the next word, is its value
            if k + 1 < len(a):
                return opts + [(opt, a[k + 1:])], j + 1
            return opts + [(opt, following)], j + 2
        opts.append((opt, True))
    return opts, j + 1


def _options(args, with_value):
    """(plain words, [(option, value or True)]) of an argument list."""
    plain, opts, j = [], [], 0
    while j < len(args):
        a = args[j]
        if a == END_OF_OPTIONS:
            plain += args[j + 1:]
            break
        if a.startswith("-") and len(a) > 1:
            found, j = _option_at(args, j, with_value)
            opts += found
        else:
            plain.append(a)
            j += 1
    return plain, opts


def _flags(args, with_value):
    """(plain words, {option: its last value, or True}) of an argument list."""
    plain, opts = _options(args, with_value)
    return plain, dict(opts)


def _values(opts, names):
    return [v for k, v in opts if k in names and isinstance(v, str)]


def _method(opts, has_body, upload=False):
    """The HTTP method of a request: named by an option, else implied by a body."""
    named = _values(opts, API_METHOD_FLAGS)
    if named:
        return named[-1].upper()
    return METHOD_OF_UPLOAD if upload else METHOD_OF_BODY if has_body else METHOD_OF_NOTHING


def _switch_branch(verb, rest, gdir, switched, lookup):
    """Remember the branch a `git checkout` / `git switch` moves to, for a later push in the same command text.
    -> True when the command creates a branch."""
    plain, flags = _flags(rest, GIT_SWITCH_WITH_VALUE)
    orphan = flags.get(GIT_SWITCH_ORPHAN) if isinstance(flags.get(GIT_SWITCH_ORPHAN), str) else None
    creating = any(f in flags for f in GIT_SWITCH_VERBS[verb]) or orphan is not None
    if END_OF_OPTIONS in rest:
        return creating                             # `git checkout REF -- FILE` restores files
    name = orphan or (plain[0] if plain else None)
    tracked = next((flags[f] for f in GIT_SWITCH_TRACK if isinstance(flags.get(f), str)), None)
    if name is None and tracked and "/" in tracked:
        name, creating = tracked.split("/", 1)[1], True     # `git checkout -t origin/NAME` makes and enters NAME
    if name is None:
        return creating
    if name == GIT_SWITCH_PREVIOUS or _unresolved in name or any(f in flags for f in GIT_SWITCH_DETACH):
        switched[gdir] = _unresolved
    elif creating or verb not in GIT_SWITCH_MAY_NAME_A_PATH or name in DEFAULT_BRANCHES:
        switched[gdir] = name
    elif lookup and _git_dir(gdir):                 # `git checkout NAME`: a branch, unless NAME is a path there
        if not os.path.lexists(os.path.join(gdir, name)):
            switched[gdir] = name
    else:
        switched[gdir] = _unresolved                # no checkout to look at: branch or path, it cannot be told
    return creating


def _git_acts(argv, cwd, switched, lookup):
    j, gdir = 1, cwd
    while j < len(argv):
        a = argv[j]
        if a in GIT_GLOBAL_WITH_VALUE:
            if a == GIT_DIR_FLAG and j + 1 < len(argv):
                gdir = _join_dir(gdir, argv[j + 1])
            j += 2
        elif a.startswith("-"):
            j += 1
        else:
            break
    if j >= len(argv):
        return []
    verb, rest = argv[j], argv[j + 1:]
    if rest and rest[0] in HELP_FLAGS:              # `git push --help`. Anywhere else the word may be a value
        return []
    if verb in GIT_COMMIT_VERBS:
        if any(f in rest for f in GIT_NO_COMMIT_FLAGS[verb]):
            return []
        return [Act("commit", "git " + verb)]
    if verb == GIT_PUSH_VERB:
        plain, flags = _flags(rest, GIT_PUSH_WITH_VALUE)
        if any(f in flags for f in GIT_PUSH_DRY_RUN + HELP_FLAGS):
            return []
        if any(f in flags for f in GIT_PUSH_EVERYTHING):
            return [Act("push_default", "git push", branch=ALL_BRANCHES)]
        remote, specs = (plain[0] if plain else GIT_DEFAULT_REMOTE), plain[1:]
        if not specs and any(f in flags for f in GIT_PUSH_TAGS):
            return [Act("push", "git push", note=NOTE_TAGS)]
        deleting = any(f in flags for f in GIT_PUSH_DELETE)
        defaults = default_branches(gdir, remote) if lookup else DEFAULT_BRANCHES
        named, unknown = [], False
        for spec in (specs or [GIT_HEAD_NAMES[0]]):
            spec = spec.lstrip("+")
            dst = spec if deleting or ":" not in spec else spec.split(":", 1)[1]
            if dst.startswith(GIT_BRANCH_PREFIX):
                dst = dst[len(GIT_BRANCH_PREFIX):]
            if GIT_REFSPEC_WILDCARD in dst:
                return [Act("push_default", "git push", branch=ALL_BRANCHES)]
            if dst in GIT_HEAD_NAMES:               # the current branch: switched to earlier in this text, else HEAD
                dst = switched.get(gdir) or (current_branch(gdir) if lookup else None) or _unresolved
            if not dst or _unresolved in dst or _varmark in dst:
                unknown = True
            else:
                named.append(dst)
        hit = [d for d in named if d in defaults]
        if hit:
            return [Act("push_default", "git push", branch=hit[0])]
        if unknown:
            return [Act("push", "git push", note=NOTE_BRANCH_UNKNOWN)]
        return [Act("push", "git push", branch=named[0])]
    if verb in GIT_SWITCH_VERBS:
        return [Act("write", "git %s (new branch)" % verb)] if _switch_branch(verb, rest, gdir, switched, lookup) else []
    if verb in GIT_WRITE_VERBS:
        return [Act("write", "git " + verb)]
    return []


def classify_api(method, path, body):
    """A GitHub REST or GraphQL request -> acts. `path` with or without the host; `body` = the request body as
    text (fields joined by newlines; a part that comes from a file is not readable)."""
    method = (method or "GET").upper()
    p = API_V3_PREFIX.sub("", API_HOST_PREFIX.sub("", path or "").lstrip("/")).split("?")[0]
    body = body or ""
    if p == GRAPHQL_PATH or p.endswith("/" + GRAPHQL_PATH):
        if _unresolved in body or body.startswith(API_FILE_BODY[0]) or API_FILE_BODY[1] in body:
            return [Act("merge", "graphql", note=NOTE_GRAPHQL_UNREADABLE)]
        if GRAPHQL_MERGE.search(body):
            return [Act("merge", "graphql", note=NOTE_GRAPHQL_MERGE)]
        if GRAPHQL_REF.search(body):
            return [Act("push_default", "graphql", branch=SOME_BRANCH)]
        return [Act("outward_other", "graphql")] if GRAPHQL_MUTATION.search(body) else []
    m = API_REPO_PATH.match(p)
    if not m:
        return [] if method in API_READ_METHODS else [Act("outward_other", "api " + method)]
    repo, tail = m.group(1) + "/" + m.group(2), m.group(3)
    merge = API_MERGE_PATH.match(tail)
    if merge:
        return [] if method in API_READ_METHODS else [Act("merge", "api merge", pr=int(merge.group(1)), repo=repo)]
    if method in API_READ_METHODS:
        return []
    found = API_BODY_BRANCH.search(body)
    branch = found.group(1) if found else None
    if tail == API_MERGES_PATH:
        to_default = branch is None or branch in DEFAULT_BRANCHES
        return [Act("push_default" if to_default else "push", "api merges", repo=repo, branch=branch or SOME_BRANCH)]
    refs = API_REFS_PATH.match(tail)
    if refs:
        branch = refs.group(1) or branch
        to_default = branch is None or branch in DEFAULT_BRANCHES
        return [Act("push_default" if to_default else "push", "api refs", repo=repo, branch=branch or SOME_BRANCH)]
    if tail.startswith(API_CONTENTS_PREFIX):
        acts = [Act("file_push", "api contents", repo=repo, branch=branch)]
        if branch is None or branch in DEFAULT_BRANCHES:
            acts.append(Act("push_default", "api contents", repo=repo, branch=branch or SOME_BRANCH))
        return acts
    if API_PULLS_PATH.match(tail):
        return [Act("pr_write", "api pulls", repo=repo)]
    return [Act("outward_other", "api " + method, repo=repo)]


def _body_parts(values):
    """Request body values; one that is read from a file (@file, key=@file) is marked unreadable."""
    return [_unresolved if (v.startswith(API_FILE_BODY[0]) or API_FILE_BODY[1] in v) else v for v in values]


def _file_text(name, cwd, known=None):
    """The text of a file a request body is read from (E): what the command text wrote into it before (`known`,
    B3: text that cannot be followed is unreadable), else the file named relative to the command's directory, a
    regular file within SCRIPT_MAX_BYTES. Standard input, a missing file or an unknown directory -> the unreadable
    mark."""
    if name == BODY_FILE_STDIN:
        return _unresolved
    key = _file_key(cwd, name)
    if known and key in known:
        return _unresolved if known[key] is None else known[key]
    try:
        path = _join_dir(cwd, _with_pwd(name, cwd))
        if not path or not os.path.isfile(path) or os.path.getsize(path) > SCRIPT_MAX_BYTES:
            return _unresolved
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return _unresolved


def _field_value(value, cwd, known=None):
    """`gh api -F key=@FILE`: the text of FILE in place of the reference. Any other form keeps today's reading."""
    if not value.startswith(API_FILE_BODY[0]) and API_FILE_BODY[1] in value:
        key, name = value.split(API_FILE_BODY[1], 1)
        text = _file_text(name, cwd, known)
        return text if text == _unresolved else key + "=" + text
    return _body_parts([value])[0]


def _gh_acts(argv, cwd=None, known=None):
    # the words `pr merge` (or `api`), with the command line's own options before and between them skipped
    j, lead, words = 1, [], []
    while j < len(argv) and len(words) < 2 and words[:1] != [GH_API_GROUP]:
        if argv[j].startswith("-") and len(argv[j]) > 1:
            found, j = _option_at(argv, j, GH_GLOBAL_WITH_VALUE)
            lead += found
        else:
            words.append(argv[j])
            j += 1
    if not words:
        return []
    group, sub, rest = words[0], (words[1] if len(words) > 1 else None), argv[j:]
    if group == GH_API_GROUP:
        plain, opts = _options(rest, GH_API_WITH_VALUE)
        if any(k in HELP_FLAGS for k, _v in lead + opts):
            return []
        body = [_field_value(v, cwd, known) if k in GH_API_FILE_FIELD_FLAGS else _body_parts([v])[0]
                for k, v in opts if k in GH_API_BODY_FLAGS and isinstance(v, str)]
        body += [_file_text(v, cwd, known) for v in _values(opts, (GH_API_INPUT_FLAG,))]    # the body read from a file
        return classify_api(_method(opts, bool(body)), plain[0] if plain else "", "\n".join(body))
    plain, opts = _options(rest, GH_GLOBAL_WITH_VALUE + GH_MERGE_WITH_VALUE)
    flags = dict(lead + opts)
    if any(f in flags for f in HELP_FLAGS):
        return []
    repo = next((flags[f] for f in GH_REPO_FLAGS if isinstance(flags.get(f), str)), None)
    repo = repo if repo and _unresolved not in repo else None
    if group == GH_PR_GROUP:
        if sub == GH_MERGE_SUB:
            if GH_DISABLE_AUTO_FLAG in flags:
                return [Act("pr_write", "gh pr merge --disable-auto", repo=repo)]
            number = None
            if plain:
                bare, url = GH_PR_NUMBER.match(plain[0]), GH_PR_URL.search(plain[0])
                if bare:
                    number = int(bare.group(1))
                elif url:
                    repo, number = url.group(1), int(url.group(2))
            route = "gh pr merge --auto" if GH_AUTO_FLAG in flags else "gh pr merge"
            return [Act("merge", route, pr=number, repo=repo, note="" if number is not None else NOTE_NO_NUMBER)]
        if sub in GH_PR_WRITE_SUBS:
            return [Act("pr_write", "gh pr " + sub, repo=repo)]
        if sub in GH_PR_OUTWARD_SUBS:
            return [Act("outward_other", "gh pr " + sub, repo=repo)]
        return []
    if (group, sub) == GH_WORKFLOW_RUN:
        return [Act("pr_write", "gh workflow run", repo=repo)]
    if group in GH_OUTWARD_GROUPS and sub and sub not in GH_READ_SUBS:
        return [Act("outward_other", "gh %s %s" % (group, sub), repo=repo)]
    return []


def _http_acts(argv, cwd=None, known=None):
    """curl, wget and their like, when they speak to the GitHub API. `-d @FILE` (curl) and `--post-file FILE`
    (wget) send the text of FILE."""
    plain, opts = _options(argv[1:], CURL_WITH_VALUE)
    flags = dict(opts)
    body = [_file_text(v[1:], cwd, known) if (k in CURL_FILE_DATA_FLAGS and v.startswith(API_FILE_BODY[0]))
            else _file_text(v, cwd, known) if k in HTTP_FILE_BODY_FLAGS
            else _body_parts([v])[0] for k, v in opts if k in CURL_DATA_FLAGS and isinstance(v, str)]
    if plain and plain[0] in HTTP_METHODS:          # `http PUT url`
        method = plain[0]
    elif _values(opts, API_METHOD_FLAGS):
        method = _method(opts, False)
    elif any(f in flags for f in CURL_HEAD_FLAGS):
        method = METHOD_OF_HEAD
    else:
        method = _method(opts, bool(body), any(f in flags for f in CURL_UPLOAD_FLAGS))
    out = []
    for a in plain + _values(opts, (CURL_URL_FLAG,)):
        url = a if HTTP_URL.match(a) else (HTTP_DEFAULT_SCHEME + a)     # curl accepts a URL without its scheme
        host = HTTP_HOST.match(url)
        host = host.group(1).rsplit("@", 1)[-1].split(":")[0].lower() if host else ""
        if host in GITHUB_API_HOSTS or (HTTP_URL.match(a) and GITHUB_ENTERPRISE_API in a):
            out += classify_api(method, url, "\n".join(body))
    return out


def _is_scratch(path, cwd):
    """The path, made absolute and normalised, lies under a scratch directory (/tmp/../home/x does not). A path
    that starts with $TMPDIR or ${TMPDIR} (SCRATCH_VARS, as a redirection keeps it) and holds no other expansion
    lies under it unless `..` climbs out ($TMPDIR/../home/x does not)."""
    for name in SCRATCH_VARS:
        lead = _varmark + name + _varmark
        rest = path[len(lead):] if path and path.startswith(lead) else None
        if rest is not None and (rest == "" or rest.startswith("/")):
            if _unresolved in rest or _varmark in rest:
                return False
            root = "/" + _unresolved
            p = os.path.normpath(root + rest)
            return p == root or p.startswith(root + "/")
    if not path or _unresolved in path or _varmark in path or path.startswith(HOME_LEAD):
        return False
    if not os.path.isabs(path):
        if not cwd:
            return False
        path = os.path.join(cwd, path)
    p = os.path.normpath(path) + "/"
    dirs = list(SCRATCH_DIRS)
    tmp = os.path.normpath(os.environ.get(TMPDIR_ENV) or "")
    if os.path.isabs(tmp) and tmp != "/":
        dirs.append(tmp + "/")
    return p.startswith(tuple(dirs))


def _screen(text, pattern, word_lists):
    """A crude look at a text that could not be parsed: the pattern anywhere, or the words of one list in order
    inside one command. One pass over the words, so a long line costs no more than its length."""
    if pattern is not None and pattern.search(text):
        return True
    for segment in FALLBACK_SPLIT.split(text):
        words = FALLBACK_WORD.findall(segment)
        for wanted in word_lists:
            at = -1
            try:
                for w in wanted:
                    at = words.index(w, at + 1)
            except ValueError:
                continue
            return True
    return False


def _fallback_acts(text):
    acts = []
    if _screen(text, FALLBACK_MERGE_TEXT, FALLBACK_MERGE_WORDS):
        m = FALLBACK_MERGE_NUMBER.search(text)
        acts.append(Act("merge", "unparsed", pr=int(m.group(1) or m.group(2)) if m else None, note=NOTE_UNPARSED))
    if _screen(text, None, FALLBACK_PUSH_WORDS):         # a push to a default branch or of every branch (D5)
        acts.append(Act("push_default", "unparsed", branch=SOME_BRANCH, note=NOTE_UNPARSED))
    if _screen(text, None, FALLBACK_OUTWARD_WORDS):
        acts.append(Act("commit", "unparsed", note=NOTE_UNPARSED))
    return acts


def _command_acts(c, switched, lookup):
    if c.unparsed is not None:
        return _fallback_acts(c.unparsed)
    argv = c.argv
    base, mine = os.path.basename(argv[0]), []
    if _unresolved in argv[0] or _varmark in argv[0]:
        for name in UNRESOLVED_READINGS:            # `$(which gh) pr merge 40`: judged as each program (D3)
            read = [name] + argv[1:]
            acts = _gh_acts(read, c.cwd, c.known) if name == GH_COMMAND else _git_acts(read, c.cwd, dict(switched), lookup)
            mine += [a for a in acts if a.kind in MERGE_GATED_KINDS]
    elif base == GIT_COMMAND:
        mine = _git_acts(argv, c.cwd, switched, lookup)
    elif base == GH_COMMAND:
        mine = _gh_acts(argv, c.cwd, c.known)
        if c.stdin_args:
            for a in mine:
                if a.kind == "merge" and a.pr is None:
                    a.note = NOTE_STDIN_NUMBER
    elif base in HTTP_COMMANDS:
        mine = _http_acts(argv, c.cwd, c.known)
    elif base in IN_PLACE_EDITORS and any(IN_PLACE_FLAG.match(a) for a in argv[1:]):
        files = [a for a in argv[1:] if not a.startswith("-")][1:]
        if not files or not all(_is_scratch(f, c.cwd) for f in files):
            mine = [Act("write", base + " in place")]
    elif base in SHELL_WRITE_COMMANDS:
        targets = [a for a in argv[1:] if not a.startswith("-")]
        targets = targets[-1:] if base in LAST_TARGET_COMMANDS else targets
        if targets and not all(_is_scratch(t, c.cwd) for t in targets):
            mine = [Act("write", base)]
    for r in c.redirs:
        if r[1] in SHELL_WRITE_REDIRECTS and r[2] and not r[2].isdigit() and not _is_scratch(r[2], c.cwd):
            mine.append(Act("write", "redirect"))
    return mine


def shell_acts(command, cwd=None, lookup=True):
    """(acts, parsed_ok) of one shell command text. `lookup` = read the checkout for the branch of a bare push."""
    text = command or ""
    try:
        cmds = parse_shell(text, cwd)
    except (ShellParseError, RecursionError, IndexError):
        return _fallback_acts(text), False
    acts, top, switched = [], [], {}
    for c in cmds:
        mine = _command_acts(c, switched, lookup)
        acts += mine
        if c.via == "top":
            top.append((c, mine))
    # When the whole text is one and-chain and it failed, its last step did not succeed (Model.outward).
    if top and len(top) == len(cmds) and all(c.before in (None, SHELL_AND) for c, _mine in top):
        for a in top[-1][1]:
            a.last_step = True
    return acts, True


def _leaf(name):
    return name.split(MCP_SEPARATOR)[-1] if name.startswith(MCP_PREFIX) else None


def classify_call(tool_name, tool_input, cwd=None, lookup=True):
    """What one tool call does -> (acts, parsed_ok). parsed_ok is False only for a shell text that had to be
    screened as text."""
    name = str(tool_name or "")
    inp = tool_input if isinstance(tool_input, dict) else {}
    leaf = _leaf(name)
    if name in SHELL_TOOLS:
        return shell_acts(str(inp.get("command") or ""), cwd if isinstance(cwd, str) else None, lookup)
    if name in WRITE_TOOLS:
        path = next((str(inp[k]) for k in WRITE_PATH_KEYS if inp.get(k)), "")
        return ([] if _is_scratch(path, cwd if isinstance(cwd, str) else None) else [Act("write", name)]), True
    if name in SCHEDULE_TOOLS or leaf in SCHEDULE_LEAVES:
        return [Act("schedule", name)], True
    repo = "%s/%s" % (inp.get("owner"), inp.get("repo")) if inp.get("owner") and inp.get("repo") else None
    if leaf in MERGE_TOOL_LEAVES:
        number = next((inp[k] for k in PR_NUMBER_KEYS if inp.get(k) is not None), None)
        try:
            number = int(number)
        except Exception:
            number = None
        return [Act("merge", leaf, pr=number, repo=repo, note="" if number is not None else NOTE_NO_NUMBER)], True
    if leaf in FILE_PUSH_LEAVES:
        branch = inp.get("branch") if isinstance(inp.get("branch"), str) else None
        if branch and branch.startswith(GIT_BRANCH_PREFIX):
            branch = branch[len(GIT_BRANCH_PREFIX):]
        acts = [Act("file_push", leaf, repo=repo, branch=branch)]
        if not branch or branch in DEFAULT_BRANCHES:
            acts.append(Act("push_default", leaf, repo=repo, branch=branch or SOME_BRANCH))
        return acts, True
    if leaf in PR_WRITE_LEAVES:
        return [Act("pr_write", leaf, repo=repo)], True
    if leaf in OTHER_OUTWARD_LEAVES:
        return [Act("outward_other", leaf, repo=repo)], True
    return [], True


def looks_like_merge(tool_name, tool_input):
    """The crude test of the error paths: could this call be a merge route?"""
    name = str(tool_name or "")
    if _leaf(name) in MERGE_TOOL_LEAVES:
        return True
    command = str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""
    return bool(name in SHELL_TOOLS and _screen(command, FALLBACK_MERGE_TEXT, FALLBACK_MERGE_WORDS))


# ----------------------------------------------------------------------------------------------------------------
# 7. The model: the window of the merge word, the governance turn, the stretch one Stop judges
# ----------------------------------------------------------------------------------------------------------------
def _last_before(ordered, row):
    """The largest member of an ascending list that is smaller than `row`, or -1."""
    n = bisect.bisect_left(ordered, row)
    return ordered[n - 1] if n else -1


def _epoch(stamp):
    """A row's `timestamp` (ISO 8601) as seconds since the epoch, or None."""
    m = ISO_STAMP.match(stamp) if isinstance(stamp, str) else None
    if not m:
        return None
    seconds = calendar.timegm(tuple(int(m.group(n)) for n in range(1, 7)))
    if m.group(8) and m.group(8) not in ISO_UTC:
        sign = -1 if m.group(8)[0] == "-" else 1
        digits = m.group(8)[1:].replace(":", "")
        seconds -= sign * (int(digits[:2]) * 3600 + int(digits[2:4] or 0) * 60)
    return seconds + float(m.group(7) or 0)


def skill_name(block):
    """The skill a Skill call loads: the name after any `scope:` prefix. None for another tool."""
    if block.get("name") != SKILL_TOOL:
        return None
    inp = block.get("input")
    return str((inp.get("skill") if isinstance(inp, dict) else "") or "").split(":")[-1].strip()


def _marked(text, mark):
    return True if mark is None else mark(text) if callable(mark) else mark in text


class Model(object):
    """What a session record shows, computed once from its rows.

    evs, uses, results, facts   the events of row_events
    owner_rows, last_owner      rows the owner typed while the assistant was idle
    stops_done                  completed stops (a stop row with hook errors is a blocked stop: no boundary)
    sched_reads                 rows where a scheduled delivery arrived
    run_starts                  rows where a scheduled run starts (a delivery read mid-turn starts none)
    auth_start, window          where the window of the merge word starts; "owner", "scheduled" or "unattended"
    turn_marks                  [(row, kind)]: every start of a governance turn, in order
    gov_start, gov_kind         the latest of them: "owner", "scheduled" or "none" (governor loads count from here)
    stretch_start               the owner's latest message or the latest completed stop, whichever is later
    """

    def __init__(self, rows):
        self.rows = rows
        self.evs, self.uses, self.results, self.facts = row_events(rows)
        evs = self.evs
        self.dropped = {"denied": 0, "error": 0, "failed_last": 0}
        self.f1_note = ""
        self._call_of = dict((id(v[1]), tid) for tid, v in self.results.items())    # result block -> its call's id
        self._loads = sorted(self._governor_loads())
        self._says = [(e.i, t) for e in evs if e.kind == "ASSISTANT" for t in e.says]

        def rows_of(*kinds):
            return [e.i for e in evs if e.kind in kinds]
        self.owner_rows = rows_of("OWNER")
        self.last_owner = self.owner_rows[-1] if self.owner_rows else -1
        self.stops_done = rows_of("STOP_DONE")
        # rows only an idle session receives (the restart notice is not one: the turn may go on after it)
        self.idle_wakes = [e.i for e in evs if e.kind == "WAKE" and e.wake_kind not in ("lead", "restart")]
        self._turn_starts = [e.i for e in evs if e.kind == "OWNER" or (e.kind == "WAKE" and e.wake_kind != "restart")]
        self.sched_reads = self._scheduled_deliveries()
        self.run_starts = []
        for r in self.sched_reads:
            if not self.midturn(r):
                wake = _last_before(self._turn_starts, r)
                announced = evs[r].kind != "WAKE" and wake >= 0 and evs[wake].kind == "WAKE"
                self.run_starts.append(wake if announced else r)
        self.run_starts = sorted(set(self.run_starts))
        # -- governance turn
        marks = [(r, "owner") for r in self.owner_rows] + [(r, "scheduled") for r in self.run_starts]
        if not WAKE_TURN_INHERITS_LOADS:            # the other policy: work woken after a stop is a turn of its own
            marks += [(e.i, "wake") for e in evs if e.kind == "WAKE" and e.wake_kind != "restart"
                      and e.i not in self.run_starts
                      and _last_before(self.stops_done, e.i) > _last_before(self.owner_rows, e.i)]
        self.turn_marks = sorted(marks)
        self.gov_start, self.gov_kind = self.turn_marks[-1] if self.turn_marks else (-1, "none")
        # -- stretch
        self.stretch_start = max(self.last_owner, self.stops_done[-1] if self.stops_done else -1)
        # -- window of the merge word
        bounds = rows_of("OWNER", "WAKE", "STOP_DONE", "INTERRUPT") + (self.sched_reads if SCHEDULED_READ_ENDS_WORD else [])
        self.auth_start = max(bounds) if bounds else -1
        if any(r >= self.auth_start and not self.midturn(r) for r in self.sched_reads):
            self.window = "scheduled"
        elif self.auth_start >= 0 and (evs[self.auth_start].kind == "OWNER" or self.auth_start in self.sched_reads):
            self.window = "owner"                   # an owner turn (a delivery read in the middle of it included)
        else:
            self.window = "unattended"

    def _governor_loads(self):
        out = []
        for tid, (i, k, b, side) in self.uses.items():
            if side or b.get("name") != SKILL_TOOL:
                continue
            name = skill_name(b)
            if name not in GOVERNORS:
                continue
            res = self.results.get(tid)
            if res is not None and res[1].get("is_error"):
                continue                            # the call failed: nothing was loaded
            out.append((i, k, name))
        return out

    def _scheduled_deliveries(self):
        """Rows where a scheduled delivery arrived: a notification read (the result of its own ReadNotifications
        call, or a result whose call row is no longer in the file and whose text starts with the notification
        lead) that holds a counted header of a scheduled origin; or a row whose `origin` says so."""
        found = set()
        for e in self.evs:
            if e.scheduled:
                found.add(e.i)
            if e.kind != "RESULT":
                continue
            for b in e.results:
                if b.get("is_error"):
                    continue
                tid = self._call_of.get(id(b))
                if tid is not None:
                    use = self.uses[tid]
                    genuine = not use[3] and use[2].get("name") in NOTIF_READ_TOOLS
                else:
                    genuine = (b.get("tool_use_id") not in self.uses
                               and _result_text(b).lstrip().startswith(NOTIF_RESULT_LEAD))
                if genuine and any(o.startswith(SCHEDULED_ORIGIN_PREFIX) for o in scheduled_origins(_result_text(b))):
                    found.add(e.i)
        return sorted(found)

    def midturn(self, row):
        """The delivery at `row` was read in the middle of an owner turn: the latest owner or wake row before it
        is the owner's and no completed stop lies between. Knowable only in a file whose rows carry `origin` or
        that has stop rows; anywhere else the answer is no."""
        if self.evs[row].kind == "WAKE":
            return False
        start = _last_before(self._turn_starts, row)
        if start < 0 or self.evs[start].kind != "OWNER" or _last_before(self.stops_done, row) > start:
            return False
        return bool(self.facts["strict"] or self.facts["has_stop_rows"])

    def authorization(self):
        """The owner's word in the window, folded in order.
        -> {"prs": set of (repository or None, number), "default_branch", "scheduled", "attended", "log"}"""
        prs, branch, log = set(), False, []
        scheduled = self.window == "scheduled"
        for ev in self.evs[max(self.auth_start, 0):]:
            ops, may_grant = None, True
            if ev.kind == "OWNER" and ev.i == self.auth_start:
                ops, may_grant = typed_ops(ev.text), ev.grantable
            elif ev.kind == "QUEUED_OWNER" and ev.i > self.auth_start:
                ops, may_grant = typed_ops(ev.text), ev.grantable
                if MIDTURN_MESSAGE_ENDS_WORD and not (may_grant and any(op[0] in GRANT_OPS for op in ops)):
                    ops = [("revoke_all",)]         # D4: typed while the assistant works, and no plain order (A4)
                if ev.grantable and QUEUED_OWNER_ATTENDS_RUN:
                    scheduled = False               # the owner is here: the rest of the run is attended
            elif ev.kind == "RESULT" and ev.i > self.auth_start:
                # A card answer is the result of its own call, paired by id. The owner's word is the click, so
                # what counts is where the answer sits: a card asked before a restart notice and answered after it
                # is answered in this window.
                for b in ev.results:
                    use = self.uses.get(self._call_of.get(id(b)))
                    if not use or use[3] or use[2].get("name") != CARD_TOOL:
                        continue
                    for question, answer, labels in card_answers(use[2], b, self.rows[ev.i]):
                        ops = (ops or []) + card_ops(question, answer, labels)
                may_grant = not scheduled           # a card answered inside a scheduled run grants nothing
            if ops is None:
                continue
            for op in ops:
                if op[0] == "revoke_all":
                    prs, branch = set(), False
                elif op[0] == "revoke":
                    prs = set(g for g in prs if not any(_same_pr(g, x) for x in op[1]))
                elif op[0] == "grant" and may_grant:
                    prs |= set(op[1])
                elif op[0] == "branch" and may_grant:
                    branch = True
            log.append((ev.i, ev.kind, [op[0] for op in ops]))
        return {"prs": prs, "default_branch": branch, "scheduled": scheduled,
                "attended": bool(log) and not scheduled, "log": log}

    def merges_made(self, number, skip=None):
        """The repositories (None where the call does not say) of every merge of pull request `number` called in
        the window of the word that the record does not show denied or failed; the call `skip` (the one being
        judged) is left out. A result flagged as an error ends a call of a tool; for a shell command it ends only
        the last step of an and-chain (as in `outward`)."""
        out = []
        for tid, (i, _k, b, _side) in self.uses.items():
            if i <= self.auth_start or (skip is not None and tid == skip):
                continue
            acts, _ok = classify_call(b.get("name"), b.get("input"), self.rows[i].get("cwd"), lookup=False)
            acts = [a for a in acts if a.kind == "merge" and a.pr == number]
            res = self.results.get(tid)
            if acts and res is not None:
                block, row = res[1], res[2]
                if was_denied(block, row):
                    continue
                if block.get("is_error"):
                    if b.get("name") not in SHELL_TOOLS:
                        continue
                    acts = [x for x in acts if not x.last_step]
            out += [a.repo for a in acts]
        return out

    def loads(self, after, before=None):
        """[(row, block index, governor)] of every governor load after row `after` (and before row `before`).
        A Skill call whose result is an error loaded nothing."""
        return [x for x in self._loads if x[0] > after and (before is None or x[0] < before)]

    def tools_ran(self, after):
        """How many tool calls other than Skill the main thread made after row `after`."""
        return sum(1 for (i, _k, b, side) in self.uses.values() if i > after and not side and b.get("name") != SKILL_TOOL)

    def outward(self, after, ledger=()):
        """[(row, block index, act)] of the counted acts after row `after` that the record does not show failed,
        a helper's rows and a helper's noted calls included. Sets `dropped` (what was left out, and why)."""
        out = []
        self.dropped = {"denied": 0, "error": 0, "failed_last": 0}
        for tid, (i, k, b, _side) in self.uses.items():
            if i <= after:
                continue
            acts, _ok = classify_call(b.get("name"), b.get("input"), self.rows[i].get("cwd"), lookup=False)
            acts = [a for a in acts if a.kind in F1_COUNTED_KINDS]
            if not acts:
                continue
            res = self.results.get(tid)
            if res is not None:                     # a call with no result yet counts
                block, row = res[1], res[2]
                denied = was_denied(block, row)
                if denied or (block.get("is_error") and b.get("name") not in SHELL_TOOLS):
                    self.dropped["denied" if denied else "error"] += 1
                    continue
                if block.get("is_error"):           # the and-chain failed: its last step did not succeed
                    self.dropped["failed_last"] += sum(1 for a in acts if a.last_step)
                    acts = [a for a in acts if not a.last_step]
            out += [(i, k, a) for a in acts]
        # The stretch's own first row (the owner's message or the stop it starts at; the file's first row when it
        # starts at the top): a note stamped after it and before the next row belongs to this stretch. A stretch
        # that starts at the owner's message also takes the notes stamped while the session was idle before it,
        # after the last completed stop (C2): no other stretch counts them, and none counts a note twice.
        low = after
        if after >= 0 and self.evs[after].kind == "OWNER" and _last_before(self.stops_done, after) >= 0:
            low = _last_before(self.stops_done, after)
        first = self.rows[max(low, 0)] if self.rows else {}
        since = _epoch(first.get("timestamp"))
        helpers = [i for (i, _k, b, side) in self.uses.values() if not side and b.get("name") in HELPER_TOOLS]
        for note in ledger:                         # a helper's outward calls, noted by the pre-tool hook
            try:
                rows_then = int(note.get("rows"))
                noted_at = note.get("t")
                if since is not None and isinstance(noted_at, (int, float)) and not isinstance(noted_at, bool):
                    counted = float(noted_at) > since        # placed by time: row numbers restart when the file is rewritten
                else:
                    counted = rows_then > low
                at = max(rows_then - 1, after + 1)
                if counted and not HELPER_ACT_PLACED_BY_TIME:
                    counted = any(after < i <= at for i in helpers)     # only a helper this stretch started
                if counted:
                    out += [(at, _ledger_block, Act(kind, "helper: " + str(note.get("tool"))))
                            for kind in note.get("kinds") or [] if kind in F1_COUNTED_KINDS]
            except Exception:
                continue
        return sorted(out, key=lambda x: (x[0], x[1]))

    def feedback(self, after, mark=None, retry=False):
        """Rows after `after` where a Stop hook's block was fed back and answered; with `mark` (a text, or a test
        of the reason) only the blocks whose reason satisfies it. A block is answered when work follows it in the
        record, or, whenever `retry` (the Stop input's stop_hook_active) is set, in any case (C1): the session went
        on after each block of the stretch, or it would not be stopping again, and its replies may never reach the
        record (an empty reply, a record that is behind). A block leaves two rows side by side (the feedback row
        and the attachment): neighbouring feedback rows are one block."""
        last_work = max([e.i for e in self.evs if e.kind == "ASSISTANT"] or [-1])
        blocks, run = [], None
        for e in self.evs:
            if e.kind == "FEEDBACK":
                if run is None:
                    run = []
                    blocks.append(run)
                run.append(e)
            elif e.kind != "OTHER":
                run = None
        return [b[0].i for b in blocks if b[0].i > after
                and (b[-1].i < last_work or retry)
                and any(_marked(e.text, mark) for e in b)]

    def prose(self, after, last_message=None):
        """What the assistant said after row `after`, plus `last_message` (the final answer the program hands a
        Stop hook) when the record does not hold it: the record does not keep every message."""
        said = [t for i, t in self._says if i > after]
        last = last_message.strip() if isinstance(last_message, str) else ""
        if last and not any(last in s for s in said):
            said.append(last_message)
        return said

    def owner_prompts(self):
        """The texts the prompt-class rule classifies: the typed message (or the slash command's arguments) that
        starts the governance turn, and every message the owner sent while the assistant worked."""
        if self.gov_kind != "owner":
            return []
        out = [self.evs[self.gov_start].text]
        for e in self.evs[self.gov_start + 1:]:
            if e.kind == "QUEUED_OWNER":
                out.append(e.text)
            elif CLASSIFY_CARD_ANSWERS and e.kind == "RESULT":
                for b in e.results:
                    use = self.uses.get(self._call_of.get(id(b)))
                    if use and not use[3] and use[2].get("name") == CARD_TOOL:
                        out += [RECOMMENDED.sub(" ", normalize(a)) for _q, a, _labels in card_answers(use[2], b, self.rows[e.i])]
        return out


def _same_pr(grant, call):
    """The granted PR covers the called one: the same number, and the same repository when both name one."""
    return grant[1] == call[1] and (grant[0] is None or call[0] is None or grant[0].lower() == call[0].lower())


# ----------------------------------------------------------------------------------------------------------------
# 8. Decisions
# ----------------------------------------------------------------------------------------------------------------
def _deny(code, text):
    return False, code, (DENY_LEAD % code) + text


def _same_repository(a, b):
    """Two calls name the same repository: both name one, and it is the same (owner/name, any case)."""
    return a is not None and b is not None and a.lower() == b.lower()


def merge_decision(model, acts, agent_id=None, call_id=None):
    """The merge gate, one row of its table after the other -> (allow, code, reason).
    codes: ok, no-record, branch-unknown, scheduled, delegate, no-owner-word, target-unknown, merge-word,
    default-branch. `model` is None when there is no record to read. `call_id` = the id of the call judged, which
    the record may already hold (it is not counted as an earlier merge)."""
    gated = [a for a in acts if a.kind in MERGE_GATED_KINDS]
    unresolved = [a for a in acts if a.kind == "push" and a.note == NOTE_BRANCH_UNKNOWN]
    if not gated and not unresolved:
        return True, "ok", ""
    readable = model is not None and any(e.kind != "BAD" for e in model.evs)
    if gated and not readable:
        return _deny("no-record", REASON_NO_RECORD)
    word = model.authorization() if readable else {"prs": set(), "default_branch": False, "scheduled": False,
                                                   "attended": False, "log": []}
    if unresolved and (PUSH_UNKNOWN_BRANCH_POLICY == POLICY_DENY
                       or (PUSH_UNKNOWN_BRANCH_POLICY == POLICY_DENY_UNATTENDED and not word["attended"])):
        return _deny("branch-unknown", REASON_BRANCH_UNKNOWN)
    if not gated:
        return True, "ok", ""
    if word["scheduled"]:
        named = [a for a in gated if a.kind == "merge" and a.pr is not None]
        return _deny("scheduled", REASON_SCHEDULED % (" PR #%d" % named[0].pr if named else ""))
    if agent_id and not DELEGATE_MAY_MERGE:
        return _deny("delegate", REASON_DELEGATE)
    if not word["log"]:
        return _deny("no-owner-word", REASON_NO_OWNER_WORD)
    for a in gated:
        if a.kind == "merge":
            if a.pr is None:
                return _deny("target-unknown", REASON_TARGET_UNKNOWN % (a.note or a.route))
            covering = [g for g in word["prs"] if _same_pr(g, (a.repo, a.pr))]
            if not covering:
                return _deny("merge-word", REASON_MERGE_WORD % (a.pr, a.pr, a.pr, a.pr))
            if BARE_NUMBER_ONE_REPOSITORY and all(g[0] is None for g in covering):
                other = [r for r in model.merges_made(a.pr, call_id) if not _same_repository(r, a.repo)]
                if other:                           # the word for a bare #n was used in another repository (AM-7)
                    return _deny("merge-word", REASON_BARE_NUMBER % (a.pr, a.pr, other[0] or NOTE_UNKNOWN_REPOSITORY,
                                                                     a.repo or NOTE_UNKNOWN_REPOSITORY, a.pr))
        elif not word["default_branch"]:
            return _deny("default-branch", REASON_DEFAULT_BRANCH % (a.branch or a.route))
    return True, "ok", ""


def _own_f1_block(reason):
    return OUR_BLOCK_MARK in reason and F1_BLOCK_MARK in reason


def own_prompt_class_block(reason):
    """A block reason of governance-enforce.py that is not its outward-action reason."""
    return OUR_BLOCK_MARK in reason and F1_BLOCK_MARK not in reason


def f1_decision(model, ledger=(), stop_hook_active=False):
    """The outward-action rule of the Stop gate -> (block, missing, kinds).

    Judged: the counted acts of the stretch. The stretch is cut at every start of a governance turn inside it
    (a scheduled run that begins mid-stretch); each part is judged on the loads of its own governance turn.
    In a part, plan-gate must be loaded before each act and adversarial-verify anywhere; a compaction voids the
    loads made before it for the acts that come after it. After this rule's own block, a plan-gate load made
    since answers the acts made before that block although it comes after them; an act made after the block
    needs plan-gate before it, as any act does (S8). The retry flag decides nothing by itself: this rule's
    earlier blocks are counted from the record (the last one also when the flag says this stop answers it), at
    most F1_MAX_BLOCKS per stretch."""
    model.f1_note = ""
    start = model.stretch_start
    retry = bool(stop_hook_active)
    own = model.feedback(start, _own_f1_block, retry)
    if retry and not model.feedback(start, None, retry):
        return False, [], []                        # the flag is set and the record shows no block: one retry
    if len(own) >= F1_MAX_BLOCKS:
        return False, [], []
    acts = model.outward(start, ledger)
    if not acts:
        return False, [], []
    cuts = [(r, kind) for r, kind in model.turn_marks if r > start]
    parts = [(max([r for r, _kind in model.turn_marks if r <= start] or [-1]), start, None)]
    parts += [(r - 1, r - 1, kind) for r, kind in cuts]
    for n, (gov, low, kind) in enumerate(parts):
        high = cuts[n][0] if n < len(cuts) else None
        mine = [x for x in acts if x[0] > low and (high is None or x[0] < high)]
        if not mine:
            continue
        loads = model.loads(gov, high)
        compactions = [e.i for e in model.evs if e.kind == "COMPACT" and e.i > gov] if COMPACTION_VOIDS_LOADS else []
        remedy = own[0] if (own and n == len(parts) - 1) else None
        plan_ok, plan_voided = True, False
        for i, k, _act in mine:
            floor = max([c for c in compactions if c < i] or [gov])
            if not any(g == PLAN_GOVERNOR and li > floor
                       and ((li, lk) < (i, k) or (remedy is not None and i < remedy and li > remedy))
                       for li, lk, g in loads):
                plan_ok = False
                plan_voided = plan_voided or any(g == PLAN_GOVERNOR and li <= floor for li, _lk, g in loads)
        floor = max([c for c in compactions if c < mine[-1][0]] or [gov])
        verify_ok = any(g == VERIFY_GOVERNOR and li > floor for li, _lk, g in loads)
        if plan_ok and verify_ok:
            continue
        missing = []
        if not plan_ok:
            missing.append(MISSING_PLAN_RELOAD if plan_voided else MISSING_PLAN)
        if not verify_ok:
            voided = any(g == VERIFY_GOVERNOR for _li, _lk, g in loads)
            missing.append(MISSING_VERIFY_RELOAD if voided else MISSING_VERIFY)
        if kind == "scheduled":
            model.f1_note = NOTE_IN_RUN
        elif cuts and cuts[0][1] == "scheduled":
            model.f1_note = NOTE_BEFORE_RUN
        return True, missing, sorted(set(a.kind for _i, _k, a in mine))
    return False, [], []


def stop_span(rows_or_model):
    """(first row of the stretch, row count): what one Stop judges. Every Stop hook takes the stretch from
    here, so they all judge the same rows."""
    m = rows_or_model if isinstance(rows_or_model, Model) else Model(rows_or_model)
    return m.stretch_start + 1, len(m.rows)


# ----------------------------------------------------------------------------------------------------------------
# 9. State files: a helper agent's outward calls are not in the main record, so the pre-tool hook notes them
# ----------------------------------------------------------------------------------------------------------------
def state_dir():
    """$TURNGATE_STATE_DIR, else $TMPDIR/turn-gates, else /tmp/turn-gates."""
    return os.environ.get(STATE_DIR_ENV) or os.path.join(os.environ.get(TMPDIR_ENV) or STATE_DIR_DEFAULT, LEDGER_DIRNAME)


def _key(*parts):
    return hashlib.sha1("\x00".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:LEDGER_KEY_CHARS]


def ledger_path(transcript_path):
    return os.path.join(state_dir(), LEDGER_FILE % _key(os.path.abspath(transcript_path or "?")))


def ledger_add(transcript_path, rows_seen, agent_id, tool, kinds):
    """Note one outward call of a helper agent: when, how many rows the main record held, who, which tool, what."""
    path = ledger_path(transcript_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"t": round(time.time(), 3), "rows": rows_seen, "agent": agent_id, "tool": tool,
                             "kinds": list(kinds)}) + "\n")


def ledger_read(transcript_path):
    out = []
    try:
        with open(ledger_path(transcript_path), encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                try:
                    note = json.loads(raw)
                except Exception:
                    continue
                if isinstance(note, dict):
                    out.append(note)
    except Exception:
        pass
    return out


def advisory_marker(session_id, load_id):
    """The file that records that the plan-shown advisory was given for one plan-gate load."""
    return os.path.join(state_dir(), ADVISORY_FILE % _key(session_id, load_id))


# ----------------------------------------------------------------------------------------------------------------
# 10. Names older callers use (governance-trigger.py, the replay tool): same call shapes, answered by the model
# ----------------------------------------------------------------------------------------------------------------
def _block_acts(block):
    acts, _ok = classify_call(block.get("name"), block.get("input") or {})
    return acts


def is_merge(block):
    return any(a.kind in MERGE_GATED_KINDS for a in _block_acts(block))


def is_outward(block):
    return any(a.kind in F1_COUNTED_KINDS for a in _block_acts(block))


def is_write(block):
    return any(a.kind in WRITE_KINDS for a in _block_acts(block))


def merge_target(block):
    number = next((a.pr for a in _block_acts(block) if a.kind == "merge" and a.pr is not None), None)
    return str(number) if number is not None else None


def owner_index(rows):
    """The row of the owner's latest typed message, or -1."""
    return Model(rows).last_owner


def turn_start(rows):
    """The row where the governance turn starts, or -1."""
    return Model(rows).gov_start


def scheduled_index(rows):
    """The row where the latest scheduled run starts, or -1."""
    starts = Model(rows).run_starts
    return starts[-1] if starts else -1


def owner_text(rows, li):
    return (_text(rows[li].get("message")) or "") if 0 <= li < len(rows) else ""


def events(rows, start):
    """("text", str) | ("tool", block) | ("answer", str) after row `start`, in order. An answer is the result of
    a card's own call."""
    m, out = Model(rows), []
    for ev in m.evs[start + 1:]:
        if ev.kind == "ASSISTANT":
            for b in _content(rows[ev.i]) or []:
                if isinstance(b, dict) and b.get("type") == "text" and str(b.get("text") or "").strip():
                    out.append(("text", b["text"]))
                elif isinstance(b, dict) and b.get("type") == "tool_use":
                    out.append(("tool", b))
        elif ev.kind == "RESULT":
            for b in ev.results:
                use = m.uses.get(m._call_of.get(id(b)))
                if use and not use[3] and use[2].get("name") == CARD_TOOL and not b.get("is_error"):
                    out.append(("answer", _result_text(b)))
    return out


def answer_choices(text):
    """The chosen options of a card answer text ("question"="choice"), never the question."""
    return ANSWER_CHOICE.findall(text or "")


def says_merge(text):
    """Does this text hold an order to merge (the grammar of typed_ops, the number aside)?"""
    return any(TYPED_ORDER.match(s.strip()) and not REFUSAL_CUE.search(s)
               for s in SENTENCE_SPLIT.split(normalize(text)) if s)


def merge_authorized(rows, li, block):
    return merge_decision(Model(rows), _block_acts(block))[0]


# ----------------------------------------------------------------------------------------------------------------
# 11. Command line, for shell hooks:  python3 turngate.py span <transcript> [last message]
# ----------------------------------------------------------------------------------------------------------------
def span(transcript_path, last_message=None):
    """The stretch one Stop judges, as a shell hook needs it: where it starts, what the assistant said in it
    (the final answer included when the record lacks it), and how many blocks of each Stop hook it holds."""
    m = Model(load(transcript_path))
    start, count = stop_span(m)
    return {"start": start, "rows": count, "gov_start": m.gov_start, "gov_kind": m.gov_kind,
            "texts": m.prose(start - 1, last_message),
            "blocks": {"any": len(m.feedback(start - 1)),
                       "by_mark": dict((mark, len(m.feedback(start - 1, mark))) for mark in SPAN_MARKS)}}


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "span":
        try:
            print(json.dumps(span(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)))
        except Exception:
            print("{}")
    else:
        print("usage: turngate.py span <transcript> [last message]")
