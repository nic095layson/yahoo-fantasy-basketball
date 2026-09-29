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
