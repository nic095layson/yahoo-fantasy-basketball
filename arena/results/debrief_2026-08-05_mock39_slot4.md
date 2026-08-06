# Mock 39 debrief — slot 4, declared punt FT%/3PTM/TO (2026-08-05)

State: `arena/data/states/draft_state_mock39.json` (upload md5 55a82c64).
Regenerate: `python3 arena/mocks/season_sim_mock39.py` →
`arena/results/season_sim_mock39_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Per-turn replay: `arena/results/m39_replay.json`. Same
instrument caveats as mocks 31–38.

## Headline — NEW BEST OWNER BUILD EVER, within 0.6pp of the oracle

| Metric | Value | Rank | Prior best |
|---|---|---|---|
| Champ% | **33.98** (34.22/33.90/33.83 per-seed) | **1 of 12** | 31.18 (m36) |
| Playoff% | 94.0 | 1 | 94.4 (m25) — still the record |
| ECW/week | **4.99** | 1 | — (2nd ever ≥ 4.90) |
| Kept-z under declared punt | **+26.84** | 1 | +26.65 (m37) |
| Kept-total, 9 cats | **−2.23** | **10** | — |

Next-best seat: 13.00% — a 2.6× gap, the most dominant owner room ever.
The only higher number in the entire ledger is the m28 hindsight oracle
(34.58), which has perfect draft-order foresight. This is a real draft
0.6pp under the oracle's ceiling.

Roster: Luka, Giannis, Trae, Amen Thompson, Sengun, Eason, Jarrett
Allen, Duren, Ausar, Ryan Rollins, Coulibaly, Gafford, RJ Barrett.

## The yardstick split, taken to its limit

Kept-total (9-cat) ranks this roster **10 of 12** (−2.23). The sim
prices it as the best owner build ever measured. That is the m37 split
(7-vs-3) stretched to its extreme — and the final burial of raw 9-cat
kept-total as a quality metric for punted builds. ECW (rank 1, 4.99,
above the winners' bar) tracks the sim; kept-total does not. E23's
September work should treat ECW as the only headline yardstick.

## Fourth straight optimal declaration — and the hardest punt ever played

FT%/3PTM/TO is the **#1 punt of all 84** for this roster (+26.85; #2 is
+22.57, not close) — after m35, m37, m38, that is FOUR consecutive
optimal declarations. New all-time punt-frame kept-z record (+26.84,
prior m37 +26.65). And the concession is real and enormous: FT% −15.2
(deepest single-cat sink ever logged), 3PTM −10.2, both rank 12; TO −3.7.

All six kept cats positive — the second fully-live kept frame (after
m37), now with TWO rank-1 categories: FG% +9.63 (1), REB +6.87 (1),
ST +4.25 (3), AST +3.06 (4), BLK +2.45 (2), PTS +0.59 (8, thin but
alive). Six live cats in a 5-of-9 game with two near-locks is exactly
what ECW 4.99 says it is.

## Card grading — the m36 playbook, run inside a hard punt

Exact card #1 at 6/13 (Luka R1, Amen R4, Eason R6, Duren R8, Rollins
R10, Gafford R12), in Top-5 9/13. The four off-card picks are the
m36 star-injection pattern fused with m38's punt-fit logic:

- R2 **Giannis** (card: Mobley) and R5 **Sengun** (card: Okongwu) —
  the same two star injections m36 made, both elite-usage bigs whose
  bad FT% rides free under this punt.
- R3 **Trae** (card: D. White) — elite AST/usage with horrid FT%: a
  pure punt-fit star unavailable to a punt-blind card.
- R13 **RJ Barrett** (card: Ellis) — low-cost volume wing, same frame.

m36 proved card-spine + stars; m37 proved the hard punt; m38 fused them
in a flat room; m39 is the fusion at full power: same declared punt
family as m36/m37, played all the way down (FT% −15.2 vs m36's never-
bound TO punt), and the sim prices it above every build in the ledger.

## Read for October

The punted-lane learning curve across four drafts: m35 6th → m37 3rd →
m38 1st (flat room) → m39 1st at 33.98 with ECW 4.99. The doctrine
holds and sharpens: declare the punt the roster wants (four straight #1
of 84), keep every kept cat alive (twice now), follow the card's spine
in the middle rounds, and spend early deviations on punt-fit stars the
punt-blind card can't see. Joins the punted screening set (E21, now
nine: 22, 31, 32, 34, 35, 36, 37, 38, 39).

## LEDGER row

`| 39 | 4 | 33.98 | 94.0 | 1 | 12 | ECW 4.99 — **NEW BEST OWNER BUILD
EVER** (prior m36 31.18; 0.6pp under the m28 oracle; next seat 13.00, a
2.6× gap). FOURTH straight optimal declaration: FT%/3PTM/TO is #1 of 84
(+26.84, new punt-frame record, prior m37 +26.65) and played to the
floor (FT% −15.2 deepest sink ever, 3PTM −10.2). All six kept cats
positive incl. two rank-1 (FG%, REB). Kept-total(9cat) ranks 10 vs champ
rank 1 — the yardstick split at its limit; ECW is the yardstick. Card
exact-#1 6/13; off-card = punt-fit stars (Giannis, Trae, Sengun, RJ)
(`season_sim_mock39.py`, `m39_replay.json`) |`
