#!/usr/bin/env bash
# selftest-reminders.sh — pipe tests for the once-per-session reminders and the compaction hook.
#
# Red-team 2026-10-19 (results/2026-10-19/system-red-team, attacks M2, M3, S3): the two first-write
# reminders read the session id with /usr/bin/jq, so on a machine with jq elsewhere every session fell
# back to one shared "nosession" sentinel and each reminder fired once per machine; session-doctrine.sh
# needed jq on PATH and otherwise emitted nothing and re-armed nothing. These cases run every hook
# with an EMPTY PATH except for bash, python3 and coreutils, so no jq is reachable.
#
# Run: bash hooks/selftest-reminders.sh   (expects 8/8)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
export TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT
NOJQ="$TMPDIR/bin"; mkdir -p "$NOJQ"
for b in bash python3 rm touch cat dirname mktemp printf; do
  p=$(command -v "$b" 2>/dev/null) && ln -s "$p" "$NOJQ/$b" 2>/dev/null
done
PASS=0; FAIL=0
check() { # <name> <expect fire|silent> <got-output>
  local got; [ -n "$3" ] && got=fire || got=silent
  if [ "$got" = "$2" ]; then echo "  ok   $1 — $got"; PASS=$((PASS+1)); else echo "  FAIL $1 — expected $2, got $got"; FAIL=$((FAIL+1)); fi
}
pre() { printf '{"hook_event_name":"PreToolUse","session_id":"%s","tool_name":"Write","tool_input":{"file_path":"/x","content":"y"}}' "$1"; }
run_nojq() { env -i PATH="$NOJQ" TMPDIR="$TMPDIR" HOME="$HOME" bash "$@" 2>/dev/null; }
# A hook that references /usr/bin/jq would still find it here whatever PATH says, so each hook runs
# as a copy with that absolute path redirected to a nonexistent one — a no-op for a hook that does
# not hard-code it, and exactly the jq-elsewhere machine of attack M2 for one that does.
nojq_copy() { sed 's#/usr/bin/jq#/nonexistent/jq#g' "$HERE/$1" > "$TMPDIR/$1"; printf '%s' "$TMPDIR/$1"; }

echo "== selftest: reminders + session-doctrine (no jq reachable) =="
for h in plan-gate-first-write-reminder.sh scope-fence-reminder.sh; do
  hc=$(nojq_copy "$h")
  a=$(pre s1 | run_nojq "$hc"); check "$h first write, session s1" fire "$a"
  b=$(pre s1 | run_nojq "$hc"); check "$h second write, same session" silent "$b"
  c=$(pre s2 | run_nojq "$hc"); check "$h first write, DIFFERENT session s2" fire "$c"
done
touch "$TMPDIR/plan-gate-reminder-s3" "$TMPDIR/scope-fence-reminder-s3"
d=$(printf '{"hook_event_name":"SessionStart","source":"compact","session_id":"s3"}' | run_nojq "$(nojq_copy session-doctrine.sh)")
check "session-doctrine compact emits the protocol" fire "$(printf '%s' "$d" | grep -o 'Post-compaction' || true)"
if [ ! -e "$TMPDIR/plan-gate-reminder-s3" ] && [ ! -e "$TMPDIR/scope-fence-reminder-s3" ]; then
  echo "  ok   session-doctrine compact re-armed both reminders"; PASS=$((PASS+1))
else
  echo "  FAIL session-doctrine compact left a sentinel in place"; FAIL=$((FAIL+1))
fi
echo "== $PASS passed, $FAIL failed =="
[ "$FAIL" -eq 0 ] || exit 1
