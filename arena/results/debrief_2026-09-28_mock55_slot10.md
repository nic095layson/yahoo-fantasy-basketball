# Mock 55 debrief — slot 10, deck MOCK mode vs the league cast, deck v30 (rev 28266d8, the deck drafted against; Porziņģis veto live)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_55.json` (md5 `c5fefb7e916ccc99a93fed44f54c8702`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v28`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **16.09%** (rank 3 of 12) |
| Playoff rate | 86.36% |
| ECW | **4.931** cats/week (rank 3; next 5.345, Oblena) — favored in 9/11 head-to-heads |
| Season-shape H2H | wins 9/11 |
| Board rank (kept-total z-sum) | **1** (+8.36; next +8.21) |
| Category rank, weekly model | FG% 7 · FT% 4 · 3PTM 4 · PTS 4 · REB 8 · AST 6 · ST 2 · BLK 8 · TO 7 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Jayson Tatum | 15 | Karl-Anthony Towns (+0.194) | 8/298 | +0.194 |
| 15 | Evan Mobley | Scottie Barnes | 15 | Evan Mobley (+0.137) | 4/294 | +0.137 |
| 34 | OG Anunoby | Kyrie Irving | 5 | Franz Wagner (+0.143) | 18/276 | +0.079 |
| 39 | Desmond Bane | Desmond Bane | 1 | Franz Wagner (+0.051) | 2/272 | owner's own later pick |
| 58 | Payton Pritchard | Donovan Clingan | 17 | Myles Turner (+0.054) | 3/254 | -0.069 |
| 63 | Cameron Johnson | De'Aaron Fox | 2 | Myles Turner (+0.076) | 9/250 | owner's own later pick |
| 82 | Cameron Johnson | Jakob Poeltl | 2 | none | 0/233 | owner's own later pick |
| 87 | Cameron Johnson | Cameron Johnson | 1 | none | 0/229 | owner's own later pick |
| 106 | Tari Eason | Tari Eason | 1 | none | 0/211 | owner's own later pick |
| 111 | Christian Braun | Christian Braun | 1 | PJ Washington (+0.042) | 2/207 | owner's own later pick |
| 130 | Jordan Poole | Jordan Poole | 1 | Saddiq Bey (+0.017) | 3/189 | owner's own later pick |
| 135 | Collin Gillespie | Collin Gillespie | 1 | Saddiq Bey (+0.039) | 4/185 | owner's own later pick |
| 154 | Malik Monk | Malik Monk | 1 | none | 0/167 | owner's own later pick |

Hindsight found **no better legal pick** at 4 turns (#82, #87, #106, #154) and exactly one at 0 (—). The owner took the card's #1 at 7 turns (#39, #87, #106, #111, #130, #135, #154) and a Top-5 row at 10 of 13.

### The turns that cost the most (by hindsight gain)

- **#10 Jayson Tatum** (card #15, availability 0.78, note `inj-achilles-risk`): 8 of 298 legal alternatives grade higher — Karl-Anthony Towns +0.194 (drafted #11 by Noah); Evan Mobley +0.124 (drafted #20 by John); Chet Holmgren +0.118 (drafted #13 by JCo).
- **#34 Kyrie Irving** (card #5, availability 0.78, note `inj-acl-risk (first season back)`): 18 of 276 legal alternatives grade higher — Franz Wagner +0.143 (drafted #43 by Kyle); Onyeka Okongwu +0.101 (drafted #44 by John); Brandon Miller +0.096 (drafted #45 by Will).
- **#15 Scottie Barnes** (card #15, availability 1.0, note ``): 4 of 294 legal alternatives grade higher — Evan Mobley +0.137 (drafted #20 by John); Anthony Davis +0.105 (drafted #22 by Cayas); Domantas Sabonis +0.066 (drafted #23 by Oblena).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 7 of 11 owner turns: #58 BLK+PTS+REB; #63 PTS (advise); #82 PTS (advise); #87 3PTM+PTS (advise); #106 3PTM+PTS (advise); #111 3PTM (advise); #130 3PTM (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 55 (out of sample) | 51 | 0.647 | 0.627 | **0.186** | 0.234 |
| pooled with every earlier scored room | 253 | 0.543 | 0.711 | 0.189 | 0.205 |

- this room: BUY NOW 4 rows, 4 gone; TOSS-UP 6 rows, 3 gone; quiet 41 rows, 29 survived.
- pooled: BUY NOW 36 rows, 24 gone; TOSS-UP 48 rows, 23 gone; quiet 169 rows, 143 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 37.29 | 98.86 | 1 | #10 Karl-Anthony Towns, #15 Jamal Murray, #34 OG Anunoby, #58 Payton Pritchard, #63 Myles Turner, #135 Herbert Jones, #154 Collin Gillespie |
| swap#10:Karl-Anthony Towns | 23.06 | 93.93 | 2 | #10 Karl-Anthony Towns |
| swap#15:Evan Mobley | 21.48 | 92.76 | 3 | #15 Evan Mobley |
| swap#34:Franz Wagner | 21.30 | 92.43 | 3 | #34 Franz Wagner |
| swap#63:Myles Turner | 20.41 | 91.22 | 3 | #63 Myles Turner |
| swap#58:Myles Turner | 19.66 | 89.66 | 3 | #58 Myles Turner |
| swap#39:Franz Wagner | 17.97 | 88.55 | 3 | #39 Franz Wagner |
| swap#135:Saddiq Bey | 17.73 | 88.28 | 3 | #135 Saddiq Bey |
| swap#111:PJ Washington | 17.43 | 87.86 | 3 | #111 PJ Washington |
| swap#130:Saddiq Bey | 16.58 | 87.17 | 3 | #130 Saddiq Bey |
| as_drafted | 16.09 | 86.36 | 3 | — |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v28`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
