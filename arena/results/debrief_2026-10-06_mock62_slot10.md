# Mock 62 debrief — slot 10, deck MOCK mode vs the league cast, deck v46 (rev 441bba6, the MOCK-seating build; the v44 pool with the 10/6 prices)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_62.json` (md5 `f185f50d5dcbe3f0ba7108e314837677`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v44`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **18.05%** (rank 2 of 12) |
| Playoff rate | 94.91% |
| ECW | **4.987** cats/week (rank 2; next 5.284, Oblena) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **3** (+1.67; next +13.15) |
| Category rank, weekly model | FG% 5 · FT% 7 · 3PTM **1** · PTS 5 · REB 3 · AST 6 · ST 6 · BLK 7 · TO 4 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Jalen Johnson | Jalen Johnson | 1 | none | 0/300 | owner's own later pick |
| 15 | Jalen Williams | Jalen Williams | 1 | Chet Holmgren (+0.103) | 7/296 | owner's own later pick |
| 34 | OG Anunoby | OG Anunoby | 1 | Dyson Daniels (+0.032) | 2/278 | owner's own later pick |
| 39 | Payton Pritchard | Payton Pritchard | 1 | none | 0/274 | owner's own later pick |
| 58 | Tyler Herro | Tyler Herro | 1 | none | 0/256 | owner's own later pick |
| 63 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | Rudy Gobert (+0.009) | 1/252 | owner's own later pick |
| 82 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Myles Turner (+0.032) | 3/234 | owner's own later pick |
| 87 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | Myles Turner (+0.026) | 3/231 | owner's own later pick |
| 106 | PJ Washington | PJ Washington | 1 | none | 0/213 | owner's own later pick |
| 111 | Saddiq Bey | Saddiq Bey | 1 | none | 0/209 | owner's own later pick |
| 130 | Collin Gillespie | Collin Gillespie | 1 | none | 0/191 | -0.036 |
| 135 | Daniel Gafford | Daniel Gafford | 1 | none | 0/187 | -0.046 |
| 154 | Cam Thomas | Cam Thomas | 1 | none | 0/169 | owner's own later pick |

Hindsight found **no better legal pick** at 8 turns (#10, #39, #58, #106, #111, #130, #135, #154) and exactly one at 1 (#63). The owner took the card's #1 at 13 turns (#10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154) and a Top-5 row at 13 of 13.

### The turns that cost the most (by hindsight gain)

- **#15 Jalen Williams** (card #1, availability 1.0, note ``): 7 of 296 legal alternatives grade higher — Chet Holmgren +0.103 (drafted #19 by Martin); Derrick White +0.041 (drafted #32 by JCo); Anthony Davis +0.039 (drafted #25 by Oblena).
- **#82 Yaxel Lendeborg** (card #1, availability 1.0, note `rookie-proj; role 9/30: Kerr — 'clearly going to play a ton', starter or not (Yahoo rookie targets, NBA.com media day); Porziņģis out indefinitely with an undisclosed health issue (CBS Sports, SI Warriors); repriced 2026-09-30 from 26 to 28 minutes, kit twin; 10/2, second pull: named the starter at SF for the 10/4 preseason opener vs the Clippers (Curry, Podziemski, Lendeborg, Green, Horford) over Gui Santos; Kerr: only Curry and Green are entrenched regular-season starters (SI Warriors, Yahoo, Heavy, Golden State of Mind); line holds for the WO-5 refresh; 10/5: started the 10/4 preseason opener at SF, 19 min, 4 pts / 9 reb / 3 ast on 1-6; Kerr wants him more aggressive (box score; NBC Sports Bay Area, Yahoo recap)`): 3 of 234 legal alternatives grade higher — Myles Turner +0.032 (drafted #91 by Martin); Day'Ron Sharpe +0.017 (drafted #83 by Cayas); Jabari Smith Jr. +0.002 (drafted #97 by Oblena).
- **#34 OG Anunoby** (card #1, availability 1.0, note ``): 2 of 278 legal alternatives grade higher — Dyson Daniels +0.032 (drafted #46 by Will); Franz Wagner +0.017 (drafted #38 by Cayas); Onyeka Okongwu -0.028 (drafted #42 by John).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 1 (#82 Fred VanVleet).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+REB; #63 REB (advise); #82 PTS+REB (advise); #87 PTS (advise); #106 PTS (advise); #111 PTS (advise); #130 PTS (advise); #135 PTS (advise); #154 PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 62 (out of sample) | 48 | 0.577 | 0.521 | **0.196** | 0.250 |
| pooled with every earlier scored room | 602 | 0.444 | 0.645 | 0.264 | 0.229 |

- this room: BUY NOW 4 rows, 4 gone; TOSS-UP 9 rows, 6 gone; quiet 35 rows, 22 survived.
- pooled: BUY NOW 161 rows, 76 gone; TOSS-UP 117 rows, 65 gone; quiet 323 rows, 250 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| swap#15:Chet Holmgren | 21.74 | 97.56 | 2 | #15 Chet Holmgren |
| swap#34:Dyson Daniels | 20.16 | 95.97 | 2 | #34 Dyson Daniels |
| swap#82:Myles Turner | 19.53 | 96.08 | 2 | #82 Myles Turner |
| swap#87:Myles Turner | 19.36 | 95.78 | 2 | #87 Myles Turner |
| swap#63:Rudy Gobert | 18.36 | 94.99 | 2 | #63 Rudy Gobert |
| follow_card_selfconsistent | 18.22 | 93.91 | 2 | #130 Herbert Jones, #135 Collin Gillespie |
| as_drafted | 18.05 | 94.91 | 2 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v44`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
