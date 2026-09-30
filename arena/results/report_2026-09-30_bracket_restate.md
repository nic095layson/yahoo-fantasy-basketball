# Bracket restatement — the live rooms re-run on the league's real playoff format (2026-09-30)

**What changed.** E14 shipped. `arena.PLAYOFF_TEAMS` went from 6 to 8 and the
season simulator's bracket became `arena.playoff_champion`: eight seeds, no
byes, fixed pairings 1v8, 4v5, 2v7, 3v6, winners in seed order, one week per
round — the format this league has played for three seasons
(`league_intel_2025-26.md` §1). The eight-team bracket was measured on
2026-08-04 (§4: elite rosters lose four to six points of title odds) and
registered as E14 "for the September re-baseline"; nothing fired that trigger,
and the kit's 2026-09-30 gap audit found the constant still at 6 (decision
D-G1: ship it before Oct 14). Red-first: `arena/test_bracket.py` (five cases)
failed on the old code — two assertion failures and three attribute errors,
including 150 playoff credits where 25 seasons of an eight-team field must
produce 200 — and passes on the port. Identity: the ported bracket and the
calibration harness's copy (`format_delta.py`, `simulate(…, 8, False)`) return
byte-identical champion and playoff tallies on the mock-57 rosters at two
seeds × 400 seasons, so the 8/4 deltas reproduce by construction.

**What was re-run.** The arms stage of `live_retro.py` for every entry in its
`MOCKS` table — mocks 51 to 57 on each mock's own grade tag, and `--tag v33`
for 51 to 56 (thirteen runs; seeds 11/23/47 × 6,000 = 18,000 CRN seasons per
arm; the same swaps, because the hindsight stage is ECW-based and has no
bracket in it) — plus the two mock-54 punt experiments (`punt_arms.py 54 63
AST`, with and without the Porziņģis veto) and the mock-51 combo arms. The
JSON files in this directory now hold the real-bracket numbers; the old ones
are in git history and in the tables below. `bracket_restate_2026-09-30.json`
holds every old/new pair.

**Headline.** The real bracket compresses every strong roster's title odds and
changes no conclusion. As drafted, the seven live rooms on their own pools
fall by 7.43 to 12.24 points where the old figure was
above 30 percent (mock 57: 35.23 to 27.44;
mock 56: 54.94 to 43.66); across
the 138 arms whose old figure exceeded five percent, new over old averages
0.809 (range 0.743 to 1.093). Playoff
odds rise everywhere, because eight of twelve qualify. **Every as-drafted room
keeps its rank (13 of 13)**, and only 4 of 151
arms change rank at all, each by one place on a mid roster. **Following the
card still beats the roster as drafted in every room**: the gap runs
+7.86 to +25.98 points on the real bracket
(it was +7.62
to +31.44
on the old one). The weakest roster is the one that gains: mock 55 on v33
goes from 1.64 to 3.02 percent and from 34 to 58 percent playoff odds — the
equity the real cut hands to mid and weak rosters, exactly as measured on
8/4. The mock-54 punt verdicts are unchanged (steering fails its bar by
6.25 points unvetoed
and 7.75 vetoed, against
6.78 and
8.96 before).

## 1. As drafted and follow-the-card, every file

