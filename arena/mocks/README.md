# Mock post-mortem harnesses

Reproduction code for the graded mock drafts in `arena/results/`.

**Why this directory exists (2026-08-03).** `LEDGER.md` states that its
tallies are "machine-derived from the simulation artifacts." On 2026-08-03
an adversarial verifier found a defective LEDGER row (mock 13 carried a
bot's numbers instead of the owner's); it was caught by *re-deriving* all 17
rows from the retained artifacts. That re-derivation was only possible
because the harnesses happened to still exist in an ephemeral session
scratchpad — they were not in the repo, and `arena/results/*.json` is
gitignored. The integrity property the LEDGER claims was therefore not
actually reproducible from a fresh clone.

**Backfill complete (2026-08-04, owner-approved):** the full harness set for
mocks 10–30 — every `season_sim_mockNN.py` and every retained `mockNN_cf.py` —
is now committed here. Every LEDGER row is re-derivable from a fresh clone.
Note the older sims read draft states from the original session's uploads
path (`STATE` constant at the top of each file); point it at your own copy
of the corresponding `draft_state_N.json` to reproduce.

## Files

- `live_retro.py <mock> <stage>`, `live_deckcard.py <mock> <deck> <out> [--punt-log]`,
  `live_advisor.py <mock> <deck> <out>`, `live_survival.py <mock> <deckcard.json> <out> [more…]`,
  `live_debrief.py <mock> <out.md>` — the live-room grading set (2026-09-22), generalized
  from the mock-51 scripts below to a mock-number argument, tolerant of poolless opponent
  picks (a human drafts a name the pool lacks: that seat plays short, the names are recorded).
  `live_retro.py 51 final|replay|hindsight` reproduces `m51_*.json` byte-for-byte; mock 52's
  outputs are `m52_*.json` and `debrief_2026-09-22_mock52_slot10.md`. Per-mock config
  (pools drafted against, the punt box as the owner drove it, click moments) sits at the top
  of `live_retro.py` / `live_deckcard.py` / `live_advisor.py`.

- **Insert-at-# integrity (mock 53, 2026-09-22).** `insert_integrity.py <deck.html> <events.json> <truth.json> <out.json>` replays the owner's whole tool log (feeds, halts, UNKNOWN fixes, undos, inserts) through the deck ENGINE headlessly, builds the same board from scratch in the Yahoo recap's order, and compares picks/seats, every roster, every seat's category ranks, the category matrix and the ΔECW card at all owner turns; it also runs `hoops.insert_pick` on the exact pre-insert boards. `live_replay_dom.mjs <deck.html> <events.json> <out.json>` drives the REAL page in headless Chromium (Playwright, pre-installed at /opt/pw-browsers) through the same events, asserting each echo line and recording the on-the-clock text and page errors after every event — the reproduction of the countdown bug the fix closes. Results: `m53_insert_integrity.json`, `m53_dom_replay_unfixed.json`, `m53_dom_replay.json`. Mock 53 itself is graded with the same live-room set on its own pool tag (`live_retro.MOCKS[53]`, v25) — outputs `m53_*.json` — and `live_debrief_generic.py <mock> <out.md>` writes the debrief from those files with no mock-specific prose (the mock-52 `live_debrief.py` stays as the record of that room). `live_retro.py` grades every mock on the pool it was drafted against: v23 is pinned to git rev f724435 (regenerated as `m52_players_v23.csv` when missing), so mocks 51/52 keep reproducing after the pool grew to 330 rows.

- `season_sim_mock27.py` — headline simulation. Rebuilds all 12 rosters from
  the uploaded draft state, runs `arena.simulate_seasons` at 6,000 seasons ×
  seeds [11, 23, 47], and reports champ%/playoff%/kept-total per team plus
  the owner's per-category z-sums and ranks.
- `season_sim_mock28.py`, `mock28_cf.py` — same pair for mock 28. The m28
  CF file additionally carries the two **oracle** arms behind LEDGER §5:
  `CF5_ecw_greedy_oracle` and `CF7_kept_greedy_oracle`. Both walk the owner's
  13 turns and take the best legal later-drafted player by their objective —
  identical hindsight, opposite objectives (34.58% vs 0.28%). They are upper
  bounds, not strategies: they know exactly when every player will be taken.
- `mock27_cf.py` — counterfactual arms. `python3 mock27_cf.py ARM [ARM...]`,
  or no args for every arm. Each arm is a set of **pairwise legal** swaps:
  the alternative must have been drafted strictly *later* than the owner pick
  it replaces (asserted in `build()`; an illegal arm is refused, not run —
  see `CF4_steals_repair`). 6,000 seasons × seeds [11, 23].

## Swap-arm screening (added 2026-08-03)

