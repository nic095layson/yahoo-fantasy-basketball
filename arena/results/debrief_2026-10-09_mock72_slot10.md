# Mock 72 debrief — slot 10, deck MOCK mode vs the league cast, deck v54 (rev 03cba0a, MOCK mode against the 11 league-mates on the real seating; engine, values, prices and pool identical to v53)

**Fingerprint.** owner slot 10, 156 picks, deck MOCK mode (11 modeled league-mates); state `arena/data/states/draft_state_72.json` (md5 `266420b4cc7e2c2cc3ce8b4bc97f211b`), reconciled pick-by-pick against the deck's own recap (156/156). Pool tag `v53`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **28.19%** (rank 1 of 12) |
| Playoff rate | 98.91% |
| ECW | **5.224** cats/week (rank 1; next 4.786, Oblena) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 10/11 |
| Board rank (kept-total z-sum) | **1** (+7.61; next +4.03) |
| Category rank, weekly model | FG% 4 · FT% 3 · 3PTM **1** · PTS 8 · REB 3 · AST 6 · ST 2 · BLK **9** · TO 5 |

League-cast mock: the opponents are the E18 behavioral models of the 11 league-mates, not the people — LEDGER-eligible.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | Chet Holmgren (+0.044) | 1/295 | owner's own later pick |
| 15 | Jamal Murray | James Harden | 6 | Chet Holmgren (+0.064) | 3/291 | -0.018 |
| 34 | OG Anunoby | Kyrie Irving | 5 | Franz Wagner (+0.076) | 8/273 | +0.030 |
| 39 | Desmond Bane | Desmond Bane | 1 | Franz Wagner (+0.014) | 1/269 | owner's own later pick |
| 58 | Payton Pritchard | Payton Pritchard | 1 | none | 0/251 | owner's own later pick |
| 63 | Jalen Suggs | Deni Avdija | 11 | Mikal Bridges (+0.030) | 8/247 | +0.010 |
| 82 | Josh Hart | Rudy Gobert | 3 | Isaiah Hartenstein (+0.008) | 2/229 | owner's own later pick |
| 87 | Zach LaVine | Josh Hart | 2 | Myles Turner (+0.030) | 3/225 | +0.028 |
| 106 | Herbert Jones | Yaxel Lendeborg | 4 | Daniel Gafford (+0.007) | 1/207 | -0.020 |
| 111 | Cason Wallace | Cason Wallace | 1 | Draymond Green (+0.007) | 1/203 | owner's own later pick |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/108 | owner's own later pick |
| 135 | Sandro Mamukelashvili | Devin Vassell | 2 | Collin Gillespie (+0.003) | 1/104 | owner's own later pick |
| 154 | Daniel Gafford | Sandro Mamukelashvili | 2 | none | 0/86 | owner's own later pick |

Hindsight found **no better legal pick** at 3 turns (#58, #130, #154) and exactly one at 5 (#10, #39, #106, #111, #135). The owner took the card's #1 at 5 turns (#10, #39, #58, #111, #130) and a Top-5 row at 11 of 13.

### The turns that cost the most (by hindsight gain)

- **#34 Kyrie Irving** (card #5, availability 0.78, note `inj-acl-risk (first season back); 10/9: out of the 10/9 Macao game vs Houston, left knee rest on ESPN's feed; May: he plays one of the two Macao games (ESPN injuries feed; Athlon, China Daily); 10/9 (research): plays Sunday 10/11 in Macao, his first game since the 3/3/2025 ACL tear and the first beside Flagg; May: Friday was left-knee rest, Sunday the unofficial comeback; ANTA to Dallas Sports Journal: cleared for Macao with no restrictions; the tag stays by the first-season-back convention (Dallas Sports Journal, SI Mavericks, Yahoo Sports, Yardbarker)`): 8 of 273 legal alternatives grade higher — Franz Wagner +0.076 (drafted #40 by Kevin); OG Anunoby +0.030 (drafted #48 by Oblena); Tyler Herro +0.023 (drafted #59 by Cayas).
- **#15 James Harden** (card #6, availability 1.0, note `10/9: did not play the 10/8 preseason opener vs Boston, right ankle soreness; Atkinson: 'just caution'; day-to-day on ESPN's feed with a 10/11 estimate, next chance Sunday vs Orlando (ESPN game feed; RotoWire, Fear The Sword/Yahoo, CelticsBlog)`): 3 of 291 legal alternatives grade higher — Chet Holmgren +0.064 (drafted #19 by Martin); Derrick White +0.026 (drafted #33 by Kevin); Kevin Durant +0.005 (drafted #16 by Kevin).
- **#10 Karl-Anthony Towns** (card #1, availability 1.0, note `10/9: started the 10/8 game vs Washington, 19 min / 8 pts / 7 reb / 3 ast on 2-7 [SINGLE-SOURCE: box score] (ESPN box score)`): 1 of 295 legal alternatives grade higher — Chet Holmgren +0.044 (drafted #19 by Martin); Jalen Johnson -0.000 (drafted #11 by Cayas); Anthony Davis -0.027 (drafted #25 by Oblena).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 BLK; #63 BLK (advise); #82 BLK (advise); #87 BLK (advise); #106 BLK (advise); #111 BLK (advise); #130 BLK (advise); #135 BLK (advise); #154 BLK (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 72 (out of sample) | 50 | 0.565 | 0.680 | **0.244** | 0.218 |
| pooled with every earlier scored room | 1118 | 0.491 | 0.621 | 0.239 | 0.235 |

- this room: BUY NOW 5 rows, 3 gone; TOSS-UP 11 rows, 3 gone; quiet 34 rows, 24 survived.
- pooled: BUY NOW 216 rows, 117 gone; TOSS-UP 236 rows, 125 gone; quiet 665 rows, 483 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| swap#15:Chet Holmgren | 31.30 | 99.60 | 1 | #15 Chet Holmgren |
| swap#34:Franz Wagner | 31.14 | 99.37 | 1 | #34 Franz Wagner |
| follow_card_selfconsistent | 30.36 | 99.42 | 1 | #15 Jamal Murray, #34 OG Anunoby, #63 Isaiah Hartenstein, #82 Zach LaVine |
| swap#87:Myles Turner | 28.72 | 99.25 | 1 | #87 Myles Turner |
| swap#135:Collin Gillespie | 28.63 | 99.09 | 1 | #135 Collin Gillespie |
| swap#39:Franz Wagner | 28.59 | 98.98 | 1 | #39 Franz Wagner |
| swap#63:Mikal Bridges | 28.49 | 99.13 | 1 | #63 Mikal Bridges |
| swap#10:Chet Holmgren | 28.48 | 99.29 | 1 | #10 Chet Holmgren |
| swap#111:Draymond Green | 28.46 | 99.07 | 1 | #111 Draymond Green |
| swap#82:Isaiah Hartenstein | 28.19 | 99.08 | 1 | #82 Isaiah Hartenstein |
| as_drafted | 28.19 | 98.91 | 1 | — |
| swap#106:Daniel Gafford | 28.12 | 98.99 | 1 | #106 Daniel Gafford |

## Limits

- The field is the model of the league (E18 personalities, the ~0.45x-divergence synthetic market), not the league: real rooms have produced deeper star falls than mocks.
- Lines are the pool the room drafted against (tag `v53`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