| room | as drafted, 6-team byes | as drafted, 8-team no byes | Δ | playoff old | playoff new | rank old | rank new | follow-card old | follow-card new | gap old | gap new |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock 51 (v23, as graded 9/21) | 55.03 | **42.79** | -12.24 | 99.82 | **99.96** | 1 | 1 | 63.47 | **51.44** | +8.44 | **+8.65** |
| mock 52 (v23) | 47.94 | **37.95** | -9.99 | 99.81 | **99.96** | 1 | 1 | 56.92 | **45.81** | +8.97 | **+7.86** |
| mock 53 (v25) | 38.53 | **31.10** | -7.43 | 99.29 | **99.95** | 1 | 1 | 55.59 | **46.14** | +17.07 | **+15.04** |
| mock 54 (v28) | 49.36 | **38.62** | -10.73 | 99.73 | **99.98** | 1 | 1 | 60.11 | **49.17** | +10.75 | **+10.55** |
| mock 55, named cast (v28) | 16.09 | **15.69** | -0.41 | 86.36 | **95.64** | 3 | 3 | 37.29 | **29.97** | +21.20 | **+14.28** |
| mock 56 (v31) | 54.94 | **43.66** | -11.28 | 99.95 | **99.98** | 1 | 1 | 62.56 | **52.58** | +7.62 | **+8.92** |
| mock 57 (v33) | 35.23 | **27.44** | -7.78 | 97.29 | **99.30** | 1 | 1 | 52.96 | **41.43** | +17.73 | **+13.99** |
| mock 51 on v33 | 39.78 | **29.72** | -10.06 | 98.08 | **99.56** | 1 | 1 | 54.21 | **42.07** | +14.43 | **+12.34** |
| mock 52 on v33 | 23.67 | **20.30** | -3.37 | 94.12 | **98.26** | 2 | 2 | 49.72 | **40.39** | +26.05 | **+20.09** |
| mock 53 on v33 | 29.34 | **24.58** | -4.76 | 97.69 | **99.64** | 2 | 2 | 45.02 | **36.99** | +15.68 | **+12.42** |
| mock 54 on v33 | 38.27 | **29.71** | -8.56 | 98.35 | **99.62** | 1 | 1 | 53.86 | **43.14** | +15.59 | **+13.43** |
| mock 55 on v33 | 1.64 | **3.02** | +1.37 | 34.31 | **58.17** | 8 | 8 | 26.41 | **22.44** | +24.76 | **+19.42** |
| mock 56 on v33 | 25.51 | **20.58** | -4.92 | 93.99 | **98.61** | 1 | 1 | 56.95 | **46.56** | +31.44 | **+25.98** |

Rank changes among the swap arms: m53_arms_v33.json swap#87:Miles Bridges 1→2, m55_arms.json swap#15:Evan Mobley 3→2, m55_arms.json swap#34:Franz Wagner 3→2, m55_arms_v33.json swap#106:Draymond Green 8→7.

## 2. What the bracket does not touch

The deck's Top-5 order, the blend50 score, ΔECW, the LAST CALL row, the punt
advisor and the build-coherence strip are weekly-model outputs; the survival
chips are price-model outputs. None of them has a bracket in it, so the card
the owner drafted against in mocks 54 to 57 is unchanged, and the deck page
was not rebuilt or republished. The hindsight stage (ECW gain per turn) and
the forecast stage are bracket-free too, which is why only the arms stage
was re-run.

## 3. A second defect the re-run caught: the mock-51 combo harness read the live pool

`mock51_retro.py` mapped its "v23" pool to `data/players.csv`, which was the
v23 pool on 2026-09-21 and is the v35 pool today. Its first re-run graded the
combo arms on the wrong pool: 67.38 became 33.91, below the single Turner swap
it contains, and the kept-total z-sum — a figure the bracket cannot move —
went from 19.88 to 14.52. The pool is now pinned to the same materialized
snapshot `live_retro.py` uses (rev f724435, `m52_players_v23.csv`); on it the
kept-total returns to 19.88 exactly, the harness's own as-drafted for seat 10
equals `live_retro.py`'s to three decimals (42.789), and the combos land at
56.16 and 59.62. LESSONS 23 carries the note.

## 4. Where old-bracket numbers still stand

- The seven live-room debriefs keep their arms tables as published, each with
  a line above the table quoting the restated as-drafted figures and pointing
  here.
- The kit's after-reports for mocks 50 to 57, the 2026-09-29 final check and
  the 2026-09-29 re-calibration quote the old numbers; they are dated records
  and are not rewritten. Their conclusions (rank 1 in ECW, follow-the-card
  beats as-drafted, the punt verdicts) all survive the restatement above.
- The ledger mocks 10 to 34 and the arena's strategy tournament were never
  re-run; `league_intel_2025-26.md` §4 holds their measured deltas for four
  mocks, and the arena README says every champ% recorded before 2026-09-30
  is on the six-team bracket.

## 5. Provenance

- Code: `arena/arena.py` (constant, header, `playoff_champion`),
  `arena/test_bracket.py` (new), `arena/mocks/mock51_retro.py` (pool pin),
  `arena/README.md`, `LESSONS.md` (23), `league_intel_2025-26.md` §7.
- Runs: 2026-09-30, thirteen `live_retro.py <mock> arms [--tag v33]`, two
  `punt_arms.py 54 63 AST [--veto]`, one `mock51_combo.py`; logs in the session
  scratchpad; every number above is read from the JSON files by the script
  that wrote this page, not typed.
