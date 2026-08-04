# Mock ledger — machine-derived from the simulation artifacts (2026-07-31)

**Why this file exists.** On 2026-07-31 the owner caught a false claim in a
debrief ("third straight first-place finish" — mock 23 had finished dead
last two drafts earlier). The subsequent integrity check found the
*measured* layer clean (all 7 headline results and all 26 counterfactual
arms matched their JSONs exactly) but exposed the real weak point: **the
cumulative tallies I carried in prose across debriefs** ("0-for-6",
"5-for-5") were narrative counters with no written membership criteria and
no derivation. One of them was wrong. This file replaces remembered
counters with a derived table and explicit rules.

**Rule going forward: no cumulative tally appears in a debrief unless it
is computed here from artifacts, with its membership criteria stated.**

## 1. Results — every graded mock (owner seat)

| Mock | Slot | Champ% | Playoff% | Finish | Board rank | Note |
|---|---|---|---|---|---|---|
| 10 | 4 | 12.11 | 67.1 | 3 | 2 | old instrument |
| 11 | 6 | 1.76 | 25.5 | 10 | 2 | old instrument |
| 12 | 8 | 4.64 | 48.4 | 7 | 10 | old instrument |
| 13 | 6 | 13.39 | 77.7 | 2 | 10 | old instrument; **row corrected 2026-08-03** |
| 14 | 11 | 5.76 | 53.5 | 6 | 10 | old instrument |
| 15 | 7 | 2.06 | 30.9 | 8 | 10 | old instrument |
| 16 | 3 | 15.37 | 73.1 | 2 | 1 | |
| 17 | 12 | 1.77 | 25.1 | 9 | 8 | |
| 18 | 2 | 4.32 | 53.9 | 6 | 6 | |
| 19 | 4 | 10.96 | 78.9 | 4 | 2 | |
| 20 | 5 | 6.43 | 61.9 | 6 | 2 | |
| 21 | 4 | 26.73 | 91.2 | 1 | 1 | |
| 22 | 11 | 0.22 | 6.9 | 11 | 9 | declared 3-cat punt |
| 23 | 12 | 0.16 | 4.2 | 12 | 9 | silent structural drift |
| 24 | 1 | **29.66** | 92.4 | 1 | 1 | best champ% measured |
| 25 | 2 | 29.00 | **94.4** | 1 | 1 | best playoff% measured |
| 26 | 3 | 22.61 | 85.6 | 1 | 3 | third gradient seat |
| 27 | 4 | 9.53 | 62.4 | 7 (4–7, see note) | 1 | **best board, first to miss top-3** |
| 28 | 5 | 6.44 | 63.2 | 6 | 5 | ECW 4.665; kept-total *anti*-correlated in this room |
| 29 | 6 | 8.99 | 58.7 | 5 | 10 | ECW 4.643; board rank 10 yet 5th — board *under*-rates this one |
| 30 | 7 | 2.09 | 31.1 | 8 | 10 | ECW 4.396; the owner's live-screenshot draft |

Verified superlatives: best champ% = m24; worst = m23; best playoff% =
m25; m21 was the best at the time it was drafted. **Streak facts:** the
only consecutive 1st-place pair is m24→m25. Mocks 22 and 23 (11th, 12th)
sit between m21 and m24 — there has never been a three-draft winning run.

**Finish precision (m27).** Slots 4/8/5/11 span 9.53–10.83 = 1.30pp,
inside the arena's ~2pp trust threshold, so m27's finish is honestly a
four-way tie for **4th–7th**. The nominal 7th is used in the table for
consistency; the load-bearing fact (outside the top 3) holds at either end.

**Board-rank-1 instances (n=5):** m16 finish 2, m21 finish 1, m24 finish 1,
m25 finish 1, **m27 finish 4–7**. Mock 27 is the first rank-1 board to miss
the top 3.

**ROW CORRECTION 2026-08-03 (mock 13).** The m13 row previously read
"| 13 | 3 | 10.05 | 72.0 | 5 | 9 |" — those are the numbers for the *bot*
in slot 3 (market persona), not the owner. The owner drafted from **slot 6**
(13.39 champ, 77.7 playoff, finish 2, board rank 10), matching
`debrief_2026-07-30_mock13_slot6.md`. The row had scraped the wrong slot.
Found by an adversarial verifier on 2026-08-03; all 17 rows were then
re-derived mechanically from the retained `season_sim_mock*_out.json`
artifacts — **16 of 17 matched, m13 was the only defect**, now fixed. The
irony is recorded deliberately: this file exists to end exactly this class
of error, and still carried one for three days. Re-derivation is now part
of the audit sweep, not an assumption.

## 2. Interior-structural tally — membership rule

*Included:* a counterfactual arm that ADDS or REMOVES interior (C/big)
coverage on the same-instrument engine. *Excluded:* pre-2026-07-30
(old-instrument) analyses, and arms that change perimeter players only.

