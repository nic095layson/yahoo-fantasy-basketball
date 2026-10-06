# Mock 61 debrief — slot 10, live public room, deck v44 (rev 583435c, the 2026-10-06 daily-pull build)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_61.json` (md5 `051fee6c1160f7fc75452b08fc3826dc`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v44`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **16.66%** (rank 2 of 12) |
| Playoff rate | 95.97% |
| ECW | **4.940** cats/week (rank 2; next 5.366, T4) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **3** (+3.39; next +9.57) |
| Category rank, weekly model | FG% 6 · FT% 2 · 3PTM **1** · PTS **11** · REB **11** · AST 8 · ST **1** · BLK 7 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Jalen Johnson (+0.013) | 1/300 | owner's own later pick |
| 15 | Donovan Mitchell | Donovan Mitchell | 1 | Chet Holmgren (+0.025) | 2/296 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | none | 0/278 | owner's own later pick |
| 39 | Derrick White | Derrick White | 1 | none | 0/274 | owner's own later pick |
| 58 | OG Anunoby | OG Anunoby | 1 | Tyler Herro (+0.017) | 1/256 | owner's own later pick |
| 63 | Jarrett Allen | Damian Lillard | 65 | Tyler Herro (+0.329) | 67/252 | +0.174 |
| 82 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/234 | owner's own later pick |
| 87 | Mikal Bridges | Mikal Bridges | 1 | Zach LaVine (+0.023) | 2/230 | owner's own later pick |
| 106 | Yaxel Lendeborg | Collin Murray-Boyles | 79 | Draymond Green (+0.207) | 72/212 | +0.205 |
| 111 | Yaxel Lendeborg | Davion Mitchell | 48 | Yaxel Lendeborg (+0.176) | 46/208 | +0.176 |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/191 | -0.024 |
| 135 | Sandro Mamukelashvili | Herbert Jones | 4 | Draymond Green (+0.059) | 5/187 | +0.033 |
| 154 | Devin Vassell | Devin Vassell | 1 | Kyle Filipowski (+0.025) | 1/169 | owner's own later pick |

Hindsight found **no better legal pick** at 4 turns (#34, #39, #82, #130) and exactly one at 3 (#10, #58, #154). The owner took the card's #1 at 9 turns (#10, #15, #34, #39, #58, #82, #87, #130, #154) and a Top-5 row at 10 of 13.

### The turns that cost the most (by hindsight gain)

- **#63 Damian Lillard** (card #65, availability 0.78, note `inj-achilles-risk (first season back)`): 67 of 252 legal alternatives grade higher — Tyler Herro +0.329 (drafted #65 by T8); Payton Pritchard +0.284 (drafted #79 by T7); De'Aaron Fox +0.257 (drafted #76 by T4).
- **#106 Collin Murray-Boyles** (card #79, availability 1.0, note ``): 72 of 212 legal alternatives grade higher — Draymond Green +0.207 (drafted #141 by T4); Yaxel Lendeborg +0.205 (drafted #133 by T12); Daniel Gafford +0.192 (drafted #119 by T2).
- **#111 Davion Mitchell** (card #48, availability 1.0, note `starting-PG role next to Giannis and Bam (NBA.com season preview, SI Heat, Last Word 9/29); repriced 2026-09-30 to the 2025-26 B-Ref line (70/70 starts, 28.6 mpg, 9.3 pts / 6.5 ast / 39% 3PT / .646 FT)`): 46 of 208 legal alternatives grade higher — Yaxel Lendeborg +0.176 (drafted #133 by T12); Sandro Mamukelashvili +0.165 (drafted #142 by T3); Draymond Green +0.146 (drafted #141 by T4).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+REB; #63 AST+REB (advise); #82 REB+AST (advise); #87 AST (advise); #106 REB+AST (advise); #111 AST+REB (advise); #130 REB+PTS (advise); #135 PTS+REB (advise); #154 REB+PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 61 (out of sample) | 51 | 0.494 | 0.549 | **0.168** | 0.248 |
| pooled with every earlier scored room | 554 | 0.432 | 0.655 | 0.270 | 0.226 |

- this room: BUY NOW 7 rows, 6 gone; TOSS-UP 14 rows, 8 gone; quiet 30 rows, 21 survived.
- pooled: BUY NOW 157 rows, 72 gone; TOSS-UP 108 rows, 59 gone; quiet 288 rows, 228 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 34.49 | 99.91 | 1 | #63 Jarrett Allen, #82 Zach LaVine, #87 Isaiah Hartenstein, #106 Sandro Mamukelashvili, #111 Cason Wallace, #130 Yaxel Lendeborg, #135 Saddiq Bey |
| swap#63:Tyler Herro | 25.73 | 99.26 | 2 | #63 Tyler Herro |
| swap#106:Draymond Green | 22.92 | 98.60 | 2 | #106 Draymond Green |
| swap#111:Yaxel Lendeborg | 20.69 | 98.35 | 2 | #111 Yaxel Lendeborg |
| swap#15:Chet Holmgren | 18.06 | 96.71 | 2 | #15 Chet Holmgren |
| swap#87:Zach LaVine | 17.60 | 95.95 | 2 | #87 Zach LaVine |
| swap#135:Draymond Green | 17.11 | 96.67 | 2 | #135 Draymond Green |
| swap#58:Tyler Herro | 16.72 | 95.69 | 2 | #58 Tyler Herro |
| as_drafted | 16.66 | 95.97 | 2 | — |
| swap#154:Kyle Filipowski | 16.66 | 95.94 | 2 | #154 Kyle Filipowski |
| swap#10:Jalen Johnson | 16.46 | 96.29 | 2 | #10 Jalen Johnson |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v44`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
