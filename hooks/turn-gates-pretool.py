#!/usr/bin/env python3
"""PreToolUse turn gates: the merge gate and the plan-shown advisory.

Merge gate. A call that merges a pull request, switches auto-merge on, or pushes to a default branch is denied
unless the owner's word for THAT pull request (or that branch) stands in the current window: a click on a card
that names it, or a typed order with its number. The word covers only what it names and ends when the assistant
stops. In a scheduled run such a call is always denied, for the routes the gate reads (a file run directly whose
first line names a program other than a shell, such as `./tool.py`, is not read: a stated limit, as `python3
FILE` is). The rule itself is turngate.merge_decision.

Plan-shown advisory. After a plan-gate load, the first real write is preceded by one reminder when the record
holds no plan text since the load. Advisory only: the record does not keep every message.

Helper agents. An outward call a helper agent makes is noted in a small ledger so that the Stop gate can count
it: the helper's own rows are not in the record this hook is handed.

Which way a failure goes. An input that cannot be read, a record that cannot be read, an error in this file or
in turngate.py, and this hook's own deadline all DENY a call that is, or crudely looks like, a merge route (a
merge, or a push that names a default branch or every branch), and let every other call through. Every path ends with exit status 0 and prints one JSON object or nothing: the
program lets a call through when a hook exits with an error or is cut off, so neither may happen here.
"""
import json
import os
import re
import signal
import sys
import threading
import time

HOOK_DEADLINE_SECONDS = 8           # under the wired timeout of 10 s: a hook the program cuts off lets the call through
CRUDE_MERGE = re.compile(r"merge_pull_request|enable_pr_auto_merge|/pulls/\d+/merge\b|mergePullRequest|"
                         r"enablePullRequestAutoMerge|enqueuePullRequest")
CRUDE_MERGE_WORDS = (("gh", "pr", "merge"),)        # the words of one command, in this order
# A push that names a default branch, or every branch: the same class as a merge (the owner's decision D3).
CRUDE_PUSH_WORDS = (("git", "push", "main"), ("git", "push", "master"), ("git", "push", "all"),
                    ("git", "push", "mirror"), ("git", "push", "branches"))
CRUDE_SPLIT = re.compile(r"[\n|;&]")
CRUDE_WORD = re.compile(r"\w+")
REASON_GATE_ERROR = ("TURN-GATE (merge word) [gate-error]: the gate %s, and neither a merge nor a push to a default "
                     "branch is let through on an error. Ask the owner with a card that names the pull request (or "
                     "the branch), then try again; if this repeats, tell the owner that the gate is failing.")
ERROR_INPUT = "could not read this call"
ERROR_MODULE = "could not load its own rules (turngate.py)"
ERROR_INTERNAL = "failed while judging this call"
ERROR_DEADLINE = "ran out of time while judging this call"
ADVISORY = ("TURN-GATE (plan shown, advisory): plan-gate is loaded and the session record holds no plan text since. "
            "The record does not keep every message, so this may be a false alarm: if you have shown the owner the "
            "compact plan (Goal · Method / parameters · Done when · If it breaks), carry on; if not, show it before "
            "this write.")

_state = {"crude": False, "gated": None}    # what is known about the call so far, for the error paths
_answered = threading.Lock()                # taken by whoever prints the one answer


