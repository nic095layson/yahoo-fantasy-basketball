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
- **Mock 58 (2026-09-30, slot 10).** Public Yahoo room, the owner's second on the concise card, drafted on
  deck v35 (rev `6426a59` — the 9/30 daily-pull build with the role pass; pool sha `3db2c63af0c3`), the veto
  live. `live_retro.MOCKS[58]` = `dict(tags=("v35",), veto=True)` (new pool tag `v35`, pinned to `6426a59`);
  no punt declared (`PUNT_TIMELINES[58] = [(0, [])]`). State rebuilt from Yahoo's recap with `hoops.py draft
  resync` (156/156 resolved, no UNKNOWN, seats match the snake, owner roster = the recap's "My Team", md5
  `84547309be00afd40ed15adcd72ff367`). **First room graded on the league's real bracket** (E14 shipped the
  same day; 8 of 12, no byes): as drafted 36.75% / ECW 5.667 rank 1 (next 4.932), favored 11/11; follow-card
  self-consistent 40.89% / 5.744 (Maxey at #10, Jalen Williams at #39, LaVine at #82); Jalen Williams at #39
  alone 40.17%, Derrick White at #39 (hindsight best, +0.119 cats/week) 40.81% — `m58_followcard_grade.json`,
  `m58_arms.json`. Deck card replayed from the page drafted against (`live_deckcard.py 58
  rev:6426a59:docs/draft-deck.html arena/results/m58_deckcard_v35.json`): 🎯 taken 9 of 13, every pick on the
  Top-5; the four off-card picks were 0.006/0.009/0.017/0.005 behind. `live_advisor.py` likewise (no advice
  at any turn; AST/PTS watched at #58, hysteresis held). Survival pooled with the 51–57 deck cards
  (`m58_survival.json`: this room 48 rows, Brier 0.189 vs base 0.246; BUY NOW 2 of 8 survived, TOSS-UP 5 of
  16, quiet 20 of 24). Tool-state integrity: the owner's tool log (`arena/data/events/m58_tool_events.json`
  — 158 events: 155 direct feeds incl. fifteen shared-surname tokens, the UNKNOWN "Gianis" with its `6-
  Giannis Antetokounmpo` fix, and the HALTED "Murray" feed the deck refused because Jamal Murray was already
  drafted) replayed through the real v35 page with `live_replay_dom.mjs`: 0 echo misses, 0 clock mismatches,
  0 page errors, all 156 positions equal to the recap, owner roster identical, four autosave reloads with no
  drift — `arena/results/m58_tool_vs_truth.json`. Repeat-name audit (`m58_repeat_names_audit.json`): the #1
  changes at 10 of 13 turns under other rooms' rosters (8 of 13 against an empty roster); of the mock-56
  watch names only Braun reached a Top-5 (once). **Harness fix (2026-09-30):** `stage_arms` built its
  follow-the-card chain from a pool that skipped the owner veto (the replay/hindsight pool applies it), so the
  chain had a vetoed Porziņģis at #82; fixed, re-run; mocks 55–57's chains carried no vetoed name and stand.
  **Finding (data):** 29 of 156 drafted men again show fewer positions in the draft room than the pool
  (superset every time; kit report `after-report-2026-09-30-draft58.md` §7 — D-G3).
- **Mock 59 (2026-10-01, slot 10).** Public Yahoo room, the owner's third on the concise card, drafted on
  deck v37 (rev `b3986f8` — the 10/01 daily-pull build; pool sha `09fe6d433264`, 334 rows), the veto live.
  `live_retro.MOCKS[59]` = `dict(tags=("v37",), veto=True)` (new pool tag `v37`, pinned to `b3986f8`); no
  punt declared (`PUNT_TIMELINES[59] = [(0, [])]`). State rebuilt from Yahoo's recap with `hoops.py draft
  resync` (155 of 156 resolved; one UNKNOWN at #126, Yang Hansen, no pool row on either plane; seats match
  the snake, owner roster = the recap's "My Team", md5 `0bfcbba343380d83e2436ed1125695d3`). **First live
  room from the real seat not to finish first**: as drafted 20.38% / ECW 5.092 rank 2 (next
  5.260), favored 10/11; follow-card self-consistent 39.18% / 5.660 (Tyrese Maxey at #10, Derrick White at #39, Jakob Poeltl at #63, Damian Lillard at #82, Miles Bridges at #87, Day'Ron Sharpe at #106);
  Derrick White at #39 alone 27.14%; Poeltl at #82 alone 23.06%; the survival-aware pair (LaVine at
  #82, Poeltl at #87) 26.36% — `m59_followcard_grade.json`, `m59_arms.json`. Deck card replayed from the
  page drafted against (`live_deckcard.py 59 rev:b3986f8:docs/draft-deck.html arena/results/m59_deckcard_v37.json`):
  🎯 taken 5 of 13, Top-5 row 9 of 13; four picks off the Top-5 (Kessler #39 card #47 0.164 behind, Sharpe #82
  #12 0.048, Edgecombe #87 #20 0.078, Queta #106 #52 0.244); hindsight prices those turns at +0.237, +0.112,
  +0.107 and +0.215 cats/week. `live_advisor.py`: ADVISE PTS·AST from #63 on (the two-turn hysteresis met at
  the #63 pre-pick moment), the finish ranked 11th weekly in both; advice only. Survival pooled with the 51–58
  deck cards (`m59_survival.json`: this room 52 rows, Brier 0.183 vs base 0.241; BUY NOW 2 of
  6 survived, TOSS-UP 5 of 13, quiet 24 of 33). Tool-state integrity: the owner's tool log
  (`arena/data/events/m59_tool_events.json` — 161 events: 156 feeds incl. sixteen shared-surname tokens, three
  UNKNOWN feeds with two fixed by number, four Insert-at-# corrections (Jalen Green #97, Keegan Murray #118,
  RJ Barrett #121, Rui Hachimura #128), the HALTED "Johnson" feed, one undo) replayed through the real v37
  page with `live_replay_dom.mjs`: [] echo misses, 0 clock mismatches, [] page errors, all
  156 positions equal to the recap, owner roster identical — `arena/results/m59_tool_vs_truth.json`.
  **Finding (owner-visible):** the history box is static text, so after an insert the earlier lines keep
  their old numbers and seats — two owner picks (Queta "#105 → Seat 9", Washington "#128 → Seat 8") never
  read as the owner's and got no card echo, and the standing UNKNOWN keeps "#125" in its name at #126
  (kit report `after-report-2026-10-01-draft59.md` §9a — D59-1, the owner's proposal). **Instrument added:**
  `arena/mocks/target_wait.py` (owner's question: does the 🎯 wait?) — across mocks 56–59, 🎯s passed on
  with a market rank 24+ slots below the pick were still there at the next owner turn 4 of 5 times
  and two turns on 1 of 5; near-price 🎯s 5 of 10 and 0 of 9 —
  `arena/results/target_wait_2026-10-01.json` (report §9b — D59-2). Repeat-name audit
  (`m59_repeat_names_audit.json`): the #1 changes at 10 of 13 turns under other rooms' rosters (10 of 13
  against an empty roster); Poeltl on the Top-5 at three turns, Braun at one. **Finding (data):** 28 of 155
  drafted men show fewer positions in the draft room than the pool (superset every time; report §7 — D-G3).
  **Harness item (D59-5):** `live_retro.py`'s card port still breaks exact blend ties by name order (its
  pre-D51R-4 rule); the page breaks them by ΔECW. One turn here (#111: port Vassell, page Gillespie, blend
  0.9835 both); the report's §3 reads the page (`live_deckcard.py`), the owner took Gillespie (hindsight-best).
- **Mock 59 re-graded on v39 (2026-10-01, calibration only).** D-WO1-1 (d), the owner's decision: the
  thirteen wide kit-vs-deck lines made one line on both planes (deck rev `bc908f6`, pool sha `1ecfb66bdcef`,
  `data/players.csv` md5 `85a682b6c556`; ten deck rows changed, the kit's three in the kit). The room's own
  record stays v37's. New pool tag `v39` (`POOLS["v39"]`, `V39_REV = "bc908f6"`; not any room's own pool) and
  `live_retro.py 59 <stage> --tag v39` wrote `m59_replay/final/hindsight/forecast/arms_v39.json` beside the
  v37 files; the six counterfactual rosters in `m59_followcard_grade_v39.json`; the card replayed on the v39
  page with `live_deckcard.py 59 docs/draft-deck.html arena/results/m59_deckcard_v39.json`. As drafted
  20.38% → 15.21% / ECW 5.092 → 4.877 (rank 2 both; next 5.260 → 5.272), favored 10 → 10 of 11;
  follow-card self-consistent 39.18% → 37.13% (Tyrese Maxey at #10, Derrick White at #39, Jarrett Allen at #63, Zach LaVine at #82, Josh Hart at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111); White at #39 alone 27.14% → 21.26%; the
  survival-aware pair 26.36% → 15.54%; Poeltl at #82 alone 23.06% → 13.28%; LaVine at #87 alone 23.32% →
  17.82%. Card: 🎯 changes at 4 of 13 turns (#58 Anunoby → Pritchard, #82 Poeltl → LaVine, #106 Poeltl →
  Lendeborg, #130 Vassell → Mamukelashvili); Lillard at #63 card #2 → #32 (his line 24.0 → 17.0 points);
  Sharpe at #82 card #12 → #5; Kessler at #39 #47 → #39. Hindsight: Lillard at #63 legal rank 2 → 43
  (Pritchard +0.265 cats/week there, +0.047 on v37); Edgecombe at #87 11 → 5; the #39 miss
  +0.237 → +0.251. Forecast ρ, shipped card, mean of 13: 0.815 → 0.838. **Reading:** the deep-🎯
  Poeltl of mocks 56–59 (D59-2) was partly the deck's own 14.5-point line, now 11.5 on both planes — Poeltl
  at #82 alone grades below as drafted on v39 (13.28% vs 15.21%, rank 3) and the survival-aware
  pair is a wash (15.54%); the D59-2 advice line rests on `target_wait.py`'s survival counts, which this
  re-grade does not touch. **Test fixture:** `test_card.py`'s D51R-4
  availability probe (state_54 #34) stopped producing an urgent read on the reconciled lines; the 9/29 pin
  scan repeated on the v39 page (16 states × 208 owner turns: four urgent reads, three withheld on
  availability) re-pointed it to mock31 #64 (Zion 0.78, un-vetoed) — 68 of 68. Planes gate after the sync:
  lines 171 (was 184), propagation 0 with the thirteen rows waived by name (`--planes-waive`) at the v39
  build and in `check_planes.py`.
- **Deck v40 (2026-10-01, D59-1 + D59-2).** Owner proposals from mock 59, red-first on both planes.
  **D59-1** — `insertPick` (page) and `hoops.insert_pick` rename a shifted standing UNKNOWN to its new
  number; history pick lines carry {pick, kind, note|raw} and the engine's `relabelLog` re-renders
  every earlier line from the state after a shift (number, seat, "(YOU)"), reporting picks moved onto /
  off the owner's seat so the app (`applyShift`) can echo the card as of now. New harness
  `history_dom_check.mjs <deck.html> <events.json> <state.json> <out.json>` drives the real page through a
  tool log and asserts the FINAL history: on v39 mock 59's Queta "#105 → Seat 9", Washington "#128 →
  Seat 8" and "UNKNOWN #125" failed; on v40 19 of 19 checks pass, 0 page errors
  (`history_dom_check_2026-10-01_v40.json`). Undo of an insert is not built (D40-3). **D59-2** — the
  two-pick 🎯: engine `pairDecision(rows, surv, decwGiven)` scores pair_i = ΔECW_i + Σ_j s_j·Π(1−s_k)·
  ΔECW(j|i) + residual over the Top-5 and moves the MARKER (never the blend50 order) when the gain ≥
  `PAIR_MIN_GAIN` 0.01 and row 1's survival ≥ `PAIR_WAIT_MIN` 0.60; `hoops.pair_decision` is the twin
  (test_card parity on five fixtures); `PAIR_MARKER` switches marker vs advice-only. **Pre-registered
  experiment** (`pair_experiment_2026-10-01_design.md`, written first; `live_retro.py <mock> pairarms`
  per room — survival priced off the page the owner drafted against, baked Yahoo price else the pre-F8
  market position; `pair_experiment.py` aggregates → `pair_experiment_2026-10-01.json`): eight public
  rooms (51, 52, 53, 54, 56, 57, 58, 59), blend-🎯 chain vs two-pick-🎯 chain, strict pairwise, real
  bracket, 6,000 seasons × seed sets (11, 23, 47) and (5, 17, 29). Mean title odds blend 45.83 /
  46.21 vs pair 45.69 / 45.89; marker moved at 6 turns (mock 53 #15: Austin Reaves now instead of Jalen Williams (+0.045); mock 53 #58: OG Anunoby now instead of Payton Pritchard (+0.010); mock 54 #34: Derrick White now instead of Jalen Williams (+0.015); mock 56 #82: Jakob Poeltl now instead of Tari Eason (+0.061); mock 59 #34: Derrick White now instead of Jalen Williams (+0.024); mock 59 #63: Payton Pritchard now instead of Jakob Poeltl (+0.031));
  per room pair better 1/1, worse 1/1, identical 5; the blend chain reproduced every
  room's recorded arms. **Verdict: BAR FAILED — PAIR_MARKER false, advice only** → v40 ships `PAIR_MARKER = false`. Mock 59's #82 by
  the rule: Bridges-now better by 0.007, under the bar — all five rows were deep (§9b restated).
- **The survival model against the owner's own league (2026-10-01, D40-2).** Owner upload: Yahoo's
  pre-draft analyst ranks for 2025-26 (Dan Titus 10/16, 199 names) — kept verbatim as
  `arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt` (the rank cell equals the row number).
  `league_survival.py <out.json>` joins them to `draft_boards.json["2025-26"]` (154 of 156 picks match;
  Tatum and Jović sit outside the top 199), builds rows at the owner's thirteen turns (every ranked man
  still on the board within 60 ranks of the pick, predicted to the next owner turn with the engine's
  own `survival_prob` form and `_norm_cdf_as`), and scores the shipped parameters against a (k, floor)
  grid, leave-one-turn-out and the base rate — `arena/results/league_survival_2025-26.json`. Result:
  719 rows, realized 0.821; Brier shipped 0.1450 vs base 0.1472 vs best fit 0.1397 (k 0.20, floor 16);
  LOTO 0.1417 vs 0.1451 — under the 0.01 bar fixed before the run, so the shipped parameters stay. The
  model is too pessimistic at every band in this league (quiet rows survived 447 of 481, BUY NOW 21 of
  53, men 24+ ranks below the pick 407 of 434); in the 30-rank window it is worse than the base rate
  (0.2337 vs 0.2158). League profile: median pick minus rank −1; Robby (−16.5) and Will (−13.2) reach,
  the owner (+4.3) and Kevin (+8.6) take value as it falls. Kit report
  `after-report-2026-10-01-league-survival.md`; decisions D-LS-1..3.
- **Mock 60 (2026-10-02, slot 10).** Public Yahoo room, the owner's fourth on the concise card and the first with
  the D59-1 re-numbered history and the D59-2 advice line live, drafted on deck v42 (rev `6ae36ab` — the Friday-morning
  second-pull build; pool sha `75a4994b4a59`, 334 rows; v41's values identical), the veto live. `live_retro.MOCKS[60]`
  = `dict(tags=("v42",), veto=True)` (new pool tag `v42`, pinned to `6ae36ab`; `PAGE_REV[60]`); no punt declared
  (`PUNT_TIMELINES[60] = [(0, [])]`). State rebuilt from Yahoo's recap with `hoops.py draft resync` (156 of 156
  resolved, no UNKNOWN; seats match the snake, owner roster = the recap's "My Team", md5 `9023d2d25d41be108230a1a90f77c3fc`).
  **Back to first from the real seat, the card followed at 11 of 13 turns**: as drafted 33.02% / ECW 5.419
  rank 1 (next 4.935), favored 11/11; follow-card self-consistent 43.14% / 5.676 (Jamal Murray at #15, Anthony Davis at #34, Payton Pritchard at #63, Zach LaVine at #82, Mikal Bridges at #87, Daniel Gafford at #106);
  Gafford at #106 alone 39.49%; the advice line's roster (Murray at #15, White at #39 as drafted) 32.31% —
  `m60_followcard_grade.json`, `m60_arms.json`. Deck card replayed from the page drafted against
  (`live_deckcard.py 60 rev:6ae36ab:docs/draft-deck.html arena/results/m60_deckcard_v42.json`): 🎯 taken 11 of 13, Top-5
  row 11 of 13; two picks off the card — Durant at #15 (card #6, 0.015 behind Jalen Williams, who waited to #34; hindsight
  5th of 296) and Murray-Boyles at #106 (card #87, 0.405 behind PJ Washington, who waited to #130; hindsight 58th of 212,
  Gafford +0.181 cats/week, +6.47 title points). **D59-2's first live room** (`m60_advice_reads.json`, the pair
  twin on the page's rows): the advice fired once, at #15 — "Jamal Murray now, Derrick White next turn (82% to survive):
  +0.039" — silent at every other turn for the stated reason; the pair rule replayed as the marker moved it at two turns
  and finished at the blend chain's own numbers (5.676, 43.14%) — advice-only verdict holds. **Wording
  defect (D60-3):** the twin's sentence names the highest-ΔECW partner regardless of survival (on the port's rows: "Kevin
  Durant next turn (1% to survive)"). `live_advisor.py`: the room-relative advisor read an assists lean at three owner turns and advised at two (#63, #82 — `m60_advisor.json` new_advise;
  this line said "never advised" until the mock-61 grade re-read the file on 2026-10-06); the
  finish is the most balanced of the nine rooms (nothing worse than 9th weekly). Survival pooled with the 51–59 deck
  cards (`m60_survival.json`: this room 50 rows, Brier 0.175 vs base 0.236 — the best out-of-sample room yet; BUY NOW
  2 of 7 survived, TOSS-UP 5 of 13, quiet 24 of 30). Tool-state integrity: the owner's tool log
  (`arena/data/events/m60_tool_events.json` — 156 events: 155 feeds incl. fourteen shared-surname tokens, one
  Insert-at-# correction (Derik Queen #95), no UNKNOWN, no halt, no undo; a page resume after #47 replayed as one session)
  replayed through the real v42 page with `live_replay_dom.mjs`: 0 echo misses, 0 clock mismatches,
  0 page errors, all 156 positions equal to the recap, owner roster identical — `m60_tool_vs_truth.json`; D59-1's
  re-numbering did on the live page what the mock-59 report asked for. **Finding (data):** the draft room's position
  display matched the pool on all 156 drafted men — the first room since the 10/01 position sync (D-ADP-3; D-G3 closable,
  D60-4). **Harness item (D59-5, re-put as D60-1):** the port's name-order tie-break differs from the page at four turns
  here (#15 rank 5 vs 6; the 🎯 at #106, #130, #154). Target-wait with this room added (`target_wait_2026-10-02.json`):
  deep 🎯s passed on were still there at the next owner turn 6 of 7 times, two turns on 2 of 7;
  near-price 5 of 10 and 0 of 9. Repeat-name audit (`m60_repeat_names_audit.json`): the #1 changes at 12
  of 13 turns under other rooms' rosters (12 of 13 against an empty roster); Gafford on the Top-5 at two turns, Braun
  at one, Poeltl at none. Debrief `debrief_2026-10-02_mock60_slot10.md`; kit report `after-report-2026-10-02-draft60.md`.
- **Mock 61 (2026-10-06, slot 10).** Public Yahoo room, the owner's fifth on the concise card, drafted on deck v44 (rev `583435c`
  — the 2026-10-06 daily-pull build; pool sha `48456b3b18ff`, 335 rows), the veto live. Page identified by replay: the owner's four
  "off the card" echoes reproduce on the v44 pool at three decimals (0.237 / 0.363 / 0.228 / 0.019) and two of them miss on v43's
  (0.364, 0.226); v45 (same pool, 10/6 prices) was published after the room closed. `live_retro.MOCKS[61]` = `dict(tags=("v44",), veto=True)`
  (new pool tag `v44`, pinned to `583435c`; `PAGE_REV[61]`); no punt declared (`PUNT_TIMELINES[61] = [(0, [])]`). State rebuilt from
  Yahoo's recap with `hoops.py draft resync` (156 of 156 resolved, no UNKNOWN; seats match the snake, owner roster = the recap's "My Team",
  md5 `051fee6c1160f7fc75452b08fc3826dc`). **Second from the real seat, the card followed at 9 of 13 turns**: as drafted 16.66% / ECW 4.940
  rank 2 (next 5.366, seat 4), favored 10/11; follow-card self-consistent 34.49% / 5.513 (Jarrett Allen at #63, Zach LaVine at #82, Isaiah Hartenstein at #87, Sandro Mamukelashvili at #106, Cason Wallace at #111, Yaxel Lendeborg at #130, Saddiq Bey at #135);
  the card at the four off-card turns alone 30.99% — `m61_followcard_grade.json`, `m61_arms.json`. Deck card replayed from the page
  drafted against (`live_deckcard.py 61 rev:583435c:docs/draft-deck.html arena/results/m61_deckcard_v44.json`): 🎯 taken 9 of 13, Top-5
  row 10 of 13; four picks off the card, none of the 🎯s recovered later — Lillard at #63 (card #65, 0.237 behind Jarrett Allen, who went #72;
  hindsight 68th of 252, Herro +0.329 cats/week, +9.07 title points; the 🎯 +4.35), Murray-Boyles at #106 (card #79, 0.363
  behind Lendeborg; +4.81), Davion Mitchell at #111 (card #48, 0.227 behind Lendeborg, who lasted to #133; +4.03), Herbert Jones at #135
  (card #4, 0.019 behind Mamukelashvili; +0.23). **The advice line's second live room** (`m61_advice_reads.json`, the pair twin on the
  page's rows and the port's): fired at no turn — the 🎯 under the 0.60 wait floor at five turns, the best pair at seven; the pair rule
  replayed as the marker finished at 34.49% against the blend chain's 34.49% (seed set 1) — advice-only verdict holds.
  `live_advisor.py`: see the debrief's advisor line (the room-relative read spoke only at the last pick). Survival pooled with the 51–60
  deck cards (`m61_survival.json`: this room 51 rows, Brier 0.168 vs base 0.248 — the best out-of-sample room yet; BUY NOW
  1 of 7 survived, TOSS-UP 6 of 14, quiet 21 of 30). Tool-state integrity: the owner's tool log
  (`arena/data/events/m61_tool_events.json` — 159 events: 158 feeds incl. sixteen shared-token feeds (thirteen surnames, three first names:
  Jalen, Miles, Tre), one UNKNOWN feed ("Gianis" at #5) fixed with "5- Giannis Antetokounmpo", one undo at #137, no insert, no halt; a page
  reload after #156 with nothing to replay) replayed through the real v44 page with `live_replay_dom.mjs`: 0 echo misses,
  0 clock mismatches, 0 page errors, all 156 positions equal to the recap, owner roster identical — `m61_tool_vs_truth.json`.
  **Finding (data):** the draft room's position display matched the pool on all 156 drafted men, teams too — the second room running
  (D60-4 stands). **Harness item (D60-1, re-put as D61-3):** the port's name-order tie-break differs from the page at six turns here
  (#63 rank 66 vs 65, #111 47 vs 48, the 🎯 at #130, the Top-5 order at #39, #106, #154). Target-wait with this room added
  (`target_wait_2026-10-06.json`): deep 🎯s passed on were still there at the next owner turn 8 of 10 times, two turns on
  3 of 9; near-price 5 of 11 and 0 of 10. Repeat-name audit (`m61_repeat_names_audit.json`): the #1 changes at 10
  of 13 turns under other rooms' rosters (11 of 13 against an empty roster); Gafford on the Top-5 at one turn, Braun at one, Poeltl at
  none. Debrief `debrief_2026-10-06_mock61_slot10.md`; kit report `after-report-2026-10-06-draft61.md`.
- **Mock 62 (2026-10-06, slot 10).** The deck's own MOCK mode against the 11 league-mates — the first room on the REAL
  2026-27 seating (JUDGMENT.draftOrder, owner directive 2026-10-06: Oblena, Noah, Will, Robby, Kyle, Martin, John, JCo,
  Kevin, owner at 10, Cayas, Hegi), drafted on deck v46 (rev `441bba6`; pool sha `48456b3b18ff` = the v44 pool with the
  10/6 prices baked), the veto live. `live_retro.MOCKS[62]` = `dict(tags=("v44",), veto=True, room="cast")`; `PAGE_REV[62]
  = "441bba6"`; no punt declared (`PUNT_TIMELINES[62] = [(0, [])]`). State = the owner's exported draft state verbatim
  (156 picks, every name a pool row, snake-consistent, `cast` = the real order; md5 `f185f50d5dcbe3f0ba7108e314837677`);
  no recap and no tool log exist for a MOCK, so no DOM replay. **The card followed at 13 of 13 turns — the first
  thirteen-for-thirteen room**: as drafted 18.05% / ECW 4.987 rank 2 (next 5.284), favored 10/11
  (`m62_followcard_grade.json`, `m62_arms.json`; the retro port's follow-card chain differs only by the D60-1 tie-break at #130/#135 and grades 18.22%). Deck card
  replayed from the v46 page (`live_deckcard.py 62 rev:441bba6:docs/draft-deck.html arena/results/m62_deckcard_v44.json`):
  🎯 taken 13 of 13. Hindsight's largest single swap: Chet Holmgren at #15 (+0.103 cats/week). **The advice line's
  third live room** (`m62_advice_reads.json`): fired at four turns (#15, #34, #39, #82) — its first room with more than one — and the
  owner took the 🎯 each time; the 'now' men as single swaps grade -0.10 / +1.30 / -1.76 / +1.48 title points, all four together
  +1.44; the pair rule replayed as the marker finished at 17.49% against the blend chain's 18.22% (seed set 1).
  Survival pooled with the 51–61 deck cards (`m62_survival.json`: this room 48 rows, Brier 0.196, mean predicted
  0.577 vs realized 0.521 — the chips ran optimistic against the cast; BUY NOW 0 of 4 survived, TOSS-UP
  3 of 9, quiet 22 of 35). **Cast fidelity** (`m62_cast_fidelity.json`, new): the market-leaning profiles
  (Noah, Robby, Hegi) drafted market fallers and sat behind on value, the value-leaning ones (Oblena, Kevin, Martin, Cayas)
  ahead on value; Kevin took eight guards; loyalty fired on 11 of the 17 loyalty names still on the board at the manager's
  turn. Target-wait with this room added (`target_wait_2026-10-06b.json`): deep 🎯s passed on were still there at the next owner
  turn 8 of 10 times (no 🎯 was passed here — every turn is `taken_now`). Repeat-name audit
  (`m62_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (11 of 13 against an
  empty roster); Gafford on the Top-5 at two turns (taken at #135), Braun at two, Poeltl at none. Debrief
  `debrief_2026-10-06_mock62_slot10.md`; kit report `after-report-2026-10-06-draft62.md`.
- **Mock 63 (2026-10-07, slot 10).** The deck's own MOCK mode against the 11 league-mates on the REAL 2026-27 seating, drafted on deck v47
  (rev `fca8f7c`, the 10/7 daily-pull build; the v44 pool with the 10/6 Yahoo prices baked), the veto live. `live_retro.MOCKS[63]` =
  `dict(tags=("v44",), veto=True, room="cast")`; `PAGE_REV[63] = "fca8f7c"`; no punt declared (`PUNT_TIMELINES[63] = [(0, [])]`). State = the
  owner's exported draft state verbatim (156 picks, every name a pool row, snake-consistent, `cast` = the real order; md5 `d9516e0c5d41aaaaa5148abfdf103c22`);
  no recap and no tool log exist for a MOCK, so no DOM replay. **The card's 🎯 taken at 13 of 13 turns**:
  as drafted 23.33% (rank 2) / ECW 5.169 rank 1 (next 5.121), favored 10/11 (`m63_followcard_grade.json`, `m63_arms.json`;
  the retro port's self-consistent follow-card chain grades 23.33%). Deck card replayed from the v47 page
  (`live_deckcard.py 63 rev:fca8f7c:docs/draft-deck.html arena/results/m63_deckcard_v44.json`). Hindsight's largest single swap: Chet Holmgren at #15 (+0.060 cats/week).
  **Advice line** (`m63_advice_reads.json`, page reading): fired at #58 (Tyler Herro now); the 'now' men as single swaps grade +0.38 title points; the pair rule replayed as the marker finished at 23.71% against the blend chain's 23.33% (seed set 1).
  Survival pooled with the 51–64 deck cards (`m63_survival.json`: this room 48 rows, Brier 0.213, mean predicted 0.608 vs realized 0.521 — optimistic against the cast again; BUY NOW 0 of 3 survived, TOSS-UP 4 of 9, quiet 21 of 36).
  **Cast fidelity** (`m63_cast_fidelity.json`): loyalty fired on 10 of the 17 loyalty names drafted by anyone. Repeat-name audit
  (`m63_repeat_names_audit.json`): the #1 changes at 11 of 13 turns under other rooms' rosters (11 of 13 against an empty roster); Gafford on the Top-5 at 3 turn(s), Braun at 0, Poeltl at 1.
  Debrief `debrief_2026-10-07_mock63_slot10.md`; kit report `after-report-2026-10-07-cast.md` (§4).
- **Mock 64 (2026-10-07, slot 10).** The deck's own MOCK mode against the 11 league-mates on the REAL 2026-27 seating, drafted on deck v47
  (rev `fca8f7c`, the 10/7 daily-pull build; the v44 pool with the 10/6 Yahoo prices baked), the veto live. `live_retro.MOCKS[64]` =
  `dict(tags=("v44",), veto=True, room="cast")`; `PAGE_REV[64] = "fca8f7c"`; no punt declared (`PUNT_TIMELINES[64] = [(0, [])]`). State = the
  owner's exported draft state verbatim (156 picks, every name a pool row, snake-consistent, `cast` = the real order; md5 `5abfd25ab6c579d7f12e49808ffb89aa`);
  no recap and no tool log exist for a MOCK, so no DOM replay. **The card's 🎯 taken at 2 of 13 turns** — off the card at #10 Jayson Tatum (card #18), #15 Kevin Durant (card #3), #34 Bam Adebayo (card #11), #39 Kyrie Irving (card #5), #63 Paolo Banchero (card #21), #82 Jaden McDaniels (card #6), #87 Jabari Smith Jr. (card #13), #106 Herbert Jones (card #4), #111 Collin Gillespie (card #4), #135 Cason Wallace (card #2), #154 Stephon Castle (card #80):
  as drafted 7.63% (rank 3) / ECW 4.555 rank 3 (next 5.357), favored 7/11 (`m64_followcard_grade.json`, `m64_arms.json`;
  the retro port's self-consistent follow-card chain grades 18.97%). Deck card replayed from the v47 page
  (`live_deckcard.py 64 rev:fca8f7c:docs/draft-deck.html arena/results/m64_deckcard_v44.json`). Hindsight's largest single swap: Jalen Johnson at #10 (+0.154 cats/week).
  **Advice line** (`m64_advice_reads.json`, page reading): fired at #15 (Kevin Durant now), #34 (Franz Wagner now), #39 (Franz Wagner now), #58 (Alperen Sengun now); the 'now' men as single swaps grade +0.00 / +1.44 / +1.54 / -1.37 title points, together -0.11; the pair rule replayed as the marker finished at 18.10% against the blend chain's 18.97% (seed set 1).
  Survival pooled with the 51–64 deck cards (`m64_survival.json`: this room 53 rows, Brier 0.196, mean predicted 0.575 vs realized 0.509 — optimistic against the cast again; BUY NOW 0 of 4 survived, TOSS-UP 5 of 14, quiet 22 of 35).
  **Cast fidelity** (`m64_cast_fidelity.json`): loyalty fired on 11 of the 17 loyalty names drafted by anyone. Repeat-name audit
  (`m64_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (11 of 13 against an empty roster); Gafford on the Top-5 at 1 turn(s), Braun at 2, Poeltl at 0.
  Debrief `debrief_2026-10-07_mock64_slot10.md`; kit report `after-report-2026-10-07-cast.md` (§4).
- **Mock 65 (2026-10-07, slot 10).** The deck's own MOCK mode against the 11 league-mates on the REAL 2026-27 seating, drafted on deck v47
  (rev `fca8f7c`, the 10/7 daily-pull build; the v44 pool with the 10/6 Yahoo prices baked), the veto live. `live_retro.MOCKS[65]` =
  `dict(tags=("v44",), veto=True, room="cast")`; `PAGE_REV[65] = "fca8f7c"`; no punt declared (`PUNT_TIMELINES[65] = [(0, [])]`). State = the
  owner's exported draft state verbatim (156 picks, every name a pool row, snake-consistent, `cast` = the real order; md5 `c5bd2cf159fdd1969244eb12b2de8782`);
  no recap and no tool log exist for a MOCK, so no DOM replay. **The card's 🎯 taken at 13 of 13 turns**:
  as drafted 23.19% (rank 2) / ECW 5.174 rank 1 (next 5.099), favored 10/11 (`m65_followcard_grade.json`, `m65_arms.json`;
  the retro port's self-consistent follow-card chain grades 23.19%). Deck card replayed from the v47 page
  (`live_deckcard.py 65 rev:fca8f7c:docs/draft-deck.html arena/results/m65_deckcard_v44.json`). Hindsight's largest single swap: Chet Holmgren at #15 (+0.117 cats/week).
  **Advice line** (`m65_advice_reads.json`, page reading): fired at #39 (Franz Wagner now); the 'now' men as single swaps grade +1.40 title points; the pair rule replayed as the marker finished at 22.97% against the blend chain's 23.19% (seed set 1).
  Survival pooled with the 51–64 deck cards (`m65_survival.json`: this room 48 rows, Brier 0.207, mean predicted 0.617 vs realized 0.542 — optimistic against the cast again; BUY NOW 0 of 2 survived, TOSS-UP 4 of 9, quiet 22 of 37).
  **Cast fidelity** (`m65_cast_fidelity.json`): loyalty fired on 12 of the 17 loyalty names drafted by anyone. Repeat-name audit
  (`m65_repeat_names_audit.json`): the #1 changes at 11 of 13 turns under other rooms' rosters (12 of 13 against an empty roster); Gafford on the Top-5 at 1 turn(s), Braun at 2, Poeltl at 0.
  Debrief `debrief_2026-10-07_mock65_slot10.md`; kit report `after-report-2026-10-07-cast.md` (§4).
- **D-CAST-1/3/4 (owner 2026-10-07, after mocks 63–65).** Unsigned free agents tagged `out-unsigned` (availability 0) on both planes; from round
  `CARD_PRICED_FROM` (11) the card's candidates are the priced rows (`cardPool()` in the engine block; twins in `full_dom_check.mjs` engineTop5,
  `check_parity.py` and `live_retro.py card_pool()` — gated on the constant's presence in the page at `PAGE_REV[mock]`, so every room drafted
  before v48 replays unchanged); the pre-registered cast-bot experiment (`castsim_design_2026-10-07.md`, `castsim_n30_2026-10-07.json`):
  no variant shipped — V2 (XRank value axis) wins M1 (7.39 vs 12.07) and M2 (7.5 vs 10.43 consensus names left) but fails the M3 regression guard (Spearman 0.30 against the shipped reach ordering); V1/V3 do not improve M2; the bots stay V0. The defense artifacts: `dcast_realism_picks_2026-10-07.json`, `dcast_botdiag_m63_2026-10-07.json`,
  `dcast_lastseason_2026-10-07.json`, `dcast_card_effect_v48.json`.
- **V4 shipped + D-CAST-2 first step (owner 2026-10-07 evening, 'implement all fixes').** The live tool was checked against the record first: in the ten human
  rooms' deck cards (rounds 11–13, 30 owner turns) no unpriced row ever reached the Top-5 and the owner never took one — the late-card symptom was
  cast-room-only. The D-CAST-3 follow-up (amendment 4 in `castsim_design_2026-10-07.md`, `castsim_n30_v4_2026-10-07.json`): the XRank value axis from
  round 7 only — M1 9.29 vs 12.07, M2 7.2 vs 10.43, guard 1.0 — shipped as `BOT_XRANK_FROM = 7` in `managerScores` with `PLAYERS[].xr` baked
  by the build (red-first in `test_card.py`, 99/99). Castle and Barrett re-derived on both planes from their 2025-26 lines (deck value rank Castle
  248 → 171, Barrett 236 → 193); kit report `after-report-2026-10-07-fixes.md`. Deck v49.
- **Mock 66 (2026-10-07 evening, slot 10).** The deck's own MOCK mode against the 11 league-mates on the REAL seating, drafted on deck v49
  (rev `269c522` — the first room with the round-11 priced-only card, the V4 bots and the re-derived Castle/Barrett lines; pool = that commit's
  data/players.csv, frozen as `m66_players_v49.csv`), the veto live. `live_retro.MOCKS[66]` = `dict(tags=("v49",), veto=True, room="cast")`;
  `PAGE_REV[66] = "269c522"`; no punt declared (`PUNT_TIMELINES[66] = [(0, [])]`). State = the owner's exported draft state verbatim (156 picks, every name
  a pool row, snake-consistent, `cast` = the real order; md5 `8f2ee9dd30cc72e87ea4f6b98299e0d8`); no recap and no tool log exist for a MOCK, so no DOM replay.
  **The card's 🎯 taken at 5 of 13 turns** — off the card at #10 Giannis Antetokounmpo (card #17), #15 Scottie Barnes (card #25), #34 Trae Young (card #16), #39 Dyson Daniels (card #4), #63 Paolo Banchero (card #13), #82 VJ Edgecombe (card #19), #106 Jalen Green (card #16), #135 Fred VanVleet (card #19 — corrected 10/7 with the replayer's cardPool fix, mock 67; the DEPTH WATCH pin at #135 named him):
  as drafted 20.16% (rank 1) / ECW 5.013 rank 1 (next 4.887), favored 11/11 (`m66_followcard_grade.json`, `m66_arms.json`;
  the retro port's self-consistent follow-card chain grades 34.93%). Deck card replayed from the v49 page (`live_deckcard.py 66 rev:269c522:docs/draft-deck.html`
  `arena/results/m66_deckcard_v49.json`). Hindsight's largest single swap: Derrick White at #34 (+0.224 cats/week).
  **The fixes' first out-of-sample room:** the late card (rounds 11–13) carried 0 unpriced rows; the cast drafted Stephon Castle #78 (Martin), RJ Barrett #112 (Kevin), Davion Mitchell #137 (JCo), Rui Hachimura #121 (Oblena), Dillon Brooks #133 (Hegi); undrafted: Saddiq Bey, Cam Thomas, Keaton Wagler.
  **Advice line** (`m66_advice_reads.json`, page reading): fired at #34 (Derrick White now), #39 (Onyeka Okongwu now), #63 (Kel'el Ware now); the 'now' men as single swaps grade +6.47 / -0.13 / -1.29 title points, together +2.05; the pair rule replayed as the marker finished at 34.93% against the blend chain's 34.93% (seed set 1).
  Survival pooled with the 51–65 deck cards (`m66_survival.json`: this room 55 rows, Brier 0.218, mean predicted 0.551 vs realized 0.691; BUY NOW 3 of 6 survived, TOSS-UP 7 of 11, quiet 28 of 38 — corrected 10/7 with the replayer's cardPool fix, mock 67; first written as 0.205 / 0.673 / 2 of 6).
  **Cast fidelity** (`m66_cast_fidelity.json`): loyalty fired on 10 of the 16 loyalty names drafted by anyone. Repeat-name audit (`m66_repeat_names_audit.json`): the #1 changes at
  12 of 13 turns under other rooms' rosters (7 of 13 against an empty roster); Gafford on the Top-5 at 5 turn(s), Braun at 0, Poeltl at 0.
  Debrief `debrief_2026-10-07_mock66_slot10.md`; kit report `after-report-2026-10-07-draft66.md`.
- **Mock 67 (2026-10-07, slot 10).** Public Yahoo room, the owner's sixth on the concise card and the first LIVE human room on deck v49 (rev `269c522` — the fixes
  build: round-11 priced-only card, the re-derived Castle/Barrett lines, the four unsigned men excluded; pool = that commit's data/players.csv, tag `v49`), the veto live.
  Page identified by the DOM replay itself: the v49 page's own cardGapText re-emitted the owner's four "off the card" echoes identically (#63 rank 2, 0.008 behind OG Anunoby; #82 rank 41, 0.163 behind De'Aaron Fox; #87 rank 58, 0.255 behind De'Aaron Fox; #111 rank 48, 0.232 behind PJ Washington).
  `live_retro.MOCKS[67]` = `dict(tags=("v49",), veto=True)`; `PAGE_REV[67] = "269c522"`; no punt declared (`PUNT_TIMELINES[67] = [(0, [])]`). State rebuilt from Yahoo's recap with
  `hoops.py draft resync` (156 of 156 resolved, no UNKNOWN; seats match the snake, owner roster = the recap's "My Team", md5 `c18bae2654100c24ae9fe17b4d99ebd7`); the tool board (simulated from the
  167 events) equals the recap pick for pick. **The card followed at 9 of 13 turns, a Top-5 row at 10 of 13**: as drafted 17.51% / ECW 5.015 rank 2 (next 5.129, seat 4),
  favored 9/11; follow-card self-consistent 37.51% (OG Anunoby at #63, De'Aaron Fox at #82, Isaiah Hartenstein at #87, Yaxel Lendeborg at #111) — `m67_followcard_grade.json`, `m67_arms.json`.
  Deck card replayed from the v49 page (`live_deckcard.py 67 rev:269c522:docs/draft-deck.html arena/results/m67_deckcard_v49.json`): off the card — Ivica Zubac at #63 (card #2, 0.008 behind OG Anunoby, who went #69 to seat 4 (Gon); the 🎯 alone +1.14 title points); Damian Lillard at #82 (card #41, 0.163 behind De'Aaron Fox, who went #92 to seat 5 (Deki); the 🎯 alone +6.53 title points); Dylan Harper at #87 (card #58, 0.255 behind De'Aaron Fox, who went #92 to seat 5 (Deki); the 🎯 alone +6.44 title points); DeMar DeRozan at #111 (card #48, 0.232 behind PJ Washington, who went #130 to seat 10 (David); the 🎯 alone +0.00 title points).
  Hindsight's largest single swap: De'Aaron Fox at #82 (+0.240 cats/week).
  **Advice line** (`m67_advice_reads.json`, the pair twin on the page's rows): silent at every turn (the 🎯 under the 0.60 wait floor at 7 turns, the best pair at 5); the pair rule replayed as the marker finished at 37.51% against the blend chain's 37.51% (seed set 1).
  Survival pooled with the 51–66 deck cards (`m67_survival.json`: this room 51 rows, Brier 0.186 vs base 0.242, mean predicted 0.445 vs realized 0.588; BUY NOW 1 of 9 survived, TOSS-UP 7 of 15, quiet 22 of 27).
  Tool-state integrity: the owner's tool log (`arena/data/events/m67_tool_events.json` — 167 events: 160 feeds incl. fifteen shared-token feeds (fourteen surnames, one first name: Miles), two namesake halts ("Murray" after #49, "Jones" after #135), one UNKNOWN feed ("CMB" at #88) fixed with "88- Collin Murray-Boyles"; three Insert-at-# (Boozer #49, Paul George #70, Grimes #141); four undos (#62, #75, #89, #93)) replayed through the real v49 page with `live_replay_dom.mjs`: 0 echo misses,
  0 clock mismatches, 0 page errors, all 156 positions equal to the recap, owner roster identical — `m67_tool_vs_truth.json`. **Finding (display):** the four undone picks' history lines were re-rendered by the later inserts (D59-1 relabelLog) as the replacement's line, so the log shows e.g. "#62: Matas Buzelis" twice — state right throughout (D67-4).
  **Finding (harness, fixed here):** `live_deckcard.py` replayed the card over the whole pool, not the page's `cardPool` — an unpriced man (Jordan Goodwin) sat on this room's replayed #154 card; the harness now applies the page's rule with a loud guard, and mock 66's deck card, survival and advice reads were regenerated (VanVleet at #135 card #24 to #19, the DEPTH WATCH pin at #135 named him; survival Brier 0.205 to 0.218, pooled 0.250 to 0.251; no arm changed).
  **Finding (data):** the draft room's position display matched the pool on all 156 drafted men, teams too — the third room running (D60-4). The fixes in a human room: the late card carried 0 unpriced rows on the page; humans drafted Castle #72, Barrett #128, Davion Mitchell #102, Hachimura #140, Bey #146, Brooks undrafted; no unsigned man appeared.
  Target-wait with this room added (`target_wait_2026-10-07e.json`): deep 🎯s passed on were still there at the next owner turn 14 of 24 times, two turns on 3 of 21; near-price 7 of 17 and 0 of 16. Repeat-name audit (`m67_repeat_names_audit.json`): the #1 changes at
  12 of 13 turns under other rooms' rosters (10 of 13 against an empty roster); Gafford on the Top-5 at 2 turn(s), Braun at 0, Poeltl at 0.
  Debrief `debrief_2026-10-07_mock67_slot10.md`; kit report `after-report-2026-10-07-draft67.md`.
- **What-if 2025-26 (2026-10-07, owner's exercise).** The real 2025-26 league draft redrafted with the v49 engine: the card at seat 4, the eleven E18 profiles in their real seats, 30 seeded rooms (`arena/results/whatif_2025-26/`, scripts in `arena/mocks/whatif/`); graded with the arena on the draft-time lines (ex ante) and on every man's actual 2025-26 Basketball-Reference line × GP/82 (ex post), both in the card's own room and dropped into the real room against the eleven real rosters unchanged. The card opened with Gilgeous-Alexander — the owner's real pick — in 20 of 30 rooms (Dončić when Martin took SGA at #3). Against the real opponents on the actual lines: the owner's real roster 6.074 ECW / 42.10% title; the SGA-opening card rosters 6.347 / 54.05% median (19 of 20 above the real roster), the Dončić rosters 36.17% (4 of 10); ex ante 36.83% real vs 45.25% SGA rooms. Calibration: on the actual lines the real rosters rank David 1st (6.074 vs 5.72 cats/week observed, 103-58-1), Will 2nd (finished 2nd), Martin 4th (champion, 78-82-2). The card's rosters carry less z-sum (+9.0 vs +14.6) and win on category balance; Kawhi (actual #5) was never taken by the card (inj-risk 0.78); Vučević (round 2–3 in 30 of 30 rooms on his 2024-25 line) was its largest miss. Write-up `arena/results/whatif_2025-26/README.md`; kit report `after-report-2026-10-07-whatif-2025-26.md`.
- **Mock 68 (2026-10-08, slot 10).** Public Yahoo room (random humans), the first LIVE room on deck v50 (rev `9f54e99` — the 10/08 pull: notes and Hawkins's team, no line, tag or card change; pool = that
  commit's data/players.csv, tag `v50`), the veto live. The owner's four "off the card" echoes (#34 rank 3, 0.011 behind Anthony Davis; #82 rank 28, 0.117 behind Coby White; #87 rank 12, 0.045 behind Mikal Bridges; #111 rank 33, 0.145 behind Sandro Mamukelashvili) are re-emitted identically by the page's own
  cardGapText in the DOM replay — on v50 and equally on v49 (the two share the engine), so the version is the one live at the standing URL when the room ran. `live_retro.MOCKS[68]` = `dict(tags=("v50",), veto=True)`; `PAGE_REV[68] = "9f54e99"`;
  no punt declared (`PUNT_TIMELINES[68] = [(0, [])]`). State rebuilt from Yahoo's recap with `hoops.py draft resync` (156 of 156, md5 `cd08323137a56fa7a31609d1c28f6447`). **The card followed at 9 of 13 turns, a Top-5 row at 10**:
  as drafted 28.36% / ECW 5.371 rank 1 (next 5.096, seat 1), favored 11/11; follow-card self-consistent 35.00% (Anthony Davis at #34, Payton Pritchard at #63, Mikal Bridges at #82, Josh Hart at #87, Sandro Mamukelashvili at #111, Fred VanVleet at #135). Off the card at Derrick White at #34 (card #3, 0.011 behind Anthony Davis, who went #38 to seat 11; the 🎯 alone +0.80 title points; the advice line's 'now' man — it read "Derrick White now, Jalen Williams next turn (55% to survive)" and the owner did both); Ty Jerome at #82 (card #28, 0.117 behind Coby White, who went #90 to seat 7; the 🎯 alone +3.51 title points); Jaden McDaniels at #87 (card #12, 0.045 behind Mikal Bridges, who went #88 to seat 9; the 🎯 alone +0.80 title points); Darryn Peterson at #111 (card #33, 0.145 behind Sandro Mamukelashvili, who went #133 to seat 12; the 🎯 alone +2.67 title points).
  **Advice line**: fired at #34 ("Derrick White now, Jalen Williams next turn") and the owner took that pair, so its arm is the roster as drafted (+0.00 title points). Pair rule as the marker 36.06% vs the blend chain 35.00% (seed set 1).
  Survival (`m68_survival.json`): this room 51 rows, Brier 0.181 vs base 0.242, mean predicted 0.463 vs realized 0.588; pooled 909 rows, 0.243.
  Tool-state integrity (`m68_tool_vs_truth.json`): 159 events (156 feeds incl. 17 shared-token feeds and the "Butler" heads-up; one UNKNOWN feed "Jurkic" at #119 fixed by "119- Jusuf Nurkic"; two Insert-at-# tries refused as ambiguous ("Wagner": Franz or Moritz) then "Franz Wagner" inserted at #50, 7 shifted; no undo, no halt) replayed through the v50 page: 0 echo misses, 0 clock mismatches, 0 page errors, 0 of 156 positions differ. Room positions vs pool 0 of 156 differ (fourth room running).
  Punt advisor (`m68_advisor.json`): watched assists from #58, advised from #63, clear path only at #135 (6/8); box left empty. Owner's punt-drought question answered from `punt_advice_effect_2026-10-08.json` (the D51R-3 harness re-run over 25 committed states, now taking an output path):
  old z-sum rule 58 proposals (9 on categories the roster was winning), room-relative rule 214 reads, clear path at 7 turns of 275. Owner's injured-rivals question: `injured_rivals_cf.py` (new) → `m68_injured_rivals.json` — rivals' Butler/Porziņģis/Ingram/Nurkić at 0 lift the owner's ECW 5.371 to 5.549.
  Debrief `debrief_2026-10-08_mock68_slot10.md`; kit report `after-report-2026-10-08-draft68.md`.
- **Chromium harnesses and TMPDIR (found 2026-09-29).** Run `full_dom_check.mjs`, `live_replay_dom.mjs`,
  `d54_dom_check.mjs` and `veto_dom_check.mjs` with the DEFAULT temp dir. With `TMPDIR` pointed at the
  session scratchpad (a ~100-character path) Playwright puts Chromium's user-data-dir there and the
  launch dies with `SIGTRAP` before any event (three of three attempts; the browser's Unix-socket paths
  exceed the socket path limit). The same command with `TMPDIR` unset passed every time (four of four).
