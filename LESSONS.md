# Lessons ledger

Hard-won operational lessons. Future sessions: read this before live drafts
or arena work. Add entries dated, with the incident that taught them.

## 2026-07-12 — 127-pick live draft simulation (Cowork)

1. **A lost tool result ≠ nothing happened.** A command whose output never
   arrives may still have mutated state. Never re-send a feed on silence —
   read the draft state first. Enforced mechanically now: every
   `draft turn` in a live draft carries `--expect <pre-feed pick count>`;
   a mismatch logs nothing and prints the state tail.
   (Incident: picks #40–43 corrupted by a double-logged feed; cost 2 undos
   + 2 fixes mid-draft.)

2. **Surname-only feeds are the top live-draft error source.** One draft
   produced ambiguous White, Murray, Robinson, Ball, Bridges, Sharpe,
   Collins, Thompson. Prefer first initial + surname for common names.
   The engine now HALTS a batch when a fed name's best match is already
   drafted, and quarantines unmatched names as UNKNOWN instead of
   fuzzy-jumping surnames (Collins→Rollins class).

3. **The Cowork sandbox can neither push nor pull git remotes.** Anything
   worth keeping must be written into the repo folder (David commits via
   GitHub Desktop) or pushed through the GitHub connector — otherwise it
   dies with the session. Session scratch (/tmp) always dies.

4. **Positive findings need fresh-seed replication before they're findings.**
   The arena's "safe_stars beats safe_floor" result (t=3.06, 10 seeds) died
   on 10 fresh seeds (+0.18, t=0.4) — seed-set luck amplified by testing
   three hypotheses at once. Refutations replicated; the enhancement didn't.
   Rule: no positive variant result enters a report headline without
   replication on unseen seeds. (Arena baseline work, same night.)

5. **Draft-price injury discounts that match expected production are still
   wrong for H2H.** Fair-priced mean, unpriced variance: flagged players
   carry ~1.8× weekly game-count variance in-sim, and real 2025-26 was
   harsher than the sim (risk-flagged: 51% of games vs 75% assumed;
   recovery: ~9% vs 60%). Variance needs its own price. (Arena calibration,
   web-verified vs StatMuse/NBA.com.)

## 2026-07-12 — Live-arena ×3 integrity run (slots 1/6/10, post-discount)

6. **Mean-priced discounts don't police concentration.** After deepening to
   ×0.60/×0.78, three full live-arena drafts at three slots converged on the
   IDENTICAL four recovery players (Haliburton, Tatum, Lillard, VanVleet):
   risk-flagged players vanished from every roster, but discounted recovery
   stars still out-price the healthy shelf where it collapses (R4–11), so
   2nd/3rd/4th concurrent bets each won "clearly" on compounded value.
   Deepening the per-player discount moved WHERE they were drafted, not
   WHETHER. Concentration needs its own rule (capped bets or steeper
   compounding) — see arena/results/report_2026-07-12_live_arena_x3.md §5-P1;
   codification gate applies. Also surfaced there: the healthy-tiebreak's ~5%
   band must name its reference number (adjusted vs compounded value — they
   gave contradictory answers mid-draft), and the skill defines no multiplier
   past the 3rd concurrent recovery bet.

## 2026-07-12 — Slot-9 manual-feed practice draft (158 picks, opening-night 2025 snapshot)

