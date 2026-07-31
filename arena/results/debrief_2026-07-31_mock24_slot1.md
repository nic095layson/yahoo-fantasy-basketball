# Mock 24 post-mortem — slot 1 wheel, first gradient-seat draft: NEW RECORD, and the card's first big miss (2026-07-31)

Completed 13-round mock (156/156). First draft ever from a gradient seat
(slot 1 ≤ GRAD_SLOTS — the Top-5 order IS the win-probability gradient)
and the first slot-1 wheel since the horizon fix. Replay via the shipped
app block; seasons 6,000 × 3; three CFs 6,000 × 2.

## Outcome — the record moves again

| Metric | Mock 24 (slot 1) | Previous best |
|---|---|---|
| Champ% | **29.66 (1st/12)** | 26.73 (m21, the day before) |
| Playoff% | **92.4** | 91.2 (m21) |
| Kept-total | **+7.26 (1st)** | second board-and-finish double |

Roster: Wemby, Murray, JJJ, Brunson, Bam, LeBron, Suggs, Avdija,
Vučević, Boozer, Grant, Melton, McCain. Balanced-strong: BLK/PTS/ST
all 4th, nothing conceded worse than 8th — the Wemby-anchor build.

## The headline: the owner beat the card at pick 1 by 14 points

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 29.82 | 1st |
| CF1 — Wemby→🎯 SGA at #1 (the gradient's standout, Δ−2.7) | **15.70** | 3rd |
| CF2 — JJJ→🎯 Bane at #25 (deep deviation, board 17) | **35.14** | 1st |
| CF3 — Bam→🎯 Hart at #49 | 26.18 | 1st |

- **CF1 is the first major counterexample against the card.** The
  gradient-ordered list put SGA at 🎯 with a standout-class lead, and
  following it would have cost **−14.1pp** — the largest single-pick
  effect ever measured, in the wrong direction. Mechanism hypothesis:
  at an EMPTY roster the gradient's Φ terms saturate on extreme
  single-cat outliers — Wemby's +7z BLK buys ~half a weekly category
  win and then flatlines, so the math systematically discounts exactly
  the outlier-anchor profile that pick-1 exists to capture. The
  slot-1–3 ordering codification (+12.67pp cross-room average, t=4.63)
  stands — but its r=0 edge case is now suspect. **Registered September
  experiment: empty-roster gradient / pick-1 anchor study** (does the
  gradient's first-pick choice underperform plain composite at r=0
  across rooms and seeds?). No engine change under the freeze on a
  single-room CF.
- **CF2: deep deviations keep costing.** JJJ at board 17 over 🎯 Bane
  left +5.3pp on the table (a 35.1% phantom — the best roster the lab
  has ever simulated). Note JJJ was interior, but the interior-family
  wins were always about FILLING a hole; with Wemby already anchoring,
  a second early big was doubling down, not repairing. The interior
  exception requires an actual hole.
- **CF3: shallow-band owner judgment is now 3-for-3** (m21 KD/Flagg,
  m24 Bam over the thrice-🎯 Hart, +3.6pp). Within ~0.6 of the top
  card, the owner's read keeps beating the sort.

**Doctrine v4:** structure ≫ price ≫ name, unchanged — with the R1 law
split in two: *a fallen star is a take* (m20/m21, both confirmed), but
*the empty-roster 🎯 is the card's least-trusted output* — at pick 1,
an outlier anchor (Wemby-class) beat the gradient's spread pick
decisively. Shallow band: trust yourself.

**CORRECTION (2026-07-31, owner-caught):** this section originally read
"deep deviations: now 0-for-6 across the ledger". That tally was wrong —
the CF-tested sample is 8 arms, of which 5 cost and 3 were washes. The
defensible claim is *no CF-tested deviation has ever clearly beaten the
card (0 of 8), but 3 cost nothing measurable*. All cumulative tallies are
now derived in `arena/results/LEDGER.md`, not carried in prose.

## Wheel-horizon fix — validated live at the other wheel

BUY NOW graded **28/30 (93%) gone** at the corrected look-through
horizon across ALL of slot 1's turns; restricted to the six
pair-boundaries the fix actually targets it is **15/17 (88%)**. (Audit
correction 2026-07-31: this paragraph originally attributed the
all-turns figure to the pair-boundaries.) The comparable pre-fix
measurement at slot 12 was 0/10. Quiet survival ran 2/9: slot-1
horizons span ~23 picks and the value-drafting mock room accelerates
across that window — the known caveat, already registered for
September recalibration. The 🎯-Hart sequence graded itself: quiet at
#49 (survived its horizon ✓), TOSS-UP ~47% at #72/#73 (gone #83,
inside the #96 horizon — correctly a coin flip).

## Room notes

`punt_ft_to` 2nd at 15.6% again (narrow 2-cat punt, big coverage kept
— the survivable punt shape, consistent with m22's nuance). `upside`
0.00%. The owner's 29.7% from the wheel with the room's best board is
the strongest absolute and relative result of all 13 graded mocks.
