# Mock 33 debrief — slot 8, declared punt FT%/3PTM/PTS (2026-08-04)

**Numbering note (2026-08-05):** this draft was analyzed as "mock 31"
before a parallel session merged its own mock 31 (slot 9, punt
FT%/3PTM/TO) and mock 32 (slot 10, punt FT%/3PTM/ST) to main. Those
numbers are taken; this slot-8 draft is renumbered **33** and its scripts
renamed to match. Same draft, same measurements — identifier only.

**Owner's report:** "Not sure how I feel about this one. Punt was declared
but then system kept only proposing for me to select C."

**Method.** Turn-by-turn replay of all 13 owner turns through the shipped
UI handlers (fake-DOM harness, same instrument as the ledger); 18,000-season
simulation (`arena/mocks/season_sim_mock33.py`); counterfactual arms
(`arena/mocks/mock33_cf.py`); a ledger-wide punt-plumbing audit; and a
lineup/saturation audit. **Every finding was then attacked by an
independent adversarial verifier**; four verdicts came back PARTIAL, and
this debrief reports the CORRECTED numbers only. Corrections that changed
a headline are flagged inline.

**Headline.** The owner's instinct is half right, and the half that is
right is worse than he thinks. **The declared punt has exactly zero effect
on the shipped recommendations — measured structurally, not estimated**
(Top-5 byte-identical at 26/26 owner turns with the punt declared vs
cleared). But that defect is NOT what produced the centers in this draft:
this particular punt (FT%+3PTM+PTS) genuinely implies bigs, and a
punt-aware card recommends centers here too (11/13 turns, same count). The
draft itself finished **4th of 12** with the room's **best board (kept-total
rank 1)**, and the real damage was elsewhere: **AST collapsed into an
undeclared fourth punt.** Critically, **following the card would have been
far worse than what the owner actually did** — full card-follow simulates
at 0.008% championship vs the owner's 9.52%.

---

## 1. What the draft actually produced

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons, seeds 11/23/47) | **9.52%** |
| Playoff rate | 68.09% |
| Finish | **4th of 12** (champ rank 4, mean place 5.30 → rank 4, ECW rank 4) |
| Expected categories won per week (ECW) | **4.630** |
| Board rank (kept-total) | **1 of 12** (+4.67 vs next best) |

Per-category league rank (weekly-model win probability):

| Kept | FG% | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|
| rank | **1** | 3 | **11** | 1 | 2 | 1 |

| Punted | FT% | 3PTM | PTS |
|---|---|---|---|
| rank | 11 | 11 | 12 |

**The finding that matters: AST is a KEPT category with a 0.202 win
probability — clustered with the punted categories (0.144–0.171), not with
the other kept categories (next lowest kept is 0.661).** The declared
three-category punt landed as a four-category punt. The six C-eligible
players account for −4.69 of the team's −4.26 AST z-sum; the declared
PTS/3PTM punt contributes structurally as well (corr(AST, PTS+3PTM) =
+0.487 across this room). Five kept categories at rank 1–3 cannot carry a
9-cat build when the sixth is dead: you need 5 of 9 weekly, and this roster
reliably delivers exactly 5 — with no margin for a bad week.

**Verifier correction, adopted:** the first draft of this analysis called
4th place a "weak-room artifact." That was refuted and is withdrawn. Every
readout here is zero-sum within the room (ECW sums to exactly 54.000 across
12 teams by construction), so none of them can detect room strength; and
measured independently, this room was the **5th most top-heavy of 22**
(leader 34.84%, HHI 0.186) and m33's champ% sits **2.20pp BELOW** what its
ECW predicts from the repo's own 15-mock calibration. If anything the
finish understates the build. Fourth is earned.

## 2. The punt defect — confirmed, and larger than this draft shows

**Mechanism (CONFIRMED, structural).** The shipped Top-5 sorts on `ds`
from `decwScores()`, which takes no punt parameter: it calls
`adjValue(p, new Set())` — an empty punt set — and `pwinsTotal()` loops
over all nine categories. Control experiment: run the real engine at all
26 owner turns across the two punted mocks, once with `state.punt`
declared and once cleared. **The Top-5 was byte-identical 26/26.** The
punt box reaches only display metadata (the `fs` column, the Soft Punt
panel, the warning line). This is a structural zero, not a small effect.

