# Mock 25 post-mortem — slot 2 gradient seat: the empty-roster finding REPLICATES (2026-07-31)

Completed 13-round mock (156/156). Second gradient seat (slot 2 ≤
GRAD_SLOTS) and the first draft with the structural-drift latch live.
Replay via the shipped app block; seasons 6,000 × 3; three CFs 6,000 × 2.

## Outcome — second consecutive 1st (third in the last five drafts)

| Metric | Mock 25 (slot 2) | Same-day ledger |
|---|---|---|
| Champ% | **29.00 (1st/12)** | m24 29.66 (1st) immediately prior; m23 0.16 (12th) and m22 0.22 (11th) before that |
| Playoff% | **94.4 — best measured** | |
| Kept-total | **+6.36 (1st)** | board-and-finish double, as in m24 and m21 |
| 🎯 exact hits | **10/13 — best measured** | the last TEN picks all exact |

Roster: Wemby, KD, Tatum, Garland, Hart, LeBron, MPJ, McDaniels,
Gordon, Collins, Nesmith, Horford, DLo. BLK 3rd, FT% 3rd, 3PTM 4th;
only real concession ST 11th.

## The headline: Wemby-over-🎯-SGA replicates at +7.5pp

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 29.19 | 1st |
| CF1 — Wemby→🎯 SGA at #2 (the gradient's empty-roster pick) | **21.66** | 1st |
| CF2 — KD→🎯 Murray at #23 (board 13, Δ−2.72) | 29.65 | 1st |
| CF3 — Tatum→🎯 Murray at #26 (board 5, Δ−1.18) | **33.28** | 1st |

**CF1 is a genuine replication of mock 24.** Yesterday, slot 1: taking
Wemby over the gradient's SGA was worth **+14.1pp**. Today, slot 2,
different room, different seeds: **+7.5pp**, same direction. Two
independent rooms now agree that the gradient's *empty-roster* choice
is beatable by an outlier anchor.

**Honest scope limit:** both instances are the SAME player pair
(Wemby vs SGA at r=0) in the same July pool — this replicates across
rooms and seeds, not across outlier profiles. The Φ-saturation
hypothesis (the gradient's curves flatten on extreme single-cat
outliers, so Wemby's +7z BLK buys ~half a category win and stops
counting) predicts the effect is specific to outlier anchors, not to
pick 1 generally. **The registered September experiment must therefore
test multiple outlier profiles and pools, not re-run Wemby.** No engine
change under the freeze on n=2 same-pair evidence.

**The deviation law needs a correction.** CF2 vs CF3 invert the usual
depth ordering: the *deeper* deviation (KD, board 13) was free (+0.5pp,
noise) while the *shallower* one (Tatum, board 5) cost 4.1pp. The two
turns are entangled — both passed the same 🎯 (Murray, who lasted to
#30) — so they are not independent single-pick tests. The correct read
is not "depth predicts cost" but **"who you gave up predicts cost"**:
KD ≈ Murray for this roster, Tatum < Murray. Depth of deviation remains
a weak prior only (current tally in `arena/results/LEDGER.md`; mock 26
later produced the first deviation bundle to clearly BEAT the card) — this
pair already shows the proxy breaking.

## New instrumentation — first live outing

- **Structural-drift latch: correctly SILENT** all 13 turns. This is
  the intended negative case (the calibration promised no fire on a
  winner) and it is the third independent winner it has stayed quiet
  on (m21 26.7%, m24 29.7%, m25 29.0%). ST at 11th was the lone dead
  cat — one is normal and survivable, which is exactly why the
  threshold sits at three.
- **Soft Punt rank annotations** rendered throughout; the wheel-
  corrected chip horizon graded BUY NOW 17/23 (74%) and quiet 12/16
  (75%) — the most balanced chip performance of any mock, at a
  non-wheel seat where the fix is a no-op by construction.

## Ledger after 14 graded mocks

The last five drafts, in order: m21 26.73% (1st), m22 0.22% (11th),
m23 0.16% (12th), m24 29.66% (1st), m25 29.00% (1st). ALL FIVE land in
one of two buckets — 1st place or catastrophe — with nothing in
between, and the separating variable is interior coverage. Mock 25 is
the second consecutive 1st, not a third: the 12th-place mock 23 sits
two drafts back. The
winning recipe is now stable and repeatable: **anchor with the outlier
big, follow the card everywhere the roster isn't screaming, and never
let three categories reach 11th.**
