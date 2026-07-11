---
name: fantasy-basketball
description: Analyze fantasy basketball decisions and run live drafts using the bundled hoops.py engine — z-score rankings, punt builds, trade evaluation, and a snake-draft tracker with best-available suggestions. Use this skill whenever the user asks about "fantasy basketball," "my fantasy team/roster," "fantasy draft," "mock draft," "who should I draft/pick," "punt build," "trade evaluation," "waiver wire," or "who should I start." Do NOT trigger for general NBA questions that are not about fantasy (real-game scores, news, career stats), and do NOT trigger for other fantasy sports (football, baseball).
---

# Fantasy Basketball (in-Claude analyzer and draft tool)

A self-contained fantasy basketball brain: no accounts, no APIs. `scripts/hoops.py` converts the projection table in `data/players.csv` into 9-cat z-score values and exposes rankings, punt builds, trade math, and a live snake-draft tracker. Your job is to run the right subcommands, then add the judgment the numbers don't carry — and to keep the data honest by refreshing it when stakes are real.

## Data honesty (read first)

`data/players.csv` is a bundled BASELINE (~125 players, per-game projections, authored 2026-07-11). Before a real draft or a real trade decision, web-search current injury news and depth-chart changes for the specific players involved, and edit the CSV where it's stale — it's a plain file; changing a row changes every ranking. Rows carry a `note` column (`inj-*`, `rookie-proj`) — always surface these flags when recommending a flagged player. Never present bundled numbers as live stats; say they're projections.

## Analysis commands

Run from the project root:

| Question | Command |
|---|---|
| Overall or punt rankings | `python3 scripts/hoops.py rank --top 30 [--punt "FT%,TO"] [--pos C]` |
| What does this roster look like | `python3 scripts/hoops.py profile --players "Name1,Name2,..." [--punt ...]` |
| Should I make this trade | `python3 scripts/hoops.py trade --send "A,B" --get "C" [--punt ...]` |
| Find a player / check the pool | `python3 scripts/hoops.py find <name-fragment>` |

Category convention: FG% and FT% are volume-weighted; TO is already inverted (positive z = fewer turnovers). +1.0 z ≈ one standard deviation above average.

## Live draft protocol

1. **Before the draft**: ask for team count, the user's slot, roster size, and whether they're committed to a punt build (offer `rank --punt` comparisons if undecided). Web-search for injury updates on likely first-two-round picks. Then `python3 scripts/hoops.py draft init --teams N --slot K [--punt ...]`.
2. **During**: the user announces picks conversationally ("Jokic went", "I'll take Booker"). Log every one immediately: `draft pick "Jokic"` for other teams, `draft pick "Booker" --mine` for the user's. Names are fuzzy-matched; if the script reports ambiguity, ask which player was meant.
3. **Approaching the user's turn** (the tracker prints their next pick number): run `draft best` and `draft status`, then recommend ONE player with a one-line reason tied to build fit — positional balance and category needs from the status profile, not just the top value. Offer one alternate.
4. **Corrections**: `draft undo` reverses the last pick.
5. If a drafted player isn't in the pool (deep-league picks), say so, log nothing, and continue — the tracker only needs the players who matter for value comparisons.

## Analysis rules

- **Commit.** One recommendation with the deciding factor named; alternatives get one line, not equal billing.
- **Punt coherence.** In a punt build, judge every pickup/pick by the KEPT categories; call out when a tempting player's value lives in the punted ones.
- **Trade verdicts** combine the script's net z with roster fit: a negative-net trade can still be right if it consolidates strength into scarce categories the user is contesting. Say which consideration wins and why.
- **H2H vs roto**: z-totals map cleanly to roto; in head-to-head, weight swing categories (close weekly margins) and streaming flexibility more heavily.
- **Never invent live data.** Season stats, injury news, and schedules beyond the CSV come from web search, labeled as such.

## Edge cases

- **User's league is deeper than the ~125-player pool** → offer to add rows to `data/players.csv` for the missing players (same columns; estimates are fine if labeled in `note`).
- **Draft state exists from a previous session** (`draft_state.json` in cwd) → `draft status` first and confirm whether to resume or `draft init --force`.
- **Yahoo/ESPN integration requests** → this tool is deliberately offline; the user can paste rosters as text and you analyze via `profile`/`trade`. (A Yahoo OAuth client was removed from this repo — see git history — after Yahoo's portal refused fantasy API scope.)

## When NOT to use this skill

- General NBA chat (real standings, awards, career stats) → answer normally or web-search; no hoops.py call.
- Multi-option dilemmas the user wants formally deliberated ("council: should I punt assists?") → the claude-council skill owns the deliberation; use this skill to fetch the numbers it debates.

## Provenance and maintenance

Authored 2026-07-11. Volatile facts: `data/players.csv` reflects 2025-26-season-informed projections (~125 players) and rots continuously — refresh via web search before real decisions; z-scores are computed over this pool, so pool edits shift all values. Re-verify the engine with `python3 scripts/hoops.py rank --top 3` (expect Jokic-tier players on top) and the draft loop with `draft init --slot 1 --force` + a few picks in a scratch directory. Update when: the CSV schema changes, Yahoo default categories change, or a season rollover makes the bundled projections misleading.
