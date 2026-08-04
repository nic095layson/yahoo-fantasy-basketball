# Mock 28 post-mortem — slot 5: the board metric is not just noisy, it points the wrong way (2026-08-03)

Completed 13-round mock (156/156, snake verified, no duplicates). Replayed
through the shipped app block on the 8/3 pull; 18,000-season headline; seven
counterfactual arms at 6,000 × 2, with the headline counterfactual replicated
at three fresh seeds.

This draft was run one day after mock 27 raised the question of whether
kept-total is the right board metric. Mock 28 answers it with a controlled
experiment, and the answer is worse than "it's noisy."

## Outcome

| Metric | Mock 28 (slot 5) |
|---|---|
| Champ% | **6.44** |
| Playoff% | 63.2 |
| Finish | 6th of 12 |
| Kept-total | +1.58 (5th) |
| **Expected cats won / week** | **4.665** (need 5.0) |
| 🎯 exact hits | 6/13 |

Roster: Luka, Durant, Murray, Brunson, Bam, LaVine, Mikal Bridges,
McDaniels, Edey, Boozer, McCollum, Keyonte George, Tobias Harris.

Same pathology as mock 27, one seat over: strong where it was already
strong (PTS 78% of weeks, 3PTM 72%, AST 65%), hollow where it wasn't
(REB 33%, BLK 28%, TO 39%). 4.665 expected categories against the 5.0
needed to win a matchup.

## The room where kept-total has the wrong sign

| Slot | Champ% | Kept-total | ECW |
|---|---|---|---|
| 2 points_chaser | 21.66 | **−1.46** | 4.968 |
| 1 market | 21.19 | **−1.89** | 5.010 |
| 4 punt_ft | 19.13 | +3.48 | 4.835 |
| 12 punt_ft_to | 14.92 | **−9.43** | 4.808 |
| 9 safe_floor | 8.52 | +0.66 | 4.722 |
| **5 OWNER** | **6.44** | **+1.58** | **4.665** |
| 6 stars | 1.66 | **+3.02** | 4.381 |
| 10 upside | 0.00 | +2.15 | 3.452 |

Within this room: **corr(champ%, kept-total) = −0.293** — the wrong sign —
against **corr(champ%, ECW) = +0.823**. The two best teams both had
*negative* boards. The team with the highest kept-total (+3.48 excepted)
finished 8th at 1.66%.

## The controlled experiment — same freedom, opposite objectives

Mock 27 could only show that ECW *describes* outcomes better. Mock 28 tests
whether it is the better **objective**, holding the amount of hindsight
constant.

Two oracles were built with identical mechanics: walk the owner's 13 turns
in order; at each, consider every player drafted strictly later; take the one
that most improves the objective. Both get exactly the same 12 hindsight
re-picks. Only the objective differs.

| Arm | Kept-total | ECW | Champ% | Finish |
|---|---|---|---|---|
| As drafted | +1.58 | 4.665 | 6.50 | 6 |
| **ECW-greedy oracle** | **−0.92** | **5.268** | **34.58** | **1** |
| **Kept-total-greedy oracle** | **+3.54** | 4.114 | **0.28** | **11** |

