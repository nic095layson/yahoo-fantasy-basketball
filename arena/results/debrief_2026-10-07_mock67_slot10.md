# Mock 67 debrief — slot 10, live public room, deck v49 (rev 269c522, the fixes build — round-11 priced-only card, re-derived Castle/Barrett lines, unsigned men excluded)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_67.json` (md5 `c18bae2654100c24ae9fe17b4d99ebd7`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v49`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **17.51%** (rank 2 of 12) |
| Playoff rate | 97.12% |
| ECW | **5.015** cats/week (rank 2; next 5.129, T4) — favored in 9/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **2** (+8.04; next +12.43) |
| Category rank, weekly model | FG% 3 · FT% 2 · 3PTM 2 · PTS 5 · REB **9** · AST 5 · ST 8 · BLK **10** · TO 3 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Chet Holmgren (+0.022) | 1/296 | owner's own later pick |
| 15 | Tyrese Haliburton | Tyrese Haliburton | 1 | Chet Holmgren (+0.163) | 7/292 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | Domantas Sabonis (+0.054) | 2/274 | owner's own later pick |
| 39 | Derrick White | Derrick White | 1 | none | 0/270 | owner's own later pick |
| 58 | Desmond Bane | Desmond Bane | 1 | OG Anunoby (+0.006) | 1/252 | owner's own later pick |
| 63 | OG Anunoby | Ivica Zubac | 2 | none | 0/248 | -0.035 |
| 82 | De'Aaron Fox | Damian Lillard | 41 | De'Aaron Fox (+0.240) | 71/230 | +0.240 |
| 87 | De'Aaron Fox | Dylan Harper | 58 | De'Aaron Fox (+0.234) | 60/226 | +0.234 |
| 106 | Zach LaVine | Zach LaVine | 1 | Yaxel Lendeborg (+0.008) | 1/208 | owner's own later pick |
| 111 | PJ Washington | DeMar DeRozan | 48 | Daniel Gafford (+0.204) | 67/204 | +0.203 |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/108 | owner's own later pick |
| 135 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | Draymond Green (+0.012) | 2/104 | owner's own later pick |
| 154 | Devin Vassell | Devin Vassell | 1 | Kyle Filipowski (+0.052) | 2/87 | owner's own later pick |

Hindsight found **no better legal pick** at 3 turns (#39, #63, #130) and exactly one at 3 (#10, #58, #106). The owner took the card's #1 at 9 turns (#10, #15, #34, #39, #58, #106, #130, #135, #154) and a Top-5 row at 10 of 13.

### The turns that cost the most (by hindsight gain)

- **#82 Damian Lillard** (card #41, availability 0.78, note `inj-achilles-risk (first season back)`): 71 of 230 legal alternatives grade higher — De'Aaron Fox +0.240 (drafted #92 by T5); Isaiah Hartenstein +0.222 (drafted #94 by T3); Myles Turner +0.219 (drafted #85 by T12).
- **#87 Dylan Harper** (card #58, availability 1.0, note `role 9/30: starter or first guard in with Fox and Castle, Johnson rotating lineups (Yahoo, CBS Sports, Air Alamo)`): 60 of 226 legal alternatives grade higher — De'Aaron Fox +0.234 (drafted #92 by T5); Isaiah Hartenstein +0.216 (drafted #94 by T3); Josh Hart +0.188 (drafted #97 by T1).
- **#111 DeMar DeRozan** (card #48, availability 1.0, note `9/30: bench unit projected, possible starter over Cam Johnson or Braun (Forbes 9/29, SI Nuggets); 10/7: 11 min / 7 pts off the bench in the 10/6 game at Utah, Johnson and Braun started [SINGLE-SOURCE: box score] (ESPN box score)`): 67 of 204 legal alternatives grade higher — Daniel Gafford +0.204 (drafted #132 by T12); Yaxel Lendeborg +0.203 (drafted #126 by T6); Draymond Green +0.194 (drafted #145 by T1).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 4 of 11 owner turns: #58 PTS+REB; #130 REB+BLK; #135 BLK (advise); #154 BLK (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 67 (out of sample) | 51 | 0.445 | 0.588 | **0.186** | 0.242 |
| pooled with every earlier scored room | 858 | 0.477 | 0.624 | 0.247 | 0.235 |

- this room: BUY NOW 9 rows, 8 gone; TOSS-UP 15 rows, 8 gone; quiet 27 rows, 22 survived.
- pooled: BUY NOW 186 rows, 96 gone; TOSS-UP 176 rows, 96 gone; quiet 495 rows, 364 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 37.51 | 99.98 | 1 | #63 OG Anunoby, #82 De'Aaron Fox, #87 Isaiah Hartenstein, #111 Yaxel Lendeborg |
| swap#82:De'Aaron Fox | 24.04 | 99.34 | 1 | #82 De'Aaron Fox |
| swap#87:De'Aaron Fox | 23.95 | 99.33 | 1 | #87 De'Aaron Fox |
| swap#111:Daniel Gafford | 22.58 | 99.16 | 2 | #111 Daniel Gafford |
| swap#15:Chet Holmgren | 22.16 | 98.94 | 2 | #15 Chet Holmgren |
| swap#34:Domantas Sabonis | 18.82 | 97.92 | 2 | #34 Domantas Sabonis |
| swap#10:Chet Holmgren | 18.78 | 97.69 | 2 | #10 Chet Holmgren |
| swap#135:Draymond Green | 18.56 | 97.33 | 2 | #135 Draymond Green |
| swap#154:Kyle Filipowski | 18.25 | 97.71 | 2 | #154 Kyle Filipowski |
| swap#58:OG Anunoby | 17.78 | 97.03 | 2 | #58 OG Anunoby |
| as_drafted | 17.51 | 97.12 | 2 | — |
| swap#106:Yaxel Lendeborg | 17.13 | 96.74 | 2 | #106 Yaxel Lendeborg |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v49`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
