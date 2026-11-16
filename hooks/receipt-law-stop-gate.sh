#!/usr/bin/env bash
# receipt-law-stop-gate: the wired entry point of the receipt gate. The rule itself is in receiptlaw.py, beside
# this file; this script only runs it.
#
# Event: Stop. Fires when the assistant is about to end its turn.
#
# The rule (adversarial-verify rule 6): "couldn't verify", "unable to confirm", "not available", "no data
# exists" and their variants, contractions included, may be written only when the same sentence names what was
# attempted and how it failed. With no attempt to cite, the honest wording is "did not check". An inability
# claim with no receipt reads as a limit when it may be a decision (INC-9).
#
# What the gate does (all of it in receiptlaw.py; hooks/README.md states the rule and its limits):
#   - it judges what the assistant said since the owner's latest message or the latest completed stop, the
#     same rows the other Stop gate judges (turngate.py), plus the final answer the program hands over;
#   - a claim needs an attempt or a failure mode in its own sentence, outside the words that say what was not
#     verified; a quoted command or error in that sentence is a receipt;
#   - it does not fire on words inside code, a block quote or quotation marks, on a question, a negation, a
#     conditional, a sentence that reports what a tool or a person said, or a table of examples;
#   - it blocks at most once in a stretch, counted from the record (no state file anywhere).
#
# History of the design, kept because the first version was wrong (2026-08-12): the gate first passed any turn
# in which some tool had run. The founding session ran three searches, stopped, and then wrote "couldn't
# verify" about eight items it had never touched. "Some tool ran" proves nothing about a specific claim: the
# receipt is owed per claim, in the claim's sentence. Rebuilt 2026-11-15 after the audit of 2026-11-12 (the
# contraction "can't" was never matched; any of about 25 words within 400 characters counted as the receipt).
#
# Fails OPEN, always: python3 missing, receiptlaw.py missing, an input or a record that cannot be read, an
# error, the gate's own deadline. Every path of this script ends with exit status 0.
#
# Wiring (checked 2026-11-15): this repository's .claude/settings.json runs it in the Stop group, after
# governance-enforce.py; the plugin (plugin/core-governance/hooks/hooks.json) runs its own copy through
# run-unless-project-wired.sh. To wire it by hand at user scope, copy this file, receiptlaw.py and turngate.py
# into one folder and add to ~/.claude/settings.json:
#   {"hooks":{"Stop":[{"hooks":[{"type":"command","command":"bash ~/.claude/hooks/receipt-law-stop-gate.sh","timeout":10}]}]}}
# Tests: bash hooks/selftest-receipt-law.sh (15 cases); python3 hooks/selftest-turn-gates.py RL (the table).
#
# Surface: Claude Code only. claude.ai has no hook layer; there the receipt law is carried by the
# custom-instructions block (instructions/claude-ai-custom-instructions.md).
here="${BASH_SOURCE[0]:-$0}"
case "$here" in
  */*) here="${here%/*}" ;;
  *)   here="." ;;
esac
python3 "$here/receiptlaw.py" 2>/dev/null     # prints one JSON object (a block) or nothing
exit 0                                        # whatever happened above: a Stop hook of this kind never fails a stop
