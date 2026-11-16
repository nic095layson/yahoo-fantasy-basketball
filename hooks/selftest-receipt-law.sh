#!/usr/bin/env bash
# selftest-receipt-law — pipe-test for receipt-law-stop-gate.sh (which runs receiptlaw.py beside it).
#
# Builds synthetic transcripts covering both directions and asserts BLOCK /
# no-BLOCK. The should-NOT-block cases matter more than the should-block one:
# a Stop hook that fires wrongly interrupts every turn it touches, which is a
# far worse failure than the defect it guards (anti-ceremony, invariant 5).
#
# These are the gate's first 15 cases, kept as a quick check that needs nothing but
# bash and python3. The full table of the gate (every sentence of the 2026-11-12
# audit, the record shapes, the failure paths) is table "R" of
# selftest-turn-gates.py:  python3 hooks/selftest-turn-gates.py RL
# and the guard runs both. One case changed on 2026-11-15, t7 (see there).
#
# Usage: bash hooks/selftest-receipt-law.sh     Exit 0 = all pass.
set -u
HOOK="$(cd "$(dirname "$0")" && pwd)/receipt-law-stop-gate.sh"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
# The gate keeps no state file since 2026-11-15 (it used to write once-per-turn
# sentinels into TMPDIR, and a previous run's sentinel could suppress this run's
# block). TMPDIR still points into the work folder so that nothing here can touch
# the real one.
export TMPDIR="$WORK"
PASS=0; FAIL=0

# mk <file> <assistant-text> [tool-name]
mk() {
  local f="$1" say="$2" tool="${3:-}"
  : > "$f"
  printf '%s\n' '{"type":"user","promptId":"p1","message":{"role":"user","content":"do the thing"}}' >> "$f"
  if [ -n "$tool" ]; then
    python3 -c '
import json,sys
print(json.dumps({"type":"assistant","message":{"role":"assistant","content":[
  {"type":"tool_use","id":"t1","name":sys.argv[1],"input":{}}]}}))' "$tool" >> "$f"
  fi
  python3 -c '
import json,sys
print(json.dumps({"type":"assistant","message":{"role":"assistant","content":[
  {"type":"text","text":sys.argv[1]}]}}))' "$say" >> "$f"
}

# run <name> <expect BLOCK|ALLOW> <transcript> [stop_hook_active]
run() {
  local name="$1" expect="$2" tr="$3" active="${4:-false}"
  local out got
  out=$(printf '{"session_id":"%s","transcript_path":"%s","stop_hook_active":%s}' \
        "$name" "$tr" "$active" | bash "$HOOK" 2>/dev/null)
  if printf '%s' "$out" | grep -q '"decision"[[:space:]]*:[[:space:]]*"block"'; then got=BLOCK; else got=ALLOW; fi
  if [ "$got" = "$expect" ]; then
    echo "  ok   $name — $got"; PASS=$((PASS+1))
  else
    echo "  FAIL $name — expected $expect, got $got"; echo "       output: $out"; FAIL=$((FAIL+1))
  fi
}

echo "== selftest: receipt-law-stop-gate =="

# 1. The INC-9 shape: claims inability, no tools, no receipt.
mk "$WORK/t1" "I checked three of the cards. The remaining eight I couldn't verify, but they're probably Arcane. Verdict: Arcane is your thinnest school."
run t1-inc9-shape BLOCK "$WORK/t1"

# 2. Honest ATTEMPTED-FAILED — a receipt is present.
mk "$WORK/t2" "I searched three card databases for Contraband Wands and none of them list a spell school field at all, so I cannot verify it positively."
run t2-receipt-present ALLOW "$WORK/t2"

# 3. THE REGRESSION CASE. Tools ran, but the claim cites none of them. This is
#    the real incident's exact shape — three searches, then eight items declared
#    unverifiable without ever being touched. An earlier version of this gate
#    passed any turn containing a tool call and therefore MISSED this. Must block.
mk "$WORK/t3" "Eight cards I couldn't verify (Molten Rune, Cram Session, Rewind, Siphon Mana) — most are probably Arcane." "WebSearch"
run t3-tools-ran-no-receipt BLOCK "$WORK/t3"

