# Mock 12 post-mortem — slot 8 (2026-07-29)

Completed 13-round mock (156/156, all names resolve incl. new entries
Alvarado/Sexton/Collier). Same gauntlet-confirmed harness as mocks 10–11
(`scratchpad/mock12_replay.js`, `season_sim_mock12.py`); seasons 6,000 ×
3 seeds; counterfactuals 6,000 × 2 seeds, roster-level (room ripple
ignored).

## Outcome

| Metric | Mock 12 (slot 8) | Mock 11 (slot 6) | Mock 10 (slot 4) |
|---|---|---|---|
| Champ% | **4.64 (7th/12)** | 1.76 (10th) | 12.11 (3rd) |
| Playoff% | 48.4 | 25.5 | 67.1 |
| Kept-total | **+16.38 (10th board — worst yet)** | +22.83 (2nd) | +23.57 (2nd) |
| Owner mean pick delta | **+4.7 (first net-premium draft)** | −2.9 | −4.8 |
| Shape | flat: best cat ranks are three 5ths | 4-cat max | offense, D conceded |

Rank 7 in all seeds. Room won by **`punt_ft` at 33.62%** — the most
dominant room result of any mock — on a +21.85 board. `punt = []` for
the fourth straight time.

Roster: Haliburton, Mitchell, Sengun, Flagg, Jaylen Brown, Markkanen,
Naz Reid, Clingan, Knueppel, Boozer, Jrue, Melton, Dosunmu.

## The finding: this time the card was right

Adherence was the lowest yet — 7/13 on-card, 4/13 card-#1 — and unlike
mock 11, the overrides cost real equity:

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 4.88 | 7th |
| Follow the card at the 3 big off-card turns (Sengun→Wagner, Brown→Poeltl, Reid→Mikal) | **9.95** | **4th** |
| Sengun→Wagner alone | 6.52 | 6th |

All three card-#1s were still available at those turns. Mock 11's
off-card picks were shape-driven and load-bearing (removing Embiid →
12th); mock 12's were price-driven and costly (following the card →
4th). The pair is now a matched experiment: **override the card for
shape, never for price** — price disagreements are exactly what the
board already adjudicates.

**Sengun flag (data risk, not settled).** Taken at #32 against deck
board #73 (+41, the draft's 5th-biggest reach). This is a genuine
model disagreement — the July points-volume board discounts him the way
it discounts Holmgren/Mobley, and real September ADP will price him
~#30. In THIS room the sim says it cost ~1.6pp; in a real room the
model may be the wrong side. September consensus data arbitrates —
logged, not adjudicated.

## Chip scorecard — the bimodal split hardens

- **CAN WAIT: 1/19 survived (5%) — the worst room ever measured.** Every
  owner card was swept within a handful of picks, turn after turn; this
  room drafted in near-board-order. Eight mocks in, WAIT survival is
  cleanly bimodal: massacre rooms 5–8% (m6, m9, m12), survivable rooms
  26–67% (m5, m7, m8, m10, m11-partial). There is no middle.
- **BUY NOW: 31/31 justified (100%)** — perfect, first time.
- **Scarcity invariant: clean** (29 chips across 156 states, 0
  outside-window, 0 dead-shelf). The Markkanen scarcity BUY NOW at #65
  was correct: the entire F shelf behind him (Lopez, Ware, LaVine,
  White) was gone within 9 picks.
- **The market-seat streak is broken**: John Collins (CAN WAIT 67%,
  chip@113) was taken at #120 by the slot-1 `market` persona — the
  first market-seat snipe in eight mocks. All-time: 80/81 failed WAITs
  by value personas.

## Shape ledger, four graded drafts

| Draft | Board | Shape | Finish |
|---|---|---|---|
| slot-3 | 1st | balanced, one concession | 2nd |
| 10 | 2nd | skewed, undeclared | 3rd |
| 11 | 2nd | sharp 4-cat | 10th |
| 12 | 10th | flat, no cat above 5th | 7th |

Flat-mediocre beat sharp-narrow (7th vs 10th) even on a far worse
board — but neither touches a committed shape. The three rooms so far
were won by `punt_ft_to` (20.7%), `market` (20.1%), and `punt_ft`
(33.6%): two of three by declared punts. The lever remains unused.
