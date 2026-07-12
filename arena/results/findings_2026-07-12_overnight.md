# Arena findings — overnight run, 2026-07-12

> **v2 (continuation run, same night).** Two claims from v1 were tested
> further and corrected: (1) safe_stars' edge over safe_floor did NOT
> replicate on fresh seeds — verdict downgraded in §3; (2) safety's
> frequency-dependence was overstated — corrected in §4. New: §7
> (replication + parameter sweep), §8 (real-world calibration — the sim
> if anything UNDERSTATES the injury penalty). Corrections left visible
> rather than silently rewritten.

Full strategy-lab cycle: slot/cadence intel, baseline diagnosis, one authored
hypothesis generation with 10-seed confirmation, the 3-generation evolution
loop David requested, and a bug audit. All runs on the frozen 2025-10-21
snapshot, fixed seed sets. Production (`scripts/hoops.py`, `data/`,
fantasy-basketball skill) untouched — codification proposals at the bottom
await owner review.

## 1. Baseline (reproduced exactly)

21,600 seasons/strategy, seeds 1/98/195, 3 rotations: safe_floor 14.89%
(±0.86), then punt_ft 10.15, stars 10.13, bpa_pure 9.93 ... council 8.36
(±1.67, 8th) ... upside 2.79. Matches the documented post-audit baseline
digit for digit — the environment is deterministic on fixed seeds.

## 2. Why availability dominates (computed mechanism)

Pool: 214 draftable players, 22 injury-flagged (20 `*-risk`, 2 `*-recovery`).
Flagged players drafted per roster: safe_floor 0.00, typical strategies
1.2–2.2, upside 5.47.

The mechanism is **fair-priced mean, unpriced variance**. The draft engine's
availability discounts (×0.85 risk, ×0.7 recovery) almost exactly equal the
sim's production haircuts (0.75/0.88 = 0.85; 0.60/0.88 = 0.68) — so flagged
players cost what they produce *on average*. But weekly game-count variance
Var[G] = 3.5·a·(1−a) is 0.66 for risk players vs 0.37 healthy (1.8×), and
nothing in any strategy's price accounts for it. safe_floor pays a small mean
premium to shed variance; in weekly H2H category coin-flips, variance is pure
downside for a team that is ahead. Championship% compounds that edge through
18 weeks plus a 3-round bracket.

## 3. Generation 1 — three authored hypotheses (10-seed confirmation)

Variants replaced the three worst optimized seats (upside, punt_ast,
specialist); realism anchors (market, bpa_pure, slot_filler) kept per arena
rules. 200 seasons × 3 rotations × 10 seeds = 72,000 seasons/strategy.
Because titles are zero-sum within a tournament, paired per-seed differences
are the correct test:

| Variant | Champ% | vs safe_floor (13.33%) | Verdict |
|---|---|---|---|
| safe_stars (value_exp 1.35 + never draft flagged) | **14.30** | +0.96, t=3.06, 8/10 seeds positive | ~~Supported~~ **CORRECTED in §7: did not replicate** |
| safe_punt_ft (punt FT% + safety) | 10.83 | −2.50 | Refuted — punting does not stack with safety (replicated §7) |
| council_safe (full council ruleset + safety) | 10.74 | −2.60, t=−5.92 | **Refuted decisively** (replicated §7) |

The council_safe result is the sharpest finding: even after adopting
safety, the council ruleset's remaining machinery (contested-category
weighting, stack penalty, need weighting) *subtracts* ~2.6 championship
points versus doing nothing but drafting healthy best-available. In this
environment the production ruleset's cleverness is net-negative, not merely
insufficient.

## 4. Evolution loop (3 generations, David's overnight request)

Interpreted "run the Arena simulation for 3 seasons" as 3 *generations* of
the evolution loop (a 3-season Monte Carlo would be pure noise); each
generation evaluated at 21,600 seasons/strategy on fixed seeds 1/98/195.
History: `evolution_3gen_2026-07-12.json`.

- Gen 0 → 1: bottom-3 adopted jittered top-3 params. The safe_floor clone
  (specialist seat) immediately jumped to 13.08% — 2nd.
- Gen 1 → 2: safety spread to 3 of 12 seats. Gen 2's board compressed hard:
  punt_ft_to 11.78 on top, safe_floor down to 10.74, top six within 1.6 pts.
- ~~Key dynamic: safety is frequency-dependent~~ **CORRECTED by a direct
  experiment (continuation run)**: fields with 1 / 3 / 6 safe seats give
  safe_floor 14.89 / 14.36 / 13.41% and a safe-cohort edge over non-safe
  strategies of +7.2 / +7.5 / +8.0 pts — the edge barely dilutes even with
  half the league drafting safe. The gen-2 board compression was mutation
  noise (jittered secondary params), not frequency dependence. Safety's
  edge is robust to field composition in this sim.

