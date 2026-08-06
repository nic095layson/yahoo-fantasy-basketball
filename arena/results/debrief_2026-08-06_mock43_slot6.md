# Mock 43 debrief — slot 6, declared punt FT%/3PTM/TO (2026-08-06)

Standard room, v2 instrument, cast recorded in-state. State:
`arena/data/states/draft_state_mock43.json` (md5 e7b6ec88). Regenerate:
`python3 arena/mocks/season_sim_mock43.py`. Replay:
`arena/results/m43_replay.json`.

## Headline — declare the frame, finish 2nd; the m42 lesson confirmed in one draft

| Metric | Value | Rank |
|---|---|---|
| Champ% | 17.65 (17.22/17.77/17.97 per-seed) | **2 of 12** |
| Playoff% | 81.1 | 2 |
| ECW/week | 4.80 | 3 |
| Kept-z under declared punt | **+22.06** | 1 (next seat: +3.33) |
| Kept-total, 9 cats | −5.24 | 10 |

Room: **Kyle 30.88 (slot 4, ECW 5.12)** — back-to-back room wins from
different seats — then owner 17.65, Noah 17.41, John 7.89, Will 7.15,
Oblena 6.51, JCo, Kevin, Robby, Martin, Cayas, Hegi.

The one-draft experiment pair is now complete: m42 (no declaration,
halves canceling) → 6th; m43 (declared FT%/3PTM/TO, drafted to it) →
2nd. Same tool, same room type, adjacent seats. **The declaration is the
difference, measured back-to-back.**

Roster: Cade, Harden, Giannis, Trae, Eason, Turner, Zion, Duren, Gobert,
Ausar, Claxton, Dylan Harper, Dosunmu.

## Frame quality

**Seventh optimal declaration in eight punted drafts** (m35, 37, 38, 39,
40, 41, 43; m36 ranked #12; m42 declared nothing): FT%/3PTM/TO is the #1
frame of 84 (+22.06 vs +14.67 runner-up) — with the standing endogeneity
caveat that coherent drafting makes its own frame the argmax; the streak
certifies coherence, not clairvoyance. All three declared cats genuinely
sunk (FT% −11.06, 3PTM −9.05, TO −7.18).

**No dead kept category**: FG% **1** (+7.55), AST **1** (+4.35), BLK 2
(+4.36), REB 2 (+3.62), ST 4 (+1.97), PTS 8 (+0.21 — thin but alive).
Two rank-1s including AST — notable because the m34 failure mode was AST
dying behind a big wall; here Cade/Harden/Trae keep it elite while seven
bigs eat the frontcourt cats.

**Yardstick split, fifth confirmation:** kept-total ranks this roster
10th (the punt sinks the 9-cat sum) while ECW ranks 3rd and the sim says
2nd. ECW is the yardstick; the split now has five one-directional data
points (m37, m39, m42, m43 + the m28 oracle pair).

## Card agreement — the streak-era shape again

Exact #1 **6/13**, Top-5 9/13. Deviations all early and all punt-fit
stars: Harden (R2, card Mobley), Giannis (R3, card White), Trae (R4,
card Anunoby), Zion (R7, card Braun). The card supplied the entire
mid-late spine: Eason, Turner, Duren, Gobert, Ausar, Dosunmu all exact
#1. This is the m38–m40 collaboration shape restored after m42's
keel-less version — early judgment INSIDE the frame, card fills it late.

## Bot note

Kyle has now won two consecutive standard rooms from two different seats
(m42 slot 1 at 37.2, m43 slot 4 at 30.9). His profile is the cast's
purest value-drafter (adp_w 0.45, low noise, no loyalties) — in rooms
where sentimental seats leak value, clean value-hoarding wins the bot
tier. Worth watching, not yet a pattern (n=2).

## LEDGER row

`| 43 | 6 | 17.65 | 81.1 | 2 | 12 | v2, standard room; the m42 lesson
confirmed in one draft — declaration restored, finish 2nd (m42 frameless:
6th). SEVENTH optimal declaration in eight punted drafts: FT%/3PTM/TO #1
of 84 (+22.06, next seat +3.33) and genuinely played (FT% −11.1, 3PTM
−9.1, TO −7.2). No dead kept cat; FG% and AST both rank 1 (Cade/Harden/
Trae keep AST elite behind seven bigs). Kept-total rank 10 vs champ rank
2 — yardstick split, fifth one-directional confirmation. Card exact-#1
6/13, deviations = early punt-fit stars, spine all exact. Kyle wins
back-to-back rooms from different seats (30.88)
(`season_sim_mock43.py`, `m43_replay.json`) |`
