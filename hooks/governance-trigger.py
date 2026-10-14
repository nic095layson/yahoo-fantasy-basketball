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
classes = classify(prompt)
if not classes:
    sys.exit(0)

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
    sys.exit(0)
parts.append("If on inspection it is genuinely trivial, say so in one line and skip.")

print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                         "additionalContext": " ".join(parts)}}))
