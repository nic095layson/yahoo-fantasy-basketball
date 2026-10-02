# Mock 60 debrief — slot 10, live public room, deck v42 (rev 6ae36ab, the 2026-10-02 second-pull build; v41 carries identical values)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_60.json` (md5 `9023d2d25d41be108230a1a90f77c3fc`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v42`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **33.02%** (rank 1 of 12) |
| Playoff rate | 99.83% |
| ECW | **5.419** cats/week (rank 1; next 4.935, T8) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+8.56; next +4.63) |
| Category rank, weekly model | FG% 4 · FT% 6 · 3PTM **1** · PTS 4 · REB 5 · AST **9** · ST **1** · BLK 5 · TO 2 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/300 | owner's own later pick |
| 15 | Jalen Williams | Kevin Durant | 6 | Chet Holmgren (+0.073) | 4/296 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | Anthony Davis (+0.076) | 2/278 | owner's own later pick |
| 39 | Derrick White | Derrick White | 1 | Anthony Davis (+0.000) | 1/274 | owner's own later pick |
| 58 | Dyson Daniels | Dyson Daniels | 1 | none | 0/256 | owner's own later pick |
| 63 | Tyler Herro | Tyler Herro | 1 | none | 0/252 | owner's own later pick |
| 82 | Mikal Bridges | Mikal Bridges | 1 | Zach LaVine (+0.003) | 2/234 | owner's own later pick |
| 87 | Josh Hart | Josh Hart | 1 | Isaiah Hartenstein (+0.036) | 1/230 | owner's own later pick |
| 106 | PJ Washington | Collin Murray-Boyles | 87 | Daniel Gafford (+0.181) | 57/212 | owner's own later pick |
| 111 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | none | 0/208 | owner's own later pick |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/190 | owner's own later pick |
| 135 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Kyle Filipowski (+0.009) | 2/186 | owner's own later pick |
| 154 | Devin Vassell | Devin Vassell | 1 | Kyle Filipowski (+0.018) | 1/169 | -0.009 |

Hindsight found **no better legal pick** at 5 turns (#10, #58, #63, #111, #130) and exactly one at 3 (#39, #87, #154). The owner took the card's #1 at 11 turns (#10, #34, #39, #58, #63, #82, #87, #111, #130, #135, #154) and a Top-5 row at 11 of 13.

### The turns that cost the most (by hindsight gain)

- **#106 Collin Murray-Boyles** (card #87, availability 1.0, note ``): 57 of 212 legal alternatives grade higher — Daniel Gafford +0.181 (drafted #127 by T7); Draymond Green +0.171 (drafted #139 by T6); John Collins +0.159 (drafted #113 by T8).
- **#34 Jalen Williams** (card #1, availability 1.0, note ``): 2 of 278 legal alternatives grade higher — Anthony Davis +0.076 (drafted #45 by T4); Domantas Sabonis +0.012 (drafted #38 by T11); Desmond Bane -0.019 (drafted #41 by T8).
- **#15 Kevin Durant** (card #6, availability 1.0, note ``): 4 of 296 legal alternatives grade higher — Chet Holmgren +0.073 (drafted #25 by T1); Anthony Davis +0.059 (drafted #45 by T4); Evan Mobley +0.058 (drafted #30 by T6).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 1 (#63 Jarrett Allen).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 3 of 11 owner turns: #58 AST; #63 AST (advise); #82 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 60 (out of sample) | 50 | 0.491 | 0.620 | **0.175** | 0.236 |
| pooled with every earlier scored room | 503 | 0.426 | 0.666 | 0.280 | 0.222 |

- this room: BUY NOW 7 rows, 5 gone; TOSS-UP 13 rows, 8 gone; quiet 30 rows, 24 survived.
- pooled: BUY NOW 150 rows, 66 gone; TOSS-UP 94 rows, 51 gone; quiet 258 rows, 207 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 43.14 | 99.98 | 1 | #15 Jamal Murray, #34 Anthony Davis, #63 Payton Pritchard, #82 Zach LaVine, #87 Mikal Bridges, #106 Daniel Gafford |
| swap#106:Daniel Gafford | 39.49 | 99.97 | 1 | #106 Daniel Gafford |
| swap#34:Anthony Davis | 36.63 | 99.91 | 1 | #34 Anthony Davis |
| swap#15:Chet Holmgren | 35.98 | 99.89 | 1 | #15 Chet Holmgren |
| swap#39:Anthony Davis | 35.09 | 99.82 | 1 | #39 Anthony Davis |
| swap#87:Isaiah Hartenstein | 34.77 | 99.88 | 1 | #87 Isaiah Hartenstein |
| swap#154:Kyle Filipowski | 34.04 | 99.83 | 1 | #154 Kyle Filipowski |
| swap#82:Zach LaVine | 33.91 | 99.85 | 1 | #82 Zach LaVine |
| swap#135:Kyle Filipowski | 33.36 | 99.84 | 1 | #135 Kyle Filipowski |
| as_drafted | 33.02 | 99.83 | 1 | — |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v42`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
