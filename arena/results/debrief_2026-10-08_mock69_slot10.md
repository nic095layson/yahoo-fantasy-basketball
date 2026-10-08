# Mock 69 debrief — slot 10, deck MOCK mode vs the league cast, deck v50 (rev 9f54e99, MOCK mode against the 11 league-mates on the real seating; engine identical to v49)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_69.json` (md5 `899ff83b23b415fee14e7c282096f029`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v50`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **27.51%** (rank 1 of 12) |
| Playoff rate | 99.37% |
| ECW | **5.229** cats/week (rank 1; next 5.058, Oblena) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **1** (+5.93; next +5.66) |
| Category rank, weekly model | FG% 5 · FT% 3 · 3PTM 3 · PTS **10** · REB 5 · AST **11** · ST 2 · BLK 5 · TO 3 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/296 | owner's own later pick |
| 15 | Jamal Murray | James Harden | 5 | Chet Holmgren (+0.014) | 1/292 | -0.049 |
| 34 | OG Anunoby | OG Anunoby | 1 | Franz Wagner (+0.071) | 3/274 | owner's own later pick |
| 39 | Onyeka Okongwu | Onyeka Okongwu | 1 | Dyson Daniels (+0.009) | 1/270 | owner's own later pick |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/252 | owner's own later pick |
| 63 | Jalen Suggs | Jalen Suggs | 1 | Paolo Banchero (+0.019) | 1/248 | owner's own later pick |
| 82 | Mikal Bridges | Mikal Bridges | 1 | none | 0/231 | owner's own later pick |
| 87 | Josh Hart | Josh Hart | 1 | none | 0/227 | owner's own later pick |
| 106 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Draymond Green (+0.002) | 1/209 | owner's own later pick |
| 111 | PJ Washington | PJ Washington | 1 | Draymond Green (+0.013) | 2/205 | owner's own later pick |
| 130 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | Cason Wallace (+0.012) | 2/109 | owner's own later pick |
| 135 | Daniel Gafford | Daniel Gafford | 1 | none | 0/105 | -0.035 |
| 154 | Collin Gillespie | Collin Gillespie | 1 | none | 0/87 | owner's own later pick |

Hindsight found **no better legal pick** at 6 turns (#10, #58, #82, #87, #135, #154) and exactly one at 4 (#15, #39, #63, #106). The owner took the card's #1 at 12 turns (#10, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154) and a Top-5 row at 13 of 13.

### The turns that cost the most (by hindsight gain)

- **#34 OG Anunoby** (card #1, availability 1.0, note ``): 3 of 274 legal alternatives grade higher — Franz Wagner +0.071 (drafted #35 by Cayas); Desmond Bane +0.055 (drafted #38 by Cayas); Dyson Daniels +0.045 (drafted #49 by Oblena).
- **#63 Jalen Suggs** (card #1, availability 1.0, note `10/6: illness, ran at Tuesday's practice, uncertain for the 10/7 preseason opener (RotoWire 10/6, Yahoo); 10/8: did not dress for the 10/7 opener at Memphis, the illness of several days; day-to-day on ESPN's feed with a 10/11 estimate; next chance Sunday at Cleveland (ESPN game feed; CBS Sports, Yahoo)`): 1 of 248 legal alternatives grade higher — Paolo Banchero +0.019 (drafted #74 by Noah); Coby White -0.000 (drafted #70 by Will); Ryan Rollins -0.010 (drafted #81 by Kevin).
- **#15 James Harden** (card #5, availability 1.0, note ``): 1 of 292 legal alternatives grade higher — Chet Holmgren +0.014 (drafted #18 by John); Anthony Davis -0.006 (drafted #32 by JCo); Josh Giddey -0.019 (drafted #26 by Noah).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+PTS; #63 AST+PTS (advise); #82 PTS+AST (advise); #87 AST (advise); #106 PTS+BLK+AST (advise); #111 PTS (advise); #130 PTS (advise); #135 PTS (advise); #154 AST+PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 69 (out of sample) | 48 | 0.564 | 0.625 | **0.219** | 0.234 |
| pooled with every earlier scored room | 957 | 0.481 | 0.622 | 0.242 | 0.235 |

- this room: BUY NOW 6 rows, 5 gone; TOSS-UP 8 rows, 3 gone; quiet 34 rows, 24 survived.
- pooled: BUY NOW 199 rows, 107 gone; TOSS-UP 201 rows, 110 gone; quiet 556 rows, 411 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| swap#15:Chet Holmgren | 30.66 | 99.72 | 1 | #15 Chet Holmgren |
| swap#39:Dyson Daniels | 30.36 | 99.39 | 1 | #39 Dyson Daniels |
| swap#34:Franz Wagner | 29.99 | 99.53 | 1 | #34 Franz Wagner |
| swap#130:Cason Wallace | 29.04 | 99.49 | 1 | #130 Cason Wallace |
| swap#106:Draymond Green | 28.98 | 99.42 | 1 | #106 Draymond Green |
| swap#111:Draymond Green | 28.88 | 99.51 | 1 | #111 Draymond Green |
| swap#63:Paolo Banchero | 27.69 | 99.23 | 1 | #63 Paolo Banchero |
| as_drafted | 27.51 | 99.37 | 1 | — |
| follow_card_selfconsistent | 26.58 | 99.22 | 1 | #15 Jamal Murray |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v50`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
