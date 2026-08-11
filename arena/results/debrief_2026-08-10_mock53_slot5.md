# Mock 53 debrief — Seat 5, NO declared punt, card autopilot (2026-08-10)

Standard room, v2 instrument, cast recorded, 245-row pool epoch. State:
`arena/data/states/draft_state_mock53.json`. Regenerate:
`python3 arena/mocks/season_sim_mock53.py`. Replay:
`arena/results/m53_replay.json`.

## Headline — second-best standard-room result in the ledger, frameless

| Metric | Value | Rank |
|---|---|---|
| Champ% | **28.71** (28.53/28.75/28.85 per-seed) | **1 of 12** |
| Playoff% | 90.69 | 1 |
| ECW/week | 4.96 | 1 |
| Kept-total, 9 cats | +7.65 | 2 |

Only m48 (46.03) is higher among standard rooms. And unlike m51's
photo finish, this is a blowout: Martin (Seat 8) second at 11.63 —
**2.5× the field's best**. Seat-edge **+24.38pp** over Seat 5's 4.33
baseline — the second-largest measured (m48's +32.09 leads); 20th
positive in 21 rooms (246-pool baseline caveat).

Roster: SGA, Giannis, Derrick White, Okongwu, Reed Sheppard, Tari
Eason, Christian Braun, Vucevic, Jaden McDaniels, Ryan Rollins, Aaron
Nesmith, Gafford, Keon Ellis.

## What this was: autopilot plus ONE star deviation

Exact-#1 **12/13** (ties m50's record), and the single deviation was
**Giannis over Mobley at R2 — fully off-card**. Every other pick,
R1 and R3–R13, was the card's #1. No declared punt.

The card organically built the m50 shape again: **FG% +7.71 rank 1,
TO +8.02 rank 1**, ST/BLK rank 3 — a defense/efficiency core — while
conceding the counting glamour cats (PTS −2.96, AST −3.75, 3PTM −2.28,
FT% −2.00, all rank 10–11). Best implied frame: 3PTM/PTS/AST **+16.63**
— a real concession, unlike m52's flat +5.30. The Giannis deviation is
exactly the punt-fit-star move for that implied frame: elite FG%
volume, and his FT% damage lands in a category the flow had already
conceded.

## The coherence hypothesis strengthens (now registered as E26)

Frameless results now split perfectly by WHO steered:

| Frameless mode | Mocks | Champ% | Finish |
|---|---|---|---|
| Judgment-heavy, no frame | m42, m46 | 6.43, 2.59 | 6th, 9th |
| Card autopilot | m52, **m53** | 15.66, **28.71** | 2nd, **1st** |

Same declaration status, opposite outcomes, and the discriminating
variable is early-round card agreement (m46: 1/8 Top-5 through R8;
m53: 12/13 exact). The punt-blind blend50, left alone, builds its own
coherent concession — declaring is how a HUMAN-steered build stays
coherent, not a magic ritual. Registered as **E26** in
SEPTEMBER-PLAN §9 with a pre-registered counterfactual design and bar
— five same-day rooms is suggestive, not controlled, and the m42/m46
comparison spans a pool epoch.

Day quintet (all 2026-08-10): m49 24.94 (1st), m50 26.64 (1st), m51
21.45 (1st-tie), m52 15.66 (2nd), m53 28.71 (1st) — five rooms, five
top-2s, three different modes of coherence.

## Roster shape

Census G6/F4/C4; daily-fill never binds (lowest w Keon Ellis 0.978).
The one visible leak: REB −1.42 rank 7 — Okongwu/Vucevic/Gafford are
the board's value centers, not glass monsters.

## LEDGER row

Appended to `arena/results/LEDGER.md` §1 (row 53), quoting
`season_sim_mock53.py` and `m53_replay.json`.
