# Mock 57 debrief — slot 10, live public room, deck v34 (rev 0dfbe77; engine and pool identical to v33)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_57.json` (md5 `de73d84f7f60ae858153f801f1319d59`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v33`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **35.23%** (rank 1 of 12) |
| Playoff rate | 97.29% |
| ECW | **5.271** cats/week (rank 1; next 5.052, Kei) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **1** (+13.52; next +6.30) |
| Category rank, weekly model | FG% 6 · FT% **1** · 3PTM 3 · PTS 5 · REB 3 · AST **9** · ST 3 · BLK 8 · TO 4 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Jayson Tatum | 16 | Chet Holmgren (+0.172) | 17/302 | owner's own later pick |
| 15 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Jalen Johnson (+0.022) | 2/298 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | Anthony Davis (+0.064) | 3/280 | owner's own later pick |
| 39 | Derrick White | Kyrie Irving | 5 | Derrick White (+0.149) | 7/276 | +0.149 |
| 58 | OG Anunoby | Damian Lillard | 7 | Payton Pritchard (+0.044) | 2/258 | owner's own later pick |
| 63 | OG Anunoby | OG Anunoby | 1 | none | 0/254 | owner's own later pick |
| 82 | Jakob Poeltl | Jakob Poeltl | 1 | none | 0/236 | -0.066 |
| 87 | Miles Bridges | Jaden McDaniels | 7 | Miles Bridges (+0.093) | 8/232 | +0.093 |
| 106 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/215 | owner's own later pick |
| 111 | Collin Gillespie | Collin Gillespie | 1 | Draymond Green (+0.008) | 2/211 | owner's own later pick |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/193 | owner's own later pick |
| 135 | Devin Vassell | Devin Vassell | 1 | Draymond Green (+0.020) | 3/190 | owner's own later pick |
| 154 | Quentin Grimes | Quentin Grimes | 1 | Draymond Green (+0.013) | 3/173 | owner's own later pick |

Hindsight found **no better legal pick** at 4 turns (#63, #82, #106, #130) and exactly one at 0 (—). The owner took the card's #1 at 9 turns (#15, #34, #63, #82, #106, #111, #130, #135, #154) and a Top-5 row at 10 of 13.

### The turns that cost the most (by hindsight gain)

- **#10 Jayson Tatum** (card #16, availability 0.78, note `inj-achilles-risk`): 17 of 302 legal alternatives grade higher — Chet Holmgren +0.172 (drafted #22 by Kei); Jalen Johnson +0.156 (drafted #16 by Jake); Anthony Davis +0.116 (drafted #38 by Alwin).
- **#39 Kyrie Irving** (card #5, availability 0.78, note `inj-acl-risk (first season back)`): 7 of 276 legal alternatives grade higher — Derrick White +0.149 (drafted #51 by Kei); Franz Wagner +0.067 (drafted #54 by Jeff); Desmond Bane +0.065 (drafted #53 by Matan).
- **#87 Jaden McDaniels** (card #7, availability 1.0, note ``): 8 of 232 legal alternatives grade higher — Miles Bridges +0.093 (drafted #99 by Kei); Myles Turner +0.067 (drafted #93 by Nathan); Zach LaVine +0.039 (drafted #100 by Nathan).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 BLK+AST; #63 BLK (advise); #82 BLK+REB+AST (advise); #87 AST+BLK (advise); #106 AST+BLK (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 57 (out of sample) | 51 | 0.518 | 0.608 | **0.178** | 0.238 |
| pooled with every earlier scored room | 354 | 0.400 | 0.698 | 0.324 | 0.211 |

- this room: BUY NOW 6 rows, 5 gone; TOSS-UP 12 rows, 7 gone; quiet 33 rows, 25 survived.
- pooled: BUY NOW 130 rows, 51 gone; TOSS-UP 53 rows, 24 gone; quiet 170 rows, 138 survived.

## Championship arms (18,000 CRN seasons each)

> **Bracket restated 2026-09-30 (E14, kit gap audit D-G1).** The table below was produced on the arena's 6-team bracket with byes; the league plays 8 of 12 with no byes. Re-run on the real bracket, same seeds and swaps: as drafted 35.23% → **27.44%** champ, 97.29% → **99.30%** playoff, rank 1 → 1; follow_card_selfconsistent 52.96% → **41.43%**. Every arm, old vs new: `report_2026-09-30_bracket_restate.md`; the JSON beside this file (`m57_arms.json`) now holds the real-bracket numbers.

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 52.96 | 99.82 | 1 | #10 Tyrese Haliburton, #34 Anthony Davis, #39 Derrick White, #58 Payton Pritchard, #87 Zach LaVine, #111 Cason Wallace |
| swap#10:Chet Holmgren | 45.06 | 99.33 | 1 | #10 Chet Holmgren |
| swap#39:Derrick White | 42.63 | 98.83 | 1 | #39 Derrick White |
| swap#87:Miles Bridges | 41.01 | 98.36 | 1 | #87 Miles Bridges |
| swap#34:Anthony Davis | 39.29 | 98.37 | 1 | #34 Anthony Davis |
| swap#58:Payton Pritchard | 37.56 | 98.07 | 1 | #58 Payton Pritchard |
| swap#135:Draymond Green | 36.75 | 97.76 | 1 | #135 Draymond Green |
| swap#154:Draymond Green | 36.01 | 97.62 | 1 | #154 Draymond Green |
| swap#111:Draymond Green | 35.98 | 97.62 | 1 | #111 Draymond Green |
| as_drafted | 35.23 | 97.29 | 1 | — |
| swap#15:Jalen Johnson | 35.12 | 97.29 | 1 | #15 Jalen Johnson |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v33`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