## 5. Bug audit ("bugs or churn")

- **Fixed (arena/arena.py, live mode)**: personality assignment used
  `names[(s-1) % 11]`, which gave seats 1 and 12 the same personality and
  silently benched one of the eleven whenever the user's slot was 2–11.
  Now one distinct personality per bot seat. Verified at slots 4 and 7
  (11/11 distinct both runs); tournament path untouched — baseline still
  reproduces exactly after the edit. (Upstream equivalent: `e871a3a`.)
- **Churn noted, not fixed** (cosmetic): `cmd_cadence` contains a dead
  `... if False else len_between(s, k)` expression and a `"pos_dr" "ain"`
  string-concat typo — both harmless.
- **Sim design notes** (not bugs): the weekly team shock scales category
  means but not sigmas; negative-value players skip the availability
  discount (`s * av if s > 0`). Neither affects the findings' direction.

## 6. Codification proposals — GATED, awaiting owner

1. **Production injury discounts are mean-correct but variance-blind.**
   Proposal: deepen effective discounts for H2H play (e.g. risk ×0.85 →
   ×0.75–0.80, recovery ×0.7 → ×0.55–0.60) *or* add an explicit "healthy
   alternative within X% of value → prefer healthy" tiebreak to the
   fantasy-basketball skill. Now carries real-world support from §8.
2. **Re-examine council's need_w / stack_pen / contested weighting** — the
   arena says they cost championships in-sim. Candidate only: the sim lacks
   waivers, trades, and schedule texture, which is exactly where contested-
   category awareness should pay. Do not weaken the production ruleset on
   this evidence alone.
3. **Calibration prerequisite** — executed in §8.

## 7. Continuation run — replication and sweep (v2)

The safe_stars result was stress-tested two ways and failed both:

- **Parameter sweep** (value_exp 1.2 / 1.5 / 1.7, all +safe, 10 seeds,
  paired): +0.15 / −0.13 / +0.23 vs safe_floor — all t < 1.5, flat. No
  neighboring exponent shows the effect.
- **Exact replication** (identical gen-1 field, 10 FRESH seeds 971–1844):
  safe_stars +0.18 vs safe_floor (t=0.4, 5/10 seeds positive). The original
  +0.96 was seed-set luck amplified by testing three hypotheses at once.

Verdict: **no reliable improvement over plain safe_floor has been found.**
Meanwhile both negative findings replicated hard on fresh seeds:
council_safe −2.87 (t=−6.7, 0/10 seeds positive), safe_punt_ft −3.20
(t=−5.7). The refutations are the durable science; the "improvement" was
noise. Methodological lesson for future lab work: any positive variant
result must survive a fresh-seed replication before entering a report's
headline — refutations replicated, enhancement didn't.

## 8. Calibration vs real 2025-26 (proposal 3 executed — v2)

Web-verified final 2025-26 games played (StatMuse/NBA.com, fetched
2026-07-12) for all 22 flagged snapshot players + 7 healthy-star controls:

| Group | Sim assumes | Reality (2025-26) |
|---|---|---|
| Healthy stars (n=7) | 88% of games | 73.5% (60.3/82; 78% excl. Giannis outlier) |
| Risk-flagged (n=20) | 75% | **50.7%** (41.6/82; range 6–72) |
| Recovery (n=2) | 60% | **8.5%** (Kyrie 0, Murray 14) |

Reality was substantially harsher than the sim on flagged players: realized
risk/healthy availability ratio ≈ 0.65–0.69 vs the sim's 0.85 (and the
production draft discount's 0.85); recovery ≈ 0.1 vs sim 0.68 (n=2 —
directional only). The spread within risk-flagged players (6–72 games) also
dwarfs the sim's variance model. Caveats: one season, one flag-assignment,
GP ≠ per-game value, small n. But the direction is unambiguous: **the sim
understates the injury penalty, so availability-dominance is conservative,
not an artifact — and production's ×0.85 risk discount is empirically too
shallow.** This strengthens codification proposal 1 and satisfies the
calibration prerequisite in proposal 3.

## Honest limits

Every number above is computed from the arena's simulated environment on the
frozen snapshot. The calibration in §8 (executed in the continuation run)
shows the sim's injury assumptions are directionally right and, if anything,
too generous — but it is one season of evidence with small groups. The
safe_stars edge did not survive replication (§7). The evolution loop's gen-2
board sits within noise bands (±1–2 pts at 3 seeds) and should not be quoted
as a ranking. Production remains untouched; proposals in §6 still await
owner review — proposal 1 now carries real-world support from §8.
