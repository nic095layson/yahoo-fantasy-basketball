# Gradient-gate experiment — hypothesis REFUTED (2026-08-03, measure-only)

**The hypothesis.** The deck applies the win-probability gradient to Top-5
*ordering* only at draft slots 1–3 (`GRAD_SLOTS = 3`). Mocks 24/25/26 were
drafted from slots 1/2/3 and all finished 1st. Mocks 27/28/29 were drafted
from slots 4/5/6 — just outside the gate — and all finished mid-table. That
pattern suggested the gate is drawn too tight, and September E6/E9 were
leaning toward widening it.

**Result: the pattern is coincidence. Widening the gate is not supported —
it is actively harmful in 2 of 3 tested rooms.**

## Method

Engine block patched `GRAD_SLOTS = 3 → 12` so the gradient orders the card at
every seat, then mocks 27/28/29 were re-replayed to capture what the gradient
card *would* have recommended at each owner turn. The gradient changes the
recommendation on 10/13, 8/13 and 7/13 turns respectively — the intervention
is real, not cosmetic.

Three arms per mock, 6,000 seasons × seeds [11,23]: as drafted; follow the
**composite** card (what the deck actually showed); follow the **gradient**
card.

## Results

| Mock | Slot | As drafted | Composite card | Gradient card |
|---|---|---|---|---|
| 27 | 4 | **9.76** (6th) | 1.05 (10th) | 3.14 (8th) |
| 28 | 5 | 6.50 (6th) | **7.34** (5th) | 0.30 (11th) |
| 29 | 6 | **8.90** (5th) | 3.21 (8th) | 0.22 (11th) |

- **Gradient beats composite in 1 of 3** (m27, +2.09pp) and loses badly in the
  other two (m28 −7.04pp, m29 −2.99pp).
- **Both cards lose to what the owner actually drafted in 2 of 3.**
- Gradient ECW is lower than composite ECW in all three (4.383/4.158/4.002 vs
  4.237/4.707/4.397 — m27 the lone exception on ECW too).

**Conclusion: do not widen `GRAD_SLOTS`.** The slot-1–3 gate keeps its
original justification (CRN-confirmed +12.67pp, t=4.63, at slots 1–3 only);
the global variant was already measured inconclusive in July, and this
experiment is consistent with that, not with the seat-band story.

## Why the original pattern looked compelling — and why it isn't

Mocks 24/25/26 (slots 1/2/3, all 1st) vs 27/28/29 (slots 4/5/6, all
mid-table) is six different rooms with six different player pools, six
different opponent draws, and — in 24/25 — a Wembanyama anchor that 27/28/29
never had. The seat is confounded with everything else. An adversarial
verifier put the between-cell noise for effects of this kind at ~9.3pp sd
from the repo's own July gap study; the observed "pattern" is well inside it.

## Harness defects found and fixed (both by adversarial verification)

1. **Fatal:** a card can name the *same player at two owner turns*. Swap
   legality was screened against the **original** board while swaps are
   applied against a **running** board, so the second occurrence became
   illegal and an assertion killed the whole arm. **3 of 9 cells died this
   way on the first run** and were initially reported as `champ = -1`
   sentinels. Fixed: the second occurrence is now dropped and recorded
   (`dropped_mid_arm`), not fatal. All 9 cells now produce numbers.
2. The degenerate-arm screen (alternative is also an owner pick — the mock-28
   lesson) worked correctly and caught 4 cases across these runs.

## Residual confounds — stated, not resolved

The verifiers flagged these and they are **not** fixed by the rerun:

- Arms differ in swap count (m29: composite 9 applied vs gradient 10) and in
  reach distance, so "better card" is partly confounded with "more
  perturbation."
- Pairwise swaps hand the owner's player to the rival who took the
  alternative, which changes *field strength* unequally between arms
  (m29: 5.01 vs 1.32 z removed from rivals).
- n=1 room per slot.

A clean version needs a perturbation-matched placebo arm (N random legal
swaps) and many more rooms. Registered below; **not** run here.

## Effect on the September plan

- **E6 / E9 narrowed:** "extend the gradient gate past slot 3" is **removed**
  as a candidate — measured and rejected. E9's remaining content is the
  expected-cats-won draft-time signal under a survival model, which is a
  different mechanism and still open.
- **New E11:** if any future card-comparison experiment is run, it must carry
  a perturbation-matched placebo arm and report field-strength delta per arm.
  Without those, card-vs-card counterfactuals cannot separate the card from
  the disturbance.
