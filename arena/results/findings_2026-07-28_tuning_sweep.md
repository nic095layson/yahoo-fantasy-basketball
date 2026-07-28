# Findings — factorial tuning sweep + codification (2026-07-28)

Executes the codification package proposed in
`findings_2026-07-28_matrix_weights.md`: re-base the arena to the real
13-round league, sweep the weight response curve, confirm causally with
common random numbers, then codify if confirmed. Owner directive
2026-07-28: "Proceed with implementing Buckets 1 and 2."

## 1. Arena re-baseline (13 rounds)

`arena.py` ROUNDS 15 → 13 (the league's actual roster depth, codified
2026-07-12). Stock tournament re-run (seed 11, 3 seeds × 3 rotations ×
200 seasons): council 7.53% ±1.75 champ under the old weights — the
"old system" anchor. Baseline preserved at
`results/tournament_seed11_baseline_oldweights.json`.

## 2. Factorial sweep — weights × TARGET obedience

`tuning_sweep.py`, fixed 11-personality field + TEST seat, 5 seeds ×
2 rotation-rounds × 12 slots × 1000 seasons = 120k championship samples
per cell:

| cell (weights / obey-TARGET) | champ % | playoff % |
|---|---|---|
| cur (0.35/0.45) / no — production | 8.37 | 50.5 |
| cur / obey | 7.78 | 51.2 |
| mid (0.70/0.70) / no | 9.27 | 49.8 |
| mid / obey | 9.77 | 55.5 |
| neutral (1.00/1.00) / no | 11.61 | 64.1 |
| **neutral / obey** | **11.71** | **67.3** |

The weight response is **monotone**: every step from the production
swing down-weighting toward neutral helps. Obeying the urgent TARGET
(the deck's pinned-row policy, with the fs-floor urgency decay) is
championship-neutral at neutral weights (+0.10pp, inside noise; 2/5
seeds better) and **+3.2pp playoff**. At production weights it *hurt*
(−0.59pp) — the old weights were mispricing exactly the scarce-family
candidates the TARGET points at.

## 3. CRN paired confirmation (13 rounds)

`matrix_paired.py` re-run at the 13-round base: 120 paired drafts,
identical lottery + identical season noise per key.

- matrix ON (0.35/0.45): **8.59%** champ, 50.7% playoff
- matrix OFF (≡ neutral): **12.37%** champ, 65.2% playoff
- causal delta **+3.78pp** champ, t = **5.16**; 79 drafts better off,
  40 better on

Stronger than the 15-round finding (+2.73pp, t=4.17). Two arena depths,
two harnesses, one conclusion.

## 4. Codification (applied)

- `arena.py` `STRATEGIES["council"]`: `locked_w=1.0, lost_w=1.0`.
  **Council seat only** — DEFAULT and every field personality keep
  0.35/0.45 so all historical baselines stay comparable.
- Deck `STRATEGIES.council` (docs/draft-deck.html): same constants,
  same rationale comment. The **Fit column stays swing-weighted** as a
  reading lens (fitWeights hardcodes 0.35/0.45 independently); column
  header + legend now state the lens/ranking split explicitly.

## 5. UI patches verified headless (both mocks replayed)

- **Urgency decay**: slot-8's TARGET rang "URGENT C" at r3,6,7,11,12,13
  pre-patch. Post-patch: r3/6/7 only (best C fit +2.72/+0.91/+0.54);
  r11–13 stay silent (best fits −0.92/−1.41/−1.74 — dead shelf, tip now
  says "do not chase").
- **Pinned TARGET row**: slot-8 r6 pins Brook Lopez (fs 0.91 under old
  weights, gap 1.26) exactly as pre-registered from the post-mortem.
- **Structural fix**: under the neutral council, slot-8 r6's Top 5 now
  contains Brook Lopez at #2 (fs 2.05, coin-flip with #1 LaVine) and
  Kel'el Ware at #4 — the original "TARGET says C, no C in the list"
  contradiction resolves inside the list itself; the pinned row remains
  as the safety net for turns where the family still misses (r7: Naz
  Reid pinned).

## 6. New-council tournament

Same stock tournament (seed 11, 3 seeds × 3 rotations × 200 seasons)
re-run with the neutralized council:

| seat | old champ % | new champ % |
|---|---|---|
| council | **7.53 ±1.75 (8th/13)** | **11.56 ±3.92 (4th/13)** |
| punt_ft | 14.48 | 13.97 |
| safe_floor | 14.43 | 13.94 |
| stars | 11.24 | 12.13 |
| bpa_pure | 10.94 | 11.12 |
| slot_filler | 12.43 | 10.63 |

Council +4.03pp, and it now edges bpa_pure — the "naive BPA beats the
production ruleset" anomaly from the activation-gate study is closed.
Honest caveat: the new council's cross-seed spread is wider (±3.92 vs
±1.75); the paired CRN test in §3, which removes that noise, is the
load-bearing evidence. Field seats' shifts are same-simulation noise
(their code is unchanged).

## Verdict

Codified. The swing down-weighting (locked ×0.35 / lost ×0.45) is
retired from council *ranking* in both the arena and the deck; it
survives only as the Fit display lens. Evidence: monotone 6-cell sweep,
+3.78pp CRN-paired causal delta (t=5.16) at the production arena depth,
corroborated at 15 rounds independently.

Evidence bundle (committed): `results/evidence_2026-07-28_tuning/` —
the 6 sweep cells, the 13-round paired confirmation, and both
post-patch mock replays.
