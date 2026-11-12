#!/usr/bin/env python3
"""PreToolUse turn gates (2026-10-29). Denies, before the tool runs:

F2 — a PR merge (`*merge_pull_request`, `gh pr merge`) without the owner's word for it: "merge" in the
     owner's latest message, in a clickable answer after it, or in the assistant's last text before that
     message together with this PR's number. The 2026-10-28 audit found PR #26 merged on "I've uploaded,
     proceed" while the assistant's own note said it was awaiting the owner's call.
F3 — the first write after a plan-gate load when no plan was shown: once plan-gate is loaded this turn,
     a write-class action (Edit/Write/NotebookEdit outside /tmp, `git checkout -b`, `sed -i`, commit,
     push, PR create/update/merge) waits for an assistant text containing "Goal". A turn that never
     loaded plan-gate is untouched, so trivia carries no ceremony. Two turns in the audit loaded
     plan-gate and wrote with no plan in the transcript between the load and the first write.

Fails open on every error. Pre-registered: experiments/hypothesis-2026-10-29-turn-gates.md;
pinned by hooks/selftest-turn-gates.py.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    import turngate
    data = json.load(sys.stdin)
    block = {"name": data.get("tool_name"), "input": data.get("tool_input") or {}}
    tp = data.get("transcript_path")
    if not tp or not os.path.exists(tp):
        sys.exit(0)
    if not (turngate.is_merge(block) or turngate.is_write(block)):
        sys.exit(0)
    rows = turngate.load(tp)
    oi = turngate.owner_index(rows)
    li = turngate.turn_start(rows)   # 2026-11-04: a scheduled run is a turn of its own
    if li < 0:
        sys.exit(0)

    # A scheduled run carries no owner message, so it carries no owner word to merge: it never merges.
    if turngate.is_merge(block) and li > oi:
        target = turngate.merge_target(block)
        deny("TURN-GATE (merge word): a scheduled run never merges" + (f" PR #{target}" if target else "")
             + ". Record it as an open decision in the run's report; the owner merges on their own word.")
    if turngate.is_merge(block) and not turngate.merge_authorized(rows, li, block):
        target = turngate.merge_target(block)
        deny("TURN-GATE (merge word): the owner has not said to merge" + (f" PR #{target}" if target else "")
             + " in this turn. Ask with a clickable choice (AskUserQuestion) and merge only on their answer.")

    ev = turngate.events(rows, li)
    loads = [k for k, (kind, b) in enumerate(ev) if kind == "tool" and turngate.skill_name(b) == "plan-gate"]
    if loads and turngate.is_write(block):
        last = loads[-1]
        shown = any(kind == "text" and turngate.PLAN_MARK.search(p) for kind, p in ev[last + 1:])
        # ADVISORY, not deny (2026-10-29): the transcript does not record every assistant text — 7 of 13
        # texts written in the authoring turn were absent from it — so "no plan in the transcript" cannot
        # prove "no plan shown", and a deny could block an honest plan, repeatedly. One reminder per
        # plan-gate load; the sentinel keys it to the session, the owner message and the load.
        if not shown:
            sid = str(data.get("session_id") or "nosession")
            mark = os.path.join(os.environ.get("TMPDIR", "/tmp"), f"turn-gate-plan-{sid}-{li}-{last}")
            if not os.path.exists(mark):
                open(mark, "w").close()
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": (
                    "TURN-GATE (plan shown, advisory): plan-gate is loaded but no plan appears in the transcript "
                    "since. If you have not shown the owner the compact plan (Goal · Method / parameters · Done "
                    "when · If it breaks), stop and show it before this write.")}}))
except SystemExit:
    raise
except Exception:
    pass
sys.exit(0)
