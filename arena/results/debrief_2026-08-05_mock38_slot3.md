# Mock 38 debrief — slot 3, declared punt FT%/3PTM/PTS (2026-08-05)

State: `arena/data/states/draft_state_mock38.json` (upload md5 cae147e2).
Regenerate: `python3 arena/mocks/season_sim_mock38.py` →
`arena/results/season_sim_mock38_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Per-turn replay: `arena/results/m38_replay.json`. Same
instrument caveats as mocks 31–37.

## Headline — first punted build to WIN its room

| Metric | Value | Rank |
|---|---|---|
| Champ% | **16.46** (16.02/16.93/16.42 per-seed) | **1 of 12** |
| Playoff% | 75.2 | 1 |
| ECW/week | 4.73 | 2 (T1: 4.74) |
| Kept-total, 9 cats | +3.54 | 3 |
| Kept-z under declared punt | +18.23 | 1 — next best in room: +8.81 |

The room is flat: a four-team cluster at the top (owner 16.46, T1 15.88,
T2 15.46, T9 15.28). The lead is narrow but held across all three seeds.
Absolute champ% is room-dependent — 16.46 in this flat room is a
first-place finish, not a weak build (compare m37: 19.04 was 3rd).
ECW 4.73 sits below the 4.90 winners' bar, but so does the entire room
(max 4.74) — a low-scoring room, not a low-quality build.

Roster: Luka, Jamal Murray, Chet Holmgren, Josh Hart, Sheppard, Poeltl,
Braun, Sarr, Wallace, Gafford, Boozer, Ausar, Queen.

## The synthesis draft: m36's method + m37's frame

The ledger's two proven styles fuse here for the first time:

**m36's card spine.** Exact card #1 followed **8/13** (R3 Chet, R6
Poeltl, R7 Braun, R9 Wallace, R10 Gafford, R11 Boozer, R12 Ausar — six
of the seven picks R6–R12), in Top-5 11/13. R1 Luka was the card's #2
behind SGA.

**m37's hard punt, played for real.** Declared FT%/3PTM/PTS is the
**#1 punt of all 84** for this roster (kept-z +18.23; #2 was
FT%/3PTM/AST at +16.41) — the owner's THIRD optimal declaration
(m35, m37, m38). And all three declared cats are genuinely sunk:
FT% rank 12 (−4.45), 3PTM rank 12 (−5.87), PTS rank 11 (−4.37).

**The only two off-card picks are punt-frame corrections.** R4 Josh Hart
(card: Okongwu) and R8 Alex Sarr (card: Vucevic) — both times the owner
swapped the punt-blind card's balanced big for a punt-fit body. Under
E20 this is exactly the intended division of labor: the ordering supplies
the value spine, the owner's declared frame supplies the two corrections
it is measured not to make.

## Category shape

| Kept | FG% | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|
| rank / z | **1** / +5.78 | 2 / +2.82 | 9 / −2.56 | 2 / +3.39 | 2 / +3.98 | 2 / +4.81 |

| Punted | FT% | 3PTM | PTS |
|---|---|---|---|
| rank / z | 12 / −4.45 | 12 / −5.87 | 11 / −4.37 |

Five kept cats at rank 1–2 — the most top-heavy kept frame in the
ledger. Dead-kept-cat check (m34/m35 pattern): AST is the soft spot at
rank 9 (−2.56), but it sits clearly above the punted cluster
(−4.4 … −5.9) — soft, not dead, same verdict as m36's PTS. Effectively
a 5-strong + 1-soft kept frame, and the sim prices it first.

No yardstick split this time: champ 1 / ECW 2 / kept-total 3 roughly
agree (contrast m37's 3-vs-7 split).

## Read for October

Three punted drafts, three declarations, ascending results: m35 optimal
punt + dead kept cat → 6th; m37 optimal punt + all-live frame,
owner-driven → 3rd; m38 optimal punt + card spine + punt-fit-only
deviations → **1st**. The doctrine writes itself: declare the punt the
roster wants, follow the card's spine, and spend deviations ONLY where
the punt-blind card offers a balanced piece your frame can't use. Joins
the punted screening set (E21, now eight: 22, 31, 32, 34, 35, 36, 37, 38).

## LEDGER row

`| 38 | 3 | 16.46 | 75.2 | 1 | 12 | ECW 4.73 (room max 4.74 — flat room);
FIRST PUNTED BUILD TO RANK 1. Declared punt FT%/3PTM/PTS is the #1 punt
of 84 (third straight optimal declaration: m35/m37/m38) and genuinely
played (FT% −4.5, 3PTM −5.9, PTS −4.4 all sunk). Card exact-#1 followed
8/13; the ONLY two off-card picks (R4 Hart over Okongwu, R8 Sarr over
Vucevic) were punt-fit corrections — the m36-spine + m37-frame synthesis.
Five kept cats at rank 1–2; AST soft (9, −2.56) but not dead
(`season_sim_mock38.py`, `m38_replay.json`) |`
