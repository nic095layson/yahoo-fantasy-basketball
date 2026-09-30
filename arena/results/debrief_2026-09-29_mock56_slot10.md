# Mock 56 debrief — slot 10, live public room, deck v31/v32 (rev e2b45ed, the deck drafted against; same pool and engine as v32; Porziņģis veto live)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_56.json` (md5 `e5305ff3b4a1b5c04a18c65e2d67e56c`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v31`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **54.94%** (rank 1 of 12) |
| Playoff rate | 99.95% |
| ECW | **5.760** cats/week (rank 1; next 4.850, Boogie) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+21.52; next +3.83) |
| Category rank, weekly model | FG% 2 · FT% **1** · 3PTM 4 · PTS 5 · REB 6 · AST **10** · ST 3 · BLK **1** · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/298 | owner's own later pick |
| 15 | Tyrese Haliburton | Tyrese Haliburton | 1 | Tyrese Maxey (+0.108) | 14/294 | owner's own later pick |
| 34 | Evan Mobley | Evan Mobley | 1 | none | 0/276 | owner's own later pick |
| 39 | Derrick White | Kyrie Irving | 3 | Desmond Bane (+0.094) | 8/272 | +0.046 |
| 58 | OG Anunoby | OG Anunoby | 1 | none | 0/254 | owner's own later pick |
| 63 | Payton Pritchard | Damian Lillard | 7 | Tyler Herro (+0.074) | 3/250 | +0.028 |
| 82 | Jakob Poeltl | Jakob Poeltl | 1 | none | 0/232 | owner's own later pick |
| 87 | Cameron Johnson | Cameron Johnson | 1 | Miles Bridges (+0.019) | 3/228 | owner's own later pick |
| 106 | Myles Turner | Myles Turner | 1 | Miles Bridges (+0.002) | 1/210 | owner's own later pick |
| 111 | Tari Eason | Tari Eason | 1 | none | 0/206 | owner's own later pick |
| 130 | Christian Braun | Reed Sheppard | 16 | Jordan Poole (+0.101) | 17/190 | owner's own later pick |
| 135 | Christian Braun | Christian Braun | 1 | none | 0/186 | owner's own later pick |
| 154 | Brook Lopez | Brook Lopez | 1 | none | 0/168 | owner's own later pick |

Hindsight found **no better legal pick** at 7 turns (#10, #34, #58, #82, #111, #135, #154) and exactly one at 1 (#106). The owner took the card's #1 at 10 turns (#10, #15, #34, #58, #82, #87, #106, #111, #135, #154) and a Top-5 row at 11 of 13.

### The turns that cost the most (by hindsight gain)

- **#15 Tyrese Haliburton** (card #1, availability 0.78, note `inj-achilles-risk (first season back)`): 14 of 294 legal alternatives grade higher — Tyrese Maxey +0.108 (drafted #18 by Boogie); Donovan Mitchell +0.091 (drafted #16 by Alonzo); Jalen Williams +0.070 (drafted #27 by Matthew).
- **#130 Reed Sheppard** (card #16, availability 1.0, note `bench-role (VanVleet healthy; role recompressed per 9/16 research; synced 9/21)`): 17 of 190 legal alternatives grade higher — Jordan Poole +0.101 (drafted #152 by john); Collin Gillespie +0.066 (drafted #None by None); Quentin Grimes +0.065 (drafted #None by None).
- **#39 Kyrie Irving** (card #3, availability 0.78, note `inj-acl-risk (first season back)`): 8 of 272 legal alternatives grade higher — Desmond Bane +0.094 (drafted #54 by Tom Cruise); Franz Wagner +0.070 (drafted #55 by Boogie); Chet Holmgren +0.062 (drafted #42 by Boogie).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+AST+ST; #63 AST (advise); #82 REB+AST (advise); #87 AST (advise); #106 AST (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 56 (out of sample) | 50 | 0.496 | 0.720 | **0.232** | 0.202 |
| pooled with every earlier scored room | 303 | 0.535 | 0.713 | 0.196 | 0.205 |

- this room: BUY NOW 9 rows, 4 gone; TOSS-UP 11 rows, 5 gone; quiet 30 rows, 25 survived.
- pooled: BUY NOW 45 rows, 28 gone; TOSS-UP 59 rows, 28 gone; quiet 199 rows, 168 survived.

## Championship arms (18,000 CRN seasons each)

> **Bracket restated 2026-09-30 (E14, kit gap audit D-G1).** The table below was produced on the arena's 6-team bracket with byes; the league plays 8 of 12 with no byes. Re-run on the real bracket, same seeds and swaps: as drafted 54.94% → **43.66%** champ, 99.95% → **99.98%** playoff, rank 1 → 1; follow_card_selfconsistent 62.56% → **52.58%**. Every arm, old vs new: `report_2026-09-30_bracket_restate.md`; the JSON beside this file (`m56_arms.json`) now holds the real-bracket numbers.

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 62.56 | 99.99 | 1 | #39 Derrick White, #63 Payton Pritchard, #130 Jordan Poole |
| swap#15:Tyrese Maxey | 59.96 | 99.98 | 1 | #15 Tyrese Maxey |
| swap#130:Jordan Poole | 58.59 | 99.97 | 1 | #130 Jordan Poole |
| swap#39:Desmond Bane | 58.01 | 99.97 | 1 | #39 Desmond Bane |
| swap#63:Tyler Herro | 57.71 | 99.96 | 1 | #63 Tyler Herro |
| swap#87:Miles Bridges | 55.17 | 99.91 | 1 | #87 Miles Bridges |
| as_drafted | 54.94 | 99.95 | 1 | — |
| swap#106:Miles Bridges | 52.76 | 99.88 | 1 | #106 Miles Bridges |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v31`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
