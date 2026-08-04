# Mock 27 post-mortem — slot 4: the best board in the room finishes 4th–7th (2026-08-03)

Completed 13-round mock (156/156, snake verified pick-by-pick). Same seat
as mock 21, the lab's first 26.73% draft. Replayed through the shipped app
block on the 8/3 pull; seasons 6,000 × 3 seeds; six counterfactual arms
6,000 × 2 (one rejected as an illegal swap, correctly).

Run with a 9-agent workflow: 6 parallel CF arms + 3 adversarial verifiers.
**Two of my own claims in this write-up were refuted by those verifiers
before publication, and one pre-existing LEDGER row was found defective.**
Both are recorded below rather than quietly corrected.

## Outcome — the first board-1st / finish-outside-top-3 split

| Metric | Mock 27 (slot 4) |
|---|---|
| Champ% | **9.53** |
| Playoff% | 62.4 |
| Finish | **4th–7th** (nominal 7th; slots 4/8/5/11 span 1.30pp, inside the ~2pp trust threshold) |
| Kept-total | **+5.72 — 1st of 12, the room's best board** |
| 🎯 exact hits | 4/13 |

Roster: SGA, Tatum, Murray, Brunson, Kessler, Embiid, Mikal Bridges,
Avdija, Edey, DeRozan, McCollum, Mathurin, Horford.

Four prior drafts held the room's best board (m16, m21, m24, m25) and all
finished top-3, three of them 1st. Mock 27 is the first to miss.

## What actually caused it — and two wrong answers I published to myself first

**Wrong answer #1: "the dead steals category."** ST is 12th at −6.00 z, and
the panel named it from #93 onward. But a verifier isolated every category
by monkeypatching the weekly model: ST *is* the largest free lever (+7.07pp
if lifted to league median, next best REB at +2.12) — and **no achievable
roster in the tested set converts more than ~1pp of it.** CF1 (Bridges→Suggs)
bought +0.76. CF6 (two-defender repair) bought +0.71. Meanwhile the arms
that left ST dead last gained 2–3× more (+2.81, +2.02), and the arm that
repaired ST all the way to 6th **lost 8.71pp**. ST is the biggest deficit;
it is not the proximate cause.

**Wrong answer #2: "the roster is too flat."** Refuted outright by the
winners' own shapes: m24 — the lab record at 29.66% — peaks at *4th*, flatter
than m27's peak. m21, m25, m26 all peak at 3rd and all finished 1st. A
3rd-best category is the winners' normal shape, not a defect.

**What survives: a conversion failure.** The surplus sits where it buys
nothing. Measured in the simulator's own units — average per-category win
probability against the other eleven rosters:

| | m27 (9.53%) | m27's winner, slot 9 (17.91%) | m25 (29.00%) |
|---|---|---|---|
| PTS | **73.9%** | 52.4% | 60.6% |
| FT% | 60.6% | 53.4% | 61.5% |
| ST | **29.2%** | 71.0% | 36.6% |
| REB | 42.5% | 71.3% | 62.7% |
| **Expected cats won / week** | **4.64** | 4.82 | **5.10** |

You need **5.0 of 9** to win a matchup. Mock 27 wins 4.64 — it loses the
average week. Winning PTS 73.9% of the time pays exactly the same single
category as winning it 51%; the ~23 points of surplus there are
unconvertible, while ST at 29.2% is a standing loss. Kept-total counts that
surplus at face value because it treats z as fungible across categories.
H2H does not.

**The metric this exposes.** Expected-cats-won predicts outcome far better
than the kept-total the debriefs have been quoting as "board rank":

| Predictor (mocks 16–27, same instrument, n=12) | corr with champ% |
|---|---|
| Kept-total (what "board rank" means today) | +0.828 |
| **Expected categories won per week** | **+0.931** |

Every mock at ≥5.0 finished 1st (m21 5.054, m24 5.059, m25 5.102); m26 at
4.898 finished 1st; everything ≤4.78 finished 4th or worse. Mock 27's 4.641
sits exactly where its finish did.

*Honest bound:* this is **not** an independent predictor. It is computed from
the same `team_week_model` the simulator uses, so it is a better *readout of
the instrument*, not new causal knowledge. Its value is to the reporting
layer — it explains cases kept-total gets wrong — and it is untested as a
draft-time signal. No engine change; the freeze holds.

## A related reporting defect: the ranks we quote are not the ranks the sim scores

The per-category ranks in every debrief come from unweighted 13-player
z-sums. The simulator scores lineup-weighted weekly means. For this roster
they disagree in four of nine categories:

| Cat | Quoted (z-sum) | Sim's actual | |
|---|---|---|---|
| ST | 12th | **11th** | the "dead last" is a descriptive artifact |
| REB | 5th | **8th** | |
| FT% | 3rd | 4th | |
| BLK | 6th | 7th | |

Flagged, not fixed — changing the debrief frame is a September decision, and
the direction of every conclusion above is unaffected.

## Counterfactuals — pick-by-pick right, policy-wise catastrophic

