# League intel — the owner's REAL league, 2025-26 season (ingested 2026-08-04)

Source: owner-provided screenshots and draft export (final standings, weekly
scoreboard, final rosters ×12, roster settings, full 13-round draft board).
This file is ground truth for the September recalibration and supersedes all
assumptions it contradicts. Owner's team: **JAMAL AL-QUETA**.

## 1. Confirmed settings

| Setting | Value | Tool's prior assumption |
|---|---|---|
| Teams | 12 | ✓ matched |
| Scoring | H2H each-category, 9-cat (162 = 18 wk × 9 cats, verified) | ✓ matched |
| Regular season | 18 weeks | ✓ matched (`WEEKS = 18`) |
| Lineup | PG SG G SF PF F C C Util Util | ✓ **exactly** `LINEUP_SLOTS` |
| Bench / IL | 3 BN + **2 IL+** | 3 BN ✓; **IL+ unmodeled** |
| **Playoffs** | **8 of 12 qualify, no byes** (8 asterisked; champion = 7th-best record) | ✗ **arena: 6 teams, seeds 1–2 byes** |
| Schedule | fixed rotation (7 opponents ×2, 4 ×1) | sim shuffles weekly — acceptable |

## 2. Final standings (regular-season record → playoff finish)

| Final | Team | Record | Pct | Moves |
|---|---|---|---|---|
| 1 🏆 | HalleLuka Amen | 78-82-2 | .488 | 50 |
| 2 | The Konclave | 89-72-1 | .553 | 83 |
| 3 | Wing Chun Wemby | 76-84-2 | .475 | 47 |
| 4 | IM SO HORT | 87-74-1 | .540 | 61 |
| 5 | John's Cool Team | 82-76-4 | .519 | 41 |
| **6** | **JAMAL AL-QUETA (owner)** | **103-58-1** | **.640** | 64 |
| 7 | ur my only hope Anti-wan | 82-79-1 | .509 | 74 |
| 8 | All guards no defense | 96-64-2 | .600 | 61 |
| 9–12 | Spida / SARR / Devin Minutes / Bamonte | .472/.466/.416/.323 | | 69/41/27/44 |

**The season's headline: the owner won the regular season by 6.5 games
(.640, best record) and finished 6th. The champion (.488, 7th-best record)
would not even have QUALIFIED under the arena's 6-team format.** The 8-seed
finished 3rd. The real league's title is three H2H weeks among eight teams.

## 3. Owner's weekly scoreboard (validation data)

Weekly cats won: 8,7,5,3,4,8,5,7,6,7,5,7,4,5,6,8,4,4 (sums exactly to
103-58-1; wk-1 tie). **Mean 5.72, sd 1.56, range 3–8.** The arena's weekly
model for a comparably strong team gives sd ≈ 1.40 — the variance engine is
in the right ballpark (~10% tight), the first real-world validation of the
instrument. Owner lost weeks 17–18 (both 4-5) then the QF: cooled at the
exact wrong time; no roster collapse visible.

## 4. Playoff-format delta (measured 2026-08-04, `arena/mocks/format_delta.py`)

Re-simulating ledger mocks under the REAL format (8 teams, no byes) vs the
shipped one (6 + byes), same seeds:

| Mock | Owner champ% 6-team → 8-team | Owner playoff% | Room-best champ% |
|---|---|---|---|
| 21 | 26.91 → **20.92** | 91.4 → 97.7 | 26.91 → 20.92 |
| 25 | 29.19 → **22.86** | 94.3 → 98.3 | 29.19 → 25.28 |
| 27 | 9.76 → 9.42 | 62.5 → 80.6 | 18.35 → 15.54 |
| 30 | 2.12 → **3.31** | 31.1 → 59.5 | 16.99 → 17.43 |

Reading: the real format taxes elite rosters ~4–6pp of champ%, hands weak
rosters equity, and makes the playoff cut a low bar (a .488 team qualifies —
and won). **Every champ% in the LEDGER is measured on the wrong bracket and
overstates top-roster safety.** Adopting the real format is registered as
E14 for the September re-baseline (not changed now: the freeze's "empty
arena diff" proof and ledger comparability are preserved; the committed
harness dual-reports until then).

## 5. Room model from the real 2025-26 draft (`arena/mocks/room_model.py`)

Reach index = pick number − frozen-Oct-2025 9-cat value rank (positive =
beats value / takes fallers; negative = reaches past value). 148/156 picks
matched.