- Suites after the change: `test_bracket.py` 5/5, `test_draft.py` 62/62,
  `test_card.py` 61/61, `test_gates.py` 34/34; `git status docs/` empty.

## Appendix — every arm, old vs new


**`m51_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|

metadata (old, new): {'_board_rank': (1, 1)}
| as_drafted | 55.03 | **42.79** | -12.24 | 99.82 | **99.96** | 1 | 1 |
| swap#39:Derrick White | 56.06 | **42.99** | -13.07 | 99.93 | **99.98** | 1 | 1 |
| swap#58:Myles Turner | 55.98 | **43.78** | -12.20 | 99.88 | **99.98** | 1 | 1 |
| swap#63:Payton Pritchard | 57.85 | **45.79** | -12.06 | 99.90 | **99.97** | 1 | 1 |
| swap#82:Myles Turner | 62.34 | **50.84** | -11.49 | 99.99 | **100.00** | 1 | 1 |
| swap#87:Myles Turner | 58.14 | **46.22** | -11.92 | 99.94 | **99.99** | 1 | 1 |
| swap#106:Brook Lopez | 57.18 | **45.17** | -12.01 | 99.93 | **99.99** | 1 | 1 |
| swap#111:Brook Lopez | 56.43 | **43.77** | -12.66 | 99.92 | **99.98** | 1 | 1 |
| swap#130:Brook Lopez | 57.41 | **45.17** | -12.24 | 99.92 | **99.99** | 1 | 1 |
| swap#135:Brook Lopez | 58.11 | **45.77** | -12.34 | 99.93 | **99.99** | 1 | 1 |
| swap#154:Brook Lopez | 63.42 | **52.06** | -11.36 | 99.98 | **100.00** | 1 | 1 |
| follow_card_selfconsistent | 63.47 | **51.44** | -12.03 | 100.00 | **100.00** | 1 | 1 |
| combo_turner82_lopez154 | 67.38 | **56.16** | -11.22 | 100.00 | **100.00** | 1 | 1 |
| combo_turner82_lopez154_pritchard63 | 69.66 | **59.62** | -10.03 | 100.00 | **100.00** | 1 | 1 |

non-arm entry `_kept_total` (old keys ['1', '2', '3', '4']; new ['1', '2', '3', '4'])

non-arm entry `_as_drafted_by_seat` (old keys ['1', '2', '3', '4']; new ['1', '2', '3', '4'])

**`m51_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 39.78 | **29.72** | -10.06 | 98.08 | **99.56** | 1 | 1 |
| swap#39:Derrick White | 41.39 | **31.00** | -10.39 | 98.64 | **99.71** | 1 | 1 |
| swap#63:Payton Pritchard | 41.98 | **31.49** | -10.49 | 98.59 | **99.71** | 1 | 1 |
| swap#82:Miles Bridges | 46.65 | **35.97** | -10.68 | 99.35 | **99.88** | 1 | 1 |
| swap#87:Myles Turner | 40.67 | **30.87** | -9.80 | 98.37 | **99.61** | 1 | 1 |
| swap#106:Ja Morant | 42.52 | **31.67** | -10.85 | 98.74 | **99.68** | 1 | 1 |
| swap#130:PJ Washington | 43.87 | **33.01** | -10.86 | 98.83 | **99.74** | 1 | 1 |
| swap#135:PJ Washington | 45.47 | **33.84** | -11.62 | 98.97 | **99.79** | 1 | 1 |
| swap#154:Kyle Filipowski | 45.03 | **34.03** | -11.00 | 99.13 | **99.80** | 1 | 1 |
| follow_card_selfconsistent | 54.21 | **42.07** | -12.14 | 99.84 | **99.97** | 1 | 1 |

