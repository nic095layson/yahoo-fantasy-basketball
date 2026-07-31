# System integrity audit — 2026-07-31 (owner-requested, post-UI-overhaul)

Nine-agent workflow (4 audit arms → 4 adversarial refuters → completeness
critic), then council (5–0), then ratified fixes. Every arm's load-bearing
claims were independently re-executed by a refuter that rebuilt fixtures
and harnesses from scratch — nothing below rests on a single measurement.

## 1. Competitive math — 9/9 PASS, zero drift under the freeze

| Check | Result |
|---|---|
| JS↔Python value parity | EXACT, 241/241 rows |
| P3 replacement-anchored z | top-156 fixed point holds: per-cat mean z < 5e-7; FG%/FT% volume-weighted impact sums ~1e-13; TO inverted (cov(tov, z) < 0) |
| adj_value / availability | ×0.78 only when tv>0 (AD exact); out-*/recovery rows availability 0; negatives never boosted |
| survivalP | matches exact-erf Φ to 7e-8 over a 2,436-point grid |
| fitWeights tiers | locked=2 / lostFrom=10 at 12 teams; ×0.35/×0.45/×0 confirmed by execution; activation at roster ≥ 2 |
| Gradient layer | GRAD_DEFL/K/SLOTS machine-identical arena↔deck; formulas token-equivalent |
| Concession diagnostic | 0.0905 / 2.148 / ELAST table match the codified study |
| Arena instrument | PCT_MIX_INFL binomial %-variance, category-record seeding, playoff ≥5, sign-aware market multipliers — all as codified |
| Determinism | seed-42 tournament twice → bit-identical (council seat 3rd/13, INFO) |

## 2. Opponent-awareness — CONFIRMED (the owner's question)

`buildRosters` constructs ALL 12 rosters from the pick log every render.
Opponent data flows into: the per-cat rank strip and Matrix; the
Strengths/Winnable/Weaknesses panel + 🔒 locks (rank vs the whole field);
the Fit lens/column (locked ≤2 ×0.35, lost ≥10 ×0.45, swing full — "lock
the lead" = flag + reallocate marginal priority); Soft Punt (standardized
against per-opponent z-sums); the top-rival line + Build-read Swing/
Surplus; and the head-to-head Vs tab. A two-world causal experiment
(identical owner roster, guard-heavy vs big-heavy opponent rooms) changed
the panel, locks, Fit values, Soft punt, and rival line — refuter-
reproduced. One precise qualification, by validated design: the Top-5
composite ORDERING itself is opponent-rank-NEUTRAL (locked_w=lost_w=1.0)
— neutral weights measured +5.6pp over rank-conditional ordering; the
rank-conditional signals live in the surfaces above, not the sort.

## 3. Render gauntlet — 65 states, 8 invariants, 0 violations

All owner-turn states of mocks 16–20, shipped app block, independent
in-harness recomputation of every invariant (single-🎯, no CAN WAIT,
verdict placement/regex, scarcity shelf window, canonical panel order +
set-equality vs independent categoryRanks, soft-punt gating, feed-title
snake math, two-directional 🔒 correctness). Mutation-tested (tampered
tiers/windows/sets all fire). Chip census: 153 BUY NOW (19 shelf), 22
TOSS-UP, 150 quiet.

## 4. Defects found (completeness critic) — fixed, council 5–0

All three in the punt-active modality no mock had exercised:

- **C4 Soft Punt was punt-unaware** — could spend an advisory slot on an
  already-punted cat. Fixed: candidates + coverage now run over KEPT cats
  only; byte-identical with no punt (verified: 65-state chip/panel census
  unchanged pre/post).
- **C3 panel degeneracy under a 3-cat punt** — Winnable overlapped the
  weakness trio in the 6-kept-cat pool. Fixed: Winnable is now disjoint
  from both trios (renders "—" when nothing qualifies).
- **C8 Identity line hardcoded 12-team thresholds** (≤4 up / ≥9 down).
  Fixed: derived from the same thirds math renderMatrix uses — identical
  at 12 teams, correct elsewhere.

New standing fixtures added to the smoke suite: punt-active (3-cat),
UNKNOWN-pick, and 14-team states — all pass on the fixed deck.

## 5. Dead weight — removed vs kept

**Removed (true-dead, zero behavior change, refuter-verified):**
JUDGMENT.starTier (~1.3KB; its reader retired with the Value/Market
strips), valueBoard.stripRank/stripSlide, 2 orphan CSS rules, 3 orphan
HTML ids, 4 doc-rot comments (claimed consumers that no longer exist).

**Kept deliberately (owner instruction + REVERT-MAP, September
checkpoint):** the ar/fx/sy archetype bake (7.8KB, currently unconsumed
by the live app) and gradImpact (unused display fn; ordering variant
lives in the engine). REVERT-MAP corrected: cheapestConcessions is
load-bearing again (Soft Punt consumes it).

## Council verdict

5–0 for the amended package: punt-aware recompute over suppression
(Contrarian's amendment), fix-now on the punt defects (PUNT BUILD makes
the path reachable live), keep the archetype bake per the owner's fresh
"keep internal" instruction. Freeze intact: no engine math changed —
parity EXACT and the arena instrument untouched throughout.

## Addendum — session-interruption post-mortem (2026-07-31, owner-requested)

The session hit a Fable usage limit overnight and ran on Opus for four PR
check-in turns before returning to Fable. Continuity verdict: **nothing
was lost or left half-finished.**

- **Timing was fortunate:** the audit turn (workflow → council → fixes →
  gates → commit `33f2ef7` → push → artifact republish) had fully
  completed BEFORE the model switch. The switch landed mid-way through
  a routine PR check-in, which completed normally under Opus.
- **Work done under Opus (verified present):** the PR #3 body update —
  sections 12–14 (archetype/compass arc, card simplification, this
  audit) added to a description that had gone 20 commits stale — plus
  three silent no-change check-ins, each correctly re-armed.
- **Fresh re-verification under Fable (this addendum):** working tree
  clean; local == remote == `33f2ef7`; all audit deliverables present
  (punt-aware concessions, Winnable de-overlap, tier-derived Identity
  thresholds, dead-weight removals, REVERT-MAP correction); gates re-run
  green — parity EXACT, syntax clean, both standing smokes, all three
  audit fixtures (punt/UNKNOWN/14-team), 65-state gauntlet 0 violations;
  published artifact serves the four script blocks byte-identical to the
  repo with `built: 2026-07-31`; exactly one active check-in trigger (no
  duplicates from the interrupted turn).
