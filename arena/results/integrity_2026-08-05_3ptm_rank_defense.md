# Integrity defense — the 3PTM rank in draft_state_24 (2026-08-05)

**Owner's challenge:** "I ranked 10th in 3PMs, despite having the league's
top 3-point shooters in Curry, Trae, Klay, Tatum, Brunson… Doesn't seem
right to me — analyze and defend if this is indeed accurate."

**Verdict (Council 5–0): ACCURATE AND DEFENSIBLE — display defended, no
fix required.** The challenge did surface a real presentation gap, folded
into E23's September scope below.

State: slot 11, no punt, 156 picks (upload `dcac04b0-draft_state_24.json`).
Owner roster: Tatum, Curry, Brunson, Trae, Sengun, Turner, DeRozan, Duren,
Wallace, Camara, Gafford, Klay, Trent.

## Three independent instruments, same answer

| Instrument | Owner value | Rank |
|---|---|---|
| Deck's `categoryRanks` (13-man 3PTM z-sum — the displayed number) | +0.29 | **10 of 12** |
| Raw projected makes/game (no z, no model — pure counting) | 23.4 | **10 of 12** |
| Weekly H2H model (started lineup, availability-weighted) | 56.4 μ | **9 of 12** |

Display truth verified end-to-end: the state replayed through the live UI
(fake-DOM harness) renders the build read from the same `categoryRanks`
source ("REB 11/12, ST 10/12 — 3PTM also weak"). The chip is reporting
its own math faithfully, and the raw count confirms that math externally.
Note in the owner's favor that the chip does NOT apply Curry's and
Tatum's 0.78 injury availability — the honest weekly number is slightly
worse than displayed, not better.

## Why it feels wrong — two measured perception gaps

**1. The "top shooters" premise doesn't hold in this pool.** Pool 3PM/g
positions: Curry **#1** (4.3), Tatum **#9** (3.2) — then Trae **#41**
(2.4), Brunson **#40** (2.4), Klay **#46** (2.4), Trent #51 (2.3),
Turner #58 (2.2). One elite source, one very good one, five mid-tier.

**2. 3PM is a 13-man sum, and the zeros cancel the stars.** Boost/drag
decomposition:

- Owner positive 3PM z: **+6.93 — 2nd best in the room**
- Owner negative drag: **−6.64 — 2nd worst** (Duren −1.83, Gafford −1.83,
  Sengun −1.31, DeRozan −1.00, Wallace −0.39, Camara −0.29)
- Net: +0.29 → 10th.

The #1 team (T9) has a WEAKER top end (+4.87) but only **−0.47 drag** —
thirteen moderate shooters beat two elite ones. The owner's drag is the
price of his real strengths (TO rank 1, FG%/BLK top tier from the
Sengun/Turner/Duren/Gafford interior) — composition cost, not error.

**Context the rank hides:** the pack is compressed — 10th (23.4/g) is
1.3/g behind 4th (24.7); only T9 (+4.0) is meaningfully clear. And the
weekly lineup sort benches Klay and Trent (weight 0.15), so two of the
five named shooters barely count on game night.

## Bounds

- Projections are the standing single-source set (self-critique N3):
  Trae/Brunson/Klay at 2.4/g are conservative vs career norms. Sensitivity
  checked: even Trae at 3.0/g moves the owner only to ~6th in this pack —
  mid-table, not top-3. **Trae, Klay, Brunson added to the September
  projection cross-check list.**
- Weekly ranks remain simulator-conditional (N1) until the weekly-fit
  data lands in the model.

## Filed into E23's September scope (display-only, registered)

1. **Rank context:** show gap-to-pack beside category rank chips —
   "10th, −1.3/g to 4th" reads correctly; "10th" alone reads as a hole.
2. **Composition note:** boost/drag per category (+6.93/−6.64 here) —
   the single readout that would have answered this challenge at a glance,
   and the stars-vs-breadth warning the card never gave mid-draft.

Regeneration: `arena/data/states/` does not carry this state (integrity
check only, not a LEDGER post-mortem); the probes concatenate the deck's
extracted engine+data blocks with the drivers described above. If this
draft later gets a full debrief, land the state per lesson 13 then.
