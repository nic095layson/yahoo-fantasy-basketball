# Mock post-mortem harnesses

Reproduction code for the graded mock drafts in `arena/results/`.

**Why this directory exists (2026-08-03).** `LEDGER.md` states that its
tallies are "machine-derived from the simulation artifacts." On 2026-08-03
an adversarial verifier found a defective LEDGER row (mock 13 carried a
bot's numbers instead of the owner's); it was caught by *re-deriving* all 17
rows from the retained artifacts. That re-derivation was only possible
because the harnesses happened to still exist in an ephemeral session
scratchpad — they were not in the repo, and `arena/results/*.json` is
gitignored. The integrity property the LEDGER claims was therefore not
actually reproducible from a fresh clone.

**Known exposure:** harnesses for mocks 10–26 still live only in session
scratchpads and are not recoverable once those sessions end. Their *results*
survive in the debriefs and the LEDGER; their *re-derivation* does not.
Mock 27 onward is committed here. Backfilling the earlier ones is an open
owner decision.

## Files

- `season_sim_mock27.py` — headline simulation. Rebuilds all 12 rosters from
  the uploaded draft state, runs `arena.simulate_seasons` at 6,000 seasons ×
  seeds [11, 23, 47], and reports champ%/playoff%/kept-total per team plus
  the owner's per-category z-sums and ranks.
- `mock27_cf.py` — counterfactual arms. `python3 mock27_cf.py ARM [ARM...]`,
  or no args for every arm. Each arm is a set of **pairwise legal** swaps:
  the alternative must have been drafted strictly *later* than the owner pick
  it replaces (asserted in `build()`; an illegal arm is refused, not run —
  see `CF4_steals_repair`). 6,000 seasons × seeds [11, 23].

## Reproduction notes

- Both scripts read the draft state from the uploads path recorded in their
  `STATE` constant. Point that at your own copy of the state JSON.
- Counterfactual arms must be paired against an `as_drafted` run at the
  **same seed/season config** as the arms — not against the 3-seed headline.
  Mixing them overstates every delta (0.23pp in mock 27).
- The per-category ranks these scripts report are unweighted 13-player
  z-sums. The simulator itself scores *lineup-weighted weekly means*; the two
  disagree in ~4 of 9 categories on a typical roster. See
  `debrief_2026-08-03_mock27_slot4.md`.
