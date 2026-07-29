# Mock 10 post-mortem — slot 4, first draft on the market-timing deck (2026-07-29)

Completed 13-round mock (156/156 picks) against the deck's 11 personalities —
the first draft taken AFTER the BUY/WAIT verdict chips, wait-chain ladder,
val-default sort, and the scarcity-override fix shipped. Replayed headlessly
through the deck's exact shipped blocks (fixcheck harness pattern); season
outcomes from unmodified `arena.simulate_seasons` on the live
`data/players.csv` pool, 6,000 seasons × 3 seeds (18,000 total). Verified by
a 4-agent workflow: three analysts + one adversarial gauntlet that
independently re-derived every load-bearing number (fresh harness, fresh
arena run at seed 101) — **all checks CONFIRMED, zero refutations**.

## Outcome

| Metric | Mock 10 (slot 4) | Prior slot-3 | Prior slot-8 |
|---|---|---|---|
| Champ% | **12.11 (3rd/12)** | 22.48 (2nd) | 0.23 (12th) |
| Playoff% | 67.1 | 89.7 | 10.8 |
| Kept-total | +23.57 (2nd-best board) | +26.8 (best) | +19.3 (3rd-worst) |
| Shape | offense/efficiency, defense conceded undeclared | balanced | uncommitted triple-punt |

Rank 3 replicated independently in all three seeds (11.90/12.47/11.97).
Room won by slot 12 `punt_ft_to` (20.65%) over slot 6 `stars` (16.61%).
Gap to 4th (10.84%) is 1.3pp — under the arena's ~2pp trust threshold, so
read it as "solid 3rd, could be 3rd-4th."

Roster: Doncic, Tatum, Jamal Murray, Brunson, Brandon Miller, Duren, MPJ,
Gafford, Norman Powell, John Collins, Nesmith, Jrue, McCain.

## Adherence and timing behavior

12/13 picks on-card, 7/13 the card's #1. The owner drafted **-4.8 mean
delta vs board rank** (10/13 picks at a value discount; room mean +1.1)
and landed the single biggest steal of the draft: MPJ at #76, board #63.

The chips were *used*, not just displayed — twice the owner ran a card as a
two-turn plan: R6 took Duren (his own ladder's #76 step, banked a round
early) then collected MPJ at #76 when MPJ's ~11% BUY NOW busted in his
favor; R12 took Jrue, then McCain at #148 after McCain's ~15% call
survived. The Gafford decision (R8 #93, chip said CAN WAIT ~99% to #100,
ladder said #117) split the difference against prior-mock history — mocks
5–9 had him sniped at 93–104, so #100 was probably safe (4/5) but the
ladder's #117 plan fails 5/5. Cost of grabbing early: the card's #1 BUY
NOW Naz Reid (~25%), gone at #99 exactly as the chip priced.

## The one bad turn

R5 (#52): off-card Brandon Miller (composite #9, only 0.14 behind card #5)
over a card of Porzingis BUY NOW ~16% + four CAN WAITs. **All five card
players were gone within 10 picks** (Kessler #53, Porzingis #54, Poeltl
#55, Turner #57, Bam #62) — the standing mock banner's warning made flesh.
That turn alone converted the deck's C plan into the Duren/Gafford
salvage path.

## Chip scorecard (first post-fix mock)

- **CAN WAIT: 8/14 survived (57%)** vs 41% pooled baseline — the
  survivable cluster (m5 67%, m7 59%, m8 57%), not the massacre cluster
  (m6 6%, m9 8%).
- **BUY NOW: 25/30 justified (83%)** vs 91% baseline. All 5 misses were
  extreme calls (~1–19%) on players this value room deprioritizes — and 3
  of the 5 the owner banked at his next turn, so the misses were mostly
  *profitable*.
- **Scarcity invariant holds**: 32 scarcity chips across all 156 board
  states, 0 outside the price window, 0 on a dead shelf. Both owner-turn
  scarcity BUY NOWs (Sabonis/JJJ at #21) were in-window on a live shelf
  of 2 — though both survived to #28: in this room the scarcity bell rang
  one turn early.
- **Snipers: 6/6 failed WAITs killed by value personas, 0 by the two
  market seats** — the streak is now 52/52 across six mocks. The
  wait-math's enemy in mock rooms remains the value bots, exactly as the
  standing banner says.
- Ladder promise busted once more: R3's "your #45: Okongwu ~99%" died at
  #42 (slot 7). Okongwu never appeared on an owner card in this draft —
  the ladder was his only offer.

## The finding: value accumulated, shape never declared

Cat profile: 3PTM 3rd, PTS 4th, FT% 4th vs **ST 12th, BLK 11th, REB 9th**
— with `punt = []`. That is an undeclared triple concession of the
defensive stats, the same disease as the slot-8 uncommitted punt, in a
milder strain. It is what caps the league's 2nd-best value board (+23.57)
at 12% champ while a committed double-punt (`punt_ft_to`, kept-total just
+13.5) wins the room at 20.65%. Third straight post-mortem where shape
commitment beat value accumulation.

**Actionable**: next mock, declare the punt in the deck by R4 (ST or
ST+BLK given this board's drift) and let TARGET/fit re-aim the mid-rounds
— or deliberately buy the defensive shelf (the R5 card WAS that shelf:
Porzingis/Poeltl/Turner/Bam/Kessler).

## Room value flow

Steals: MPJ -13 (owner), Suggs/Mikal/Hart/McDaniels -11. Reaches: RJ
Barrett +108 and Kuzma +85 (both slot 1 market), Banchero/Keyonte +56,
Zion +48. Persona means: value bots -5.4..-6.8, punt seats +5.9/+7.3,
points_chaser +9.2, market +16.5 — the market seats systematically
overpay vs this board, which is why they never snipe a WAIT.