| Mock | Arm | Base | Alt | Interior worth | Source |
|---|---|---|---|---|---|
| 19 | CF2_interior_removed | 10.72 | 0.73 | **+9.99pp** | artifact |
| 20 | CF3_interior_removed | 6.51 | 4.64 | **+1.87pp** | artifact |
| 21 | CF3_interior_removed | 26.91 | 21.78 | **+5.13pp** | artifact |
| 23 | CF2_interior_repair_only | 0.17 | 3.17 | **+3.00pp** | artifact |
| 28 | CF6_interior_repair (Kessler + Claxton ADDED) | 6.50 | 9.37 | **+2.87pp** | artifact |
| 18 | CF1 (interior overrides removed) | 4.33 | 0.49 | +3.84pp | debrief only — CF JSON not retained |

**Verified: 5/5 positive from retained artifacts; 6/6 including m18's
debrief-recorded value.** Mock 28's arm is the first to measure the effect
by *adding* interior coverage rather than removing it, and it points the
same way (+2.87pp). Prior debriefs said "5-for-5 (m13, m18, m19,
m20, m21)" — that membership list was wrong: m13 predates this instrument
and has no CF artifact, and m23 (which does qualify) was omitted because
it hadn't happened yet. The *count* survived; the *list* did not.

## 3. Deviation tally — membership rule

*Included:* any counterfactual arm that replaces an owner's off-card pick
with the card's 🎯 at that turn. "COST" = following the card beats the
draft by >1pp; "WASH" = within ±1pp; "DEVIATION WON" = the card is worse
by >1pp.

