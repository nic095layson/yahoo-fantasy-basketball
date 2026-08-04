# Mock 16 post-mortem — slot 3, first live draft with gradient ordering active (2026-07-30)

Completed 13-round mock (156/156). The acceptance test of the
slot-gated gradient: slot 3 means the ⚡ ordering ranked every Top-5
card the owner saw. Replay harness runs gradient-faithful
(`strategyScores(..., gradK=1.0)`); seasons 6,000 × 3 seeds.

## Outcome — best of the honest-instrument era

| Metric | Mock 16 (slot 3) | m13 (s6) | m14 (s11) | m15 (s7) |
|---|---|---|---|---|
| Champ% | **15.37 (2nd/12, rank 2 all seeds)** | 13.39 (co-2nd) | 5.76 (6th) | 2.06 (8th) |
| Playoff% | 73.1 | 77.7 | 53.5 | 30.9 |
| Kept-total | **+4.79 (1st — best board in the room)** | 10th | 10th | 10th |
| Mean pick delta | −2.6 (9/13 at discount) | | | |

Roster: SGA, Tatum, Kessler, Brunson, Eason, LeBron, Duren, Quickley,
Naz Reid, Grant, McCollum, Jrue, Dosunmu. Room won by `market`@slot 1
(18.17%) — the fourth straight slot-1/Wemby room win; owner 2nd,
`stars` 3rd.

## The gradient's fingerprints

- **#27 Walker Kessler**: the composite ranked him **#18**; the
  gradient card ranked him **#4** (Okongwu #1). The owner's early-C
  BLK/FG% anchor was a gradient-enabled pick the old deck would have
  buried off-card.
- R1–R2 (SGA, Tatum) and R5 (Eason at card #2): card-aligned; the R4
  Brunson (card #5) and R6–R7 LeBron/Duren (gradient-list #12/#6)
  were owner shape/price calls. Adherence 8/13 on-card, 5/13 #1.
- Board discipline returned: −2.6 mean delta, worst reach Kessler +17
  (which the CF-free sim outcome retroactively endorses).

**Ledger nuance (new):** this build has no top-4 category (best ranks:
AST 5, PTS 5, FG% 6) — yet finished 2nd, because the board was the
room's best and category-record standings reward breadth of small
edges. Refined rule: *flat shape + dominant board can win; flat shape
+ mediocre board loses (m12/m15); committed shape + good board wins
biggest (m13, stars here and in m15).* `punt = []` for the eighth
straight mock; the ⚖ commitment meter (best rank 5 → would fire past
R4) ships from this build forward.

## Chip scorecard — best room ever

- **CAN WAIT: 12/16 survived (75%) — best measured**, first clearly
  survivable room since m14. Busts: Braun, Poeltl, Edey, Ellis — all
  value-persona kills (all-time **124/125**).
- **BUY NOW: 24/28 (86%)**; two "misses" were owner-banked next turn.
- **Scarcity invariant: clean** — 27 chips, 156 states, 0 violations.
- Ladder note: R3's `#70 Walker Kessler ~98%` step became moot when
  the owner took him at #27 — the gradient and the ladder now
  occasionally argue about *when*; filed as a display-harmony nit.

## Verdict on the codification

One live draft is one draw, not a t-statistic — but the acceptance
test agrees with the arena: gradient-active slot-3 seat → best board,
best champ%, rank 2 in every seed, and the signature pick (Kessler)
was surfaced by the new ordering. The arena's +12.67pp (t=4.63)
remains the load-bearing evidence; this mock is consistent with it.
