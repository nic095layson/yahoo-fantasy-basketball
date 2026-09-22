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

**Backfill complete (2026-08-04, owner-approved):** the full harness set for
mocks 10–30 — every `season_sim_mockNN.py` and every retained `mockNN_cf.py` —
is now committed here. Every LEDGER row is re-derivable from a fresh clone.
Note the older sims read draft states from the original session's uploads
path (`STATE` constant at the top of each file); point it at your own copy
of the corresponding `draft_state_N.json` to reproduce.

## Files

- `live_retro.py <mock> <stage>`, `live_deckcard.py <mock> <deck> <out> [--punt-log]`,
  `live_advisor.py <mock> <deck> <out>`, `live_survival.py <mock> <deckcard.json> <out> [more…]`,
  `live_debrief.py <mock> <out.md>` — the live-room grading set (2026-09-22), generalized
  from the mock-51 scripts below to a mock-number argument, tolerant of poolless opponent
  picks (a human drafts a name the pool lacks: that seat plays short, the names are recorded).
  `live_retro.py 51 final|replay|hindsight` reproduces `m51_*.json` byte-for-byte; mock 52's
  outputs are `m52_*.json` and `debrief_2026-09-22_mock52_slot10.md`. Per-mock config
  (pools drafted against, the punt box as the owner drove it, click moments) sits at the top
  of `live_retro.py` / `live_deckcard.py` / `live_advisor.py`.

- `season_sim_mock27.py` — headline simulation. Rebuilds all 12 rosters from
  the uploaded draft state, runs `arena.simulate_seasons` at 6,000 seasons ×
  seeds [11, 23, 47], and reports champ%/playoff%/kept-total per team plus
  the owner's per-category z-sums and ranks.
- `season_sim_mock28.py`, `mock28_cf.py` — same pair for mock 28. The m28
  CF file additionally carries the two **oracle** arms behind LEDGER §5:
  `CF5_ecw_greedy_oracle` and `CF7_kept_greedy_oracle`. Both walk the owner's
  13 turns and take the best legal later-drafted player by their objective —
  identical hindsight, opposite objectives (34.58% vs 0.28%). They are upper
  bounds, not strategies: they know exactly when every player will be taken.
- `mock27_cf.py` — counterfactual arms. `python3 mock27_cf.py ARM [ARM...]`,
  or no args for every arm. Each arm is a set of **pairwise legal** swaps:
  the alternative must have been drafted strictly *later* than the owner pick
  it replaces (asserted in `build()`; an illegal arm is refused, not run —
  see `CF4_steals_repair`). 6,000 seasons × seeds [11, 23].

## Swap-arm screening (added 2026-08-03)

Before running a pairwise arm, check that the alternative is **not also an
owner pick**. Mock 28's `keyonte_to_harris` swapped two of the owner's own
picks (#140 and #149), which only reorders the owner's roster and reproduces
the baseline to the last decimal. `build_seq()` enforces legality (alt drafted
strictly later) but cannot tell a degenerate arm from a real one — that check
is on the author. See LEDGER §3.

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
