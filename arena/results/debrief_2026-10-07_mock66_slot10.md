# Mock 66 debrief — slot 10, deck MOCK mode vs the league cast, deck v49 (rev 269c522, the fixes build — round-11 priced-only card, V4 bots, Castle/Barrett re-derived; the cast on the real seating)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_66.json` (md5 `8f2ee9dd30cc72e87ea4f6b98299e0d8`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v49`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **20.16%** (rank 1 of 12) |
| Playoff rate | 96.75% |
| ECW | **5.013** cats/week (rank 1; next 4.887, Will) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 8/11 |
| Board rank (kept-total z-sum) | **4** (-0.68; next +7.32) |
| Category rank, weekly model | FG% **11** · FT% **12** · 3PTM 3 · PTS **1** · REB 7 · AST **1** · ST **1** · BLK 7 · TO **12** |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Jalen Johnson | Giannis Antetokounmpo | 17 | Chet Holmgren (+0.073) | 4/296 | +0.042 |
| 15 | Derrick White | Scottie Barnes | 25 | Chet Holmgren (+0.181) | 9/292 | -0.081 |
| 34 | Dyson Daniels | Trae Young | 16 | Derrick White (+0.224) | 35/274 | owner's own later pick |
| 39 | OG Anunoby | Dyson Daniels | 4 | Onyeka Okongwu (+0.028) | 4/270 | +0.014 |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/252 | owner's own later pick |
| 63 | Zach LaVine | Paolo Banchero | 13 | Myles Turner (+0.004) | 1/248 | -0.064 |
| 82 | Coby White | VJ Edgecombe | 19 | Myles Turner (+0.138) | 32/230 | owner's own later pick |
| 87 | Coby White | Coby White | 1 | Myles Turner (+0.045) | 3/226 | owner's own later pick |
| 106 | PJ Washington | Jalen Green | 16 | Sandro Mamukelashvili (+0.047) | 4/208 | +0.047 |
| 111 | PJ Washington | PJ Washington | 1 | none | 0/204 | owner's own later pick |
| 130 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Sandro Mamukelashvili (+0.008) | 2/109 | owner's own later pick |
| 135 | Daniel Gafford | Fred VanVleet | 24 | Sandro Mamukelashvili (+0.142) | 24/105 | +0.142 |
| 154 | Daniel Gafford | Daniel Gafford | 1 | none | 0/87 | owner's own later pick |

Hindsight found **no better legal pick** at 3 turns (#58, #111, #154) and exactly one at 1 (#63). The owner took the card's #1 at 5 turns (#58, #87, #111, #130, #154) and a Top-5 row at 6 of 13.

### The turns that cost the most (by hindsight gain)

- **#34 Trae Young** (card #16, availability 1.0, note ``): 35 of 274 legal alternatives grade higher — Derrick White +0.224 (drafted #35 by Cayas); Onyeka Okongwu +0.177 (drafted #43 by Martin); Desmond Bane +0.155 (drafted #40 by Kevin).
- **#15 Scottie Barnes** (card #25, availability 1.0, note ``): 9 of 292 legal alternatives grade higher — Chet Holmgren +0.181 (drafted #19 by Martin); Anthony Davis +0.147 (drafted #27 by Will); Evan Mobley +0.137 (drafted #20 by Kyle).
- **#135 Fred VanVleet** (card #24, availability 0.78, note `inj-acl-risk (first season back); 10/1: fully cleared, five-on-five scrimmages for weeks, practiced Wednesday 9/30; no back-to-backs to open the season, minutes limit set by camp progress per Udoka (CBS Sports, The Dream Shake, Yahoo, RotoWire) — D-BV2`): 24 of 105 legal alternatives grade higher — Sandro Mamukelashvili +0.142 (drafted #149 by Kyle); Kyle Filipowski +0.134 (drafted #None by None); Jakob Poeltl +0.097 (drafted #138 by John).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 1 (#154 Herbert Jones).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 3PTM+FT%; #63 FT%+3PTM (advise); #82 FT%+3PTM (advise); #87 FT%+TO (advise); #106 REB+BLK+FT% (advise); #111 TO+BLK+FT% (advise); #130 TO+BLK+REB (advise); #135 TO+FT%+BLK (advise); #154 TO+BLK+FT% (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 66 (out of sample) | 55 | 0.551 | 0.673 | **0.205** | 0.220 |
| pooled with every earlier scored room | 807 | 0.479 | 0.625 | 0.250 | 0.234 |

- this room: BUY NOW 6 rows, 4 gone; TOSS-UP 11 rows, 4 gone; quiet 38 rows, 28 survived.
- pooled: BUY NOW 177 rows, 89 gone; TOSS-UP 161 rows, 88 gone; quiet 468 rows, 342 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 34.93 | 99.90 | 1 | #10 Jalen Johnson, #15 Kevin Durant, #34 Derrick White, #39 Desmond Bane, #63 De'Aaron Fox, #82 Jalen Suggs, #87 Isaiah Hartenstein, #106 Sandro Mamukelashvili, #135 Cason Wallace |
| swap#34:Derrick White | 26.63 | 99.07 | 1 | #34 Derrick White |
| swap#15:Chet Holmgren | 25.88 | 98.73 | 1 | #15 Chet Holmgren |
| swap#135:Sandro Mamukelashvili | 24.65 | 98.45 | 1 | #135 Sandro Mamukelashvili |
| swap#82:Myles Turner | 24.26 | 98.30 | 1 | #82 Myles Turner |
| swap#10:Chet Holmgren | 22.74 | 97.97 | 1 | #10 Chet Holmgren |
| swap#87:Myles Turner | 21.73 | 97.23 | 1 | #87 Myles Turner |
| swap#106:Sandro Mamukelashvili | 21.31 | 97.13 | 1 | #106 Sandro Mamukelashvili |
| swap#130:Sandro Mamukelashvili | 20.76 | 96.78 | 1 | #130 Sandro Mamukelashvili |
| as_drafted | 20.16 | 96.75 | 1 | — |
| swap#39:Onyeka Okongwu | 20.03 | 96.68 | 1 | #39 Onyeka Okongwu |
| swap#63:Myles Turner | 20.01 | 96.47 | 1 | #63 Myles Turner |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v49`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
