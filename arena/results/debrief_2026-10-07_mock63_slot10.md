# Mock 63 debrief — slot 10, deck MOCK mode vs the league cast, deck v47 (rev fca8f7c, the 10/7 daily-pull build, the cast on the real seating; the v44 pool with the 10/6 prices)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_63.json` (md5 `d9516e0c5d41aaaaa5148abfdf103c22`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v44`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **23.33%** (rank 2 of 12) |
| Playoff rate | 98.37% |
| ECW | **5.169** cats/week (rank 1; next 5.121, Oblena) — favored in 10/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **2** (+4.57; next +11.15) |
| Category rank, weekly model | FG% **1** · FT% 6 · 3PTM 4 · PTS **9** · REB 6 · AST 3 · ST 5 · BLK 4 · TO 3 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Jalen Johnson | Jalen Johnson | 1 | none | 0/300 | owner's own later pick |
| 15 | Jamal Murray | Jamal Murray | 1 | Chet Holmgren (+0.060) | 10/296 | owner's own later pick |
| 34 | Derrick White | Derrick White | 1 | none | 0/278 | owner's own later pick |
| 39 | Onyeka Okongwu | Onyeka Okongwu | 1 | OG Anunoby (+0.041) | 1/274 | owner's own later pick |
| 58 | Payton Pritchard | Payton Pritchard | 1 | Tyler Herro (+0.005) | 1/256 | owner's own later pick |
| 63 | De'Aaron Fox | De'Aaron Fox | 1 | none | 0/252 | owner's own later pick |
| 82 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/235 | owner's own later pick |
| 87 | Yaxel Lendeborg | Yaxel Lendeborg | 1 | PJ Washington (+0.005) | 1/231 | owner's own later pick |
| 106 | Sandro Mamukelashvili | Sandro Mamukelashvili | 1 | none | 0/213 | owner's own later pick |
| 111 | Herbert Jones | Herbert Jones | 1 | Saddiq Bey (+0.023) | 1/209 | owner's own later pick |
| 130 | Collin Gillespie | Collin Gillespie | 1 | Saddiq Bey (+0.045) | 2/191 | owner's own later pick |
| 135 | Daniel Gafford | Daniel Gafford | 1 | none | 0/187 | owner's own later pick |
| 154 | Cam Thomas | Cam Thomas | 1 | Santi Aldama (+0.013) | 2/169 | -0.021 |

Hindsight found **no better legal pick** at 6 turns (#10, #34, #63, #82, #106, #135) and exactly one at 4 (#39, #58, #87, #111). The owner took the card's #1 at 13 turns (#10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154) and a Top-5 row at 13 of 13.

### The turns that cost the most (by hindsight gain)

- **#15 Jamal Murray** (card #1, availability 1.0, note `healthy (75 GP in 2025-26; the 9/8 inj-achilles-risk tag was a Dejounte Murray garble - removed 2026-09-28); 10/5: DNP the 10/4 preseason opener for personal reasons (box score; Denver Stiffs, Deseret); 10/7: started the 10/6 game at Utah after missing the opener for personal reasons, 16 min / 4 pts / 3 ast [SINGLE-SOURCE: box score] (ESPN box score)`): 10 of 296 legal alternatives grade higher — Chet Holmgren +0.060 (drafted #17 by JCo); Jalen Williams +0.050 (drafted #24 by Oblena); Anthony Davis +0.045 (drafted #32 by JCo).
- **#130 Collin Gillespie** (card #1, availability 1.0, note ``): 2 of 191 legal alternatives grade higher — Saddiq Bey +0.045 (drafted #136 by Kevin); Jerami Grant +0.002 (drafted #131 by Cayas); Bilal Coulibaly -0.030 (drafted #None by None).
- **#39 Onyeka Okongwu** (card #1, availability 1.0, note ``): 1 of 274 legal alternatives grade higher — OG Anunoby +0.041 (drafted #48 by Oblena); Donovan Clingan -0.038 (drafted #49 by Oblena); Cameron Boozer -0.039 (drafted #53 by Kyle).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 2 (#58 Zach LaVine, #135 Reed Sheppard).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 PTS+REB; #63 REB+PTS (advise); #82 REB+PTS (advise); #87 PTS (advise); #106 PTS (advise); #111 PTS (advise); #130 PTS (advise); #135 PTS (advise); #154 PTS (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 63 (out of sample) | 48 | 0.608 | 0.521 | **0.213** | 0.250 |
| pooled with every earlier scored room | 650 | 0.456 | 0.635 | 0.260 | 0.232 |

- this room: BUY NOW 3 rows, 3 gone; TOSS-UP 9 rows, 5 gone; quiet 36 rows, 21 survived.
- pooled: BUY NOW 164 rows, 79 gone; TOSS-UP 126 rows, 70 gone; quiet 359 rows, 271 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| swap#15:Chet Holmgren | 25.74 | 99.16 | 1 | #15 Chet Holmgren |
| swap#39:OG Anunoby | 25.46 | 98.70 | 1 | #39 OG Anunoby |
| swap#130:Saddiq Bey | 24.39 | 98.71 | 1 | #130 Saddiq Bey |
| swap#111:Saddiq Bey | 24.23 | 98.49 | 2 | #111 Saddiq Bey |
| swap#87:PJ Washington | 23.91 | 98.39 | 1 | #87 PJ Washington |
| swap#154:Santi Aldama | 23.87 | 98.66 | 2 | #154 Santi Aldama |
| swap#58:Tyler Herro | 23.71 | 98.29 | 2 | #58 Tyler Herro |
| as_drafted | 23.33 | 98.37 | 2 | — |
| follow_card_selfconsistent | 23.33 | 98.37 | 2 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v44`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