**Counterfactual divergence (CONFIRMED).** Same blend, same α=0.5, only
`adjValue(p, puntSet)` and pwins over kept categories: the #1 changes at
**21 of 26 turns**, the Top-5 set changes at 26/26, and the punt-aware #1
sits at mean shipped rank 11.73 (median 6, max 40) — typically buried
below a card that shows five rows.

**Mock 22 is where this defect is ugly, and mock 33 hides it.** In mock 22
the declared punt was **REB + BLK + FG% — the big-man categories** — and
the shipped card still recommended a center at 8/13 turns and a big at
9/13. The punt-aware card recommended a center at **0/13** (all thirteen
were guards). The owner overrode the card in that draft (his actual pick
was in the shipped Top-5 only 4/13, but in the punt-aware Top-5 7/13) —
he drafted the punt-aware answer without the tool's help. In mock 33 the
punt happens to point the same direction as the punt-blind card, so both
recommend centers and the defect is invisible from the card alone.

**Process failure (mine, disclosed).** This regression entered with the
E9 blend50 ship earlier the same day. The Python reference it was
validated against (`arena/mocks/decw_card_v2.py`) contains no punt logic
either, so JS↔Python parity passed 182/182 EXACT while both sides were
punt-blind — a validation instrument with the same blind spot as the
thing it validated. Worse: the 14-mock ship panel spans mocks 16–21 and
23–30, and **mock 22 — the only punted mock that existed — is the single
number skipped in that range.** `findings_2026-08-04_decw_round2.md`
contains zero occurrences of the word "punt." The ordering that made the
punt box inert was never screened against a declared punt.

**Honest counterweight, not to be skipped:** the punt-blind *value half*
is deliberate and documented. `findings_2026-08-04_decw_round1.md`
diagnosed raw ΔECW spontaneously rediscovering the concession spiral
(worst full-follow −27.6pp) and pre-registered a neutral-value blend as
the regularizer; separately, every punt-DECLARING policy measured −5 to
−11pp (G1a). So a punt-aware card is **not** established as better — the
measurements above show only that it *differs*. What has no documented
rationale is the nine-category `pwinsTotal` half.

## 3. Counterfactual arms (corrected)

| Arm | Champ% | vs baseline |
|---|---|---|
| **ARM 0 — as drafted (owner)** | **9.522%** | — |
| ARM 1 — follow shipped card #1 every turn | 0.008% | −9.51pp |
| ARM 2 — follow punt-aware card #1 every turn | 3.261% | −6.26pp |
| ARM 3 — placebo (matched swap count) | 0.003% | −9.52pp |

**The robust result: both card-follow arms lose catastrophically to the
owner's own judgment.** The owner's deviations are what saved this draft.

**Verifier corrections, adopted:** (a) ARM1 is 3 championships in 36,000
seasons (0.008%), not 0/18,000 — the original discarded the half of the
seasons containing the events. (b) The punt-aware arm's "+3.2pp advantage"
rests on an exact score tie (ds = 0.9957) at turn 8 resolved
alphabetically toward Giannis; the honest statement is **+0.5pp
attributable to the ordering, up to +3.3pp if that arbitrary tie falls the
right way.** (c) The claim that the shipped card is "indistinguishable
from random" is withdrawn — on ECW it beats the random control (3.950 vs
3.450). (d) ARM2's later recommendations were computed against a roster
that arm no longer held (frozen-card limitation); the self-consistent
variant is worth only +0.483pp. Treat arm ordering as directional at n=1.

## 4. Why the card kept saying "center" (corrected mechanism)

Three candidate mechanisms were tested; the audit's first two answers were
refuted by the verifier and are corrected here.

1. **The punt itself.** Punting FT%, 3PTM and PTS removes the categories
   guards win. What remains — FG%, REB, BLK, TO (and nominally AST) — is
   the center's stat line. Both the punt-blind and the punt-aware ordering
   recommend a center at 11/13 turns here. **The tool never said this out
   loud.** The declared-punt warning fires on 3-cat punts and cites the
   G1a cost, but nothing tells the owner *"this punt makes you a
   big-man-only drafter, and AST will die with it."*
