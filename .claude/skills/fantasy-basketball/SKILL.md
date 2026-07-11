---
name: fantasy-basketball
description: Analyze fantasy basketball decisions and run live drafts using the bundled hoops.py engine — z-score rankings, punt builds, trade evaluation, and a snake-draft tracker with best-available suggestions. Use this skill whenever the user asks about "fantasy basketball," "my fantasy team/roster," "fantasy draft," "mock draft," "who should I draft/pick," "punt build," "trade evaluation," "waiver wire," or "who should I start." Do NOT trigger for general NBA questions that are not about fantasy (real-game scores, news, career stats), and do NOT trigger for other fantasy sports (football, baseball).
---

# Fantasy Basketball (in-Claude analyzer and draft tool)

A self-contained fantasy basketball brain: no accounts, no APIs. `scripts/hoops.py` converts the projection table in `data/players.csv` into 9-cat z-score values and exposes rankings, punt builds, trade math, and a live snake-draft tracker. Your job is to run the right subcommands, then add the judgment the numbers don't carry — and to keep the data honest by refreshing it when stakes are real.

## Data honesty (read first)

`data/players.csv` is a bundled BASELINE (~125 players, per-game projections, authored 2026-07-11). It's a plain file; changing a row changes every ranking. Rows carry a `note` column (`inj-*`, `rookie-proj`) — always surface these flags when recommending a flagged player. Never present bundled numbers as live stats; say they're projections.

**Mandatory daily refresh (owner's rule).** Every hoops.py command checks `data/freshness.json` and prints a stale-data banner if the data wasn't refreshed today. That banner is BLOCKING for you: on the first fantasy request of a new day, before delivering any analysis, (1) web-search current NBA rosters/trades, injury reports, and rotation news for the players that matter to the request (the user's roster, draft-relevant tiers, any player being evaluated); (2) update the affected `players.csv` rows — team, stats, and `note` column; (3) record it: `python3 scripts/hoops.py freshness --stamp --note "<what changed>"`. Only then run the analysis. If web search is unavailable, say so explicitly, deliver the analysis labeled as running on unrefreshed data, and do not stamp.

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
2. **During**: the user announces picks conversationally ("Jokic went", "I'll take Booker"). Log every one immediately with `draft pick "Name"` — the picking team is inferred from snake order automatically, so **every team's roster builds as the draft runs**. Add `--mine` on the user's own picks as a sanity check (it warns if the snake math disagrees, which catches missed picks), and `--slot N` for out-of-order picks (keepers, traded picks). Names are fuzzy-matched; if the script reports ambiguity, ask which player was meant.
3. **At the user's turn** (owner's rule): run `draft best` (candidates annotated with the user's two weakest kept categories) and `draft matrix` (per-category rank vs the whole field), then present **3–5 candidates** — each with a one-line rationale covering (a) synergy with the current build and (b) the field-relative gain: which category ranks the pick would climb (prefer categories where the user is mid-pack and can move over ones already won or lost). Mark exactly ONE as the top recommendation. **Position diversity is mandatory**: the candidate list must span at least two (ideally three) different position groups, never mostly one position — check the roster's filled/unfilled slots (PG, SG, SF, PF, C×2, G, F, Utils in a standard Yahoo roster) and stop suggesting positions the roster is saturated at.
4. **Opponent intel on demand**: `draft rosters` lists every team; `draft vs --team N` gives a head-to-head category comparison (useful in H2H leagues to spot rivals' weaknesses and in the endgame to pick fights the user can win).
5. **Corrections**: `draft undo` reverses the last pick (any team's).
6. If a drafted player isn't in the pool (deep-league picks), say so, log nothing, and continue — but note the skipped pick means snake attribution is off by one from then on; log remaining picks with explicit `--slot`.

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
