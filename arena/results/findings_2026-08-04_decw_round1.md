# E9 round 1 — the ΔECW card: enormous promise, FAILS the ship bar (2026-08-04)

Owner-authorized prototype (Q15). Card: each candidate scored by marginal
expected-categories-won vs current partial opponent rosters, arena's own
weekly model, no foresight (`arena/mocks/decw_card.py`, ~0.6s/draft).
Validation: follow-the-card counterfactual vs as-drafted on all 14 ledger
mocks, each with an E11 perturbation-matched placebo (same swap count,
random legal targets). 6,000 × seeds [11,23] per arm, hardened swap
machinery. Full artifacts: `decw_cf_m*_*.json`.

## Results

| Mock | As drafted | ΔECW card | Δ | Placebo |
|---|---|---|---|---|
| 16 | 15.44 | 30.12 | **+14.68** | 2.85 |
| 17 | 1.64 | 0.19 | −1.45 | 0.00 |
| 18 | 4.33 | 30.19 | **+25.86** | 0.00 |
| 19 | 10.72 | 26.90 | **+16.18** | 3.65 |
| 20 | 6.51 | 13.80 | **+7.29** | 0.00 |
| 21 * | 26.91 | 42.21 | **+15.30** | 0.76 |
| 23 | 0.17 | 13.29 | **+13.12** | 0.00 |
| 24 * | 29.82 | 42.15 | **+12.33** | 1.75 |
| **25 *** | 29.19 | **1.62** | **−27.57** | 0.00 |
| **26 *** | 22.57 | **3.12** | **−19.45** | 0.00 |
| 27 | 9.76 | 19.41 | **+9.65** | 1.33 |
| 28 | 6.50 | 10.51 | +4.01 | 1.09 |
| 29 | 8.90 | 0.41 | −8.49 | 0.01 |
| 30 | 2.12 | 12.32 | **+10.20** | 0.01 |

(* = winner-regression gate mocks.) Mean **+5.12pp**, median **+9.93pp**,
10/14 improved by >1pp. Placebo mean 0.82 vs card mean 17.59 — the
objective, not the perturbation, drives the gains (E11 satisfied).

## Verdict: DOES NOT SHIP

The pre-registered bar — no regression on m21/m24/m25/m26 — is failed
twice, and not marginally: **m25 −27.6pp, m26 −19.5pp.** The bar exists
precisely because a median this good tempts a ship; the tails are
disqualifying. The current composite card's worst full-follow outcome ever
measured is −8.7pp; this prototype's is −27.6.

## Failure mode, diagnosed from the swap lists

The marginal objective **concedes categories emergently**. Once a category
falls behind (or gets far ahead), its marginal value → 0, so the greedy
card stops paying for it, which pushes it further out, which zeroes it
harder — a self-reinforcing concentration spiral. m25's card swapped OUT
the Wemby anchor (for Jokić) and then bought SIX guards (Sheppard, Suggs,
Quickley, Edgecombe, McCollum, Rollins), building an all-guards roster that
died exactly the way m22's declared punt died. This is **G1a re-emerging
as an emergent behavior of the objective** — the lab measured every
punt-*declaring* policy at −5 to −11pp, and ΔECW rediscovers punt-declaring
on its own. Sometimes the concentration lands on a winnable coalition
(m18 +25.9, m21 +15.3); when it misses, it is catastrophic. High variance
is intrinsic to the unregularized objective, not a bug in the code.

Also consistent with two prior laws: the matrix-weighting discovery
(down-weighting locked/lost cats during drafting is causally harmful) and
the r=0 outlier finding (the objective undervalues Wemby-class anchors —
it swapped Wemby out on turn one).

## Round 2 directions (pre-registered for the next iteration)

1. **Concession floor** — never let a category's effective marginal weight
   fall below a fraction of its neutral z-weight (the matrix-weighting law,
   applied to the new objective).
2. **Value blend** — score = α·ΔECW + (1−α)·neutral value; sweep α on the
   14-mock panel; the bar is unchanged.
3. **Anchor protection** — rounds 1–2 pure value (the r=0 lesson; ΔECW's
   turn-one opponent context is 0–1 partial rosters, i.e. noise).
4. Re-validate under BOTH playoff formats (these arms used the shipped
   6-team bracket; the real 8-team format from `league_intel` §4 may shift
   where concentration pays).

Bar for round 2, unchanged: beat the composite across the panel with
**zero** winner regressions. These arms are E9 prototype tests, not
deviation-tally members (different membership: the card under test never
shipped).
