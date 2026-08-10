# REVERT-MAP — rollback recipes per layer (2026-07-30)

Every codified change in this repo is an atomic, documented commit with
its validation evidence in `arena/results/`. Any layer can be reverted
independently in minutes without touching the others. The deck rebuilds
from any commit (`python3 scripts/build_deck.py` after checkout of the
relevant files) and republishes to the standing artifact URL.

## Kill switches (no revert needed)

| Layer | Switch | Effect |
|---|---|---|
| Slot-gated gradient ordering | set `GRAD_SLOTS = 0` in `arena/arena.py` AND `docs/draft-deck.html` (one constant each) | **STALE, corrected 2026-08-09 (audit F59):** since the E9 blend50 ship the deck's Top-5 ordering is governed solely by `ds` — `GRAD_SLOTS = 0` now affects the ARENA and the deck's `fs`/tooltip metadata only, NOT the shipped card order. To change the card order use the decw-ordering kill switch below. |
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

## decw-ordering (E9 blend50, shipped 2026-08-04)

The Top-5 ORDER at every seat is the ΔECW blend50 score (`ds`), replacing
the composite `fs` sort and the slot-1–3 gradient gate. Validation:
`arena/results/findings_2026-08-04_decw_round2.md` (14/14 improved, 0
winner regressions, fresh-seed replicated; JS↔Python ordering parity
182/182 EXACT). **Kill switch:** in the app block, change the scoredAll
sort back to `.sort((a, b) => b.fs - a.fs)` (one line; `fs` is still
computed on every row), restore the fs-unit coin-flip/standout thresholds
(0.25 / 1.5), and revert the score display spans from `ds * 100` to
`fmtZ(fs, 2)`. The engine-block ΔECW section (RAW_COLS … decwScores) and
the `r` array in PLAYERS are inert once the sort reverts — safe to leave.
**Standing kill RULE:** two consecutive out-of-sample mocks where
blend50-follow measures worse than composite-follow beyond noise trigger
this revert plus a written post-mortem (findings file, §Standing caveats).


## named-room (E18 mock cast, shipped 2026-08-04)

Mock seats are held by the 11 named league-mates (`MANAGERS` +
`managerScores` in the engine block; per-draft seat shuffle stored as
`state.cast` in the app's start handler). Validation:
`arena/results/findings_2026-08-04_e18_named_room.md` (smoke 5/5 owner
slots, owner-card parity 7/7 byte-identical, scaled reach band 11/11,
Spearman 0.936; noise model corrected same day by E18b — see below). **Kill switch:** in the app block's start handler, delete
the `if (mockMode) { ... deck.state.cast = cast; }` block — `mockCastFor()`
already falls back to the legacy `MOCK_CAST` persona cast when no cast is
stored, and `advanceAI` dispatches non-manager names through
`strategyScores` unchanged. The engine-block `MANAGERS`/`managerScores`
section is inert once no cast references it — safe to leave. The owner's
ΔECW blend50 card is independent of this ship (parity-proven) and keeps
its own kill switch above.

### E18b amendment (noise model, shipped 2026-08-04)

Owner-reported realism defect (SGA alive at pick 8) fixed:
`managerScores` noise became log-normal on rank (`r *= exp(N(0, noise/
MGR_NOISE_DIV))`, `MGR_NOISE_DIV = 50`), availability became proportional
(`r *= 1 + (1-av)*0.35`, streamers `0.15`), loyalty discount floored at 1;
Noah refit to manual drafter (owner correction: autodraft was 2025-26
only) and Kyle refit to his measured mild reach. Validation:
`arena/results/findings_2026-08-04_e18b_noise_model.md` (all six gates
pass; owner-card parity 7/7 byte-identical). **Narrow revert** (noise
model only, keeps the named room): restore the three lines in `score()` —
`r -= m.loyal[p.n]` un-floored, `r += (1-av)*(streamer?15:40)`, and the
additive `s += rng.gauss(0, m.noise)` after the need bonus — and restore
Noah/Kyle's prior MANAGERS entries. The full named-room kill switch above
also covers this.