**`m52_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 47.94 | **37.95** | -9.99 | 99.81 | **99.96** | 1 | 1 |
| swap#10:Jalen Johnson | 52.82 | **43.82** | -9.00 | 99.90 | **99.99** | 1 | 1 |
| swap#15:Derrick White | 48.27 | **38.70** | -9.57 | 99.83 | **99.97** | 1 | 1 |
| swap#34:Derrick White | 47.58 | **37.78** | -9.80 | 99.78 | **99.97** | 1 | 1 |
| swap#39:Derrick White | 52.44 | **42.52** | -9.92 | 99.91 | **99.99** | 1 | 1 |
| swap#58:Tyler Herro | 47.58 | **37.51** | -10.07 | 99.73 | **99.97** | 1 | 1 |
| swap#82:Isaiah Hartenstein | 47.01 | **37.78** | -9.23 | 99.75 | **99.97** | 1 | 1 |
| swap#106:Brook Lopez | 48.10 | **38.71** | -9.39 | 99.79 | **99.97** | 1 | 1 |
| swap#130:Christian Braun | 49.53 | **40.30** | -9.23 | 99.87 | **99.97** | 1 | 1 |
| swap#135:Christian Braun | 48.67 | **38.50** | -10.17 | 99.83 | **99.97** | 1 | 1 |
| swap#154:Christian Braun | 48.42 | **38.73** | -9.69 | 99.83 | **99.97** | 1 | 1 |
| follow_card_selfconsistent | 56.92 | **45.81** | -11.11 | 99.96 | **100.00** | 1 | 1 |

**`m52_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 23.67 | **20.30** | -3.37 | 94.12 | **98.26** | 2 | 2 |
| swap#10:Karl-Anthony Towns | 34.98 | **27.86** | -7.12 | 97.96 | **99.58** | 1 | 1 |
| swap#15:Karl-Anthony Towns | 28.93 | **23.77** | -5.16 | 96.46 | **99.14** | 1 | 1 |
| swap#39:Derrick White | 28.25 | **23.45** | -4.80 | 96.93 | **99.27** | 2 | 2 |
| swap#87:Isaiah Hartenstein | 24.03 | **20.98** | -3.05 | 94.34 | **98.30** | 2 | 2 |
| swap#111:Malik Monk | 25.33 | **21.77** | -3.56 | 94.83 | **98.53** | 2 | 2 |
| swap#130:Devin Vassell | 40.52 | **31.39** | -9.13 | 99.09 | **99.82** | 1 | 1 |
| swap#135:Collin Gillespie | 26.29 | **21.99** | -4.30 | 95.68 | **98.73** | 2 | 2 |
| follow_card_selfconsistent | 49.72 | **40.39** | -9.33 | 99.95 | **99.99** | 1 | 1 |

**`m53_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 38.53 | **31.10** | -7.43 | 99.29 | **99.95** | 1 | 1 |
| swap#10:Chet Holmgren | 46.26 | **36.96** | -9.30 | 99.72 | **99.98** | 1 | 1 |
| swap#39:Anthony Davis | 39.18 | **32.18** | -7.00 | 99.47 | **99.96** | 1 | 1 |
| swap#58:Payton Pritchard | 43.14 | **34.06** | -9.08 | 99.52 | **99.97** | 1 | 1 |
| swap#82:Ja Morant | 40.54 | **33.82** | -6.73 | 99.53 | **99.97** | 1 | 1 |
| swap#111:Christian Braun | 42.21 | **35.44** | -6.77 | 99.65 | **99.98** | 1 | 1 |
| swap#130:Christian Braun | 44.23 | **36.94** | -7.29 | 99.80 | **99.98** | 1 | 1 |
| swap#135:Brook Lopez | 38.71 | **32.08** | -6.63 | 99.34 | **99.94** | 1 | 1 |
| swap#154:Brook Lopez | 41.68 | **34.53** | -7.14 | 99.58 | **99.98** | 1 | 1 |
| follow_card_selfconsistent | 55.59 | **46.14** | -9.45 | 99.97 | **100.00** | 1 | 1 |

**`m53_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 29.34 | **24.58** | -4.76 | 97.69 | **99.64** | 2 | 2 |
| swap#10:Chet Holmgren | 36.80 | **29.83** | -6.97 | 99.02 | **99.88** | 1 | 1 |
| swap#34:Anthony Davis | 29.85 | **24.67** | -5.18 | 97.83 | **99.62** | 2 | 2 |
| swap#39:Anthony Davis | 30.26 | **24.91** | -5.35 | 98.06 | **99.69** | 2 | 2 |
| swap#58:Payton Pritchard | 33.78 | **27.48** | -6.29 | 98.42 | **99.77** | 1 | 1 |
| swap#82:Ja Morant | 31.67 | **26.66** | -5.01 | 98.34 | **99.78** | 1 | 1 |
| swap#87:Miles Bridges | 31.01 | **25.99** | -5.02 | 98.04 | **99.72** | 1 | 2 |
| swap#111:Devin Vassell | 31.09 | **25.96** | -5.13 | 98.26 | **99.78** | 1 | 1 |
| swap#130:Draymond Green | 34.21 | **28.22** | -5.99 | 98.69 | **99.75** | 1 | 1 |
| swap#135:Malik Monk | 32.34 | **27.01** | -5.33 | 98.39 | **99.78** | 1 | 1 |
| follow_card_selfconsistent | 45.02 | **36.99** | -8.02 | 99.79 | **99.99** | 1 | 1 |

