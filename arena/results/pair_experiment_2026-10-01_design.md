# Pre-registration — the two-pick 🎯 (D59-2 large) against the D58-3 bar

Written 2026-10-01 before the experiment ran. The verdict and the ship decision
follow this document; nothing below was edited after the numbers landed (the
result file `pair_experiment_2026-10-01.json` carries the numbers and the verdict).

## Hypothesis

The card's 🎯 is the blend50 #1 and is price-blind. When the room prices him far
below his value he waits (target_wait 2026-10-01: deep 🎯s the owner passed on
were still there at the next owner turn 4 of 5) while a near-equal scarce row is
lost. A 🎯 chosen on the expected value of the next TWO owner turns (`pairDecision`,
engine block; `hoops.pair_decision` twin) takes the scarce row first and the deep
row next turn, and the roster that results is worth at least as much.

## Rule under test (shipped code, PAIR_MARKER switch)

For the Top-5 rows in blend order, with s_j the price-only survival to the
look-through next owner turn and ΔECW(j | i) from the weekly model with i on the
roster: pair_i = ΔECW_i + Σ_j s_j · Π_{k before j}(1 − s_k) · ΔECW(j | i) + residual.
The marker moves to argmax only if the gain over row 1 ≥ 0.01 cats/week and
row 1's survival ≥ 0.60. Order never changes. An urgent pin still outranks it.

## Design

- Rooms: the eight public live rooms with committed states and deck cards —
  mocks 51, 52, 53, 54, 56, 57, 58, 59 (55 is the cast room, excluded). Each
  graded on its own pool tag (the pool the owner drafted against).
- Prices for survival: the Yahoo price baked into the page the owner drafted
  against (its deck revision, F8) when that page carried one; else the internal
  market position the page used before F8 (mocks 51, 52). Recorded per room.
- Two chains per room, built the way `stage_arms` builds the self-consistent
  follow-the-card chain (strict pairwise swaps with a pick that went later to a
  non-owner seat; the owner veto applied where the room had it): (A) follow the
  blend 🎯 (the shipped card); (B) follow the two-pick 🎯. Identical code path,
  the only difference being the candidate order at each owner turn.
- Grading: `run_arm` on the real 8-team no-bye bracket, 6,000 seasons per seed,
  seed set S1 = (11, 23, 47) (the standing set) and S2 = (5, 17, 29).
- Validity check: chain (A) must reproduce each room's recorded
  `follow_card_selfconsistent` swaps from `m<NN>_arms.json` where that file
  exists on the same pool tag.

## Bar (D58-3, as applied to D59-2 large)

Mean title odds of chain (B) across the eight rooms ≥ chain (A) on BOTH seed
sets. Reported but not the bar: per-room results, the number of turns where the
marker moved, ECW of each chain.

## Decision rule

- Bar holds and the marker moved at ≥ 1 turn across the rooms → ship the marker
  (PAIR_MARKER = true) in v40.
- Bar holds but the marker never moved → the rule is inert on the evidence; ship
  PAIR_MARKER = false (the advice sentence still says when the read fires) and
  revisit after the next live room.
- Bar fails on either seed set → PAIR_MARKER = false; the sentence ships as
  advice only; the failure is written up.
