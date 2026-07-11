---
name: fantasy-basketball
description: Analyze fantasy basketball decisions and run live drafts using the bundled hoops.py engine — z-score rankings, punt builds, trade evaluation, and a snake-draft tracker with best-available suggestions. Use this skill whenever the user asks about "fantasy basketball," "my fantasy team/roster," "fantasy draft," "mock draft," "who should I draft/pick," "punt build," "trade evaluation," "waiver wire," or "who should I start." Do NOT trigger for general NBA questions that are not about fantasy (real-game scores, news, career stats), and do NOT trigger for other fantasy sports (football, baseball).
---

# Fantasy Basketball (in-Claude analyzer and draft tool)

A self-contained fantasy basketball brain: no accounts, no APIs. `scripts/hoops.py` converts the projection table in `data/players.csv` into 9-cat z-score values and exposes rankings, punt builds, trade math, and a live snake-draft tracker. Your job is to run the right subcommands, then add the judgment the numbers don't carry — and to keep the data honest by refreshing it when stakes are real.

## Data honesty (read first)

`data/players.csv` is the research baseline (~210 players, 2025-26 per-game production, July 2026 rosters; method in data/RESEARCH.md, rebuilt 2026-07-11). It's a plain file; changing a row changes every ranking. Rows carry a `note` column — always surface these flags when recommending a flagged player. **Injury handling is mechanical (owner's rule)**: a note starting `out-` (season-ending injury) removes the player from every ranking and draft board automatically; `*-recovery` notes apply a 0.7 value downgrade and `*-risk` 0.85 (shown as `*` injury-adjusted values). During the daily refresh, encode injury news with exactly these note conventions — announced out-for-the-season → `out-<reason>`; returning from serious injury → `inj-<reason>-recovery`. Never present bundled numbers as live stats; say they're projections.

