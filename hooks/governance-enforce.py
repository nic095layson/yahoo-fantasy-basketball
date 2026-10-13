#!/usr/bin/env python3
"""Stop hook: if the turn answered governed-class work AND no governor Skill loaded for it, BLOCK once
and force the load. Single retry (stop_hook_active) => loop-safe. Fails open on every error.

This is the mechanism behind the kit's promise that "the core governors run on every session": a
promise with no mechanism was INC-2026-10-13-01. Validated form (2026-07-15, phase 2b A/B): every
governed case loaded the governor 3/3 under enforcement vs 0/3 without; both should-not cases silent.

Rebuilt 2026-10-13 on hooks/govclass.py (shared with the trigger) and made robust to user messages
whose content is a list of blocks, which is how cloud sessions record them.

What counts as "loaded": a Skill tool call this turn whose input names the governor — including a
synced copy such as "anthropic-skills:plan-gate". Governor text merely re-attached after a compaction
does NOT count (it is bound to an earlier task); that distinction is the gauntlet skill's rule, and
this hook enforces it by looking only at Skill calls after the latest owner message.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from govclass import classify, governors, ENFORCED
except Exception:
    sys.exit(0)
try:
    from govclass import HARNESS_MARKERS
except Exception:  # older classifier without the constant: same markers, kept in step by the fixture
    HARNESS_MARKERS = ("[SYSTEM NOTIFICATION", "<task-notification>", "<wake ", "<agent-message", "<webhook-payload")


def user_text(msg):
    """Plain text of a user message, or None when it carries no owner text (tool results etc.)."""
    c = msg.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        texts = [b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(t for t in texts if t) or None
    return None


try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if data.get("stop_hook_active"):
    sys.exit(0)  # already forced one retry -> allow (loop-safe)
tp = data.get("transcript_path")
if not tp or not os.path.exists(tp):
    sys.exit(0)

lines = []
try:
    with open(tp, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                lines.append(json.loads(raw))
            except Exception:
                pass
except Exception:
    sys.exit(0)

prompt, li = None, -1
for i, d in enumerate(lines):
    if d.get("type") != "user":
        continue
    # Harness-injected user entries (loaded skill text, hook feedback, compaction summaries) are
    # marked isMeta / isCompactSummary. They are not the owner's request: in the 2026-10-13 live
    # A/B the gate took a loaded skill's own text as "the prompt", put the Skill call before it,
    # and blocked a compliant turn. Only un-marked user text counts.
    if d.get("isMeta") or d.get("isCompactSummary"):
        continue
    m = d.get("message") or {}
    if not isinstance(m, dict):
        continue
    t = user_text(m)
    # Harness-generated user turns (background-task notifications, wake envelopes, subagent hand-backs)
    # are not the owner's request either. Before 2026-10-13 they were taken as "the prompt", classified
    # as nothing, and let a governed, unloaded turn through whenever a background task finished
    # mid-turn (reproduced red-first, results/2026-10-13/system-validation/).
    if t and any(mk in t for mk in HARNESS_MARKERS):
        continue
    if t and not t.startswith("GOV-ENFORCE") and not t.startswith("Stop hook feedback"):
        prompt, li = t, i
if not prompt:
    sys.exit(0)

classes = [c for c in classify(prompt) if c in ENFORCED]
if not classes:
    sys.exit(0)  # not governed, or advisory-only -> allow
needed = set(governors(classes))

loaded = set()
for d in lines[li:]:
    if d.get("type") != "assistant":
        continue
    m = d.get("message") or {}
    for b in (m.get("content") or []) if isinstance(m, dict) else []:
        if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
            inp = json.dumps(b.get("input", {}))
            for g in ("plan-gate", "adversarial-verify", "scope-fence"):
                if g in inp:
                    loaded.add(g)

if loaded & needed:
    sys.exit(0)  # complied

first = governors(classes)[0]
reason = ("GOV-ENFORCE: this is governed work (" + ", ".join(governors(classes)) + ") and you finished "
          "WITHOUT loading it. Load " + first + " with the Skill tool now, follow its procedure, and revise "
          "your answer before finishing. Governor text already in your context from before a compaction "
          "does not count: it was loaded for an earlier task.")
print(json.dumps({"decision": "block", "reason": reason}))
