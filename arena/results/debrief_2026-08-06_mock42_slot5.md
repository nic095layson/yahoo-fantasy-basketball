# Mock 42 debrief — slot 5, NO punt declared (2026-08-06)

Standard room (first post-discard mock; no sharp flag), v2 instrument,
real cast recorded in-state. State: `arena/data/states/draft_state_mock42.json`
(md5 b6372829). Regenerate: `python3 arena/mocks/season_sim_mock42.py`.
Replay: `arena/results/m42_replay.json`.

## Headline — the streak ends, and that is the healthiest possible result

| Metric | Value | Rank |
|---|---|---|
| Champ% | 6.43 (6.75/6.35/6.18 per-seed) | **6 of 12** |
| Playoff% | 52.5 | 6 |
| ECW/week | 4.46 | 7 |
| Kept-total, 9 cats | +4.49 | **2** |

**Kyle (slot 1) won the room at 37.21% / ECW 5.07** — a bot, decisively,
from the Wemby anchor seat. Room: Kyle 37.2, Kevin 13.1, John 10.0,
Cayas 7.6, Oblena 7.2, owner 6.4, then JCo, Martin, Noah, Hegi, Robby,
Will.

One turn after the integrity audit asked "has the room gone soft?", the
standard room produced a bot champion and graded the owner mid-table.
The instrument scores the build, not the seat.

## What happened: a frameless draft, precisely as the doctrine predicts

No punt was declared, and no frame ever emerged. The early picks bought
scoring guards (Haliburton R1, Lillard R2, Jaylen Brown R5); the entire
endgame followed the card's defense shell (R7–R13 ALL exact #1: Braun,
Gobert, Nesmith, Gafford, Ellis + Sarr/McDaniels nearby). The two halves
cancel:

| Strong | TO **1** (+8.15) | BLK 3 (+4.93) | FG% 2 (+1.14) |
|---|---|---|---|
| **Flat** | FT% 7 (+0.17) | 3PTM 7 (+0.29) | ST 7 (+0.26) |
| **Sunk, undeclared** | PTS **11** (−3.62) | AST 10 (−4.67) | REB 10 (−2.17) |

PTS rank 11 *with three scoring guards aboard* — the low-usage shell
drowned them. Effectively a three-cat punt (PTS/REB/AST, implied-optimal
frame +14.94) that nobody declared and the early rounds actively fought:
win TO/BLK/FG%, then coin-flip three ~zero cats every week. ECW prices
that shape 7th.

**The yardstick split, reversed:** kept-total ranks this roster 2nd
(+4.49, mostly TO hoarding — one banked cat) while ECW and the sim say
6th–7th. Every prior split (m37, m39) had ECW right and kept-z wrong;
same verdict here. ECW is the yardstick.

## Card agreement

Exact #1 **7/13**, Top-5 9/13 — but the SHAPE of agreement is the story:
R7–R13 all exact (the shell), deviations all early (Lillard over Mobley,
Brown over Okongwu, NAW over Poeltl, Sarr over Hartenstein). In the
streak drafts the early deviations built a frame the card's late spine
then served. Here the early deviations bought scorers and the late spine
built for defense — collaboration without a declaration has no keel.
(E10's "quiet zone" signature: not drift-latched, not healthy.)

## Integrity postscript (out-of-sample confirmation of the audit)

`integrity_2026-08-06_streak_audit.md` concluded the streak was doctrine
plus tool, not bias. Mock 42 is the natural experiment: same tool, same
standard room, same manager — remove the declaration discipline and the
finish is 6th while a bot wins the room. The doctrine, restated from six
drafts of evidence: **declare the frame the roster wants, spend early
judgment INSIDE it, let the card fill it late.** Skipping step one cost
the streak.

## LEDGER row

`| 42 | 5 | 6.43 | 52.5 | 6 | 12 | v2, standard room; STREAK ENDS — and a
BOT (Kyle, slot 1) wins the room at 37.21/ECW 5.07, out-of-sample
confirmation of the integrity audit. NO punt declared and none emerged:
scoring guards early (Haliburton/Lillard/Brown), card's defense shell
late (R7–R13 all exact #1), the halves cancel — PTS rank 11 WITH three
scoring guards; implied frame PTS/REB/AST (+14.94) undeclared and
fought. Kept-total rank 2 (TO +8.15 hoarding) vs ECW rank 7 — the
yardstick split reversed, ECW right again. First state with cast
recorded in a standard room (`season_sim_mock42.py`, `m42_replay.json`) |`
