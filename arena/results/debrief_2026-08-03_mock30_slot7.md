# Mock 30 post-mortem — slot 7: the owner's live objection, answered with a number (2026-08-03)

Completed 13-round mock (156/156, snake verified, no duplicates). Replayed
through the shipped app block on the 8/3 pull; 18,000-season headline; five
counterfactual arms at 6,000 × 2.

**This is the draft the owner screenshotted mid-run** at pick #138, asking why
the card recommended a center with five already rostered. The completed state
lets that question be answered by measurement rather than argument.

**Harness validation, incidentally:** the replay reproduces the owner's live
screenshot exactly — same Top-5, same order, and an identical panel
(`Strengths FG% · 3PTM · PTS | Winnable FT% · REB · BLK | Weaknesses AST · ST ·
TO | Soft punt ST 12/12 · AST 11/12`). The offline harness and the live tool
are the same instrument.

## Outcome

| Metric | Mock 30 (slot 7) |
|---|---|
| Champ% | **2.09** |
| Playoff% | 31.1 |
| Finish | 8th of 12 |
| Kept-total | −2.72 (10th) |
| Expected cats won/week | 4.396 |
| 🎯 exact hits | 4/13 |

Roster: Towns, Durant, JJJ, Brunson, LaVine, Embiid, Duren, Norman Powell,
Knueppel, John Collins, McCollum, Anfernee Simons, Caleb Wilson.

Per-category win rates: **PTS 78%, FG% 65%, 3PTM 65%** — and **ST 19%, AST
24%, TO 38%, BLK 41%**. The now-familiar shape: surplus stacked where the
roster already wins, two categories effectively forfeited. Fourth consecutive
draft where the build is scoring-heavy and stock-poor.

## The owner's question, answered

At #138 the card's 🎯 was **Dereck Lively II, C**; the owner took **Anfernee
Simons** instead. Lively went at #139, so the swap is legal and testable.

| Arm | Champ% | Δ vs as-drafted |
|---|---|---|
| As drafted | 2.12 | — |
| **#138 Simons → Lively (the screenshot turn)** | **2.24** | **+0.12 — WASH** |

**The objection was right about that pick.** Following the card at #138 was
worth +0.12pp — indistinguishable from zero, well inside seed noise. The
override cost nothing. And the diagnosis in
`findings_2026-08-03_target_family_defect.md` holds: the `TARGET:
Rim-protecting C` line came from the board's shape, not roster need.

**But the card was right in aggregate, and by a lot.**

| Arm | Champ% | Δ | Verdict |
|---|---|---|---|
| Follow the card at all 9 deviation turns | **8.66** (6th) | **+6.54** | **COST** |
| #66 Embiid (board 13) → Brook Lopez | 4.30 | +2.18 | COST |
| #55 LaVine (board 10) → Christian Braun | 2.04 | −0.08 | WASH |
| #138 Simons → Lively | 2.24 | +0.12 | WASH |

The two deep reaches that actually cost the draft were **#66 Embiid over Brook
Lopez** (board 13, −2.18pp) and the early ones; the late-round center the
owner questioned was irrelevant either way. **The card was worth listening to
at picks 18–114 and worth ignoring at 138.**

This is the cleanest illustration yet of a pattern the ledger has been
circling: the card's late-round suggestions are low-stakes noise, and its
mid-round structural calls are where the points are. It also breaks the recent
run of DEVIATION WON bundles (m26, m27, m29) — here the full card-follow was
the best line tested.

## Instrument notes — the quiet chip has failed

| | m27 | m28 | m29 | **m30** |
|---|---|---|---|---|
| BUY NOW precision | 84% | 85% | 95% | **100% (36/36)** |
| **Quiet survival** | 50% | 37% | 22% | **0% (0/24)** |

**Every single player the card marked quiet — "safe to wait" — was gone by the
owner's next turn, 24 times out of 24.** Across the four drafts the slide is
monotone: 50 → 37 → 22 → 0.

The BUY NOW side is healthy and getting sharper. The failure is one-sided: the
survival model is systematically optimistic in these value-drafting rooms,
because the mock field takes players by value while the model prices them by
market ADP. A quiet card currently carries no information at all about whether
a player will last.

**Owner-facing implication, effective immediately:** *treat a quiet card as
telling you nothing about survival.* Do not bank on a quiet player still being
there next turn. The BUY NOW marker remains trustworthy.

This escalates September **E2** from a recalibration to a correctness fix, and
it is the strongest candidate yet for a pre-September display fix — a chip
that is wrong 24/24 times is arguably worse than no chip. Registered as
**E13**, below.

- **Drift latch: correctly silent** for the fourth consecutive draft. ST 12/12
  and AST 11/12 are two dead kept cats, one short of the three-cat threshold,
  and the roster had ample bigs. Four straight non-winning drafts with no
  structural alarm is now a substantial body of evidence for **E10**.

## Ledger effects

- Deviation tally gains four arms (2 COST, 2 WASH) → **22 arms: 10 COST,
  9 WASH, 3 DEVIATION WON**.
- Mock 30 row added. Board rank 10 → finish 8; ECW 4.396 → 8th. ECW again
  tracks the finish where kept-total does not.

## New registration

- **E13 — quiet-chip suppression or recalibration.** Measured 0/24 survival in
  m30 and a monotone 50→0 slide across m27–m30 (n=96 quiet observations).
  Options: recalibrate the survival model on value-drafting rooms, or suppress
  the "no marker = safe to wait" semantics entirely until it is recalibrated.
  Bar: BUY NOW precision must not fall below 80% as a side effect.
