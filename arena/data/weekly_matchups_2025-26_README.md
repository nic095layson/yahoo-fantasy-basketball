# weekly_matchups_2025-26.csv — real per-category weekly matchup totals

**What this is.** The owner's Yahoo league weekly scoreboard totals,
2025-26 season, both teams of every matchup involving the owner's team
(JAMAL AL-QUETA). This is the fit data for the weekly-model refit (the
2026-08-04 system review's R7 / self-critique N1): per-category CV,
PCT_MIX_INFL, TEAM_WEEK_SHOCK, and the availability/games model are to be
re-estimated from these observed weeks instead of the hand-set constants
in `arena/arena.py` / the deck's `DECW_CV` block.

**Provenance.** Owner-uploaded Yahoo scoreboard screenshots, delivered
2026-08-04 in batches (weeks 1–5, 6–10, 11–15; more expected — append
below, two rows per week). Transcribed same-day. **Validation:** every
week's category score was recomputed from the transcribed totals (8 count
cats + FG%/FT% from makes/attempts, TOV inverted) and matched against the
recorded matchup result — 15/15 weeks reconcile exactly. Week 15's date
range is inferred from week sequence (its screenshot header was cropped);
all other date ranges are as displayed.

**Schema.** One row per team per week:
`season,week,dates,manager,team_name,fgm,fga,ftm,fta,tpm,pts,reb,ast,stl,blk,tov,gp,cats_won,opponent_manager`
— `gp` is that team's player-games actually played that week (Yahoo
"Games Played" tracker); FG%/FT% are derivable from makes/attempts (kept
raw for fitting). Manager first names match `arena/profiles.json`.

**Known limits.** (a) Owner-matchup weeks only — 2 of 6 league matchups
per week; opponent-vs-opponent weeks are not visible to this account's
scoreboard view. (b) One season. (c) Team totals, not per-day lines —
sufficient for weekly variance/covariance fitting, not for within-week
lineup reconstruction. Do not fit TEAM_WEEK_SHOCK cross-team covariance
from the owner's rows alone; each row-pair IS a valid (team, opponent)
draw for per-category weekly variance at observed GP.
