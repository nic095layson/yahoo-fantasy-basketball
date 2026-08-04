# Mock post-mortem — slot-3 and slot-8 deck drafts (2026-07-27)

Two completed 13-round mocks against the deck's 11 personalities, replayed
headlessly through the deck's EXACT engine (scratchpad harness drives
`strategyScores`/`archetypeRead`/`fitWeights` + the app's judgment/slide
pipeline verbatim). Season outcomes from `arena.simulate_seasons`, 6,000
seasons × 3 seeds each. Gauntlet: 5 adversarial verifiers over the
load-bearing claims (1 count corrected: urgent-C calls were 6, not 5).

## Outcomes

| Draft | Champ% | Playoff% | Kept-total | Shape |
|---|---|---|---|---|
| slot 3 | 22.48 (2nd/12, co-favorite) | 89.7 | +26.8 (league best) | balanced, REB conceded |
| slot 8 | 0.23 (12th/12) | 10.8 | +19.3 (3rd worst) | UNCOMMITTED triple-punt (REB 12th, BLK 10th, FG% 9th) |

## The compliance paradox (the finding)

Slot 8: the drafter followed the **Top 5 card in 12 of 13 picks** — and
finished dead last. TARGET called **family C in 8 of 13 rounds, urgent in
6 (r3, r6, r7, r11, r12, r13)** — and only ONE center ever appeared as a
Top-5 #1 (Vučević, r8, passed for Herb Jones by Δfs 0.16). The tool's two
channels pointed opposite directions; the drafter followed the prominent
one; the season simulation says the quiet one was right.

Slot 3: Top-5 compliance 10/13, but the drafter ANSWERED the C call three
times (r9 Naz Reid cnc#1; r10 Sarr cnc#46; r11 Lively cnc#24 — the latter
two at real council-score cost) — and that roster hit co-favorite.
Suggestive, not causal (n=2); the causal test is an arena experiment.

## Why the channels diverge (from code, not vibes)

- **Top 5** ranks by fs = matrix-weighted z × availability + need(0.3×fills)
  − stack(0.5) ± judgment ± slide-bonus, bench-bound ×0.15. It answers
  "who adds most value THIS pick." Its positional need bonus (~0.3–0.45)
  cannot bridge the 0.5–1.5z gaps to remaining bigs, so late-draft C
  candidates never crack it.
- **TARGET** compresses the fit-z top-8 with a scarcity override. The
  URGENT ("act now") calls fire when ≤2 of a family remain inside the
  market's next-two-rounds window; non-urgent family calls come from the
  fallback chain (below-floor imbalance → top-8 dominance) — gauntlet
  scope caveat: 9 of 15 C-calls across both replays were shelf-driven,
  6 were fallback. Either way it answers "what won't survive / what the
  build needs," and the council score contains NO market-window term
  (scarcity_w=0 for council).
- **Fairness note (gauntlet)**: the dual-metric Top-5 design is disclosed
  — the title says "ranked by council + judgment + value · showing FIT Z"
  and fs lives in the hover tooltip. Disclosed ≠ usable on a 45-second
  clock; the defect is decision-aid design, not honesty.
- **Fit column** (Best Available default sort) = swing-weighted z, no
  judgment/slide/need/stack/bench. Pool players can legitimately out-Fit
  Top-5 members — and the Top-5 card *displays* fit z while *ranking* by
  fs ("showing FIT Z" title on a non-fit-ordered list).


## Which C did TARGET mean (slot 8, urgent turns; deck's own numbers)

| Rnd | You took | Best C by fit (fs) | Top-5 #1 (fs) | Obey cost |
|---|---|---|---|---|
| 3 | Booker | Markkanen (2.72) | Bane (4.53) | −1.81 — too early, correctly skipped |
| 6 | Embiid (fs 0.41) | **Brook Lopez (0.91)** | LaVine (2.18) | −1.27 — right family, wrong instance |
| 7 | Siakam | **Naz Reid (0.54)** | Bridges (2.46) | −1.92 — the last real window |
| 11 | Ellis | Aldama (−0.92) | Ellis (0.20) | shelf already dead |
| 12 | Caruso | W. Carter (−1.41) | Caruso (0.23) | shelf dead |
| 13 | Dosunmu | Queen (−1.74) | Dosunmu (−0.28) | shelf dead |

Two additional findings this table exposes: **(a) urgency doesn't decay**
— TARGET kept flashing "act now" at r11–13 when every remaining C was
negative value (ringing the bell after the fire); urgency should gate on
the best family candidate clearing an fs floor. **(b)** The real
championship-saving sequence per the tool's own numbers was r6 Lopez +
r7 Naz Reid — a ~3.2z council-value sacrifice across two picks to avoid
the −22pp championship structure. Neither channel prices that exchange
rate; that is exactly the arena experiment the council queued.

## Council verdict (5–0)

Ship two surfacing fixes, zero math changes: (1) pinned TARGET row in the
Top 5 when the flagged family is absent — best fit-z candidate of that
family with fs + shelf count; (2) display fs as the labeled ranking number,
fit z secondary, honest title. Queue the real reconciliation — an
urgency-scaled scarcity bonus inside fs — as an ARENA EXPERIMENT behind
the codify gate (precedent: the punt-gate study measured an intuitive
knob at −5.8 to −6.6% relative championship output).

## Drafting rules pending the tool fix

1. ⚠ TARGET ("act now") + no matching family in Top 5 → click TARGET
   (it filters Best Available to the family by fit); take the top name
   unless its fs deficit to the Top-5 #1 exceeds ~0.5.
2. Small Δfs (<0.25, the coin-flip band) NEVER outranks an urgent shelf call.
3. Three cats at rank ≥9 with no punt adopted = the slot-8 death shape;
   the Drift line is the alarm — act on it by the next pick.
