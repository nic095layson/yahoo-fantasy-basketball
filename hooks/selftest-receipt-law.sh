#!/usr/bin/env bash
# selftest-receipt-law — pipe-test for receipt-law-stop-gate.sh.
#
# Builds synthetic transcripts covering both directions and asserts BLOCK /
# no-BLOCK. The should-NOT-block cases matter more than the should-block one:
# a Stop hook that fires wrongly interrupts every turn it touches, which is a
# far worse failure than the defect it guards (anti-ceremony, invariant 5).
#
# Usage: bash hooks/selftest-receipt-law.sh     Exit 0 = all pass.
set -u
HOOK="$(cd "$(dirname "$0")" && pwd)/receipt-law-stop-gate.sh"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
# Hermetic: the gate writes once-per-turn sentinels into TMPDIR. Sharing the real
# /tmp across runs let a previous run's sentinel suppress this run's block — the
# first version of this file failed exactly that way on its second execution.
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

# 5. Loop guard: we are already continuing because of this hook.
mk "$WORK/t5" "The remaining items are unverified and I couldn't confirm them."
run t5-loop-guard ALLOW "$WORK/t5" true

# 6. Ordinary answer, no inability claim.
mk "$WORK/t6" "PostgreSQL listens on port 5432 by default."
run t6-plain-answer ALLOW "$WORK/t6"

# 7. Once per turn: same session+turn must not block twice.
mk "$WORK/t7" "Three of the twelve I could not determine, so I am going with the estimate."
run t7-first-fire BLOCK "$WORK/t7"
run t7-first-fire ALLOW "$WORK/t7"   # same sid+promptId -> sentinel suppresses

# 8. Fail-open: transcript missing entirely.
run t8-missing-transcript ALLOW "$WORK/does-not-exist.jsonl"

echo "== $PASS passed, $FAIL failed =="
[ "$FAIL" -eq 0 ] || exit 1
