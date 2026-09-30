# Mock 58 debrief — slot 10, live public room, deck v35 (rev 6426a59, the 9/30 daily-pull build)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_58.json` (md5 `84547309be00afd40ed15adcd72ff367`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v35`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **36.75%** (rank 1 of 12) |
| Playoff rate | 99.99% |
| ECW | **5.667** cats/week (rank 1; next 4.932, Elie) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+17.62; next +6.25) |
| Category rank, weekly model | FG% 4 · FT% 5 · 3PTM 4 · PTS 5 · REB 5 · AST 8 · ST 2 · BLK 3 · TO 2 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Tyrese Haliburton | 4 | Tyrese Maxey (+0.007) | 2/301 | owner's own later pick |
| 15 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/297 | owner's own later pick |
| 34 | Anthony Davis | Anthony Davis | 1 | none | 0/279 | owner's own later pick |
| 39 | Jalen Williams | Kyrie Irving | 4 | Derrick White (+0.119) | 9/275 | +0.098 |
| 58 | OG Anunoby | OG Anunoby | 1 | none | 0/257 | owner's own later pick |
| 63 | Payton Pritchard | Payton Pritchard | 1 | none | 0/253 | owner's own later pick |
| 82 | Jakob Poeltl | Miles Bridges | 5 | none | 0/235 | owner's own later pick |
| 87 | Jakob Poeltl | Jakob Poeltl | 1 | none | 0/231 | owner's own later pick |
| 106 | Ja Morant | Ja Morant | 1 | none | 0/214 | owner's own later pick |
| 111 | PJ Washington | PJ Washington | 1 | none | 0/210 | owner's own later pick |
| 130 | Collin Gillespie | Collin Gillespie | 1 | none | 0/192 | owner's own later pick |
| 135 | Daniel Gafford | Herbert Jones | 2 | Quentin Grimes (+0.033) | 3/188 | owner's own later pick |
| 154 | Daniel Gafford | Daniel Gafford | 1 | Kyle Filipowski (+0.001) | 1/171 | owner's own later pick |

Hindsight found **no better legal pick** at 9 turns (#15, #34, #58, #63, #82, #87, #106, #111, #130) and exactly one at 1 (#154). The owner took the card's #1 at 9 turns (#15, #34, #58, #63, #87, #106, #111, #130, #154) and a Top-5 row at 13 of 13.

### The turns that cost the most (by hindsight gain)

- **#39 Kyrie Irving** (card #4, availability 0.78, note `inj-acl-risk (first season back)`): 9 of 275 legal alternatives grade higher — Derrick White +0.119 (drafted #42 by Brandon); Jalen Williams +0.098 (drafted #41 by Mindaugas); Desmond Bane +0.098 (drafted #49 by Alonzo).
- **#135 Herbert Jones** (card #2, availability 1.0, note ``): 3 of 188 legal alternatives grade higher — Quentin Grimes +0.033 (drafted #142 by Noel); Malik Monk +0.015 (drafted #None by None); Saddiq Bey +0.002 (drafted #None by None).
- **#10 Tyrese Haliburton** (card #4, availability 0.78, note `inj-achilles-risk (first season back)`): 2 of 301 legal alternatives grade higher — Tyrese Maxey +0.007 (drafted #11 by Gamze); Jalen Johnson +0.004 (drafted #14 by Gamze); Donovan Mitchell -0.018 (drafted #12 by Alan).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 5 of 11 owner turns: #58 AST+PTS; #63 AST (advise); #82 AST (advise); #87 AST (advise); #106 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 58 (out of sample) | 48 | 0.444 | 0.562 | **0.189** | 0.246 |
| pooled with every earlier scored room | 401 | 0.407 | 0.681 | 0.306 | 0.217 |

- this room: BUY NOW 8 rows, 6 gone; TOSS-UP 16 rows, 11 gone; quiet 24 rows, 20 survived.
- pooled: BUY NOW 137 rows, 57 gone; TOSS-UP 68 rows, 35 gone; quiet 195 rows, 159 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 40.89 | 100.00 | 1 | #10 Tyrese Maxey, #39 Jalen Williams, #82 Zach LaVine |
| swap#39:Derrick White | 40.81 | 99.99 | 1 | #39 Derrick White |
| swap#10:Tyrese Maxey | 38.51 | 99.99 | 1 | #10 Tyrese Maxey |
| swap#135:Quentin Grimes | 37.79 | 99.99 | 1 | #135 Quentin Grimes |
| as_drafted | 36.75 | 99.99 | 1 | — |
| swap#154:Kyle Filipowski | 36.36 | 99.98 | 1 | #154 Kyle Filipowski |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v35`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
