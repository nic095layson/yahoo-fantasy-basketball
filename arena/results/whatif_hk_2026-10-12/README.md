# Towns at #10, or Haliburton at #10 and Towns at #15 (2026-10-12)

Owner question (2026-10-12, verbatim): "Can you please explain to me from your arithmetic perspective why Towns is suggested as my first round pick, when potentially Maxey, Edwards, Haliburton may still be on the board? Also.. Can you please review on previous mock / live draft records? What if I were to select Haliburton at 10, and KAT at 15?" — then the owner's PDF of Hashtag Basketball's 2025-26 final 9-cat ranks (read with pdfplumber; raw text pinned in the kit as `report/market/hashtag-final-9cat-2025-26-raw-2026-10-12.txt`).

## Files

- `survival_records.json` (`arena/mocks/whatif_hk_survival_records.py`): where Towns and Haliburton went in every committed slot-10 room 51–75, and whether each lasted #11–#14 when the owner left him at #10.
- `card_lines_2025-26.json` (`arena/mocks/whatif_hk_lines2526.py`): mock 75's #10 card on the shipped lines and with 2025-26 per-game lines (Towns only; Towns, Maxey, Edwards; every row with 2025-26 GP 40+), from `arena/results/actuals_2026-10-09/actuals_2025-26.csv`.
- `breakeven.txt` (`arena/mocks/whatif_hk_breakeven.py`): mock 75's #10 card as Haliburton's availability moves from the shipped risk tag (value ×0.78, weekly 0.75) to a healthy row (×1.0, 0.88).
- `shipped/`, `haliburton_healthy/`, `lines_2025-26/`: `arena/mocks/whatif_hk.py <mock> <out>` for the 13 rooms where both men were on the board at #10 (51, 52, 53, 56, 57, 58, 59, 60, 61, 67, 73, 74, 75), with `HALI_HEALTHY=1` or `LINES2526=1` for the two sensitivities; `aggregate.json` / `aggregate.txt` from `arena/mocks/whatif_hk_aggregate.py <folder>`. Room files written before a switch existed carry no key for it (off).

## Method

Every arm holds the owner's other eleven picks as drafted and moves players by strict pairwise swaps (the `live_retro` convention), on the current pool (tag v58 = v59 values), graded by 18,000 CRN seasons (seeds 11/23/47) on the league's real eight-team bracket, the owner veto on. Arms: as drafted; Towns + Haliburton at #10/#15 (the same thirteen men in either order); Towns at #10 with Haliburton taken at #11 or #14 and #15 = the card's #1 on that board; Haliburton at #10 with Towns taken at #11 or #14 and #15 = the card's #1 (the two picks averaged). Expected title odds: Towns first = p(Haliburton lasts) × both + (1 − p) × Towns-path; Haliburton first = p(Towns lasts) × both + (1 − p) × Haliburton-path.

## Results

### the shipped lines (v58 = v59 values)

Means over 13 rooms: Towns + Haliburton 19.27%; Towns + the card's #15 21.24%; Haliburton + the card's #15 17.03%. Losing Towns costs more than losing Haliburton in 12 of 13 rooms; the card's #15 man beats Haliburton as Towns' partner in 12 of 13. Haliburton first wins at no Towns survival rate (Haliburton's own at 0.43).

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 20.70% | 19.27% | -1.44 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 20.39% | 18.21% | -2.18 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 20.39% | 17.03% | -3.37 |

| room | owner #10 / #15 as drafted | as drafted | Towns + Haliburton | Towns + the card's #15 (Haliburton gone) | Haliburton + the card's #15 (Towns gone) | the card's #15 on each path |
|---|---|---|---|---|---|---|
| mock 51 | Anthony Edwards / Karl-Anthony Towns | 19.04% | 10.92% | 19.04% | 8.54% | Towns path: Anthony Edwards; Haliburton path: Chet Holmgren |
| mock 52 | Jayson Tatum / Donovan Mitchell | 11.15% | 15.89% | 17.59% | 13.75% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 53 | Jayson Tatum / Karl-Anthony Towns | 12.96% | 15.43% | 12.96% | 14.58% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 56 | Karl-Anthony Towns / Tyrese Haliburton | 9.63% | 9.63% | 13.74% | 5.73% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 57 | Jayson Tatum / Karl-Anthony Towns | 13.21% | 15.16% | 18.23% | 13.83% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 58 | Tyrese Haliburton / Karl-Anthony Towns | 22.63% | 22.63% | 24.92% | 19.30% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 59 | Tyrese Haliburton / Karl-Anthony Towns | 14.95% | 14.95% | 15.75% | 12.71% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 60 | Karl-Anthony Towns / Kevin Durant | 33.73% | 33.22% | 33.73% | 32.27% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 61 | Karl-Anthony Towns / Donovan Mitchell | 16.60% | 15.42% | 16.60% | 14.54% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 67 | Karl-Anthony Towns / Tyrese Haliburton | 18.48% | 18.48% | 21.14% | 19.73% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 73 | Karl-Anthony Towns / Donovan Mitchell | 34.17% | 33.22% | 34.89% | 28.19% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 74 | Karl-Anthony Towns / Donovan Mitchell | 17.91% | 16.10% | 17.91% | 12.29% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 75 | Karl-Anthony Towns / Tyrese Haliburton | 29.39% | 29.39% | 29.66% | 25.86% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |

