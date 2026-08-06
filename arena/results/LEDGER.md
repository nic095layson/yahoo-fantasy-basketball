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

**Instrument epoch note (2026-08-05, owner-directed scoring audit).** Every
champ%/playoff%/ECW number in this file through mock 39 was graded by the
STATIC-lineup week model (10 starters × 1.0, 3 bench × 0.15, fixed all
week). The scoring audit (`findings_2026-08-05_scoring_model_audit.md`)
measured that real daily-managed Yahoo lineups start ~99.4% of played
games, so the instrument moved to **v2 (daily-fill start rates)** the same
day — started games count 100%, bench games 0, bench backfills open slots
daily. Pre-v2 numbers regenerate exactly with `ARENA_WEEK_MODEL=static`;
cross-epoch comparisons of absolute champ% are not valid. The v2 ordering
consequence is disclosed in `v2_panel_disclosure_out.json` (per E21).
Rows added after this note are v2 unless marked otherwise.

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
| 31 | 9 | 6.16 | 59.4 | 5 | 12 | ECW 4.610; declared 3-cat punt (FT%/3PM/TO) — kept-z +23.50 under own punt, rank 1 by 16 z; cf. m22 (last 3-cat punt: 0.22%, 11th). First lesson-13-compliant harness (`season_sim_mock31.py`, state + out.json committed) |
| 32 | 10 | 4.11 | 39.0 | 9 | 12 | ECW 4.450; declared 3-cat punt (FT%/3PM/ST) — punt INVERTED for the drafted roster (ST kept-rank 3 punted, TO rank 11 kept; single-swap punt-TO worth +6.5 kept-z); five balanced-board picks inside the punt frame (`season_sim_mock32.py`) |
| 33 | 10 | 11.37 | 64.4 | 3 | 7 | ECW 4.650; balanced, NO punt declared — best owner mock since m26; board rank 7 vs finish 3 (ECW out-predicts kept-total again, m29 pattern); implied punt FT%/PTS/REB kept-z +6.50 (`season_sim_mock33.py`) |
| 34 | 8 | 9.52 | 68.1 | 4 | 12 | ECW 4.630; declared 3-cat punt (FT%/3PTM/PTS) — board rank **1** of 12 (+4.67). AST fell to an UNDECLARED 4th punt (kept-cat pwin 0.202, clustered with the punted cats' 0.144-0.171). Punt-box defect measured here: shipped Top-5 byte-identical 26/26 turns with the punt declared vs cleared (`decwScores` is punt-blind); full card-follow 0.008% vs as-drafted 9.52%. Analyzed as "31", then "33", pre-merge; renumbered 34 (a parallel session claimed 31/32/33). Draft fingerprint: slot 8, punt FT%/3PTM/PTS, state md5 4afb5778. (`season_sim_mock33.py`, `mock33_cf.py`) |
| 35 | 12 | 7.11 | 54.7 | 6 | 12 | ECW 4.54; declared punt FT%/AST/3PTM is the OPTIMAL punt of all 84 for this roster (kept-z +15.72, best frame in room) — but KEPT PTS died (rank 12, −2.75z): second straight punted mock with an undeclared extra punt (cf. m34 AST at 0.202 pwin). Shipped-card follow 9/13; the punt-blind card led R4 Pritchard (pool #4 3PM on a 3PTM punt) and R6 Markkanen (E20 evidence). Room: T1 30.77%/ECW 5.02 — above the winners' bar (`season_sim_mock35.py`, `m35_replay.json`) |
| 36 | 1 | 31.18 | 93.4 | 1 | 12 | ECW 5.06 — **BEST OWNER BUILD EVER** (prior best m24 29.82; first above the 4.90 winners' bar; only the m28 hindsight oracle is higher). Card's exact #1 followed 10/13 incl. all of R6–R13; deviations were Giannis/Harden/Sengun star injections. Declared punt FT%/3PTM/TO ranks #12 of 84 (the TO punt never bound — the low-TO role shell held TO to rank 5, +2.02z). blend50 out-of-sample SUCCESS (`season_sim_mock36.py`, `m36_replay.json`) |
| 37 | 2 | 19.04 | 82.2 | 3 | 12 | ECW 4.83; declared punt FT%/TO/3PTM is the #1 punt of 84 AND genuinely played (FT% −10.5, 3PTM −8.9, TO −6.3 sunk) — highest punt-frame kept-z ever (+26.65, prior m31 +23.50); FIRST punted build with all six kept cats positive (no m34/m35 dead-cat). Owner-driven: card exact-#1 followed only 3/13. Kept-total ranks 7th vs ECW/champ rank 3 — the yardstick split again (`season_sim_mock37.py`, `m37_replay.json`) |
| 38 | 3 | 16.46 | 75.2 | 1 | 12 | ECW 4.73 (room max 4.74 — flat room); FIRST PUNTED BUILD TO RANK 1. Declared punt FT%/3PTM/PTS is the #1 punt of 84 (third straight optimal declaration: m35/m37/m38) and genuinely played (FT% −4.5, 3PTM −5.9, PTS −4.4 all sunk). Card exact-#1 followed 8/13; the ONLY two off-card picks (R4 Hart over Okongwu, R8 Sarr over Vucevic) were punt-fit corrections — the m36-spine + m37-frame synthesis. Five kept cats at rank 1–2; AST soft (9, −2.56) but not dead (`season_sim_mock38.py`, `m38_replay.json`) |
| 39 | 4 | 33.98 | 94.0 | 1 | 12 | ECW 4.99 — **NEW BEST OWNER BUILD EVER** (prior m36 31.18; 0.6pp under the m28 oracle; next seat 13.00, a 2.6× gap). FOURTH straight optimal declaration: FT%/3PTM/TO is #1 of 84 (+26.84, new punt-frame record, prior m37 +26.65) and played to the floor (FT% −15.2 deepest sink ever, 3PTM −10.2). All six kept cats positive incl. two rank-1 (FG%, REB). Kept-total(9cat) ranks 10 vs champ rank 1 — the yardstick split at its limit; ECW is the yardstick. Card exact-#1 6/13; off-card = punt-fit stars (Giannis, Trae, Sengun, RJ) (`season_sim_mock39.py`, `m39_replay.json`) |
| 40 | 4 | 26.29 | 88.0 | 1 | 12 | **v2 EPOCH (first)** — ECW 4.94, all three lead the room; 1.66x the next seat, widest owner margin over #2 in the ledger. Declared punt 3PTM/TO/FT% is the #1 of 84 (FIFTH straight optimal declaration) and genuinely played (3PTM -5.05, FT% -3.66, TO -3.28). FIVE C-eligible players and it WINS: all six kept cats positive (FG% 2, BLK 2, REB 2, ST 4, PTS 5, AST 5) - the m34 dead-AST pattern absent because guard equity survives. v2's late card went 0-2/5 C-eligible in R10-R13 (led Ausar, Nesmith, Ellis) where v1 produced all-big cards. Card exact-#1 4/13, owner-driven (Harden/Giannis/Trae star injections) (`season_sim_mock40.py`, `m40_replay.json`) |
| 41* | 4 | 43.84 | 96.7 | 1 | 12 | ***SHARP-ROOM draft** (E25 stress test, since discarded) — NOT a standard-room result and not a ledger record; v2 epoch.* ECW 5.11 (highest ever measured) and 4.9x the next seat, the most lopsided room in the ledger. SIXTH straight optimal declaration: FT%/3PTM/TO is #1 of 84 (+27.43) and sunk to the floor (FT% -13.2, 3PTM -9.9). FOUR rank-1 categories (FG% +9.80 - strongest single category z ever, REB, ST, BLK) plus AST rank 2. Most owner-driven build yet: card exact-#1 only 2/13, six off-card punt-fit picks. First state with an exact recorded cast (`season_sim_mock41.py`, `m41_replay.json`) |
| 42 | 5 | 6.43 | 52.5 | 6 | 12 | v2, standard room; STREAK ENDS — and a BOT (Kyle, slot 1) wins the room at 37.21/ECW 5.07, out-of-sample confirmation of the integrity audit. NO punt declared and none emerged: scoring guards early (Haliburton/Lillard/Brown), card's defense shell late (R7-R13 all exact #1), the halves cancel — PTS rank 11 WITH three scoring guards; implied frame PTS/REB/AST (+14.94) undeclared and fought. Kept-total rank 2 (TO +8.15 hoarding) vs ECW rank 7 — the yardstick split reversed, ECW right again. First standard-room state with cast recorded (`season_sim_mock42.py`, `m42_replay.json`) |
| 43 | 6 | 17.65 | 81.1 | 2 | 12 | v2, standard room; the m42 lesson confirmed in one draft — declaration restored, finish 2nd (m42 frameless: 6th). SEVENTH optimal declaration in eight punted drafts: FT%/3PTM/TO #1 of 84 (+22.06, next seat +3.33) and genuinely played (FT% -11.1, 3PTM -9.1, TO -7.2). No dead kept cat; FG% and AST both rank 1 (Cade/Harden/Trae keep AST elite behind seven bigs). Kept-total rank 10 vs champ rank 2 — yardstick split, fifth one-directional confirmation. Card exact-#1 6/13, deviations = early punt-fit stars, spine all exact. Kyle wins back-to-back rooms from different seats (30.88) (`season_sim_mock43.py`, `m43_replay.json`) |

Verified superlatives (v1 epoch, mocks 10–39 — m40 is v2 and NOT
comparable on absolute champ%): best champ% = **m39 (33.98, 2026-08-05)**
— prior holders m36 (31.18) then m24; worst = m23; best playoff% = m25
(94.4, still standing; m39's 94.0 is #2); m21 was the best at the time it
was drafted. **Streak facts** (epoch-independent, rank-based): the only
consecutive 1st-place pair through m35 was m24→m25; mocks 38→39→40 are
the ledger's longest standard-room first-place streak (m41 was a
SHARP-ROOM draft, excluded; the streak ended at m42, 6th, the first
frameless draft since m33). Mocks 22 and 23
(11th, 12th) sit between m21 and m24.

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
itself falsified the same day by mock 26; the 2026-08-01 restatement ("10
arms — 5 COST, 4 WASH, 1 DEVIATION WON") went stale in place as twelve
more arms accumulated, and on 2026-08-04 this paragraph briefly offered a
second "current" tally contradicting the derived line above — in the file
that exists to end exactly that error (caught by the independent system
review). **No tally in this history paragraph is ever quotable. The only
quotable tally is the bold "Verified" line directly under the arm table,
derived from the table itself.**

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

