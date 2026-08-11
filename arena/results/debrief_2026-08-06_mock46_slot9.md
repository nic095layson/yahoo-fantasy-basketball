# Mock 46 debrief — slot 9, NO punt declared (2026-08-06)

Standard room, v2 instrument, cast recorded. State:
`arena/data/states/draft_state_mock46.json`. Regenerate:
`python3 arena/mocks/season_sim_mock46.py`. Replay:
`arena/results/m46_replay.json`.

## Headline — worst v2 result, and the frameless finding replicates

| Metric | Value | Rank |
|---|---|---|
| Champ% | **2.59** (2.43/2.68/2.67 per-seed) | **9 of 12** |
| Playoff% | 30.9 | 9 |
| ECW/week | 4.30 | 10 |
| Kept-total, 9 cats | — | 9 |

Room: Kevin 22.56 (Seat 3), John 20.13 (Seat 1), Kyle 15.86, Robby 11.73,
then a long tail; owner 9th. Roster: Tatum, Lillard, Herro, Flagg,
Embiid, Sengun, Hart, Herb Jones, Clingan, Camara, Gafford, Ellis,
Caruso.

**This is the first negative seat-edge in 14 measured rooms.** Seat 9's
bot baseline is 4.26%; the owner returned 2.59% — **−1.67pp**, breaking a
13-of-13 streak of beating his own seat (mean +13.34pp,
`findings_2026-08-06_seat_equity.md`).

## The frameless finding replicates (EVIDENCE)

Both v2 standard rooms with no declaration are now the two worst results:

| Declaration | Mocks | Mean champ% | Mean finish |
|---|---|---|---|
| **Declared frame** | 40, 43, 44, 45 | **19.91** | **2.2** |
| **No frame** | 42, 46 | **4.51** | **7.5** |

n=2 vs n=4 is a small sample and these are different seats and rooms —
but the separation is total (no overlap: worst declared 12.05 vs best
frameless 6.43), and the mechanism is identical in both frameless cases.

## Mechanism — the same failure, twice

The build has **no strength above rank 2 and no true concession**:
REB 2 (+2.11), ST 6 (+2.54), BLK 4 (+1.31), TO 6 (+0.77), FT% 7 (+0.82),
FG% 7 (−1.44), AST 8 (−1.12), PTS 11 (−2.75), 3PTM 12 (−3.41).

Best implied frame is only **+6.43** (punt 3PTM/FG%/PTS) — the weakest
frame value in the v2 ledger by a wide margin (m44: +32.97, m45: +26.83,
m43: +22.06). Even under its own best frame, AST is dead. The roster is
flat: it wins nothing outright and loses two badly.

Compare m42, the other frameless draft: same signature — scoring stars
early, defensive shell late, halves cancelling, no category above rank 1–2.
**Both times the two halves of the draft pulled in opposite directions.**

## Card agreement — the diagnostic detail

Exact #1 **5/13**, all five in **R9–R13** (Clingan, Camara, Gafford,
Ellis, Caruso — the entire endgame). The first eight rounds are 1/8 in
Top-5: Tatum, Lillard, Herro, Embiid, Sengun, Hart all off-card, with the
card calling KAT, Mobley, Derrick White, Tari Eason, Brook Lopez.

That is exactly the m42 shape: **judgment builds a scoring core early,
the card builds a defensive shell late, and nothing reconciles them.**
With a declared frame, the early deviations and the late spine point the
same way (m43: deviations were all punt-fit stars; m44: Top-5 11/13).

## Read

Three drafts now separate cleanly on one variable. The doctrine is
unchanged and stronger:

> **Declare the frame → spend early judgment INSIDE it → let the card
> fill it late.** Skipping step one has cost 6th and 9th; doing all three
> has produced 1st, 2nd, 2nd, 4th.

Registered honestly: the frameless sample is n=2, both in seats whose bot
baselines differ (Seat 5 4.33, Seat 9 4.26), and no counterfactual arm
was simulated for either. The claim is a strong pattern with a clear
mechanism, not a controlled measurement.

## LEDGER row

`| 46 | 9 | 2.59 | 30.9 | 9 | 12 | v2, standard room; WORST v2 owner
result and the FIRST NEGATIVE SEAT-EDGE in 14 rooms (Seat 9 baseline
4.26 vs owner 2.59, −1.67pp; prior 13-of-13 positive, mean +13.34).
Second frameless draft, and the frameless split now separates completely:
declared (m40/43/44/45) mean 19.91% / finish 2.2 vs frameless (m42/46)
mean 4.51% / finish 7.5, no overlap. Mechanism identical to m42: scoring
stars early (Tatum/Lillard/Herro/Embiid/Sengun all off-card, 1/8 Top-5
through R8), card's defensive shell late (exact #1 on ALL of R9–R13),
halves cancel — no cat above rank 2, PTS 11, 3PTM 12. Best implied frame
only +6.43, weakest in the v2 ledger, and AST dead even under it
(`season_sim_mock46.py`, `m46_replay.json`) |`
