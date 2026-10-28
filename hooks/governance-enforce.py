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

# F1 (2026-10-29): gate on what the turn DID. If it took an outward action (commit, push, PR create/
# update/merge, scheduled-task change), plan-gate must have loaded before the first such action and
# adversarial-verify somewhere in the turn — whatever the prompt said. (First draft required
# adversarial-verify AFTER the first outward action; the replay control "verify, then commit and push"
# — 2026-10-21 17:13 — was blocked by it, so the rule was narrowed, not the fixture loosened.) Every governor miss in the 2026-10-28 session
# audit was a short follow-up turn the prompt classifier does not match ("Continue", "proceed").
# Pre-registered: experiments/hypothesis-2026-10-29-turn-gates.md.
try:
    import turngate
    _li = turngate.owner_index(lines)
    if _li >= 0:
        _ev = turngate.events(lines, _li)
        _first = next((k for k, (kind, b) in enumerate(_ev) if kind == "tool" and turngate.is_outward(b)), None)
        if _first is not None:
            _pg = any(kind == "tool" and turngate.skill_name(b) == "plan-gate" for kind, b in _ev[:_first])
            _av = any(kind == "tool" and turngate.skill_name(b) == "adversarial-verify" for kind, b in _ev)
            if not (_pg and _av):
                _miss = [g for g, ok in (("plan-gate (before the first outward action)", _pg),
                                          ("adversarial-verify", _av)) if not ok]
                print(json.dumps({"decision": "block", "reason": (
                    "GOV-ENFORCE: this turn took an outward action (commit, push, PR or merge) without "
                    + " and ".join(_miss) + ". Load the missing governor with the Skill tool now and follow it."
                    + (" The plan comes after the action this time: say so plainly to the owner, then state"
                       " the goal and what was done." if not _pg else "")
                    + " This applies however short the owner's message was ('continue', 'proceed').")}))
                sys.exit(0)
except SystemExit:
    raise
except Exception:
    pass  # fail open: the prompt-class gate below still runs

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

# What must have loaded: the PRIMARY governor of every enforced class the prompt matched (the first in
# its GOVERNORS_FOR tuple). Before 2026-10-19 any one needed governor passed, so a dispute — which needs
# adversarial-verify's assessment — passed on a scope-fence load alone (red-team attack G4).
try:
    from govclass import GOVERNORS_FOR
    needed = {GOVERNORS_FOR[c][0] for c in classes}
except Exception:
    needed = set(governors(classes))

loaded, tools_ran, said = set(), 0, []
for d in lines[li:]:
    if d.get("type") != "assistant":
        continue
    m = d.get("message") or {}
    for b in (m.get("content") or []) if isinstance(m, dict) else []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            said.append(b.get("text") or "")
        if b.get("type") != "tool_use":
            continue
        if b.get("name") == "Skill":
            # Exact match on the Skill NAME (after any scope prefix). Before 2026-10-19 a substring
            # match on the whole input let a call whose ARGS merely mentioned a governor count as
            # loading it (red-team attack G3).
            inp = b.get("input") or {}
            name = str(inp.get("skill") or "").split(":")[-1].strip()
            if name in ("plan-gate", "adversarial-verify", "scope-fence"):
                loaded.add(name)
        else:
            tools_ran += 1

if needed <= loaded:
    sys.exit(0)  # complied

# Trivia allowance (D-SV-5, 2026-10-19), REVIEW-ONLY: a review-class turn that ran no tool and
# answered in under TRIVIA_MAX_CHARS characters did no governed work — "quick sanity check: 2+2=4,
# right?" was blocked 2/2 live and the forced load added nothing. Scoped to {review} alone: a dispute,
# build or analysis answered short without tools is the INC-2026-10-13-01 shape (acquiescing without
# the assessment), not trivia. TRIVIA_MAX_CHARS is hand-set (uncalibrated, registry
# results/2026-10-19/system-red-team). Any tool call or a longer answer re-arms the gate.
TRIVIA_MAX_CHARS = 400
if set(classes) == {"review"} and tools_ran == 0 and len("".join(said).strip()) < TRIVIA_MAX_CHARS:
    sys.exit(0)

first = sorted(needed - loaded)[0]
reason = ("GOV-ENFORCE: this is governed work (" + ", ".join(sorted(needed)) + ") and you finished "
          "WITHOUT loading " + ("it" if len(needed) == 1 else "all of it") + ". Load " + first +
          " with the Skill tool now, follow its procedure, and revise "
          "your answer before finishing. Governor text already in your context from before a compaction "
          "does not count: it was loaded for an earlier task.")
print(json.dumps({"decision": "block", "reason": reason}))
