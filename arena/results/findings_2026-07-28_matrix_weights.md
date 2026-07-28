# Matrix-weighting study — 2026-07-28

**Trigger:** owner asked whether the swing-weighting should wait until the
3rd drafted player. The activation-timing sweep answered that question and
surfaced a much larger one.

## Evidence chain (all 12-team, fixed 11-personality field + test seat)

1. **Rank-signal stability** (36 drafts): at roster size 2 — the current
   activation point — locked/lost labels agree with final-roster reality
   47.8%; 52.9% of down-weight labels are harmful mislabels (cats that end
   contested). Signal crosses 60% at 3 players, 70% at 5.
2. **Activation sweep** (120k championship samples/variant): activate at
   2nd pick 8.18%, 3rd (current) 9.34%, 4th 9.12%, 5th 9.42%, 6th 9.57% —
   timing is second-order. **Weights OFF entirely: 12.09%**, winning all
   5 seeds outright.
3. **Paired causal test** (120 common-random-number draft pairs): matrix
   ON 9.04% vs OFF 11.77% — **+2.73pp causal, t = 4.17**, 76/44 drafts
   better off. Same methodology that rejected the punt two-gate.
4. **Independent corroboration** (stock tournament, seeds 11/108/205,
   54k seasons/strategy, after the seated-count crash fix): bpa_pure
   (no matrix, no need/stack) 11.25% vs council 8.23%. AND the crucial
   counter-shape: **specialist (locked 1.4 / lost 0.2) dead last at
   0.93%** — over-feeding strengths and abandoning weaknesses is even
   worse than the current dampers.

## Reading

The response to rank-reactive weighting is **non-monotone with an optimum
near neutral (1.0/1.0)**. The z-value signal already prices category
value; second-guessing it with rank-reactive multipliers — in EITHER
direction — trades certain weekly category wins for coin-flips. The
current (0.35, 0.45) costs ~2.7pp championship (~30% relative); the
aggressive inverse (1.4, 0.2) costs ~8pp. The activation-timing question
dissolves: no activation point rescues weights that shouldn't be applied
at their current magnitudes.

Side observation for a future study: safe_floor led the corroboration
board (14.6%) — the injury-risk discounts may underprice weekly
availability drag in the sim. Not acted on.

## Proposed codification package (owner sign-off required)

1. FIRST fix arena ROUNDS 15→13 (codified league) and re-baseline.
2. Response-curve sweep: (locked_w, lost_w) in {(0.35,0.45) current,
   (0.6,0.6), (0.8,0.8), (1.0,1.0), (1.2,0.8)} on the re-based arena;
   paired-confirm the winner vs current.
3. If (≈1.0, ≈1.0) confirms: neutralize the layer in arena council AND
   the deck (fitWeights/strategyScores share the constants; the Fit
   column and TARGET inherit). Punt zeroing is untouched (independent
   code path). Board/kit plane unaffected.
4. Log accepted values here; deck republish carries them.

Pre-registered criteria honored throughout; prediction for the original
sweep ("never loses clearly") was WRONG and is recorded as such.

## Crash fix landed with this study

`tournament()` broke when the 13th personality was added (7/22):
enumerate walked 13 names into 12 seats → KeyError on every stock
tournament/slots/cadence run since. Fixed with per-name seated counts;
percentages now normalize by drafts actually seated.