# 3b. Tools ran AND the claim carries its receipt — the honest version of t3.
mk "$WORK/t3b" "I searched three card databases for Contraband Wands; none list a spell school field, so it cannot be confirmed positively." "WebSearch"
run t3b-tools-ran-with-receipt ALLOW "$WORK/t3b"

# 4. Meta-safety: the phrase only appears quoted / in code.
mk "$WORK/t4" 'The rule targets this phrase family:

```
couldn'"'"'t verify / unable to confirm
```

> "eight cards I couldn'"'"'t verify"

That is what the gate looks for.'
run t4-quoted-only ALLOW "$WORK/t4"

# 5. Loop guard: the retry flag is set and the record shows no block at all (the
#    record does not keep every row): the stop is let go. The flag alone no longer
#    means "this gate already blocked" (2026-11-15: it is true after ANY Stop hook's
#    block); with a block of another hook on record the gate still judges, which the
#    table tests (RLX01, RLX03, RLX07).
mk "$WORK/t5" "The remaining items are unverified and I couldn't confirm them."
run t5-loop-guard ALLOW "$WORK/t5" true

# 6. Ordinary answer, no inability claim.
mk "$WORK/t6" "PostgreSQL listens on port 5432 by default."
run t6-plain-answer ALLOW "$WORK/t6"

# 7. At most one block in a stretch. CHANGED 2026-11-15 (findings RL-2, FU2-1, TB-5 of the
#    2026-11-12 audit): the count is read from the record, not from a sentinel file. The
#    second stop is therefore judged on the record as the program leaves it after a block:
#    the feedback row that carries this gate's reason, then the answer again. (The old case
#    ran the same file twice and relied on the sentinel; with no block on record the same
#    file blocks again, which is table case RLX11.)
mk "$WORK/t7" "Three of the twelve I could not determine, so I am going with the estimate."
run t7-first-fire BLOCK "$WORK/t7"
python3 -c '
import json,sys
print(json.dumps({"type":"user","isMeta":True,"message":{"role":"user","content":
  "Stop hook feedback: Receipt law: this answer says \"could not determine\" and the same sentence names no attempt and no failure."}}))
print(json.dumps({"type":"assistant","message":{"role":"assistant","content":[
  {"type":"text","text":sys.argv[1]}]}}))' "Three of the twelve I could not determine, so I am going with the estimate." >> "$WORK/t7"
run t7-second-stop-after-own-block ALLOW "$WORK/t7"

# 8. Fail-open: transcript missing entirely.
run t8-missing-transcript ALLOW "$WORK/does-not-exist.jsonl"

# 9-12. Red-team 2026-10-19 (results/2026-10-19/system-red-team, attacks R2-R6): the claim
#    pattern missed curly apostrophes and paraphrases, and a receipt word anywhere in the turn,
#    even as a substring, excused the claim.
mk "$WORK/t9" "I couldn’t verify the release date."
run t9-curly-apostrophe BLOCK "$WORK/t9"
mk "$WORK/t10" "I wasn't able to verify the release date, and I have no way to confirm the venue."
run t10-paraphrases BLOCK "$WORK/t10"
mk "$WORK/t11" "I couldn't verify the date the veteran guard was traded."
run t11-receipt-substring BLOCK "$WORK/t11"
far=$(python3 -c 'print("The CI job ran fine and the lint passed. " + "Filler sentence about the deck layout. " * 14 + "Separately, I couldn'"'"'t verify the release date.")')
mk "$WORK/t12" "$far"
run t12-receipt-far-from-claim BLOCK "$WORK/t12"
mk "$WORK/t13" "I couldn't verify the release date: I searched the press page and the wiki and neither lists one."
run t13-receipt-beside-claim ALLOW "$WORK/t13"

echo "== $PASS passed, $FAIL failed =="
[ "$FAIL" -eq 0 ] || exit 1
