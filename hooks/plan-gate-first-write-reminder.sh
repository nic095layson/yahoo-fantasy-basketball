#!/usr/bin/env bash
# plan-gate-first-write-reminder — mechanical trigger aid for the plan-gate skill.
# Fires once per session, at the FIRST write-class tool use (Write|Edit|NotebookEdit):
# injects a one-line plan reminder into model context at the moment the DEAD-1
# lesson class showed description-based triggering misses — when the model is
# already hands-on and about to mutate state without a written plan.
# Advisory, not blocking: a hook cannot judge triviality, and a hard block on
# every edit would violate the anti-ceremony invariant (architecture-contract,
# invariant 5). Pattern and sentinel mechanics mirror scope-fence-reminder.sh
# (verified live 2026-07-12). Shipped 2026-08-03, UNMEASURED — A/B plan:
# experiments/hypothesis-2026-08-03-hook-enforcement.md.
set -u
input=$(cat)
sid=$(printf '%s' "$input" | /usr/bin/jq -r '.session_id // "nosession"' 2>/dev/null || echo nosession)
sentinel="${TMPDIR:-/tmp}/plan-gate-reminder-${sid}"
if [ ! -e "$sentinel" ]; then
  touch "$sentinel"
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"Plan check (plan-gate skill): first file write of this session. If the task is non-trivial (multi-step, costly if wrong, or relied upon) and no goal + success criteria were written before this edit, run the plan-gate skill now — pre-committed criteria are the finish line; criteria written afterward are a rationalization. Trivial one-step edits: proceed, no ceremony. This reminder fires once per session."},"suppressOutput":true}'
fi
exit 0