| Team | Mean | Early (R1–6) | Read |
|---|---|---|---|
| **JAMAL AL-QUETA (owner)** | **+24.3** | **+14.2** | the room's biggest value-getter |
| All guards no defense | +10.0 | −15.8 | early name reaches, late value |
| IM SO HORT | +8.7 | +5.5 | value-anchored |
| Anti-wan / John's | −1.0 / −1.3 | −7 / −8 | mild reachers |
| HalleLuka Amen (champ) | −4.4 | −14.8 | early reaches (Embiid R7 gamble) |
| Itsy Bitsy Spida | −5.5 | +9.3 | value early, hype late |
| The Konclave | −7.4 | −16.5 | reaches, then out-streams everyone (83 moves) |
| Wing Chun Wemby | −15.0 | +4.3 | mixed |
| Not hurt just SARR | −17.2 | −26.0 | heavy reacher |
| Gotta Be Bamonte | −18.8 | −25.7 | heavy reacher |
| Devin Minutes in Heaven | −30.9 | −43.5 | extreme name/hype drafter |

**Real-world validation of the value doctrine:** reach index vs record is
strongly positive — the owner (+24.3) had the best record; the three biggest
reachers finished 10th/11th/12th in Pct. Drafting value works in this room.

**Room-composition implication:** 8–9 of 11 opponents reach past 9-cat value
early — the REAL room behaves closer to the *market/name* persona than the
arena's value-bot majority. The mock rooms are harsher on value players than
reality; the 8/4 chip recalibration (fit to value-bot rooms) likely
overcorrects for the real draft. Registered as E17 (refit `MOCK_CAST` /
survival blend to these measured reach profiles).

## 6. Owner profile (2025-26)

Drafted from **slot 4**: SGA, Brunson, JJJ, Jamal Murray, OG, Porziņģis,
Kawhi, Clingan, Eason, Herbert Jones, Brook Lopez, Gary Trent, DiVincenzo.
Value-anchored, injury-risk tolerant (Kawhi/KP/Murray), stocks-and-guards
core → **.640 regular season**. 64 in-season moves (top-third streamer).
Final roster shows heavy churn. The failure mode was not drafting, not
management — it was three playoff weeks of variance in a format that gives
the #1 seed no shelter.

## 7. What this changes (registered)

- **E14** — adopt the real playoff format (8, no byes) at the September
  arena re-baseline; until then debriefs may dual-report via the harness.
- **E15** — IL+ stash revaluation: 2 IL+ slots make recovery stashes ~free
  (the champion stashed Embiid; IM SO HORT drafted Tatum R13 as a pure
  stash). The recovery-exclusion rule (P3) was calibrated for a world with
  no IL slots; late-round stash candidates deserve a measured revisit.
- **E16** — streaming gap: 27–83 moves/team vs the arena's zero. Unmodeled;
  at minimum the September report must state that draft champ% is a
  no-streaming bound, and bench-slot value should tilt toward flexibility.
- **E17** — refit the arena room to the measured reach profiles (more
  name/market drafters, fewer value bots); re-run chip calibration on it.
- **E9 refinement** — in an 8/12-qualify league the binding objective is
  winning 3 H2H weeks vs playoff-tier teams, not season-long dominance:
  evaluate ECW against projected playoff-tier opponents specifically.

## 8. ~~Still missing~~ — ANSWERED (owner, 2026-08-04)

## 9. Owner's answers, verbatim facts (2026-08-04) — all 17 questions

1. **Exact 9 cats confirmed**: FG%, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO.
2. **Playoffs: 1 week per matchup, weeks 19–21** (chosen to dodge late-season
   rest). Completes the E14 spec: 8 teams, no byes, three 1-week rounds.
3. **Daily lineup setting** (not weekly). Raises streaming/bench-flexibility
   value further; E16 scope input.
4. **Unlimited moves.**
5. **Daily waivers, free-for-all; players lock at game time.**
6. **IL+ accepts day-to-day/GTD — but the owner drafts ONLY for active
   roster + bench, never for IL+ stashes.** Standing owner rule. This
   CLOSES E15 in the direction already shipped: the recovery-exclusion
   rule stands; no stash-drafting logic will be added.
7. **No keepers** — full redraft.
8. **Real draft: October, the week before the NBA season opens.** September
   is regimen-building; date TBD.
9. **Snake confirmed**; slot TBD.
10. **Live deck use on draft day confirmed** — the mock workflow is the
    real workflow.
11. **Same 11 managers return.** E17's measured reach profiles carry over
    at full weight.
12. No extra manager quirks beyond the data; synthesize from the board.
13. **Risk preference: value-first, risk-tolerant when the price is right.**
    Kawhi/KP were best-available steals at their draft positions, not a
    deliberate ceiling strategy. This matches the tool's adj-value + haircut
    design; no repricing needed.
