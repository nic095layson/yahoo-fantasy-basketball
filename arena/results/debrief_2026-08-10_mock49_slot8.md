# Mock 49 debrief — Seat 8, declared punt FT%/3PTM (2026-08-10)

Standard room, v2 instrument, cast recorded. **First mock graded on the
245-row pool** (post 8/9–8/10 refresh and the main merge); seat baselines
remain 246-pool epoch, so seat-edges carry that caveat until the September
re-baseline. State: `arena/data/states/draft_state_mock49.json`.
Regenerate: `python3 arena/mocks/season_sim_mock49.py`. Replay:
`arena/results/m49_replay.json`.

## Headline — a room win, in the tightest winning room measured here

| Metric | Value | Rank |
|---|---|---|
| Champ% | **24.94** (24.72/25.33/24.77 per-seed) | **1 of 12** |
| Playoff% | 87.84 | 1 |
| ECW/week | 4.89 | 2 |
| Kept-z under declared punt | +21.42 | 1 |
| Kept-total, 9 cats | −1.41 | 8 |

Room: owner 24.94, then **Kyle 22.19 (Seat 2)** — a +2.75pp margin, with
Kyle running a balanced +6.84 nine-cat build that nearly matched a hard
two-cat punt. Then Robby 11.21, Cayas 10.46, Oblena 9.71, long tail.
Seat-edge **+21.74pp** over Seat 8's bot baseline (3.20) — 16th positive
edge in 17 rooms (246-pool-epoch baseline caveat).

Roster: AD, Giannis, Brunson, Trae, Sengun, Eason, Allen, Duren, Gobert,
Ausar, Jrue, Caruso, Coulibaly.

## Doctrine scorecard

1. **Optimal declaration** — FT%/3PTM is the **#1 frame of 36** (+21.42,
   nearly double the +11.76 runner-up). Tenth optimal declaration in
   twelve punted drafts.
2. **Genuinely played** — FT% −11.72 and 3PTM −11.11 both rank 12. No
   hedging.
3. **Kept cats** — THREE rank-1s (FG% +9.10, REB +5.84, BLK +3.41) plus
   ST rank 3. Two kept cats drifted negative: PTS −1.45 (rank 10) and TO
   −0.07 (rank 5). PTS was the natural third punt (best 3-frame
   FT%/3PTM/PTS at +22.87) and was left in — drift, not death, and the
   main gap to m48's 46.03 alongside the stronger room.
4. **AST protected** — rank 5 (+0.64) behind Brunson (R3), Trae (R4),
   Jrue (R11), Caruso (R13). The m44 refinement holds again: seven bigs
   never starved the backcourt cats.

## Card agreement — the m48 shape, replicated

Exact-#1 **7/13**, Top-5 8/13 — and the split is perfectly clean:

- **R1–R5, all off-card**: AD (card said KAT), Giannis (Jamal Murray),
  Brunson (Dyson Daniels), Trae (OG), Sengun (Eason). Every deviation a
  punt-fit star for the declared FT%/3PTM frame.
- **R6–R13, all exact-#1 except one**: Eason, Allen, Duren, Ausar,
  Coulibaly, Jrue, Caruso all the card's #1; Gobert (R9) a Top-5 take
  over Cason Wallace.

Judgment declared the frame and spent the early rounds inside it; the
card, punt-blind by design, supplied the entire back-half spine. That is
the doctrine in its written form, second consecutive execution.

## The lineup-cap question, measured on this build

Six C-eligibles (Giannis, AD, Sengun, Allen, Duren, Gobert) against a
C·C·Util·Util = 4 startable ceiling — the exact shape the owner flagged
on 2026-08-05. The daily-fill instrument says the ceiling **never
binds**: lowest start rate on the roster is Jrue 0.960, then Gobert
0.980; every other player ≥0.989. AD and Giannis flex to PF, so the four
C slots go to Sengun/Allen/Duren/Gobert on their game nights with no one
stranded. A cap warning that fires on eligibility alone would have cried
wolf here — the E22b display-only resolution (warn, never reorder)
continues to look right.

## The Zion sidebar (mid-draft question, now graded)

At pick #80 the owner asked why the card led with Allen while Zion showed
Fit +1.41. The live answer: ~3.7 of Zion's ~4.0 positive z sat in the
build's three locked cats while his FT% −3.23/TO −1.65 damaged live ones.
The owner took Allen (exact-#1). Zion went to Noah at #91; Seat 6
finished **10th at 2.57%**. One room, not causal — Noah's whole draft is
in that number — but the mirage-vs-measurement framing survived contact,
and it produced the ΔECW pool column shipped the same day.

## LEDGER row

Appended to `arena/results/LEDGER.md` §1 (row 49), quoting
`season_sim_mock49.py` and `m49_replay.json`.
