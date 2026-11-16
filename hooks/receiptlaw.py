#!/usr/bin/env python3
"""The receipt law, as a Stop hook (wired through receipt-law-stop-gate.sh, which runs this file).

The rule (adversarial-verify rule 6): "couldn't verify", "unable to confirm", "not available", "no data exists"
and their variants, contractions included, may be written only when the same sentence names what was attempted
and how it failed. With no attempt to cite, the honest wording is "did not check".

What is judged: the texts the owner is asked to read in the stretch this stop answers for (the rows since the
owner's latest message or the latest completed stop: turngate.stop_span, the same rows the other Stop gate judges):
every text except a working note, and the final answer the program hands over in the input
(`last_assistant_message`) unless a judged text holds it. A working note is a text whose next tool call is a
look-up (NOTE_TOOLS, or an MCP tool whose name holds a word of MCP_LOOKUP_WORDS); any other call after a text (a
card, a task list, a file sent, a write, a helper, a Skill call) leaves it judged (RECEIPT_JUDGES; the other
reading judges every text).

How a text is read:
  1. Fenced code, block quotes, inline code and words inside quotation marks are not the assistant's claim.
     A code span, a fenced block or a block quote is evidence: in the claim's sentence it is a receipt.
  2. The text is cut into sentences. A table row and a list item are sentences of their own; a line that ends
     with a colon belongs to every list item under it; a fenced block belongs to the sentence above it (also
     across one short label line such as "Attempt and failure:"). A heading is a title, not a claim.
  3. A claim is a match of one of CLAIM_FAMILIES that is the assistant's own and stands: not in a question,
     not negated ("nothing I couldn't verify"), not conditional ("if I can't verify it ..."), not reported
     ("git says it cannot ...", "he wrote that the figures were not available"), not about somebody else ("the
     vendor could not ...", "could not be verified by older clients"), not superseded ("at first I couldn't
     ..."), not a sentence about wording, not a row of a table of examples (a header cell names sentences,
     phrases ...), not a count ("| Unconfirmed | 0 |"). The assistant's whole work as subject ("this run", "my
     report", "the scheduled weekly task") is the assistant with a verb of verifying (EPISTEMIC_VERBS) only;
     "the nightly job couldn't reach X" is a system's. "I wanted to verify X but couldn't." is a claim
     (the elliptical family). A statement about code or a product is not a
     claim either: the verbs of finding and reaching (ACCESS_VERBS) with "we" or in the passive are claims in
     the past tense only ("we can't access the DOM from a worker" against "we couldn't access the dashboard");
     "no way to know" is a claim of "I" or in the past tense; a clause that states a condition or describes
     ("when the server could not be reached", "a player whose team could not be found") and an event told with
     its period ("could not be reached while the certificate was rotated") claim nothing.
  4. A receipt is, in the same sentence and outside the words that say what was not verified (they end at a
     comma, a colon, a bracket, a clause word, or a phrase of means or source: "with", "from", "per", "in 50
     runs"; a clause such as "whether the job ran" runs on to a comma or a clause word): an attempt (ATTEMPT), a
     failure mode (FAILURE), a stated choice (CHOICE: "did not check, to save time"), or a code
     span, fenced block or block quote. A search that names its place ("couldn't find X in the repository")
     carries its receipt. RECEIPT_SCOPE widens "same sentence" to its two neighbours.

The first claim with no receipt blocks the stop, at most RECEIPT_MAX_BLOCKS times in one stretch. The count is
read from the record (the feedback rows a blocked stop leaves), never from a file. The retry flag
(stop_hook_active) is true after ANY Stop hook blocked, so it does not mean "this gate already blocked": only
when the flag is set and the record shows no block at all is the stop let go.

Which way a failure goes: an input or a record that cannot be read, an error here or in turngate.py, and this
hook's own deadline all ALLOW the stop. Every path ends with exit status 0 and prints one JSON object or
nothing. No environment variable and no key of the input switches the rule off.

Limits (also in hooks/README.md): this is a reading of words, not of meaning. A paraphrase outside the families
passes; a claim under a heading, or after a word of MENTION_WORDS, passes; a receipt word that sits outside the
unverified thing but is about something else still counts; a reason given in free words is not read as a receipt.
Where a sentence can be read both as the assistant's inability and as a statement about a system, the gate lets
it through: it blocks a stop, so a doubt goes to the answer. Standard library only; imports only turngate.
"""
import json
import os
import re
import signal
import sys
import threading
import time

# ------------------------------------------------------------------------------------------------- policy values
HOOK_DEADLINE_SECONDS = 8           # under the wired timeout of 10 s: the hook ends itself, quietly, before it is cut off
RECEIPT_MAX_BLOCKS = 1              # blocks of this gate in one stretch (counted from the record)
SCOPE_NEIGHBOURS = "neighbours"     # the other value RECEIPT_SCOPE may take: the sentence before and the one after count too
RECEIPT_SCOPE = "sentence"          # where a claim's receipt may sit: its own sentence ("sentence"), or SCOPE_NEIGHBOURS
NOT_VERIFIED_IS_A_CLAIM = False     # whether "X was not verified / has not been confirmed" (no "could not") needs a receipt
JUDGES_EVERY_TEXT = "every-text"    # the other value RECEIPT_JUDGES may take: every text of the stretch is judged
RECEIPT_JUDGES = "answers"          # which texts are judged: what the owner is asked to read ("answers"), or JUDGES_EVERY_TEXT
NOTE_TOOLS = ("Bash", "Read", "Grep", "Glob", "WebFetch", "WebSearch", "ToolSearch", "Monitor",
              "NotebookRead")       # under "answers", a text is a working note only when the next tool call is a look-up: one of these ...
MCP_PREFIX = "mcp__"                # ... or a tool of an MCP server (a name that starts with this) ...
MCP_LOOKUP_WORDS = ("get", "list", "read", "search", "query", "fetch", "view")   # ... whose own name holds one of these words
BLOCKED_STOP_ENDS_ANSWER = True     # a text the assistant stopped on is an answer, also when another Stop hook blocked that stop
REASON_EXCERPT_CHARS = 160          # how much of the sentence the block reason quotes
REASON = ('Receipt law: this answer says "%s" and the same sentence names no attempt and no failure (the sentence: '
          '"%s"). A claim that something could not be verified, found or reached needs its receipt in the sentence '
          "that makes it. Do one of these before you finish:\n"
          "  1. Run the check. If it is cheap, this is almost always the right move.\n"
          '  2. Write "did not check" instead, and say why (cost, time, tool budget): a stated choice the reader '
          "can overrule.\n"
          "  3. If it cannot be settled, say in that same sentence what you tried and how it failed, or what you "
          "searched and why it cannot settle the question.\n"
          "If a conclusion rests on this item, option 2 does not finish the job: resolve it or withdraw the "
          "conclusion. If the words are not a claim of yours (you quote a tool or a person, or describe the rule), "
          "put them in quotation marks. This gate speaks once in a stretch of work.")

# ------------------------------------------------------------------------------------------------- reading a text
MARK_BLOCK = "\ue000"               # stands for a fenced block or a block quote
MARK_CODE = "\ue001"                # stands for an inline code span
MARK_QUOTE = "\ue002"               # stands for words inside quotation marks
CHAR_MAP = (("’", "'"), ("‘", "'"), ("ʼ", "'"), ("“", '"'), ("”", '"'), ("–", " - "), ("—", " - "),
            ("\u00a0", " "), ("\u200b", ""), ("\r\n", "\n"), ("\r", "\n"))    # one spelling for quotes, dashes, spaces