7. **Confirm teams × rounds = total picks BEFORE pick #1.** The draft ran on
   `--size 15` per the session brief; the owner ended it at #158 and only then
   surfaced that the intended roster was smaller (real league: 13 slots).
   Cheap to catch at init ("12×15 = 180 picks, last pick #180, yours are
   9/16/.../177 — confirm"), expensive to catch at the end: uneven rosters bias
   every cross-team comparison. Add the arithmetic echo to the prime checklist.

8. **Owner resubmits during processing are a normal input, not an anomaly —
   and the 2026-07-12 protocol absorbs them.** Four feeds' results/echoes were
   lost this draft because the owner re-sent while the engine call was in
   flight (owner-confirmed root cause). State-read-first + `--expect` on every
   feed produced zero double-logs and zero drift across 158 picks. Keep both
   forever; also: when a new message arrives during processing, always
   `draft status` before feeding it.

## 2026-07-12 — GitHub connector debugging (Cowork ↔ cloud relay)

9. **The Cowork GitHub connector cannot reach this repo — treat the GitHub
   Desktop relay as the standard path, not a fallback.** Exhaustively
   diagnosed 2026-07-12: the connector authenticates as nic095layson but its
   token sees ZERO repositories (repo reads 404; a `user:` repo search returns
   "no permission"), while the "Claude" GitHub App installation HAS the repo
   grant (cloud sessions push over it all day). The user-authorization half of
   the connector handshake never completes — the connect flow dead-ends on an
   "organization settings / Team and Enterprise plans" error page — so
   GitHub-side settings cannot fix it, and reconnect attempts (2×, plus a
   verified installation grant) changed nothing. Standing procedure: Cowork
   writes deliverables into the repo folder, David commits/pushes via GitHub
   Desktop, the cloud session pulls. Do not spend session time re-debugging
   this; retest only after a Claude connector update, with the one-liner
   "read LESSONS.md from nic095layson/yahoo-fantasy-basketball" in a FRESH
   Cowork conversation.

## 2026-07-27 — The unlanded 2026-07-24 pull (fantasy-basketball-2026-27)

10. **A pull that isn't pushed didn't happen — the repo is the only
    persistence layer.** A draft-kit data pull was run on 2026-07-24 but its
    output was never committed: no data-file commit exists after 2026-07-13
    on any branch of `fantasy-basketball-2026-27` (the same day's daily pull
    DID land in this repo — `3e4e827`, LeBron→PHI — the draft-kit half was
    what got left behind). The next session (2026-07-27) had no way to see
    the Friday work — chat transcripts, analysis, and delivered-but-
    uncommitted files are invisible across sessions — so it correctly
    measured the data layer as 14 days stale and re-did the window. Changes
    dated 7/13–7/19 (Bridges official, Valanciunas to EuroLeague, the Dort
    three-team trade) were still unapplied on 7/27, confirming the 7/24
    draft-kit output never landed anywhere. Same root pattern as
    lesson-of-7/12 (memory-sourced CSV): work exists only when it lands in
    the repo, with provenance. Countermeasure: DATA-PULL.md §0 in
    `fantasy-basketball-2026-27` makes push-to-main the definition of done,
    with SHA verification on origin/main; quiet days still commit a pull-log
    row and after-report, because those records are what date the next
    pull's window.

## 2026-07-27 — The stale Draft Deck (published-artifact drift)

11. **A published artifact is part of the deliverable — a refresh that
    doesn't republish it didn't finish.** The owner opened the Draft Deck
    on 2026-07-27 and found it serving the 2026-07-24 pool (header stamp:
    3 days old) even though a fresh draft-kit pull had landed on
    `fantasy-basketball-2026-27` `main` that morning. Two compounding
    causes: (a) the deck renders only what `scripts/build_deck.py` baked
    in at the last republish — repo pushes never reach the published
    page; (b) the deck's source, builder, verifier, and the 7/23–24 data
    refreshes were stranded on the unmerged PR #2 branch, so this repo's
    `main` data plane still said fresh-as-of 7/11 while the published
    deck said 7/24 and the draft-kit repo said 7/27 — three surfaces,
    three different truths, no error anywhere a session would look.
    Countermeasures: `DATA-PULL.md` §0 items 5–6 and §7 in the draft-kit
    repo (deck sync + republish are definition-of-done for every pull),
    the fantasy-basketball skill's publish-gate law now names republish
    staleness a live defect, and the stranded branch was consolidated
    into PR #3. Corollary of lesson 10 at the delivery layer: work
    exists only where the consumer looks — the repo for sessions, the
    published URL for the owner.