2. **`decwScores` has no saturation term at all** (CONFIRMED — it never
   calls `benchBound`, and position never enters the score). A relabelling
   proof holds: rewriting every center's position string to PG leaves
   ECW(kept) bit-identical at 4.041857269.
3. **The bench weight is an amplifier, not a brake** (verifier's finding,
   overturning the audit's claim that it cancels out). Ablating the
   candidate's bench discount at round 13 moves the Top-5 from **5/5
   C-eligible to 2/5**. `BENCH_WEIGHT` inside `teamWeekModel` is the
   measured driver of the late-round all-center card.

Withdrawn as unsupported: "benchBound is structurally unreachable in a
13-round draft" (false — it fires from a 5-man roster; it fired zero times
*here* only because this owner held ≤3 centers through round 10), and the
saturation-elasticity table (arms were asymmetric — the de-saturated arm
lost starting slots, so those deltas measure slot loss, not saturation).

Context worth stating: **the owner's own build is 6 C-eligible of 13.**
He drafted big too; the card did not impose this alone.

## 5. Decision sheet (owner disposes — nothing shipped)

No engine change was made. The feature freeze holds and these are
proposals, ordered by measured support.

1. **Make the punt box honest — pick one.** Either (a) pass the punt set
   into `decwScores` (both halves), or (b) if the punt-blind blend is to
   stay as the validated regularizer, **say so in the UI** — the box
   currently accepts a declaration and silently discards it, which is the
   worst of the three options. My recommendation: (b) now as a
   display-only truth fix, (a) measured in September against mock 22 and
   mock 33 before any ordering change.
2. **Register a punted-draft ship bar.** No future ordering change ships
   without being screened on every punted mock in the ledger. This is the
   specific hole that let today's regression through.
3. **Add a positional-saturation term to `decwScores`** — measured first.
   It has none, confirmed.
4. **Warn on punt implications, not just punt cost.** "FT%+3PTM+PTS leaves
   only big-man categories; expect an all-big card and watch AST" is
   information the owner needed at declaration time.
5. **Re-run the E9 ledger validation including mock 22**, which the
   original panel skipped.

## 5b. Cross-reference: the two punt defects compound

A parallel session's `debrief_2026-08-04_mock32_slot10.md` reports a
different punt failure on a different draft: the owner **declared the
wrong punt** — conceding ST (a rank-3 strength, +1.68z) while keeping TO
(a rank-11 weakness, −4.81z); the inverted declaration was worth +6.5z of
kept value.

The two findings are independent and they compound. That draft shows the
punt box is easy to get wrong; this one shows the tool would not have
corrected it either way, because the declaration never reaches the
ordering. A punt-aware card is the only mechanism that could have
surfaced either problem at declaration time, which raises the priority of
E20/E23 relative to what this debrief alone would justify.

## 6. Bounds

- n is small: the punt audit covered the 2 punted drafts available in
  this session's uploads (26 owner turns, 2 seats). Rates carry roughly
  ±15pp of binomial noise — read 0.808 as "most turns," not a constant.
  **Superseded scope (2026-08-05):** main now also carries mock 31
  (slot 9, FT%/3PTM/TO) and mock 32 (slot 10, FT%/3PTM/ST), so the
  punted-draft screening set for E21 is now FOUR drafts, not two. The
  audit should be re-run across all four before E20 is decided.
- All champ% are simulator-conditional (self-critique N1). The weekly
  category data the owner delivered today (`arena/data/weekly_matchups_2025-26.csv`)
  is the fit set that will finally test this model; it has not yet been
  used here.
- Counterfactual arms use frozen per-turn recommendations; after an arm
  diverges, later card entries were computed against a roster that arm no
  longer holds.
- The arena's own frozen snapshot is not used for these projections (live
  pool, 246 players), so these numbers are not comparable to arena
  tournament rates.

## 7. Provenance

Produced 2026-08-04 by an 8-agent workflow (4 measurement + 4 adversarial
verification, ~750k tokens). Scripts:
`arena/mocks/season_sim_mock33.py`, `arena/mocks/mock33_cf.py`. Replay and
audit artifacts in the session scratchpad (`m33_replay.json`,
`m33_legacy.json`, `ledger_punt_results.json`). Every headline number in
this debrief was independently re-run by a verifier agent; the four
PARTIAL verdicts and their corrections are folded in above rather than
appended.