FENCE_ONE_LINE = re.compile(r"```[^`\n]+```")                                  # a fenced span that opens and closes on one line
FENCE = re.compile(r"^[ \t]*(```|~~~)[^\n]*\n.*?(?:^[ \t]*\1[ \t]*$|\Z)", re.M | re.S)   # a fenced block; unclosed: to the end
BLOCKQUOTE = re.compile(r"(?:^[ \t]*>[^\n]*(?:\n|\Z))+", re.M)                 # consecutive lines that start with ">"
INLINE_CODE = re.compile(r"``[^\n]+?``|`[^`\n]+`")
QUOTED_DOUBLE = re.compile(r'"(?:[^"\n]|\n(?![ \t]*\n)){1,400}?"')            # may wrap over a line, never over a blank line
QUOTED_SINGLE = re.compile(r"(?<![A-Za-z0-9])'(?=\S)(?:[^'\n]|\n(?![ \t]*\n)|'(?=[A-Za-z])){1,400}?'(?![A-Za-z0-9])")
EMPHASIS = re.compile(r"(?<![A-Za-z0-9])[*_]{1,3}(?=\S)|(?<=\S)[*_]{1,3}(?![A-Za-z0-9])")    # bold and italic marks
HEADING = re.compile(r"^[ \t]{0,3}#{1,6}\s")
LIST_ITEM = re.compile(r"^[ \t]*(?:[-*+]|\d{1,3}[.)])\s+")
TABLE_ROW = re.compile(r"^[ \t]*\|.*\|[ \t]*$")
TABLE_RULE = re.compile(r"^[ \t]*\|?[ \t:|-]*-[ \t:|-]*\|?[ \t]*$")              # the line under a table's header
EXAMPLE_TABLE_WORDS = ("example", "examples", "sentence", "sentences", "phrase", "phrases", "text", "texts", "fixture",
                       "fixtures")              # a header cell that names language samples: a table of examples
TALLY_LABEL = re.compile(r"^(?:unverified|unconfirmed|unverifiable|unconfirmable)$", re.I)   # "| Unconfirmed | 0 |": a count ...
TALLY_NUMBER = re.compile(r"^(?:\d{1,3}(?:,\d{3})+|\d+)(?:\s*(?:of|/)\s*(?:\d{1,3}(?:,\d{3})+|\d+))?$|^\d+(?:\.\d+)?\s*%$",
                          re.I)               # ... when every other cell is a count: a whole number, "N of M", "N / M" or a share
DATA_CELL = re.compile(r"^v?\d[\w.:/-]*$", re.I)   # a header cell that is a number, a date or a version: the header is a row of data
ASSUMPTION_TABLE_WORDS = ("assumption", "assumptions", "basis")                 # ... and of a register of assumptions
SENTENCE_END = re.compile(r"(?:(?<=[.!?])|(?<=[.!?][)\]'\"]))(?<!\be\.g\.)(?<!\bi\.e\.)(?<!\bvs\.)(?<!\bcf\.)\s+"
                          r"(?=[A-Z0-9\"'(\[\ue001\ue002])")
LABEL_MAX_CHARS = 60                # a line this short that ends with a colon may introduce a fenced block
LABEL_WORDS = ("attempt", "attempts", "tried", "failure", "failed", "error", "errors", "output", "command", "commands",
               "result", "results", "response", "log", "logs", "trace", "traceback", "message", "stderr", "stdout",
               "ran", "got", "receipt")                                         # what such a label must talk about

# ------------------------------------------------------------------------------------------------- claims
ADVERB = r"(?:\w+ly|yet|still|even|ever|really|quite|just|also|now|either)"    # may stand between "could not" and the verb
MODAL_NOT = r"(?:can't|cannot|can\s+not|cant|couldn't|could\s+not|couldnt)"
MODAL_NOT_PAST = r"(?:couldn't|could\s+not|couldnt)"       # the past forms: a report of what happened, not a general statement
VERIFY_VERBS = ("verify", "confirm", "double-check", "cross-check", "validate", "reproduce", "establish", "ascertain",
                "corroborate", r"tell\s+(?:whether|if|which|what|who|how|when|where|why|from)\b",
                r"get\s+(?:any\s+|a\s+|an\s+|the\s+)?(?:confirmation|verification|access|response|reply|answer)\b")
# verbs that also describe code and products ("we can't access the DOM from a worker"): with "we" a claim only in the past tense
ACCESS_VERBS = (r"check\b(?!\s+(?:(?:this|that|it|them|these|those)\s+)?(?:in|out|off)\b)", "determine",
                r"find\b(?!\s+(?:any(?:thing)?\s+|a\s+|an\s+|no\s+|the\s+|another\s+)?(?:\w+\s+)?(?:wrong|amiss|issues?|problems?|"
                r"bugs?|errors?|faults?|defects?|flaws?|mistakes?|regressions?|discrepanc\w+|inconsistenc\w+|violations?|"
                r"conflicts?|ways?|alternatives?|workarounds?|solutions?|approach(?:es)?|reasons?|differences?|mismatch(?:es)?|"
                r"duplicates?|typos?)\b)(?!\s+a\s+single\b)"
                r"(?!\s+(?:any|one|another)\s+(?:\w+\s+)?(?:failing|failed|broken|failures?|counter-?examples?)\b)"
                r"(?!\s+(?:a|an|any)\s+(?:better|simpler|cheaper|faster|cleaner|shorter|smaller|safer|stronger|more\s+\w+|less\s+\w+)\b)",
                r"reach\b(?!\s+(?:(?:a|an|any|the|another)\s+)?(?:\w+\s+)?(?:conclusion|verdict|decision|agreement|consensus)\b)",
                "access", "obtain", r"locate\b(?!\s+a\s+single\b)", "retrieve")
VERIFY_PARTICIPLES = ("verified", "confirmed", "validated", "reproduced", "established", "ascertained", "corroborated")
ACCESS_PARTICIPLES = ("determined", "checked", "found", "reached", "accessed", "obtained", "located",
                      "retrieved")                                              # "could not be reached": in the past tense only
CLAIM_GERUNDS = ("verifying", "confirming", "checking", "determining", "finding out",
                 "validating", "reproducing", "establishing", "ascertaining")
KNOW_VERBS = (r"know\b", r"tell\b", r"be\s+sure\b")      # "no way to know": said of code in the present tense; a claim in the past or of "I"
KNOW_GERUNDS = ("knowing", "telling")
NOMINAL_GERUNDS = ("verifying", "confirming", "validating")     # "VERIFYING the upload wasn't possible"
NOMINAL_REACH = 6                   # words between "verification (of)" or such a gerund and "was not possible"
NOT_POSSIBLE = r"(?:\bimpossible|\binfeasible|(?:\bnot|n't)\s+(?:possible|feasible))"
DATA_NOUNS = ("data", "information", "info", "figure", "figures", "number", "numbers", "statistic", "statistics",
              "stats", "record", "records", "log", "logs", "detail", "details", "documentation",
              "history")                                                        # what "not available" must be said of
UNVERIFIED_FOLLOWERS = ("at", "in", "on", "by", "as", "so", "and", "but", "or", "because", "since", "from", "for",
                        "until", "after", "here", "yet", "still", "due", "pending", "to", "with", "when", "while",
                        "although", "though", "now", "today", "however")       # after "unverified": still a predicate
DEGREE_WORDS = ("yet", "independently", "fully", "currently", "publicly", "readily", "still", "simply", "now")   # "not YET verified"
LINK_WORDS = ("for", "from", "of", "on", "in", "about")                        # "the figures FOR 2024 are not available"
STREAM_WORDS = ("more", "further", "additional", "new", "remaining", "longer")  # "there is no MORE data to read": a stream ran dry
DATA_FOLLOWERS = ("for", "on", "about", "in", "from", "of", "at", "that", "which", "here", "available", "yet", "anywhere",
                  "whatsoever", "to", "before", "after", "since", "between", "and", "or", "so",
                  "but")                    # after "there is no data": any other word makes "data" part of a name ("no data loss")
