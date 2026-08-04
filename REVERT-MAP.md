# REVERT-MAP — rollback recipes per layer (2026-07-30)

Every codified change in this repo is an atomic, documented commit with
its validation evidence in `arena/results/`. Any layer can be reverted
independently in minutes without touching the others. The deck rebuilds
from any commit (`python3 scripts/build_deck.py` after checkout of the
relevant files) and republishes to the standing artifact URL.

## Kill switches (no revert needed)

| Layer | Switch | Effect |
|---|---|---|
| Slot-gated gradient ordering | set `GRAD_SLOTS = 0` in `arena/arena.py` AND `docs/draft-deck.html` (one constant each) | gradient ordering off everywhere; composite ordering unaffected |
| Single-🎯 system-pick marker | remove the `isRec`/`tgOnPin` marks in the Top-5 loop + pinned row | marker gone; ordering untouched |
| Strengths/Weaknesses header | remove the `#swline` render block in renderDecision | header gone |
| Market-timing chips / ladder | display blocks in the app script, all marked | display-only by construction |

**Display surfaces RETIRED 2026-07-30 (owner: noise)** — all removed in
commits `d2e930d` (archetype tags + roster census) and the simplification
commit after it (🧭 compass line, 🎯 NN% confidence spans, Value/Market
strips, composite title line). The underlying layers stay internal:
`ar/fx/sy` still bake into PLAYERS (currently UNCONSUMED by the live app —
audit 2026-07-31; September checkpoint to drop or re-use), `gradImpact`
remains defined for harnesses/future surfaces, and `cheapestConcessions`
is LOAD-BEARING again — the Soft Punt panel line consumes it (punt-aware
since the 2026-07-31 audit fix). To restore any retired surface,
`git revert` the removing commit (each is atomic and display-only).

## Full-layer reverts (git)

Ordered newest-first; each SHA is the commit that INTRODUCED the layer.
`git revert <sha>` (or checkout the prior SHA's versions of the listed
files), rebuild deck, run gates (verify_rosters, build round-trip,
parity), republish.

| Layer | Introduced | Files | Known-good prior state |
|---|---|---|---|
| Commitment meter + 🎯 boundary copy | `d9e1c80`+ | deck | `a1d01cd` |
| Gradient ordering + 🎯 display | `a1d01cd` | deck, arena | `b7ea017` |
| 9-CAT codification (P1 %-variance, P2 seeding, P3 draftable-156 z, market-mult hygiene) | `b328ef7` | arena, hoops, deck | `1ae3693` — NOTE: reverting this restores the four confirmed instrument/engine defects; do not revert below this line without re-reading `findings_2026-07-30_ninecat_math.md` |
| Market-timing layer + scarcity fix | `fd4edbc`, `0866df1` | deck | `beb2c72` |
| Buckets 1+2 (neutral weights, deck UI) | `8c65750`, `201c23c` | arena, deck | pre-7/28 history |

## What each layer's evidence says (why reverting is NOT currently indicated)

- Neutral weights: +5.59pp t=7.18 (re-quoted on the fixed instrument).
- P1–P3 instrument/engine fixes: anchored to external facts (binomial
  floors, Yahoo's seeding rule, the draftable universe); council
  tournament 4th→2nd; all-pass integrity suite.
- Slot-gated gradient: +12.67pp t=4.63 at 18 virgin-seed CRN cells;
  gated precisely because the global test was inconclusive and the
  mock-15 counterfactual confirmed mid-seat greedy-following hurts.
- Display layers (chips, 🎯, ⚖): never re-rank anything; each carries
  its evidence and its limits in its own tooltip.

Reproducibility: historical experiment harnesses pin their engines
(scratch copies or the 0.35/0.45 field pins) and reproduce against the
SHAs noted in their findings files. Arena numbers before `b328ef7` are
old-instrument and not comparable to current runs.

## 2026-08-04 — owner-directed display fixes (both single-site reverts)

- **Room-mix survival model** (`docs/draft-deck.html`, app block): constants
  `SURV_K/SURV_FLOOR/SURV_W_VAL/SURV_W_MKT`, `VAL_RANK`, `survPhi`, and the
  blended `survivalP(name, pickN)`; chip thresholds BUY ≤0.20 / TOSS <0.40.
  REVERT: restore `survivalP(mkt, pickN)` with Φ((mkt−N)/max(6,0.15·mkt)) and
  thresholds 0.40/0.60, and re-point the three call sites at `MKT_RANK.get`.
  Calibration record: `arena/results/after_2026-08-04_fixes_recalibration.md`.
- **TARGET/BOARD LEAN provenance** (`engine` block `archetypeRead` returns
  `boardOnly`; app block label template). REVERT: drop the `boardOnly` const +
  tip line and restore the fixed `TARGET:` prefix.

