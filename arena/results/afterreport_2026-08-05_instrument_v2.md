# After-report — instrument v2 (daily-fill scoring) and the day's fix chain (2026-08-05)

**Owner directives executed:** "research how fantasy basketball scoring
works… that your system is calculating correctly" → "implement effective
and calculated fixes with this knowledge, provide after report and ELI5."
Method and verification stated up front; every number regenerates from a
fresh clone via the cited harnesses; EVIDENCE = measured/committed,
INFERENCE = marked.

## Verdict tiers

| Item | Verdict |
|---|---|
| Was the system scoring like Yahoo before today? | **NO on lineup dynamics** (fixed weekly lineup, bench at 0.15) — YES on everything else audited (9-cat set, TO inversion, weekly pooled FG%/FT%, volume-weighted percent impacts, playoff bracket, symmetric instrument) |
| Instrument v2 shipped? | **YES** — daily-fill start rates in both the season sim and the deck, bit-identical cross-language (72/72 hash vectors, 2808/2808 weight parity), old instrument preserved under `ARENA_WEEK_MODEL=static` |
| Ordering consequence acceptable? | **YES per the registered disclosure rule** — escalation required ≥2 record mocks >5pp worse; measured: exactly 1 (m25 −9.0), against +3.7/+3.8 gains on m21/m26 and a 5-of-9 punted-set win |
| Owner's "5–6 centers" complaint | **Fixed organically by v2** (m34 R13 card: 5/5 bigs → 3/5 with two guards) after two override designs failed their bars; LINEUP CAP truth warning retained as backstop |

## 1. What was measured wrong (EVIDENCE)

Real Yahoo H2H lineups are set daily; started slots (incl. Util = any
position) count 100%, bench counts 0, and bench players backfill open
slots on their game days (owner ground truth + Yahoo SLN22673/SLN6775/
SLN28136). The daily-fill MC (`arena/mocks/daily_lineup_mc.py`, committed
output) measured on two real rosters: **99.4% of all played games get a
starting slot; the bench trio starts ~97.5% of theirs; the static model's
0.15 bench weight was ~6.5× too low; weekly counting totals ran 8–23%
low** with the skew concentrated in bench specialists' categories. Full
audit: `findings_2026-08-05_scoring_model_audit.md`.

## 2. The fix (EVIDENCE)

`team_week_model` (arena) and `teamWeekModel` (deck) now weight every
player by his **daily-fill start rate**: K=32 deterministic
common-random-number weeks; games/week ~ P(2)=.08 P(3)=.55 P(4)=.35
P(5)=.02 on heavy/light-weighted days; availability per game; greedy
daily slot fill in season-value order; w = started/played. No bench
floor — unstarted games count 0, exactly the league's rule. Measured
weights on real rosters: 0.98–1.00 for everyone (worst case, a C-only
player behind five C-eligibles: 0.988). Verification: dfHash 72/72
cross-language test vectors; **2808/2808 exact-float weight parity**
across every seat of all 13 panel states, full and mid-draft.

## 3. Ordering consequence and disclosure (EVIDENCE)

The deck's ΔECW half consumes the same model, so the Top-5 changes where
daily fill disagrees with the static lineup: **22 of 169 panel turns,
all R8+** (`v2_replay_m*.json` vs `e22_replay_m*.json`). Disclosure per
E21 — three arms per mock under v2 grading, 18k CRN-paired seasons each
(`v2_panel_disclosure.py` → `v2_panel_disclosure_out.json`):

| Mock | Baseline | v1 cards | v2 cards | Δ(v2−v1) |
|---|---|---|---|---|
| 22 | 0.58 | 2.43 | **8.06** | +5.62 |
| 31 | 13.54 | 15.89 | **18.93** | +3.04 |
| 32 | 6.60 | 0.42 | **3.41** | +2.98 |
| 34 | 17.59 | 0.04 | 0.67 | +0.62 |
| 35 | 8.82 | **9.09** | 6.85 | −2.24 |
| 36 | 30.78 | **29.11** | 27.78 | −1.32 |
| 37 | 29.69 | 12.65 | **12.97** | +0.32 |
| 38 | 19.38 | **31.03** | 29.21 | −1.82 |
| 39 | 40.75 | **26.69** | 24.31 | −2.38 |
| 21 | 21.03 | 39.50 | **43.18** | +3.68 |
| 24 | 22.83 | **30.53** | 29.89 | −0.64 |
| 25 | 25.06 | **30.62** | 21.58 | **−9.04** |
| 26 | 23.12 | 27.97 | **31.72** | +3.76 |

- Punted set: v2 wins **5 of 9**, mean +0.54. Record set: +3.68 / −0.64 /
  **−9.04** / +3.76. The registered escalation rule (≥2 record mocks
  worse by >5pp) does **not** fire — one breach.
- m25's −9.04 traces to ONE knife-edge substitution (R8, pick 95: v2
  leads PJ Washington over Jaden McDaniels; net roster diff after the
  cascade is McDaniels vs Quickley). Same single-player tail-sensitivity
  family documented in the E22 findings (±24pp swings, seed-robust).
  INFERENCE: a per-mock delta of this size on one player is instrument
  tail noise around a real but small effect, which is exactly why the
  registered rule counts breaches instead of reacting to one.
- Note the baseline column: under corrected physics the owner's REAL
  drafts grade higher across the board (m39 33.98→40.75, m37
  19.04→29.69, m34 9.52→17.59). INFERENCE: the owner's
  depth-and-balance drafting style was being under-credited by the old
  instrument — consistent with his stated philosophy being right.

## 4. The day's full fix chain (context)

1. E22 (SLF re-ranking): measured, failed its bar — written negative.
2. E22b (guard-rail): measured, failed its bar — written negative.
3. LINEUP CAP truth warning: shipped (display-only backstop).
4. **Instrument v2: shipped** — the root-cause fix; the all-big card
   corrects itself under real scoring physics.
5. Scoring audit + this report: committed with all evidence.

## 5. Bounds and open items (owner decisions, registered)

- v2's schedule constants (game-count distribution, day weights) are
  research-anchored assumptions, not fitted values; September E22c
  calibrates them against the owner's real weekly breakdowns.
- Absolute champ% is not comparable across the instrument epoch;
  pre-v2 numbers regenerate under `ARENA_WEEK_MODEL=static` (LEDGER
  epoch note).
- Audit gaps registered but NOT fixed today: the injury haircut no-op
  (mean-anchored zero), availability-blind trade math, no per-week
  schedule data, no streaming/IL in the sim, arena AI seats still
  drafting with the old scorer.
- The E24 candidate question for September: whether the deck's ΔECW
  half should ALSO consume week-specific real NBA schedules once
  October data exists.