SCOPE_WORDS = ("at", "in", "on", "until", "before", "during", "when", "while", "unless", "if", "under", "within",
               "by")                        # "not available AT compile time": where or when a thing is offered, not a missing fact
HERE_AND_NOW = (r"the\s+moment", r"this\s+time", "present", r"this\s+(?:session|environment|sandbox|container|machine|point|stage)",
                r"my\b", r"our\b")           # ... unless that scope is the assistant's own here and now
_vverb = r"(?:%s)" % "|".join(v if v.endswith((")", "b")) else v + r"\b" for v in VERIFY_VERBS)
_averb = r"(?:%s)" % "|".join(v if v.endswith((")", "b")) else v + r"\b" for v in ACCESS_VERBS)
_verb = r"(?:%s|%s)" % (_vverb, _averb)
_vpart = r"(?:%s)" % "|".join(VERIFY_PARTICIPLES)
_apart = r"(?:%s)" % "|".join(ACCESS_PARTICIPLES)
_ger = r"(?:%s)" % "|".join(CLAIM_GERUNDS).replace(" ", r"\s+")
_noun = r"(?:%s)" % "|".join(DATA_NOUNS)
_advs = r"(?:\s+%s){0,2}" % ADVERB
_of = r"(?:\s+(?:%s)\s+(?:[\w'./-]+\s+){0,4}[\w'./-]+)?" % "|".join(LINK_WORDS)
_degree = r"(?:(?:%s)\s+){0,2}" % "|".join(DEGREE_WORDS)
_know = r"(?:%s)" % "|".join(KNOW_VERBS)
_knowing = r"(?:%s)" % "|".join(KNOW_GERUNDS)
_not_know = r"(?!%s)" % _know
_scoped = r"(?!\s+(?:%s)\b(?!\s+(?:%s)))" % ("|".join(SCOPE_WORDS), "|".join(HERE_AND_NOW))
_data_end = r"(?=\s*(?:$|[.,;:!?)\]]|(?:%s)\b))" % "|".join(DATA_FOLLOWERS)
_no_stream = r"(?!(?:%s)\b)" % "|".join(STREAM_WORDS)
# (family, pattern, whose claim must be settled): the families of inability claims
ELLIPTICAL_END = (r"(?:couldn't|could\s+not|couldnt|(?:wasn't|was\s+not|weren't|were\s+not)\s+able\s+to|"
                  r"(?:was|were)\s+unable\s+to)")   # "I wanted to verify the deploy but COULDN'T.": the verb stands earlier
CLAIM_FAMILIES = (
    ("passive", re.compile(r"\b%s%s\s+be%s\s+%s\b" % (MODAL_NOT, _advs, _advs, _vpart), re.I), False),
    ("passive-past", re.compile(r"\b%s%s\s+be%s\s+%s\b" % (MODAL_NOT_PAST, _advs, _advs, _apart), re.I), False),
    ("modal", re.compile(r"\b%s%s\s+%s" % (MODAL_NOT, _advs, _vverb), re.I), True),
    ("modal-access", re.compile(r"\b%s%s\s+%s" % (MODAL_NOT, _advs, _averb), re.I), True),
    ("unable", re.compile(r"\bunable\s+to%s\s+%s" % (_advs, _verb), re.I), True),
    ("not-able", re.compile(r"(?:\bnot|n't)\s+(?:(?:been|yet|be|%s)\s+){0,2}able\s+to%s\s+%s" % (ADVERB, _advs, _verb), re.I), True),
    ("failed-to", re.compile(r"\bfailed\s+to%s\s+%s" % (_advs, _verb), re.I), True),
    ("no-way", re.compile(r"\bno\s+way\s+(?:for\s+(?:me|us)\s+)?(?:to%s\s+%s%s|of\s+%s\b)" % (_advs, _not_know, _verb, _ger), re.I), True),
    ("know", re.compile(r"\bno\s+way\s+(?:for\s+(?:me|us)\s+)?(?:to%s\s+%s|of\s+%s\b)" % (_advs, _know, _knowing), re.I), True),
    ("no-access", re.compile(r"\b(?:(?:do\s+not|don't|did\s+not|didn't|does\s+not|doesn't)\s+have|(?:have|has|had)\s+no|"
                             r"lack(?:s|ed)?)\s+(?:any\s+|direct\s+|read\s+|write\s+)?access\s+to\b", re.I), True),
    ("impossible", re.compile(r"%s\s+(?:for\s+(?:me|us)\s+)?to%s\s+%s%s" % (NOT_POSSIBLE, _advs, _not_know, _verb), re.I), False),
    ("know", re.compile(r"%s\s+(?:for\s+(?:me|us)\s+)?to%s\s+%s" % (NOT_POSSIBLE, _advs, _know), re.I), False),
    ("impossible", re.compile(r"\b(?:(?:verification|confirmation|validation)(?:\s+of)?|%s)(?:\s+[\w'./-]+){0,%d}?\s+"
                              r"(?:(?:was|is|were)\s*(?:\s+not|n't)|has\s+not\s+been|hasn't\s+been)\s+(?:possible|feasible)\b"
                              % ("|".join(NOMINAL_GERUNDS), NOMINAL_REACH), re.I), False),
    ("unverified", re.compile(r"(?<![\w-])(?:unverified|unconfirmed|unverifiable|unconfirmable)\b(?=\s*(?:$|[^\w\s]|(?:%s)\b))"
                              % "|".join(UNVERIFIED_FOLLOWERS), re.I), False),
    ("not-verified", re.compile(r"(?<!have\s)(?<!has\s)(?<!had\s)(?<!'ve\s)(?<!did\s)(?<!do\s)(?<!does\s)\bnot\s+%s"
                                r"(?:verified|confirmed)\b|\bnot\s+(?:yet\s+)?been\s+%s(?:verified|confirmed)\b|"
                                r"\b(?:is|was|are|were)n't\s+%s(?:verified|confirmed)\b|"
                                r"\b(?:has|have|had)n't\s+(?:yet\s+)?been\s+%s(?:verified|confirmed)\b|"
                                r"\bnot\s+(?:be\s+)?(?:verifiable|confirmable)\b" % (_degree, _degree, _degree, _degree), re.I), False),
    ("not-available", re.compile(r"\b%s\b%s\s+(?:(?:is|are|was|were)\s+%snot|(?:is|are|was|were)n't)\s+%s(?:available|accessible)\b%s|"
                                 r"\b%s\b%s\s+(?:is|are|was|were)\s+%s(?:unavailable|inaccessible)\b%s|"
                                 r"(?:\bnot|n't)\s+%s(?:available|accessible)\s+(?:to\s+(?:me|us)\b|here\b|from\s+here\b|"
                                 r"in\s+this\s+(?:session|environment|sandbox|container)\b|to\s+this\s+session\b)"
                                 % (_noun, _of, _degree, _degree, _scoped, _noun, _of, _degree, _scoped, _degree), re.I), False),
    ("elliptical", re.compile(r"\bto%s\s+%s[^.;:!?]*?\bbut\s+(?:(?:i|we)\s+)?(?P<claim>%s)(?=\s*(?:$|[.;:!?,)\]]))"
                              % (_advs, _verb, ELLIPTICAL_END), re.I), True),
    ("no-data", re.compile(r"\bno\s+%s\s+(?:exists?|existed|(?:is|are|was|were)\s+(?:available|recorded|kept|published|accessible))\b|"
                           r"\bthere\s*(?:\s+(?:is|are|was|were)|'s)\s+no\s+%s(?:\w+\s+){0,2}?%s\b%s"
                           % (_noun, _no_stream, _noun, _data_end), re.I), False),
)

