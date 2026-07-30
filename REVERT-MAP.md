# REVERT-MAP — rollback recipes per layer (2026-07-30)

Every codified change in this repo is an atomic, documented commit with
its validation evidence in `arena/results/`. Any layer can be reverted
independently in minutes without touching the others. The deck rebuilds
from any commit (`python3 scripts/build_deck.py` after checkout of the
relevant files) and republishes to the standing artifact URL.

## Kill switches (no revert needed)

| Layer | Switch | Effect |
|---|---|---|
| Slot-gated gradient ordering | set `GRAD_SLOTS = 0` in `arena/arena.py` AND `docs/draft-deck.html` (one constant each) | gradient ordering off everywhere; 🎯 display + composite ordering unaffected |
| 🎯 confidence display | remove the `gc` span block in the Top-5 loop (single block, marked) | display gone; ordering untouched |
| 🧭 Draft Compass | remove the compass block (marked, self-contained; absorbed the retired ⚖ meter and 🪙 chip 2026-07-30) | shape guidance line gone |
| Archetype layer | remove the `at` tag block + roster census + drop `ar/fx/sy` from build_deck.py (scripts/archetypes.py standalone) | chips gone; data fields regenerate away next build |
| Market-timing chips / ladder | display blocks in the app script, all marked | display-only by construction |

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