Maximizing kept-total with perfect foresight produced the **second-worst
roster in the room**. Maximizing expected-cats-won produced **34.58%** —
higher than any result in the ledger (m24's 29.66% is the standing record).
The ECW winner did it while ending with a **negative** kept-total.

Replicated at three fresh seeds (101/202/303, 18,000 seasons):
oracle **35.63%**, baseline 6.59%. The effect is not seed noise.

**What this does and does not prove.** It proves the *objective* is doing the
work, not the hindsight — that was the whole point of the control, and the
control lost by 34pp. It does **not** prove ECW is usable at the draft table:
the oracle knows exactly when every player will be taken, so it is an upper
bound on what an ECW-guided card could reach, not a strategy anyone can run.
Building the realizable version — marginal ΔECW per candidate under a
*survival model* rather than perfect foresight — is exactly the registered
E9 experiment, and this is now its strongest supporting evidence.

The ECW roster's shape is instructive: LaVine, Sabonis, Franz Wagner, Brandon
Miller, Myles Turner, McCollum, Gobert, Avdija, PJ Washington, Filipowski,
Luka, Coward, Keyonte George — REB 89%, PTS 79%, 3PTM 73%, AST 65%, BLK 55%,
conceding TO (23%) and FT% (45%). It keeps Luka; it does not chase a third
scorer. Note it *emerged* into a soft concession rather than declaring one —
this does not contradict G1a, which measured punt-**declaring** policies that
zero-weight categories during drafting.

## Counterfactuals — and one arm that turned out to be degenerate

Paired against as-drafted at the arms' own config (6,000 × [11,23] = **6.50**).

| Arm | Champ% | Δ | Verdict |
|---|---|---|---|
| CF2 — Brunson (board 9) → Kessler | 8.40 | +1.90 | COST |
| CF1 — all 7 deviations → the card | 7.34 | +0.84 | WASH |
| CF4 — Bam (board 4) → Zubac | 7.09 | +0.59 | WASH |
| CF6 — interior repair (Kessler + Claxton) | 9.37 | **+2.87** | interior arm |
| CF3 — Keyonte (board 13) → Tobias Harris | 6.50 | **0.00** | **degenerate — excluded** |

**CF3 is a null swap and is excluded from the tally.** Keyonte George (#140)
and Tobias Harris (#149) were *both owner picks*. Swapping them only reorders
the owner's own roster, so the final roster — and every number — is identical
by construction. This is not a finding about the deviation; it is an artifact
of the swap methodology, and it is being recorded so the arm is never counted
as a wash.

What it *does* reveal is genuinely good news: the owner's board-13 "reach" at
#140 cost nothing **because the card's own pick was correctly marked quiet**.
Tobias Harris carried no BUY NOW chip at #140, meaning safe to wait — and he
survived nine picks to the owner's next turn. Take the scarce one, let the
quiet one wait: the instrument and the owner agreed, and both were right.

## Instrument notes

- **Chips:** BUY NOW 29/34 gone before the next turn (**85%**) — in the
  83–91% normal band, third consecutive draft in range. Quiet survival 37%,
  the lowest measured (m27 was 50%); the quiet chip is running optimistic in
  these value-heavy rooms, which is the recalibration already registered as
  E2. n=27 here.
- **Drift latch: correctly silent again.** REB reached 12/12 and BLK 11/12,
  but the latch needs *three* dead kept cats **and** fewer than two C-eligible
  players — the owner had Bam and Edey. As in mock 27, the build failed
  without ever meeting the structural-drift definition. Two consecutive
  mid-table finishes now sit in the gap between "healthy" and "drifting,"
  and nothing on the card marks that zone.
- **Panel narration was accurate throughout:** REB and BLK appear in
  Weaknesses or Soft punt from #53 onward, `REB 12/12` by #92. The read was
  right; there is no escalation attached to it.

## Ledger effects

- Deviation tally gains three arms (CF2 COST, CF1 WASH, CF4 WASH) →
  **17 arms: 8 COST, 7 WASH, 2 DEVIATION WON**. CF3 excluded as degenerate.
- Interior tally gains an *additive* arm (CF6, +2.87pp) → **5/5 positive from
  retained artifacts**, and for the first time from adding coverage rather
  than removing it.
- Mock 28 row added; ECW recorded alongside kept-total.

## September consequences

- **E8** (replace board rank with ECW in reporting) is upgraded from
  "better correlation" to "the incumbent metric has the wrong sign within a
  room." The m28 room is the case to include in the re-derivation.
- **E9** (ECW as a draft-time signal) now has a controlled result behind it:
  objective, not hindsight, produced the 34pp gap. The experiment's real work
  is the survival model that replaces perfect foresight — and the honest
  prior is that a realizable version captures much less than 28pp.
- **New: E10** — a "quiet zone" escalation for builds that are neither healthy
  nor drift-latched. Two drafts (m27, m28) have now finished mid-table with
  the latch correctly silent. Any proposal must keep the latch's 0-false-
  positive record on m21/m24/m25/m26.

## Corrections log

1. **"The oracle gave away Luka" — I nearly wrote this and it is false.**
   The greedy swapped Luka out at #5 and back in at #68, then again to #125;
   all three are owner picks, so Luka stayed on the roster throughout. Caught
   by printing the final roster before writing the claim.
2. **CF3 counted as a real arm — corrected before publication** once both
   players were traced to owner picks. Excluded from the tally with the
   reason recorded.
3. **CF6's first formulation was illegal** (Jarrett Allen went #62, before the
   #101 turn) and was refused by the legality assertion, not silently run.
   Re-specified with Nic Claxton (#109).
