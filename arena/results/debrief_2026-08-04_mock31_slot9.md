# Mock 31 debrief — slot 9, declared triple punt (FT% / 3PM / TO)

Owner-uploaded state (`arena/data/states/draft_state_mock31.json`), analyzed
2026-08-04. Every number here regenerates from
`python3 arena/mocks/season_sim_mock31.py` →
`arena/results/season_sim_mock31_out.json` — the first harness written
repo-relative under LESSONS.md lesson 13 (no machine paths, no scratch
outputs). 18,000 simulated seasons (6,000 × seeds 11/23/47).

## Headline

| Metric | Value | Rank |
|---|---|---|
| Champ% | **6.16** (per-seed 5.77 / 6.37 / 6.33) | 5 of 12 |
| Playoff% | 59.4 | — |
| ECW (expected cats won/week) | 4.610 | 5 of 12 |
| Kept-total, all 9 cats | −12.14 | **12 of 12** |
| Kept-total under the declared punt | **+23.50** | **1 of 12, by 16 z** |

The spread between the last two rows is the whole story: this roster is the
worst 9-cat team in the room and by far the best 6-cat team. Execution of
the declared build was near-total — per-cat ranks 1/1/1/3/3/4 in the six
kept categories (FG%, REB, AST, PTS, BLK, ST) and 12/12/12 in the three
punted ones. Room winners: slot 5 (SGA/J.Williams/Giddey/OG core, 32.2%),
slot 2 (Jokić/Dame/Mobley, 26.9%).

## Verdict on the strategy (before the picks)

A triple punt caps the weekly ceiling at 6 cats: winning a week 5–4
requires taking five of six kept cats against *every* opponent — an ~83%
weekly hit rate with zero slack for variance. That is why a +23.5 kept
monster converts to only 4.61 ECW (the 4.5 line is a coin flip) and 6%
champ. The house evidence stack all points the same way: every
punt-*declaring* policy the arena has tested cost −5 to −11pp; the
clear-path rule demands ≥70% of kept cats winnable before committing; the
owner's own brief bounds punting at 1–2 cats; and the direct precedent —
**mock 22, the last declared 3-cat punt, finished 0.22%, 11th**. Mock 31
ran the same handicapped strategy ~28× better (6.16%, 5th), which is
simultaneously impressive drafting and evidence the ceiling is the
strategy, not the drafter. Dropping ONE punt (most plausibly TO, keeping a
FT%+3PM double punt around this exact anchor core) re-opens 7-cat weeks
while keeping Giannis/Zion/Sengun value intact.

## Decision ledger (kept-z under the declared punt; alternatives are from
the players actually still available at that pick — pickwise reads, not
compounded counterfactual sims; no E11 placebo arms were run)

| Pick | Took | kept-z | Best available punt-fit | Δ | Read |
|---|---|---|---|---|---|
| 9 | KAT (bal-rank 6, punt-rank 13) | +4.2 | **Giannis +9.2** | −5.0 | Drafted the balanced board, not the build. Giannis luckily survived to 16 anyway, so the net cost compressed to ~1 z — but the process miss is real: under a declared punt, P9 is Giannis/AD, not the room's consensus star. |
| 16 | Giannis | +9.2 | (was the best) | 0 | Correct — the build's anchor. |
| 33 | **Trae Young** (bal 65, punt 48) | **+0.7** | **Dyson Daniels +5.1** | **−4.4** | The draft's biggest leak. Trae's value lives in 3PM/FT% (both punted) and he keeps only bad FG%; Dyson is the perfect triple-punt guard (STL/FG%, no 3PM dependence). Wrong player for *any* lens: below his own balanced rank too. |
| 40 | Cooper Flagg | +1.9 | Amen Thompson +4.7 | −2.8 | Amen is this build's dream wing (elite STL/REB/FG%, no 3s, bad FT% made free). Flagg defensible on upside, anti-fit on math. |
| 57 | Šengūn | +3.8 | Zion +3.9 | ≈0 | Fine — and Zion was taken next pick anyway. |
| 64 | Zion | +3.9 | (best available) | 0 | Correct. |
| 81 | Banchero | +1.4 | Kessler +2.7 | −1.3 | Moderate leak; Kessler's BLK/FG% fits tighter. |
| 88 | **Dylan Harper** | **−1.3** | Duren +2.4 | −3.7 | Negative kept-z: under this punt he subtracts. Rookie-upside thesis collides with build math. |
| 105 | **Darryn Peterson** | **−2.1** | Gobert +1.9 | −4.0 | Same shape, worse. Two elite punt-fit centers (Duren, Gobert) sat on the board through both picks. |
| 112–136 | Clingan / Ausar / Claxton | +1.2/+0.5/+0.6 | ≈best each time | ≈0 | Clean tail — exactly the right archetypes. |
| 153 | Isaiah Collier | −1.5 | (nothing meaningful left) | ≈0 | Dart throw, fine. |

Pickwise total left on the board ≈ **16 kept-z** — against the +23.5
achieved, a fully card-disciplined version of this same build plausibly
lands near +40 kept and pushes the champ% materially (unquantified —
running that counterfactual properly needs E11 placebo arms).

## Instrument caveats (all three known, none fixed today by design)

1. Sim still runs the shipped 6-team-bye playoff format; E14 (real 8-team,
   no byes, weeks 19–21) lands at the September re-baseline — measured −4
   to −6pp for elite rosters, likely mildly favorable to mid-tier seeds
   like this one.
2. The weekly variance constants are the unfit hand-set ones (self-critique
   N1). A triple-punt build's ECW is *unusually* sensitive to per-category
   variance dials, so 6.16% carries a wider error bar than a balanced
   build's number would. The owner's real 2025-26 weekly data
   (`arena/data/weekly_matchups_2025-26.csv`) now exists to fix this.
3. Mock-room texture carries ~0.45× of real Yahoo board divergence (E18
   bar note), and this state file contains **no E18 seat map** — opponents
   are unnamed personas here, so no per-manager reads.

## Lessons

- **L-m31a:** A declared triple punt converts elite kept-value into
  mediocre win probability by construction (6-cat ceiling, 5-of-6 weekly
  requirement). The kept-total lens (+23.5, rank 1) actively flatters it —
  ECW (4.61, rank 5) is the honest metric, exactly the E8 finding.
- **L-m31b:** The recurring in-draft failure shape was *lens-switching*:
  three picks (KAT, Trae, Flagg) were taken off the balanced/market lens
  inside a declared-punt draft. The card's punt-aware ranking exists to
  prevent precisely this; following it pickwise was worth ~16 kept-z.
- **L-m31c:** Rookie guards and a triple punt are structurally
  incompatible in redraft (negative kept-z at picks 88/105 while elite
  punt-fit centers waited). Rookie TO being punt-free is real but only
  pays for rookies whose *kept* production is positive.
