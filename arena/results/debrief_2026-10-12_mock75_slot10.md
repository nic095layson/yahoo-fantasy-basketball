# Mock 75 debrief — slot 10, live public room, deck v59 (rev f918062, LIVE mode in a public Yahoo room; the 10/12 ADP refresh page, pool and values identical to v58)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_75.json` (md5 `2dbbc53780830fdb7055c9f844a1af00`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v58`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **29.39%** (rank 2 of 12) |
| Playoff rate | 99.92% |
| ECW | **5.486** cats/week (rank 2; next 5.508, T1) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **1** (+12.39; next +10.74) |
| Category rank, weekly model | FG% 5 · FT% 5 · 3PTM 5 · PTS **9** · REB 3 · AST 6 · ST 3 · BLK 3 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Jalen Johnson (+0.003) | 1/295 | owner's own later pick |
| 15 | Tyrese Haliburton | Tyrese Haliburton | 1 | none | 0/291 | owner's own later pick |
| 34 | Anthony Davis | Anthony Davis | 1 | none | 0/273 | owner's own later pick |
| 39 | Derrick White | Derrick White | 1 | none | 0/269 | owner's own later pick |
| 58 | Payton Pritchard | OG Anunoby | 2 | Tyler Herro (+0.000) | 1/251 | owner's own later pick |
| 63 | Payton Pritchard | Payton Pritchard | 1 | Tyler Herro (+0.009) | 1/247 | owner's own later pick |
| 82 | Coby White | Coby White | 1 | none | 0/229 | owner's own later pick |
| 87 | Isaiah Hartenstein | Day'Ron Sharpe | 3 | Zach LaVine (+0.028) | 2/225 | owner's own later pick |
| 106 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/207 | owner's own later pick |
| 111 | Devin Vassell | Rui Hachimura | 67 | Aaron Gordon (+0.159) | 59/203 | +0.149 |
| 130 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | none | 0/108 | owner's own later pick |
| 135 | Devin Vassell | Devin Vassell | 1 | none | 0/104 | owner's own later pick |
| 154 | Draymond Green | Draymond Green | 1 | none | 0/86 | -0.046 |

Hindsight found **no better legal pick** at 8 turns (#15, #34, #39, #82, #106, #130, #135, #154) and exactly one at 3 (#10, #58, #63). The owner took the card's #1 at 10 turns (#10, #15, #34, #39, #63, #82, #106, #130, #135, #154) and a Top-5 row at 12 of 13.

### The turns that cost the most (by hindsight gain)

- **#111 Rui Hachimura** (card #67, availability 1.0, note `role 9/30: starter (SI Clippers, Yardbarker); 10/9: started the 10/4 opener vs Golden State, 15 min / 21 pts / 5 reb / 1 blk on 8-11, 4-5 from three (ESPN box score; CBS Sports, Yardbarker, Yahoo); 10/9 (research): the second scoring option while Ingram misses at least the 10/21 opener, Lue will push Garland and him; one game, the 28-mpg line is Sunday's WO-5 question (CBS Sports, Yardbarker, Basketnews 10/5); 10/11: started the 10/10 game at Toronto in Vancouver, 19 min / 14 pts / 3 reb / 1 ast on 3-8 [SINGLE-SOURCE: box score] (ESPN box score)`): 59 of 203 legal alternatives grade higher — Aaron Gordon +0.159 (drafted #123 by T3); Collin Gillespie +0.159 (drafted #138 by T7); Saddiq Bey +0.155 (drafted #156 by T12).
- **#87 Day'Ron Sharpe** (card #3, availability 1.0, note `starting-center role (Yahoo Nets camp breakdown, TalkBasket); twinned 2026-09-30 to the kit's 28.2-mpg starter line (built from the 2025-26 B-Ref per-36: 16.8 pts / 12.8 reb / 4.5 ast / 2.1 stl); 10/7: started at C in the 10/6 preseason opener at Charlotte, 18 min / 8 pts / 7 reb / 3 ast / 2 blk [SINGLE-SOURCE: box score] (ESPN box score); 10/9: did not play the 10/8 game vs Philadelphia, left shoulder soreness after playing the opener; Wagner started in his place; day-to-day on ESPN's feed with a 10/12 estimate (ESPN game feed; NBC Sports, NetsDaily)`): 2 of 225 legal alternatives grade higher — Zach LaVine +0.028 (drafted #101 by T5); Jalen Suggs +0.024 (drafted #96 by T1); PJ Washington -0.012 (drafted #120 by T1).
- **#63 Payton Pritchard** (card #1, availability 1.0, note `10/9: did not play the 10/8 opener at Cleveland (undisclosed on ESPN's feed) (ESPN game feed; CelticsBlog, NBC Sports Boston); 10/11: off the bench in the 10/10 game vs Philadelphia, 24 min / 25 pts / 4 reb / 7 ast / 4 to on 7-12, 5-8 from three (ESPN box score; NBC Sports Boston, CelticsBlog; led Boston)`): 1 of 247 legal alternatives grade higher — Tyler Herro +0.009 (drafted #80 by T8); De'Aaron Fox -0.038 (drafted #72 by T1); Zach LaVine -0.107 (drafted #101 by T5).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 8 of 11 owner turns: #58 PTS+AST+ST; #63 AST+PTS (advise); #82 PTS+AST (advise); #106 PTS; #111 PTS (advise); #130 AST+PTS (advise); #135 AST+PTS (advise); #154 AST+PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 75 (out of sample) | 49 | 0.499 | 0.633 | **0.185** | 0.232 |
| pooled with every earlier scored room | 1268 | 0.489 | 0.617 | 0.233 | 0.236 |

- this room: BUY NOW 5 rows, 5 gone; TOSS-UP 13 rows, 6 gone; quiet 31 rows, 24 survived.
- pooled: BUY NOW 239 rows, 137 gone; TOSS-UP 281 rows, 148 gone; quiet 747 rows, 546 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 35.79 | 99.96 | 1 | #87 Jalen Suggs, #111 Sandro Mamukelashvili |
| swap#111:Aaron Gordon | 34.64 | 99.97 | 1 | #111 Aaron Gordon |
| swap#10:Jalen Johnson | 30.63 | 99.92 | 2 | #10 Jalen Johnson |
| swap#58:Tyler Herro | 29.96 | 99.89 | 2 | #58 Tyler Herro |
| swap#87:Zach LaVine | 29.52 | 99.88 | 2 | #87 Zach LaVine |
| as_drafted | 29.39 | 99.92 | 2 | — |
| swap#63:Tyler Herro | 29.23 | 99.90 | 2 | #63 Tyler Herro |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v58`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
