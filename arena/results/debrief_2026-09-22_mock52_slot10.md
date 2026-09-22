# Mock 52 debrief — slot 10, live public room, deck v23 (2026-09-22)

**Fingerprint:** owner slot 10, 156 picks, Yahoo public mock (random humans, not the cast), state `arena/data/states/draft_state_52.json` (md5 `ba6c2a94fa41b02d7871fb42d13cc923`, reconciled pick-by-pick against Yahoo's recap 2026-09-22: 156/156 match, including the tool's one insert, four unknown-name corrections and two halted re-sends). Deck used: the published v23 artifact (pool 264, sha c1f87ac1db09) — proven by the log's FULL TILT / Retarget lines, which only the pre-2026-09-21 advisor renders, and by two live-drafted names the pool lacks (Daniss Jenkins, Gui Santos; seats 4 and 11 play 12 men in every simulation here). Punt box: empty through #39, then the advisor's FULL TILT (FG%+AST, "clear path 6/7") and an immediate Retarget to FG%+TO ("+2.9 roster fit"), both right after the owner's #39; no later change.

**Method.** Card reconstructed two ways at all 13 owner turns — the Python port (`live_retro.py replay`, the check_parity port of decwScores) and the deck's own JS under node (`live_deckcard.py`, DOM survival model and 🎯 pin reproduced from source) — and they agree on the Top-5 names and blend scores at 13/13 turns (max |Δds| 0.0000). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H (draft_50/51 method), championships (18,000 seasons, seeds 11/23/47, CRN). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`, the owner's own later picks screened as degenerate. The generalized harnesses reproduce mock 51's landed final/replay/hindsight byte-for-byte.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **47.94%** (rank 1 of 12) |
| Playoff rate | 99.81% |
| ECW | **5.634** cats/week (rank 1; next 5.195, David (seat 8)) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+20.84; next +3.78) |
| Category rank, weekly model | FG% **9** · FT% 4 · 3PTM 3 · PTS **1** · REB 5 · AST **10** · ST **1** · BLK 4 · TO 6 |

