# Mock 52 debrief — Seat 12, NO declared punt (2026-08-10)

Standard room, v2 instrument, cast recorded, 245-row pool epoch. State:
`arena/data/states/draft_state_mock52.json`. Regenerate:
`python3 arena/mocks/season_sim_mock52.py`. Replay:
`arena/results/m52_replay.json`.

## Headline — the first frameless draft that did NOT collapse

| Metric | Value | Rank |
|---|---|---|
| Champ% | **15.66** (16.12/15.10/15.77 per-seed) | **2 of 12** |
| Playoff% | 73.29 | 3 |
| ECW/week | 4.73 | 2 |
| Kept-total, 9 cats | −1.17 | 9 |

Room: Cayas (Seat 2) 21.25 wins, owner 15.66 second, Kyle 14.84, Robby
12.40. From **Seat 12 — the wheel** (baseline 3.36, worst block):
seat-edge **+12.30pp**, 19th positive in 20 rooms (246-pool caveat).

Roster: Jalen Johnson, Donovan Mitchell, Scottie Barnes, Brandon
Miller, Markkanen, Myles Turner, Jarrett Allen, Malik Monk, Cason
Wallace, CJ McCollum, Gafford, Keyonte George, Caruso.

## This result REVISES the frameless finding — record it honestly

The prior claim (m46 debrief): declared (m40/43/44/45) vs frameless
(m42/46) separated **with no overlap**. Mock 52 breaks the no-overlap
half of that claim: 15.66 beats two declared results (m45 12.05, m47
12.49). Updated table, all v2 standard rooms:

| Declaration | Mocks | Mean champ% | Mean finish |
|---|---|---|---|
| Declared frame | 40,43,44,45,47,48,49,50,51 | 22.24 | 1.8 |
| No frame | 42, 46, **52** | 8.23 | 5.7 |

Frameless is still clearly worse on average — but the mechanism now
resolves finer than "declare or die." The flat signature is identical
across all three frameless drafts (m52: no cat above rank 3, best
implied frame only **+5.30**, weaker even than m46's +6.43, kept-total
rank 9). What differs is **who was steering**:

- m42/m46: judgment built a scoring core early, the card built a
  defensive shell late, **1/8 Top-5 through R8 (m46)** — two halves
  pulling apart, finishes 6th and 9th.
- m52: **exact-#1 9/13, Top-5 10/13, including R1/R2** (Jalen Johnson,
  Mitchell on the wheel). No dueling halves — the card ran the draft,
  and blend50's ECW half quietly optimized weekly matchup cells the
  z-ledger can't see (ECW rank 2 vs kept-z rank 9, the yardstick split
  at its widest).

**Refined reading (n=3 frameless, offered as hypothesis, not law):
coherence is the load-bearing variable, and there are two ways to get
it — declare a frame and spend judgment inside it (m48/m49/m51), or
hand the card the whole draft (m50 descriptive-declared, m52
frameless). The failure mode is the middle: heavy early judgment with
no frame to reconcile it against the card's late spine (m42/m46).**
A declared frame remains the higher-ceiling path: every result above
20% is a declared build; m52's 15.66 looks like the card-autopilot
ceiling from a weak seat.

## Card agreement detail

Deviations were few and mild: Barnes over OG (R3, Top-5), Miller over
OG (R4), Monk over Wallace (R8 — Wallace taken next turn anyway),
Keyonte George over Jrue (R12). Everything else exact, including the
entire R5–R7 middle and both wheel pairs.

## Roster shape

Census G6/F4/C4; daily-fill never binds (lowest w Keyonte George
0.964). 3PTM rank 3 (+1.93) is the closest thing to a strength; FG%
−1.97 and REB −2.45 rank 8 are the quiet leaks that kept the ceiling
at 15 instead of 20+.

## LEDGER row

Appended to `arena/results/LEDGER.md` §1 (row 52), quoting
`season_sim_mock52.py` and `m52_replay.json`. The row supersedes the
m46 row's "no overlap" phrasing per the append-only registry rule —
the m46 row stands as written; this row records the revision.
