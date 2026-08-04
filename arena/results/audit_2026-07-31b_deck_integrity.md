# Draft Deck system integrity audit #2 — 2026-07-31 (owner-requested)

Second full audit of the day, covering the **eleven commits shipped since
audit #1** (`33f2ef7`): wheel-seat horizon fix, cat-filter cap, structural
drift escalation, Soft-Punt rank annotations, declared-punt warnings, card
v4 layout, plus five mock debriefs and the derived LEDGER.

Run solo (no subagents) using the standing harness suite, extended: the
render gauntlet grew from 65 states / 8 invariants to **130 states / 10
invariants**, and a **mutation suite** was added to prove the gauntlet can
actually fail.

## Verdict

**No defects in the shipped tool.** Every functional check passed. Three
defects were found and fixed — **all three in the reporting layer**
(debrief prose), which is precisely where the owner-caught error earlier
today also lived. The pattern is now unmistakable and is addressed
structurally below.

## 1. Provenance & freeze compliance

| Check | Result |
|---|---|
| Working tree | clean (0 modified) |
| local == remote | `d053eff` both |
| Data freshness | stamped 2026-07-31, 246/246 rows verified |
| **Engine code diff since audit #1** | **EMPTY** — `arena/*.py`, `scripts/*.py` untouched |
| Files touched by all 11 commits | `docs/draft-deck.html` + report markdown, nothing else |
| Build round-trip | deterministic (rebuild produced no diff) |

The "display-only" claim attached to eleven commits is now *proven*, not
asserted: the engine-code diff is literally empty.

## 2. Engine math

JS↔Python parity **EXACT** (241/241 rows). All four script blocks parse
clean. Build gates fail-closed and pass. Audit #1's nine math checks
(fixed-point z, survivalP vs erf, fit tiers, gradient constants,
concession constants, arena instrument, determinism) remain valid by
construction — the code implementing them has not changed a byte.

## 3. Render gauntlet — 130 states, 10 invariants, 0 violations

Every owner-turn state of mocks 16–25 (10 drafts × 13 rounds), booted
through the shipped app block with independent in-harness recomputation.

| Invariant | Violations |
|---|---|
| I1 single 🎯 marker | 0 |
| I2 no CAN WAIT text | 0 |
| I3 verdict form + bottom-right placement | 0 |
| I4 canonical panel cat order | 0 |
| I5 🔒 lock correctness (two-directional) | 0 |
| I6 Soft-Punt roster gate | 0 |
| I7 feed-title snake math | 0 |
| I8 no punted-cat leak into panel | 0 |
| I9 drift payload well-formed | 0 |
| I10 cat-filter state integrity | 0 |

Chip census: 353 BUY NOW (25 shelf), 56 TOSS-UP, 241 quiet. 0 harness
errors across 130 states.

**Mutation suite (new).** Seven deliberate defects injected into the
shipped code; all seven were caught:

| Injected defect | Caught by |
|---|---|
| mark every row with 🎯 | I1 |
| resurrect the CAN WAIT chip | I2 |
| reverse panel category order | I4 |
| widen the lock tier to rank ≤ 6 | I5 |
| remove the Soft-Punt roster gate | I6 (early-roster states only) |
| change the feed-title format | I7 |
| let punted cats into the panel | I8 |

*Honest note:* the gate mutant initially escaped a 4-state probe because
every probe state had roster ≥ 4. It is caught the moment early-roster
states are included — a lesson about probe coverage, recorded here so the
suite is not trusted beyond what it exercises.

## 4. New-feature validation

- **Drift-latch calibration, all 10 mocks:** fires on m23 (#61) only;
  **0 false positives** across the six non-catastrophes *and* both
  record-holders (m24 29.66%, m25 29.00%); **0 uncovered catastrophes** —
  m22 is covered by the declared-punt warning at all 13 turns instead, the
  designed division of labour.
- **Wheel horizon, both wheel seats:** first-half-of-pair BUY NOW
  precision **17/17 (100%)** at slot 12 and **15/17 (88%)** at slot 1,
  against **0/10** pre-fix.
- **Cat-filter cap:** 9/9 interaction assertions (block at 4th/5th,
  one-shot prompt, re-click re-asserts, × removal, re-add, Reset).
- **Regression:** both standing smokes and all three fixtures
  (punt-active, UNKNOWN-pick, 14-team) pass.

## 5. Defects found — all in the reporting layer

1. **Wheel figures conflated (m24 debrief).** "28/30 (93%) across slot 1's
   six pair-boundaries" attributed an *all-turns* number to
   *pair-boundaries only*. Both figures are real (all-turns 28/30;
   pair-boundaries 15/17) — the sentence merged them. **Fixed:** both now
   stated separately and labelled.
2. **Stale cumulative tallies (m20/m21/m22 debriefs).** Four surviving
   "0-for-4" / "4-for-4 (m13…)" claims predating the LEDGER, with the same
   membership defect the LEDGER was created to end. **Fixed:** all rebased
   on `LEDGER.md`.
3. **Superseded superlatives (m22 debrief).** "Worst result ever measured"
   and "worst playoff% measured" were true when written and false three
   hours later (m23: 0.16% / 4.2%). **Fixed:** dated, marked superseded,
   with the rule that live superlatives live only in the LEDGER.

## 6. Root-cause assessment

Three audits' worth of evidence now separates the system cleanly:

- **Computational layer — consistently sound.** Two full audits, 195
  cumulative gauntlet states, a mutation suite, exact parity, empty engine
  diffs. Zero defects found in shipped behaviour today.
- **Reporting layer — the recurring weak point.** Every defect found in
  this audit, plus the owner-caught streak error, is a *derived* claim
  (tally, superlative, or cross-measurement comparison) asserted from
  memory rather than recomputed. Single measurements have never been
  wrong; relationships between measurements repeatedly have.

**Structural mitigation, now in force:** `arena/results/LEDGER.md` holds
every cumulative tally and live superlative, derived from artifacts with
written membership criteria. Debriefs cite it rather than restating it.
Superlatives in historical debriefs are dated and may be superseded — only
the LEDGER is current. This audit added the enforcement pass: a grep sweep
for unbacked derived claims, which is how all three defects above were
found and should be repeated at each future audit.

## 7. Standing limits (unchanged, restated)

- The drift alarm is a weak classifier on the broad base (25 fires /108
  team-drafts, bust recall 7/23, one elite FP at 15.56%) — a severity
  marker, not a rescue mechanism; catastrophe sample n=2.
- Quiet-chip survival remains optimistic in mock rooms (value-drafters
  accelerate); recalibration registered for September ADP.
- The empty-roster gradient finding (m24 −14.1pp, m25 −7.5pp) replicates
  across rooms but is the **same player pair in the same pool** — the
  September experiment must vary outlier profiles, not re-run Wemby.
- `ar/fx/sy` (7.8KB) and `gradImpact` remain baked but unconsumed, kept by
  owner instruction with a September use-or-drop checkpoint.
