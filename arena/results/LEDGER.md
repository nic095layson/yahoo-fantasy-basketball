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
| 18 | CF1 (interior overrides removed) | 4.33 | 0.49 | +3.84pp | debrief only — CF JSON not retained |

**Verified: 4/4 positive from retained artifacts; 5/5 including m18's
debrief-recorded value.** Prior debriefs said "5-for-5 (m13, m18, m19,
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

**Verified: 14 arms — 7 COST, 5 WASH, 2 DEVIATION WON.**

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
