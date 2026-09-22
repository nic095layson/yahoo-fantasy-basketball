# Mock 53 debrief — slot 10, live public room, deck v25 (2026-09-22; possibly v24 — same prices)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_53.json` (md5 `a9da6c92935fadfb1b98951903701397`), reconciled pick-by-pick against Yahoo's recap (156/156 incl. the tool's inserts, unknown-name fixes and undos — `m53_insert_integrity.json`). Pool tag `v25`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **38.53%** (rank 1 of 12) |
| Playoff rate | 99.29% |
| ECW | **5.563** cats/week (rank 1; next 5.274, MichaelH) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **1** (+12.78; next +8.37) |
| Category rank, weekly model | FG% 8 · FT% 3 · 3PTM 3 · PTS 3 · REB 5 · AST 6 · ST 2 · BLK 4 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Jayson Tatum | 17 | Chet Holmgren (+0.129) | 18/298 | owner's own later pick |
| 15 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/294 | owner's own later pick |
| 34 | Evan Mobley | Evan Mobley | 1 | none | 0/276 | owner's own later pick |
| 39 | Jalen Williams | Jalen Williams | 1 | Anthony Davis (+0.024) | 1/272 | owner's own later pick |
| 58 | OG Anunoby | Damian Lillard | 6 | Payton Pritchard (+0.068) | 5/254 | owner's own later pick |
| 63 | OG Anunoby | OG Anunoby | 1 | none | 0/250 | owner's own later pick |
| 82 | Myles Turner | Immanuel Quickley | 20 | Ja Morant (+0.056) | 10/232 | owner's own later pick |
| 87 | Myles Turner | Myles Turner | 1 | none | 0/228 | owner's own later pick |
| 106 | Jakob Poeltl | Jakob Poeltl | 1 | none | 0/210 | owner's own later pick |
| 111 | Cameron Johnson | Reed Sheppard | 16 | Christian Braun (+0.109) | 18/206 | owner's own later pick |
| 130 | Cameron Johnson | Tre Jones | 33 | Christian Braun (+0.141) | 21/188 | +0.131 |
| 135 | Cameron Johnson | Cameron Johnson | 1 | Brook Lopez (+0.000) | 1/184 | -0.012 |
| 154 | Brook Lopez | PJ Washington | 2 | Brook Lopez (+0.060) | 1/167 | +0.060 |

Hindsight found **no better legal pick** at 5 turns (#15, #34, #63, #87, #106) and exactly one at 3 (#39, #135, #154). The owner took the card's #1 at 7 turns (#15, #34, #39, #63, #87, #106, #135) and a Top-5 row at 8 of 13.

### The turns that cost the most (by hindsight gain)

- **#130 Tre Jones** (card #33, availability 1.0, note `backup-role (CHI primary backup PG; live-drafted in mock-51 while poolless)`): 21 of 188 legal alternatives grade higher — Christian Braun +0.141 (drafted #145 by Eran); Tari Eason +0.131 (drafted #137 by Jordan); Brook Lopez +0.101 (drafted #None by None).
- **#10 Jayson Tatum** (card #17, availability 0.78, note `inj-achilles-risk`): 18 of 298 legal alternatives grade higher — Chet Holmgren +0.129 (drafted #23 by MichaelH); Anthony Davis +0.117 (drafted #46 by Tony); Tyrese Haliburton +0.109 (drafted #14 by Anmol).
- **#111 Reed Sheppard** (card #16, availability 1.0, note `bench-role (VanVleet healthy; role recompressed per 9/16 research; synced 9/21)`): 18 of 206 legal alternatives grade higher — Christian Braun +0.109 (drafted #145 by Eran); Tari Eason +0.086 (drafted #137 by Jordan); Brook Lopez +0.077 (drafted #None by None).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 1 (#82 Christian Braun).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 2 of 11 owner turns: #58 AST; #82 AST.

## Survival chips — first out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 53 (out of sample) | 53 | 0.501 | 0.755 | **0.217** | 0.185 |
| pooled with mocks 51 + 52 (refit cards) | 152 | 0.511 | 0.717 | 0.197 | 0.203 |

- this room: BUY NOW 8 rows, 4 gone; TOSS-UP 12 rows, 5 gone; quiet 33 rows, 29 survived.
- pooled: BUY NOW 23 rows, 14 gone; TOSS-UP 32 rows, 16 gone; quiet 97 rows, 84 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 55.59 | 99.97 | 1 | #10 Anthony Davis, #15 Derrick White, #34 Karl-Anthony Towns, #58 Payton Pritchard, #82 Tari Eason, #87 Christian Braun, #106 Myles Turner, #111 Jakob Poeltl, #130 Immanuel Quickley |
| swap#10:Chet Holmgren | 46.26 | 99.72 | 1 | #10 Chet Holmgren |
| swap#130:Christian Braun | 44.23 | 99.80 | 1 | #130 Christian Braun |
| swap#58:Payton Pritchard | 43.14 | 99.52 | 1 | #58 Payton Pritchard |
| swap#111:Christian Braun | 42.21 | 99.65 | 1 | #111 Christian Braun |
| swap#154:Brook Lopez | 41.68 | 99.58 | 1 | #154 Brook Lopez |
| swap#82:Ja Morant | 40.54 | 99.53 | 1 | #82 Ja Morant |
| swap#39:Anthony Davis | 39.18 | 99.47 | 1 | #39 Anthony Davis |
| swap#135:Brook Lopez | 38.71 | 99.34 | 1 | #135 Brook Lopez |
| as_drafted | 38.53 | 99.29 | 1 | — |

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the current pool (v25); the room may have drafted against the previous same-day build (v24) — identical prices, 66 fewer rows.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
