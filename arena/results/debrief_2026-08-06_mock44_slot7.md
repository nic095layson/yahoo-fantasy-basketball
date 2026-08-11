# Mock 44 debrief — slot 7, declared punt FT%/3PTM/PTS (2026-08-06)

Standard room, v2 instrument, cast recorded. State:
`arena/data/states/draft_state_mock44.json` (md5 c208cba7). Regenerate:
`python3 arena/mocks/season_sim_mock44.py`. Replay:
`arena/results/m44_replay.json`.

## Headline

| Metric | Value | Rank |
|---|---|---|
| Champ% | 23.64 (23.45/23.28/24.20 per-seed) | **2 of 12** |
| Playoff% | 88.7 | 2 |
| ECW/week | 4.76 | 3 |
| Kept-z under declared punt | **+32.97 — NEW RECORD** (prior standard-room best m39 +26.84) | 1 |
| Kept-total, 9 cats | +0.72 | 5 |

A three-team race: **Cayas 25.08 (ECW 5.02)**, owner 23.64, **Noah 21.66
(ECW 5.00)**, then a cliff to Will at 7.77. Kyle — winner of the last two
rooms — finishes DEAD LAST from slot 12 (1.31%): seat texture, not a
super-bot. Roster: KAT, Giannis, Dyson Daniels, Amen Thompson, Sheppard,
Turner, Hart, Duren, Hartenstein, Ausar, Gafford, Caruso, TJD.

## The frame — deepest concession ever, and the old ghost returns

**Eighth optimal declaration in nine punted drafts**: FT%/3PTM/PTS is #1
of 84 at +32.97 (endogeneity caveat standing). All three declared cats
sunk to the floor (FT% −12.83, 3PTM −12.13, PTS −7.27 — all rank 12).

The kept frame is the most top-heavy ever: **FG% +13.02 (rank 1 — the
strongest single category z in the ledger, prior m41 +9.80), REB +7.74
(1), BLK +6.08 (1), TO +5.37 (2), ST +4.82 (2).**

**But AST died undeclared: rank 11, −4.06 — the m34/m35 dead-kept-cat
pattern returns.** This is effectively a FOUR-cat concession played as
three: the build wins its five live cats with overwhelming margin and
must never lose one — a 5-of-9 build with zero slack. The sim still
prices it 2nd because five rank-1/-2 cats rarely slip, but the shape is
the doctrine's known failure mode, softened only by the extremity of the
five strengths. The #2 frame (FT%/3PTM/AST, +29.76) was the honest
declaration for this roster once AST was conceded in practice.

Contrast m43 (yesterday's build): same punt family, AST kept ALIVE at
rank 1 via Cade/Harden/Trae. Here the guard corps (Daniels, Amen,
Sheppard, Caruso) is all defense, no playmaking volume — great for
ST/TO, fatal for AST. The lesson refines the doctrine: **a punt frame
needs one genuine playmaker or AST must be declared, not drifted.**

## Card agreement

Exact #1 6/13, **Top-5 11/13** — the highest top-5 agreement since m36.
Only two off-card picks, both punt-fit: R2 Giannis (card: Jalen
Williams) and R13 Trayce Jackson-Davis (card: Ellis). R1 KAT was the
card's own #1 — first time in the v2 epoch the owner's anchor and the
card agreed at the top.

## LEDGER row

`| 44 | 7 | 23.64 | 88.7 | 2 | 12 | v2, standard room; three-team race
(Cayas 25.08, owner 23.64, Noah 21.66, cliff to 7.77; Kyle LAST from
slot 12 — his two-win run was seat texture). EIGHTH optimal declaration
in nine punted drafts: FT%/3PTM/PTS #1 of 84 at **+32.97, new record**
(FG% +13.02 rank 1 — strongest single cat ever; REB/BLK also rank 1).
BUT AST died undeclared (11, −4.06) — the m34/m35 dead-kept-cat returns:
a 5-of-9 build with zero slack, priced 2nd only because all five live
cats are rank 1-2. Doctrine refinement: a punt frame needs one genuine
playmaker or AST must be declared. Card exact-#1 6/13, Top-5 11/13 (best
since m36); only two off-card picks, both punt-fit
(`season_sim_mock44.py`, `m44_replay.json`) |`
