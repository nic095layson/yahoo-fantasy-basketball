# 🏀 Fantasy Basketball for Claude Code

An **in-Claude fantasy basketball analyzer and draft tool**. No accounts, no
API keys, no OAuth — a bundled projection dataset plus a z-score engine
(`scripts/hoops.py`), and a Claude Code skill that turns natural conversation
("who should I take here?") into rankings, punt-build math, trade verdicts,
and a live snake-draft assistant.

## Synopsis

Three layers:

1. **Data — `data/players.csv`.** ~125 players with per-game 9-cat
   projections and injury/rookie notes. It's a plain CSV: edit a row, add a
   player, and every ranking updates. Claude refreshes stale rows via web
   search before real decisions.
2. **Engine — `scripts/hoops.py`** (stdlib-only Python). Converts projections
   into volume-weighted z-scores across FG%, FT%, 3PTM, PTS, REB, AST, ST,
   BLK, TO (turnovers inverted). Commands: `rank` (punt-aware, position
   filters), `profile` (category strengths of any roster), `trade` (per-category
   deltas + net), `find`, and a `draft` tracker (snake order, best-available,
   build profile, undo).
3. **Judgment — Claude** via `.claude/skills/fantasy-basketball/SKILL.md`:
   when to fire, how to run a live draft turn-by-turn, and the rules that keep
   advice honest (commit to one recommendation, respect punt coherence, flag
   injury notes, never invent live stats).

## Quick start

```bash
git clone https://github.com/nic095layson/yahoo-fantasy-basketball
cd yahoo-fantasy-basketball

python3 scripts/hoops.py rank --top 20              # who's valuable
python3 scripts/hoops.py rank --punt "FT%,TO"       # punt-build rankings
python3 scripts/hoops.py trade --send "Luka Doncic" --get "Sabonis,Derrick White"
```

Live draft:

```bash
python3 scripts/hoops.py draft init --teams 12 --slot 5 --punt "FT%"
python3 scripts/hoops.py draft pick "Jokic"           # team inferred from snake order
python3 scripts/hoops.py draft pick "Giannis" --mine  # your pick (sanity-checked)
python3 scripts/hoops.py draft best                   # best available + your needs
python3 scripts/hoops.py draft status                 # your build + rank vs field
python3 scripts/hoops.py draft matrix                 # all teams' category totals
python3 scripts/hoops.py draft vs --team 8            # head-to-head vs one opponent
python3 scripts/hoops.py draft rosters                # every team's picks so far
```

Every pick is attributed to its team automatically (snake order), so the
tracker holds all 12 rosters — recommendations weigh not just your build but
where you rank per category against the field, and which fights are winnable.

## With Claude Code

Open this folder in Claude Code and just talk:

> "I'm drafting 5th in a 12-team 9-cat league tonight and thinking about
> punting FT%. Run my draft with me."

The skill handles the bookkeeping (logging picks, best-available math) and
Claude adds the judgment (build fit, injury flags, when to reach).

## Repo layout

```
├── README.md
├── data/players.csv                  # editable projection pool (~125 players)
├── scripts/hoops.py                  # z-score engine + draft tracker
├── .claude/skills/fantasy-basketball/SKILL.md
└── evals/evals.json
```

## Notes

- Values are z-scores over the bundled pool: +1.0 ≈ one standard deviation
  above average in a category. FG%/FT% are weighted by attempt volume.
- Draft state lives in `./draft_state.json` (start over with `draft init --force`).
- The projections are a **baseline, not live data**. A daily freshness rule
  is enforced: every command warns until the data has been refreshed that day
  (Claude web-searches rosters/injuries, updates the CSV, then runs
  `freshness --stamp`). The `note` column flags injuries and rookie estimates.
- History: this repo briefly contained a Yahoo Fantasy API OAuth client
  (see git history) — scrapped after Yahoo's developer portal refused to
  grant fantasy scope to new apps.