Paired against an as-drafted run at the arms' own config (6,000 × [11,23] =
**9.76**, not the 3-seed headline 9.53).

| Arm | Champ% | Δ | Verdict |
|---|---|---|---|
| As drafted | 9.76 | — | |
| CF3 — **all 8 deviations → the card** | **1.05** (10th) | **−8.71** | **DEVIATION WON** |
| CF2 — Mathurin (board **44**) → Wendell Carter | 12.57 (4th) | +2.81 | COST |
| CF5 — Embiid (board 15) → Coby White | 11.78 (4th) | +2.02 | COST |
| CF1 — Mikal Bridges → Suggs (the ST repair) | 10.52 | +0.76 | WASH |
| CF6 — two-defender ST repair | 10.47 | +0.71 | WASH |
| CF4 — rejected: Camara went #113, four picks *before* the #117 turn | — | — | illegal swap, correctly refused |

**The non-additivity is the finding.** Following the card at two individual
turns was worth +2.81 and +2.02. Following it at *all eight* produced the
worst line measured — 1.05%, 10th — while carrying the **highest kept-total
of any m27 arm (+7.68)** and a **repaired ST (6th)**. The two things the
board-quality story says should win, both maximized, in the worst roster.

Ledger tally after m27: **14 arms — 7 COST, 5 WASH, 2 DEVIATION WON**
(`LEDGER.md` §3). The deep-reach law took another hit: the board-44 reach at
#141 — the deepest deviation ever tested — cost 2.81pp, but the board-15
reach at #69 cost about the same (2.02pp). Depth still does not predict.

## Instrument notes

- **Chips:** BUY NOW 31/37 gone before the next turn (**84%**), squarely in
  the 83–91% normal-mode band. Quiet survival 50% — below the 82% seen in
  punt mode and worth watching, but n=22 on one draft.
- **Drift latch: correctly silent.** Its condition (≥3 kept cats at rank
  ≥11 **and** <2 C-eligible) was never close — one dead cat, four centers.
  This draft is not structural drift, and the alarm was right not to fire.
  It also means **no instrument on the card flags a single-category collapse
  on an otherwise healthy build** — the panel narrated it (ST went from
  🔒 locked strength at #28 to `Soft punt ST 11/12` for six straight turns)
  but "Soft punt" reads as *concede this*, which the CFs say was roughly
  correct anyway (repairs bought ~1pp).
- **The repair was on the card and declined** — at #76 the 🎯 was Jalen
  Suggs, an elite steals guard; the owner took Mikal Bridges. Same shape as
  the m23 finding in the tunnel-vision study. But unlike m23, taking it was
  worth only +0.76pp. Visibility was not the failure here, and neither was
  adherence.

## What this draft teaches

The doctrine has said **structure ≫ price ≫ name** since m22. Mock 27 adds
the missing qualifier: *structure* has never meant "the largest pile of z."
It means enough edge in enough categories to win five of nine — and this
roster bought a third pile of points it had already won instead of the
first steal it hadn't.

The owner drafted the best board in the room and lost with it. That is not
a failure of the picks; nine of thirteen were board top-5, and following the
card everywhere would have been far worse. It is the board-quality *metric*
failing, which is a reporting problem, not a drafting one.

## September consequences (registered, nothing shipped)

- **E8 (new)** — replace or augment "board rank" in debriefs and the LEDGER
  with expected-cats-won; re-derive all retained mocks on the new metric.
  Reporting-layer only, no engine change.
- **E9 (new)** — test expected-cats-won as a *draft-time* card signal
  (marginal Δ-cats-won per candidate). This is the diminishing-returns idea
  the r=0 gradient already implements for slots 1–3 — mock 27 was slot **4**,
  just outside that gate. Bar: must beat the incumbent on the ledger replays
  without regressing m21/m24/m25/m26.
- Sharpens **E6** (slot-3 refinement / k-scheduling) with a concrete
  hypothesis: extend the gradient gate past slot 3.
- **E4** (bundle lookahead) gains its second and largest data point: the
  m27 non-additivity, −8.71pp.

## Corrections log for this draft

1. **My ST-causation claim — REFUTED** by category-isolation experiments and
   the CF arms, before publication. Rewritten above.
2. **My flatness claim — REFUTED** by m24's flatter, record-setting shape.
   Rewritten above.
3. **My saturation proxy — WRONG.** A Φ-based expected-cats-won using the
   *gradient's* fixed σ constants scored m27 at 5.034 (≈ m24/m25) and
   explained nothing. Only the simulator's own variance model gave 4.641.
   The proxy is discarded; the measured version is what is quoted.
4. **LEDGER row m13 — DEFECTIVE, now fixed.** It carried the slot-3 *bot's*
   numbers (10.05 / 72.0 / finish 5 / board 9) instead of the owner's slot-6
   line (13.39 / 77.7 / finish 2 / board 10). All 17 rows were then
   re-derived mechanically from the retained artifacts: 16 of 17 matched.
   See `LEDGER.md` for the correction and the standing rule it adds.