**`m54_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 49.36 | **38.62** | -10.73 | 99.73 | **99.98** | 1 | 1 |
| swap#34:Derrick White | 50.57 | **40.03** | -10.53 | 99.83 | **99.98** | 1 | 1 |
| swap#39:Derrick White | 52.71 | **42.29** | -10.41 | 99.89 | **99.99** | 1 | 1 |
| swap#58:Tyler Herro | 48.62 | **38.64** | -9.98 | 99.73 | **99.95** | 1 | 1 |
| swap#63:Tyler Herro | 48.79 | **39.09** | -9.70 | 99.71 | **99.98** | 1 | 1 |
| swap#82:Coby White | 52.96 | **42.28** | -10.68 | 99.87 | **99.99** | 1 | 1 |
| swap#130:Christian Braun | 48.69 | **38.49** | -10.21 | 99.74 | **99.98** | 1 | 1 |
| swap#135:Christian Braun | 56.93 | **46.29** | -10.64 | 99.94 | **99.99** | 1 | 1 |
| swap#154:Brook Lopez | 53.25 | **42.15** | -11.10 | 99.88 | **99.99** | 1 | 1 |
| follow_card_selfconsistent | 60.11 | **49.17** | -10.93 | 99.99 | **100.00** | 1 | 1 |

**`m54_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 38.27 | **29.71** | -8.56 | 98.35 | **99.62** | 1 | 1 |
| swap#15:Chet Holmgren | 41.22 | **32.29** | -8.93 | 98.96 | **99.84** | 1 | 1 |
| swap#34:Derrick White | 39.48 | **30.86** | -8.62 | 98.63 | **99.71** | 1 | 1 |
| swap#39:Derrick White | 42.47 | **32.72** | -9.74 | 99.32 | **99.87** | 1 | 1 |
| swap#58:Tyler Herro | 37.16 | **28.34** | -8.82 | 98.02 | **99.53** | 1 | 1 |
| swap#82:Miles Bridges | 41.64 | **32.03** | -9.62 | 98.98 | **99.81** | 1 | 1 |
| swap#87:Miles Bridges | 37.73 | **29.13** | -8.60 | 98.25 | **99.59** | 1 | 1 |
| swap#106:Devin Vassell | 39.17 | **30.89** | -8.28 | 98.61 | **99.72** | 1 | 1 |
| swap#130:Malik Monk | 40.09 | **30.93** | -9.16 | 98.63 | **99.73** | 1 | 1 |
| swap#135:Saddiq Bey | 44.63 | **34.78** | -9.86 | 99.33 | **99.86** | 1 | 1 |
| follow_card_selfconsistent | 53.86 | **43.14** | -10.72 | 99.92 | **99.99** | 1 | 1 |

**`m54_punt_arms.json`** (punt experiment, mock 54 from pick 63, punt ['AST'])

| arm | champ% 6-team byes | champ% 8-team no byes | playoff% old | playoff% new |
|---|---|---|---|---|
| as_drafted | 49.36 | **38.62** | 99.73 | **99.98** |
| follow_card_from63 | 59.27 | **48.74** | 99.97 | **99.99** |
| follow_card_from63_puntAST | 52.49 | **42.49** | 99.93 | **99.99** |

verdict old: {'bar': 'steered beats unsteered by >= 2.0 pp on >= 2 of 3 seeds', 'seeds_meeting_bar': 0, 'steered_minus_unsteered_pp': -6.778, 'passes': False} — new: {'bar': 'steered beats unsteered by >= 2.0 pp on >= 2 of 3 seeds', 'seeds_meeting_bar': 0, 'steered_minus_unsteered_pp': -6.255, 'passes': False}

**`m54_punt_arms_veto.json`** (punt experiment, mock 54 from pick 63, punt ['AST'])

