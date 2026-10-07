# Mock 64 debrief — slot 10, deck MOCK mode vs the league cast, deck v47 (rev fca8f7c, the 10/7 daily-pull build, the cast on the real seating; the v44 pool with the 10/6 prices)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_64.json` (md5 `5abfd25ab6c579d7f12e49808ffb89aa`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v44`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **7.63%** (rank 3 of 12) |
| Playoff rate | 74.98% |
| ECW | **4.555** cats/week (rank 3; next 5.357, Oblena) — favored in 7/11 head-to-heads |
| Season-shape H2H | wins 4/11 |
| Board rank (kept-total z-sum) | **4** (+0.16; next +11.76) |
| Category rank, weekly model | FG% **11** · FT% 7 · 3PTM 4 · PTS 6 · REB **9** · AST **9** · ST 4 · BLK 8 · TO 4 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Jalen Johnson | Jayson Tatum | 18 | Jalen Johnson (+0.154) | 14/300 | +0.154 |
| 15 | Jalen Williams | Kevin Durant | 3 | Chet Holmgren (+0.064) | 6/296 | -0.019 |
| 34 | Dyson Daniels | Bam Adebayo | 11 | Franz Wagner (+0.052) | 5/278 | -0.009 |
| 39 | OG Anunoby | Kyrie Irving | 5 | Franz Wagner (+0.071) | 9/274 | +0.058 |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/256 | owner's own later pick |
| 63 | Jalen Suggs | Paolo Banchero | 21 | none | 0/252 | -0.078 |
| 82 | Isaiah Hartenstein | Jaden McDaniels | 6 | Isaiah Hartenstein (+0.058) | 8/235 | +0.058 |
| 87 | Myles Turner | Jabari Smith Jr. | 13 | Julius Randle (+0.017) | 2/231 | -0.062 |
| 106 | PJ Washington | Herbert Jones | 4 | PJ Washington (+0.044) | 6/213 | +0.035 |
| 111 | Yaxel Lendeborg | Collin Gillespie | 4 | Sandro Mamukelashvili (+0.041) | 4/209 | +0.014 |
| 130 | Daniel Gafford | Daniel Gafford | 1 | none | 0/191 | -0.009 |
| 135 | Saddiq Bey | Cason Wallace | 2 | Saddiq Bey (+0.037) | 1/187 | +0.037 |
| 154 | Cam Thomas | Stephon Castle | 80 | Wendell Carter Jr. (+0.149) | 54/169 | +0.141 |

Hindsight found **no better legal pick** at 3 turns (#58, #63, #130) and exactly one at 1 (#135). The owner took the card's #1 at 2 turns (#58, #130) and a Top-5 row at 7 of 13.

### The turns that cost the most (by hindsight gain)

- **#10 Jayson Tatum** (card #18, availability 0.78, note `inj-achilles-risk`): 14 of 300 legal alternatives grade higher — Jalen Johnson +0.154 (drafted #11 by Cayas); Chet Holmgren +0.095 (drafted #17 by JCo); Anthony Davis +0.088 (drafted #29 by Kyle).
- **#154 Stephon Castle** (card #80, availability 1.0, note ``): 54 of 169 legal alternatives grade higher — Wendell Carter Jr. +0.149 (drafted #None by None); Santi Aldama +0.148 (drafted #None by None); Cam Thomas +0.141 (drafted #None by None).
- **#39 Kyrie Irving** (card #5, availability 0.78, note `inj-acl-risk (first season back)`): 9 of 274 legal alternatives grade higher — Franz Wagner +0.071 (drafted #41 by JCo); OG Anunoby +0.058 (drafted #49 by Oblena); Onyeka Okongwu +0.036 (drafted #43 by Martin).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+ST+REB; #63 BLK+REB+ST (advise); #82 BLK+ST+REB (advise); #87 AST (advise); #106 AST+ST (advise); #111 AST (advise); #130 REB+AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 64 (out of sample) | 53 | 0.575 | 0.509 | **0.196** | 0.250 |
| pooled with every earlier scored room | 703 | 0.465 | 0.626 | 0.256 | 0.234 |

- this room: BUY NOW 4 rows, 4 gone; TOSS-UP 14 rows, 9 gone; quiet 35 rows, 22 survived.
- pooled: BUY NOW 168 rows, 83 gone; TOSS-UP 140 rows, 79 gone; quiet 394 rows, 293 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 18.97 | 95.62 | 2 | #10 Jalen Johnson, #34 OG Anunoby, #39 Franz Wagner, #63 Jalen Suggs, #82 Zach LaVine, #87 Day'Ron Sharpe, #106 Yaxel Lendeborg, #111 Sandro Mamukelashvili, #130 Saddiq Bey, #135 Daniel Gafford |
| swap#154:Wendell Carter Jr. | 11.07 | 85.12 | 3 | #154 Wendell Carter Jr. |
| swap#10:Jalen Johnson | 10.67 | 84.56 | 2 | #10 Jalen Johnson |
| swap#39:Franz Wagner | 9.17 | 79.48 | 3 | #39 Franz Wagner |
| swap#15:Chet Holmgren | 9.11 | 80.04 | 3 | #15 Chet Holmgren |
| swap#34:Franz Wagner | 9.07 | 79.89 | 3 | #34 Franz Wagner |
| swap#106:PJ Washington | 8.47 | 77.45 | 3 | #106 PJ Washington |
| swap#111:Sandro Mamukelashvili | 8.38 | 77.83 | 3 | #111 Sandro Mamukelashvili |
| swap#82:Isaiah Hartenstein | 8.14 | 78.34 | 3 | #82 Isaiah Hartenstein |
| swap#135:Saddiq Bey | 7.97 | 77.06 | 3 | #135 Saddiq Bey |
| swap#87:Julius Randle | 7.84 | 75.15 | 4 | #87 Julius Randle |
| as_drafted | 7.63 | 74.98 | 3 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v44`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
