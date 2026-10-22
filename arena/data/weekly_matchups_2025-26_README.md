# weekly_matchups_2025-26.csv — real per-category weekly matchup totals

**What this is.** The owner's Yahoo league weekly scoreboard totals,
2025-26 season, both teams of every matchup involving the owner's team
(JAMAL AL-QUETA). This is the fit data for the weekly-model refit (the
2026-08-04 system review's R7 / self-critique N1): per-category CV,
PCT_MIX_INFL, TEAM_WEEK_SHOCK, and the availability/games model are to be
re-estimated from these observed weeks instead of the hand-set constants
in `arena/arena.py` / the deck's `DECW_CV` block.

**Provenance.** Owner-uploaded Yahoo scoreboard screenshots, delivered
2026-08-04 in batches (weeks 1–5, 6–10, 11–15, 16–19). Transcribed
same-day. **Validation:** every week's category score was recomputed from
the transcribed totals (8 count cats + FG%/FT% from makes/attempts, TOV
inverted) and matched against the recorded matchup result — 22/22 matchups
reconcile exactly (19 owner weeks + the champion's 3 playoff rounds). Stronger check: the owner's regular-season rows
(weeks 1–18) sum to 103 wins with exactly one tie (week 1, TO 68–68),
independently reproducing the displayed season record 103-58-1. Weeks 15
and 19 date ranges are inferred from week sequence (screenshot headers
cropped); all others as displayed. **Week 17 spans two calendar weeks
(2/9–2/22, All-Star break — GP 56/55); weeks 1–18 are regular season;
week 19 is the playoff quarterfinal (owner eliminated 2–7 by JCo — lost
ST by 1, PTS by 10, REB by 9: the bracket-variance data point E14
models).** Reconciliation flag for the September profiles work: the co-GM
brief (`fantasy-basketball-2026-27/instructions/...`) says the owner was
"1st seed, lost in semis last season" — this scoreboard shows a 6th-place
display and a round-1 exit in 2025-26; one of those claims is about a
different season or is wrong.

**Schema.** One row per team per week:
`season,week,dates,manager,team_name,fgm,fga,ftm,fta,tpm,pts,reb,ast,stl,blk,tov,gp,cats_won,opponent_manager`
— `gp` is that team's player-games actually played that week (Yahoo
"Games Played" tracker); FG%/FT% are derivable from makes/attempts (kept
raw for fitting). Manager first names match `arena/profiles.json`.

**Champion's playoff run added (owner-delivered, same 2026-08-04 batch
set):** Martin (HalleLuka Amen) won the title **5-4, 5-4, 5-4** — QF vs
Kevin, SF vs Justin, F vs William — three consecutive one-category
margins, with a sub-.500 regular-season cat record (78-82-2). Final
placements shown by Yahoo ("| Nth") are post-playoff standings (Martin
1st, William 2nd, JCo 3rd, Justin 4th, David 6th); David's 103-58-1 was
the league's best cat record, consistent with the co-GM brief's "1st
seed" — the brief's "lost in semis" remains unreconciled with the
week-19 round-1 exit shown here (possibly a prior-season memory). This
is the strongest in-league evidence for the E14 bracket emphasis: the
title ran through three coin-flip weeks, not through season-long
category dominance.

**Corrections.**

- **2026-10-21 — week 1, Kyle, `gp` 29 → 28.** The owner supplied the Yahoo
  week-1 matchup page (David vs Kyle), which reads `Games Played 32/32` and
  `28/28`. The stored row said 29. Receipt: that screenshot, delivered
  2026-10-21. All 20 other week-1 values reproduce the screenshot exactly
  (both teams' makes/attempts and all nine categories), and recomputing the
  nine categories from the stored totals returns David **8-0-1** with the
  TO 68-68 tie, matching the recorded `cats_won`. `gp` is not a scoring
  category, so the matchup result is unaffected. **The `gp` column of the
  other 43 rows has NOT been checked against a screenshot** — only week 1 has
  one in hand, so an isolated slip and a systematic one are not yet
  distinguishable. Anything fitting the games/shock model on this file should
  treat `gp` as carrying unquantified transcription error until the remaining
  weeks are re-checked.
- **2026-10-22 — what `gp` counts (owner decision D-GP-2: do not fit on it).**
  `gp` is Yahoo's "Games Played" counter as displayed. It does **not** equal
  the player-games behind the row's recorded totals. Five team-weeks were
  rebuilt from Yahoo's daily rosters (Flaim) and Basketball-Reference game
  logs: weeks 13 and 5 for David, week 8 for Robert, and week 1 for both
  teams. The players in active slots reproduce the row's eleven totals
  exactly in four of them, and ten of eleven in the fifth (Kyle's week-1
  assists, 88 against 87). Yet their games differ from `gp` by −7 to +8,
  including both screenshot-verified week-1 values (32 against 33, and 28
  against 35). What Yahoo's counter counts is unsettled. Do not fit the
  games, shock or availability model on `gp`. The totals columns are
  unaffected; all 44 rows equal Yahoo's own recorded totals. Record: kit
  `report/after-reports/after-report-2026-10-22-gp-reconstruction.md` §2–§3
  (kit PR #162). The player-games behind each 2025-26 row are being counted
  there (D-GP-1); this file is unchanged.

**Known limits.** (a) Mostly owner-matchup weeks (2 of 6 league matchups
per week) plus the champion's three playoff matchups; other
opponent-vs-opponent weeks are not visible to this account's scoreboard
view. (b) One season. (c) Team totals, not per-day lines —
sufficient for weekly variance/covariance fitting, not for within-week
lineup reconstruction. Do not fit TEAM_WEEK_SHOCK cross-team covariance
from the owner's rows alone; each row-pair IS a valid (team, opponent)
draw for per-category weekly variance at observed GP.
