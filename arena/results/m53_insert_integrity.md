# Insert-at-# integrity test — mock 53 (2026-09-22)

**Owner's questions.** (1) After Insert-at-#, does the deck keep saying "(you're on the clock)"? (2) Does the insert assign the shifted players to the right teams, and is the categorical computation still accurate?

**Inputs.** The owner's full tool log (169 events: 163 feeds incl. 2 halts, 2 UNKNOWN placeholders and their fixes, 3 undos, 3 Insert-at-# uses of which 1 refused as ambiguous) and Yahoo's round-by-round recap (156 picks, a clean snake, managers consistent per seat across all 13 rounds).

## 1. Placement and computation (engine-level, `insert_integrity.py`)

| check | result |
|---|---|
| tool echo lines reproduced by the engine, event by event | 169/169 |
| final board (156 picks with seats) equals the from-scratch board in Yahoo order | YES (first difference: none) |
| every roster equal | YES |
| category ranks (all 12 seats) equal | YES |
| category matrix (9 cats × 12 seats) equal | YES |
| ΔECW card ordering equal at all 13 owner turns (#10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154) | YES |
| `hoops.insert_pick` on the exact pre-insert boards reproduces the JS board | refused & equal, ok & equal, ok & equal |
| Python rosters equal the deck's | YES |

After both successful inserts the board returned to an exact prefix of the Yahoo order (the only non-prefix moments are the owner's own mid-course states: Turner typed at #86 before the Coby White insert, the UNKNOWN #125/#129 placeholders before their fixes, Herbert Jones before the undo, and the four picks logged before the Portis insert). So the insert placed Coby White at #86 (Anmol), moved your Myles Turner to #87 (you), and every later pick to the seat Yahoo shows; Portis at #142 (Tony) shifted Carter, Draymond, Braun and Vučević exactly one slot each.

**One precision note (not an insert defect).** The Python helper `my_category_ranks` and the deck disagree on one owner rank (3PTM: deck 2nd, Python 3rd) because seats 10 and 2 tie at 2.49269 in 3PTM to six decimals; the deck carries z-scores rounded to six decimals, Python carries full precision, and the tie breaks differently. The deck's own computation is self-consistent (built-by-insert vs from-scratch identical); totals agree to 1e-6.

## 2. The on-the-clock defect (real page, headless Chromium, `live_replay_dom.mjs`)

Replaying the same 169 events through the published page: page errors 0; the countdown under the feed title was wrong at 2 events — after picks #154 and #155 it read "(YOU'RE ON THE CLOCK)" while the strip beside it correctly read "Seat 11 on the clock" / "Seat 12 on the clock". Root cause: once your 13th pick is in, `myNextPick` returns null and the countdown treated null as "0 until your pick". It fires after the owner's LAST pick, whatever came before; in this room the second Insert-at-# episode ended at #154, which is why it looked like the insert broke the deck. The insert itself rendered the correct clock at both uses (#87 after Coby White: "18 until your pick"; #147 after Portis: "7 until your pick").

**Fix (D-M53).** Engine `clockRead(state)` with phases done / you / none-left / wait is now the single read of the clock; the countdown says "(your roster is full — N picks left in the draft)" in the none-left phase; the strip says "no picks left for you". A refused insert now re-renders the log so its warning is visible immediately (it used to surface only on the next action). Red-first: 8 `test_card` cases on the mock-53 board, parity item 8 against `hoops.clock_read`, and the Chromium replay re-run on the fixed page (`m53_dom_replay.json`).
