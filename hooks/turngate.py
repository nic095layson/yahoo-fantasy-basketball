#!/usr/bin/env python3
"""Shared helpers for the turn gates (2026-10-29): what a turn DID, not how its prompt was worded.

Used by governance-enforce.py (Stop, F1) and turn-gates-pretool.py (PreToolUse, F2 merge word and F3
plan shown). Why: the 2026-10-28 compliance audit of a two-week session found every governor miss in a
short follow-up turn ("Continue", "proceed", "re-pasted instructions complete") that the prompt
classifier does not match, so the prompt-class gate never looked at it. Pre-registered in
experiments/hypothesis-2026-10-29-turn-gates.md; pinned by hooks/selftest-turn-gates.py.

Everything here reads the transcript and fails open: an unreadable transcript yields "no turn".
"""
import json
import os
import re

try:
    from govclass import HARNESS_MARKERS
except Exception:
    HARNESS_MARKERS = ("[SYSTEM NOTIFICATION", "<task-notification>", "<wake ", "<agent-message", "<webhook-payload",
                       "<command-name>", "<local-command-stdout>", "<local-command-caveat>")

GOVERNORS = ("plan-gate", "adversarial-verify", "scope-fence")

# OUTWARD actions (F1): leave the machine or change shared state. Edits alone are not outward; they reach
# anyone only through a commit, push or PR, which is outward.
OUTWARD_TOOL_SUFFIXES = ("merge_pull_request", "create_pull_request", "update_pull_request", "push_files",
                         "create_or_update_file", "delete_file", "create_trigger", "update_trigger", "delete_trigger")
OUTWARD_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?(commit|push)\b|\bgh\s+pr\s+(create|merge)\b")

# WRITE actions (F3): the first change of state, local or outward.
WRITE_TOOLS = ("Edit", "Write", "NotebookEdit")
WRITE_BASH = re.compile(r"\bgit\s+(-C\s+\S+\s+)?checkout\s+(-q\s+)?-[bB]\b|\bsed\s+-i\b")

MERGE_BASH = re.compile(r"\bgh\s+pr\s+merge\b")
SCRATCH = ("/tmp/",)

PLAN_MARK = re.compile(r"\bGoal\b")


def load(path):
    rows = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                raw = raw.strip()
                if raw:
                    try:
                        rows.append(json.loads(raw))
                    except Exception:
                        pass
    except Exception:
        return []
    return rows


def _text(msg):
    c = (msg or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text") or None
    return None


def owner_index(rows):
    """Index of the owner's latest message, or -1. Harness-written user rows are skipped."""
    li = -1
    for i, d in enumerate(rows):
        if d.get("type") != "user" or d.get("isMeta") or d.get("isCompactSummary"):
            continue
        t = _text(d.get("message"))
        if not t or any(m in t for m in HARNESS_MARKERS):
            continue
        if t.startswith(("GOV-ENFORCE", "Stop hook feedback")):
            continue
        li = i
    return li


def owner_text(rows, li):
    return _text(rows[li].get("message")) if li >= 0 else ""


def events(rows, start):
    """(kind, payload) after `start` in order: ("text", str), ("tool", block), ("answer", str)."""
    out = []
    for d in rows[start + 1:]:
        m = d.get("message") or {}
        c = m.get("content") if isinstance(m, dict) else None
        if d.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and (b.get("text") or "").strip():
                    out.append(("text", b["text"]))
                elif b.get("type") == "tool_use":
                    out.append(("tool", b))
        elif d.get("type") == "user" and isinstance(c, list):
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    cc = b.get("content")
                    t = cc if isinstance(cc, str) else " ".join(x.get("text", "") for x in (cc or []) if isinstance(x, dict))
                    if "questions have been answered" in t:   # an AskUserQuestion answer: the owner's own click
                        out.append(("answer", t))
    return out


def skill_name(block):
    if block.get("name") != "Skill":
        return None
    return str((block.get("input") or {}).get("skill") or "").split(":")[-1].strip()


def _cmd(block):
    return str((block.get("input") or {}).get("command") or "")


def _scratch_only(block):
    p = str((block.get("input") or {}).get("file_path") or (block.get("input") or {}).get("notebook_path") or "")
    return any(p.startswith(s) for s in SCRATCH)


def is_outward(block):
    name = str(block.get("name") or "")
    if name.endswith(OUTWARD_TOOL_SUFFIXES):
        return True
    return name == "Bash" and bool(OUTWARD_BASH.search(_cmd(block)))


def is_write(block):
    name = str(block.get("name") or "")
    if name in WRITE_TOOLS:
        return not _scratch_only(block)
    if name == "Bash" and WRITE_BASH.search(_cmd(block)):
        return True
    return is_outward(block)


def is_merge(block):
    name = str(block.get("name") or "")
    return name.endswith("merge_pull_request") or (name == "Bash" and bool(MERGE_BASH.search(_cmd(block))))


def merge_target(block):
    inp = block.get("input") or {}
    n = inp.get("pullNumber") or inp.get("pull_number")
    if n is None and block.get("name") == "Bash":
        m = re.search(r"\bgh\s+pr\s+merge\s+#?(\d+)", _cmd(block))
        n = m.group(1) if m else None
    return str(n) if n is not None else None


MERGE_WORD = re.compile(r"\bmerg(e|ed|ing)\b", re.I)


def merge_authorized(rows, li, block):
    """F2: the owner's word for THIS merge — in their latest message, in a click after it, or in the
    assistant's last text before their message together with the PR's number."""
    if li < 0:
        return False
    if MERGE_WORD.search(owner_text(rows, li) or ""):
        return True
    for kind, payload in events(rows, li):
        if kind == "answer" and MERGE_WORD.search(payload):
            return True
    target = merge_target(block)
    for d in reversed(rows[:li]):
        if d.get("type") != "assistant":
            continue
        t = _text(d.get("message")) or ""
        if not t.strip():
            continue
        return bool(MERGE_WORD.search(t) and target and re.search(r"#\s?" + re.escape(target) + r"\b", t))
    return False