# -- whose claim it is: the word before the claim, past auxiliaries and adverbs
SELF_SUBJECTS = ("i", "we")
GENERAL_SUBJECT = "we"              # "we can't access X from a worker" describes code; "we couldn't access X" reports
PAST_MODAL = re.compile(MODAL_NOT_PAST, re.I)
SELF_NOUNS = ("session", "container", "sandbox", "environment", "assistant", "agent")   # "this session cannot reach ..."
EPISTEMIC_VERBS = ("verify", "confirm", "check", "validate", "establish", "determine", "prove",
                   "reproduce")             # only with one of these verbs can a subject that names a piece of work be the assistant
WORK_NOUNS = ("run", "session", "report", "audit", "review", "pass", "task", "job", "analysis",
              "check")                      # "THIS RUN couldn't confirm ...": the assistant's whole work when, in the subject's ...
WORK_SUBJECT_WORDS = 5                      # ... first this many words, such a noun stands with an owner or a time word:
WORK_OWNERS = ("this", "my", "our", "today's", "tonight's")
WORK_TIMES = ("weekly", "daily", "nightly", "morning", "afternoon", "scheduled", "automated", "unattended")
OTHER_OWNERS = ("your", "their", "his", "her", "its")   # a subject that names somebody else's work is not the assistant's ...
TIME_POSSESSIVES = ("today's", "tonight's", "week's", "month's", "night's", "morning's",
                    "yesterday's")          # ... nor is one with a possessive ("the client's job"), unless it is one of these
IMPERSONAL_SUBJECTS = ("there",)
JOINING_WORDS = ("and", "but", "so", "then", "or", "yet", "nor", "plus")       # the subject is left out after these
SELF_WORD = re.compile(r"(?<![\w'-])(?:i|we)(?![\w-])", re.I)                  # ... and is the assistant when the clause before says "I"
OTHER_START = re.compile(r"(?:the|a|an|this|that|these|those|its|their|his|her|each|every|some|no|it|they|he|she|you)\b", re.I)
SKIPPED_WORDS = ("am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
                 "will", "would", "shall", "may", "might", "still", "also", "just", "simply", "really", "honestly",
                 "currently", "therefore", "thus", "however", "unfortunately", "sadly", "ultimately", "actually",
                 "frankly", "genuinely", "truly", "now", "again", "ever", "even", "too", "both", "either")
SUBJECT_REACH = 6                   # how many such words are skipped on the way back to the subject
BEFORE_REACH = 600                  # how many characters before a claim are read to tell whose it is and whether it stands
AFTER_REACH = 300                   # how many characters after a claim are read for "at first", "while ..." and the searched place
CLAUSE_OPENERS = ":;(,|" + MARK_BLOCK + MARK_CODE + MARK_QUOTE      # a claim right after one of these has no subject before it
SUBJECT_PRONOUNS = ("i", "we", "you", "they", "he", "she", "it", "there")      # may stand between "if", "nothing", "said" and the claim
_subj = r"(?:%s)" % "|".join(SUBJECT_PRONOUNS)
_aux = r"(?:(?:%s|\w+ly)\s+)*" % "|".join(SKIPPED_WORDS)
# -- sentences that hold the words and make no claim
NEGATED_BEFORE = re.compile(
    r"\b(?:nothing|none|no\s+\w+|not\s+a\s+single\s+\w+|never|not\s+that|n't\s+that|no\s+one|nobody|(?:not|n't|hardly)\s+anything)"
    r"(?:\s+(?:that|which|left|else|here|of\s+\w+))?\s+(?:%s\s+)?%s$" % (_subj, _aux), re.I)
NEGATED_CLAUSE = re.compile(r"\b(?:none|nothing|no|never|neither|nor|no\s+longer|not\s+the\s+case)\b[^,;:.!?]*$|\bnot\s+$", re.I)
CONDITIONAL_BEFORE = re.compile(
    r"\b(?:if|unless|whenever|in\s+case|should|whatever|wherever|anything|everything|any\s+\w+)"
    r"(?:\s+(?:that|which))?\s+(?:%s\s+)?%s$" % (_subj, _aux), re.I)
REPORTED_VERBS = (r"said|says|say|saying|wrote|writes|reported|reports|printed|prints|replied|replies|answered|answers|"
                  r"responded|stated|states|claimed|claims|warned|warns|complained|complains|reads")
# "it says so (can't confirm ...)": the words of an open parenthesis right after a verb of saying are what was said
REPORTED_OPEN = re.compile(r"\b(?:%s)\s+(?:so\s+|back\s+|this\s+|as\s+much\s+)?\([^()]*$" % REPORTED_VERBS, re.I)
# "he wrote (that) the figures were not available": the clause after a verb of saying, whatever its subject
REPORTED_NOUNS = "claim|statement|remark|assertion|finding|caveat|sentence|allegation"      # "the claim that X could not be verified"
REPORTED_THAT = re.compile(r"(?:\b(?:%s|told\s+\w+)(?:\s+that)?\b|(?:\b(?:%s|not)|n't)\s+that\b)[^,;:.!?()]*$"
                           % (REPORTED_VERBS, REPORTED_NOUNS), re.I)
REPORTED_BEFORE = re.compile(
    r"(?:\b(?:said|says|say|saying|wrote|writes|reported|reports|printed|prints|replied|replies|answered|answers|responded|"
    r"told\s+\w+|stated|states|claimed|claims|warned|warns|complained|complains|reads|stopped\s+with|failed\s+with|"
    r"exited\s+with|aborted\s+with|errored\s+with|died\s+with)\s*(?:back\s+)?(?:that\s+|the\s+message\s+|the\s+error\s+)?:?"
    r"|\b(?:message|error|warning|output|log)\s*:)\s*(?:%s\s+)?%s$" % (_subj, _aux), re.I)
SUPERSEDED_WORDS = ("at first", "initially", "earlier", "previously", "originally", "at the start", "until then",
                    "before that")                                              # the claim is about a state that ended
SUPERSEDED_BEFORE = re.compile(r"\b(?:%s)\b[^;:.!?]*$" % "|".join(SUPERSEDED_WORDS).replace(" ", r"\s+"), re.I)
SUPERSEDED_AFTER_WORDS = ("at first", "initially", "at the start", "to begin with", "for a while")   # "couldn't find it AT FIRST; ..."
SUPERSEDED_AFTER = re.compile(r"[^;:.!?]*?\b(?:%s)\b" % "|".join(SUPERSEDED_AFTER_WORDS).replace(" ", r"\s+"), re.I)
CONDITION_WORDS = ("if", "unless", "whenever", "when", "where", "whose", "once", "until", "while", "in case")
# "... WHEN the server could not be reached": a clause that states a condition claims nothing (a comma ends the clause)
CONDITION_BEFORE = re.compile(r"\b(?:%s)\b[^,;:.!?()]*$" % "|".join(CONDITION_WORDS).replace(" ", r"\s+"), re.I)
PERIOD_WORDS = ("while", "during", "whenever", "when", "until")
# "the dashboard could not be reached WHILE the certificate was rotated": an event in the world, with its period
PERIOD_AFTER = re.compile(r"[^,;:.!?()]*?\b(?:%s)\b" % "|".join(PERIOD_WORDS), re.I)
EVENT_FAMILIES = ("passive", "passive-past")                                    # the families PERIOD_AFTER is read for
NOT_AGENTS = ("me", "us", "myself", "ourselves", "yourselves", "this", "the time", "the end", "then", "now", "today",
              "tomorrow", "hand", "means", "ways", "methods")   # after "could not be verified by": the assistant, a time or a means
AGENT_END_WORDS = ("which", "who", "whom", "whose", "that", "because", "since", "so", "but", "and", "or", "when", "while",
                   "as", "after", "before", "until", "if", "though", "although")   # where the "by" phrase ends, besides a mark
PASSIVE_AGENT = re.compile(r"\s+by\s+(?!(?:%s)\b)(?![a-z]+ing\b)(?P<agent>[a-z][^,;:.!?()]*?)(?=\s*(?:[,;:.!?()]|$)|\s+(?:%s)\b)"
                           % ("|".join(NOT_AGENTS).replace(" ", r"\s+"), "|".join(AGENT_END_WORDS)), re.I)
