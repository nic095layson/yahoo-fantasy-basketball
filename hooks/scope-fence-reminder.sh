#!/usr/bin/env bash
# scope-fence-reminder — mechanical trigger aid for the scope-fence skill.
# Fires once per session, at the FIRST file edit: injects a one-line scope
# reminder into model context at exactly the moment description-based
# triggering was measured to miss (~60-67%, nic095layson/claude-core-skills
# campaign, 2026-07-11). Silent on every subsequent edit in the session.
set -u
input=$(cat)
# python3, not jq: the hard-coded /usr/bin/jq made every session on a jq-elsewhere machine share one
# "nosession" sentinel, so the reminder fired once per machine (red-team 2026-10-19, attack M3; D-GF-8).
sid=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("session_id") or "nosession")' 2>/dev/null || echo nosession)
sentinel="${TMPDIR:-/tmp}/scope-fence-reminder-${sid}"
if [ ! -e "$sentinel" ]; then
  touch "$sentinel"
  printf '%s' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"Scope check (scope-fence skill): you are about to edit files. If any change strays outside what the user asked for, flag it in one line instead of silently fixing it — approval is per-scope. This reminder fires once per session."},"suppressOutput":true}'
fi
exit 0
