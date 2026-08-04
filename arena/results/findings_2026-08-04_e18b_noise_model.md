# E18b — the room's noise model, fixed the day it shipped (2026-08-04)

**Owner's report (first mock on the named room):** "Shai is still available
by the 8th pick… I'd still like to keep it as realistic as possible."
Screenshot evidence: SGA on the card at pick #8, and Noah — then modeled
as near-deterministic autodraft — spending #7 on Jalen Johnson.

## Diagnosis (measured, 300 rooms)

The deterministic layer was innocent: Noah's zero-noise board IS the
market board (Wemby, Jokic, Luka, SGA…). The defect was the noise model:
**flat additive gaussian in rank units, drawn independently per candidate.**
With ~250 candidates each drawing their own sample, the maximum of those
draws routinely promotes deep names over locked-in stars — top-of-board
chaos that no real room exhibits.

Shipped-model baseline (E18a, flat additive):

- P(a market-top-2 name still available at pick 5) = **31.8%**
- P(a market-top-4 name still available at pick 8) = **15.0%** ← the owner's screenshot
- Off-book R1 picks (both boards > pick+8) = **10.4%**
- SGA specifically: past pick #7 in 20% of rooms, worst fall #20

Real reference: in the owner's real 2025-26 draft, the market top-4 went
in the top 4, and every R1 pick was within book of at least one board.

## Owner corrections folded in (same session)

1. **Noah autodrafted in 2025-26 ONLY** — 23-24/24-25 were manual. His
   −43.5 reach is therefore pure Yahoo-board geometry (the cleanest
   geometry reading the data contains): retained as the seat-free scale
   reference, **excluded from his behavioral fit** per the owner's
   instruction. Forward model: manual ADP-leaning drafter (adp_w 0.75,
   noise 9) with genuine LaMelo loyalty (R1/R2, both manual seasons).
   Naz Reid pair dropped (R8 leg was the autodraft).
2. The geometry scale is now computed seat-free — mean over the first 72
   market-board slots of (slot − valueRank) — instead of reading Noah's
   simulated seat.

## The fix and the sweep

**Log-normal rank noise:** `rank × exp(N(0, noise/50))` — the top of the
board is near-deterministic, disagreement grows with depth (this is how
real ADP variance behaves). Availability became proportional
(`×(1 + (1−av)·0.35)`, streamers 0.15) instead of a flat +8.8-rank shove
that unrealistically buried market-loved injured stars in R1. Loyalty
discounts floored at rank 1.

8-variant workflow sweep (σ divisor 0/35/50/65 × availability flat/mult;
300 realism rooms + 60 full 13-round reach rooms per cell, owner seat
following the shipped blend50 card). Every multiplicative cell passed the
realism gates; the multiplicative-availability arm was uniformly better
on off-book rate (0.9% vs 2.6%) and reach ordering. One gate failed
everywhere: Spearman ≥ 0.85 — traced to a single param misfit: **Kyle**,
whose measured reach is mild (−7, 7th-deepest of 10) but whose hand-set
adp_w 0.55 simmed him 3rd-deepest. Refit to his own measurement
(adp_w 0.45, noise 9) — the same class of data-driven refit as Robby's,
in the opposite direction.

## Final validation (winner: divisor 50, multiplicative availability)

| Gate | Baseline (E18a) | Shipped (E18b) | Bar |
|---|---|---|---|
| P(market-top-2 alive at pick 5) | 31.8% | **0.0%** | ≤2% |
| P(market-top-4 alive at pick 8) | 15.0% | **0.0%** | ≤5% |
| Off-book R1 picks | 10.4% | **0.9%** | ≤3% |
| Scaled reach band (10 behavioral managers, ±8) | 10/10 | **10/10** | 10/10 |
| Reach-ordering Spearman (n=10) | 0.915* | **0.952** | ≥0.85 |
| P(Robby drafts Jarrett Allen) | 0.40 | **0.77** | ≥0.25 |

*pre-fix model recomputed on the new 10-manager definition for honest
comparison.

- **Port equivalence:** the deck's shipped `managerScores` reproduces the
  winning sweep cell EXACTLY (identical per-manager reach to the decimal
  on the same seeds) — the validated code is the shipped code.
- **App smoke:** full-draft completion at owner slots 2/8/11, cast stored
  and legal, all rosters position-complete.
- **Owner-card parity: 7/7 ledger replays byte-identical** vs the
  pre-E18 engine — the ΔECW blend50 card is untouched by both E18a and
  E18b.

Adversarial verification (independent agent): no CRITICAL or MAJOR
defects; port equivalence proven behaviorally (byte-identical outputs at
identical seeds); rng save/resume determinism confirmed (single-shot
Box-Muller, no cached spare; cast shuffle uses a derived seed and is
persisted). One honest caveat it surfaced: the scaled reach band's ±8
tolerance is loose relative to the scaled targets (span ≈ [−5.6, +2.0]),
so within this gate set the Spearman ordering gate is the discriminating
reach test — worth remembering when the absolute band re-arms in October.

## Standing notes

- MGR_NOISE_DIV = 50 is the single new engine constant; kill switch
  documented in REVERT-MAP (named-room section).
- The absolute reach band still re-arms at the October real-ADP sync
  (market geometry is ~0.45× reality until then — unchanged by E18b).
- Whether Noah autodrafts again in October is unknown. If the owner
  learns he will, set his entry back to adp_w 1.0 / val_w 0 / noise 2
  (one line in MANAGERS + profiles.json).