AGENT_PLURAL_MIN = 3                # ... it is another agent only when it ends in a plural noun: this many letters or more, ending in "s",
AGENT_NOT_PLURAL_ENDS = ("ss", "us", "is")   # ... but not in one of these ("the process", "the status"), and not in NOT_AGENTS
HYPOTHETICAL_BEFORE = re.compile(r"\b(?:would|might|may)\s+(?:be|prove|become)\s+(?:\w+ly\s+)?$", re.I)   # "it WOULD BE impossible to ..."
CAUSATIVE_BEFORE = re.compile(r"\b(?:made|makes|make|making|renders?|rendered|rendering)\s+it\s+(?:\w+ly\s+)?$", re.I)   # "a bug MADE IT impossible to ..."
PAST_STATE = re.compile(r"\b(?:was|were|had|been)(?:n't)?(?![\w])", re.I)       # "there WAS no way to know": a report of what happened
PAST_REACH = 30                     # how many characters before "no way to know" are read for such a word
OWN_IN_CLAIM = re.compile(r"\bfor\s+(?:me|us)\b", re.I)                        # "no way FOR ME to know"
MENTION_WORDS = ("phrase", "phrases", "wording", "wordings", "pattern", "patterns", "word list", "the words", "the word",
                 "the term", "the string", "regex", "spelling", "spellings", "contraction", "contractions", "label", "labels")
MENTION_BEFORE = re.compile(r"\b(?:%s)\b[^.!?]*$" % "|".join(MENTION_WORDS).replace(" ", r"\s+"), re.I)   # a sentence about wording
GENERIC_BEFORE = re.compile(r"(?:^|[.;:!?(]\s*|,\s+)(?:a|an|any|every|each)\s+(?:[\w'-]+\s+){1,4}$", re.I)   # "a rule cannot be checked ..."
# -- "unverified" and "unconfirmed" as the house's own labels (plan-gate's register, after-report's section name)
ASSUMPTION_BEFORE = re.compile(r"(?:\bassum(?:e|ed|es|ing|ption|ptions)\b|(?<![\w-])A\d{1,2}\b)[^.!?]*$", re.I)   # the status of an assumption, also named by its number ("A1 ... is unconfirmed")
# "three tiers: verified, likely, and unverified", "12 verified, 3 unverified": a list of labels or a tally, not a claim
_sep = r"(?:\s*[,/|]\s*|\s+(?:and|or)\s+)"
ENUMERATION_BEFORE = re.compile(r"\b(?:verified|confirmed)\b%s(?:[\w-]+%s){0,3}(?:(?:and|or)\s+)?(?:\d+\s+)?$" % (_sep, _sep), re.I)
STATUS_BEFORE = re.compile(r"\bstatus\s*:\s*$", re.I)                           # "Status: unconfirmed", a register field
SECTION_BEFORE = re.compile(r"\bin\s+scope(?:\s+and|\s+but|,)\s+$", re.I)       # the section "In scope and unverified"
LABELLED_BEFORE = re.compile(r"\b(?:as|labell?ed|label|marked|mark|tagged|called|from)\s+(?:(?:it|them|this|that)\s+)?$", re.I)
ATTRIBUTIVE_BEFORE = re.compile(r"\b(?:a|an|any|another|some|these|those|its|their|my|our)\s+$", re.I)   # "an unverified, old assertion"
QUESTION_END = re.compile(r"\?[\s)\]\"'" + MARK_QUOTE + MARK_CODE + r"]*$")

# ------------------------------------------------------------------------------------------------- receipts
LABEL_COLON = re.compile(r"\s*:\s*")    # "Unverified: X": what was not verified starts after the colon
# "X cannot be reproduced: ...": in these families what was not verified stands BEFORE the claim
SUBJECT_FIRST = ("passive", "passive-past", "unverified", "not-verified", "not-available",
                 "no-data", "elliptical")
OWN_SUBJECT_FAMILIES = ("not-available", "no-data")     # their match holds the subject: a colon after it opens the explanation
OBJECT_END = re.compile(                # where the words that say WHAT was not verified end
    r"[:;(),|" + MARK_BLOCK + r"]|\s-{1,2}\s|(?<=[.!?])\s|"
    r"\b(?:because|since|after|despite|although|though|whereas|while|via|using|without|due\s+to|owing\s+to|given\s+that|"
    r"so|but|when\s+(?:i|we)|as\s+(?:the|it|i|we|there|no|none|neither)|and\s+(?:i|we|it|they|that|this|then|so)|"
    r"by\s+\w+ing)\b", re.I)
NUMBER_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
                "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "a dozen",
                "dozens of")            # a count in a receipt may be written in words ("despite three retries", "in two runs")
_numword = r"(?:%s)" % "|".join(NUMBER_WORDS).replace(" ", r"\s+")
MEANS_END = re.compile(r"\b(?:with|from|per)\b|\b(?:in|over|across)\s+(?=\d|%s\b)" % _numword, re.I)   # ... also a phrase that names the
                                        # means or the source ("in 50 runs", "from the changelog"), after at least one word
CLAUSE_OBJECT = re.compile(r"\s*(?:that|whether|if|which|what|who|whom|whose|how|when|where|why)\b", re.I)   # ... but not
                                        # in a clause ("whether the job ran per the schedule"): it runs to OBJECT_END
FIRST_WORD = re.compile(r"\s*\S+")    # the first word of what was not verified: a means after it ends it
TRIED_NAMES_NOTHING = ("hard", "harder", "hardest", "everything", "anything", "again", "twice", "once", "to", "but", "and",
                       "or", "so", "then", "it", "this", "that", "them", "really", "very", "too", "also", "still", "yet",
                       "repeatedly")            # "tried" before one of these (or a comma, an end, an -ly word) names no attempt
TRIED_OWN_NOTHING = ("best", "hardest", "utmost", "level", "luck")      # nor does "tried my BEST"
_tried = (r"tried(?=\s+(?!(?:%s)\b)(?!(?:my|our|your|their)\s+(?:%s)\b)(?![a-z]+ly\b)[\w#\"'%s%s])"
          % ("|".join(TRIED_NAMES_NOTHING), "|".join(TRIED_OWN_NOTHING), MARK_CODE, MARK_QUOTE))
ATTEMPT = re.compile(                   # an attempt: a verb of trying, or the source or the means that was used
    r"(?<![\w-])(?:ran|re-?ran|" + _tried + r"|attempted|attempts?|searched|searching|"
    r"search(?:ed|ing|es)?\s+(?:for|of|on|in|through)|"
    r"looked\s+(?:up|for|at|in|into|through|on)|looking\s+(?:up|for|at|in|into|through)|queried|querying|fetched|fetching|"
    r"called|calling|opened|opening|(?:i|we)\s+asked|read|reading|re-?read|grepped|grepping|inspected|inspecting|checked|"
    r"checking|requested|requesting|pinged|curled|downloaded|downloading|executed|executing|invoked|invoking|tested|"
    r"testing|probed|scanned|browsed|visited|pulled|cloned|logged\s+in|consulted|reviewed|examined|compared|diffed|"
    r"re-?computed|replayed|sampled|sampling|spot-check(?:s|ed|ing)?|"
    r"re-?runs?|(?:\d+|" + _numword + r")\s+(?:[\w-]+\s+)?(?:runs|attempts|tries|trials|iterations|passes|requests|searches|"
    r"queries|retries)|"
    r"attempted-failed|according\s+to|per\s+(?:the|its|their|this|that)\s+[\w./-]+|"
    r"from\s+the\s+(?:[\w'-]+\s+){0,2}?(?:docs?|documentation|page|site|logs?|output|files?|repo|repository|code|source|config|"
    r"readme|changelog|api|response|records?|transcript|diff)|(?:using|via)\s+(?:the\s+)?[\w./" + MARK_CODE + r"-]+)(?![\w-])", re.I)
