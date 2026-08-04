# Self-critical system analysis — owner-requested (2026-08-04)

**The owner's prompt:** ~6 days of Fable capability remain; conduct a
self-critical analysis of weaknesses in the tool's computation and
knowledge/logic layers; name what is still needed from the owner. "With the
last several drafts, I feel like we are still a ways away."

**The feeling is backed by the record.** Same-instrument ledger, mocks 16–30:
4 wins in 15, and the last four drafts (m27–m30, slots 4–7) finished
7th / 6th / 5th / 8th — zero wins, all with the same measured shape: surplus
stacked in categories already won, two-plus categories forfeited. This
analysis is ordered by how much each weakness contributed to that run.

The arithmetic layer is explicitly NOT on this list. Two full audits, exact
JS↔Python parity, byte-identical determinism, 130-state gauntlets — the
z-math, the sim mechanics, and the build pipeline have never produced a wrong
number. The weaknesses are in what the numbers *optimize*, what feeds them,
and what I have claimed on top of them.

---

## T1 — The core objective is misaligned with how H2H is won

**The single deepest computational weakness.** The Top-5 ranks by additive
z-value (composite = council + judgment + slide). H2H 9-cat is won by taking
5 of 9 categories in a week. Additive z does not saturate: the 4th unit of
PTS surplus scores the same as the 1st, though it buys nothing once the
category is already won ~75% of weeks.

Measured, repeatedly:

- m27: room's best kept-total (+5.72, 1st of 12) → finished 4th–7th at 9.53%.
  Won PTS 73.9% of weeks; ST stood at 29.2%; expected cats won 4.64 vs the
  5.0 needed.
- m28 controlled oracle pair (LEDGER §5): identical hindsight, opposite
  objectives — kept-total-maximizer finished **11th (0.28%)**, expected-cats-
  won-maximizer finished **1st (34.58%, above the all-time record)** with a
  *negative* board.
- Every winner's ECW ≥ 4.90 (m21 5.054, m24 5.059, m25 5.102, m26 4.898);
  every mid-table finisher ≤ 4.67 (m27 4.641, m28 4.665, m29 4.643, m30
  4.396). The line is clean across all 12 same-instrument drafts:
  corr(champ%, ECW) = +0.931 vs +0.828 for kept-total, and *within* rooms
  kept-total has even run negative (m28: −0.29).

The gradient (slots 1–3) is the right *kind* of objective — marginal
category-win probability — but the gradient-gate experiment showed the
current implementation loses at seats 4–6 (2 of 3 rooms, badly). So today
the tool optimizes the wrong quantity at 9 of 12 seats and an
imperfect version of the right quantity at 3.

**Fix path:** E9 — a draft-time ΔECW score (marginal expected-cats-won under
the survival model, not foresight). Buildable and testable against all 15
ledger replays *now*; the E11 placebo methodology exists; ship bar is
pre-registered (beat composite without regressing m21/24/25/26). This is
the highest-leverage item for the remaining Fable window, pending owner
authorization since it is an engine change under the freeze.

## T2 — No external validation: every grade comes from a simulator we built

The deepest *epistemic* weakness. Champ%, every counterfactual, the chip
calibrations, ECW itself — all are readings of `arena.simulate_seasons`,
whose weekly model (CV constants, TEAM_WEEK_SHOCK, PCT_MIX_INFL, the 0.88/
0.75/0.60 availability tiers) was estimated from research, not fit to any
real league's observed weeks. ECW predicts the sim well partly *because it is
computed from the sim's own model*. If real Yahoo weeks are noisier, or
percent categories swingier, or GP distributions fatter-tailed than modeled,
every effect size in the ledger shifts by an unknown factor.

**Fix path:** backtest against reality. The owner's actual league history —
last season's final standings, weekly category records, and draft results
(Yahoo exports all three) — would let the weekly model be validated and re-fit
against real outcomes. This is the single most valuable data the owner can
provide. Without it, the honest label on every number in this repo is
"simulator-conditional."

## T3 — The room model is not the owner's room

All calibrations are against 11 fixed personas (2 market seats, 9
value/strategy seats including two punt personas). Real Yahoo rooms track
ADP far more tightly than value-drafting bots. Consequences, already visible:

- The market board (`MKT_RANK`) is my constructed estimate; the survival
  model was *just* recalibrated (8/4) to mock-room behavior — the blend's
  9/11 value weight is right for the arena and probably wrong for September.
- m22 measured punt-mode BUY NOW at 54% — the chips mis-time whenever the
  room's behavior diverges from the model, and a real room is a third
  behavior none of this has seen.
- Effect sizes in counterfactuals (interior worth, deviation costs) are
  conditional on how *these* bots respond, n=1 room type.

**Fix path:** September consensus ADP (registered) re-anchors the market
half; the calibration harness now produces tables on demand, so re-weighting
is a one-day job when ADP lands. But the bigger unlock is T2's league
history: if the same opponents return, last year's draft IS the room model.

## T4 — The projection layer: single-source, no uncertainty, hand-tended

- 246 hand-authored per-game projections. No variance per player — the card
  cannot distinguish a safe −0.5z veteran from a boom/bust −0.5z youngster,
  so risk preference is unexpressible.
