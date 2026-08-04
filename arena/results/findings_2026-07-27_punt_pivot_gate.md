# Punt-Pivot Gate Study — 2026-07-27

**Question** (owner, 2026-07-27): is the clear-path rule's 0.7 actionability
threshold (owner law 2026-07-23; deck `puntPath`, gates the lean strip and the
one-click adopt offer) too conservative — should a "strong-calculations live
pivot" be allowed below it?

**Harnesses:** `arena/punt_pivot_experiment.py` (7-variant sweep) and
`arena/punt_pivot_paired.py` (common-random-numbers causal pairing). One
adaptive seat in a fixed 11-personality field drafts council-style until its
gate fires, then commits to a single-category punt. Variants differ ONLY in
the gate. 5 seeds × 1,000 seasons × 2 rotation-rounds = 120,000 championship
samples per variant; frozen 2025-10-21 snapshot.

## Sweep (unconditional, slot-rotated)

| gate | champ% | Δ vs control | pivot rate | paired-seed wins |
|---|---|---|---|---|
| control (never pivot) | 9.032 | — | 0% | — |
| static ≥0.5 | 8.433 | −0.599pp (−6.6% rel) | 70% | 1/5 |
| static ≥0.6 | 8.512 | −0.520pp (−5.8% rel) | 26% | 0/5 |
| static ≥0.7 (current law) | 9.032 | ±0 (never fires) | 0% | — |
| static ≥0.8 | 9.032 | ±0 (never fires) | 0% | — |
| two-gate, rank credit | 8.988 | −0.044pp (noise) | 9% | 2/5 |
| two-gate, z-gap credit | 8.729 | −0.303pp | 7% | 1/5 |

Determinism: control, static70, static80 produced bit-identical boards from
three separate processes (identical decision paths, same seeds).

## Paired counterfactual (the causal test)

Every fired draft redrafted with the gate disabled from the same rng;
both league states season-simulated under identical noise:

| gate | fired | champ% with pivot | without | causal Δ | t | improved/hurt |
|---|---|---|---|---|---|---|
| two-gate rank | 15/120 | 10.52 | 13.68 | **−3.16pp** | −1.58 | 6/9 |
| two-gate z-gap | 13/120 | 13.35 | 12.72 | +0.63pp | 0.32 | 7/6 |
| static ≥0.5 | 76/120 | 7.71 | 9.13 | **−1.42pp** | −1.91 | 36/39 |

The sweep's conditional stat ("champ% when pivoted" of 14.0/16.3) was
almost entirely **selection**: gates fire on drafts that are already strong
(without-pivot counterfactual 12.7–13.7% ≫ 9.0% baseline), and pivoting then
damages or fails to improve them. Loss tails are fat: single-draft causal
deltas reached −24.5pp.

## Mechanism

Mid-draft category ranks are bimodal in a 12-team room (a council-style
roster sits top-4 in 4–5 cats and 10th+ in the rest, with nothing at ranks
5–6). A mid-draft punt therefore concentrates a roster that was not built
for the punt, while a from-pick-1 punt personality builds coherently —
and balanced council drafting keeps the flexibility premium. The 0.7 gate,
which never fires mid-draft, is functionally a "punt commitment belongs at
draft start, not mid-draft" rule — and that rule wins.

## Verdict (pre-committed criteria D1–D4 all applied)

**Keep 0.7.** Lowering it is measurably harmful (−5.8% to −6.6% relative
championship output). The refined z-gap two-gate — the strongest candidate
this study could construct — shows +0.63pp on fired drafts at t=0.32
(indistinguishable from zero, n=13 fired drafts) with an overall ceiling of
~+0.07pp (fire-rate bounded); it FAILS the pre-committed acceptance bar.
The one candidate improvement worth a future generation: reframe the deck's
"no clear path yet" copy to state the empirical finding (build strengths or
commit pre-draft; mid-draft pivots measured net-negative) rather than
implying more winnable cats would justify the pivot.

## Caveats

Arena bots ≠ owner + deck advisory (the gate tested as full auto-commitment;
production semantics only gate an offer). ROUNDS=15 in arena vs codified
13-slot league (relative comparisons unaffected; flagged separately).
Two-gate n_fired is small (13–15 drafts) — powered only to detect ~±4pp.
No production files changed by this study (codify gate: owner sign-off
pending).