FAILURE = re.compile(                   # a failure mode: what came back, or why it could not work
    r"(?<![\w-])(?:returned|returns|returning|printed|answered|responded|replied|raised|threw|came\s+back|comes\s+back|"
    r"timed\s+out|times?\s+out|time-?outs?|denied|refused|rejected|forbidden|unauthori[sz]ed|not\s+authori[sz]ed|"
    r"not\s+permitted|not\s+allowed|no\s+permission|failed|fails|failing|failure|errors?|errored|exception|traceback|"
    r"crash(?:ed|es)?|exit(?:ed)?\s+(?:status|code)|exited\s+with|rate[- ]?limit(?:ed|ing|s)?|throttled|paywall(?:ed)?|captcha|"
    r"behind\s+(?:a\s+|an\s+|the\s+)?(?:login|paywall|firewall|vpn|sso)|expired|not\s+installed|not\s+found|no\s+such\s+file|"
    r"does\s+not\s+exist|doesn't\s+exist|missing|no\s+network|no\s+internet|no\s+connection|offline|unreachable|"
    r"not\s+reachable|not\s+responding|no\s+response|no\s+reply|blocked|cut-?\s?off|not\s+(?:in|within|part\s+of)\s+my\s+training|"
    r"no\s+(?:[\w-]+\s+){0,2}(?:tools?|connector|access|credentials?|api|endpoint|command|cli|client|binary|network|token|key|"
    r"login|permissions?|path|route|way|means|connection)|not\s+exposed|does\s+not\s+expose|doesn't\s+expose|"
    r"read-?only|requires?\s+(?:a\s+|an\s+)?(?:login|account|subscription|credentials?|token|key|password|sudo|root|approval|"
    r"permission|vpn|network|javascript)|without\s+[\w'./-]+|"
    r"(?:shows?|showed|gives?|gave|lists?|listed|holds?|held|contains?|contained|prints?|printed)\s+(?:none|nothing)|needs\s+(?:sudo|root|credentials?|a\s+token|network|a\s+login)|"
    r"no\s+results?|no\s+hits?|zero\s+hits?|no\s+match(?:es)?|found\s+(?:nothing|none|no\b)|nothing\s+(?:found|came\s+back|matched)|"
    r"none\s+(?:of\s+(?:them|these|those|the\s+\w+)\s+)?(?:lists?|mentions?|shows?|has|have|contains?|includes?|gives?|states?|says?)|"
    r"neither\s+(?:of\s+them\s+)?(?:lists?|mentions?|shows?|has|contains?|includes?|gives?|states?|says?)|"
    r"came\s+back\s+empty|empty\s+(?:response|result|reply|output|body|page)|(?:is|was|are|were)\s+empty|"
    r"there(?:'s|\s+is|\s+was)\s+nothing|"
    r"(?:is|are|was|were)\s+not\s+(?:in|on|part\s+of|within)\s+(?:this|the)\s+(?:repo|repository|container|session|machine|"
    r"environment|sandbox|record|file|checkout)|"
    r"(?:does\s+not|doesn't|do\s+not|don't|did\s+not|didn't)\s+(?:list|mention|show|say|state|include|contain|record|publish|find)|"
    r"(?:http\s*)?(?:40[0134589]|410|422|429|50[0-4])(?!\.\d|%))(?![\w-])", re.I)
CHOICE = re.compile(                    # the honest alternative, said in the claim's own sentence
    r"(?<![\w-])(?:did\s+not\s+(?:check|try|attempt|look|run|test|verify|confirm)|didn't\s+(?:check|try|attempt|look|run|"
    r"test|verify|confirm)|not\s+checked|have\s+not\s+(?:checked|tried|verified|looked)|haven't\s+(?:checked|tried|verified|"
    r"looked)|not[- ]attempted|by\s+choice|to\s+save\s+(?:time|tool\s+calls|tokens|budget|effort)|ran\s+out\s+of\s+(?:time|budget|tool\s+calls|"
    r"tokens)|out\s+of\s+(?:time|budget)|stopped\s+(?:checking|looking|searching)|skipped|out\s+of\s+scope|chose\s+not\s+to|"
    r"decided\s+not\s+to|deliberately|on\s+purpose|time-?box(?:ed)?)(?![\w-])", re.I)
EVIDENCE_MARKS = MARK_BLOCK + MARK_CODE     # a quoted command or error in the claim's sentence is a receipt
SEARCH_CLAIM = re.compile(r"(?:find|locate)$", re.I)        # a claim whose verb is a search ...
SEARCHED_PLACE = re.compile(r"[^;:.!?()]*?\s(?:in|on|under|across|within|among)\s+(?:the|this|that|these|those|either|any|both|all|"
                            r"my|our|your|its|" + MARK_CODE + r")", re.I)   # ... names what was searched: "couldn't find X IN THE repository"

_epistemic = re.compile(r"\b(?:%s)\b" % "|".join(EPISTEMIC_VERBS), re.I)
_answered = threading.Lock()                # taken by whoever ends the hook


# ------------------------------------------------------------------------------------------------- the reading
def prepare(text):
    """A text with code, block quotes and quoted words replaced by one mark each, and emphasis marks removed."""
    for mark in (MARK_BLOCK, MARK_CODE, MARK_QUOTE):
        text = text.replace(mark, " ")
    for a, b in CHAR_MAP:
        text = text.replace(a, b)
    text = FENCE_ONE_LINE.sub(MARK_CODE, text)
    text = FENCE.sub("\n" + MARK_BLOCK + "\n", text)
    text = BLOCKQUOTE.sub(MARK_BLOCK + "\n", text)
    text = INLINE_CODE.sub(MARK_CODE, text)
    text = QUOTED_DOUBLE.sub(MARK_QUOTE, text)
    text = QUOTED_SINGLE.sub(MARK_QUOTE, text)
    return EMPHASIS.sub("", text)


def _is_label(sentence):
    """A short line that ends with a colon and says it introduces an attempt, an error or an output."""
    s = sentence.strip()
    if not s.endswith(":") or len(s) > LABEL_MAX_CHARS or find_claims(s):
        return False
    words = set(re.findall(r"[a-z]+", s.lower()))
    return any(w in words for w in LABEL_WORDS)


def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _tally(row):
    """A row that counts ("| Unconfirmed | 0 |", "| 3 | unconfirmed |"): one cell is only a status word, every other
    cell a count (TALLY_NUMBER: not a date, not a version)."""
    cells = _cells(row)
    labels = [c for c in cells if TALLY_LABEL.match(c)]
    return len(cells) >= 2 and len(labels) == 1 and all(TALLY_NUMBER.match(c) for c in cells if not TALLY_LABEL.match(c))


