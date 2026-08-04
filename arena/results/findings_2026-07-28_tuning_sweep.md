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

Three engine states, all replayed on both uploaded mocks and committed
to the evidence bundle:

- `replay_oldsystem_*.json` — old weights + pre-patch UI (the shipped
  7/27 system). Slot-8's TARGET rang "URGENT C" at r3,6,7,11,12,13 —
  including three dead-shelf rounds — and at r6 called a C that the Top
  5 never showed (Brook Lopez, fs 0.91 vs LaVine 2.18 per
  `debrief_2026-07-27_mock_postmortem.md`).
- `replay2_*.json` — neutral weights + first-iteration UI (fs-floor
  urgency decay, pinned row). Urgent collapsed to r3/6/7; Lopez entered
  the Top 5 itself at r6 (#2, fs 2.05, coin-flip with LaVine #1;
  Kel'el Ware #4) — the "TARGET says C, no C in the list" contradiction
  resolves inside the list; r7 pinned Naz Reid as the safety net.
- `replay3_*.json` — FINAL shipped engine after gauntlet hardening
  (§7): urgency additionally requires a positive-value candidate INSIDE
  the priced window (and names them in the tip), TARGET candidate
  ordering is neutral punt-aware (the retired 0.35/0.45 lens no longer
  picks any actionable candidate), and family coverage is
  eligibility-aware. Net effect on slot-8: urgent still exactly r3/6/7,
  and rounds 9–13 stop calling for a C entirely — Markkanen (PF,C)
  finally counts as C coverage, which the primary-position counter had
  missed all draft. Slot-3 flips from C to F exactly when Sarr completes
  the C floor at r10.

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
Honest caveats: (a) the new council's cross-seed spread is wider (±3.92
vs ±1.75); the paired CRN test in §3, which removes that noise, is the
load-bearing evidence; field seats' shifts are same-simulation noise.
(b) With 13 personalities in 12 seats the tournament's first
rotation-round is unshuffled, so slot coverage is not perfectly
balanced across strategies and the header's seasons/strategy figure
overstates the 12 short-seated seats — a bias shared identically by
the old and new runs (both committed to the evidence bundle), so the
old-vs-new delta is internally consistent even though absolute champ%
carries the composition artifact.

## 7. Gauntlet (14 agents, find → adversarial verify → critic)

Six adversarial dimensions over the changed system; data plane and deck
build came back clean; 7 findings survived independent refutation
attempts (zero refuted) and every one was fixed before push:

1. `cmd_slots` still crashed on the 13th personality (KeyError: 13) —
   the seated-prefix fix had only been applied to `tournament()`. Fixed
   the same way; smoke-tested.
2. The pinned TARGET's candidate and its "act now" gate were ranked by
   the retired 0.35/0.45 lens — an actionable path the evidence had
   just retired from ranking, and one the obey-cell harness never
   validated. Candidate ordering and the urgency floor are now neutral
   punt-aware.
3. "Act now" could point at a player priced far OUTSIDE the 2-round
   window whose scarcity triggered it (urgency about one shelf, button
   on another). Urgency now requires a positive-value candidate inside
   the window and names those candidates in the tip.
4. Family coverage counted only each player's first-listed position —
   a PF,C roster read "0C", falsely opening the scarcity gate. Coverage
   is now eligibility-aware (dual-eligible count both).
5. The new Fit legend overclaimed ("every category at full weight") —
   false under an active punt. Copy now says "every non-punted
   category".
6. The archived 6-cell sweep and the historical paired/gate harnesses
   were irreproducible from repo head after the codification changed
   the field's own council seat. All three harnesses now pin the
   pre-codification 0.35/0.45 field explicitly.
7. Findings §5's r6-Lopez numbers cited an artifact that was never
   committed (the old-weights replay had been overwritten by the
   neutral rerun). The bundle now carries all three engine states
   (`replay_oldsystem_*`, `replay2_*`, `replay3_*`) plus both
   tournament anchors, which the top-level `arena/results/*.json`
   gitignore had silently excluded.

Critic gaps also closed: the judgment layer was re-authored for 7/28
(Draymond's stale unsigned discount removed, JUDGMENT.date rolled), and
the tournament composition caveat was added to §6.

## Verdict

Codified. The swing down-weighting (locked ×0.35 / lost ×0.45) is
retired from council *ranking* in both the arena and the deck; it
survives only as the Fit display lens. Evidence: monotone 6-cell sweep,
+3.78pp CRN-paired causal delta (t=5.16) at the production arena depth,
corroborated at 15 rounds independently.

Evidence bundle (committed): `results/evidence_2026-07-28_tuning/` —
the 6 sweep cells, the 13-round paired confirmation, mock replays for
all three engine states (old system / first iteration / final), and
both tournament anchors (old weights and new council).
