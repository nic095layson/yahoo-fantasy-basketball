# 🏟️ The Arena — self-play draft tournament

Sole purpose: **test the fantasy system's draft-day analysis and league
simulation** by making it draft against itself, at scale. Everything here is
isolated from the production tool:

- **Reads** the production engine (`scripts/hoops.py`) — never modifies it.
- **Own frozen dataset**: `data/players_2025-10-21.csv` — the 2025-26 season
  opening night, reconstructed with no hindsight: October 2025 rosters
  (Giannis on MIL, LeBron on LAL, Brown/George un-swapped, ...), opening-night
  injury statuses (Haliburton/Lillard/Tatum/VanVleet `out-for-season`, Kyrie
  mid-season ACL recovery), the 2025 rookie class (Flagg, Edgecombe, Harper,
  Bailey, ...) and **no 2026 rookies**. Stat lines are entering-season
  projections (2024-25 production, hindsight breakouts dampened — see
  STAT_ADJ in the snapshot generator history).
- **Writes** only under `arena/results/` (gitignored except curated reports).

## Run it

```bash
python3 arena/arena.py draft --seed 1               # one draft, rosters shown
python3 arena/arena.py live --slot 4                # YOU vs 11 AI managers
python3 arena/arena.py tournament                    # 12-slot rotation + seasons
python3 arena/arena.py tournament --seasons 500 --generations 3
```

**Live practice mode** (`live`): eleven arena personalities take the other
seats and log their picks into the PRODUCTION draft state, pausing whenever
it's your turn — so the normal `draft turn` confidence cards, flags, and
rules fire exactly as they will on real draft night. Log your pick, re-run
`live`, repeat. Post-draft, all production analysis (matrix/status/vs)
works, and the arena's season simulator can grade the finished league.

A full tournament (12 drafts × 200 seasons × 12 strategies) takes ~2 seconds.

## How scoring works

Drafts are scored by **championships, not draft value**: each drafted league
plays 18 weekly H2H category matchups (rosters become per-category weekly
mean/variance models; injury notes reduce expected availability — recovery
0.60, risk 0.75, healthy 0.88), top-6 make the playoffs (1-2 byes), and the
bracket winner takes the title. Championship% aggregates over every draft
slot, so no strategy benefits from slot luck.

## The twelve personalities

`council` (the production ruleset: contested-category weighting, recovery
compounding, stack penalty), `bpa_pure`, `punt_ft`, `punt_ast`, `punt_ft_to`,
`stars`, `slot_filler`, `scarcity`, `safe_floor`, `upside`, `specialist`,
`market` (value + noise, plays the role of a typical league-mate).

`--generations N` runs a baseline numeric hill-climb (bottom-3 adopt jittered
top-3 parameters). The intended evolution loop is the **Fable 5 strategy
lab** (Cowork phase 2): read results → author/mutate strategies with
reasoning → re-run → codify what wins back into the production engine and
skill, with a council audit gating any rule change.

## Verification (2026-07-12)

Three adversarial agents audited the arena before baseline: a fact-checker
(web-verified the snapshot against Oct 2025 reality — caught a retired
Brogdon, a fabricated Bamba row, missing rookie tags and opening-night
injuries, all fixed), a math reviewer (caught a 100x variance bug on
percentage categories, a no-lineup-cap depth bias, uniform category CVs,
uncorrelated game-count shocks — all fixed: STARTERS cap + bench weight,
per-category CVs, availability-tier game variance, shared weekly shock),
and a statistician (established that champ% gaps under ~2 points need ~10
seeds x 200 seasons; generations now evaluate on a FIXED seed set).

## Baseline result (post-fix; 21,600 seasons/strategy, seeds 1/98/195)

`safe_floor` **14.9%** (±0.9) championships — ~5 points clear of the field
(punt_ft 10.2, stars 10.1, bpa_pure 9.9, ... council 8.4 ±1.7, upside 2.8).
The robust finding: **availability dominates this simulated environment** —
never drafting injury-flagged players beats every clever weighting tested.
Phase 2's first questions: are the production engine's injury discounts too
shallow, and is the sim's availability model itself calibrated right
(grade it against how 2025-26 actually unfolded)?
