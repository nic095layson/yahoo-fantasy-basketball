# Mock 40 debrief — slot 4, declared punt 3PTM/TO/FT% (2026-08-06)

**FIRST MOCK GRADED UNDER INSTRUMENT v2 (daily-fill scoring).** State:
`arena/data/states/draft_state_mock40.json` (md5 5710a02c). Regenerate:
`python3 arena/mocks/season_sim_mock40.py` →
`arena/results/season_sim_mock40_out.json`, 18,000 seasons (6,000 × seeds
11/23/47), v2 epoch pinned in the harness. Per-turn replay (v2 deck):
`arena/results/m40_replay.json`.

**Epoch caveat:** absolute champ% is NOT comparable to mocks 10–39, which
were graded by the static-lineup instrument (LEDGER epoch note). Ranks
within this room, the punt audit, and card agreement are unaffected.

## Headline

| Metric | Value | Rank |
|---|---|---|
| Champ% | **26.29** (26.10/26.38/26.38 per-seed) | **1 of 12** |
| Playoff% | **88.0** | 1 |
| ECW/week | **4.94** | 1 |
| Kept-total, 9 cats | +2.77 | 4 |
| Kept-z under declared punt | **+14.76** | 1 (next: +7.94) |

A dominant seat: 26.29% is **1.66× the next team** (15.86), the widest
margin over #2 in any owner win, and the per-seed spread is 0.28pp — the
tightest in the ledger. Playoff% 88.0 and ECW 4.94 both lead the room.

Roster: SGA, Harden, Giannis, Trae, Embiid, Myles Turner, Banchero,
Gobert, Jaden McDaniels, Ausar Thompson, Nesmith, Gafford, Caruso.

## The center question, answered by the data

This roster holds **five C-eligible players** (Giannis, Embiid, Turner,
Gobert, Gafford) — the exact shape the owner flagged as pathological. It
finished FIRST. The distinction that matters, and the reason the m34
failure does not repeat here:

1. **The bigs are the punt.** Declared 3PTM/TO/FT% is the **#1 punt of
   all 84** for this roster (kept-z +14.76 vs +10.58 for the runner-up) —
   the owner's **fifth straight optimal declaration** (m35, m37, m38, m39,
   m40). Bigs cost 3PTM and FT%; both are declared dead (ranks 12 and 11),
   TO sunk to 8th. The concession is coherent, not accidental.
2. **No kept category died.** All six kept cats positive: FG% 2 (+3.51),
   BLK 2 (+4.93), REB 2 (+1.79), ST 4 (+1.40), PTS 5 (+2.23), AST 5
   (+0.89). Compare m34 — the six-center disaster — where AST collapsed
   into the punted cluster as an undeclared fourth punt. Guard equity
   (SGA, Harden, Trae, Caruso, Ausar) is what keeps AST/ST/PTS alive here.
3. **v2 stopped adding centers exactly where v1 wouldn't have.** Card
   C-eligible count by round: R6 4/5, R8 4/5 (roster still had only two
   true centers) → **R10 0/5, R11 2/5, R12 1/5, R13 0/5**. The late card
   led Ausar Thompson (R10), Nesmith (R11), Keon Ellis (R12, R13) — all
   guards/wings — while the owner took Gafford at R12. Under the old
   instrument this is precisely where the all-big card appeared.

**Reading:** the problem was never "centers." It was centers *the lineup
can't start* and *categories nobody declared dead*. v2 prices the first;
the owner's declaration handles the second.

## Card agreement

Exact #1 at **4/13** (R1 SGA, R6 Turner, R10 Ausar, R11 Nesmith), in
Top-5 8/13. An owner-driven build in the m37 mold: the three early
deviations are star injections the card ranked lower (R2 Harden over
Mobley, R3 Giannis over Holmgren, R4 Trae over Amen Thompson) and R5
Embiid, R7 Banchero are punt-fit bigs. The card supplied the late spine
(Ausar/Nesmith) and the owner supplied the star core — the m36/m38
collaboration pattern with the roles reversed by round.

## LEDGER row

`| 40 | 4 | 26.29 | 88.0 | 1 | 12 | **v2 EPOCH (first)** — ECW 4.94, all
three lead the room; 1.66× the next seat, widest owner margin over #2 in
the ledger. Declared punt 3PTM/TO/FT% is the #1 of 84 (FIFTH straight
optimal declaration) and genuinely played (3PTM −5.05, FT% −3.66, TO
−3.28). FIVE C-eligible players and it WINS: all six kept cats positive
(FG% 2, BLK 2, REB 2, ST 4, PTS 5, AST 5) — the m34 dead-AST pattern
absent because guard equity survives. v2's late card went 0–2/5 C-eligible
in R10–R13 (led Ausar, Nesmith, Ellis) where v1 produced all-big cards.
Card exact-#1 4/13, owner-driven (Harden/Giannis/Trae star injections)
(`season_sim_mock40.py`, `m40_replay.json`) |`