| Mock | Arm | As drafted | Card-follow | Δ | Verdict |
|---|---|---|---|---|---|
| 19 | price_overrides_to_card | 10.72 | 12.93 | +2.21 | COST |
| 20 | tail_to_system_pick | 6.51 | 6.03 | −0.48 | WASH |
| 21 | quickley_to_suggs | 26.91 | 36.48 | +9.57 | COST |
| 22 | deep_deviations_to_target | 0.23 | 0.03 | −0.20 | WASH |
| 23 | deep_deviations_to_card | 0.17 | 2.44 | +2.27 | COST |
| 24 | jjj_to_bane | 29.82 | 35.14 | +5.32 | COST |
| 25 | kd_to_murray | 29.19 | 29.65 | +0.46 | WASH |
| 25 | tatum_to_murray | 29.19 | 33.28 | +4.09 | COST |
| 26 | early_deviations_to_card (3 swaps) | 22.57 | 16.81 | **−5.76** | **DEVIATION WON** |
| 26 | pritchard_to_lopez | 22.57 | 21.91 | −0.66 | WASH |
| 27 | all_deviations_to_card (8 swaps) | 9.76 | 1.05 | **−8.71** | **DEVIATION WON** |
| 27 | mathurin_to_wcj (board-44 reach) | 9.76 | 12.57 | +2.81 | COST |
| 27 | embiid_to_white | 9.76 | 11.78 | +2.02 | COST |
| 27 | bridges_to_suggs | 9.76 | 10.52 | +0.76 | WASH |
| 28 | brunson_to_kessler | 6.50 | 8.40 | +1.90 | COST |
| 28 | all_deviations_to_card (7 swaps) | 6.50 | 7.34 | +0.84 | WASH |
| 28 | bam_to_zubac | 6.50 | 7.09 | +0.59 | WASH |
| 29 | all_deviations_to_card (9 swaps) | 8.90 | 3.21 | **−5.69** | **DEVIATION WON** |
| 30 | all_deviations_to_card (9 swaps) | 2.12 | 8.66 | **+6.54** | COST |
| 30 | embiid_to_lopez (board-13 reach) | 2.12 | 4.30 | +2.18 | COST |
| 30 | simons_to_lively (#138, owner-questioned) | 2.12 | 2.24 | +0.12 | WASH |
| 30 | lavine_to_braun (board-10 reach) | 2.12 | 2.04 | −0.08 | WASH |

**Verified: 22 arms — 10 COST, 9 WASH, 3 DEVIATION WON.**

**Bundle arms cut both ways — the m29 generalisation did not survive m30.**
Three full-bundle card-follows WON for the owner (m26, m27, m29; −5.69 to
−8.71pp) but m30's bundle was the largest COST in the table (+6.54pp). After
22 arms the honest statement is narrower: **a full card-follow has high
variance in both directions and is not predictable from the draft's shape.**
The claim written one draft earlier — "the card is reliably wrong as a
whole-draft policy" — is withdrawn; it was a 3-instance pattern that the very
next draft inverted. See also `findings_2026-08-03_gradient_gate.md`, where following the
card beat as-drafted in only 1 of 3 rooms.

**EXCLUDED as degenerate (m28, `keyonte_to_harris`).** Both players were
*owner* picks (#140 and #149), so the swap only reorders the owner's own
roster and returns the baseline to the last decimal by construction. It is
not a wash — it is not an arm. Recorded here so it is never counted.
Swap arms must be screened for alt-is-also-an-owner-pick before they run.

*m27 baseline note:* the m27 arms are paired against an as-drafted run at
the **same** config as the arms (6,000 × seeds [11,23] = 9.76), not the
3-seed headline (9.53). Pairing the arms to the headline would overstate
every m27 delta by 0.23pp.

**The m27 non-additivity — the sharpest result in this table.** Following
the card at *individual* turns was right twice (+2.81, +2.02), but
following it at *all eight* deviation turns was the worst outcome measured
in the arm set (−8.71pp, 1.05% champ, 10th) — despite that arm holding the
**highest kept-total of any m27 line (+7.68)**. Pick-by-pick correctness
and policy correctness are different questions, and the card is graded only
on the first. This is the same bundle effect m26 showed, now with the sign
reversed and eight swaps instead of three.

**SUPERSEDED 2026-07-31 (mock 26).** The prior statement "no CF-tested
deviation has ever clearly beaten the card (0 of 8)" is now FALSE. Mock
26's bundle of three deep early reaches (Tatum board 14, Sabonis board 19,
Pritchard board 16) beat the card by **5.76pp**. The surviving, weaker
claim: deviations lose more often than they win (5 COST vs 1 WON), and
board depth remains a poor predictor of which is which.

**History of this tally (kept so the drift is visible).** It was first
published as "0-for-4", then "0-for-6" — both wrong on sample size, and
both implying every deviation cost when several were washes. It was
corrected to "0 of 8, 3 washes" on 2026-07-31, and that statement was
itself falsified the same day by mock 26. Current standing claim, and the
only one to quote: **10 arms — 5 COST, 4 WASH, 1 DEVIATION WON.**

Board depth is a weak predictor throughout: m25's board-13 deviation was
free while its board-5 deviation cost 4.1pp, and m26's board-14/19/16
bundle *won*. **Who you gave up predicts cost better than how deep the
deviation was.**

These arms are not independent single-pick tests: m19, m22, m23 and m26
each bundle 3 swaps, and m25's two arms both target the same passed
player. Treat the tally as directional, not as 10 independent trials.

## 4. Empty-roster gradient (open question, not a tally)

| Mock | Arm | As drafted | Card-follow | Δ |
|---|---|---|---|---|
| 24 | wemby_to_sga (slot 1) | 29.82 | 15.70 | **−14.12** |
| 25 | wemby_to_sga (slot 2) | 29.19 | 21.66 | **−7.53** |

| 26 | luka_to_sga (slot 3) | 22.57 | 28.85 | **+6.28 — CARD WON** |

**REVERSED 2026-07-31 by mock 26.** The broad claim "the empty-roster 🎯
is the card's least-trusted output" is REFUTED. With a *different* anchor
(Luka, a conventional high-usage guard rather than an extreme single-cat
outlier), following the card at r=0 was **better by 6.28pp**.

What survives is narrower and *consistent with the original mechanism
hypothesis*: the r=0 gradient appears to undervalue **extreme single-cat
outliers specifically** (Wemby, +7z BLK — 2 instances, both large), and to
be **correct for conventional profiles** (Luka — 1 instance, card wins).
The Φ-saturation story predicted exactly this asymmetry. Still n=3 across
2 anchor types in one pool; September experiment stands, now with a
sharper hypothesis to test. No engine change.

## 5. Board metric — the controlled result (mock 28, 2026-08-03)

*Not a tally; a single controlled experiment, recorded here because it bears
on how every row in §1 should be read.*

Two oracles, identical mechanics and identical hindsight (walk the owner's 13
turns; at each, consider every player drafted strictly later; take the best by
the objective). **Only the objective differs.**

| Arm | Kept-total | Expected cats won/wk | Champ% | Finish |
|---|---|---|---|---|
| m28 as drafted | +1.58 | 4.665 | 6.50 | 6 |
| ECW-greedy oracle | **−0.92** | **5.268** | **34.58** | **1** |
| Kept-total-greedy oracle | **+3.54** | 4.114 | **0.28** | **11** |

Replicated at three fresh seeds (101/202/303, 18,000 seasons): oracle 35.63%,
baseline 6.59%.

**Reading of the "Board rank" column in §1.** It ranks kept-total. Maximizing
that quantity with perfect foresight produced the second-worst roster in the
room, and within the m28 room kept-total correlates with champ% at **−0.293**
while expected-cats-won correlates at **+0.823**. Across mocks 16–28 the
same comparison is +0.828 (kept-total) vs +0.931 (ECW). **Board rank is
retained in §1 for continuity with every prior debrief, but it should not be
read as a quality ranking.** Replacing it is registered as September E8.

*Bound:* ECW is computed from the simulator's own `team_week_model`, so it is
a better readout of the instrument, not an independent predictor. The oracle
has perfect draft-order foresight and is an upper bound, not a strategy.