Mock 51 from the same seat read ECW 5.610 / rank 1 / 11 of 11; this room reads 5.634 / rank 1 / 11 of 11. Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the v23 deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Tuned 🎯 = the same turn on the tuned deck (PRs #34 + #37: ΔECW tie-break, pin gate); "=" when unchanged. Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took at a later turn (screened).

| pick | card 🎯 | tuned 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | = | Jayson Tatum | 15 | Jalen Johnson (+0.154) | 18/234 | +0.105 |
| 15 | Karl-Anthony Towns | Evan Mobley | Donovan Mitchell | 8 | Derrick White (+0.029) | 3/230 | -0.010 |
| 34 | Anthony Davis | = | Anthony Davis | 1 | Derrick White (+0.013) | 1/212 | owner's own later pick |
| 39 | Jalen Williams | = | Kyrie Irving | 5 | Derrick White (+0.139) | 8/208 | +0.049 |
| 58 | Kristaps Porzingis | Franz Wagner | Franz Wagner | 1 | Tyler Herro (+0.001) | 1/190 | owner's own later pick |
| 63 | OG Anunoby | = | Dyson Daniels | 2 | none | 0/186 | -0.041 |
| 82 | Jakob Poeltl | = | Jakob Poeltl | 1 | Isaiah Hartenstein (+0.010) | 1/168 | owner's own later pick |
| 87 | Cameron Johnson | = | Myles Turner | 2 | none | 0/164 | owner's own later pick |
| 106 | Cameron Johnson | = | Miles Bridges | 4 | Brook Lopez (+0.002) | 1/146 | owner's own later pick |
| 111 | Cameron Johnson | = | Cameron Johnson | 1 | none | 0/142 | owner's own later pick |
| 130 | Christian Braun | = | Jordan Poole | 3 | Christian Braun (+0.053) | 4/125 | +0.053 |
| 135 | Christian Braun | = | Tari Eason | 3 | Christian Braun (+0.053) | 4/121 | +0.053 |
| 154 | Christian Braun | = | PJ Washington | 2 | Christian Braun (+0.033) | 1/104 | +0.033 |

Hindsight found **no better legal pick** at 3 turns (#63, #87, #111) and exactly one at 5 (#34, #58, #82, #106, #154). The owner took the card's #1 at 4 turns and a Top-5 row at 11 of 13.

### The turns that cost something

- **#10 Jayson Tatum** (card #15, availability 0.78, note `inj-achilles-risk`): 18 of 234 legal alternatives grade higher. Jalen Johnson +0.154 (drafted #11 by Jack); Tyrese Haliburton +0.144 (drafted #14 by Jack); Karl-Anthony Towns +0.105 (drafted #17 by David (seat 8)).
- **#39 Kyrie Irving** (card #5, availability 0.78, note `inj-acl-risk (first season back)`): 8 of 208 legal alternatives grade higher. Derrick White +0.139 (drafted #43 by Mark); Payton Pritchard +0.065 (drafted #80 by David (seat 8)); Desmond Bane +0.060 (drafted #56 by David (seat 8)).
- **Christian Braun, passed three times** (#130, #135, #154; card 🎯 each time, gains +0.053, +0.053, +0.033): he went #156, the last pick of the draft, to Michael.

### What the card got right, live

- #34 Anthony Davis and #58 Franz Wagner and #82 Jakob Poeltl and #111 Cameron Johnson: the owner took the card's #1; hindsight confirms each within 0.013 of the best legal alternative.
- **#58 is D51R-4 vindicated live.** The v23 deck moved the 🎯 off Franz onto an urgent Shot-block C pin, Kristaps Porziņģis (availability 0.78) — LAST CALL. The owner ignored it and took Franz (card #1, hindsight: 1 better alternative of 190, by +0.001). The tuned deck withholds that pin (`availability 0.78`) and keeps the 🎯 on Franz.
- #63 Dyson Daniels and #87 Myles Turner were card #2 and turned out hindsight-best (0 better alternatives); the card's #1 at those turns (Anunoby, Cam Johnson) grades −0.041 and screened respectively.
- #15: the tuned deck's ΔECW tie-break flips the 🎯 from Towns to Mobley (ΔECW 2.236 vs 2.179); the owner took Donovan Mitchell (card #8), which hindsight grades within 0.03 of the best alternative anyway.

## Punt advisor — the buttons the owner clicked vs the room-relative read (D51R-3)

`live_advisor.py` reproduces both log lines from the engine: right after #39 (roster 4, box empty) the old advisor shows FULL TILT FG%·AST with path 6/7; on the box that click set (FG%+AST) the old coherence strip reads inverted and offers Retarget (AST in, punt TO, +2.92 fit). The room-relative read at the same two moments: no lean (AST beats 46% of the room with Kyrie aboard), and on the FG%+AST box "drifting: punting AST though this roster beats 46% of the room in it — smaller box".

| owner turn | box | TO beats | old strip | new strip |
|---|---|---|---|---|
| #58 | FG%+TO | 90% | aligned | inverted: punt AST for TO (+0.80 cats/wk) |
| #63 | FG%+TO | 66% | aligned | inverted: punt REB for TO (+0.34 cats/wk) |
| #82 | FG%+TO | 80% | aligned | inverted: punt REB for TO (+0.58 cats/wk) |
| #87 | FG%+TO | 68% | aligned | inverted: drop TO (+0.68 cats/wk) |
| #106 | FG%+TO | 81% | aligned | inverted: punt AST for TO (+0.65 cats/wk) |
| #111 | FG%+TO | 67% | aligned | inverted: punt AST for TO (+0.38 cats/wk) |
| #130 | FG%+TO | 74% | aligned | inverted: punt AST for TO (+0.53 cats/wk) |
| #135 | FG%+TO | 52% | aligned | inverted: drop TO (+0.52 cats/wk) |
| #154 | FG%+TO | 62% | aligned | inverted: punt AST for TO (+0.37 cats/wk) |

At all 9 owner turns with the FG%+TO box the old strip read *aligned* while the roster was beating 52%–90% of the room in the punted TO; the new strip reads *inverted* at 9 of them. Mock 51's finding, live again — and this time the box was the old advisor's own product. TO finished ranked 6 by the weekly model (z-sum 8) after the late picks stopped protecting it.

## Survival chips — calibration data for the refit (D51R-1)

| room | rows | mean predicted survival | realized | Brier |
|---|---|---|---|---|
| mock 52 (v23 deck, chips still live) | 50 | 0.043 | 0.700 | 0.655 |
| pooled with mock 51 | 98 | 0.044 | 0.694 | 0.651 |

BUY NOW on 47 of 50 scored rows at a mean 0.028 predicted survival; 33 of those players were still there at the owner's next turn. Second live room of the two the owner set as the refit threshold; the chips stay suspended (PR #34) until the refit lands.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 56.92 | 99.96 | 1 | #10 Karl-Anthony Towns, #39 Jalen Williams, #58 OG Anunoby, #63 Payton Pritchard, #106 Christian Braun, #130 Miles Bridges, #135 Cason Wallace |
| swap#10:Jalen Johnson | 52.82 | 99.90 | 1 | #10 Jalen Johnson |
| swap#39:Derrick White | 52.44 | 99.91 | 1 | #39 Derrick White |
| swap#130:Christian Braun | 49.53 | 99.87 | 1 | #130 Christian Braun |
| swap#135:Christian Braun | 48.67 | 99.83 | 1 | #135 Christian Braun |
| swap#154:Christian Braun | 48.42 | 99.83 | 1 | #154 Christian Braun |
| swap#15:Derrick White | 48.27 | 99.83 | 1 | #15 Derrick White |
| swap#106:Brook Lopez | 48.10 | 99.79 | 1 | #106 Brook Lopez |
| as_drafted | 47.94 | 99.81 | 1 | — |
| swap#34:Derrick White | 47.58 | 99.78 | 1 | #34 Derrick White |
| swap#58:Tyler Herro | 47.58 | 99.73 | 1 | #58 Tyler Herro |
| swap#82:Isaiah Hartenstein | 47.01 | 99.75 | 1 | #82 Isaiah Hartenstein |

## Limits

- Seats 4 and 11 simulate with 12 men (Daniss Jenkins and Gui Santos have no pool row), which flatters the owner against those two seats only; both were already the room's weakest by ECW.
- Random public room, not the league cast: the field's weakness is in every denominator above.
- The punt box after #39 is taken from the tool log (no later Retarget was logged).