| arm | champ% 6-team byes | champ% 8-team no byes | playoff% old | playoff% new |
|---|---|---|---|---|
| as_drafted | 49.36 | **38.62** | 99.73 | **99.98** |
| follow_card_from63 | 56.93 | **46.29** | 99.94 | **99.99** |
| follow_card_from63_puntAST | 47.98 | **38.54** | 99.76 | **99.96** |

verdict old: {'bar': 'steered beats unsteered by >= 2.0 pp on >= 2 of 3 seeds', 'seeds_meeting_bar': 0, 'steered_minus_unsteered_pp': -8.955, 'passes': False} — new: {'bar': 'steered beats unsteered by >= 2.0 pp on >= 2 of 3 seeds', 'seeds_meeting_bar': 0, 'steered_minus_unsteered_pp': -7.755, 'passes': False}

**`m55_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 16.09 | **15.69** | -0.41 | 86.36 | **95.64** | 3 | 3 |
| swap#10:Karl-Anthony Towns | 23.06 | **20.94** | -2.11 | 93.93 | **98.57** | 2 | 2 |
| swap#15:Evan Mobley | 21.48 | **19.04** | -2.44 | 92.76 | **98.07** | 3 | 2 |
| swap#34:Franz Wagner | 21.30 | **19.43** | -1.87 | 92.43 | **97.87** | 3 | 2 |
| swap#39:Franz Wagner | 17.97 | **16.66** | -1.31 | 88.55 | **96.52** | 3 | 3 |
| swap#58:Myles Turner | 19.66 | **18.26** | -1.41 | 89.66 | **96.88** | 3 | 3 |
| swap#63:Myles Turner | 20.41 | **17.74** | -2.67 | 91.22 | **97.59** | 3 | 3 |
| swap#111:PJ Washington | 17.43 | **16.31** | -1.13 | 87.86 | **96.38** | 3 | 3 |
| swap#130:Saddiq Bey | 16.58 | **15.83** | -0.75 | 87.17 | **95.82** | 3 | 3 |
| swap#135:Saddiq Bey | 17.73 | **16.42** | -1.31 | 88.28 | **96.23** | 3 | 3 |
| follow_card_selfconsistent | 37.29 | **29.97** | -7.32 | 98.86 | **99.86** | 1 | 1 |

**`m55_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 1.64 | **3.02** | +1.37 | 34.31 | **58.17** | 8 | 8 |
| swap#10:Karl-Anthony Towns | 3.78 | **5.67** | +1.89 | 52.61 | **76.07** | 7 | 7 |
| swap#15:Anthony Davis | 3.25 | **4.85** | +1.60 | 47.07 | **70.04** | 7 | 7 |
| swap#34:Franz Wagner | 2.99 | **4.68** | +1.69 | 46.53 | **69.30** | 7 | 7 |
| swap#39:Franz Wagner | 2.19 | **3.59** | +1.40 | 38.10 | **61.73** | 8 | 8 |
| swap#58:Payton Pritchard | 2.68 | **3.99** | +1.32 | 39.23 | **63.22** | 7 | 7 |
| swap#63:Miles Bridges | 1.99 | **3.61** | +1.62 | 37.91 | **61.89** | 8 | 8 |
| swap#82:Miles Bridges | 1.73 | **3.05** | +1.32 | 34.08 | **57.68** | 8 | 8 |
| swap#87:Zach LaVine | 3.43 | **4.96** | +1.53 | 47.17 | **70.74** | 6 | 6 |
| swap#106:Draymond Green | 2.46 | **4.26** | +1.80 | 42.72 | **67.17** | 8 | 7 |
| swap#111:Draymond Green | 2.44 | **4.09** | +1.66 | 42.71 | **66.98** | 8 | 8 |
| swap#130:Quentin Grimes | 8.53 | **9.33** | +0.79 | 67.18 | **85.08** | 4 | 4 |
| swap#135:Saddiq Bey | 1.89 | **3.14** | +1.25 | 36.96 | **60.52** | 8 | 8 |
| swap#154:Herbert Jones | 1.79 | **3.27** | +1.48 | 36.50 | **60.37** | 8 | 8 |
| follow_card_selfconsistent | 26.41 | **22.44** | -3.97 | 97.11 | **99.52** | 2 | 2 |