14. **Projections: the owner will upload multiple ranking datasets in
    September; Claude synthesizes them into its OWN projection set** with
    injury adjustments, rookie scaling, and independent analysis — the
    intended edge over the room. This becomes the core of the September
    data-refresh step.
15. **ΔECW draft-time prototype (E9/P1): AUTHORIZED.** Engine change may
    ship if it passes the pre-registered bar.
16. Harness backfill: approved per recommendation — **done 2026-08-04**
    (all mock 10–30 harnesses committed to `arena/mocks/`).
17. **Two-stage calendar confirmed:** September recalibration run when
    multi-source projections land; **final refresh + deck rebuild the week
    before the October draft.**

## 10. Second season ingested: 2024-25 (owner-provided 2026-08-04)

Standings + full 13-round draft board. Same format verified again: 162
cat-games = 18 weeks × 9, 8 playoff teams. Owner drafted from **slot 9** as
"David's Demure Team" and finished **3rd** (.506, 8th-best record).

| Final | Team (2024-25 name) | Record | Pct | Record rank | Moves |
|---|---|---|---|---|---|
| 1 🏆 | Put Me in Coach | 84-76-2 | .525 | **7** | **16** |
| 2 | Sales & Markkanen | 90-71-1 | .559 | 3 | 87 |
| 3 | **David's Demure Team (owner)** | 81-79-2 | .506 | 8 | 84 |
| 4 | MOO DURANT | 87-75-0 | .537 | 5 | 45 |
| 5 | Match My Freak | 94-67-1 | .584 | 2 | 40 |
| 6 | LAME TIME | 85-75-2 | .531 | 6 | 70 |
| 7 | Poop and Scoot Streaks | 88-72-2 | .550 | 4 | 61 |
| 8 | John's Matchless Team | 99-63-0 | **.611** | **1** | 31 |
| 9–12 | Quickley Luk-a… / Day to Davis / BALLSACK LAVINE / Jericho's | .469/.466/.346/.315 | | | |

**The two-season structural signature — no longer a one-year fluke:**

- **Both #1 seeds lost in the playoffs without reaching the final**: 2024-25
  John's (.611) finished 8th of 8 playoff teams; 2025-26 the owner (.640)
  finished 6th.
- **Both champions had exactly the 7th-best record** (.525 and .488).
- 2024-25's playoff order nearly *inverted* the record order (record ranks
  by finish: 7, 3, 8, 5, 2, 6, 4, 1). n=2 seasons, so this is an observed
  pattern, not a law — but it is now the league's defining feature, and it
  makes E14 (real bracket in the sim) and the E9 playoff-tier refinement
  first-order, not cosmetic.
- The 2024-25 champion made **16 moves all season** (fewest in the league)
  — a set-and-forget title. Streaming (E16) helps but is demonstrably not
  required. That same manager finished last in record the next year.

**Cross-season identity map (owner-confirmed + safe inference):**

| 2024-25 | 2025-26 | Note |
|---|---|---|
*(superseded by the complete owner-provided map below, 2026-08-04)*

**Owner's two-season profile:** slot 9 → 3rd place; slot 4 → #1 seed. Ant/
Chet/PG/Jaylen Brown core in 24-25, SGA/Brunson/JJJ in 25-26 — consistently
value-anchored, consistently strong, twice stopped short by the bracket.

**2024-25 draft board:** recorded in full for September's two-season manager
profiling (`room_model.py` cannot grade it quantitatively — the arena's
frozen pool is October 2025, and grading a 2024 draft against a 2025 board
would be dishonest; qualitative reads only until/unless an Oct-2024 value
reference is sourced). Raw board preserved in this repo's git history via
the owner's message of 2026-08-04.

## 11. Third season ingested: 2023-24 (owner-provided 2026-08-04) — calibration set complete

Standings + full draft board. **Note: 20-week regular season that year**
(180 cat-games); the league moved to 18 weeks in 2024-25 and stayed there.
8 playoff teams again. Owner = **LayBron**, drafted slot 5, finished **7th**
(.531, record rank 3).

Playoff finish vs record rank: 1st=rank 2 (Poole-ootan), 2nd=rank 6,
3rd=rank 4, 4th=**rank 1** (REBUILDING SZN .596), 5th=5, 6th=8, 7th=3, 8th=7.

**The three-season signature, finalized:**

- **The #1 record has never won the title** in three seasons: finished 4th
  (23-24, .596), 8th (24-25, .611), 6th (25-26, the owner at .640).
- Champions' record ranks: **2, 7, 7**.
- The regular season selects the field; the 3-week bracket decides the
  title, and it has repeatedly favored mid-seeds. E14 and the E9
  playoff-tier objective are the response.