### Haliburton fully healthy (his first-season-back tag cleared)

Means over 13 rooms: Towns + Haliburton 23.71%; Towns + the card's #15 21.07%; Haliburton + the card's #15 21.31%. Losing Towns costs more than losing Haliburton in 7 of 13 rooms; the card's #15 man beats Haliburton as Towns' partner in 1 of 13. Haliburton first wins once Towns lasts to #15 with probability 0.37 or more (Haliburton's own at 0.43).

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 21.79% | 23.71% | +1.92 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 22.20% | 22.58% | +0.38 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 22.20% | 21.31% | -0.89 |

| room | owner #10 / #15 as drafted | as drafted | Towns + Haliburton | Towns + the card's #15 (Haliburton gone) | Haliburton + the card's #15 (Towns gone) | the card's #15 on each path |
|---|---|---|---|---|---|---|
| mock 51 | Anthony Edwards / Karl-Anthony Towns | 18.67% | 14.76% | 18.67% | 12.15% | Towns path: Anthony Edwards; Haliburton path: Chet Holmgren |
| mock 52 | Jayson Tatum / Donovan Mitchell | 11.05% | 19.82% | 17.60% | 17.07% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 53 | Jayson Tatum / Karl-Anthony Towns | 12.99% | 20.41% | 12.99% | 19.24% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 56 | Karl-Anthony Towns / Tyrese Haliburton | 13.52% | 13.52% | 13.47% | 8.47% | Towns path: Tyrese Maxey; Haliburton path: Anthony Davis |
| mock 57 | Jayson Tatum / Karl-Anthony Towns | 12.70% | 19.76% | 17.86% | 18.65% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 58 | Tyrese Haliburton / Karl-Anthony Towns | 26.92% | 26.92% | 24.90% | 23.90% | Towns path: Tyrese Maxey; Haliburton path: Chet Holmgren |
| mock 59 | Tyrese Haliburton / Karl-Anthony Towns | 18.47% | 18.47% | 15.75% | 15.62% | Towns path: Tyrese Maxey; Haliburton path: Anthony Davis |
| mock 60 | Karl-Anthony Towns / Kevin Durant | 33.39% | 38.42% | 33.39% | 37.78% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 61 | Karl-Anthony Towns / Donovan Mitchell | 16.36% | 20.18% | 16.36% | 19.19% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 67 | Karl-Anthony Towns / Tyrese Haliburton | 22.64% | 22.64% | 20.93% | 24.11% | Towns path: Jalen Johnson; Haliburton path: Chet Holmgren |
| mock 73 | Karl-Anthony Towns / Donovan Mitchell | 33.09% | 38.31% | 34.34% | 33.34% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |
| mock 74 | Karl-Anthony Towns / Donovan Mitchell | 17.84% | 19.70% | 17.84% | 16.42% | Towns path: Jalen Williams; Haliburton path: Chet Holmgren |
| mock 75 | Karl-Anthony Towns / Tyrese Haliburton | 35.31% | 35.31% | 29.77% | 31.12% | Towns path: Donovan Mitchell; Haliburton path: Chet Holmgren |

### last season's lines (every row with 2025-26 GP 40+ on its 2025-26 per-game)

Means over 13 rooms: Towns + Haliburton 6.62%; Towns + the card's #15 9.20%; Haliburton + the card's #15 8.68%. Losing Towns costs more than losing Haliburton in 9 of 13 rooms; the card's #15 man beats Haliburton as Towns' partner in 13 of 13. Haliburton first wins at no Towns survival rate (Haliburton's own at 0.43).

