# Post report — instrument v2 full-system integration, calibration, and integrity (2026-08-06)

**Owner directive:** "Conduct a full system integration of this new,
effective formula. Conduct system calibration and integrity test
afterwards, and provide post report before pushing to cloud." This report
was written, and every test below run, BEFORE the push that carries it.
Regenerate: `arena/mocks/daily_lineup_mc.py`, `v2_panel_disclosure.py`,
`v2_calibration_out.json` (battery inputs listed per section).

## 1. Integration — where the formula now lives, and where it deliberately does not

Sweep of every consumer of the lineup/week model across the stack:

| Consumer | Layer | Decision |
|---|---|---|
| `arena.team_week_model` → `simulate_seasons` | season-sim grading | **v2 daily-fill** |
| deck `teamWeekModel` → `decwScores` (Top-5 ΔECW half) | live advice | **v2 daily-fill** (same function, one source of truth per side) |
| `decw_card_v2.py` (python ordering reference) | parity reference | **v2** (consumes `arena.team_week_model` directly) |
| deck `strategyScores` bench-discount (×0.15 when bench-bound) | mock-AI drafting behavior | **static, by design** — models how value-drafters avoid redundant picks; not scoring. E18b room calibration untouched (AI seats never consume `teamWeekModel`) |
| arena strategy scorer bench check | arena AI seats | static, same reason |
| deck `benchBound` chip + LINEUP CAP warning | display | static, by design — "at full strength, this pick can't crack the lineup" is a structural statement; retained as the saturation backstop |

**Epoch pinning (regeneration integrity):** the instrument flag is now read
at CALL time, and all 29 v1-epoch harnesses (season_sim_mock30–39,
e20/e22/e22b/seedcheck, the E9-era decw/gradgate/mock-cf set) hard-pin
`ARENA_WEEK_MODEL=static` so every number quoted in the ledger regenerates
exactly as published. `e22_measurement.py` pins only under `__main__` (it
is also the library the v2 disclosure imports); `v2_panel_disclosure.py`
hard-sets `daily`. No harness depends on import order.

## 2. Calibration (EVIDENCE — `v2_calibration_out.json`)

| Test | Result | Reading |
|---|---|---|
| K-precision (K=32 vs K=512, all 169 panel players) | max weight drift **0.034**, mean **0.002** | the K=32 approximation is far inside decision noise (percentile-blend granularity and the ~1–3pp placebo scale) |
| v2 weekly mu vs the independent 2,000-week team-shared-schedule MC | within **0.4–0.9% per category** (schedule-matched), both test rosters | the OLD model missed by 14–30%; v2 tracks an independently-built reference to under 1% |
| Symmetry (12 identical rosters, 3,000 seasons) | champ% 7.97–8.90 vs 8.33 expected | no seat bias under v2 — the instrument stays fair |
| ECW scale | m36 5.046 (v1: 5.06), m39 5.088 | ECW is relative, so the scale barely moves; the 4.90 winners' bar remains approximately comparable (formal re-derivation stays September work) |

## 3. Integrity gauntlet (EVIDENCE)

| Gate | Result |
|---|---|
| Deck syntax (assembled blocks, `node --check`) | PASS |
| Replay regression: m38 + m34 full 13-turn replays vs committed v2 cards | **byte-identical** |
| Cross-language parity (from the ship): dfHash 72/72 vectors; daily-fill weights 2808/2808 exact floats, all seats, all 13 states | PASS |
| Feature tests: per-pick input memory (14 assertions), slot memory (phases A+B) | PASS |
| **Epoch regeneration proof**: full 18k-season rerun of pinned `season_sim_mock38.py` vs its committed output | **byte-identical** (git-clean after rerun) |
| Panel disclosure (E21): v2 cards vs v1 cards under v2 grading | 5/9 punted wins, mean +0.54; record set +3.7/−0.6/−9.0/+3.8; registered escalation rule does not fire |

## 4. Verdict

**Integrated, calibrated, and integrity-clean.** The scoring physics is v2
everywhere scoring happens, static only where it models drafting behavior
or displays structural facts — each such exception named and reasoned
above. Calibration error against an independent daily-schedule reference
dropped from 14–30% to under 1% per category. Both instrument epochs
regenerate their published numbers exactly. No gate failed; nothing was
skipped.

## 5. Bounds and registered follow-ups (owner decisions)

- v2's schedule constants (game-count distribution, heavy/light day
  weights) are research-anchored assumptions — September E22c fits them to
  the owner's real weekly breakdowns.
- The winners' ECW bar (4.90) and all cumulative-tally doctrine remain
  v1-epoch numbers; formal re-derivation under v2 is September scope
  (LEDGER epoch note governs until then).
- Audit gaps still open (registered, untouched): mean-anchored injury
  haircut no-op, availability-blind trade math, per-week schedule data,
  streaming/IL in the sim, arena AI seats on the old scorer.
