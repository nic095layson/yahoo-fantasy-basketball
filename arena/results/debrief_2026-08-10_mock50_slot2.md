# Mock 50 debrief — Seat 2, declared punt AST/3PTM/PTS (2026-08-10)

Standard room, v2 instrument, cast recorded, 245-row pool epoch. State:
`arena/data/states/draft_state_mock50.json`. Regenerate:
`python3 arena/mocks/season_sim_mock50.py`. Replay:
`arena/results/m50_replay.json`.

## Headline — a clean-sweep room win, on card autopilot

| Metric | Value | Rank |
|---|---|---|
| Champ% | **26.64** (26.52/26.42/27.00 per-seed) | **1 of 12** |
| Playoff% | 93.95 | 1 |
| ECW/week | 5.01 | 1 |
| Kept-z under declared punt | +20.96 | 1 |
| Kept-total, 9 cats | +8.43 | 1 |

**Every yardstick rank 1** — the first sweep in the ledger. But the room
was a photo finish at the top: Kyle (Seat 1) 25.86, a **+0.78pp margin**,
then Oblena 19.72 and a cliff to 7.22. Second consecutive room win.
Seat-edge +12.56pp over Seat 2's baseline 14.08 (246-pool-epoch caveat) —
17th positive in 18 rooms.

Roster: SGA, Mobley, Derrick White, Bam, Cameron Johnson, Eason, Mikal
Bridges, Hartenstein, Cason Wallace, John Collins, Nesmith, Claxton,
Keon Ellis.

## Two firsts

**1. First AST-punt, and a brand-new frame family.** Every prior punted
draft was FT%-anchored. AST/3PTM/PTS is a defense/efficiency frame that
keeps FT%, and it is the **#1 frame of 84** (+20.96 vs +17.57 runner-up)
— eleventh optimal declaration in thirteen punted drafts. Genuinely
played: AST −5.09 and PTS −4.14 both rank 12, 3PTM −3.30 rank 10. All
six kept cats positive — **TO +9.41 is rank 1 and the largest single-cat
edge in any graded mock** (White/Mikal/Wallace/Nesmith/Ellis are all
low-turnover), with FG% +4.74 and BLK +3.02 at rank 2.

**2. Highest card agreement ever recorded: exact-#1 12/13, Top-5 13/13.**
The only deviation was Claxton over Tobias Harris at R12 — still Top-5.
This was card autopilot from a live seat, and it makes the mock a natural
replication of the integrity audit's synthetic card-following control
(23.76% from the owner seat, `mkt_control_out.json`): the live version
scored 26.64 from Seat 2. The card, punt-blind by design, produced a
coherent #1-of-84 frame organically.

## Doctrine note — the AST step, inverted (observation, n=1)

The written doctrine says *protect the threatened category (usually AST)
with an early star playmaker*. This build did the opposite: it conceded
AST completely — and won. The reconciliation is that the doctrine's
step 1 comes first: **declare the frame the roster wants.** Here the
card's Seat-2 value flow never wanted AST (SGA's assists ride along, but
White/Mikal/Wallace want steals and clean hands), and the owner's
declaration was *descriptive* — he named the frame the card was already
building instead of fighting for a category it had conceded. Protecting
AST is what you do when you intend to KEEP it; m44 died keeping it
half-heartedly. One room — recorded as an observation, not a doctrine
edit.

## Roster shape

Census G4/F6/C5 — balanced; five C-eligibles (Mobley, Bam, Hartenstein,
Collins, Claxton) against the 4-C ceiling, and daily-fill start rates
never bind (lowest w: Claxton 0.979, everyone else ≥1.00 effective).

## LEDGER row

Appended to `arena/results/LEDGER.md` §1 (row 50), quoting
`season_sim_mock50.py` and `m50_replay.json`.
