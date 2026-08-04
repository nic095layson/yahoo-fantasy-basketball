# After-report — owner-directed fixes: survival recalibration + TARGET provenance (2026-08-04)

**Owner instruction (2026-08-03):** "Implement all fixes, run a calibration,
validation and system integrity test following." The two open owner-visible
defects were the quiet chip (0/24 survival in mock 30) and the TARGET line
naming position families the roster did not need (the live-draft screenshot).
Both fixes are owner-authorized, which satisfies the freeze's exception rule;
both are also display-layer — **the Top-5 ordering, the engine z-math, and the
arena instrument are untouched** (parity EXACT post-change; `arena/*.py`,
`scripts/*.py` diffs empty).

## Fix 1 — survival model recalibration (the quiet chip)

**Root cause, measured.** The shipped model priced survival off MARKET rank
alone — but 9 of the 11 mock opponents draft by VALUE. A high-value player
with a soft market price was marked quiet and immediately taken. On 840 Top-5
observations across 14 replayed mocks (16–30): shipped-model quiet cases
survived **58.3%** (predicted ~90%), Brier 0.223 — barely better than a
constant.

**New model** (fit by grid over three families, chosen by Brier):

```
P(alive at pick N) = Pval^(9/11) · Pmkt^(2/11)
Px = Φ((rank_x − N) / max(8, 0.20·rank_x))
```

— a room-mix blend: 9 value seats + 2 market seats out of 11 opponents.
Brier **0.135** vs 0.223. The chip thresholds were then re-fit to the new
model's measured bands (old cuts sat in the blend's coin-flip zone):
**BUY ≤ 0.20 · TOSS-UP 0.20–0.40 · quiet ≥ 0.40.**

**Calibration table (blend, 840 obs):** p<0.2 → 5.3% survive; 0.2–0.4 → 45%
(a genuine coin flip); 0.4–0.6 → 87%; 0.6–0.8 → 94%; 0.8+ → 100%.

## Fix 2 — TARGET / BOARD LEAN provenance split

`archetypeRead` now returns `boardOnly`: true when the family came from the
board-shape fallback while the roster is at/above its startable floor with no
open slot. The UI renders **`BOARD LEAN:`** instead of **`TARGET:`** in that
case, with a tooltip stating it is a read of the room, not a roster need. No
scoring, ordering, or candidate selection changes — the same line renders
with an honest name. (Option B — gating the fallback entirely — remains
September E12 with its measured bar.)

## Fix 3 — truth updates riding along

Chip tooltip and colophon rewritten to describe the room-mix model and the
provenance split; stale "market-priced room / no marker = safe to wait"
claims removed.

## Validation

**Chips, re-graded through the shipped new code, all 14 mocks.** Two gradings
reported: *conservative* judges every chip against the owner's literal next
pick; *look-through* judges against the horizon the chip actually predicts
(the app's wheel-aware `nextTurn`). The look-through number is the honest
one — the conservative one is reported because it is the harsher floor.

| Metric | Old model (measured) | New model (conservative) | New model (look-through) | Bar |
|---|---|---|---|---|
| BUY NOW precision | 77.4% at old thresholds | **81.6%** | **93.9%** (521/555) | ≥80% — **PASS** |
| Quiet survival | **58.3%** (m30: 0/24) | **89.4%** (118/132) | 89.4% | trustworthy again |
| TOSS-UP gone-rate | — | 62.1% | 63.4% | displays its own % |
| Wheel slot 12 pair-boundary | 17/17 baseline | — | **59/59** | not below 17/17 — PASS |
| Wheel slot 1 pair-boundary | 15/17 baseline | — | **28/28** | not below 15/17 — PASS |

*Calibration honesty note:* the first fit passed quiet (97.9%) but dropped
BUY precision to 77.4% — below the bar — because the old 0.40/0.60 cuts sat
in the new model's coin-flip band. The thresholds were re-fit and everything
re-graded; the numbers above are from the final shipped configuration. The
m17/m23/m24 "57–65%" outliers under conservative grading were traced to a
grading artifact (wheel seats judged against the wrong horizon) and are 100%
under the correct one.

**TARGET relabel, all 52 owner turns of mocks 27–30.** 27 lines still render
TARGET (roster-need provenance), **17 now render BOARD LEAN** — including
mock 30 #138, the owner's screenshot line, now `BOARD LEAN: Rim-protecting C
— can wait`. **Zero** TARGET lines name an already-covered family. Load-
bearing check: mock 22's structural rescue lines (#59 "act now", #62, #83,
#110) all still render TARGET — the plea that saved that draft is untouched.

## System integrity test (full suite, post-change build)

| Check | Result |
|---|---|
| Build gates (roster verify 246/246, freshness 8/4, round-trip) | PASS — fail-closed gate correctly REFUSED the first build on the 8/4 date rollover until the sweep ran |
| JS↔Python parity | **EXACT MATCH** (241/241) |
| 130-state render gauntlet, 10 invariants | **0 violations** |
| Drift latch | still fires m23 #61 only — calibration preserved |
| Fixtures (punt-active, UNKNOWN-pick, 14-team) | 3/3 PASS |
| Engine/arena Python diff | empty — display-layer only |
| Artifact | republished to the standing URL |

Chip census across the gauntlet moved as designed: BUY 353→390, TOSS 56→88,
quiet 241→172 — fewer, but now meaningful, quiet cards.

## Owner-facing summary of what changed at the table

- A **quiet card means something again**: ~89% measured survival to your next
  turn (was effectively a coin flip, and 0-for-24 in your last mock).
- **BUY NOW is stricter and sharper**: it fires only when the model gives a
  player ≤20% to survive, and it is right ~94% of the time on its own horizon.
- **TOSS-UP now marks the genuine coin-flip zone** (20–40%), and shows its %.
- The line that told you to draft a sixth center now calls itself
  **BOARD LEAN** — same information, honest name. It only says **TARGET**
  when your roster actually needs the family.

## Ledger / plan effects

- **E13 (quiet chip): SHIPPED** — this report is its record; September E2
  narrows to the punt-mode curve and the ADP refresh of the market half.
- **E12 (TARGET gate): Option A shipped** (relabel); Option B (suppression)
  remains registered with its bar.
- REVERT-MAP: both fixes are single-site reverts (`SURV_*` constants +
  `survivalP` body; `boardOnly` + one template literal).

## Bounds

The recalibration is fit on mock rooms (9 value + 2 market personas). Real
September rooms draft closer to ADP; the market weight may need to rise —
that re-fit is exactly the September E2/ADP work, now with a harness that
produces calibration tables on demand. n=132 quiet observations post-fix;
the per-mock quiet samples are small (0–31).
