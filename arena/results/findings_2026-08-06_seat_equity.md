# Seat equity — ranking all 12 draft slots by title odds (2026-08-06)

**Owner question:** "In all the mock draft data that I've had you analyze,
can you rank the 12 seats in their prob% to win the league?"

Derived from **13 v2-instrument standard rooms** (mocks 40, 42, 43, 44, 45
+ the 8 E25 default rooms), each 18,000 simulated seasons, all 12 seats
recorded. Mock 41 excluded (sharp room); v1-epoch rooms reported
separately since absolute champ% is not comparable across the instrument
change.

**Method note that matters:** the seat table below uses **bot-occupied
seats only**. Including the owner's seat would measure "seat + owner
skill," not seat. The owner sat in a different slot nearly every mock, so
his results are analyzed separately in §3.

## 1. Seat ranking (v2, bot-occupied, fair share = 8.33%)

| Rank | Seat | Champ% | sd | n |
|---|---|---|---|---|
| 1 | **1** | **15.18** | 10.29 | 12 |
| 2 | **2** | **14.08** | 6.46 | 13 |
| 3 | **4** | **13.94** | 9.35 | 10 |
| 4 | 3 | 8.99 | 6.59 | 12 |
| 5 | 6 | 7.32 | 4.47 | 11 |
| 6 | 7 | 6.01 | 2.43 | 12 |
| 7 | 5 | 4.33 | 2.38 | 12 |
| 8 | 9 | 4.26 | 2.57 | 13 |
| 9 | 11 | 3.96 | 2.55 | 13 |
| 10 | 12 | 3.36 | 2.89 | 12 |
| 11 | 8 | 3.20 | 2.51 | 11 |
| 12 | **10** | **2.03** | 1.30 | 12 |

**By block — this is the load-bearing result:**

| Seats 1–4 | Seats 5–8 | Seats 9–12 |
|---|---|---|
| **13.03%** | 5.21% | 3.43% |

Early vs late: **Welch t = 7.57** (n = 47 vs 50). Not noise. A top-four
seat is worth roughly **4× a bottom-four seat** in this simulator.

Within-block ordering (3 vs 4, 5 vs 6, 8 vs 10) is NOT resolved — those
gaps sit inside one standard error. **Read the blocks, not the ranks.**

## 2. Why early seats win here (INFERENCE, mechanism)

The 2026 projection pool is extremely top-heavy: Wemby, Jokic, Luka and
SGA carry z-totals far above the rest of round 1, and no pair of
mid-round picks replaces one of them. The snake's compensation for a late
seat — back-to-back picks at the turn (Seat 12 gets 12+13, 36+37) — is
worth less than one franchise center in a 9-cat z model. Seat 12 does out-
perform seats 8 and 10 slightly, which is the wheel showing up, but it
does not close the gap to seats 1–2.

Note also the sd column: early seats have **4× the variance** of late
seats (10.29 at Seat 1 vs 1.30 at Seat 10). An early seat is a high-
ceiling lottery ticket; a late seat is reliably mediocre.

## 3. The owner's edge over his own seat (EVIDENCE)

For each v2 standard room, the owner's result vs that seat's bot baseline:

| Room | Seat | Owner | Seat baseline | Edge |
|---|---|---|---|---|
| e25-606 | 3 | 32.93 | 8.99 | **+23.94** |
| e25-202 | 1 | 37.66 | 15.18 | +22.47 |
| e25-707 | 10 | 20.29 | 2.03 | +18.26 |
| mock44 | 7 | 23.64 | 6.01 | +17.63 |
| e25-505 | 8 | 19.62 | 3.20 | +16.42 |
| e25-404 | 12 | 16.98 | 3.36 | +13.62 |
| mock40 | 4 | 26.29 | 13.94 | +12.35 |
| e25-303 | 6 | 19.06 | 7.32 | +11.73 |
| e25-101 | 4 | 24.31 | 13.94 | +10.37 |
| mock43 | 6 | 17.65 | 7.32 | +10.33 |
| mock45 | 8 | 12.05 | 3.20 | +8.85 |
| e25-808 | 4 | 19.24 | 13.94 | +5.30 |
| mock42 | 5 | 6.43 | 4.33 | +2.10 |
| **mean** | | | | **+13.34pp** |

**Positive in 13 of 13**, from every seat tested (1, 3, 4, 5, 6, 7, 8,
10, 12). The smallest edge (+2.10) is mock 42 — the frameless draft. The
largest come from *late* seats, where the baseline is low and structure
matters most.

**Practical reading: the owner's edge (+13.3pp) is larger than the entire
seat spread (15.18 − 2.03 = 13.2pp).** A well-built team from Seat 10
(20.29 in e25-707) beats an average team from Seat 1 (15.18). Draft
position matters a lot; how you use it matters slightly more.

## 4. v1-epoch comparison (older instrument, shape check)

| Seats 1–4 | Seats 5–8 | Seats 9–12 |
|---|---|---|
| 13.41% | 6.08% | 3.69% |

Same shape, same ordering of blocks, under a materially different week
model — the seat gradient is a property of the draft-value curve, not of
the scoring instrument.

## 5. Bounds — do NOT read these as real-league title odds

- **These are simulator numbers.** The real league's bracket (8 teams, no
  byes, three 1-week rounds) is more chaotic than the sim's top-6, and
  its last two champions had the **7th-best record**. Real seat equity is
  almost certainly flatter than 4:1.
- **No streaming, trades, or waivers** in the sim; a late seat in reality
  can recover value in-season through the 16–87 moves real managers make.
- **n ≈ 12 per seat** is enough for the block conclusion (t = 7.6) and
  not enough for individual seat ordering inside a block.
- Seat effect is conditional on THIS projection pool's top-heaviness.
  September's re-projection (E-2b) could flatten or steepen it; this
  table should be regenerated after the pool refresh.
