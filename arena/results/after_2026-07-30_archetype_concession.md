# After-report — archetype layer (A) + concession diagnostic (B) (2026-07-30)

Implements the two authorized items from the gap study
(`findings_2026-07-30_gap_study.md`), council-ratified 5–0. Both are
**display-only**: no ranking, arena, or engine behavior changed —
verified by an empty `arena/ + hoops.py` diff, bit-identical arena
determinism, and the council seat holding 2nd/13 in the smoke
tournament.

## A — Archetype layer (shipped)

- **`scripts/archetypes.py`** (new): pinned PCA loadings (PC1
  big-vs-guard 42.3% var, PC2 usage 26.6%) + pool-quantile thresholds
  from the verified study; projects *standardized* z columns scaled to
  unit-variance PC scores; flags compare raw z. `build_deck.py` primes
  it and bakes `ar` (BIG/ALPHA/GEN/3D/""), `fx` (out-of-position
  flags), `sy` (style) into every PLAYERS row — regenerated at every
  daily republish, like the judgment layer.
- **Deck surfaces**: archetype tag on Top-5 rows (✦ marks
  out-of-position providers; Balanced renders nothing — 98 of 246 rows
  are chip-free by design); tag tooltip with profile-not-position note;
  roster panel build census + axis lean (`2 BIG + 1 GEN — big-axis
  lean`); the ⚖ meter names the *lean* and which cats to deepen —
  framing corrected per the G1a causal result (no punt prescription
  anywhere).
- **Fidelity vs the study snapshot**: exemplars exact (Wemby ALPHA
  style +0.20 with 3s/FT-from-big flags; Jokić ALPHA −0.68 +
  AST-from-big; Dyson Balanced + stocks; Amen BIG from PG); counts
  60/21/34/14/112 vs the study's 61/21/36/19/104 — **8/241 flips, all
  at quantile boundaries** (the study's disclosed artifact class;
  both labels defensible for each). The module recomputes column stats
  at build time, so September data regenerates everything coherently.

## B — Concession diagnostic (shipped, reframed per G1a)

- **🪙 chip** ("cheapest cats to stop chasing: X · Y") on the
  recommendation card from R4: `score = cov_gain/0.0905 − sunk/2.148`
  with the board-richness term demoted per the study refinement —
  fully static, computed live from the draft state (opponent roster
  z-sums standardize winnability; elasticity weights from the session
  table).
- **Validation on a known state**: at mock 15's R4 the chip's #1 is
  REB — the study's ground-truth #1 exactly; ST lands #4 (the
  rich-demotion reshuffles the mid-ranks within the same big-axis
  concession family — acceptable for a diagnostic).
- **The causal warning is structural**: the chip's tooltip, the ⚖
  meter, and the footer all state that punt-DECLARING measured −5 to
  −11pp (CRN, t −3.0 to −8.0) and that this line advises what to stop
  paying premiums for — never what to zero-weight. No surface
  prescribes a punt.

## System integrity (the battery)

| Check | Result |
|---|---|
| `arena/` + `scripts/hoops.py` diff | **empty** — display-only confirmed |
| Arena determinism (repeat tournament, seed 42) | bit-identical |
| Council rank (smoke tournament) | 2nd/13 (unchanged) |
| verify_rosters | 246/246, 0 mismatches |
| build_deck round-trip | byte-identical |
| JS↔Python parity | **EXACT** |
| engine/app/data syntax | clean |
| 780-state render invariant sweep | 0 scarcity violations, 0 band violations |
| Baked-field spot checks | Wemby/Dyson exact vs study |
| Council ratification | 5–0 (boundary-flip disclosure; rich-demotion; warning coverage) |

## Not shipped (per the study's verdicts, unchanged)

Threshold gradient (shelved, inconclusive twice); adaptive-R4 punt
(hypothesis only); any punt-declaring or punt-weighting policy
(causally refuted). The ⚖/🪙 surfaces exist to steer *coherent
axis-building*, which is the behavior the six-mock ledger and the
G1a arms jointly support.


## Addendum — 🧭 Draft Compass consolidation + FEATURE FREEZE (same day)

Owner-directed consolidation, council-ratified 5–0: the ⚖ commitment
meter, 🪙 concession chip, and roster lean suffix are **merged into one
always-visible Draft Compass line** — axis gauge (guard ↔ big), lean
value, state (EXPLORING → LEANING → COMMITTED at the measured
archetype thresholds), deepen-list, and stop-chasing list. Net card
density DOWN (3 surfaces → 1). The flat-past-R4 warning survives as
the NO-LEAN state's alarm. The compass informs the punt box and never
gates or prescribes it (G1a stands). State tests: empty → EXPLORING;
mock-17 R4 → COMMITTED GUARD −1.21 (the exact state drafted against);
AD/Gobert/Sabonis/Duren → COMMITTED BIG +1.42; mock-16 top-5 →
LEANING GUARD. Gates: build clean, parity EXACT, syntax clean, old
blocks fully removed.

**FEATURE FREEZE (owner-ratified intent, effective now → September
consensus ADP):** no new engine or display layers. In scope during the
freeze: daily data pulls, mock workups/debriefs, truth fixes to
existing copy, and the already-registered follow-up experiments
(slot-3 refinement, k-scheduling, PCT_MIX_INFL re-estimate, September
re-run of the full ladder). The next feature decision happens on
September data.