| survival read | Towns first | Haliburton first | Haliburton first minus Towns first |
|---|---|---|---|
| public rooms on record (Towns 6 of 6, Haliburton 3 of 11) | 8.50% | 6.62% | -1.88 |
| the deck's survival read at #10 (v59 prices) (Towns 0.53, Haliburton 0.43) | 8.09% | 7.59% | -0.50 |
| the league cast on the real seating (Towns taken at #11 in 3 of 3 cast rooms; Haliburton 0.43 from the model) | 8.09% | 8.68% | +0.59 |

| room | owner #10 / #15 as drafted | as drafted | Towns + Haliburton | Towns + the card's #15 (Haliburton gone) | Haliburton + the card's #15 (Towns gone) | the card's #15 on each path |
|---|---|---|---|---|---|---|
| mock 51 | Anthony Edwards / Karl-Anthony Towns | 6.32% | 3.66% | 5.81% | 4.18% | Towns path: Jamal Murray; Haliburton path: Lauri Markkanen |
| mock 52 | Jayson Tatum / Donovan Mitchell | 5.49% | 4.11% | 5.39% | 6.46% | Towns path: Jamal Murray; Haliburton path: Anthony Davis |
| mock 53 | Jayson Tatum / Karl-Anthony Towns | 8.05% | 10.37% | 12.22% | 12.14% | Towns path: Jamal Murray; Haliburton path: Lauri Markkanen |
| mock 56 | Karl-Anthony Towns / Tyrese Haliburton | 1.48% | 1.48% | 6.14% | 4.73% | Towns path: Tyrese Maxey; Haliburton path: Tyrese Maxey |
| mock 57 | Jayson Tatum / Karl-Anthony Towns | 2.93% | 3.13% | 4.54% | 4.31% | Towns path: Jamal Murray; Haliburton path: Lauri Markkanen |
| mock 58 | Tyrese Haliburton / Karl-Anthony Towns | 6.14% | 6.14% | 10.46% | 11.12% | Towns path: Tyrese Maxey; Haliburton path: Tyrese Maxey |
| mock 59 | Tyrese Haliburton / Karl-Anthony Towns | 9.66% | 9.66% | 15.12% | 15.12% | Towns path: Tyrese Maxey; Haliburton path: Tyrese Maxey |
| mock 60 | Karl-Anthony Towns / Kevin Durant | 20.29% | 19.82% | 24.24% | 22.31% | Towns path: Jamal Murray; Haliburton path: Anthony Davis |
| mock 61 | Karl-Anthony Towns / Donovan Mitchell | 6.30% | 5.34% | 7.48% | 6.13% | Towns path: Jamal Murray; Haliburton path: Kawhi Leonard |
| mock 67 | Karl-Anthony Towns / Tyrese Haliburton | 4.72% | 4.72% | 5.99% | 6.98% | Towns path: Jamal Murray; Haliburton path: Lauri Markkanen |
| mock 73 | Karl-Anthony Towns / Donovan Mitchell | 13.28% | 10.97% | 13.29% | 10.99% | Towns path: Jamal Murray; Haliburton path: Kawhi Leonard |
| mock 74 | Karl-Anthony Towns / Donovan Mitchell | 3.58% | 2.54% | 3.58% | 3.65% | Towns path: Jamal Murray; Haliburton path: Anthony Davis |
| mock 75 | Karl-Anthony Towns / Tyrese Haliburton | 4.09% | 4.09% | 5.38% | 4.70% | Towns path: Jamal Murray; Haliburton path: Kawhi Leonard |

## The card's arithmetic at #10 (mock 75's board)

Shipped lines: Towns #1 (value 4.15, ΔECW 4.327), Maxey #2 (3.63, 4.185), Jalen Johnson #3 (3.15, 4.365), Haliburton #4 (3.87 = 4.96 raw × 0.78, 4.146). Haliburton passes Towns between value ×0.835 / weekly 0.782 and value ×0.846 / weekly 0.789 (`breakeven.txt`).
2025-26 lines: Towns only, he falls to card #26 (Maxey #1, Haliburton #2); Towns, Maxey and Edwards, Towns #26 and Maxey #1; every row with 2025-26 GP 40+, Maxey #1, Haliburton #8, Towns #23 (`card_lines_2025-26.json`). 44 of the 52 top-60 board rows with a 2025-26 season of 20+ games sit closer to their 2024-25 line than to 2025-26: the owed WO-5 refresh (2025-26 per-36 scaled to projected minutes) has not run.

## Bounds

- Pairwise swaps hold every other seat's picks fixed; in mock 51 the Towns path's #15 is the owner's own #10 (Edwards), who would likely not last #11–#14 (means without mock 51 in `aggregate.txt`).
- The 2025-26 sensitivity replaces lines with last season's per-game: a bound, not a projection (no minutes forecast, no shrinkage toward career).
- Survival reads: public human rooms are strangers drafting near Yahoo's prices; the cast rooms are the deck's own league-mate bots, whose rounds 1–6 value axis is the deck's own (Towns rank 6), so their Towns picks lean early.

