# Mock 48 debrief — Seat 4, declared punt FT%/3PTM/TO (2026-08-06)

Standard room, v2 instrument, cast recorded. State:
`arena/data/states/draft_state_mock48.json`. Regenerate:
`python3 arena/mocks/season_sim_mock48.py`. Replay:
`arena/results/m48_replay.json`.

## Headline — the best draft in the ledger, on every metric

| Metric | Value | Rank | Prior best (all mocks, computed from artifacts) |
|---|---|---|---|
| Champ% | **46.03** (46.23/46.03/45.82 per-seed) | **1 of 12** | 43.84 (m41, sharp room); 33.98 (m39) |
| Playoff% | **97.96** | 1 | 96.65 (m41); 93.99 (m39) |
| ECW/week | **5.137** | 1 | 5.111 (m41); 5.059 (m36) |
| Kept-z under declared punt | +26.42 | 1 | — |
| Kept-total, 9 cats | — | 6 | — |

**All three headline records, and this one is a standard room** — unlike
m41 (sharp-room, asterisked) and unlike m28's 34.58 (a hindsight oracle,
not a draft). Per-seed spread is 0.41pp, so it is not a seed artifact.

Room: owner 46.03, then Noah 13.58, Martin 6.94, Will 6.30 — **3.4× the
next seat**, the widest margin in the ledger. Playoff odds of 97.96% mean
the build misses the postseason once in fifty seasons.

**Seat-edge: +32.09pp** over Seat 4's bot baseline (13.94) — the largest
measured, and the 15th positive edge in 16 rooms.

Roster: SGA, Giannis, Trae, Amen Thompson, Sengun, Tari Eason, Duren,
Gobert, Clingan, Ausar, RJ Barrett, Darryn Peterson, Caruso.

## Why it worked — every doctrine condition satisfied at once

1. **Optimal declaration.** FT%/3PTM/TO is the **#1 frame of 84**
   (+26.42 vs +23.65 runner-up) — ninth optimal declaration in eleven
   punted drafts.
2. **Genuinely played.** FT% −12.69, 3PTM −11.21 both rank 12; TO −2.58
   rank 10. No hedging.
3. **No dead kept category** — all six positive: FG% **+8.98 (rank 1)**,
   REB **+6.23 (1)**, BLK **+4.17 (1)**, ST +5.39 (2), AST +1.46 (4),
   PTS +0.19 (7). **Three rank-1 categories with the fourth at rank 2.**
4. **AST alive at rank 4** — the m44/m45 dead-AST failure avoided, and
   the mechanism is exactly the doctrine refinement recorded after m44:
   SGA, Trae and Amen Thompson are genuine playmakers, so the seven-big
   frontcourt never starves the backcourt cats.

This is the first build to satisfy all four conditions simultaneously.
m39 (33.98) had all six kept cats positive but only two rank-1s; m44
(23.64) had the deeper frame (+32.97) but killed AST; m40 (26.29) had
five C-eligibles and softer strengths.

## Card agreement — the collaboration shape

Exact #1 **5/13**, Top-5 8/13. The card supplied the spine (SGA R1, Amen
R4, Eason R6, Ausar R10, Caruso R13 all exact #1; Duren and Gobert in
Top-5), and every deviation was a punt-fit star or big: **Giannis** (R2,
card said Mobley), **Trae** (R3, card said Derrick White), **Sengun**
(R5), **Clingan** (R9), **RJ Barrett** (R11), **Darryn Peterson** (R12).

Note R3 in particular: taking Trae over Derrick White is the AST
insurance that saved the build — the card, punt-blind by design, could
not see that the frontcourt was about to eat six roster spots.

## Read for October

This is the template draft. Seat 4 is a strong seat (3rd best, baseline
13.94), the declaration was optimal and hard, the guards were protected
early, and the card filled the middle and end. The doctrine in its final
form, now with a 46% example behind it:

> **Declare the frame the roster wants → protect the one category your
> shape threatens (usually AST) with an early star → let the card fill
> the spine.**

## LEDGER row

`| 48 | 4 | **46.03** | **98.0** | 1 | 12 | **BEST DRAFT IN THE LEDGER —
all three headline records, in a STANDARD room**: champ 46.03 (prior
43.84 m41-sharp, 33.98 m39), playoff 97.96, ECW 5.137 — each computed
from artifacts. 3.4× the next seat (Noah 13.58), widest margin measured;
seat-edge +32.09pp over Seat 4's baseline 13.94, largest measured (15th
positive in 16). NINTH optimal declaration in eleven punted drafts:
FT%/3PTM/TO #1 of 84 (+26.42) and hard-played (FT% −12.7, 3PTM −11.2
both rank 12). FIRST build to satisfy all four doctrine conditions at
once — no dead kept cat, THREE rank-1 cats (FG% +8.98, REB +6.23, BLK
+4.17) plus ST rank 2, and AST alive at rank 4 because SGA/Trae/Amen
protect it behind seven bigs (the m44 refinement, confirmed). Card
exact-#1 5/13 supplying the spine; all six deviations punt-fit stars
(`season_sim_mock48.py`, `m48_replay.json`) |`
