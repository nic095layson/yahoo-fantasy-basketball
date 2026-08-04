# Mock 26 post-mortem — slot 3: a win that BREAKS TWO LAWS (2026-07-31)

Completed 13-round mock (156/156, Coward resolves). Third gradient seat,
completing the slot 1→2→3 trio in three consecutive drafts. First
gradient-seat draft where the owner did NOT get an outlier anchor (Wemby
went #1). Replay via the audited app block; seasons 6,000 × 3; three CFs
6,000 × 2.

## Outcome — 1st place, but the counterfactuals are the story

| Metric | Mock 26 (slot 3) |
|---|---|
| Champ% | **22.61 (1st/12)** |
| Playoff% | 85.6 |
| Kept-total | +2.96 (3rd) — first 1st-place finish WITHOUT the best board |
| 🎯 exact hits | 8/13 — but shaped oddly: the first five picks all deviated, the last eight were all exact |

Roster: Luka, Tatum, Sabonis, Pritchard, Flagg, Suggs, Duren, McDaniels,
Vučević, Grant, Nesmith, DLo, McCain. 3PTM 3rd, REB 4th; conceded BLK
9th, FG% 9th, ST 8th.

## LAW BROKEN #1 — the empty-roster gradient claim REVERSES

| Mock | Seat | Anchor taken | As drafted | Card (SGA) | Verdict |
|---|---|---|---|---|---|
| 24 | 1 | Wembanyama | 29.82 | 15.70 | deviation won +14.12 |
| 25 | 2 | Wembanyama | 29.19 | 21.66 | deviation won +7.53 |
| **26** | **3** | **Dončić** | **22.57** | **28.85** | **CARD WON +6.28** |

Yesterday's conclusion — *"the empty-roster 🎯 is the card's least-trusted
output"* — is **refuted as a general claim**. Swap the anchor from an
extreme outlier to a conventional high-usage guard and the card is right
by 6.3pp.

**What survives is narrower, and it is exactly what the original mechanism
hypothesis predicted.** The Φ-saturation story said the gradient's curves
flatten on *extreme single-cat outliers*, so a +7z BLK stops paying after
about half a category win. That predicts the effect is specific to
Wemby-class profiles — and Luka is not one (high PTS/AST/3PTM, negative
FG%/BLK/TO). So mock 26 simultaneously **kills the broad claim and
supports the mechanism**. Restated for September:

> The r=0 gradient appears to undervalue extreme single-cat outliers
> (2 instances, both large) and to be correct for conventional profiles
> (1 instance). Trust the r=0 🎯 unless the alternative is a genuine
> outlier anchor.

Still n=3 across 2 anchor types in one pool. No engine change.

## LAW BROKEN #2 — a deep-deviation bundle WINS for the first time

| Line | Champ% |
|---|---|
| As drafted | 22.57 |
| CF2 — the three deep early reaches → the card (Tatum→KD board 14, Sabonis→JJJ board 19, Pritchard→Lopez board 16) | **16.81** |
| CF3 — Pritchard→Lopez alone | 21.91 (wash) |

Following the card at those three turns would have cost **5.76pp**. This
is the **first CF-tested deviation bundle to clearly beat the card** in
ten arms. The standing claim "no tested deviation has ever clearly won"
— itself only a day old and already a correction of two earlier wrong
tallies — is now false.

Updated tally (`LEDGER.md`): **10 arms — 5 COST, 4 WASH, 1 DEVIATION
WON.** Board depth is now demonstrably a poor predictor in both
directions: m25's board-13 deviation was free while its board-5 cost
4.1pp; m26's board-14/19/16 bundle won outright.

## What this draft actually teaches

The owner won from a gradient seat **without** the room's best board
(3rd) and **without** the anchor the previous two winners had. The
mechanism was the back half: eight consecutive exact 🎯 hits from #70
onward, on a roster whose early shape the owner had chosen against the
card. That is the doctrine's real content — *shape early, then execute* —
and it is the first time the ledger shows it working with the card
disagreeing at the top.

Structural instrumentation stayed correctly quiet (drift latch never
fired; BLK 9th and FG% 9th never reached the 11th-or-worse dead zone).

## Honesty note on this session's tallies

Three of my cumulative claims have now been wrong or superseded within
24 hours ("0-for-4" → "0-for-6" → "0 of 8, 3 washes" → falsified by this
draft). Each individual measurement has been correct every time; the
generalizations drawn across them have not. `LEDGER.md` now carries the
full revision history of this tally deliberately, so the drift is visible
rather than smoothed away — and debriefs cite it instead of restating a
number.