Before running a pairwise arm, check that the alternative is **not also an
owner pick**. Mock 28's `keyonte_to_harris` swapped two of the owner's own
picks (#140 and #149), which only reorders the owner's roster and reproduces
the baseline to the last decimal. `build_seq()` enforces legality (alt drafted
strictly later) but cannot tell a degenerate arm from a real one — that check
is on the author. See LEDGER §3.

## Reproduction notes

- Both scripts read the draft state from the uploads path recorded in their
  `STATE` constant. Point that at your own copy of the state JSON.
- Counterfactual arms must be paired against an `as_drafted` run at the
  **same seed/season config** as the arms — not against the 3-seed headline.
  Mixing them overstates every delta (0.23pp in mock 27).
- The per-category ranks these scripts report are unweighted 13-player
  z-sums. The simulator itself scores *lineup-weighted weekly means*; the two
  disagree in ~4 of 9 categories on a typical roster. See
  `debrief_2026-08-03_mock27_slot4.md`.
- `veto_dom_check.mjs <deck.html> <draft_state.json> <out.json> [picksToKeep]`
  (2026-09-28) drives the real page in headless Chromium: imports the state,
  then asserts no `JUDGMENT.doNotDraft` name is on the decision card, the
  Best-available table still lists it marked DO NOT DRAFT, a `my:` pick of it
  logs the warning and Undo takes it back, and no page error fired. Record:
  `arena/results/veto_dom_check_2026-09-28.json` (mock 51 at #63, where
  Porziņģis had been the 5th row).
- **Mock 54 (2026-09-28, slot 10).** Graded with the live-room set on its own pool tag
  (`live_retro.MOCKS[54]`, v28 — `data/players.csv` as of the 9/28 pull build, pinned to git rev
  b150541 and regenerated as `m54_players_v28.csv` when missing; v25 is now pinned the same way to
  rev 2e217f9 as `m53_players_v25.csv`, because the live file moved on 9/23 and 9/28). The deck card
  is replayed from the deck the owner drafted against (`live_deckcard.py 54 rev:b150541:docs/draft-deck.html`,
  pre-veto); `MOCKS[54]` sets no `veto`, so the replay is the card the owner saw. Outputs `m54_*.json`;
  `m54_tool_vs_truth.json` is the owner's tool log replayed into its final board and diffed against
  Yahoo's recap (13 positions off after an UNKNOWN was followed by a fresh feed instead of a
  `N- Name` fix); `live_debrief_generic.py` renders that diff as a "Tool-state integrity" section
  whenever the file exists, and its survival and limits wording is now room-generic.
- **Full-control DOM check (system validation 2026-09-29).** `full_dom_check.mjs <deck.html> <draft_state_54.json> <out.json>`
  drives the real page in headless Chromium through every interactive control it has — setup fields
  and their echo, invalid-config refusals, LIVE/MOCK toggles, the nine punt chips, Daily sweep panel,
  Import (chooser, invalid JSON, missing keys, a full 156-pick state), Export (download), Copy, the
  two-click Reset, the feed (Log + Enter + numbered fix + live hint), Undo, Insert-at-#, Resync, all
  five tabs, every Best-available filter / lens / header sort / cat chip / drill / row click, the
  Take buttons, the TARGET button, the head-to-head select, the tooltip, a full LIVE replay of the
  mock-54 room with the card's #1 taken at all 13 owner turns, a punt-declared room, and a full MOCK
  room through "Draft them" — and cross-checks every number the page shows against the engine
  functions the page itself carries (strip counts vs availablePool, matrix cells vs categoryRanks,
  rosters vs totalValue, head-to-head vs rosterTotals, Mkt column vs marketRanks, the card's top-5
  vs rankCard(decwScores) over the owner pool at every owner turn). Result:
  `arena/results/full_dom_check_2026-09-29.json`; report: kit
  `report/after-reports/after-report-2026-09-29-validation.md`. Since 2026-09-29 it is a
  GATE (owner decision D6): exit 1 on any failed assertion or page error, run on every built
  page before it is republished (kit DATA-PULL.md §7 step 5b).
