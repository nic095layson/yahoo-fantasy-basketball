# Mock 41 debrief — slot 4, declared punt FT%/3PTM/TO (2026-08-06)

State: `arena/data/states/draft_state_mock41.json`. Regenerate:
`python3 arena/mocks/season_sim_mock41.py` →
`arena/results/season_sim_mock41_out.json`, 18,000 seasons (6,000 × seeds
11/23/47), v2 instrument. Replay: `arena/results/m41_replay.json`.

## Two caveats that govern how this number may be quoted

1. **This was a SHARP ROOM draft** (`"sharp": true` in the state) — the
   E25 stress-test opponents, which **failed their bar** and have since
   been **discarded from the deck** at the owner's instruction. The room
   is therefore not the standard cast and not a draft-night forecast.
2. **v2 epoch.** Absolute champ% is not comparable to mocks 10–39.

Against mock 40 (v2, standard room, 26.29%) the comparison is also
imperfect: different room type, different seed. **Rank and margin within
this room are the safe readings; the headline champ% is not a ledger
record and is marked as such.**

## Headline (within its own room)

| Metric | Value | Rank |
|---|---|---|
| Champ% | **43.84** (44.62/43.33/43.58 per-seed) | **1 of 12** |
| Playoff% | **96.7** | 1 |
| ECW/week | **5.11** | 1 |
| Kept-z under declared punt | **+27.43** | 1 (next: +1.17) |
| Kept-total, 9 cats | +0.94 | 4 |

The most lopsided room in the ledger: **4.9× the next seat** (8.91) and
the first owner build to clear 96% playoff odds. ECW 5.11 is the highest
figure ever recorded on either instrument.

Roster: Jokic, Giannis, Mobley, Trae, Jaylen Brown, Zion, Coulibaly,
Gobert, Jaden McDaniels, Ausar Thompson, Dylan Harper, Gafford, Caruso.

## Category shape — four rank-1 categories

| Kept | FG% | REB | ST | BLK | AST | PTS |
|---|---|---|---|---|---|---|
| rank / z | **1** / +9.80 | **1** / +4.45 | **1** / +5.10 | **1** / +3.60 | 2 / +3.57 | 6 / +0.91 |

| Punted | FT% | 3PTM | TO |
|---|---|---|---|
| rank / z | 12 / −13.21 | 12 / −9.87 | 9 / −3.42 |

FG% at +9.80 is the single strongest category z in the ledger. Four
categories won outright, a fifth (AST) at rank 2 — that is 4.5 categories
banked before the week starts, in a 5-of-9 format.

**Sixth straight optimal declaration.** FT%/3PTM/TO is the **#1 punt of
all 84** for this roster (+27.43 vs +23.10 runner-up), continuing
m35→m37→m38→m39→m40→m41. All three declared cats genuinely sunk.

## Card agreement — the most owner-driven build yet

Exact #1 only **2/13** (R1 Jokic, R12 Gafford), Top-5 7/13. Six off-card
picks: Giannis (R2), Trae (R4), Jaylen Brown (R5), Zion (R6), Coulibaly
(R7), Dylan Harper (R11). The card kept offering balanced value (Mobley,
Derrick White, Amen Thompson, Tari Eason, Myles Turner ×2) while the
owner built a punt-coherent big/defense core. The punt-blind ordering and
a hard declared frame diverge by design (E20) — this is the m37 pattern
at its most extreme, and it produced the strongest category profile yet.

## First exact cast attribution (the export fix working)

Mock 41 is the **first state that records who sat where** — the
2026-08-06 export change. No fingerprinting needed:

| Seat | Manager | Champ% | ECW |
|---|---|---|---|
| 4 | **OWNER** | 43.84 | 5.11 |
| 6 | Oblena | 8.91 | 4.58 |
| 7 | Cayas | 8.59 | 4.58 |
| 1 | Kevin | 8.44 | 4.58 |
| 2 | Martin | 5.91 | 4.48 |
| 9 | JCo | 5.44 | 4.48 |
| 8 | Will | 4.23 | 4.45 |
| 11 | Noah | 3.83 | 4.44 |
| 12 | Hegi | 3.78 | 4.40 |
| 3 | John | 3.52 | 4.36 |
| 5 | Robby | 1.94 | 4.30 |
| 10 | Kyle | 1.57 | 4.23 |

Consistent with the E25 measurement: the stress-test bots cluster tightly
(4.23–4.58 ECW) and none builds a real category identity — which is
precisely why that experiment failed its bar and was discarded.

## LEDGER row

`| 41* | 4 | 43.84 | 96.7 | 1 | 12 | ***SHARP-ROOM draft** (E25 stress
test, since discarded) — NOT a standard-room result and not a ledger
record; v2 epoch.* ECW 5.11 (highest ever measured) and 4.9× the next
seat, the most lopsided room in the ledger. SIXTH straight optimal
declaration: FT%/3PTM/TO is #1 of 84 (+27.43) and sunk to the floor (FT%
−13.2, 3PTM −9.9). FOUR rank-1 categories (FG% +9.80 — strongest single
category z ever, REB, ST, BLK) plus AST rank 2. Most owner-driven build
yet: card exact-#1 only 2/13, six off-card punt-fit picks. First state
with an exact recorded cast (`season_sim_mock41.py`, `m41_replay.json`) |`