**Mandatory daily refresh (owner's rule).** Every hoops.py command checks `data/freshness.json` and prints a stale-data banner if the data wasn't refreshed today. That banner is BLOCKING for you: on the first fantasy request of a new day, before delivering any analysis, (1) web-search current NBA rosters/trades, injury reports, and rotation news for the players that matter to the request (the user's roster, draft-relevant tiers, any player being evaluated); (2) update the affected `players.csv` rows — team, stats, and `note` column; (3) record it: `python3 scripts/hoops.py freshness --stamp --note "<what changed>"` (the stamp validates pool completeness; `--force` bypasses with a stated reason). Only then run the analysis. If web search is unavailable, say so explicitly, deliver the analysis labeled as running on unrefreshed data, and do not stamp. **Boundary with the speed rule**: live-draft commands never print the stale banner and never trigger a refresh — staleness is checked once at `draft init`; if a draft crosses midnight, finish the draft and refresh after.

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

**Owner's league (defaults)**: 12 teams, 15-player rosters, 5 utility spots (exact non-util slot layout to confirm at draft init; owner provides their draft slot closer to the season). Deep-draft dynamics (owner's rule): through roughly the first 10 rounds (~120 picks) teams draft to fill position slots — weigh position need heavily there; from round ~11 on, shift to best-player-available and category specialists that extend the user's leads or rescue winnable categories.

1. **Before the draft**: confirm the user's slot and the exact roster-slot layout, and whether they're committed to a punt build (offer `rank --punt` comparisons if undecided). Web-search for injury updates on likely first-two-round picks. Then `python3 scripts/hoops.py draft init --teams 12 --size 15 --slot K [--punt ...]`.
2. **During — SPEED RULE (owner's rule, non-negotiable)**: the user is on a 60-second pick clock and needs suggestions within seconds, so a live-draft turn uses **exactly ONE command**: `python3 scripts/hoops.py draft turn "Name; Name; my:Name"` — semicolon-separated picks in draft order, the user's own prefixed `my:`. It logs everything (snake attribution automatic, nicknames like SGA/KAT/Dame resolve, bad names are reported without aborting) and emits the complete decision card in ~50ms: candidates annotated with the user's weakest categories, per-category rank vs the field, position counts, and the top rival's head-to-head edge. NEVER chain extra commands mid-draft (no separate best/matrix/status calls, no web searches, no CSV edits — the freshness refresh happens BEFORE the draft starts); `draft pick`/`--slot` remain for corrections between turns only.
3. **At the user's turn**: straight from the `turn` card, present **3–5 candidates** — each with a one-line rationale covering (a) synergy with the current build and (b) the field-relative gain: which category ranks the pick would climb (prefer categories where the user is mid-pack and can move over ones already won or lost). Mark exactly ONE as the top recommendation. **Position diversity is binding in the slot-filling phase (~rounds 1–10)**: candidates must span at least two (ideally three) position groups, and stop suggesting positions the roster is saturated at. **In the BPA/specialist phase (rounds ~11+) diversity yields to category fit** — an all-centers candidate list is fine if those are the best category plays; just note the saturation.
4. **Response protocol during drafts (owner's rule)**: when logging picks that are NOT the user's turn, reply with mirror lines ONLY (`✓ #N Player`) — no analysis, no prose. Full candidate cards fire exclusively when the user is on the clock. Recovery keywords: **SYNC** → report picks-logged count, last 3-6 picks, and next pick number; **RESYNC:** followed by a pasted pick list → wipe and rebuild the whole board from the paste.
5. **Corrections and ambiguity (owner's rule, learned 2026-07-11)**: treat a re-sent already-drafted name in a bulk feed as user error and skip it silently — NEVER infer it is a correction to the earlier pick; apply corrections only when explicitly formatted "Pick N, Player", and echo before/after in one line. For ambiguous names under the clock, assume the most fantasy-relevant match, log it, and flag the assumption in one line ("took OKC's Williams — say if you meant Mark") instead of stalling; the user can correct after.
6. **Opponent intel on demand**: `draft rosters` lists every team; `draft vs --team N` gives a head-to-head category comparison (useful in H2H leagues to spot rivals' weaknesses and in the endgame to pick fights the user can win).
7. **Corrections**: `draft undo` reverses the last pick; `draft fix N "Name" [--slot]` corrects any logged pick. Numeric prefixes in `draft turn` ("44- Herro") auto-correct when the number matches an existing pick — but 3+ corrections in one batch halts as suspected numbering drift; run `draft status` and verify before resending.
8. If a drafted player isn't in the pool, `draft turn` logs an UNKNOWN placeholder automatically — snake attribution never drifts. Between turns (or post-draft), add the player's row to `data/players.csv`, then `draft fix N "Name"`. Never edit the CSV while the user is on the clock.

## Analysis rules

- **Commit.** One recommendation with the deciding factor named; alternatives get one line, not equal billing.
- **Punt coherence.** In a punt build, judge every pickup/pick by the KEPT categories; call out when a tempting player's value lives in the punted ones.
- **Trade verdicts** combine the script's net z with roster fit: a negative-net trade can still be right if it consolidates strength into scarce categories the user is contesting. Say which consideration wins and why.
- **H2H vs roto**: z-totals map cleanly to roto; in head-to-head, weight swing categories (close weekly margins) and streaming flexibility more heavily.
- **Never invent live data.** Season stats, injury news, and schedules beyond the CSV come from web search, labeled as such.

## Edge cases

- **A drafted player is missing from the ~210-player pool** → offer to add rows to `data/players.csv` for the missing players (same columns; estimates are fine if labeled in `note`).
- **Draft state exists from a previous session** (`draft_state.json` in cwd) → `draft status` first and confirm whether to resume or `draft init --force`.
- **Yahoo/ESPN integration requests** → this tool is deliberately offline; the user can paste rosters as text and you analyze via `profile`/`trade`. (A Yahoo OAuth client was removed from this repo — see git history — after Yahoo's portal refused fantasy API scope.)

## When NOT to use this skill

- General NBA chat (real standings, awards, career stats) → answer normally or web-search; no hoops.py call.
- Multi-option dilemmas the user wants formally deliberated ("council: should I punt assists?") → the claude-council skill owns the deliberation; use this skill to fetch the numbers it debates.

## Provenance and maintenance

Authored 2026-07-11. Volatile facts: `data/players.csv` holds the top-210 2026-27 baseline (see data/RESEARCH.md) and rots continuously — refresh via web search before real decisions; z-scores are computed over this pool, so pool edits shift all values. Re-verify the engine with `python3 scripts/hoops.py rank --top 3` (expect Jokic-tier players on top) and the draft loop with `draft init --slot 1 --force` + a few picks in a scratch directory. Update when: the CSV schema changes, Yahoo default categories change, or a season rollover makes the bundled projections misleading.