- **Third implementation of the weekly model (2026-09-29, owner decision D5).**
  `decw_reference.mjs <deck.html> <states_dir> <out.json>` dumps the engine's own ΔECW, blend
  score and rankCard ordering for EVERY candidate at every committed owner turn (the parity
  gate's 143), the owner's roster model (mu/var and daily-fill start rates) at each, and the
  dfHash parity vectors; `decw_third.py <deck.html> <states_dir> <reference.json> <out.json>
  [--approx-cdf]` is a from-specification Python implementation of the whole chain (hash,
  daily fill, weekly model, category-win probabilities, percentile blend, card sort) that
  imports neither arena.py nor hoops.py and never executes the page, compared against that
  dump. Two runs: exact Φ (math.erf) to show the model agrees, and the engine's polynomial
  Φ to show the numbers agree to floating-point. Results in `arena/results/decw_third_2026-09-29*.json`.
- **D54 fixes (2026-09-28).** `d54_dom_check.mjs <deck.html> <events.json> <truth.json> <state.json> <out.json>`
  drives the real page in headless Chromium: (A) replays the owner's mock-54 tool log
  (`arena/data/events/m54_tool_events.json`, built from the log's feeds, raw UNKNOWN texts,
  inserts, undos and numbered fixes) through the feed box and diffs the resulting board
  against Yahoo's recap — with the D54-2 auto-fix the 13-position drift collapses to the one
  UNKNOWN the owner never fixed (#97), the still-open warning fires and the strip names it;
  (B) imports the recap at 129 picks, feeds #130–#134 so the advisor's two-turn hysteresis
  runs as it did live, types `my: Ajay Mitchell` and reads the card-gap hint (D54-1), logs it
  and reads the log line, and reads the dead-category trap sentence (D54-3). Record:
  `arena/results/d54_dom_check_2026-09-28.json`. `punt_arms.py <mock> <from_pick> <CATS> [--veto]`
  is the paired championship test behind D54-3: as drafted vs follow-card from pick N vs a
  punt-STEERED follow-card (kept-cats-only value and ΔECW), per-seed, with the bar registered in
  the output (`m54_punt_arms.json`, `m54_punt_arms_veto.json`).
- **Mock 55 (2026-09-28, slot 10).** The first room graded with this set that is NOT a public Yahoo room:
  the deck's own MOCK mode against the 11 modeled league-mates, drafted on deck v30 (rev 28266d8, veto
  live). `live_retro.MOCKS[55]` = `dict(tags=("v28",), veto=True, room="cast")` — lines are v28
  (players.csv byte-unchanged b150541 → 28266d8); `room="cast"` switches `live_debrief_generic.py`'s
  room wording (title, source, LEDGER eligibility, limits) — public rooms render unchanged (mock 54's
  debrief regenerates byte-identical below the title). State rebuilt from the deck's recap with
  `hoops.py draft resync` (156/156 names and seats match, no UNKNOWN). Deck card replayed from the deck
  drafted against (`live_deckcard.py 55 rev:28266d8:docs/draft-deck.html arena/results/m55_deckcard_v28.json`);
  survival pooled with the 51–54 deck cards. Stage order matters: `arms` reads `m55_hindsight.json`.
- **Mock 56 (2026-09-29, slot 10).** Public Yahoo room drafted on deck v31/v32 (same pool, sha
  `c0bf82bf4d39`, and the same engine — only the resolver's dot-folding differs between the two), the
  owner's stated "how I would actually want to draft" (Haliburton / Lillard / Kyrie at the point).
  `live_retro.MOCKS[56]` = `dict(tags=("v31",), veto=True)`; the v31 pool is pinned to rev `e2b45ed`
  and regenerated as `m56_players_v31.csv` when missing. State rebuilt from Yahoo's recap with
  `hoops.py draft resync` (156/156 "Last, First" lines resolved, no UNKNOWN, seats match the snake,
  md5 `e5305ff3b4a1b5c04a18c65e2d67e56c`). Deck card replayed from the deck drafted against
  (`live_deckcard.py 56 rev:e2b45ed:docs/draft-deck.html arena/results/m56_deckcard_v31.json`);
  survival pooled with the 51–55 deck cards; `arms` reads `m56_hindsight.json`. Tool-state
  integrity: the owner's tool log (`arena/data/events/m56_tool_events.json` — 162 feeds and one undo:
  bare surnames where the echo said "assumed over" / "only X left" / "skipped", the four raw UNKNOWN
  texts with their `N- Name` fixes, the #120 "Reed" undo, the "Mitchell" HALT) replayed through the
  real page with `live_replay_dom.mjs` on BOTH the v31 and the v32 page: 163 events, 0 echo misses,
  0 clock mismatches, 0 page errors, all 156 positions equal to the recap on both —
  `arena/results/m56_tool_vs_truth.json`. **Repeat-name audit** (owner question, same day):
  `repeat_names_audit.mjs <deck.html> <states_dir> <mock> <other mocks csv> <out.json> [watch names]`
  re-ranks the available pool at every owner turn with the deck's own engine under the actual
  roster, each other room's owner roster at that turn (substituted in and removed from any
  opponent holding those men), an empty roster, and value-only / ΔECW-only orders, and records the
  watch-list names' value, ΔECW and market ranks per turn — `m56_repeat_names_audit.json`; the
  six-room draft-slot and card-🎯 history of the same names is `m56_repeat_names_history.json`.
  **Re-calibration on v33 (2026-09-29, owner: "conduct re-calibration testing as well with these
  new player rankings").** After the re-derivation pass (Yahoo official positions, nine lines
  re-derived, four rows added; deck v33, rev `a3b4d31`, pool sha `6efb01cd772b`) every live room was
  re-graded on the NEW pool without touching its own record: `live_retro.py <mock> <stage> --tag v33`
  grades on `POOLS["v33"]` (`players_v33.csv`, regenerated from rev a3b4d31 when missing) and reads
  and writes `m<mock>_<stage>_v33.json` beside the room's own files; `live_deckcard.py <mock>
  rev:a3b4d31:docs/draft-deck.html arena/results/m<mock>_deckcard_v33.json` replays each room's
  card on the v33 page; `live_survival.py 56 m56_deckcard_v33.json m56_survival_v33.json
  m51…m55_deckcard_v33.json` pools the survival calibration across the six rooms on v33; and
  `repeat_names_audit.mjs … arena/results/m56_repeat_names_audit_v33.json` re-runs the mock-56
  audit on v33 with the same watch list. The before/after reading lives in the kit's
  `report/after-reports/after-report-2026-09-29-final-check.md`.
  Finding: the #1 changes at 9 of 13 turns under other rosters (11 of 13 against an empty roster);
  the late-round SET of names recurs because rooms price them 30–80 slots below the deck's value
  (kit report `after-report-2026-09-29-draft56.md` §7).
- **Mock 57 (2026-09-29, slot 10).** Public Yahoo room, the owner's first on deck v34 (rev `0dfbe77`
  — the concise card and YOUR PICK banner; data, engine and judgment blocks byte-identical to v33/`a3b4d31`,
  so the v33 pool is this room's own pool). `live_retro.MOCKS[57]` = `dict(tags=("v33",), veto=True)`;
  no punt declared (`PUNT_TIMELINES[57] = [(0, [])]`). State rebuilt from Yahoo's recap with `hoops.py
  draft resync` (156/156 resolved, no UNKNOWN, seats match the snake, owner roster = the recap's "My
  Team", md5 `de73d84f7f60ae858153f801f1319d59`). Deck card replayed from the deck drafted against
  (`live_deckcard.py 57 rev:0dfbe77:docs/draft-deck.html arena/results/m57_deckcard_v33.json`);
  `live_advisor.py` likewise; survival pooled with the 51–56 deck cards (`m57_survival.json`); `arms`
  reads `m57_hindsight.json`; follow-the-card counterfactual rosters graded in
  `m57_followcard_grade.json` (as drafted 35.23% / ECW 5.271 rank 1; follow-card self-consistent 52.96%
  / 5.678; White at #39 alone 42.63%, Bridges at #87 alone 41.01%, both 47.21%). Tool-state integrity:
  the owner's tool log (`arena/data/events/m57_tool_events.json` — 159 events: 154 direct feeds, the two
  raw UNKNOWN texts "Gianis" and "Giffey" with their `6- Giannis Antetokounmpo` / `19- Josh Giddey`
  fixes, the duplicate "OG" feed the deck skipped) replayed through the real v34 page with
  `live_replay_dom.mjs`: 0 echo misses, 0 clock mismatches, 0 page errors, all 156 positions equal to
  the recap, owner roster identical — `arena/results/m57_tool_vs_truth.json` (the D54 "#19 is still
  UNKNOWN" reminder fired live when #20 was fed over the open #19). Repeat-name audit re-run with the
  mock-56 watch list plus this room's late names (`m57_repeat_names_audit.json`): the #1 changes at 10 of
  13 turns under other rooms' rosters (11 of 13 against an empty roster); Lopez, Cameron Johnson, Braun
  and Eason made no Top-5 in this room. **Finding (data):** the draft room's recap shows FEWER positions
  than the pool for 29 of the 156 drafted men (the pool copies Yahoo's 9/28 rankings-page paste; e.g.
  Edwards PG,SG in the room vs PG,SF,SG in the pool) — kit report `after-report-2026-09-29-draft57.md`
  §7, decision D57-1. The owner's roster-balance question (LEAN / LINEUP CAP flags vs the card) is
  answered from the code in that report's §6; the deck's own `dailyFillWeights` on this roster starts
  every man 99–100% of his game days under either position set.
- **Chromium harnesses and TMPDIR (found 2026-09-29).** Run `full_dom_check.mjs`, `live_replay_dom.mjs`,
  `d54_dom_check.mjs` and `veto_dom_check.mjs` with the DEFAULT temp dir. With `TMPDIR` pointed at the
  session scratchpad (a ~100-character path) Playwright puts Chromium's user-data-dir there and the
  launch dies with `SIGTRAP` before any event (three of three attempts; the browser's Unix-socket paths
  exceed the socket path limit). The same command with `TMPDIR` unset passed every time (four of four).
