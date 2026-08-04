# Findings — roster-conditional gradient: slot-gated ordering + the 🎯 confidence layer (2026-07-30)

Follow-up to the mock 13–14 pattern (flat composite ordering fails at
shape-critical turns while the card's shelf holds the winner) and the
owner's Confidence-% proposal. Two pre-registered CRN experiments, one
codification, council-ratified 5–0.

## The mechanism

`grad(p) = Σ_c w_c·[Φ((S_c+z_c)/σ_c) − Φ(S_c/σ_c)]` — expected weekly
category wins a candidate adds to *this* roster. `S_c` = roster z-sum
(par = 0 on the replacement-anchored P3 scale), `σ_c(r) = k·√(r+1)/defl_c`
with the G-score weekly-noise deflations. Diminishing returns on
dominated cats, premium on contested cats, ~0 on lost ones — the
formalization of every good manual override in mocks 11–14.

## Experiment 1 — global ordering (36 CRN cells, k ∈ {0.7, 1.0, 1.4})

**INCONCLUSIVE**: best arm k=1.0 +1.06pp, t=0.64. Mechanism verified
behaving as designed (saturates Jokić's stacked AST at pick 1; tops the
weakest cat mid-draft). Slot structure replicated: +7.12pp slots 1–3 vs
−0.97 slots 4–12 — the same fingerprint as the P6 elasticity-weights
experiment (+9.73 slots 1–3). Global ordering NOT codified.

## Experiment 2 — slot-conditional confirmatory (18 fresh cells)

Pre-registered: gradient (k=1.0) vs stock council, **slots 1–3 only**,
six virgin seeds {7,13,21,34,55,89} × 3 slots, 2,500 seasons/arm-cell,
CRN-paired, zero seed overlap with any prior run.

**CODIFY: Δ = +12.67pp champ, t(17) = 4.63, 16/18 cells positive, all
six seeds positive.** Per-slot: S1 +22.19, S2 +8.40, S3 +7.41. Playoff
+34.5pp. Base determinism bit-identical; harness bit-reproduces the
prior experiment's cells. The strongest causal result of the lab to
date. Slot 3 is the weakest edge (both negative cells; 4/6 seeds
positive) — a slot-3-specific refinement test is registered, not run.

## Codified (council 5–0)

- **Arena** (`arena/arena.py`): council seat at draft slots ≤ 3 scores
  by the gradient core (GRAD_K=1.0, GRAD_SCALE=10, punt-respecting via
  `weight(c)`); explicit `grad_k` overrides still win (experiment
  plumbing preserved). Verified: codified arena bit-reproduces the
  confirmatory cell (seed 7 slot 1 → champ 19.16%, exact).
- **Deck** (`docs/draft-deck.html`): when the user drafts from slots
  1–3, the Top-5 ORDER is the gradient (⚡ badge shown, tooltip cites
  the evidence); from slots 4–12 the composite orders. Verified: R1
  gradient order reorders the elite exactly as the arena example
  (SGA > Jokić > Wemby); at mock-14's fatal #62 the gradient core ranks
  Lopez/Ware/Allen over the flat order's Cam Johnson (the counterfactual
  dead-last pick).
- **🎯 Confidence layer (all slots, display)**: every Top-5 row shows
  `% conf · ±X.XX cats/wk` — the candidate's marginal weekly category
  wins for the owner's actual roster, confidence = share of the best
  visible pick. Acid test at mock-14 #62: Lopez 100% · Allen 54% ·
  Cam Johnson 0% · Embiid 0% — the display flags the +3.9pp repair the
  flat card buried. This is the owner's Confidence-% proposal with real
  units instead of a rescaled composite.

Gates: build round-trip OK, JS↔Python parity EXACT, engine/app syntax
clean, arena smoke clean; slot/cadence intel regenerated on the
gradient-council arena (gitignored scratch; regenerated at draft-prime
per SKILL.md). Historical note: arena runs before this commit lack the
slot-gated council; the confirmatory experiments pin their own engines
in scratch and remain reproducible.

## Registered follow-ups

1. Slot-3-specific refinement (drop or keep slot 3 in the gate).
2. k-scheduling by slot (S1 signal is 3× S2/S3).
3. September re-run of the whole ladder on consensus ADP + real weekly
   variance data.
