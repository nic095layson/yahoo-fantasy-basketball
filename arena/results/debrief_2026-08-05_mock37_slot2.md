# Mock 37 debrief — slot 2, declared punt FT%/TO/3PTM (2026-08-05)

State: `arena/data/states/draft_state_mock37.json` (upload md5 f0c9c04d).
Regenerate: `python3 arena/mocks/season_sim_mock37.py` →
`arena/results/season_sim_mock37_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Per-turn replay: `arena/results/m37_replay.json`. Same
instrument caveats as mocks 31–36.

## Headline

| Metric | Value | Rank |
|---|---|---|
| Champ% | **19.04** (18.90/19.22/19.00 per-seed) | **3 of 12** |
| Playoff% | 82.2 | 3 |
| ECW/week | 4.83 | 3 |
| Kept-total, 9 cats | +0.94 | 7 |
| Kept-z under declared punt | **+26.65** | 1 — **highest punt-frame total in the ledger** (prior: m31 +23.50) |

Room: a three-team cluster at the top — T4 21.67 (ECW 4.87), T1 19.26,
owner 19.04. Fifth-best owner champ% ever (m36 31.18, m24 29.82, m25
29.19, m21 26.91); ECW 4.83 sits just under the 4.90 winners' bar.

Roster: Jokic, Harden, Giannis, Trae, Eason, Jarrett Allen, Zion, Sarr,
Ausar, Jalen Green, Coulibaly, Gafford, Queen.

## Two firsts

**1. The declaration is optimal AND the build actually plays it.**
FT%/TO/3PTM is the **#1 punt of all 84** for this roster (kept-z +26.65)
— the owner's second optimal declaration in three punted drafts (m35 was
#1, m36 was #12). And unlike every prior punted mock, this is a REAL
three-category concession: FT% −10.52, 3PTM −8.85, TO −6.34 all deeply
sunk, exactly as declared.

**2. No dead kept category — the m34/m35 pattern did NOT recur.** All six
kept cats are POSITIVE: FG% +7.39, REB +5.64, AST +4.19, ST +3.96, BLK
+3.21, PTS +2.25. First punted build in the ledger with a fully live kept
frame. That is why a hard 3-cat punt still clears ECW 4.83 — six live
categories in a 5-of-9 game is exactly one cat of margin, and the sim
prices it at a top-3 finish.

Note the yardstick split again: kept-total (9-cat) ranks this roster
**7th** while ECW ranks it 3rd and the sim agrees — the punt sinks the
9-cat sum, ECW sees the shape.

## Card grading

The inverse of mock 36: actual pick in shipped Top-5 at **7/13**, exact
#1 only **3/13** (R10 Green, R12 Gafford, R13 Queen). This build is
owner-driven: Jokic over SGA at 1.2, Giannis over White (R3), Trae (R4),
Eason (R5), Allen (R6), Zion (R7), Sarr (R8), Ausar (R9), Coulibaly
(R11) — while the punt-blind card called Turner, Lopez, Clingan, Herb
Jones through the middle rounds. The card's balanced spine and the
owner's hard-punt spine diverge by design here (E20: the ordering is
punt-blind and validated as such); the owner's frame delivered the
ledger's best-ever punt coherence.

**Blend50 out-of-sample note:** no arm simulation run; follow-counts are
descriptive. m36 (10/13 follow → 31.2%) vs m37 (3/13 follow → 19.0%)
CANNOT be read causally — different rooms, anchors, and seats. Both are
top-3 builds; the pair now brackets the two working styles (card-spine +
star deviations vs owner-driven hard punt).

## Read for October

Same punt family as mock 36, one seat over, opposite method, both land
top-3. The mock-36 collaboration remains the measured record holder, but
this draft proves the hard-punt lane is real when (a) the declaration
matches the roster (#1 of 84, twice now) and (b) every kept cat stays
positive — the two conditions m32/m34/m35 each violated one of. Joins the
punted screening set (E21, now seven: 22, 31, 32, 34, 35, 36, 37).

## LEDGER row

`| 37 | 2 | 19.04 | 82.2 | 3 | 12 | ECW 4.83; declared punt FT%/TO/3PTM
is the #1 punt of 84 AND genuinely played (FT% −10.5, 3PTM −8.9, TO −6.3
sunk) — highest punt-frame kept-z ever (+26.65, prior m31 +23.50); FIRST
punted build with all six kept cats positive (no m34/m35 dead-cat).
Owner-driven: card exact-#1 followed only 3/13. Kept-total ranks 7th vs
ECW/champ rank 3 — the yardstick split again
(`season_sim_mock37.py`, `m37_replay.json`) |`
