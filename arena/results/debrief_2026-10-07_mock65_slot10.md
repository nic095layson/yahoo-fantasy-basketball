# Mock 65 debrief — slot 10, deck MOCK mode vs the league cast, deck v47 (rev fca8f7c, the 10/7 daily-pull build, the cast on the real seating; the v44 pool with the 10/6 prices)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_65.json` (md5 `c5bd2cf159fdd1969244eb12b2de8782`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v44`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **23.19%** (rank 2 of 12) |
| Playoff rate | 98.39% |
| ECW | **5.174** cats/week (rank 1; next 5.099, Oblena) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **3** (+4.07; next +12.37) |
| Category rank, weekly model | FG% 8 · FT% 5 · 3PTM **1** · PTS 6 · REB 6 · AST 5 · ST 5 · BLK **10** · TO **1** |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Jalen Johnson | Jalen Johnson | 1 | none | 0/300 | owner's own later pick |
| 15 | Jamal Murray | Jamal Murray | 1 | Chet Holmgren (+0.117) | 9/296 | owner's own later pick |
| 34 | Derrick White | Derrick White | 1 | none | 0/278 | owner's own later pick |
| 39 | OG Anunoby | OG Anunoby | 1 | Franz Wagner (+0.031) | 1/274 | owner's own later pick |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/256 | owner's own later pick |
| 63 | Mikal Bridges | Mikal Bridges | 1 | Rudy Gobert (+0.028) | 8/252 | owner's own later pick |
| 82 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/235 | owner's own later pick |
| 87 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Daniel Gafford (+0.020) | 2/231 | owner's own later pick |
| 106 | PJ Washington | PJ Washington | 1 | Daniel Gafford (+0.018) | 1/213 | owner's own later pick |
| 111 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | Daniel Gafford (+0.054) | 3/209 | owner's own later pick |
| 130 | Collin Gillespie | Collin Gillespie | 1 | Daniel Gafford (+0.039) | 1/191 | owner's own later pick |
| 135 | Saddiq Bey | Saddiq Bey | 1 | Daniel Gafford (+0.041) | 1/187 | owner's own later pick |
| 154 | Cam Thomas | Cam Thomas | 1 | none | 0/169 | owner's own later pick |

Hindsight found **no better legal pick** at 5 turns (#10, #34, #58, #82, #154) and exactly one at 4 (#39, #106, #130, #135). The owner took the card's #1 at 13 turns (#10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154) and a Top-5 row at 13 of 13.

### The turns that cost the most (by hindsight gain)

- **#15 Jamal Murray** (card #1, availability 1.0, note `healthy (75 GP in 2025-26; the 9/8 inj-achilles-risk tag was a Dejounte Murray garble - removed 2026-09-28); 10/5: DNP the 10/4 preseason opener for personal reasons (box score; Denver Stiffs, Deseret); 10/7: started the 10/6 game at Utah after missing the opener for personal reasons, 16 min / 4 pts / 3 ast [SINGLE-SOURCE: box score] (ESPN box score)`): 9 of 296 legal alternatives grade higher — Chet Holmgren +0.117 (drafted #17 by JCo); Anthony Davis +0.103 (drafted #24 by Oblena); Giannis Antetokounmpo +0.086 (drafted #26 by Noah).
- **#111 Sandro Mamukelashvili** (card #1, availability 1.0, note `10/7: started at C in the 10/6 game at Golden State with Kessler out, 18 min / 15 pts, 3-4 from three (ESPN box score; NBA.com Starting 5)`): 3 of 209 legal alternatives grade higher — Daniel Gafford +0.054 (drafted #136 by Kevin); Kyle Filipowski +0.010 (drafted #127 by John); John Collins +0.005 (drafted #126 by Martin).
- **#135 Saddiq Bey** (card #1, availability 1.0, note `10/7: 20 min / 5 pts off the bench in the 10/6 game at Oklahoma City [SINGLE-SOURCE: box score] (ESPN box score)`): 1 of 187 legal alternatives grade higher — Daniel Gafford +0.041 (drafted #136 by Kevin); Jakob Poeltl -0.005 (drafted #151 by John); Wendell Carter Jr. -0.022 (drafted #147 by Will).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 1 (#58 Joel Embiid).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+REB; #63 REB+PTS (advise); #82 REB+PTS (advise); #87 PTS+REB (advise); #106 PTS+REB (advise); #111 PTS (advise); #130 PTS (advise); #135 PTS (advise); #154 PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 65 (out of sample) | 48 | 0.617 | 0.542 | **0.207** | 0.248 |
| pooled with every earlier scored room | 751 | 0.475 | 0.621 | 0.253 | 0.235 |

- this room: BUY NOW 2 rows, 2 gone; TOSS-UP 9 rows, 5 gone; quiet 37 rows, 22 survived.
- pooled: BUY NOW 170 rows, 85 gone; TOSS-UP 149 rows, 84 gone; quiet 431 rows, 315 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| swap#15:Chet Holmgren | 27.87 | 99.35 | 1 | #15 Chet Holmgren |
| swap#135:Daniel Gafford | 25.27 | 98.76 | 1 | #135 Daniel Gafford |
| swap#111:Daniel Gafford | 25.09 | 98.80 | 1 | #111 Daniel Gafford |
| swap#130:Daniel Gafford | 24.98 | 98.78 | 1 | #130 Daniel Gafford |
| swap#63:Rudy Gobert | 24.92 | 98.64 | 2 | #63 Rudy Gobert |
| swap#39:Franz Wagner | 24.59 | 98.67 | 1 | #39 Franz Wagner |
| swap#106:Daniel Gafford | 23.95 | 98.54 | 2 | #106 Daniel Gafford |
| swap#87:Daniel Gafford | 23.82 | 98.54 | 2 | #87 Daniel Gafford |
| as_drafted | 23.19 | 98.39 | 2 | — |
| follow_card_selfconsistent | 23.19 | 98.39 | 2 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v44`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
