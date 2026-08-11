# Mock 51 debrief — Seat 5, declared punt FT%/3PTM/AST (2026-08-10)

Standard room, v2 instrument, cast recorded, 245-row pool epoch. State:
`arena/data/states/draft_state_mock51.json`. Regenerate:
`python3 arena/mocks/season_sim_mock51.py`. Replay:
`arena/results/m51_replay.json`.

## Headline — third consecutive room win, by a coin-flip margin

| Metric | Value | Rank |
|---|---|---|
| Champ% | **21.45** (21.32/21.57/21.47 per-seed) | **1 of 12** |
| Playoff% | 83.76 | 2 |
| ECW/week | 4.87 | 2 |
| Kept-z under declared punt | +12.17 | — |
| Kept-total, 9 cats | −1.44 | 7 |

**Honesty first: this is a statistical tie.** John (Seat 4) finished
21.21 — a +0.24pp gap on 18,000 seasons, inside noise. Cayas (Seat 1)
18.45 close behind, then a cliff to Kyle 10.03. Read it as "co-favorite
in a three-team room," not a clear win. Seat-edge +17.12pp over Seat 5's
baseline 4.33 (246-pool caveat) — 18th positive in 19 rooms.

Roster: Ant Edwards, Mobley, Giannis, Amen Thompson, Reed Sheppard,
Myles Turner, Kel'el Ware, Cason Wallace, Herb Jones, Filipowski,
D'Angelo Russell, RJ Barrett, Keon Ellis.

## Declaration — optimal again, but the softest winning frame yet

FT%/3PTM/AST is the **#1 frame of 84** (+12.17) — twelfth optimal
declaration in fourteen punted drafts. But +12.17 is the weakest
declared-frame value of any v2 room win (m49 +21.42, m50 +20.96), and
the punts were only half-played: FT% −10.73 rank 12 is hard, but
**3PTM −1.45 is rank 8 and AST −1.43 rank 10** — semi-live, not
conceded. Ant Edwards (good FT%, heavy 3PTM) headlining an FT%/3PTM punt
is the shape mismatch behind it. Kept cats: FG% +3.91 and ST +2.54 rank
2, BLK +3.60 and REB +1.12 rank 3, TO +2.30 rank 5 — and **PTS −1.30
(rank 9), the second straight draft where kept-PTS drifted negative.**

The frame held anyway because the room's other declared builds
imploded (Noah's Seat 3 kept −24.90) — but a 46%-class result needs
either harder punts or a top pick that matches the frame. m48 and m50
both had that; this build's ceiling was capped by carrying two
half-punted categories.

## Card agreement

Exact-#1 **6/13**, Top-5 9/13. The deviations tell the familiar story:
Giannis over Derrick White at R3 is the doctrine's punt-fit-star move
(the FT%-punt centerpiece), Turner over Eason and Ware over Hart bought
BLK depth, and the R12/R13 pair (RJ over Ellis, then Ellis anyway) cost
nothing. The card supplied the guard spine (Amen, Sheppard, Wallace,
Herb Jones, Ellis all exact-#1).

## Roster shape

Census G6/F6/C5; five C-eligibles, ceiling never binds (lowest
daily-fill start rate: D'Angelo Russell 0.968).

## Day summary — three rooms, three frames, three wins

Mocks 49–51, all drafted 2026-08-10, all rank 1: FT%/3PTM (2-cat, Seat
8, 24.94), AST/3PTM/PTS (card autopilot, Seat 2, 26.64), FT%/3PTM/AST
(Seat 5, 21.45 co-favorite). Three different seats, three different
frame families, all declared #1-of-N and all winners — the declaration
discipline, not any single frame, is the common factor.

## LEDGER row

Appended to `arena/results/LEDGER.md` §1 (row 51), quoting
`season_sim_mock51.py` and `m51_replay.json`.
