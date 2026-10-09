# Mock 73 debrief — slot 10, live public room, deck v54 (rev 03cba0a, LIVE mode in a public Yahoo room; engine, values, prices and pool identical to v53)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_73.json` (md5 `69a8c03ee2c922c9a14b5d6aea8bed1d`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v53`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **34.17%** (rank 1 of 12) |
| Playoff rate | 99.94% |
| ECW | **5.497** cats/week (rank 1; next 5.080, T2) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+14.02; next +6.99) |
| Category rank, weekly model | FG% 5 · FT% 6 · 3PTM 2 · PTS 7 · REB 4 · AST **11** · ST **1** · BLK 4 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/295 | owner's own later pick |
| 15 | Donovan Mitchell | Donovan Mitchell | 1 | none | 0/291 | owner's own later pick |
| 34 | Chet Holmgren | Anthony Davis | 2 | Chet Holmgren (+0.014) | 1/273 | +0.014 |
| 39 | Derrick White | Derrick White | 1 | none | 0/269 | owner's own later pick |
| 58 | OG Anunoby | Dyson Daniels | 2 | Tyler Herro (+0.007) | 2/251 | owner's own later pick |
| 63 | Payton Pritchard | OG Anunoby | 2 | none | 0/247 | owner's own later pick |
| 82 | Payton Pritchard | Payton Pritchard | 1 | none | 0/229 | owner's own later pick |
| 87 | Josh Hart | Dylan Harper | 59 | Immanuel Quickley (+0.131) | 50/225 | +0.127 |
| 106 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | Myles Turner (+0.004) | 1/207 | owner's own later pick |
| 111 | Sandro Mamukelashvili | Aaron Gordon | 2 | Myles Turner (+0.001) | 1/203 | owner's own later pick |
| 130 | PJ Washington | Sandro Mamukelashvili | 2 | none | 0/108 | owner's own later pick |
| 135 | PJ Washington | PJ Washington | 1 | Kyle Filipowski (+0.005) | 1/104 | owner's own later pick |
| 154 | Christian Braun | Tari Eason | 9 | Kyle Filipowski (+0.086) | 11/88 | +0.049 |

Hindsight found **no better legal pick** at 6 turns (#10, #15, #39, #63, #82, #130) and exactly one at 4 (#34, #106, #111, #135). The owner took the card's #1 at 6 turns (#10, #15, #39, #82, #106, #135) and a Top-5 row at 11 of 13.

### The turns that cost the most (by hindsight gain)

- **#87 Dylan Harper** (card #59, availability 1.0, note `role 9/30: starter or first guard in with Fox and Castle, Johnson rotating lineups (Yahoo, CBS Sports, Air Alamo); 10/9: started the 10/8 game vs Atlanta, 19 min / 16 pts / 4 reb / 4 ast on 5-7, 3-5 from three (ESPN box score; Yahoo, News 4 San Antonio, Eurohoops)`): 50 of 225 legal alternatives grade higher — Immanuel Quickley +0.131 (drafted #98 by T2); Myles Turner +0.127 (drafted #120 by T1); Josh Hart +0.127 (drafted #88 by T9).
- **#154 Tari Eason** (card #9, availability 1.0, note `repriced 2026-09-29: FG% and stocks to the 2024-26 blend (2025-26 .416 / 1.2 stl / 0.5 blk vs 2024-25 .487 / 1.7 / 0.9 - B-Ref); bench role, minutes trending up, 5yr/$81.5M (The Dream Shake, CBS Sports); 10/9: off the bench in the 10/9 game in Macao at Dallas, 24 min / 20 pts / 9 reb / 2 ast / 2 stl on 6-10 [SINGLE-SOURCE: box score] (ESPN box score)`): 11 of 88 legal alternatives grade higher — Kyle Filipowski +0.086 (drafted #None by None); Draymond Green +0.071 (drafted #None by None); Nikola Vucevic +0.052 (drafted #None by None).
- **#34 Anthony Davis** (card #2, availability 0.78, note `inj-risk; 10/9: started the 10/8 game at New York, 17 min / 16 pts / 7 reb / 2 ast on 6-11 (ESPN box score; Bullets Forever/Yahoo, Sportando, TalkBasket); 10/9 (research): healthy and a full camp participant per the Wizards beat (Finberg via RotoWire 10/1), the debut 16 pts in 17 min at New York (CBS Sports has 17); no minutes restriction or availability note found in October; inj-risk stays, 20 games last season (RotoWire, CBS Sports, Yahoo)`): 1 of 273 legal alternatives grade higher — Chet Holmgren +0.014 (drafted #36 by T12); Domantas Sabonis -0.024 (drafted #35 by T11); Franz Wagner -0.106 (drafted #51 by T3).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST; #63 AST (advise); #82 AST (advise); #87 AST (advise); #106 AST (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 73 (out of sample) | 49 | 0.474 | 0.612 | **0.193** | 0.237 |
| pooled with every earlier scored room | 1167 | 0.491 | 0.620 | 0.237 | 0.236 |

- this room: BUY NOW 9 rows, 7 gone; TOSS-UP 13 rows, 6 gone; quiet 27 rows, 21 survived.
- pooled: BUY NOW 225 rows, 124 gone; TOSS-UP 249 rows, 131 gone; quiet 692 rows, 504 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 40.44 | 99.98 | 1 | #34 Chet Holmgren, #87 Josh Hart, #154 Cameron Johnson |
| swap#87:Immanuel Quickley | 37.78 | 99.97 | 1 | #87 Immanuel Quickley |
| swap#111:Myles Turner | 36.25 | 99.96 | 1 | #111 Myles Turner |
| swap#154:Kyle Filipowski | 36.21 | 99.97 | 1 | #154 Kyle Filipowski |
| swap#34:Chet Holmgren | 35.43 | 99.94 | 1 | #34 Chet Holmgren |
| swap#106:Myles Turner | 35.11 | 99.96 | 1 | #106 Myles Turner |
| as_drafted | 34.17 | 99.94 | 1 | — |
| swap#135:Kyle Filipowski | 33.69 | 99.93 | 1 | #135 Kyle Filipowski |
| swap#58:Tyler Herro | 31.82 | 99.88 | 1 | #58 Tyler Herro |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v53`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
