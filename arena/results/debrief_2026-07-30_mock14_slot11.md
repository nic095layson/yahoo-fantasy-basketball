# Mock 14 post-mortem — slot 11, first back-of-snake draft (2026-07-30)

Completed 13-round mock (156/156, all names resolve incl. Anthony
Black). Second mock on the codified deck, graded on the honest
instrument (`scratchpad/mock14_replay.js`, `season_sim_mock14.py`,
6,000 × 3 seeds; counterfactuals 6,000 × 2).

## Outcome

| Metric | Mock 14 (slot 11) | Mock 13 (slot 6) |
|---|---|---|
| Champ% | **5.76 (6th/12)** | 13.39 (co-2nd) |
| Playoff% | 53.5 | 77.7 |
| Kept-total | −1.20 (10th) | +0.04 (10th) |
| Shape | ST 1st, AST 3rd, PTS 4th vs BLK 10th, FG% 9th, TO/REB/3PTM 8th | premium won, cheap conceded |

Roster: Cade, Tatum, Booker, Flagg, Bam, Embiid, LeBron, Hart, Wiggins,
McCollum, Keon Ellis, Caruso, Harper. A PTS/AST/ST veteran perimeter
build that won one premium lever (AST 3rd) and conceded the other
(BLK 10th) — five cats rank 8th or worse. `punt = []`, sixth straight.

## The finding: the card's order was wrong, its shelf was right

The pivotal turn was R6 #62: owner took Embiid (composite #19, the
draft's worst owner delta at +16) over a card of Cam Johnson (#1),
Braun, **Jarrett Allen (CAN WAIT ~95%)**, Markkanen (scarcity BUY NOW),
Lopez. Counterfactuals:

| Line | Champ% | Finish |
|---|---|---|
| As drafted (Embiid) | 5.75 | 6th |
| Card #1 (Cam Johnson) | **0.34** | **12th** |
| Shape repair (Jarrett Allen) | **9.65** | **5th** |

Three-way split, one lesson deeper than mocks 12–13: following the
card's *order* is catastrophic (the flat composite crowned a wing the
build didn't need), and the star gamble is mid — but the **right shape
call was sitting on the same card**: Allen patches the conceded BLK
premium lever (2.73 pp/z) plus REB/FG%, and both the chip (CAN WAIT
95%) and the ladder (`#83 Jarrett Allen ~95%`) had him flagged. The
elasticity table read this turn correctly; the composite ranking
could not. This is the P6 slot-finding wearing a jersey: flat value
ordering cannot see shape, and the declared-punt lever (still unused)
is the mechanism that would re-aim it.

## Chip scorecard

- **CAN WAIT: 13/23 (57%) — a survivable room**, with a structural
  caveat now visible from the back of the snake: at the double-tap
  turns (2-pick gaps) waits are nearly free and BUY NOW calls are
  over-aggressive (Giddey/Murphy "BUY NOW" both survived the 2-pick
  gap at R3→R4). Survival math is correct per pick distance; the
  verdict *labels* could deserve a turn-aware threshold — filed as a
  display-layer candidate, no engine change.
- **BUY NOW: 16/20 (80%)**; all four misses benign (owner banked or
  short-gap survivals).
- **Scarcity invariant: clean** — 25 chips, 156 states, 0 violations.
- **Snipers: 10/10 value personas — all-time 104/105.**
- Owner used the double-taps well: Cade+Tatum (R1–R2) and LeBron+Hart
  (R7–R8) were both two-for-two card captures.

## Room notes

- **The `market` persona won its third straight room (33.34%)** — but
  the slot-3 market seat finished 0.77%, so this is substantially a
  slot-1 effect (Wembanyama anchor + balanced fill), not persona magic.
- **Value decoupled from outcome again**: `stars` held the room's best
  kept-total (+4.14) and finished 1.18%; the winner's kept-total was
  −0.14. Two mocks into the honest instrument, board-value accumulation
  has zero predictive record.
- Reach ledger: RJ Barrett +112 (punt_ft_to), Banchero +56; Embiid +16
  was the owner's worst. Owner mean delta −2.0 (room +0.5).

## Standing ledger (honest instrument only)

| Mock | Slot | Shape read | Finish |
|---|---|---|---|
| 13 | 6 | elasticity-aligned (BLK/REB/AST up, cheap cats down) | co-2nd |
| 14 | 11 | half-aligned (AST yes, BLK conceded) | 6th |

The elasticity table is now 2-for-2 as the outcome predictor. Next
lever, unchanged and now with three exhibits: **declare the punt by R4**
so TARGET re-aims the composite order toward the shape the table
already knows is winning.
