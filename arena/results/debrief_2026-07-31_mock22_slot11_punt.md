# Mock 22 post-mortem — slot 11, the first declared-punt draft: G1a confirmed live (2026-07-31)

Completed 13-round mock (156/156, Kuzma/Bailey/Simons all resolve) with a
DECLARED 3-cat punt: **REB + BLK + FG%**. First punt-active draft in the
ledger — and the first production outing for the audit's punt-mode fixes.
Replay run TWICE (punt-on and punt-off cards — the state file doesn't
record when the punt was declared; grading below uses punt-off for R1–2
and punt-on from R3, disclosed); seasons 6,000 × 3; two CFs 6,000 × 2.

## Outcome — worst result ever measured

| Metric | Mock 22 (slot 11, punt) | Ledger context |
|---|---|---|
| Champ% | **0.22 (11th/12)** | m21 the day before: 26.73, 1st |
| Playoff% | **6.9** | worst measured |
| Kept-total | −5.47 (9th) | |
| 🎯 hits (hybrid grading) | 7/13 | adherence was fine — structure wasn't |

Roster: Ant, Cade, Trae, OG, Coby, Markkanen, LeBron, Quickley,
Knueppel, Jabari, DLo, Kuzma, Simons. Zero true centers; the two C
slots are legal only via Markkanen and Jabari (both PF,C) — zero slack.

## The punt did exactly what it promised — and lost anyway

The punted build delivered its own categories at the highest levels ever
recorded here: **3PTM 1st (+9.94z), FT% 1st, AST 2nd, PTS 3rd**. But
conceding all three big-man cats meant rostering no bigs, and the stocks
rode along: **ST 11th and TO 8th collapsed as collateral**. Final shape:
five effectively-lost categories (REB/BLK/FG% 12th, ST 11th, TO 8th) —
a weekly ceiling of 4–5 that no strength elsewhere can raise. This is
the G1a mechanism (every punt-declaring policy −4.9 to −11.2pp, CRN)
confirmed live at owner scale.

**The honest nuance:** `punt_ft_to` finished 3rd in this very room
(15.6%) on a kept-total of −11.7. Narrow 2-cat punts that keep big
coverage are survivable when drafted coherently from pick 1. The killer
here was the SHAPE of this punt — REB+BLK+FG% is the entire big-man
archetype, and forfeiting it forfeits steals and turnovers with it.
Doctrine unchanged and now owner-tested: soft punt (stop paying
premiums) yes; declared punts no; three-cat big-side punts never.

## Counterfactuals — no pick could have saved it

| Line | Champ% | Playoff% |
|---|---|---|
| As drafted | 0.23 (11th) | 7.1 |
| CF1 — deep deviations → punt-🎯s (LeBron→Poole #83, Jabari→Grimes #110, Kuzma→Caruso #134) | **0.03 (12th)** | 0.9 |
| CF2 — LeBron→Naz Reid (the TARGET's urgent C plea, gap 3.72) | 0.27 (11th) | 9.4 |

CF1 is the sharpest lesson of the pair: following the punt-coherent card
HARDER made things worse — within a doomed structure, better coherence
just digs faster. The deep-deviation law (board-20+ reaches, previously
0-for-4) is hereby scoped: it operates WITHIN a sound structure; it
cannot rescue an unsound one. The structure decision was worth ~±25pp;
every within-structure pick decision combined was worth <2.5.

## Card v4 in punt mode — instrument notes

- **Audit fixes held in production:** across all 11 panel states, zero
  punted-cat leaks anywhere (Strengths/Winnable/Weaknesses/Soft punt);
  Soft punt advised only kept cats (TO · FT%+TO · ST); Winnable rendered
  "—" throughout — correct by design with 6 kept cats fully consumed by
  the strengths/weakness trios.
- **First wild 🎯-transfer:** the urgent structural TARGET carried the
  🎯 to Markkanen at #59 and #62 ("best C in reach — act now, shelf 2");
  the owner converted at #62 at zero cost. The pinned-TARGET plea then
  ran the rest of the draft (Naz Reid, Jabari) and was never truly
  answered — the panel saw the structural failure coming from R5.
- **New punt-mode chip caveat:** BUY NOW gone-rate fell to **54%**
  (vs 83–91% in normal mocks) and quiet-survival rose to 82% — the deck
  prices urgency punt-coherently but the ROOM isn't punting, so your
  targets systematically outlive the market model. In a punt build,
  treat BUY NOW as softer and quiet as safer than their normal-mode
  calibrations.

## Ledger after 12 graded mocks

m21 and m22, drafted a day apart, are the doctrine's two poles: the
26.73% draft followed the card inside a sound value structure; the 0.22%
draft executed near-perfect punt coherence inside an unsound one. The
system's hierarchy is now measured end-to-end: **structure ≫ price ≫
name.** The deck's job in September is to keep the owner out of
structurally dead builds (it tried: the TARGET row and Soft punt both
flagged this one from mid-draft) — and the owner's job is to let it.
