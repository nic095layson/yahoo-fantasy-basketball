# TARGET names a position family the roster does not need — owner-reported defect (2026-08-03)

**Reported by the owner from a live draft**, with a screenshot: at pick #138
(round 12 of 13, roster 11/13, families **G 5 / F 5 / C 5**), the decision
card read `TARGET: Rim-protecting C — can wait` and the 🎯 sat on Dereck
Lively II, C, with two more centers in the Top 5. The owner's objection: *"The
system is suggesting me to draft a C when I already have 5 on my roster."*

**Verdict: the objection is correct about the TARGET line, and the defect is
real and reproducible. It is a distinct issue from the Top-5 ordering, which
is behaving as designed.**

## Two different surfaces, only one of which is broken

### The Top-5 ordering is working as designed (not a defect)

Reconstructing the owner's exact roster and asking the engine what each
candidate's lineup weight would be:

| Candidate | Pos | Would start? |
|---|---|---|
| Dereck Lively II | C | **bench** (0.15) |
| Mitchell Robinson | C | **bench** (0.15) |
| Jrue Holiday | PG | **bench** (0.15) |
| Tobias Harris | PF | **bench** (0.15) |
| Wendell Carter Jr. | C | **bench** (0.15) |

At 11/13 with all ten lineup slots filled, *every* remaining candidate is
bench-bound regardless of position — a guard is no more startable than a
sixth center. So the card is not preferring centers over needed positions;
there is no needed position left. Two guards in `strategyScores` make the
bench penalty inert here (`nStarted >= LINEUP_SLOTS.length` short-circuits
`benchBound` to false, and the penalty `s *= BENCH_WEIGHT` only applies when
`s > 0`, while every late-round candidate scores negative). Both are
deliberate, and neither discriminates by position.

*Defensible, and worth saying to the owner:* with Embiid ▲ and JJJ ▲ both
carrying injury-risk tags, a backup center is real insurance. The Top-5 is
not obviously wrong here.

### The TARGET line IS defective

`archetypeRead()` picks the family with:

```js
let fam = scarceFam || imbalance || (domOK ? domFam : null);
```

- `scarceFam` — roster-aware (requires an open lineup slot for that family, or
  zero rostered, or an existing imbalance). **Off here:** `unfilledSlots()`
  returns `[]`.
- `imbalance` — roster-aware (family below its startable floor, `G:3 F:3 C:2`).
  **Off here:** C is at 5, floor 2.
- `domFam` — **purely board-shaped**: whichever family holds ≥4 of the top-8
  available players. **No roster-need check whatsoever.**

With both roster-aware branches off, the family can only have come from
`domFam` — i.e. the label said "C" because the *board* was center-heavy, not
because the roster needed a center. The line then renders under the word
**TARGET**, which reads as a prescription.

## How often this fires

Every owner turn of mocks 27/28/29 (the three most recent graded drafts),
re-derived from the shipped engine:

| | count |
|---|---|
| Turns where TARGET produced a family | 32 |
| …of those, family came from the `domFam` fallback alone | 18 |
| …**of those, the family was already at/above floor with no open slot** | **12** |

**12 of 32 TARGET lines (38%) name a family the roster demonstrably does not
need.** Examples: m28 #149 said "G" with 6 guards rostered; m27 #148 said "G"
with 5; m29 #139 said "F" with 5.

This is not a scoring error — no pick ordering changes — but it is a
*prescriptive-sounding line making a false claim about roster need*, and the
owner read it exactly as intended-to-be-read.

## Two candidate fixes (neither shipped — freeze + owner decision)

**Option A — relabel (display-only, zero blast radius on picks).** When the
family comes from `domFam` with no roster need, the line is descriptive, so
say so: render `BOARD LEAN: Rim-protecting C` instead of `TARGET:`. The
docstring already describes the label as "a compression of what the board is
already recommending" — this makes the UI match the documented intent.

**Option B — gate the fallback (logic change in `archetypeRead`).**

```js
const domNeed = domOK &&
  (balCt[domFam] < FLOOR[domFam] || openFams.includes(domFam));
let fam = scarceFam || imbalance || (domNeed ? domFam : null);
```

Suppresses the family component when the roster is already covered; the
category term (e.g. "Rim-protecting") still renders where coherent, and the
coherence gate already handles the empty case. Larger blast radius: it
silences the family half of ~12 of 32 late-draft TARGET lines and would need
re-running the 130-state gauntlet plus the ledger replays.

**Recommendation: Option A now** — it is display-only, it makes a false claim
true, and it is exactly the class the freeze permits. Option B is a genuine
behavior change and belongs in September with a measured bar.

## Registered

- **E12** — TARGET family-need gate (Option B), measured against the ledger
  replays, with the requirement that no TARGET line which *was* load-bearing
  (the m22 Markkanen structural transfer, the m23 repair pleas) goes silent.
