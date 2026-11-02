#!/usr/bin/env python3
"""UserPromptSubmit trigger (load-only, NO receipt ask — nothing to confabulate; INC-13).

Classifies the owner's message with hooks/govclass.py and, when it is governed work, injects one
context line telling the model which governor to LOAD with the Skill tool before answering.
Advisory: it never blocks. The Stop hook (governance-enforce.py) is the blocking half.

Rebuilt 2026-10-13 on the shared classifier after INC-2026-10-13-01 (three of the four owner messages
in the incident were silent under the 2026-07-15 patterns). Fails open on any error.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from govclass import classify, governors
except Exception:
    sys.exit(0)
try:
    from govclass import cue
except Exception:  # older classifier without the cue tier
    def cue(_):
        return False

MESSAGES = {
    "dispute": (
        "Governance auto-trigger: the owner is questioning or disputing the work. A question gets an "
        "assessment, not a fix. Load adversarial-verify (re-examine the work against the objection) and "
        "scope-fence (no fix, candidate, rewrite or dry run unless the owner asks for one) with the Skill "
        "tool before answering. State the data window, sample and method choices you will use in one line "
        "BEFORE running them, not in a tool label."
    ),
    "requirement": (
        "Governance note (scope-fence rule 4): a stated requirement is not a build order. Note it, apply it "
        "to the work already requested, and do not build something new to satisfy it unless asked."
    ),
}

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "").strip()


def card_reminder():
    """Decision-cards advisory (2026-11-02): the previous assistant turn posed a decision as a list line
    with "(Recommended)" and asked no AskUserQuestion. In the Solo-Leveling session 5 of 13 decisions went
    out as text lists, each with a stated default; the owner's rule now says a default goes first on the
    card, it is not an exemption. Advisory: never blocks. Fails open (returns "")."""
    try:
        import re
        import turngate
        rows = turngate.load(data.get("transcript_path") or "")
        li = turngate.owner_index(rows)
        if li < 0:
            return ""
        # The transcript may or may not already hold this prompt: step back past it if it does.
        if (turngate.owner_text(rows, li) or "").strip() == prompt and prompt:
            li_prev = turngate.owner_index(rows[:li])
            seg = turngate.events(rows[:li], li_prev) if li_prev >= 0 else []
        else:
            seg = turngate.events(rows, li)
        if any(kind == "tool" and b.get("name") == "AskUserQuestion" for kind, b in seg):
            return ""
        line = re.compile(r"^\s*(\d+[.)]|[-*•])\s.*\(Recommended\)", re.M)
        if any(kind == "text" and line.search(p) for kind, p in seg):
            return ("Decision-cards reminder (owner rule 4, advisory): your previous reply posed a decision as a "
                    "'(Recommended)' text list without a clickable card. If that decision is still open and the "
                    "owner's message does not settle it, put the decision as a clickable card (AskUserQuestion), "
                    "default first as (Recommended). A default is not an exemption. Ignore this in an unattended "
                    "scheduled run, where nobody can click.")
    except Exception:
        pass
    return ""


CARD = card_reminder()


def emit(parts):
    parts = [p for p in parts if p]
    if parts:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": " ".join(parts)}}))
    sys.exit(0)


classes = classify(prompt)
if not classes:
    # The advisory cue tier (2026-10-19, D-SV-3 option c): the patterns catch 14/36 governed owner
    # prompts on the sealed set, so prompts they miss get one advisory line. Never enforced.
    emit([(
        "Governance cue (advisory, from your operating rules): if this request is non-trivial work the "
        "owner will rely on, load the governor it calls for with the Skill tool before acting — plan-gate "
        "before building, adversarial-verify before delivering or when checking, scope-fence when the ask "
        "could widen. A trivial or conversational message: answer directly, no ceremony.") if cue(prompt) else "",
        CARD])

parts = []
if "dispute" in classes:
    parts.append(MESSAGES["dispute"])
else:
    gov = governors([c for c in classes if c != "requirement"])
    if gov:
        names = " and ".join(gov)
        parts.append(
            f"Governance auto-trigger (from your operating rules): this is governed work ({names}). "
            f"Load {names} with the Skill tool and follow its procedure BEFORE you produce the answer."
        )
if "requirement" in classes:
    parts.append(MESSAGES["requirement"])
if not parts:
    emit([CARD])
# The skip clause stays OFF build-class prompts: in 4/4 live build runs it was taken before the first
# write, so the governor loaded only after the Stop block (red-team 2026-10-19, runs L1/L8). Plan-gate's
# own triage rule is the anti-ceremony valve once it loads. Other classes keep the clause: with it, the
# Stop gate's trivia allowance, and invariant 5, a trivial review is answered in one line, not ritualized.
if "build" not in classes:
    parts.append("If on inspection it is genuinely trivial, say so in one line and skip.")

emit(parts + [CARD])
