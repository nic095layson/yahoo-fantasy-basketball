# Player-profile audit: Dylan Harper — the owner is right, the row is stale (2026-08-06)

**Owner question:** "What is your draft player profile on Dylan Harper? I
noticed he is being passed on such as rookies of THIS year like Boozer,
Dybantsa and Peterson. Harper is now entering his 2nd pro year, and was
already very productive last year."

**Verdict: the observation is correct and the cause is a data defect, not
a ranking defect.** Harper's row is a hand-authored PRE-rookie-season
projection that was never updated with what he actually did as a rookie.
The system's own July audit already named it
(`analysis_2026-08-04_self_critique.md` T4: "14 rookie rows are the least
defensible numbers in the pool (Dybantsa, Boozer, Peterson, **Harper**,
Wilson…)"). This entry pins the specifics and routes the fix.

## 1. What the tool currently believes (EVIDENCE — `data/players.csv:106`)

`Dylan Harper, SAS, PG, .455 FG% on 12.5 FGA, .760 FT% on 3.8 FTA,
1.4 3PM, 15.5 PTS, 4.2 REB, 5.0 AST, 1.3 ST, 0.4 BLK, 2.5 TO` — **note
field empty**.

Per-category z, and why he sinks:

| FG% | FT% | 3PTM | PTS | REB | AST | ST | BLK | TO | **total** |
|---|---|---|---|---|---|---|---|---|---|
| −0.53 | −0.48 | −0.39 | −0.41 | −0.80 | **+0.47** | **+0.59** | −0.66 | −0.53 | **−2.74** |

Two positives (AST, ST) against seven negatives. League baselines are
FG% .4759 and FT% .7894, both of which his line sits below on real
volume — so the volume-weighted percentage impacts are negative, and the
1.4 3PM and 2.5 TO compound it. Value-board rank **150**. That is why
the bots leave him until picks ~124–139 regardless of his market pin.

## 2. Why the rookies "jump" him (EVIDENCE)

Not hype in the ranking layer — **two separate mechanisms**:

- **Market pins** (`arena.py:175`): `Flagg 18, Dybantsa 30, Peterson 55,
  Harper 60, Boozer 70`. Harper IS pinned ahead of Boozer. But a pin only
  moves `market_ranks`; the bots blend ADP with *value*, and his value is
  −2.74, so he falls anyway.
- **The rookie multiplier** (`arena.py:189`): rows noted `rookie-proj` get
  ×1.15 on positive market score (÷1.15 when negative). Boozer, Dybantsa,
  Peterson and Coward carry that note. **Harper does not** — correctly, as
  a second-year player. So he is not being *penalized* as a rookie; he is
  being priced off a projection that never grew up.

Actual draft positions across the last six mocks: Harper 124–139,
Dybantsa 103–129, Boozer 98–122, Peterson 134–143. Boozer and Dybantsa
going earlier than Harper is the ×1.15 hype multiplier at work on rows
that are *equally* unverified.

## 3. Sensitivity — what a real second-year line would be worth (EVIDENCE)

Same engine, only Harper's row edited:

| Row | z-total | Value-board rank |
|---|---|---|
| as-is (current) | −2.74 | **150** |
| efficiency only (FG% .470, FT% .800) | −1.95 | 128 |
| genuine leap (19/5/6, FG% .470, FT% .800, 2.0 3PM) | −0.30 | **78** |

**Efficiency is the lever, not counting stats.** Moving only FG% and FT%
to roughly league-average lifts him 22 board spots; a full second-year
leap moves him ~72 spots into the R7 range. Note the pool's own comps:
Reed Sheppard (+0.40) beats Harper by 3.1z on nearly identical counting
stats, purely on .830 FT% and 2.7 3PM.

## 4. Bounds — what I am NOT claiming

- I have **not** verified Harper's actual 2025-26 production against a
  primary source in this session, and the repo holds no game-log data to
  check it against. The owner's report that he was productive is taken as
  the informed observation it is; the finding here is narrower and fully
  supported: **the tool's row is a pre-season guess with no post-rookie
  update, and its own audit flagged that class of row as least reliable.**
- Nothing was changed in `data/players.csv`. Editing a single player's
  projection by hand, mid-freeze, on one observation is exactly the
  ad-hoc move this project's discipline exists to prevent.

## 5. Routing (registered, no ad-hoc edit)

This is precisely what **September E-2b** exists for: the owner uploads
multiple third-party projection sets, they get synthesized into the
tool's own numbers, and any player deviating >15 ranks from consensus
gets documented provenance. Harper is now on the **named watch list** for
that pass, alongside the other 13 unverified young rows.

**Added to the E-2b checklist (registered here, 2026-08-06):**
1. Re-project all 14 flagged young rows from actual production, not
   pre-draft expectation — Harper first, since he now has a full season.
2. **Retire his `MKT_PIN` entry** once the projection is real: a
   rookie-hype pin on a second-year player is a stale artifact by
   definition.
3. Re-check the `rookie-proj` ×1.15 multiplier membership at the same
   time — it should cover only players with zero NBA games.