**The dynasty profile — Poole-ootan Party = Put Me in Coach = Gotta Be
Bamonte (owner-confirmed): back-to-back champion (23-24, 24-25), then
last-place record (25-26).** Their 23-24 title came from record rank 2 with
28 moves; their 24-25 title from rank 7 with 16 moves — low-churn,
draft-it-and-ride manager whose 25-26 draft (Sabonis R1) collapsed. Watch
for reversion, not repetition.

**Owner three-season arc (LayBron → David's Demure → JAMAL AL-QUETA):**
playoff finishes 7th → 3rd → 6th; record ranks 3 → 8 → **1**. The
regular-season engine has improved every year; the bracket has been the
ceiling all three years.

**Season-length caveat for any cross-season rate comparison:** 23-24 rates
are per-20-weeks; 24-25/25-26 per-18. Current league = 18 (`WEEKS = 18`
stays correct).

2023-24 draft board recorded via the owner's message (git history);
qualitative use only — no Oct-2023 value reference exists.

## 12. COMPLETE manager map, all three seasons (owner-provided 2026-08-04)

*(Supersedes the earlier partial map — the owner's quick answer had matched
Match My Freak to the 25-26 champion; the complete list corrects this:
HalleLuka = Sales & Markkanen = Martin.)*

| Manager | 2023-24 (finish) | 2024-25 (finish) | 2025-26 (finish) |
|---|---|---|---|
| **David (owner)** | LayBron (7) | David's Demure Team (3) | **JAMAL AL-QUETA (6, record #1)** |
| Robby | **Poole-ootan Party (1)** | **Put Me in Coach (1)** | Gotta Be Bamonte (12th record) |
| Martin | Martin you're him (5) | Sales & Markkanen (2) | **HalleLuka Amen (1)** |
| Oblena | D.O.L.L.A. (8) | Match My Freak (5, record #2) | Itsy Bitsy Spida (9) |
| Kevin | The Big Deuce (11) | Day to Davis (10) | All guards no defense (8, record #2) |
| **Noah — AUTODRAFTS** | Strokin my Saboner (9) | Poop and Scoot Streaks (7) | Devin Minutes in Heaven (11) |
| Cayas | REBUILDING SZN (4, record #1) | BALLSACK LAVINE (11) | IM SO HORT (4) |
| John | Steph BoyArdee (2) | John's Matchless Team (8, record #1) | John's Cool Team (5) |
| Hegi | Sing to me Paolo (12) | Quickley Luk-a Fox and a Kat (9) | Not hurt just SARR (10) |
| Will | TEAM MENISCUS TEAR (3) | LAME TIME (6) | The Konclave (2) |
| Kyle | Last Place HumilAyton (10) | Jericho's Incredible Team (12) | ur my only hope Anti-wan (7) |
| JCo | Beats by Dray (6) | MOO DURANT (4) | Wing Chun Wemby (3) |

**Three-season profiles for the October brief:**

- **Martin is the room's apex threat**: 5th → 2nd → champion, ascending
  every year, heavy streamer (87→50 moves). The reach index (−14.8 early in
  25-26) says he reaches for *his* guys and makes it work.
- **Robby (the dynasty)**: back-to-back titles then total collapse. Watch
  for reversion toward competence.
- **Will**: 3rd → 6th → 2nd, top-2 streamer every year (87/70/83 moves) —
  the in-season grinder; his drafts matter less than his waiver wire.
- **JCo**: 6 → 4 → 3, quietly ascending. Sneaky.
- **Noah AUTODRAFTS** — his 25-26 reach index (−43.5) is Yahoo's default
  board, not a persona. For E17, model Noah as pure market/ADP drafter —
  the single most predictable seat in the room. Slots near Noah inherit
  clean ADP-chalk expectations.
  **CORRECTED (owner, 2026-08-04): the autodraft was 2025-26 ONLY —
  2023-24 and 2024-25 were manual.** The −43.5 stays as the room's pure
  board-geometry reference; Noah's behavioral model is refit to the manual
  seasons (ADP-leaning, real LaMelo loyalty) — see
  report_2026-08-04_manager_profiles.md §5 and profiles.json.
- **Hegi**: 12 → 9 → 10, low engagement; a source of falling value around
  his picks (he took Sochan #150 in 25-26-style spots).
- **Kevin**: guard-heavy identity three years running (name literally says
  it) — REB/BLK/FG% fall to his neighbors.
- **Cayas**: volatile — record #1, then 11th, then 4th.
- **Kyle**: 10 → 12 → 7, improving from the basement.
- **John**: steady mid-to-high; 24-25's record #1 that lost the QF.

E17's room refit now has named, three-season behavioral profiles for all
11 opponents plus one confirmed autodrafter.
