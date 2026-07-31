# Mock 21 post-mortem — slot 4, first draft on card v4: BEST RESULT EVER (2026-07-31)

Completed 13-round mock (156/156, all names resolve incl. Ace Bailey/
Simons). First draft on the final card (single 🎯, S/W/Winnable/Soft-punt
panel, quiet-wait semantics, no CAN WAIT chips). Replay via the shipped
app block at all 13 owner states; seasons 6,000 × 3; three CFs 6,000 × 2.

## Outcome — new lab record

| Metric | Mock 21 (slot 4) | Previous best |
|---|---|---|
| Champ% | **26.73 (1st/12)** | 15.37 co-2nd (m16) |
| Playoff% | **91.2** | 73.1 (m16) |
| Kept-total | **+7.13 (1st)** | — first time board AND finish both #1 |
| 🎯 exact hits | **8/13** (prior best 6) | |

Roster: Jokić, Tatum, KD, Flagg, Kessler, Coby, Quickley, Powell,
Hartenstein, DeRozan, Nesmith, Tobias, Melton. Broad-strong shape
(REB 3rd, PTS 4th, FG%/FT% 5th) on the Jokić anchor; conceded
3PTM/ST/TO (all 8th).

## The lessons landed

- **The R1 standout law, applied.** Cade went #1 overall and Jokić fell
  to #4 — the exact situation that cost −3.3pp in mock 20 (fallen SGA
  passed). This time the owner took the fallen #1. That single habit
  change is worth more than any layer we've shipped.
- **Quiet-wait banking, 3-for-3 on debut.** Hartenstein (quiet at #93 →
  taken #100, with the TARGET row endorsing Powell in between — the
  double-dip the new card is designed to produce), Nesmith (#117→#124),
  Melton (#141→#148). All held.

## Counterfactuals — the doctrine gets sharper

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 26.91 | 1st |
| CF1 — Quickley→🎯 Suggs (#76, board 23) | **36.48** | 1st |
| CF2 — shallow misses→🎯 (KD→Murray #28, Flagg→Pritchard #45) | 21.06 | 2nd |
| CF3 — interior removed (Kessler→Garland #52) | 21.78 | 2nd |

- **The one deep deviation left +9.6pp on the table.** Suggs was the 🎯
  at BUY NOW ~1% and went two picks later; Quickley was board #23. A
  36% draft — which would have been the best roster this lab has ever
  simulated — was one card-follow away. Deep deviations (board ≥ ~10)
  are now 0-for-4 across the ledger.
- **Shallow overrides inside the coin-flip band were GOOD (−5.9pp to
  undo them).** KD (Δ−0.38) and Flagg (Δ−0.18) beat the card's own #1s.
  Refinement: within ~0.4 of the top card, the owner's shape judgment
  outperforms the composite's ordering — exactly the band where the
  card itself declares a coin flip.
- **Interior structural family: 5-for-5** (m13, m18, m19, m20, m21).
  Quiet-C Kessler at #52 was worth +5.1pp over the on-card guard.

**Doctrine, v3 (11 graded mocks):** take the 🎯 when it's a fallen R1
star or the gap is deep; trust your own read inside the coin-flip band;
buy structural interior whenever the card underprices it; never deviate
to board-#20+ names — that class is 0-for-4 and just cost a 36% draft.

## Chip scorecard (card-v4 methodology debut)

- BUY NOW **28/33 (85%) gone** before the next turn; TOSS-UP 3/4 gone.
- Quiet cards (no marker = safe to wait): **9/13 (69%) survived** to
  the next turn (four final-round rows unmeasurable — no next turn);
  misses cluster in the known mock-room acceleration class (Duren,
  Vučević, Edey taken within 1–4 picks of the flag). All three
  quiet-banks the owner actually attempted succeeded.
- Scarcity: 3 shelf chips, all vindicated (JJJ, Collins, WCJ gone 1–3
  picks after the flag); invariant clean.

## Room notes

`points_chaser` — mock 20's 39% winner — collapsed to 0.07% here
(Cade at #1 instead of Wemby): persona results are seat-and-fall
dependent, another reason champ% comparisons only mean anything
within a room. `stars` 2nd at 21.4%. `bpa_pure` 0.00% again.
