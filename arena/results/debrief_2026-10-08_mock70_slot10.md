# Mock 70 debrief — slot 10, deck MOCK mode vs the league cast, deck v50 (rev 9f54e99, MOCK mode against the 11 league-mates on the real seating; engine identical to v49)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_70.json` (md5 `e55be4f72a1f354c7ad42935f48a551d`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v50`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **20.68%** (rank 2 of 12) |
| Playoff rate | 96.98% |
| ECW | **5.092** cats/week (rank 2; next 5.144, Oblena) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **3** (-0.91; next +1.48) |
| Category rank, weekly model | FG% 4 · FT% **11** · 3PTM **1** · PTS 4 · REB 5 · AST 6 · ST 3 · BLK 6 · TO 5 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Giannis Antetokounmpo | 16 | Karl-Anthony Towns (+0.035) | 2/296 | +0.035 |
| 15 | Jalen Williams | Cooper Flagg | 8 | Chet Holmgren (+0.075) | 3/292 | -0.078 |
| 34 | Dyson Daniels | Trae Young | 16 | Desmond Bane (+0.107) | 11/274 | +0.064 |
| 39 | OG Anunoby | OG Anunoby | 1 | Franz Wagner (+0.011) | 3/270 | owner's own later pick |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/252 | owner's own later pick |
| 63 | Jalen Suggs | Kon Knueppel | 29 | Paolo Banchero (+0.090) | 20/248 | +0.049 |
| 82 | Jalen Suggs | Day'Ron Sharpe | 6 | Isaiah Hartenstein (+0.052) | 1/230 | -0.064 |
| 87 | Jalen Suggs | Myles Turner | 3 | Isaiah Hartenstein (+0.001) | 1/226 | -0.070 |
| 106 | Sandro Mamukelashvili | Yaxel Lendeborg | 3 | none | 0/208 | owner's own later pick |
| 111 | Sandro Mamukelashvili | Ty Jerome | 10 | Collin Gillespie (+0.036) | 8/204 | owner's own later pick |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/109 | owner's own later pick |
| 135 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | none | 0/105 | owner's own later pick |
| 154 | Daniel Gafford | Saddiq Bey | 2 | Kyle Filipowski (+0.013) | 1/87 | -0.014 |

Hindsight found **no better legal pick** at 4 turns (#58, #106, #130, #135) and exactly one at 3 (#82, #87, #154). The owner took the card's #1 at 4 turns (#39, #58, #130, #135) and a Top-5 row at 7 of 13.

### The turns that cost the most (by hindsight gain)

- **#34 Trae Young** (card #16, availability 1.0, note ``): 11 of 274 legal alternatives grade higher — Desmond Bane +0.107 (drafted #40 by Kevin); Franz Wagner +0.095 (drafted #41 by JCo); Dyson Daniels +0.064 (drafted #44 by Kyle).
- **#63 Kon Knueppel** (card #29, availability 1.0, note `hamstring-monitor (left hamstring strain 9/25: out for preseason, likely misses the start of the season, re-eval first week); 10/1: hamstring pain gone, rebuilding strength, no five-on-five yet; re-evaluation the week of 10/19, the 10/21 opener undecided per Peterson (Yahoo, NBC Sports); 10/2: will miss the entire preseason, the 10/21 opener in doubt, re-evaluation the week of 10/19 (NBA.com, Yahoo, WBTV); 10/5: 'trending positively', doing a little more on the court each day per Lee 10/4; still out for the preseason, re-evaluated the first week of the season (Yahoo, SI Hornets); 10/6: 'iffy for opening night' (RotoBaller 10/6, NBC Sports); no change from Lee's 10/4 update; 10/7: out of the 10/6 preseason opener as announced; ESPN's feed carries a 10/21 estimate, the opener (ESPN game feed; TSN, NBC Sports); 10/8: a little more on-court work each day per the coach (10/4); re-check the week of 10/19, his target the 10/21 opener at Brooklyn (Roundtable 10/4, ClutchPoints, NBC Sports); D-1002-1 holds`): 20 of 248 legal alternatives grade higher — Paolo Banchero +0.090 (drafted #73 by Oblena); Zach LaVine +0.075 (drafted #101 by Kyle); Naz Reid +0.070 (drafted #65 by JCo).
- **#15 Cooper Flagg** (card #8, availability 1.0, note ``): 3 of 292 legal alternatives grade higher — Chet Holmgren +0.075 (drafted #18 by John); Anthony Davis +0.027 (drafted #32 by JCo); Evan Mobley +0.023 (drafted #24 by Oblena).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 3PTM+FT%; #63 FT% (advise); #82 REB+BLK+FT% (advise); #87 FT% (advise); #106 FT% (advise); #111 FT% (advise); #130 FT% (advise); #135 FT% (advise); #154 FT% (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 70 (out of sample) | 54 | 0.562 | 0.630 | **0.203** | 0.233 |
| pooled with every earlier scored room | 1011 | 0.485 | 0.622 | 0.240 | 0.235 |

- this room: BUY NOW 6 rows, 4 gone; TOSS-UP 11 rows, 4 gone; quiet 37 rows, 25 survived.
- pooled: BUY NOW 205 rows, 111 gone; TOSS-UP 212 rows, 114 gone; quiet 593 rows, 436 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 30.77 | 99.69 | 1 | #10 Karl-Anthony Towns, #15 Jamal Murray, #34 Desmond Bane, #63 Josh Hart, #82 Zach LaVine, #87 Isaiah Hartenstein, #111 Cason Wallace |
| swap#63:Paolo Banchero | 24.33 | 98.11 | 1 | #63 Paolo Banchero |
| swap#34:Desmond Bane | 24.11 | 98.56 | 1 | #34 Desmond Bane |
| swap#10:Karl-Anthony Towns | 23.25 | 98.27 | 1 | #10 Karl-Anthony Towns |
| swap#15:Chet Holmgren | 22.72 | 98.22 | 2 | #15 Chet Holmgren |
| swap#111:Collin Gillespie | 22.31 | 97.66 | 2 | #111 Collin Gillespie |
| swap#82:Isaiah Hartenstein | 21.81 | 97.79 | 2 | #82 Isaiah Hartenstein |
| swap#39:Franz Wagner | 21.40 | 97.10 | 2 | #39 Franz Wagner |
| swap#154:Kyle Filipowski | 21.01 | 97.17 | 2 | #154 Kyle Filipowski |
| swap#87:Isaiah Hartenstein | 20.79 | 96.94 | 2 | #87 Isaiah Hartenstein |
| as_drafted | 20.68 | 96.98 | 2 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v50`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
