# Mock 54 debrief — slot 10, live public room, deck v28 (rev b150541, the deck drafted against; pre-veto)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_54.json` (md5 `c576efd303176ee0e884fbc1e9050cc8`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v28`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **49.36%** (rank 1 of 12) |
| Playoff rate | 99.73% |
| ECW | **5.552** cats/week (rank 1; next 4.912, gaby) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+13.81; next +1.43) |
| Category rank, weekly model | FG% 4 · FT% 6 · 3PTM 4 · PTS 8 · REB 3 · AST **10** · ST **1** · BLK 3 · TO 4 |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/299 | owner's own later pick |
| 15 | Jalen Johnson | Jalen Johnson | 1 | none | 0/295 | owner's own later pick |
| 34 | Jalen Williams | Jalen Williams | 1 | Derrick White (+0.028) | 1/277 | owner's own later pick |
| 39 | Derrick White | Kyrie Irving | 4 | Derrick White (+0.101) | 4/273 | +0.101 |
| 58 | OG Anunoby | OG Anunoby | 1 | Tyler Herro (+0.046) | 2/255 | owner's own later pick |
| 63 | Payton Pritchard | Payton Pritchard | 1 | Tyler Herro (+0.004) | 1/251 | owner's own later pick |
| 82 | Myles Turner | Jaden McDaniels | 16 | Coby White (+0.124) | 24/233 | owner's own later pick |
| 87 | Myles Turner | Myles Turner | 1 | none | 0/229 | owner's own later pick |
| 106 | Cameron Johnson | Cameron Johnson | 1 | none | 0/211 | owner's own later pick |
| 111 | Jakob Poeltl | Jakob Poeltl | 1 | none | 0/207 | owner's own later pick |
| 130 | Christian Braun | Tari Eason | 2 | Christian Braun (+0.015) | 3/189 | +0.015 |
| 135 | Christian Braun | Ajay Mitchell | 33 | Christian Braun (+0.165) | 30/186 | +0.165 |
| 154 | Brook Lopez | PJ Washington | 3 | Brook Lopez (+0.065) | 3/168 | +0.065 |

Hindsight found **no better legal pick** at 5 turns (#10, #15, #87, #106, #111) and exactly one at 2 (#34, #63). The owner took the card's #1 at 8 turns (#10, #15, #34, #58, #63, #87, #106, #111) and a Top-5 row at 11 of 13.

### The turns that cost the most (by hindsight gain)

- **#135 Ajay Mitchell** (card #33, availability 1.0, note ``): 30 of 186 legal alternatives grade higher — Christian Braun +0.165 (drafted #145 by gaby); Jordan Poole +0.127 (drafted #None by None); Collin Gillespie +0.118 (drafted #140 by Team 5).
- **#82 Jaden McDaniels** (card #16, availability 1.0, note ``): 24 of 233 legal alternatives grade higher — Coby White +0.124 (drafted #89 by Bonani); Miles Bridges +0.092 (drafted #96 by gaby); Zach LaVine +0.091 (drafted #99 by Isaiah).
- **#39 Kyrie Irving** (card #4, availability 0.78, note `inj-acl-risk (first season back)`): 4 of 273 legal alternatives grade higher — Derrick White +0.101 (drafted #45 by Justin); Desmond Bane +0.057 (drafted #48 by gaby); Tyler Herro +0.045 (drafted #75 by Isaiah).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST; #63 AST (advise); #82 AST (advise); #87 AST (advise); #106 AST (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 54 (out of sample) | 50 | 0.534 | 0.780 | **0.168** | 0.172 |
| pooled with every earlier scored room | 202 | 0.517 | 0.733 | 0.190 | 0.196 |

- this room: BUY NOW 9 rows, 6 gone; TOSS-UP 10 rows, 4 gone; quiet 31 rows, 30 survived.
- pooled: BUY NOW 32 rows, 20 gone; TOSS-UP 42 rows, 20 gone; quiet 128 rows, 114 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 60.11 | 99.99 | 1 | #39 Derrick White, #135 Christian Braun |
| swap#135:Christian Braun | 56.93 | 99.94 | 1 | #135 Christian Braun |
| swap#154:Brook Lopez | 53.25 | 99.88 | 1 | #154 Brook Lopez |
| swap#82:Coby White | 52.96 | 99.87 | 1 | #82 Coby White |
| swap#39:Derrick White | 52.71 | 99.89 | 1 | #39 Derrick White |
| swap#34:Derrick White | 50.57 | 99.83 | 1 | #34 Derrick White |
| as_drafted | 49.36 | 99.73 | 1 | — |
| swap#63:Tyler Herro | 48.79 | 99.71 | 1 | #63 Tyler Herro |
| swap#130:Christian Braun | 48.69 | 99.74 | 1 | #130 Christian Braun |
| swap#58:Tyler Herro | 48.62 | 99.73 | 1 | #58 Tyler Herro |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **13 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: Andrew Wiggins, Devin Vassell; tool names not in the recap: UNKNOWN #97, UNKNOWN #118.

| # | tool board | Yahoo recap | seat |
|---|---|---|---|
| 97 | UNKNOWN #97 | Andrew Wiggins | 1 |
| 118 | UNKNOWN #118 | Sandro Mamukelashvili | 3 |
| 119 | Sandro Mamukelashvili | Jalen Green | 2 |
| 120 | Jalen Green | Maxime Raynaud | 1 |
| 121 | Maxime Raynaud | CJ McCollum | 1 |
| 122 | CJ McCollum | Klay Thompson | 2 |
| 123 | Klay Thompson | Ayo Dosunmu | 3 |
| 124 | Ayo Dosunmu | Darryn Peterson | 4 |
| 125 | Darryn Peterson | Brandin Podziemski | 5 |
| 126 | Brandin Podziemski | Keegan Murray | 6 |
| 127 | Keegan Murray | Reed Sheppard | 7 |
| 128 | Reed Sheppard | Kevin Porter Jr. | 8 |
| 129 | Kevin Porter Jr. | Devin Vassell | 9 |

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v28`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