def _blocks(text):
    """The parts of one prepared text, in order, as (kind, indent, sentences): a paragraph ("para"), a list item
    ("item"), the rows of a table ("rows"), a fenced block or block quote ("code"), a heading or a table of
    examples ("title")."""
    blocks, para, table = [], [], []
    kind = ["para", 0]

    def flush_para():
        if para:
            joined = " ".join(p.strip() for p in para)
            del para[:]
            parts = [s.strip() for s in SENTENCE_END.split(joined) if s.strip()]
            if parts:
                blocks.append((kind[0], kind[1], parts))
        kind[0], kind[1] = "para", 0

    def flush_table():
        rows = table[:]
        del table[:]
        if len(rows) >= 2 and TABLE_RULE.match(rows[1]) and any(DATA_CELL.match(c) for c in _cells(rows[0])):
            rows = rows[:1] + rows[2:]              # a header that holds a number, a date or a version is a row of data
        elif len(rows) >= 2 and TABLE_RULE.match(rows[1]):
            cells = set(re.findall(r"[a-z]+", rows[0].lower()))
            if any(w in cells for w in EXAMPLE_TABLE_WORDS + ASSUMPTION_TABLE_WORDS):
                blocks.append(("title", 0, []))     # examples, or a register of assumptions: no row is an inability claim
                return
            rows = rows[2:]                         # the header is a title
        blocks.append(("rows", 0, [r.strip() for r in rows if not TABLE_RULE.match(r) and not _tally(r)]))

    for line in text.split("\n"):
        stripped = line.strip()
        if TABLE_ROW.match(line):
            flush_para()
            table.append(line)
            continue
        if table:
            flush_table()
        if stripped == MARK_BLOCK:
            flush_para()
            blocks.append(("code", 0, []))
        elif not stripped:
            flush_para()
        elif HEADING.match(line):
            flush_para()
            blocks.append(("title", 0, []))
        else:
            item = LIST_ITEM.match(line)
            if item:
                flush_para()
                kind[0], kind[1] = "item", len(line) - len(line.lstrip())
                para.append(line[item.end():])
            else:
                para.append(line)
    flush_para()
    if table:
        flush_table()
    return blocks


def sentences(text):
    """The sentences of one prepared text, in order. See the module text, point 2. A sentence that ends with a
    colon is not finished: it goes on in every list item under it, in every row of the table under it, or in
    the first sentence of the paragraph after it."""
    blocks = _blocks(text)
    out, carry = [], None                           # carry = (the unfinished sentence, "items" or "next", its indent)
    for n, (kind, indent, parts) in enumerate(blocks):
        parts = list(parts)
        following = blocks[n + 1] if n + 1 < len(blocks) else None
        if carry and carry[1] == "items" and (kind != "item" or indent <= carry[2]):
            carry = None                            # the list under the unfinished sentence has ended
        if kind == "code":
            if out:
                if len(out) >= 2 and _is_label(out[-1]):
                    label = out.pop()
                    out[-1] = out[-1] + " " + label
                out[-1] = out[-1] + " " + MARK_BLOCK
            continue
        if kind == "title":
            carry = None
            continue
        if carry:
            if kind == "rows":
                parts = [carry[0] + " " + p for p in parts] or [carry[0]]
            elif parts:
                parts[0] = carry[0] + " " + parts[0]
            if carry[1] == "next":
                carry = None
        if kind in ("para", "item") and parts and parts[-1].endswith(":") and following is not None:
            if following[0] == "item" and (kind == "para" or following[1] > indent):
                carry = (parts.pop(), "items", indent if kind == "item" else -1)
            elif following[0] == "rows" or (following[0] == "para" and kind == "para"):
                carry = (parts.pop(), "next", -1)
        out.extend(parts)
    return out


def _word_start(text, i):
    while i > 0 and (text[i - 1].isalnum() or text[i - 1] in "'_"):
        i -= 1
    return i


def _whose(before, claim=""):
    """Whose claim it is, from the words before it: "self", "we", "other", or "none" (no subject: the assistant's).
    `claim`: the claim's own words; a piece of work as subject is the assistant only with a verb of verifying."""
    rest = before.rstrip()
    for _ in range(SUBJECT_REACH):
        if not rest or rest[-1] in CLAUSE_OPENERS or rest[-1] in ".!?":
            return "none"
        m = re.search(r"[^\s]+$", rest)
        word = m.group(0).lower().strip("\"')]*_")
        base = word.split("'")[0] if "'" in word else word
        if base in SELF_SUBJECTS or base in SELF_NOUNS:
            return "we" if base == GENERAL_SUBJECT else "self"
        if base in WORK_NOUNS and _epistemic.search(claim) and _own_work(rest[:m.start()], base):
            return "self"
        if base in IMPERSONAL_SUBJECTS:
            return "none"
        if base in JOINING_WORDS:                   # "X did this and couldn't ...": whose claim is said in the clause before
            head = re.split(r"[.;:!?(]", rest[:m.start()])[-1].strip()
            if SELF_WORD.search(head):
                return "self"
            return "other" if OTHER_START.match(head) else "none"
        if word in SKIPPED_WORDS or base in SKIPPED_WORDS or (word.endswith("ly") and len(word) > 3):
            rest = rest[:m.start()].rstrip()
            continue
        return "other"
    return "other"


def _own_work(before, noun):
    """The subject that ends in `noun` (a noun of WORK_NOUNS) is the assistant's whole work: the noun stands in the
    subject's first WORK_SUBJECT_WORDS words with an owner (WORK_OWNERS) or a time word (WORK_TIMES) before it, and no
    word names another owner ("this week's run", "the scheduled weekly task"; not "your nightly job")."""
    head = re.split(r"[.;:!?(),|" + MARK_BLOCK + MARK_CODE + MARK_QUOTE + "]", before)[-1]
    words = [w.lower().strip("\"'*_") for w in head.split()] + [noun]
    if len(words) > WORK_SUBJECT_WORDS:
        return False
    if any(w in OTHER_OWNERS or (w.endswith("'s") and w not in TIME_POSSESSIVES) for w in words):
        return False
    return any(w in WORK_OWNERS or w in WORK_TIMES for w in words[:-1])


def _other_agent(sentence, at):
    """ "could not be verified by older Android clients": the phrase after "by" ends in a plural noun, so it names
    other agents. A time ("by midnight"), a means ("by any means") or the assistant ("by the assistant") does not."""
    m = PASSIVE_AGENT.match(sentence, at)
    if not m:
        return False
    last = m.group("agent").split()[-1].lower().strip("\"'*_")
    return (len(last) >= AGENT_PLURAL_MIN and last.endswith("s") and not last.endswith(AGENT_NOT_PLURAL_ENDS)
            and last not in NOT_AGENTS)


def find_claims(sentence):
    """[(start, end, words, family)] of the standing inability claims of one sentence, in order."""
    if QUESTION_END.search(sentence):
        return []
    found = []
    for family, pattern, personal in CLAIM_FAMILIES:
        for m in pattern.finditer(sentence):
            start = _word_start(sentence, m.start())
            before = sentence[max(0, start - BEFORE_REACH):start]
            said = _word_start(sentence, m.start("claim")) if "claim" in pattern.groupindex else start   # "... but COULDN'T"
            who = _whose(sentence[max(0, said - BEFORE_REACH):said], m.group(0)) if personal else "self"
            if who == "other":
                continue
            if (not personal or who == "none") and (CONDITION_BEFORE.search(before) or REPORTED_THAT.search(before)):
                continue
            if family in ("impossible", "know") and (CAUSATIVE_BEFORE.search(before) or HYPOTHETICAL_BEFORE.search(before)):
                continue
            if family in EVENT_FAMILIES and PERIOD_AFTER.match(sentence[m.end():m.end() + AFTER_REACH]):
                continue
            if family in EVENT_FAMILIES and _other_agent(sentence, m.end()):
                continue                            # "could not be verified by older clients": somebody else's inability
            if family == "know" and not (OWN_IN_CLAIM.search(m.group(0)) or (personal and who != "none")
                                         or PAST_STATE.search(sentence[max(0, start - PAST_REACH):m.end()])):
                continue
            if family == "modal-access" and who == GENERAL_SUBJECT and not PAST_MODAL.match(sentence, m.start()):
                continue
            if family == "not-verified" and not NOT_VERIFIED_IS_A_CLAIM:
                continue
            if family == "passive" and GENERIC_BEFORE.search(before):
                continue
            if family == "unverified" and (
                    NEGATED_CLAUSE.search(before) or ASSUMPTION_BEFORE.search(before) or SECTION_BEFORE.search(before)
                    or LABELLED_BEFORE.search(before) or ATTRIBUTIVE_BEFORE.search(before) or ENUMERATION_BEFORE.search(before)
                    or (m.group(0).lower() == "unconfirmed" and STATUS_BEFORE.search(before))):
                continue
            if (NEGATED_BEFORE.search(before) or CONDITIONAL_BEFORE.search(before) or REPORTED_BEFORE.search(before)
                    or SUPERSEDED_BEFORE.search(before) or MENTION_BEFORE.search(before) or REPORTED_OPEN.search(before)
                    or SUPERSEDED_AFTER.match(sentence[m.end():m.end() + AFTER_REACH])):
                continue
            found.append((start, m.end(), " ".join(sentence[start:m.end()].split()), family))
    found.sort()
    kept = []
    for c in found:
        if not kept or c[0] >= kept[-1][1]:
            kept.append(c)
    return kept


