# Mock 68 debrief — slot 10, live public room, deck v50 (rev 9f54e99, the 10/08 pull build — notes and Hawkins's team, no line, tag or card change)

**Fingerprint.** owner slot 10, 156 picks, Yahoo public mock; state `arena/data/states/draft_state_68.json` (md5 `cd08323137a56fa7a31609d1c28f6447`), reconciled pick-by-pick against Yahoo's recap (156/156). Pool tag `v50`; poolless names in this room: none. Punt box: none declared.

**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, `live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **28.36%** (rank 1 of 12) |
| Playoff rate | 99.73% |
| ECW | **5.371** cats/week (rank 1; next 5.096, T1) — favored in 11/11 head-to-heads |
| Season-shape H2H | wins 11/11 |
| Board rank (kept-total z-sum) | **1** (+8.12; next +5.24) |
| Category rank, weekly model | FG% 3 · FT% 3 · 3PTM 5 · PTS 4 · REB 3 · AST **10** · ST **1** · BLK 3 · TO **1** |

Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25).

## Decision ledger — card vs owner vs hindsight

Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "owner's own later pick" = the card's #1 was a player the owner took later (screened).

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |
|---|---|---|---|---|---|---|
| 10 | Karl-Anthony Towns | Karl-Anthony Towns | 1 | none | 0/296 | owner's own later pick |
| 15 | Tyrese Maxey | Tyrese Maxey | 1 | none | 0/292 | owner's own later pick |
| 34 | Anthony Davis | Derrick White | 3 | none | 0/274 | -0.010 |
| 39 | Jalen Williams | Jalen Williams | 1 | none | 0/270 | owner's own later pick |
| 58 | OG Anunoby | OG Anunoby | 1 | Payton Pritchard (+0.016) | 1/252 | owner's own later pick |
| 63 | Ivica Zubac | Ivica Zubac | 1 | none | 0/248 | -0.085 |
| 82 | Coby White | Ty Jerome | 28 | Coby White (+0.109) | 19/230 | +0.088 |
| 87 | Mikal Bridges | Jaden McDaniels | 12 | Coby White (+0.078) | 16/226 | +0.066 |
| 106 | Isaiah Hartenstein | Isaiah Hartenstein | 1 | none | 0/208 | owner's own later pick |
| 111 | Sandro Mamukelashvili | Darryn Peterson | 33 | Sandro Mamukelashvili (+0.099) | 26/204 | +0.099 |
| 130 | PJ Washington | PJ Washington | 1 | none | 0/108 | -0.010 |
| 135 | Devin Vassell | Devin Vassell | 1 | Saddiq Bey (+0.009) | 1/104 | -0.044 |
| 154 | Herbert Jones | Herbert Jones | 1 | Draymond Green (+0.031) | 3/88 | owner's own later pick |

Hindsight found **no better legal pick** at 7 turns (#10, #15, #34, #39, #63, #106, #130) and exactly one at 2 (#58, #135). The owner took the card's #1 at 9 turns (#10, #15, #39, #58, #63, #106, #130, #135, #154) and a Top-5 row at 10 of 13.

### The turns that cost the most (by hindsight gain)

- **#82 Ty Jerome** (card #28, availability 1.0, note `10/6: started at PG in the 10/5 preseason opener, 15 min / 12 pts / 5 ast, Pippen Jr. 16 min off the bench (box score; SI Grizzlies); one game, WO-5 decides; 10/8: started at PG again in the 10/7 game vs Orlando, 19 min / 17 pts (team high) / 4 ast on 7-14; Pippen Jr. 14 min off the bench; two starts in two games, WO-5 decides (ESPN box score; Yahoo, SI Grizzlies)`): 19 of 230 legal alternatives grade higher — Coby White +0.109 (drafted #90 by T7); Zach LaVine +0.088 (drafted #105 by T9); Mikal Bridges +0.074 (drafted #88 by T9).
- **#111 Darryn Peterson** (card #33, availability 1.0, note `rookie-proj; role 9/30: camp day-one first unit in purple with George, Markkanen, Jackson Jr. and Nurkić (Yahoo rookie targets, Yahoo camp footage); the fifth spot is contested with Bailey, Sensabaugh and Mykhailiuk (Hoops Rumors Jazz Notes); repriced 2026-09-30 from 28 to 30 minutes on the same per-minute line, kit twin; 10/7: started the 10/6 game vs Denver, 30 min (team high), 23 pts on 10-18 / 1-6 from three with 3 reb / 3 ast, the game high (ESPN box score; NBA.com Starting 5; KSL, Deseret, Salt Lake Tribune 10/6)`): 26 of 204 legal alternatives grade higher — Sandro Mamukelashvili +0.099 (drafted #133 by T12); Aaron Gordon +0.086 (drafted #125 by T5); Saddiq Bey +0.081 (drafted #153 by T9).
- **#87 Jaden McDaniels** (card #12, availability 1.0, note `10/8: started the 10/7 game vs Indiana in Ames, 21 min / 16 pts, 4-6 from three [SINGLE-SOURCE: box score] (ESPN box score)`): 16 of 226 legal alternatives grade higher — Coby White +0.078 (drafted #90 by T7); Mikal Bridges +0.066 (drafted #88 by T9); Zach LaVine +0.065 (drafted #105 by T9).

Sixth-row pins: LAST CALL took the 🎯 at 0 turn(s) (—); urgent pin withheld by the D51R-4 gate at 0 (—); DEPTH WATCH (informational) at 0 (—).

## Punt advisor (room-relative read, D51R-3)

Box empty all draft. Room-relative lean at 9 of 11 owner turns: #58 AST+REB; #63 AST+REB (advise); #82 AST (advise); #87 AST (advise); #106 AST (advise); #111 AST (advise); #130 AST (advise); #135 AST (advise); #154 AST (advise).

## Survival chips — out-of-sample room for the price-only refit (D51R-1R)

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 68 (out of sample) | 51 | 0.463 | 0.588 | **0.181** | 0.242 |
| pooled with every earlier scored room | 909 | 0.476 | 0.622 | 0.243 | 0.235 |

- this room: BUY NOW 7 rows, 6 gone; TOSS-UP 17 rows, 11 gone; quiet 27 rows, 23 survived.
- pooled: BUY NOW 193 rows, 102 gone; TOSS-UP 193 rows, 107 gone; quiet 522 rows, 387 survived.

## Championship arms (18,000 CRN seasons each)

| arm | champ% | playoff% | rank | swaps |
|---|---|---|---|---|
| follow_card_selfconsistent | 35.00 | 99.96 | 1 | #34 Anthony Davis, #63 Payton Pritchard, #82 Mikal Bridges, #87 Josh Hart, #111 Sandro Mamukelashvili, #135 Fred VanVleet |
| swap#82:Coby White | 31.87 | 99.90 | 1 | #82 Coby White |
| swap#111:Sandro Mamukelashvili | 31.03 | 99.92 | 1 | #111 Sandro Mamukelashvili |
| swap#87:Coby White | 30.06 | 99.86 | 1 | #87 Coby White |
| swap#135:Saddiq Bey | 28.71 | 99.73 | 1 | #135 Saddiq Bey |
| as_drafted | 28.36 | 99.73 | 1 | — |
| swap#154:Draymond Green | 28.10 | 99.79 | 1 | #154 Draymond Green |
| swap#58:Payton Pritchard | 27.99 | 99.76 | 1 | #58 Payton Pritchard |

## Tool-state integrity — the deck's board vs Yahoo's recap

The owner's tool log replayed into its final board (156 picks) and diffed position by position against the recap: **0 position(s) differ**; the owner's own roster is identical. Recap names missing from the tool board: none; tool names not in the recap: none.

## Limits

- Random public room, not the league cast: the field's weakness is in every denominator above.
- Lines are the pool the room drafted against (tag `v50`); a later same-day build can differ in judgment or veto, never in lines.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.
