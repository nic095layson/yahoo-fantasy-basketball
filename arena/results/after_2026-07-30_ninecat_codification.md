# After-report — 9-CAT math codification (2026-07-30)

Implements the approved proposals from `findings_2026-07-30_ninecat_math.md`
in the pre-registered order. Every change was validated on the fixed
instrument by a 6-agent measurement workflow whose load-bearing numbers were
re-derived by an adversarial gauntlet at fresh seeds (one phrasing
correction, zero refutations), then ratified by the Council 5–0.

## Codified

- **P1 — honest percentage variance** (`arena/arena.py`): weekly FG%/FT%
  variance is now per-roster binomial × `PCT_MIX_INFL = 1.15`, replacing
  the flat `PCT_WEEK_SD = 0.012` that made the better team win FT% in
  99.4% of weeks. Post-fix better-team FT% win probs land at 0.55–0.88
  (punt tails higher) — no more deterministic coins. Variance is now
  roster-dependent (low-volume punt teams are correctly volatile).
- **P2 — Yahoo-true standings** (`arena/arena.py`): regular-season
  seeding accumulates the cumulative **category** record
  (`record[a] += wa; record[b] += 9 − wa`), matching Yahoo H2H-each-cat;
  playoff matches decided by `week_result ≥ 5`. The retired weekly-binary
  rule had shifted playoff% by up to ±29pp on identical rosters.
- **P3 — draftable-pool z** (`scripts/hoops.py`): standardization
  parameters (league % baselines, means, stds) come from the top-156
  draftable fixed point (true fixed point, verified to 1.3e−15), applied
  to all rows. The z-sum's zero now sits at replacement level.
- **P4 — haircut re-audit** (no code change needed): on the
  replacement-anchored scale the 0.78 risk haircut taxes only the 11
  risk players with above-replacement value (AD, Haliburton, Kyrie …)
  and is correctly inert for the 19 below-replacement risk vets (FVV,
  Dejounte, PG, LeBron, Embiid …). The 0.78 (draft price, includes
  real-league streaming) vs 0.852 (arena world ratio) constant pair is
  intentional and documented — not aligned.
- **Hygiene — sign-aware market multipliers** (`arena/arena.py` +
  `docs/draft-deck.html`): rookie hype now raises and risk now lowers
  negative-score players (division below zero), fixing the inverted tail.

Deck rebuilt from the new engine; gates green: verify_rosters 246/246
(0 mismatches, 2026-07-30), build round-trip byte-identical, JS↔Python
parity **EXACT**, freshness stamped 2026-07-30 (news sweep: zero roster
changes; Draymond→GSW now official; Beal opt-out and DeRozan waiver
already carried as FA). Artifact republished to the standing URL.

## Board movers (drafting intuition update)

Risers: **FVV 84→70, Dejounte 80→67, Kessler 54→44, Paul George 81→72,
Tatum 25→20** (risk-tagged vets whose haircut was inflated by the old
pool). Fallers: **KD 16→21, Morant 69→75, Poole 74→82, Jaylen Brown
77→83** (healthy players whose z rode the soft baseline). Top-7
membership unchanged. Matches the dissertation's predictions exactly.

## Validation on the fixed instrument

- **Neutral-weights re-quote: +5.59pp champ, t = 7.18** (n = 120 paired
  drafts; was +3.78pp t = 5.16 on the old instrument) — the flagship
  codification survives and strengthens. Independently reproduced at
  fresh seeds (+4.01pp, t = 3.37).
- **Council validation tournament: council 2nd/13 at 12.43% champ with
  the room-best 68.85% playoff%** (was 4th/13 at 11.56%). safe_floor 1st
  at 13.78% (gap within cross-seed spread). The old punt-dominance
  artifact evaporates — punt_ft falls from 33%+ mock-room winner to 7th
  at 8.88%: committed punts were partly a %-determinism exploit.
  Council rank reproduced exactly at a fresh verifier seed.
- **Integrity: ALL PASS** — champ normalization exact (100.0000/draft),
  playoff exact (600.0000), CRN determinism bit-identical, category-
  record identity (972 = 9·18·12/2 per season) exact in all checked
  seasons, zero crashes across 72 drafts.
- **Sensitivity (Council flag, resolved):** council's tournament rank
  is 2/13 at every `PCT_MIX_INFL ∈ {1.0, 1.15, 1.3}` (champ 13.17 /
  13.18 / 13.10%, seed 314 × 2 rotations × 1500 seasons; safe_floor 1st
  and slot_filler 3rd at all three) — the estimated constant does not
  drive any conclusion.

## New category exchange rates (champ pp per +1 z, fixed instrument)

AST **2.75** · BLK **2.73** · 3PTM 1.74 · PTS 1.72 · REB 1.67 · TO 1.60 ·
ST 1.58 · FT% 1.53 · FG% 1.21 (max/min 2.28). Headlines: **3PTM jumped
#8→#3** (threes are NOT cheap on the honest instrument); **FG% collapsed
relatively** (#3→#9, flat-within-noise absolutely — gauntlet-corrected
phrasing); AST/BLK remain the premium levers. Overall level rose ×1.57
because P2 converts marginal category strength directly into standings.

## Measured and NOT codified (the protocol saying no)

- **P5 TO down-weight: REJECT** — TO=0.5 costs −6.31pp (t = −4.74),
  TO=0.25 costs −7.41pp (t = −6.68). Surprise mechanism: inverted TO z is
  a *star turnover tax*; removing it pivots the council into
  high-usage/high-TO builds that concede TO+ST+BLK+FG%+REB weekly. The
  TO column is real draft signal, not bench-piece overpay.
- **P6 global elasticity weights: INCONCLUSIVE** (−1.92pp, t = −1.05;
  playoff −13.8pp) — do not codify. **Filed discovery:** the effect is
  slot-structured (+9.73pp from slots 1–3, −5.80pp from slots 4–12):
  elasticity-weighting pays only when the elite AST/BLK anchors are
  reachable. A *slot-conditional* weighting is a registered follow-up
  experiment, not a codification.

## Comparability note (Council-mandated)

**All arena numbers dated before 2026-07-30 were measured on the old
instrument and are not comparable to new runs.** This includes the mock
10–12 debrief champ%/finish grades and every historical findings file.
Historical results stand as measured; re-grades of mocks 10–12 on the
honest instrument are an open follow-up. Historical harnesses
(`matrix_paired.py` etc.) still pin their original fields and remain
reproducible only against commit `1ae3693` or earlier.

## Follow-up register

1. Slot-conditional elasticity weights (slots 1–3 only) — CRN experiment.
2. Re-grade mocks 10–12 season sims on the fixed instrument.
3. `PCT_MIX_INFL` re-estimate from real weekly data when the season starts.
4. Surface the new exchange rates (3PTM #3, AST/BLK premium) in deck
   guidance copy — display-only change, needs no arena run.

*Method: 6-agent measurement workflow (M1 elasticity refit → M4 P6 test;
M2 re-quote; M3 P5 sweep; M5 tournament + integrity) + adversarial
gauntlet at fresh seeds; Council ratification 5–0. Scratchpad artifacts:
`elasticity_exp_v2.py`, `m2_neutral_paired.py`, `m3_to_sweep.py`,
`m4_council_weights.py`, `run_seed.py`/`integrity.py`,
`verify_elasticity.py`, `verify_m5.py`.*
