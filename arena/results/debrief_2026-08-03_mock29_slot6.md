# Mock 29 post-mortem — slot 6: the board metric misses in the other direction (2026-08-03)

Completed 13-round mock (156/156, snake verified, no duplicates). Replayed
through the shipped app block on the 8/3 pull; 18,000-season headline; the
counterfactual work folded into the gradient-gate experiment
(`findings_2026-08-03_gradient_gate.md`), 6,000 × 2 per arm.

## Outcome

| Metric | Mock 29 (slot 6) |
|---|---|
| Champ% | **8.99** |
| Playoff% | 58.7 |
| Finish | 5th of 12 |
| Kept-total | **−1.26 (10th of 12)** |
| Expected cats won/week | 4.643 |
| 🎯 exact hits | 4/13 |

Roster: Cade Cunningham, Donovan Mitchell, JJJ, Scottie Barnes, Bam Adebayo,
Jalen Duren, Mikal Bridges, Deni Avdija, Norman Powell, Cameron Boozer,
Dylan Harper, Bilal Coulibaly, Neemias Queta.

**The board metric erred in the opposite direction from mock 27.** Where m27
held the room's *best* kept-total and finished outside the top 3, m29 held the
room's *tenth-best* and finished 5th. Two consecutive drafts, opposite signs,
same lesson: kept-total is not measuring what decides the season.
Room-level correlations: **kept-total +0.326, ECW +0.733**.

The roster is the flattest yet measured — per-category win rates run 36% to
63%, nothing dominant, nothing dead. That shape converts to a respectable
mid-table finish and almost no championship equity.

## The winner's shape, for contrast

Slot 4 (`punt_ft`) won at 21.96% on a kept-total of just +1.24, with a
deliberately lopsided profile: FG% 86%, REB 87%, ST 78%, BLK 86%, TO 76% —
five categories won decisively — while conceding FT% 21%, 3PTM 4%, PTS 28%,
AST 14%. It wins 5 of 9 nearly every week by construction.

That is the third consecutive room where a *concentrated* build beat a
*balanced* one, and it is the same mechanism the mock-28 oracle found. It is
**not** an endorsement of declared punting: G1a measured every punt-declaring
*policy* at −4.9 to −11.2pp, and the bot here is a fixed persona, not a
strategy the deck can adopt mid-draft. What it argues for is the concession
being *chosen* rather than *drifted into*.

## Counterfactual — the card lost again

| Line | Champ% | Δ |
|---|---|---|
| As drafted | **8.90** | — |
| Follow the composite card at all 9 deviation turns | 3.21 (8th) | **−5.69** |

**DEVIATION WON**, the third in the ledger — and the tally now shows a clean
pattern: all three DEVIATION WON arms are full-bundle card-follows (m26, m27,
m29; 3, 8 and 9 swaps; −5.76 to −8.71pp), while every COST arm is a single
swap or a small set. Across 18 arms the card is usually right about *a* pick
and reliably wrong as a whole-draft policy.

## The gradient-gate hypothesis — raised and REFUTED the same day

Mocks 24/25/26 (slots 1/2/3) all finished 1st; 27/28/29 (slots 4/5/6) all
finished mid-table. The deck's win-probability gradient orders the Top 5 only
at slots 1–3, so the boundary lined up exactly with the results and the
obvious inference was that the gate is too tight.

It is coincidence. Patching `GRAD_SLOTS = 3 → 12` and re-running all three
drafts under both cards:

| Mock | Slot | As drafted | Composite card | Gradient card |
|---|---|---|---|---|
| 27 | 4 | 9.76 | 1.05 | 3.14 |
| 28 | 5 | 6.50 | **7.34** | 0.30 |
| 29 | 6 | **8.90** | 3.21 | 0.22 |

The gradient card beats the composite card in **1 of 3** and loses badly in
the other two. Widening the gate is removed from September E9 as a measured
negative. Full method, residual confounds and two harness defects (one fatal,
which killed 3 of 9 cells on the first run and was caught by adversarial
verification) are in `findings_2026-08-03_gradient_gate.md`.

## Instrument notes

- **BUY NOW 37/39 = 95%** — the highest precision measured, comfortably above
  the 83–91% band.
- **Quiet survival 5/23 = 22%** — the lowest measured, continuing a clear
  slide: **m27 50% → m28 37% → m29 22%**. A quiet card is supposed to mean
  "safe to wait," and in these value-heavy rooms it increasingly is not. This
  sharpens September E2 from "recalibrate" to "the quiet chip is currently
  the least trustworthy marker on the card." Owner-facing implication until
  then: **treat a quiet card as weaker evidence than the label suggests.**
- **Drift latch correctly silent** for the third consecutive draft — FT% 10th
  and 3PTM 9th never reached the dead tier, and the roster had ample bigs.
  Three straight mid-table finishes with no structural alarm is now the E10
  case ("quiet zone" escalation).

## Owner-reported defect, same session

The owner reported from a live draft that the card suggested a center with
five already rostered. Investigated and confirmed as a real defect in the
**TARGET** line specifically — its family fallback has no roster-need check,
and 12 of 32 TARGET lines across mocks 27–29 name a family already at or
above its startable floor. The Top-5 ordering itself is behaving as designed
(every candidate that late is bench-bound regardless of position). Full
diagnosis and two candidate fixes:
`findings_2026-08-03_target_family_defect.md`.

## Corrections log

1. **The gradient-gate hypothesis was mine, and it is refuted.** It was the
   most promising lead of the last three drafts and it did not survive
   contact with the counterfactual. Recorded as a negative result rather
   than quietly dropped.
2. **My counterfactual harness had a fatal bug** — a card naming the same
   player at two owner turns crashed the arm, because legality was screened
   against the original board while swaps apply to a running one. It killed
   3 of 9 cells and was initially reported as `-1` sentinels. Found by
   adversarial verification, fixed, all 9 cells re-run.
