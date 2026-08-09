# 🏀 Fantasy Basketball for Claude Code

An **in-Claude fantasy basketball analyzer and draft tool**. No accounts, no
API keys, no OAuth — a bundled projection dataset plus a z-score engine
(`scripts/hoops.py`), and a Claude Code skill that turns natural conversation
("who should I take here?") into rankings, punt-build math, trade verdicts,
and a live snake-draft assistant.

## Synopsis

Three layers:

1. **Data — `data/players.csv`.** the pool is whatever the file holds
   (currently 246 rows) with per-game 9-cat
   projections and injury/rookie notes (top-200 consensus research baseline). It's a plain CSV: edit a row, add a
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
python3 scripts/hoops.py draft init --teams 12 --size 13 --slot 4   # 12x13 = 156 picks
python3 scripts/hoops.py draft turn "Jokic; my:Wemby; SGA"   # THE live-draft command:
#   logs every announced pick (yours prefixed my:), snake attribution automatic,
#   nicknames + typos resolve, and it emits the full decision card in ~50ms —
#   candidates, category ranks vs the field, feasibility/team-stack flags.
python3 scripts/hoops.py draft fix 15 "Donovan Mitchell"     # correct any pick
python3 scripts/hoops.py draft matrix                        # all teams' category totals
python3 scripts/hoops.py draft vs --team 8                   # head-to-head vs one opponent
```

(`draft pick/best/status/rosters/undo` exist for between-turn use; during a
live draft, `draft turn` is the one-command-per-turn workflow.)

Every pick is attributed to its team automatically (snake order), so the
tracker holds all 12 rosters — recommendations weigh not just your build but
where you rank per category against the field, and which fights are winnable.

## The Draft Deck

The live draft-night board is the published Draft Deck artifact — a
self-contained page built from this repo by `scripts/build_deck.py`
(`docs/draft-deck.html`). **On draft night the deck is the board and the
ledger**; `scripts/hoops.py` is the fallback board, the punt-coherence layer
(the deck's ordering is punt-blind by design), and the state-integrity layer.
See `.claude/skills/fantasy-basketball/SKILL.md` — "Draft-night surface".

## With Claude Code

Open this folder in Claude Code and just talk:

> "I'm drafting 5th in a 12-team 9-cat league tonight and thinking about
> punting FT%. Run my draft with me."

The skill handles the bookkeeping (logging picks, best-available math) and
Claude adds the judgment (build fit, injury flags, when to reach).

## Repo layout

```
├── README.md
├── data/players.csv                  # editable projection pool (currently 246 rows)
├── scripts/hoops.py                  # z-score engine + draft tracker
├── .claude/skills/fantasy-basketball/SKILL.md
└── evals/evals.json
```

## Notes

- Values are z-scores over the bundled pool: +1.0 ≈ one standard deviation
  above average in a category. FG%/FT% are weighted by attempt volume.
- Draft state lives in `./draft_state.json` (start over with `draft init --force`).
  Writes are atomic and keep one `.bak`; `draft resync "<pasted picks>"` rebuilds
  a board from a paste, `draft status --tail N` prints the recent-picks tail.
- The projections are a **baseline, not live data**. A daily freshness rule
  is enforced: analysis commands warn until the data has been refreshed that
  day (live-draft commands are exempt by design — staleness is checked at
  `draft init`)
  (Claude web-searches rosters/injuries, updates the CSV, then runs
  `freshness --stamp`). The `note` column flags injuries and rookie estimates.
- History: this repo briefly contained a Yahoo Fantasy API OAuth client
  (see git history) — scrapped after Yahoo's developer portal refused to
  grant fantasy scope to new apps.
