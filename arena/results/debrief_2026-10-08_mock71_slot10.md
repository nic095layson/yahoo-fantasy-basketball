# Mock 71 debrief — slot 10, deck MOCK mode vs the league cast, deck v51 (rev 1026558, MOCK mode against the 11 league-mates on the real seating; engine, values and pool identical to v50)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_71.json` (md5 `0fb234a092690b115e61cdf0c24bcd89`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v50`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **3.48%** (rank 9 of 12) |
| Playoff rate | 52.43% |
| ECW | **4.316** cats/week (rank 9; next 5.346, Oblena) — favored in 4/11 head-to-heads |
| Season-shape H2H | wins 3/11 |
| Board rank (kept-total z-sum) | **10** (-6.30; next +6.81) |
| Category rank, weekly model | FG% 6 · FT% **12** · 3PTM **12** · PTS 6 · REB 2 · AST 2 · ST **1** · BLK 8 · TO **12** |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Jayson Tatum | 19 | Karl-Anthony Towns (+0.202) | 17/296 | +0.202 |
| 15 | Jalen Williams | Giannis Antetokounmpo | 23 | none | 0/292 | -0.187 |
| 34 | Dyson Daniels | Trae Young | 24 | Franz Wagner (+0.098) | 20/274 | +0.022 |
| 39 | Dyson Daniels | Jaylen Brown | 20 | Ivica Zubac (+0.157) | 20/270 | +0.025 |
| 58 | Payton Pritchard | Damian Lillard | 72 | Tyler Herro (+0.299) | 89/252 | +0.271 |
| 63 | Jalen Suggs | Deni Avdija | 6 | Paolo Banchero (+0.083) | 6/248 | -0.052 |
| 82 | Jalen Suggs | Zion Williamson | 41 | Zach LaVine (+0.142) | 17/230 | +0.142 |
| 87 | Jalen Suggs | Day'Ron Sharpe | 3 | Zach LaVine (+0.053) | 4/226 | -0.014 |
| 106 | Yaxel Lendeborg | Draymond Green | 11 | Daniel Gafford (+0.056) | 7/208 | owner's own later pick |
| 111 | PJ Washington | Yaxel Lendeborg | 3 | Daniel Gafford (+0.025) | 4/204 | +0.012 |
| 130 | Daniel Gafford | Herbert Jones | 3 | Daniel Gafford (+0.085) | 6/109 | +0.059 |
| 135 | Daniel Gafford | Tari Eason | 11 | Daniel Gafford (+0.124) | 9/105 | +0.086 |
| 154 | Saddiq Bey | Bilal Coulibaly | 11 | Kyle Filipowski (+0.068) | 8/87 | +0.056 |

Hindsight found **no better legal pick** at 1 turns (#15) and exactly one at 0 (—). The owner took the card's #1 at 0 turns (—) and a Top-5 row at 3 of 13.

### The turns that cost the most (by hindsight gain)

- **#58 Damian Lillard** (card #72, availability 0.78, note `inj-achilles-risk (first season back); 10/8: started the 10/7 opener vs Golden State, his first game since the Achilles tear, 19 min / 15 pts, 3-8 from three / 2 stl; the Lillard-Morant backcourt 8-19 with five turnovers, minus-9, Nori: rough around the edges; tag kept by convention for the first season back (ESPN box score; NBA.com Starting 5, Blazer's Edge, SI Blazers, Yahoo, KATU)`): 89 of 252 legal alternatives grade higher — Tyler Herro +0.299 (drafted #59 by Cayas); Paolo Banchero +0.281 (drafted #73 by Oblena); Payton Pritchard +0.271 (drafted #61 by Hegi).
- **#10 Jayson Tatum** (card #19, availability 0.78, note `inj-achilles-risk`): 17 of 296 legal alternatives grade higher — Karl-Anthony Towns +0.202 (drafted #11 by Cayas); Anthony Davis +0.181 (drafted #31 by John); Chet Holmgren +0.176 (drafted #18 by John).
- **#39 Jaylen Brown** (card #20, availability 1.0, note ``): 20 of 270 legal alternatives grade higher — Ivica Zubac +0.157 (drafted #56 by JCo); Alperen Sengun +0.110 (drafted #47 by Noah); Franz Wagner +0.106 (drafted #40 by Kevin).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 BLK+FT%; #63 BLK+FT% (advise); #82 BLK+REB+FT% (advise); #87 BLK+TO+FT% (advise); #106 3PTM+BLK+FT% (advise); #111 3PTM+TO+FT% (advise); #130 3PTM+FT%+TO (advise); #135 3PTM+TO+FT% (advise); #154 3PTM+FT%+TO (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 71 (out of sample) | 57 | 0.539 | 0.544 | **0.222** | 0.248 |
| pooled with every earlier scored room | 1068 | 0.488 | 0.618 | 0.239 | 0.236 |

- this room: BUY NOW 6 rows, 3 gone; TOSS-UP 13 rows, 8 gone; quiet 38 rows, 23 survived.
- pooled: BUY NOW 211 rows, 114 gone; TOSS-UP 225 rows, 122 gone; quiet 631 rows, 459 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 27.13 | 99.59 | 2 | #10 Karl-Anthony Towns, #15 Jamal Murray, #34 OG Anunoby, #39 Desmond Bane, #58 Payton Pritchard, #63 De'Aaron Fox, #82 Isaiah Hartenstein, #87 Jalen Suggs, #106 Sandro Mamukelashvili, #130 Daniel Gafford, #135 Cason Wallace, #154 Saddiq Bey |
| swap#58:Tyler Herro | 9.63 | 79.04 | 3 | #58 Tyler Herro |
| swap#10:Karl-Anthony Towns | 7.08 | 72.04 | 6 | #10 Karl-Anthony Towns |
| swap#39:Ivica Zubac | 6.30 | 68.83 | 6 | #39 Ivica Zubac |
| swap#82:Zach LaVine | 6.13 | 66.93 | 6 | #82 Zach LaVine |
| swap#135:Daniel Gafford | 5.16 | 64.96 | 8 | #135 Daniel Gafford |
| swap#34:Franz Wagner | 5.00 | 62.21 | 8 | #34 Franz Wagner |
| swap#130:Daniel Gafford | 4.63 | 60.56 | 8 | #130 Daniel Gafford |
| swap#154:Kyle Filipowski | 4.63 | 58.52 | 8 | #154 Kyle Filipowski |
| swap#63:Paolo Banchero | 4.48 | 58.76 | 8 | #63 Paolo Banchero |
| swap#87:Zach LaVine | 4.35 | 57.58 | 9 | #87 Zach LaVine |
| swap#106:Daniel Gafford | 4.09 | 57.73 | 8 | #106 Daniel Gafford |
| swap#111:Daniel Gafford | 3.66 | 55.50 | 9 | #111 Daniel Gafford |
| as_drafted | 3.48 | 52.43 | 9 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v50`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
