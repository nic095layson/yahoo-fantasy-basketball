# Mock 19 post-mortem — slot 4, the doctrine's first clean mid-seat run (2026-07-30)

Completed 13-round mock (156/156, all names resolve). Slot 4 = NOT a
gradient seat (composite ordering). Replay ran the shipped app block
end-to-end (fake-DOM boots at all 13 owner states — zero
reimplementation drift); seasons 6,000 × 3 seeds; two counterfactuals
6,000 × 2. Same-day instrument (draftable-156 z, b328ef7 lineage) —
comparable to m13–m18. Note: the compass/🎯% reads quoted below were
captured from the deck as it stood at draft time; those display
surfaces were retired later the same day (owner simplification pass) —
the internal math they read is unchanged.

## Outcome

| Metric | Mock 19 (slot 4) | Ledger context |
|---|---|---|
| Champ% | **10.96 (4th/12)** | best non-gradient-seat finish on the fixed instrument (m14 11th · m15 7th · m17 9th · m18 6th) |
| Playoff% | 78.9 | |
| Kept-total | **+3.13 (2nd)** | room's best board discount aside |
| Compass | **followed** — COMMITTED GUARD from pick 3 (#28) to the end; deepen AST·3PTM·FT% → delivered FT% **1st** (z +8.1), AST 4th, PTS 4th | |
| Card | 6/13 exact #1; 7 overrides splitting exactly along the doctrine line (below) | |

Roster: SGA, Tatum, Lillard, Trae, Markkanen, LaVine, Duren, Gafford,
Vučević, Keyonte, Peterson, Jrue, Tobias. Conceded: ST 11th, BLK 9th,
TO 8th, REB 7th.

## Counterfactuals — third consecutive confirmation of the doctrine

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 10.72 | 4th |
| CF1 — remove the price/name overrides (Dame→card-#1 JJJ #28, Trae→Herro #45, Keyonte→Nesmith #117, Peterson→Lendeborg #124) | **12.93** | **2nd** |
| CF2 — remove the interior overrides (Duren→card-#1 Coby White #69, Gafford→Avdija #93) | **0.73** | **9th** |

- **Structural interior overrides were the spine (−10.0pp if removed).**
  Duren at #69 was the deck's own pinned TARGET ("Best C — shelf: 2 in
  window"); Gafford at #93 banked the second big while Vučević's CAN
  WAIT ~76% held, and the card's #1 Vučević still arrived at #100.
  Three bigs on a guard chassis: same family as m13 Sengun/Duren and
  m18 Clingan/Edey, now at the largest measured magnitude.
- **Price/name overrides cost again (+2.2pp recoverable, → 2nd).**
  Dame #28 (board 7, −0.81) over JJJ, Trae #45 (board 24, −1.01) over
  same-axis Herro, Keyonte #117 (board 35, −1.13) and rookie Peterson
  #124 (board 41, −2.01 — the draft's worst delta; the sim grades
  projections and cannot see rookie upside, but −3.1z across two tail
  picks is the measured price). Same family as m12 and m18's vets.

**Doctrine, unchanged and now 3-for-3 on CF pairs (m13/m18/m19):**
compass sets direction, card prices candidates, structural holes
justify overrides, price/name never does. m19 is the first mock where
the owner ran all three legs together from a mid seat — and it produced
the best mid-seat finish of the ledger with the #2 board at even money.

## Chip scorecard

- CAN WAIT **15/21 (71%)**; the misses cluster at the #52 turn (Eason/
  Poeltl/Turner swept in a 4-pick run) and the known probabilistic
  class (Nesmith ~61% → gone 2 picks later).
- BUY NOW **29/32 (91%) gone before the next turn** — sharpest urgency
  measurement yet.
- Scarcity invariant clean: 2 shelf chips (JJJ #21, Filipowski #117),
  0 violations.

## Room notes

`market` at slot 1 won **41.34% — the highest room result ever
measured** (beats m18's 38.06 stars): the Wemby seat plus market
pricing remains the room's dominant combination. `bpa_pure` 0.00%
dead last again. Owner's 10.96 from seat 4 against that is the
strongest relative showing at a non-gradient seat.

## Same-day system changes (context for the next mock)

This workup landed the same day as the owner's simplification passes:
archetype tags/census retired (d2e930d), then the 🧭 compass line, 🎯NN%
confidence spans, Value/Market strips, and composite title retired in
favor of a Strengths/Weaknesses header (🔒 = dominated cat) and a single
🎯 on the system pick — which goes to the pinned TARGET card when the
structural need is urgent, i.e. the deck now *marks* the exact override
class these CFs keep validating. Mock 20 will be the first draft on the
simplified card.