def _outside(sentence, claims):
    """The sentence without its claims and without the words that say what was not verified."""
    parts, at = [], 0
    for n, (start, end, _words, family) in enumerate(claims):
        label = LABEL_COLON.match(sentence, end)
        if label and family in SUBJECT_FIRST and re.search(r"[A-Za-z]", sentence[:start]):
            label = None                    # the colon opens the explanation, not the list of what was not verified
        if label and family in OWN_SUBJECT_FAMILIES:
            label = None                    # "Data for last week is not available: ...": the claim holds its subject
        begin = label.end() if label else end
        limit = claims[n + 1][0] if n + 1 < len(claims) else len(sentence)
        stop = OBJECT_END.search(sentence, begin, max(begin, limit))    # never past the next claim: one long sentence stays cheap
        if not CLAUSE_OBJECT.match(sentence, begin):
            # in the families whose subject stands first the words after the claim are no object: a means ends at once
            first = FIRST_WORD.match(sentence, begin)
            word = begin if family in SUBJECT_FIRST or not first else first.end()
            means = MEANS_END.search(sentence, word, max(word, limit))
            if means and (stop is None or means.start() < stop.start()):
                stop = means
        finish = min(stop.start() if stop else len(sentence), limit)
        parts.append(sentence[at:max(at, start)])
        at = max(at, finish)
    parts.append(sentence[at:])
    return " ".join(parts)


def _has_receipt(text):
    return bool(any(mark in text for mark in EVIDENCE_MARKS) or ATTEMPT.search(text) or FAILURE.search(text)
                or CHOICE.search(text))


def _searched_place(sentence, claims):
    """ "I couldn't find X in the repository": the search and where it was made are named in the claim itself."""
    return any(SEARCH_CLAIM.search(words) and SEARCHED_PLACE.match(sentence[end:end + AFTER_REACH]) for _start, end, words, _family in claims)


def bare_claim(text):
    """(claim words, sentence) of the first claim of a text that has no receipt, or None."""
    units = sentences(prepare(text))
    claims = [find_claims(u) for u in units]
    outside = [_outside(u, c) for u, c in zip(units, claims)]
    placed = [_searched_place(u, c) for u, c in zip(units, claims)]
    for n, unit in enumerate(units):
        if not claims[n]:
            continue
        reach = outside[n]
        if RECEIPT_SCOPE == SCOPE_NEIGHBOURS:
            reach = " ".join(outside[max(0, n - 1):n + 2])
        if not _has_receipt(reach) and not placed[n]:
            shown = unit
            for mark, word in ((MARK_BLOCK, "[block]"), (MARK_CODE, "[code]"), (MARK_QUOTE, "[quoted]")):
                shown = shown.replace(mark, word)
            return claims[n][0][2], " ".join(shown.split())
    return None


# ------------------------------------------------------------------------------------------------- the hook
def finish(answer):
    """Print the one answer (or nothing) and end with status 0. Only the first caller prints."""
    if not _answered.acquire(False):
        return
    try:
        if answer is not None:
            sys.stdout.write(json.dumps(answer) + "\n")
        sys.stdout.flush()
    except Exception:
        pass
    os._exit(0)


def on_deadline(*_unused):
    finish(None)                            # a Stop hook does not hold ordinary work on its own failure


def arm_deadline():
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, on_deadline)
        signal.alarm(HOOK_DEADLINE_SECONDS)
    else:
        timer = threading.Timer(HOOK_DEADLINE_SECONDS, on_deadline)
        timer.daemon = True
        timer.start()


def _look_up(name):
    """A tool call that only looks something up (NOTE_TOOLS, or an MCP tool whose name holds MCP_LOOKUP_WORDS)."""
    name = str(name or "")
    if name in NOTE_TOOLS:
        return True
    if not name.startswith(MCP_PREFIX):
        return False
    own = name.split("__")[-1]
    words = re.findall(r"[a-z]+", re.sub(r"([a-z])([A-Z])", r"\1 \2", own).lower())
    return any(w in MCP_LOOKUP_WORDS for w in words)


def judged_texts(model, after, last_message):
    """The texts after row `after` that the owner is asked to read, in order: the final answer (every text after the
    last tool call that is not a Skill call) and the texts before a card (back to the last tool call that is neither
    a Skill call nor a card), plus `last_message` when the record does not hold it. A text followed by an ordinary
    tool call is a working note and is not judged. With BLOCKED_STOP_ENDS_ANSWER, a text the assistant stopped on is
    an answer also when another Stop hook blocked that stop. RECEIPT_JUDGES = JUDGES_EVERY_TEXT judges every text."""
    if RECEIPT_JUDGES == JUDGES_EVERY_TEXT:
        return model.prose(after, last_message)
    judged, pending = [], []
    for e in model.evs:
        if e.i <= after:
            continue
        if e.kind in ("FEEDBACK", "STOP_BLOCKED") and BLOCKED_STOP_ENDS_ANSWER:
            judged, pending = judged + pending, []
        if e.i in model.run_starts or e.kind == "WAKE":
            judged, pending = judged + pending, []      # the session had stopped: what it said last was an answer
        if e.kind != "ASSISTANT":
            continue
        message = model.rows[e.i].get("message")
        content = message.get("content") if isinstance(message, dict) else None
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and str(block.get("text") or "").strip():
                pending.append(str(block["text"]))
            elif block.get("type") == "tool_use":
                if not _look_up(block.get("name")):
                    judged += pending           # no look-up follows it: a card, a task list, a file sent, a write ...
                pending = []                    # a working note: a look-up follows it
    judged += pending                           # the final answer
    last = last_message.strip() if isinstance(last_message, str) else ""
    if last and not any(last in t for t in judged):
        judged.append(last_message)             # held by the record only when a judged text holds it
    return judged


def decide(data):
    """The answer to one Stop input: a block, or None."""
    if not isinstance(data, dict):
        return None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import turngate
    path = data.get("transcript_path")
    rows = turngate.load(path) if isinstance(path, str) and path else []
    if not any(row.get("type") != "BAD" for row in rows):
        return None                         # no record to judge
    model = turngate.Model(rows)
    start = turngate.stop_span(model)[0] - 1        # the row before the stretch: the same stretch the other Stop gate judges
    retry = bool(data.get("stop_hook_active"))
    if retry and not model.feedback(start, None, retry):
        return None                         # the flag is set and the record shows no block: the one retry
    if len(model.feedback(start, turngate.RECEIPT_BLOCK_MARK, retry)) >= RECEIPT_MAX_BLOCKS:
        return None                         # this gate has spoken in this stretch
    for text in judged_texts(model, start, data.get("last_assistant_message")):     # the final answer too, when the record lacks it
        bare = bare_claim(text)
        if bare:
            return {"decision": "block", "reason": REASON % (bare[0], bare[1][:REASON_EXCERPT_CHARS])}
    return None


def main():
    return decide(json.loads(sys.stdin.read()))


if __name__ == "__main__":
    arm_deadline()
    try:
        answer = main()
    except BaseException:
        answer = None
    finish(answer)
    time.sleep(HOOK_DEADLINE_SECONDS)       # reached only while the deadline's timer thread is ending the hook
    os._exit(0)
