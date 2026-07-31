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
| 13 | 3 | 10.05 | 72.0 | 5 | 9 | old instrument |
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

Verified superlatives: best champ% = m24; worst = m23; best playoff% =
m25; m21 was the best at the time it was drafted. **Streak facts:** the
only consecutive 1st-place pair is m24→m25. Mocks 22 and 23 (11th, 12th)
sit between m21 and m24 — there has never been a three-draft winning run.

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

**Verified: 8 arms — 5 COST, 3 WASH, 0 where the deviation clearly won.**

**Correction to prior debriefs.** Mock 24's debrief claimed deep
deviations were "0-for-6 across the ledger". Two errors: the sample is
8 arms, not 6, and three of them are WASHES, not losses. The defensible
statement is narrower: *no CF-tested deviation has ever clearly beaten
the card (0 of 8), but 3 of 8 cost nothing measurable.* The m25 pair
(KD board-13 free, Tatum board-5 costly) further shows board depth is a
weak proxy — **who you gave up predicts cost better than how deep the
deviation was.**

Note also that these arms are not all independent single-pick tests: m19,
m22 and m23's arms each bundle 3 swaps, and m25's two arms both target
the same passed player. Treat the tally as directional, not as 8
independent trials.

## 4. Empty-roster gradient (open question, not a tally)

| Mock | Arm | As drafted | Card-follow | Δ |
|---|---|---|---|---|
| 24 | wemby_to_sga (slot 1) | 29.82 | 15.70 | **−14.12** |
| 25 | wemby_to_sga (slot 2) | 29.19 | 21.66 | **−7.53** |

Two rooms agree the gradient's r=0 pick is beatable by an outlier anchor,
**but both are the same player pair in the same pool** — replication
across rooms/seeds, not across outlier profiles. Registered as a
September experiment; no engine change on this evidence.
