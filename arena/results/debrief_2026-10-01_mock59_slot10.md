# Mock 59 debrief — slot 10, live public room, slot 10 — v37

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_59.json` (md5 `0bfcbba343380d83e2436ed1125695d3`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v37`; poolless names in this room: UNKNOWN #126. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **20.38%** (rank 2 of 12) |
| Playoff rate | 98.50% |
| ECW | **5.092** cats/week (rank 2; next 5.260, T2) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **1** (+8.27; next +6.07) |
| Category rank, weekly model | FG% 2 · FT% 7 · 3PTM 7 · PTS **11** · REB 3 · AST **11** · ST 2 · BLK 3 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Tyrese Haliburton | 3 | Tyrese Maxey (+0.029) | 2/301 | owner's own later pick |
| 15 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/297 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | Derrick White (+0.019) | 1/279 | owner's own later pick |
| 39 | Derrick White | Walker Kessler | 47 | Derrick White (+0.237) | 31/275 | +0.237 |
| 58 | OG Anunoby | OG Anunoby | 1 | Payton Pritchard (+0.014) | 2/257 | owner's own later pick |
| 63 | Payton Pritchard | Damian Lillard | 2 | Payton Pritchard (+0.047) | 1/253 | +0.047 |
| 82 | Jakob Poeltl | Day'Ron Sharpe | 12 | Miles Bridges (+0.112) | 12/235 | +0.085 |
| 87 | Zach LaVine | VJ Edgecombe | 20 | Zach LaVine (+0.107) | 10/231 | +0.107 |
| 106 | Jakob Poeltl | Neemias Queta | 52 | Jakob Poeltl (+0.215) | 44/213 | +0.215 |
| 111 | Collin Gillespie | Collin Gillespie | 1 | none | 0/209 | owner's own later pick |
| 130 | Devin Vassell | PJ Washington | 2 | none | 0/192 | owner's own later pick |
| 135 | Devin Vassell | Yaxel Lendeborg | 5 | Saddiq Bey (+0.013) | 1/189 | owner's own later pick |
| 154 | Devin Vassell | Devin Vassell | 1 | Malik Monk (+0.007) | 1/171 | owner's own later pick |

Hindsight found **no better legal pick** at 3 turns (#15, #111, #130) and exactly one at 4 (#34, #63, #135, #154). The owner took the card's #1 at 5 turns (#15, #34, #58, #111, #154) and a Top-5 row at 9 of 13.

### The turns that cost the most (by hindsight gain)

- **#39 Walker Kessler** (card #47, availability 0.78, note `inj-shoulder-risk (first season back; fully cleared for all basketball activity per Pelinka at the 9/28 media day — NBC Sports, CBS)`): 31 of 275 legal alternatives grade higher — Derrick White +0.237 (drafted #45 by T4); Domantas Sabonis +0.214 (drafted #41 by T8); Desmond Bane +0.197 (drafted #52 by T4).
- **#106 Neemias Queta** (card #52, availability 1.0, note `role 9/30: starting-center favorite in a three-man platoon with Mitchell Robinson and Garza (Yahoo, SI Celtics)`): 44 of 213 legal alternatives grade higher — Jakob Poeltl +0.215 (drafted #129 by T9); Aaron Gordon +0.154 (drafted #131 by T11); Draymond Green +0.134 (drafted #147 by T3).
- **#82 Day'Ron Sharpe** (card #12, availability 1.0, note `starting-center role (Yahoo Nets camp breakdown, TalkBasket); twinned 2026-09-30 to the kit's 28.2-mpg starter line (built from the 2025-26 B-Ref per-36: 16.8 pts / 12.8 reb / 4.5 ast / 2.1 stl)`): 12 of 235 legal alternatives grade higher — Miles Bridges +0.112 (drafted #102 by T6); Zach LaVine +0.101 (drafted #94 by T3); Jakob Poeltl +0.085 (drafted #129 by T9).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+3PTM+AST; #63 AST+PTS (advise); #82 PTS+AST (advise); #87 PTS+AST (advise); #106 PTS+AST (advise); #111 PTS+3PTM+AST (advise); #130 PTS+AST+3PTM (advise); #135 PTS+AST (advise); #154 PTS+AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 59 (out of sample) | 52 | 0.514 | 0.596 | **0.183** | 0.241 |
| pooled with every earlier scored room | 454 | 0.418 | 0.672 | 0.294 | 0.220 |

- this room: BUY NOW 6 rows, 4 gone; TOSS-UP 13 rows, 8 gone; quiet 33 rows, 24 survived.
- pooled: BUY NOW 144 rows, 61 gone; TOSS-UP 82 rows, 43 gone; quiet 227 rows, 182 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 39.18 | 99.97 | 1 | #10 Tyrese Maxey, #39 Derrick White, #63 Jakob Poeltl, #82 Damian Lillard, #87 Miles Bridges, #106 Day'Ron Sharpe |
| swap#39:Derrick White | 27.14 | 99.67 | 2 | #39 Derrick White |
| swap#106:Jakob Poeltl | 26.53 | 99.63 | 2 | #106 Jakob Poeltl |
| swap#87:Zach LaVine | 23.32 | 99.18 | 2 | #87 Zach LaVine |
| swap#82:Miles Bridges | 22.79 | 99.12 | 2 | #82 Miles Bridges |
| swap#63:Payton Pritchard | 22.20 | 98.98 | 2 | #63 Payton Pritchard |
| swap#10:Tyrese Maxey | 21.69 | 98.72 | 2 | #10 Tyrese Maxey |
| swap#34:Derrick White | 21.49 | 98.82 | 2 | #34 Derrick White |
| swap#135:Saddiq Bey | 20.69 | 98.52 | 2 | #135 Saddiq Bey |
| as_drafted | 20.38 | 98.50 | 2 | — |
| swap#58:Payton Pritchard | 20.34 | 98.39 | 2 | #58 Payton Pritchard |
| swap#154:Malik Monk | 20.13 | 98.61 | 2 | #154 Malik Monk |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v37`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
