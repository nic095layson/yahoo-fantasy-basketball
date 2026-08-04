# Mock 15 post-mortem — slot 7, first draft with the 🎯 layer live (2026-07-30)

Completed 13-round mock (156/156, all names resolve incl. Simons/
Wilson/Collier/Sexton). Third mock on the codified deck; the slot-1–3
gradient ordering was NOT active (slot 7); the 🎯 confidence display
was live on every card. Standard harnesses; seasons 6,000 × 3;
counterfactuals 6,000 × 2.

## Outcome

| Metric | Mock 15 (slot 7) | m13 (s6) | m14 (s11) |
|---|---|---|---|
| Champ% | **2.06 (8th/12)** | 13.39 (co-2nd) | 5.76 (6th) |
| Playoff% | 30.9 | 77.7 | 53.5 |
| Kept-total | −0.78 (10th) | +0.04 (10th) | −1.20 (10th) |
| Shape | **flattest yet: nothing above rank 5; ST 11th, REB 9th; neither premium lever won** | aligned | half-aligned |

Roster: Haliburton, Curry, JJJ, Brunson, Turner, Duren, Mikal, Powell,
Edey, DeRozan, Harper, Caleb Wilson, Simons. Drafted at a +3.0 mean
premium (second net-premium mock); Caleb Wilson +53 is the largest
owner reach of any graded draft. `punt = []`, seventh straight.

## The finding: 🎯 is a scalpel, not an autopilot — and now we know both edges

🎯-top adherence was 3/13. Counterfactuals:

| Line | Champ% | Finish |
|---|---|---|
| As drafted | 2.13 | 8th–9th |
| Follow the 🎯 top at the 4 biggest divergences (Okongwu/Hartenstein/Monk/Jrue) | **0.19** | **11th** |
| Okongwu swap alone | 2.07 | 8th–9th (playoff +4.6) |

**Greedy gradient-following from a mid seat made things much worse.**
The mechanism is now clear from both directions: the gradient patches
the currently-weakest category each turn, so followed wholesale on a
shapeless roster it spreads value across all nine cats — manufacturing
exactly the flat profile that loses (this mock: nothing above rank 5).
Mock 14 showed the opposite edge: pointed at ONE hole in a committed
build, 🎯 flagged the +3.9pp repair the composite buried.

This triangulates cleanly with the arena evidence: gradient ordering
confirmed +12.7pp from slots 1–3 (elite anchor = built-in commitment to
shape around) and inconclusive-to-negative elsewhere. The slot gate is
validated from the failure side; the deck tooltip now states the
boundary explicitly (diagnostic from mid seats, order only at 1–3).

**The constant beneath all six graded mocks: commitment wins.** Shaped
builds: co-2nd, 3rd, 2nd. Flat builds: 7th, 8th, 10th-with-4-cats. The
punt declaration remains the commitment device the engine already
supports — `weight(c)` re-aims BOTH the composite and the gradient —
and it has now been unused in seven straight mocks while being the
difference between 2nd and 8th.

## Chip scorecard

- **CAN WAIT: 0/16 (0%) — the worst room ever measured** (massacre
  cluster now 4 of 6 rooms). Every C-shelf card was swept on contact.
- **BUY NOW: 27/29 (93%)**; both misses survived to be available later.
- **Scarcity invariant: clean** — 35 chips, 156 states, 0 violations.
- **Snipers: 16/16 value personas — all-time 120/121.**

## Room notes

`stars` won at 22.5% (best board +4.16 AND a committed top-heavy
shape — when value and shape agree, it's a monster); `bpa_pure` 0.01%
dead last for the third straight room. RJ Barrett +112 remains the
market model's favorite reach donor.

## Registered follow-up (display, no engine change)

A "commitment meter" candidate: when `punt = []` and the roster is
past R4 with no category above ~5th projected, surface a nudge chip
("no declared shape — flat builds grade 7th–10th; declare a punt to
re-aim"). Cheap, display-only, directly evidence-backed by six mocks.