def deny(reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": reason}}


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


def crude_merge(text):
    """Could this text be a merge route (a merge, or a push that names a default branch or every branch)? The
    pattern anywhere, or the words of one list in order inside one command. One pass over the words, so that no
    text can keep this screen busy. Crude on purpose: `git push origin main-fix` is taken for a push to main."""
    if CRUDE_MERGE.search(text):
        return True
    for segment in CRUDE_SPLIT.split(text):
        words = CRUDE_WORD.findall(segment)
        for wanted in CRUDE_MERGE_WORDS + CRUDE_PUSH_WORDS:
            at = -1
            try:
                for w in wanted:
                    at = words.index(w, at + 1)
            except ValueError:
                continue
            return True
    return False


def merge_route():
    """Is the call a merge route, as far as is known: its classification once there is one, else the crude screen."""
    return _state["crude"] if _state["gated"] is None else _state["gated"]


def on_deadline(*_unused):
    finish(deny(REASON_GATE_ERROR % ERROR_DEADLINE) if merge_route() else None)


def arm_deadline():
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, on_deadline)
        signal.alarm(HOOK_DEADLINE_SECONDS)
    else:                                   # no alarm on this system: a timer thread ends the hook instead
        timer = threading.Timer(HOOK_DEADLINE_SECONDS, on_deadline)
        timer.daemon = True
        timer.start()


def advisory(turngate, model, data):
    """One reminder per plan-gate load, before the first real write after it, when no plan text is on record."""
    loads = [(i, k) for i, k, governor in model.loads(model.gov_start) if governor == turngate.PLAN_GOVERNOR]
    if not loads:
        return None
    row, block = loads[-1]
    if any(turngate.PLAN_MARK.search(text) for text in model.prose(row)):
        return None
    load_id = next((tid for tid, use in model.uses.items() if use[0] == row and use[1] == block), "%d:%d" % (row, block))
    marker = turngate.advisory_marker(str(data.get("session_id") or ""), load_id)
    try:
        if os.path.exists(marker):
            return None
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        open(marker, "w").close()
    except Exception:
        return None                         # a reminder that cannot be marked as given would repeat on every write
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": ADVISORY}}


def judge(turngate, data, name, inp):
    cwd = data.get("cwd") if isinstance(data.get("cwd"), str) else None
    acts, _parsed = turngate.classify_call(name, inp, cwd)
    _state["gated"] = any(a.kind in turngate.MERGE_GATED_KINDS for a in acts)
    looked_at = turngate.WRITE_KINDS + turngate.MERGE_GATED_KINDS
    if not any(a.kind in looked_at or a.note == turngate.NOTE_BRANCH_UNKNOWN for a in acts):
        return None                         # nothing these gates look at: the record is not read
    path = data.get("transcript_path")
    rows = turngate.load(path) if isinstance(path, str) and path else []
    model = turngate.Model(rows) if rows else None
    agent = data.get("agent_id") or None
    call_id = data.get("tool_use_id") if isinstance(data.get("tool_use_id"), str) else None
    allow, _code, reason = turngate.merge_decision(model, acts, agent, call_id)
    if not allow:
        return deny(reason)
    if agent:                               # a helper's call: note it for the Stop gate; no advisory, because
        counted = sorted(set(a.kind for a in acts if a.kind in turngate.F1_COUNTED_KINDS))    # its plan is not in this record
        if counted and model is not None:
            try:
                turngate.ledger_add(path, len(rows), str(agent), str(name), counted)
            except Exception:
                pass                        # no note: nothing is counted and nothing is blocked
        return None
    return advisory(turngate, model, data) if model is not None else None


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("the input is not an object")
    except Exception:
        return deny(REASON_GATE_ERROR % ERROR_INPUT) if crude_merge(raw or "") else None
    name = data.get("tool_name")
    inp = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    _state["crude"] = crude_merge(str(name or "")) or crude_merge(str(inp.get("command") or ""))
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import turngate
    except Exception:
        return deny(REASON_GATE_ERROR % ERROR_MODULE) if _state["crude"] else None
    try:
        return judge(turngate, data, name, inp)
    except Exception:
        return deny(REASON_GATE_ERROR % ERROR_INTERNAL) if merge_route() else None


if __name__ == "__main__":
    arm_deadline()
    try:
        answer = main()
    except BaseException:
        answer = deny(REASON_GATE_ERROR % ERROR_INTERNAL) if merge_route() else None
    finish(answer)
    time.sleep(HOOK_DEADLINE_SECONDS)       # reached only while the deadline's timer thread is printing its answer
    os._exit(0)
