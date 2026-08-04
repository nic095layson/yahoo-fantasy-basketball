# Mock 11 post-mortem — slot 6 (2026-07-29)

Completed 13-round mock (156/156 picks, all names resolve incl. new pool
entries Dort/Queen/Wilson). Replayed through the shipped deck blocks with
the mock-10 gauntlet-confirmed harness (`scratchpad/mock11_replay.js`);
seasons via unmodified `arena.simulate_seasons` on the live pool, 6,000 ×
3 seeds, plus roster-level counterfactuals at 6,000 × 2 seeds. Run inline
(no workflow); the harness and method are unchanged from the
independently verified mock-10 workup.

## Outcome

| Metric | Mock 11 (slot 6) | Mock 10 (slot 4) | Prior slot-3 | Prior slot-8 |
|---|---|---|---|---|
| Champ% | **1.76 (10th/12)** | 12.11 (3rd) | 22.48 (2nd) | 0.23 (12th) |
| Playoff% | 25.5 | 67.1 | 89.7 | 10.8 |
| Kept-total | **+22.83 (2nd-best board)** | +23.57 (2nd) | +26.8 (1st) | +19.3 (10th) |
| Shape | 4-cat max: BLK 3rd, ST 4th, 3PTM 4th, PTS 5th vs AST 11th, FG% 9th, REB 9th | offense, D conceded | balanced | uncommitted triple-punt |

Rank 10 in every seed (1.95/1.52/1.82). Room won by **slot 1 `market`
(20.14%)** — first market-persona win, on a middling +19.50 board —
over `bpa_pure` (16.84). Roster: AD, Mitchell, JJJ, Flagg, Turner,
Embiid, Suggs, Powell, Vassell, Keegan Murray, Coulibaly, Jrue, Dosunmu.

**This is the sharpest value-vs-outcome split yet**: 2nd-best board,
10th-place equity. A four-category build wins four categories; five
losses are structural. `punt = []` again — the mock-10 actionable
(declare the punt by R4) was not followed.

## Counterfactuals (roster-level, room ripple ignored, 12k seasons each)

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 1.73 | 10th |
| R6 Embiid → card-#1 Coby White | **0.31** | **12th** |
| R8/R9 follow the C card (Powell→Hartenstein, Vassell→Gobert) | 2.41 | 10th |
| Both | 4.26 | 7th–8th |

Three readings, all uncomfortable:
1. **The off-card Embiid gamble (#67, composite #15) was load-bearing,
   not the leak** — deleting it alone collapses the 4-cat core to dead
   last. The build's entire equity lived in BLK/ST/3PTM/PTS.
2. **No single pick fixes this draft.** It was capped by construction in
   R1–R6: four big-family anchors (AD/JJJ/Turner/Embiid) with Mitchell
   as the only AST source. Every later choice was picking which hole to
   leave open.
3. The owner's two shape-instinct off-card picks (Powell #91, Vassell
   #102 over an all-center card) patched the *wrong* hole — they added
   3PTM/PTS the build already had. Following the "redundant" C card was
   worth more (+0.7pp); doing both (guard at 67 AND centers at 91/102)
   nearly triples equity and still only reaches half of par.

## Engine finding (candidate bucket — not actioned)

At #91 and #102 the Top-5 card was **100% C-family for a roster already
holding four bigs** (Vucevic/Hartenstein/Gobert/Reid/McDaniels, then
Hartenstein/Gobert/Edey/Gafford/PJW) while AST sat 11th. The value-board
slide bonus on discounted vets swamps family fit in the mid-rounds. CF2
shows the C card wasn't strictly wrong for this roster's equity — but it
was right for the value reason, not the fit reason, and it never offered
the AST shelf at all. Candidate: fit-aware damping of the slide bonus
when a family is at/over its startable floor. Needs an arena CRN-paired
test before touching the engine — filed here, deliberately not
implemented.

## Chip scorecard

- **CAN WAIT: 5/19 survived (26%)** — a new member of the massacre
  cluster (m6 6%, m9 8%) vs the survivable cluster (m5 67%, m7 59%, m8
  57%, m10 57%). Six mocks in: the split is bimodal and room-run driven,
  not gradual. The R9 all-center card died 5-for-5 in picks 103–107 — a
  positional value-cliff run, the exact pattern the standing banner
  warns about.
- **BUY NOW: 27/28 justified (96%)** — best yet (baseline 91%). The lone
  miss was Suggs@67, whom the owner himself banked at #78.
- **Scarcity invariant: clean.** 12 scarcity chips across all 156
  states, 0 outside-window, 0 dead-shelf.
- **Snipers: 14/14 failed WAITs by value personas, 0 by market seats —
  streak now 66/66 across seven mocks.** safe_floor alone took 5.

## Room value flow

Steals: Grant −16 (stars), Hartenstein −15 (slot_filler), Gobert −15
(scarcity), Edey −13 (upside), Gordon −13 (bpa_pure) — all the C-run
players the owner's card had listed as CAN WAIT. Reaches: RJ Barrett
+128 (punt_ft this time), Banchero +58, Zion +48, Cam Thomas +42,
Dybantsa +38. Owner: mean −2.9 (room +0.7), 9/13 at a discount, worst
Embiid +11 (the deliberate gamble). Adherence 9/13 on-card, 5/13 card-#1
(mock 10: 12/13, 7/13).

## The three-mock pattern

| Mock | Board value | Shape | Finish |
|---|---|---|---|
| slot-3 | 1st | balanced, one concession | 2nd |
| 10 (slot 4) | 2nd | undeclared triple concession | 3rd |
| 11 (slot 6) | 2nd | 4-cat max, five holes | 10th |

Value accumulation is a solved problem for this deck — three straight
top-2 boards. **Shape is now the entire gap between 2nd and 10th.** The
punt declaration isn't a UI nicety; it's the only lever that re-aims the
mid-draft engine, and it has gone unused in every mock since it shipped.