- 14 rookie rows are the least defensible numbers in the pool (Dybantsa,
  Boozer, Peterson, Harper, Wilson…), and rookie-hype pins in the market
  model compound the guess.
- Unsigned FAs (Harden, DeRozan, Beal) carry projections with no team; a
  landing spot moves usage materially and the judgment layer catches it only
  as fast as the manual news pull runs.
- Availability is three flat tiers; real GP is heavy-tailed, and the arena's
  weekly tiers (0.88/0.75/0.60) were never fit to observed GP data.

**Fix path:** owner names the projection sources he trusts for a cross-check
when September numbers publish; a variance column is an engine change for the
September run (registered candidate, not yet an E-item).

## T5 — The tool grades picks; nobody grades the plan

The deviation tally (22 arms) shows full-bundle card-follows swinging from
−8.71 to +6.54 — the card is a greedy per-pick advisor with no memory of
where the build is going. Meanwhile the last three rooms were each won by a
*concentrated* build (m28's ECW oracle shape; m29/m30's punt_ft persona
winning 5 cats by construction), and the doctrine correctly forbids
*declared* punting (G1a: −5 to −11pp) — but the tool has no way to steer
toward the emergent concentration that keeps winning. The panel narrates the
state; nothing owns the destination. The drift latch marks only catastrophe;
m27–m30 lived and died in the unmarked "quiet zone" (E10).

**Fix path:** the same ΔECW objective from T1 resolves most of this
naturally — marginal category-win value falls to ~0 in saturated *and*
hopeless categories, which is emergent concentration without a declared punt.
E10 (quiet-zone marker) covers the narration gap.

## T6 — The knowledge layer: my inductions keep failing at small n

The honest audit of my own reasoning, because the owner asked: the measured
layer has never produced a wrong number, but the *generalization* layer has
been wrong repeatedly — the owner-caught "3rd straight" fabrication; the m13
LEDGER row; "0-for-4/0-for-6" tallies; "no deviation has ever clearly won"
(falsified next draft); "the card is reliably wrong as whole-draft policy"
(withdrawn next draft); the r=0 gradient claim (reversed); the gradient-gate
hypothesis (refuted same day it was raised). Pattern: pattern-matching on
3–5 non-independent observations and writing it as law. Mitigations now in
force (LEDGER derivation rule, adversarial verification, withdrawal notes)
are working — every recent failure was caught in-session — but the residual
rule stands: **doctrine lines ("structure ≫ price ≫ name") are working
hypotheses at n≈15 drafts in one synthetic room, not laws.** They should be
re-tested, not trusted, when the real room arrives.

## T7 — Smaller known items (tracked, honest, not urgent)

- Punt-mode chip curve still uncalibrated (single m22 observation).
- `ar/fx/sy` + `gradImpact`: 7.8KB baked and unconsumed (E7 checkpoint).
- Judgment layer is small, hand-authored, staleness-prone by design (manual
  pulls are the owner's standing instruction).
- Roster/lineup config is assumed Yahoo-default (PG SG G SF PF F C C U U +
  3 BN, weekly H2H each-cat). If the owner's league differs at all, lineup
  weights, ECW, and the FLOOR constants all shift.
- Mocks 10–26 harnesses remain unreproducible from a fresh clone (results
  survive; re-derivation doesn't). Backfill is an open owner decision.

---

## What I need from the owner, in priority order

1. **Last season's league history** (Yahoo → League → export, or screenshots):
   final standings, weekly category records if visible, and the draft board.
   Unlocks T2 (real-world backtest) and T3 (real room model). Highest value.
2. **Exact league settings**: team count, scoring type (H2H each-category?),
   lineup slots, bench/IL count, weekly or daily lineups, games-played caps,
   playoff format/weeks, keeper rules if any.
3. **Returning opponents?** Same league as last year, and roughly how many of
   the same managers. Even qualitative reads ("two guys always punt FT%",
   "one auto-drafts") are usable room-model input.
4. **Draft logistics**: date, snake vs auction, and slot when known.
5. **Risk preference**: chase ceiling or protect floor — this sets how
   rookies and injury-risk players should be priced for *you* specifically.
6. **Trusted projection sources** for a September cross-check (or explicit
   OK to use public consensus when it publishes).
7. **Authorization decision** on the T1 prototype: build and test the ΔECW
   draft-time ordering now against the ledger replays (measure-only first;
   ship only if it beats the composite without regressing the four winners).

## Proposed use of the ~6 Fable days (pending owner's word)

| Priority | Work | Status |
|---|---|---|
| P1 | ΔECW draft-time ordering prototype + ledger-wide test with placebo arms | needs authorization (engine change if it passes) |
| P2 | E8 reporting swap — ECW column derived for every retained mock | reporting-only, no authorization needed |
| P3 | E10 quiet-zone measurement (what should have flagged m27–m30) | measure-only |
| P4 | Ingest owner's league history + settings; re-fit lineup/room constants | needs items 1–2 above |
| Deferred | Market re-weight, punt-mode curve, variance column | September (ADP-dependent) |
