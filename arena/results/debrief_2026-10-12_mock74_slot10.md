# Mock 74 debrief — slot 10, live public room, deck v58 (rev df1c754, LIVE mode in a public Yahoo room, the owner's export pasted; the 10/12 daily-pull build with the 10/9 prices)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_74.json` (md5 `e59b01d991e3ff32d8bbd7264736f652`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v58`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **17.91%** (rank 2 of 12) |
| Playoff rate | 96.98% |
| ECW | **4.953** cats/week (rank 2; next 5.137, T1) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **4** (+2.74; next +6.34) |
| Category rank, weekly model | FG% 2 · FT% 6 · 3PTM **10** · PTS **11** · REB **1** · AST **10** · ST 4 · BLK 2 · TO 2 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Anthony Edwards (+0.041) | 1/295 | owner's own later pick |
| 15 | Jalen Williams | Donovan Mitchell | 2 | none | 0/291 | owner's own later pick |
| 34 | Derrick White | Jalen Williams | 2 | none | 0/273 | owner's own later pick |
| 39 | Derrick White | Derrick White | 1 | none | 0/269 | owner's own later pick |
| 58 | OG Anunoby | OG Anunoby | 1 | none | 0/251 | owner's own later pick |
| 63 | Jarrett Allen | Damian Lillard | 69 | Payton Pritchard (+0.260) | 44/247 | -0.013 |
| 82 | Josh Hart | Josh Hart | 1 | Coby White (+0.110) | 14/229 | owner's own later pick |
| 87 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | Coby White (+0.141) | 27/225 | owner's own later pick |
| 106 | Myles Turner | Yaxel Lendeborg | 2 | Saddiq Bey (+0.055) | 13/207 | owner's own later pick |
| 111 | Myles Turner | Khaman Maluach | 95 | Saddiq Bey (+0.275) | 128/203 | +0.251 |
| 130 | PJ Washington | Wendell Carter Jr. | 21 | Saddiq Bey (+0.153) | 29/108 | +0.113 |
| 135 | Devin Vassell | Daniel Gafford | 16 | Saddiq Bey (+0.093) | 14/104 | +0.085 |
| 154 | Devin Vassell | Tari Eason | 6 | Devin Vassell (+0.078) | 5/87 | +0.059 |

Hindsight found **no better legal pick** at 4 turns (#15, #34, #39, #58) and exactly one at 1 (#10). The owner took the card's #1 at 5 turns (#10, #39, #58, #82, #87) and a Top-5 row at 8 of 13.

### The turns that cost the most (by hindsight gain)

- **#111 Khaman Maluach** (card #95, availability 1.0, note `rookie-proj; 10/6: 17 min / 6 pts off the bench in the 10/5 preseason opener, Ighodaro started (box score; Bright Side of the Sun); 10/8: 25 min / 8 pts / 7 reb / 4 ast off the bench in the 10/7 game at Chicago, Ighodaro started again [SINGLE-SOURCE: box score] (ESPN box score); two games, WO-5 decides; 10/9 (research): the 10/7 line confirmed (8 pts / 7 reb / 4 ast in 25 min, five free throws); Ighodaro has started both games, Maluach 21 mpg off the bench to Ighodaro's 16; Ott: the rotation is not settled, three games left, a third big wanted; Mark Williams about five months per Gambadoro (the team names no timetable); the 24-mpg line already assumes the split, WO-5 decides (SI Suns 10/7, Bright Side of the Sun 10/8, Arizona Sports, BVM Sports, Yahoo); 10/11: started the 10/10 game vs San Antonio, 23 min / 10 pts / 15 reb / 3 ast on 4-9 [SINGLE-SOURCE: box score] (ESPN box score)`): 128 of 203 legal alternatives grade higher — Saddiq Bey +0.275 (drafted #151 by T7); Myles Turner +0.273 (drafted #117 by T4); Collin Gillespie +0.273 (drafted #126 by T6).
- **#63 Damian Lillard** (card #69, availability 0.78, note `inj-achilles-risk (first season back); 10/8: started the 10/7 opener vs Golden State, his first game since the Achilles tear, 19 min / 15 pts, 3-8 from three / 2 stl; the Lillard-Morant backcourt 8-19 with five turnovers, minus-9, Nori: rough around the edges; tag kept by convention for the first season back (ESPN box score; NBA.com Starting 5, Blazer's Edge, SI Blazers, Yahoo, KATU)`): 44 of 247 legal alternatives grade higher — Payton Pritchard +0.260 (drafted #73 by T1); Tyler Herro +0.222 (drafted #72 by T1); Dyson Daniels +0.192 (drafted #68 by T5).
- **#130 Wendell Carter Jr.** (card #21, availability 1.0, note `10/8: started at C in the 10/7 opener at Memphis, 15 min / 13 pts, 3-4 from three [SINGLE-SOURCE: box score] (ESPN box score); 10/12: started the 10/11 game at Cleveland, 19 min / 4 pts / 5 reb / 2 ast on 2-4 [SINGLE-SOURCE: box score] (ESPN box score)`): 29 of 108 legal alternatives grade higher — Saddiq Bey +0.153 (drafted #151 by T7); Devin Vassell +0.135 (drafted #None by None); PJ Washington +0.113 (drafted #140 by T5).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 7 of 11 owner turns: #58 AST+REB; #63 AST+REB (advise); #82 REB+AST (advise); #87 REB (advise); #130 AST+PTS; #135 AST+PTS (advise); #154 AST+PTS+3PTM (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 74 (out of sample) | 52 | 0.429 | 0.519 | **0.178** | 0.250 |
| pooled with every earlier scored room | 1219 | 0.488 | 0.616 | 0.235 | 0.237 |

- this room: BUY NOW 9 rows, 8 gone; TOSS-UP 19 rows, 11 gone; quiet 24 rows, 18 survived.
- pooled: BUY NOW 234 rows, 132 gone; TOSS-UP 268 rows, 142 gone; quiet 716 rows, 522 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 40.41 | 99.98 | 1 | #63 Jarrett Allen, #87 Zach LaVine, #106 Myles Turner, #111 Yaxel Lendeborg, #130 PJ Washington, #135 Saddiq Bey |
| swap#63:Payton Pritchard | 25.71 | 99.38 | 1 | #63 Payton Pritchard |
| swap#111:Saddiq Bey | 24.21 | 99.32 | 1 | #111 Saddiq Bey |
| swap#130:Saddiq Bey | 21.14 | 98.65 | 2 | #130 Saddiq Bey |
| swap#87:Coby White | 20.17 | 98.18 | 2 | #87 Coby White |
| swap#82:Coby White | 19.65 | 98.03 | 2 | #82 Coby White |
| swap#154:Devin Vassell | 19.27 | 97.80 | 2 | #154 Devin Vassell |
| swap#135:Saddiq Bey | 19.03 | 97.53 | 2 | #135 Saddiq Bey |
| swap#106:Saddiq Bey | 18.54 | 97.35 | 2 | #106 Saddiq Bey |
| swap#10:Anthony Edwards | 17.95 | 96.92 | 2 | #10 Anthony Edwards |
| as_drafted | 17.91 | 96.98 | 2 | — |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's exported tracker board (the paste; no tool log exists for this room) (156 picks) and diffed position by position against the recap: **1 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: Jusuf Nurkic; tool names not in the recap: UNKNOWN #112.

| # | tool board | Yahoo recap | seat |
|---|---|---|---|
| 112 | UNKNOWN #112 (raw 'Jurkic') | Jusuf Nurkic | 9 |

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v58`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
