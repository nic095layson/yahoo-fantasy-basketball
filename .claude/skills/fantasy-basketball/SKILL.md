---
name: fantasy-basketball
description: Manage and analyze the user's Yahoo Fantasy Basketball leagues through the bundled yfb.py CLI — rosters, standings, weekly head-to-head matchups, and waiver-wire pickups. Use this skill whenever the user asks about "my fantasy team," "my roster," "fantasy basketball," "Yahoo fantasy," "waiver wire," "free agents," "who should I start," "who should I drop/pick up," "my matchup," or "league standings." Do NOT trigger for general NBA questions that are not about the user's fantasy league (real-game scores, trade rumors, career stats), and do NOT trigger for other fantasy sports (football, baseball).
---

# Fantasy Basketball (Yahoo)

Turns Claude Code into a fantasy basketball assistant for the user's Yahoo leagues. All data access goes through one stdlib-only script — `scripts/yfb.py` at this project's root — which handles Yahoo OAuth2, token refresh, and the Fantasy Sports API's deeply nested JSON. Your job is to run the right subcommands, then add the analysis the raw numbers don't give: start/sit calls, pickup targets, punt strategy, matchup math.

## Procedure

1. **Check auth state first**: `python3 scripts/yfb.py status`. If credentials or token are missing, walk the user through setup (see Setup below) — do not attempt live calls before that.
2. **Resolve keys before data calls.** Most commands need a `league_key` or `team_key`. Get them once with `python3 scripts/yfb.py leagues` and `... standings --league <league_key>` (standings lists every team_key). Remember them for the rest of the session.
3. **Fetch, then analyze.** Pull the data with the relevant subcommand, then answer the user's actual question. Add `--json` when you want machine-readable output to reason over instead of a table.

| User asks about | Run |
|---|---|
| Their leagues | `python3 scripts/yfb.py leagues` |
| Standings / playoff race | `python3 scripts/yfb.py standings --league <league_key>` |
| Their roster / who to start | `python3 scripts/yfb.py roster --team <team_key>` |
| This week's matchup | `python3 scripts/yfb.py matchup --team <team_key>` |
| Waiver wire / pickups | `python3 scripts/yfb.py free-agents --league <league_key>` |

4. **Demo mode.** Append `--demo` to any data command to use bundled sample data — for testing the pipeline, demonstrating the tool, or when the user has no Yahoo credentials yet.

## Analysis rules

- **Commit to a recommendation.** "Start Booker over Jaquez" beats a list of considerations. Name the deciding factor in one line.
- **Respect the format.** Head-to-head category (`scoring_type: head`) is won in swing categories — check the matchup command's per-category leader column before advising; roto is won on season-long balance. Never give H2H advice to a roto team.
- **Injury status is load-bearing.** Flag any rostered player with status `O`, `INJ`, or `DTD` when discussing lineups; check `status` in roster output before recommending a start.
- **TO is inverted.** Lower turnovers win the category — the matchup command already accounts for this; don't double-invert.
- **Never guess live data.** Player stats, game schedules, and injury news beyond what the API returns must come from a web search, clearly labeled — do not invent numbers.

## Setup (first run)

1. User creates a Yahoo app at https://developer.yahoo.com/apps/ — Confidential Client, Redirect URI `https://localhost:8080`, API permission "Fantasy Sports" (read).
2. Export `YAHOO_CLIENT_ID` and `YAHOO_CLIENT_SECRET` (or write `~/.config/yfb/credentials.json`).
3. Run `python3 scripts/yfb.py auth` — the user opens the printed URL, approves, then pastes back the `localhost:8080` URL from the browser's address bar (the "can't connect" error page is expected; the script extracts the `code=` value). Tokens cache to `~/.config/yfb/token.json` (chmod 600) and auto-refresh.

Never print, log, or commit the client secret, access token, or refresh token. The token file and credentials file are gitignored; keep it that way.

## Edge cases

- **No credentials and the user just wants to explore** → use `--demo` and say clearly the data is sample data.
- **API returns 401 after refresh** → token is revoked; re-run `auth`.
- **User is in multiple leagues** → ask which one once, then stick with it for the session.
- **Trade evaluation** → the API gives rosters and ownership, not projections; fetch both rosters, then reason about category impact explicitly, flagging that projections are your judgment, not Yahoo data.

## When NOT to use this skill

- General NBA chat (real standings, awards, career stats) → answer normally or web-search; no yfb.py call.
- Complex multi-option decisions the user wants deliberated ("council: should I trade Luka?") → the claude-council skill owns the deliberation; use this skill only to fetch the data it debates.

## Provenance and maintenance

Authored 2026-07-11 against Yahoo Fantasy Sports API v2 (`fantasysports.yahooapis.com/fantasy/v2`, OAuth2 at `api.login.yahoo.com`). Volatile facts: NBA game code `nba` resolves to the current season's game_key; stat-id → category map in `yfb.py` (`STAT_LABELS`) reflects the default 9-cat H2H settings. Re-verify with `python3 scripts/yfb.py --demo leagues` (pipeline) and a live `leagues` call (API contract). Update when: Yahoo changes OAuth endpoints, the JSON envelope shape changes (`merge_fragments`/`iter_collection` break), or a new NBA season changes the game_key.
