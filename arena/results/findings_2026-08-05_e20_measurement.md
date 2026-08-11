# E20 measurement — the punt-aware ordering FAILS its bar (2026-08-05)

**Owner-authorized measure-only run** ("Run the E20 measurement now"),
executed under the freeze. Both Top-5 orderings followed at every owner
turn across ALL FIVE punted mocks, 18,000 CRN-paired seasons per arm
(seeds 11/23/47 × 6,000), depth-matched placebo per the mock-34
verifier's corrections. Regenerate: `python3 arena/mocks/e20_measurement.py`
→ `arena/results/e20_measurement_out.json` (per-mock partials committed
alongside). Replays committed: `m22/m31/m32/m34/m35_replay.json`.

## Result: a clean negative — the incumbent stands

| Mock | Punt | Baseline (as-drafted) | Shipped-follow | Punt-aware-follow | Placebo (depth-matched ×3) |
|---|---|---|---|---|---|
| 22 | REB/BLK/FG% | 0.22 | **6.14** | 0.00 | 1.23 |
| 31 | FT%/3PTM/TO | 6.16 | **15.87** | 3.11 | 1.03 |
| 32 | FT%/3PTM/ST | **4.11** | 0.01 | 0.00 | 0.65 |
| 34 | FT%/3PTM/PTS | **9.52** | 0.00 | 3.26 | 1.42 |
| 35 | FT%/AST/3PTM | 7.11 | **7.71** | 0.66 | 3.00 |
| **mean** | | 5.42 | **5.94** | 1.40 | 1.47 |

- **Punt-aware beats the shipped incumbent on 1 of 5** (m34 only — the
  draft whose exact ds-tie at turn 8 resolves alphabetically toward
  Giannis; the mock-34 verifier already showed that edge collapses to
  +0.5pp when the tie flips).
- **Punt-aware NEVER beats the as-drafted baseline (0 of 5)**, and its
  mean (1.40%) is indistinguishable from depth-matched random swaps
  (1.47%). Followed wholesale, punt-awareness rediscovers the concession
  spiral — precisely what `findings_2026-08-04_decw_round1.md` predicted
  the neutral value half was regularizing against, and consistent with
  G1a's −5 to −11pp for punt-declaring policies.
- The shipped card is high-variance as a full policy (beats baseline on
  3 of 5, including +9.7pp on m31; zeros on m32/m34) — full-follow arms
  measure the ordering as an autopilot, not as advice; the owner's actual
  drafts beat both cards on m32 and m34.

## Gates

- **Winners' regression gate: satisfied by verified identity.** With an
  empty punt set the punt-aware scorer IS the shipped scorer; verified
  byte-identical top-5s on m21/m24 replayed turns (the single non-compare
  was the documented turn-1 no-opponent fallback, shared by both).
- **Instrument stability:** m34's committed replay reproduces 26/26
  top-5 lists on the current deck (card redesign did not touch ordering).
- **Tie disclosure:** exact top-2 ds ties at m22 shipped turns 35/62/86,
  m31 punt-aware turns 57/81/129/153, m34 both arms (incl. the turn-8
  tie), m32 punt-aware 111. None besides m34's changes an arm winner.

## Registered consequence (executed per the E20 bar)

The bar reads: *"A punt-aware ordering ships only if it beats the
incumbent on the punted mocks… If it does not ship, the UI must stop
implying the punt box affects recommendations (display-only truth fix,
allowed under the freeze)."* It did not ship — so the truth fix is now
live: the declared-punt flag block carries the line **"The declared punt
shapes panels and warnings, NOT the Top-5 ordering"** with the measured
citation. Render verified on a punted mid-draft state via the fake-DOM
harness; the line is structurally gated to punted drafts only.

## Bounds

- Frozen-card limitation: after an arm diverges, later recommendations
  were computed against rosters the arm no longer holds (disclosed in
  every prior CF; unchanged here). n=5 punted drafts, 2 seats repeated.
- All numbers simulator-conditional (pre-E14 bracket, unfit weekly
  constants). The September re-baseline re-derives this table; direction
  (punt-aware ≈ random, incumbent stands) is the durable finding.
- E22 (saturation term) and E23 (punt-implication + dead-kept-cat
  warnings) are UNTOUCHED by this result — the dead-kept-cat pattern
  (m34 AST, m35 PTS) is real and still needs its warning; what failed is
  reordering the card, not informing the drafter.
