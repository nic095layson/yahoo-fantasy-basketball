# E9 round 2 — blend50 PASSES the ship bar (2026-08-04)

Variant: per-turn percentile blend, `score = 0.5·pct(ΔECW) + 0.5·pct(adjValue)`,
no anchor gate needed (`arena/mocks/decw_card_v2.py`). The value half keeps
every category priced, which kills round 1's concession spiral at the source.

## Screen (14 mocks, 6,000 × seeds [11,23], vs as-drafted)

| Mock | Base | v1 raw | **blend50** | Δ |
|---|---|---|---|---|
| 16 | 15.44 | 30.12 | 20.48 | +5.04 |
| 17 | 1.64 | 0.19 | 11.82 | +10.18 |
| 18 | 4.33 | 30.19 | 30.73 | +26.40 |
| 19 | 10.72 | 26.90 | 16.04 | +5.32 |
| 20 | 6.51 | 13.80 | 20.61 | +14.10 |
| 21 * | 26.91 | 42.21 | 40.58 | +13.67 |
| 23 | 0.17 | 13.29 | 25.12 | +24.95 |
| 24 * | 29.82 | 42.15 | 31.34 | +1.52 |
| 25 * | 29.19 | 1.62 | 40.42 | +11.23 |
| 26 * | 22.57 | 3.12 | 29.18 | +6.61 |
| 27 | 9.76 | 19.41 | 24.10 | +14.34 |
| 28 | 6.50 | 10.51 | 18.33 | +11.83 |
| 29 | 8.90 | 0.41 | 12.67 | +3.77 |
| 30 | 2.12 | 12.32 | 15.93 | +13.81 |

**14/14 improved >1pp. Zero winner regressions. Mean +11.63, median +11.53.**
Where full composite-card-follow arms exist (m27–m30), blend50 beats the
composite card by +23.1 / +11.0 / +9.5 / +7.3pp.

## Robustness

- **Fresh seeds (101/202/303, 18k seasons), never used in tuning:** m21
  41.52, m24 32.37, m25 40.41, m26 28.64, m17 11.56, m29 13.03 — every
  screen result replicates within noise. Winner gate PASS.
- **α neighborhood:** α=0.4 identical on the winners but craters m29
  (1.02); α=0.6 regresses m25 (20.23). **α=0.5 is the only tested value
  clean everywhere.** This sensitivity is real and is the reason for the
  out-of-sample rule below.
- Placebo control from round 1 (same swap counts, random targets, mean
  0.82% vs card mean): the objective drives the gains, not perturbation.

## Ship decision

The pre-registered bar — beat the incumbent across the ledger replays with
zero regressions on m21/m24/m25/m26 — is **met**, under both seed sets.
Owner authorization (league_intel §9, Q15) covers shipping. Proceeding to
deck integration.

**Integration ships exactly what was tested:** Top-5 *ordering* becomes the
blend50 score at ALL seats — replacing both the composite `fs` ordering and
the slot-1–3 gradient gate (the tested card used neither, and beat drafts
that did, including all three gradient-seat winners). Judgment adjustments
and board-slide remain visible as card metadata; they no longer reorder.
Chips, TARGET, panel, ladder are untouched.

**Engineering requirements (all fail-closed):**
1. `build_deck.py` injects the raw per-game columns (counting stats, fga/
   fta/percentages) into PLAYERS — the weekly model consumes raw stats,
   which the deck data block does not currently carry.
2. JS port of the weekly model (means/variances, lineup weights,
   availability tiers, PCT_MIX_INFL) + pwins + percentile blend.
3. **New parity gate:** JS blend ordering vs Python `decw_card_v2.py`
   (α=0.5) must match EXACTLY on replayed ledger states before publish.
4. 130-state render gauntlet + fixtures + rebuild round-trip + republish.
5. REVERT-MAP entry: single kill switch back to composite ordering.

## Standing caveats (attached to this ship, not waivable)

- The 14-mock panel is the tuning set. **Out-of-sample rule: every future
  uploaded mock is graded against both cards (blend50 and legacy composite)
  in its debrief.** Two consecutive out-of-sample failures (blend50-follow
  worse than composite-follow beyond noise) trigger the kill switch and a
  written post-mortem.
- All arms simulate the shipped 6-team-bye playoff format; the September
  re-baseline (E14, real 8-team bracket) re-derives this table. Direction
  is expected to hold (the blend's gains come from category coverage, which
  the flatter bracket taxes less, not more) — but that is a prediction,
  not a measurement.
- ECW remains a readout of the arena's own weekly model (T2 in the
  self-critique); the three-season league data validated that model's
  variance to ~10%, which is the best external anchor available today.
