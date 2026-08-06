# Mock 40 room synergy + the bot-competence question (2026-08-06)

**Owner-directed:** "quick team synergy analysis of the other opponent
teams… name them using the 11 personalities… can you use this data to
train the 11 other manager bots to make their mock drafting prowess
stronger?" Data: `arena/data/states/draft_state_mock40.json`,
`season_sim_mock40_out.json` (v2 instrument, 18k seasons).

## 0. Attribution caveat and the fix (EVIDENCE)

The exported `draft_state.json` did NOT record which manager sat in which
seat — `engineState()` projected only teams/slot/size/punt/picks, so the
per-draft shuffled cast was lost at export. Seats below are attributed by
**loyalty-token fingerprint** (each personality carries named players it
reaches for), with confidence stated. **Fixed the same day:** the export
now carries `cast` in mock mode (additive; legacy fields unchanged; live
mode unaffected; ordering replay byte-identical). Future mocks are exact.

| Confidence | Basis | Seats |
|---|---|---|
| HIGH | 3 loyalty tokens | Martin T3, Robby T7, John T6 |
| MEDIUM | 2 tokens | Will T2, JCo T10 |
| LOW | 1 token | Kevin T9, Oblena T11, Noah T12, Hegi T8 |
| INFERRED | no tokens; split by noise signature | Cayas T1, Kyle T5 |

## 1. Room synergy table (v2 grading)

| Seat (attrib.) | Champ% | ECW | Shape G/F/C | Live cats | Its own best punt | Dead kept cats |
|---|---|---|---|---|---|---|
| **T4 OWNER** | **26.29** | 4.94 | 5/7/5 | **6** | 3PTM/FT%/TO (+14.8) | **0** |
| T2 Will | 15.86 | 4.76 | 7/9/3 | 4 | 3PTM/BLK/TO (+6.8) | 2 |
| T1 Cayas | 15.14 | 4.70 | 11/5/3 | 5 | AST/FG%/REB (+15.9) | 1 |
| T9 Kevin | 10.08 | 4.62 | 5/11/4 | 4 | 3PTM/FT%/ST (+4.5) | 2 |
| T7 Robby | 7.08 | 4.54 | 8/9/2 | 4 | BLK/ST/TO (+6.1) | 2 |
| T3 Martin | 6.71 | 4.49 | 11/5/3 | 4 | BLK/FG%/TO (+9.2) | 2 |
| T6 John | 5.38 | 4.45 | 6/9/4 | 4 | 3PTM/AST/PTS (+7.2) | 2 |
| T5 Kyle | 5.37 | 4.46 | 10/7/3 | 6 | AST/BLK/REB (+6.1) | **0** |
| T10 JCo | 3.53 | 4.39 | 8/4/6 | 4 | 3PTM/FT%/PTS (+21.2) | 2 |
| T8 Hegi | 2.13 | 4.27 | 11/7/2 | 4 | BLK/ST/TO (+8.0) | 2 |
| T11 Oblena | 1.68 | 4.25 | 6/5/4 | 4 | AST/BLK/REB (+11.9) | 2 |
| T12 Noah | 0.74 | 4.14 | 9/8/2 | 5 | BLK/FG%/TO (+17.8) | 1 |

Quick reads:
- **T1 Cayas** — the guard swarm (11 G-eligible). Coherent by accident:
  best frame AST/FG%/REB is worth +15.9 and he half-plays it, which is
  why the room's noisiest personality finishes 3rd.
- **T10 JCo** — the anti-owner. Holds the room's **highest punt potential
  (+21.2)** on a 6-center frame and converts it into 3.53%: the frame is
  right there and the roster never commits to it.
- **T12 Noah** — the widest category spread in the room (19.9) and the
  worst finish. Extreme shape with two kept cats underwater is the
  classic "punted by accident" build.
- **T5 Kyle** — the only bot with **zero dead kept cats**, yet 5.37%:
  balance without a strength wins nothing in a 5-of-9 format. The
  owner's build is balanced AND spiked (spread 9.98 with 6 live cats).

## 2. Where the bots are actually weak (EVIDENCE)

| Metric | 11 bots (mean) | Owner |
|---|---|---|
| Dead kept categories (under each team's own best frame) | **1.64** | **0** |
| Live categories (z > 0) | 4.36 | 6 |
| Category spread (max−min z) | 9.01 | 9.98 |
| Daily-fill lineup waste (v2 unstartable share) | 0.01–0.14 players | 0.03 |

**The bots' weakness is category coherence, not roster construction.**
Lineup waste is negligible for every seat (v2 says nobody stacked
unstartable players in this room), and their spreads are healthy. What
they lack is the discipline the owner has been demonstrating for five
straight drafts: **finish with every kept category alive.** They punt by
accident (1.64 dead cats each), so their shape is noise rather than a
frame — exactly the m34/m35 failure mode the owner learned to avoid.

## 3. Can this data "train" the bots? — the honest answer

**Yes, but there is a design tension that is the owner's call, not mine.**

These 11 bots exist to be *forecasts of specific humans*: their
parameters were fit to the real managers' actual draft histories (E18,
E18b — Spearman 0.952 against measured reach). Making them better
drafters makes the mock room **less predictive of the owner's real
October draft**: the board would clear differently than it actually will,
and the mocks would stop rehearsing the draft he is preparing for.

So there are two products, and they want opposite things:

| Goal | Room needed |
|---|---|
| **Rehearsal** — what will really happen on draft day | today's realistic cast (keep as default) |
| **Stress test** — is my build robust against sharp opposition? | a "sharp mode" variant of the same 11 |

**Recommendation: build sharp mode as an OPT-IN toggle, keep the fitted
cast as the default.** Additive, so realism is never silently traded away.

### Registered as E25 (measure-first, bar written before any run)

**Change under test:** a competence term in `managerScores` — late-round
picks (R8+) receive a bonus for categories where the bot is currently
within reach of the pack and a penalty for adding to an already-dead
category, i.e. an anti-dead-cat rule. Nothing else changes; ADP weights,
noise, and loyalty stay fitted (personality is preserved; only competence
moves).

**Bar (both prongs required to ship, even as an opt-in):**
1. **Sharp bots must actually be sharper** — across ≥6 fresh mock rooms,
   mean bot dead-kept-cats drops from 1.64 to ≤0.8 and mean bot ECW rises
   by ≥0.05/week.
2. **They must be harder opposition** — replaying the OWNER's identical
   mock-40 draft into a sharp room lowers his champ% by ≥3pp (if his
   number doesn't move, the bots got different, not better).
3. **Realism guard:** default mode's cast behavior must stay
   byte-identical (no accidental change to the fitted room), and the E18b
   Spearman reach gate must still pass in default mode.

**Not run tonight** — it needs fresh mock rooms generated by the deck's
own AI (a new harness), and the freeze rule says a behavioral change to
the room ships only after its bar clears. Say the word and I'll run it.

## 4. Bounds

- Seat attribution is fingerprint-based for mock 40 (§0); only the three
  HIGH rows are safe to quote as fact. All synergy metrics are
  seat-accurate regardless of the name attached.
- One room, one draft: the bots' 1.64 dead-cats mean is a mock-40
  measurement, not a fitted constant. E25's prong 1 re-measures it across
  ≥6 rooms before anything ships.