**`m56_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 54.94 | **43.66** | -11.28 | 99.95 | **99.98** | 1 | 1 |
| swap#15:Tyrese Maxey | 59.96 | **48.82** | -11.13 | 99.98 | **100.00** | 1 | 1 |
| swap#39:Desmond Bane | 58.01 | **46.76** | -11.25 | 99.97 | **99.99** | 1 | 1 |
| swap#63:Tyler Herro | 57.71 | **46.34** | -11.37 | 99.96 | **100.00** | 1 | 1 |
| swap#87:Miles Bridges | 55.17 | **43.96** | -11.21 | 99.91 | **99.99** | 1 | 1 |
| swap#106:Miles Bridges | 52.76 | **41.98** | -10.78 | 99.88 | **99.99** | 1 | 1 |
| swap#130:Jordan Poole | 58.59 | **47.93** | -10.67 | 99.97 | **100.00** | 1 | 1 |
| follow_card_selfconsistent | 62.56 | **52.58** | -9.98 | 99.99 | **100.00** | 1 | 1 |

**`m56_arms_v33.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 25.51 | **20.58** | -4.92 | 93.99 | **98.61** | 1 | 1 |
| swap#15:Anthony Davis | 34.08 | **26.49** | -7.58 | 97.31 | **99.58** | 1 | 1 |
| swap#34:Anthony Davis | 26.54 | **21.18** | -5.36 | 94.43 | **98.81** | 1 | 1 |
| swap#39:Chet Holmgren | 33.51 | **25.40** | -8.11 | 97.04 | **99.56** | 1 | 1 |
| swap#58:Tyler Herro | 26.45 | **20.04** | -6.41 | 94.04 | **98.50** | 1 | 1 |
| swap#63:Tyler Herro | 29.95 | **23.39** | -6.56 | 95.67 | **99.12** | 1 | 1 |
| swap#87:Miles Bridges | 33.51 | **26.09** | -7.42 | 97.44 | **99.50** | 1 | 1 |
| swap#106:Miles Bridges | 27.84 | **21.52** | -6.32 | 95.22 | **98.93** | 1 | 1 |
| swap#111:Miles Bridges | 32.02 | **23.86** | -8.16 | 96.96 | **99.42** | 1 | 1 |
| swap#130:PJ Washington | 30.12 | **23.48** | -6.64 | 95.92 | **99.35** | 1 | 1 |
| swap#135:PJ Washington | 29.80 | **23.62** | -6.18 | 96.08 | **99.24** | 1 | 1 |
| swap#154:Kyle Filipowski | 31.86 | **24.37** | -7.48 | 97.13 | **99.50** | 1 | 1 |
| follow_card_selfconsistent | 56.95 | **46.56** | -10.39 | 99.98 | **100.00** | 1 | 1 |

**`m57_arms.json`**

| arm | champ% 6-team byes | champ% 8-team no byes | Δ | playoff% old | playoff% new | rank old | rank new |
|---|---|---|---|---|---|---|---|
| as_drafted | 35.23 | **27.44** | -7.78 | 97.29 | **99.30** | 1 | 1 |
| swap#10:Chet Holmgren | 45.06 | **34.74** | -10.32 | 99.33 | **99.85** | 1 | 1 |
| swap#15:Jalen Johnson | 35.12 | **27.49** | -7.63 | 97.29 | **99.24** | 1 | 1 |
| swap#34:Anthony Davis | 39.29 | **30.49** | -8.80 | 98.37 | **99.62** | 1 | 1 |
| swap#39:Derrick White | 42.63 | **32.37** | -10.26 | 98.83 | **99.78** | 1 | 1 |
| swap#58:Payton Pritchard | 37.56 | **29.13** | -8.43 | 98.07 | **99.49** | 1 | 1 |
| swap#87:Miles Bridges | 41.01 | **30.46** | -10.55 | 98.36 | **99.61** | 1 | 1 |
| swap#111:Draymond Green | 35.98 | **28.35** | -7.63 | 97.62 | **99.33** | 1 | 1 |
| swap#135:Draymond Green | 36.75 | **28.68** | -8.07 | 97.76 | **99.46** | 1 | 1 |
| swap#154:Draymond Green | 36.01 | **28.17** | -7.84 | 97.62 | **99.43** | 1 | 1 |
| follow_card_selfconsistent | 52.96 | **41.43** | -11.52 | 99.82 | **99.97** | 1 | 1 |
