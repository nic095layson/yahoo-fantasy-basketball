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
   *(2026-07-13: partially superseded — repos now public; READ half is moot,
   WRITE half stands. See addendum 9-A below, ported 2026-08-04 during the
   LESSONS fork reconciliation.)*

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

## 2026-07-13 — Addendum to lesson 9: all four repos made public
*(ported 2026-08-04 from the `claude/lesson-9-addendum-public-repos` branch,
PR #1, during the LESSONS fork reconciliation — original date preserved)*

9-A. **Reads are un-broken; writes still need the relay.** David made all
   four repos public 2026-07-13. Verified the same day from a cloud session:
   `https://raw.githubusercontent.com/nic095layson/<repo>/main/<path>`
   returns HTTP 200 with NO auth for all four repos, and `add_repo` + clone
   succeeded where reads previously 404'd. Lesson 9's read failure (the
   connector token sees zero repos) is therefore moot for READS: any surface
   with plain web fetch — claude.ai projects, Cowork, cloud sessions — can
   read live repo state without the connector at all. Amended standing
   procedure: **pull-first via raw URLs for reads** (codified in
   `fantasy-basketball-2026-27/instructions/claude-ai-project-instructions.md`);
   **writes unchanged** — GitHub Desktop relay or a Claude Code cloud
   session, because the connector's user-authorization half is still dead
   and public visibility grants no write. Lesson 9's retest one-liner is
   still worth running in a fresh Cowork conversation to check whether the
   connector itself now reads public repos, but nothing depends on it
   anymore. Corollary: public repos mean anyone can read these files — keep
   credentials, tokens, and anything private out of all four repos.

## 2026-07-13 — Roster audit: 39/220 stale team values in the draft-kit CSV
*(ported 2026-08-04 from PR #1, where it was numbered lesson 10; renumbered
12 here because this branch's lessons 10–11 were written later under those
numbers — content unchanged)*

12. **A ledger of headline moves is not roster verification — bind data-policy
   gates to the artifact, not the occasion.** The 2026-27 draft-kit CSV
   (fantasy-basketball-2026-27) shipped 220 player-team pairings; a live-web
   audit corrected 39 (17.7%), every one describing a move already public at
   authoring — a January trade, February-deadline secondary pieces, and ten
   days of live July free agency, including a four-team deal from two days
   prior. Root cause: teams came from model memory patched with ~15 verified
   headline moves, authored in a 24-minute window with no per-player pass;
   the repo's own "never assert a team from memory / verify within 14 days"
   rules were scoped to "the October run," so the interim artifact skipped
   them; with no per-row provenance the staleness was invisible; and the
   generated board overclaimed ("every verified move"). The headline research
   itself held up 100% — coverage failed, not accuracy. Fix (same repo, PR
   #1): a per-row source ledger (`roster-provenance.csv`), a mechanical gate
   (`check_provenance.py`) that `rank_engine.py` runs before it will build a
   board (mismatch → no artifact; `--allow-stale` → "Do not draft off this
   board" stamped in the header), and PROMPT.md §0.6 binding the data policy
   to every claims-bearing artifact. Portable rule: any committed file
   asserting live-world facts carries per-row source + date, and a machine
   check — not a checklist item — stands between it and whatever consumes it.
   Full analysis: fantasy-basketball-2026-27
   `report/postmortem-2026-07-13-roster-audit.md`.

## 2026-08-04 — Shipped results whose evidence lives outside the repo

13. **A result is only as landed as its derivation — the evidence-landing
   law.** The 2026-08-04 independent system review tried to re-derive the
   shipped E9/blend50 and E18 numbers and could not: the mock draft states
   live under a session-scoped uploads path, the result JSONs in a session
   scratchpad, and the committed harnesses hardcode a foreign machine's
   `os.chdir` — none of it reachable from a fresh clone. The measured-side
   numbers that COULD be recomputed from committed artifacts all reproduced
   exactly (which is why this is a lesson, not a retraction), but the
   sim-side numbers (panel tables, Spearman checks, parity counts) currently
   rest on records, not re-derivable artifacts. This is lesson 10's failure
   shape (work that never landed) and the LEDGER's founding defect
   (remembered tallies), recurring at the validation layer. Law: **no
   shipped number is quotable unless a fresh clone plus one committed
   command regenerates it — commit the inputs and outputs, or a
   regeneration manifest with repo-relative paths; anything else is quoted
   as [UNREPRODUCIBLE] until backfilled.** Backfill of the existing mock
   states/results is queued for the September run (see SEPTEMBER-PLAN).

## 2026-08-04 — The E18 bar re-scope (pre-registration must be append-only)

14. **A bar you can edit while shipping is not a bar.** E18's pre-registered
   replay-calibration bar ("±8 reach index") was registered at 21:05, failed
   7/11 at test, was re-scoped to a Noah-anchored scaled band, and shipped
   at 21:38 — the pre-registration lived 33 minutes, never crossed a session
   boundary, and the ship commit itself edited the bar's wording in the
   registration file. The re-scope's diagnosis was defensible (the absolute
   bar largely tested the market proxy's geometry, not the manager model);
   the process was not — and a second, undisclosed instance existed the same
   week (blend50 shipped without its pre-registered both-formats
   re-validation, recorded as a prediction instead of a measurement). Laws,
   now bound here where every session reads them: **(a) bar registries are
   append-only — a re-scope adds a dated row beside the original wording,
   never edits it; (b) two re-scopes of the same bar = the bar failed;
   write the negative result and stop; (c) a dropped or deferred
   pre-registered check is disclosed in the ship note itself, not
   discovered by the next audit.** The E18 original ±8 bar re-arms at the
   October real-ADP sync exactly as registered.

## 2026-08-09 — Round-3 audit: four lessons from 66 verified findings

15. **A gate that reads a date the gated script wrote is not a gate.** The
    three-gate publish pipeline was walked end to end having done zero
    research — `verify_rosters.py` wrote `date.today()` unconditionally,
    `hoops.py` and `build_deck.py` checked that self-written date, and the run
    ended in "safe to publish" with the deck header rendering "fresh today".
    It was not hypothetical: during the audit itself an agent ran the script
    against the working tree and the only trace was
    `data/roster_verification.json`'s date advancing 08-05 → 08-08. Nothing
    warned; the file simply became a day's worth of "verified" (reverted before
    commit). A second hole in the same shape: a pool row on no official roster
    landed in `unmatched`, which was never a mismatch, so a fabricated team
    (`Bronny James,ZZZ`) exited 0 and passed every gate — exempting exactly the
    rows most likely to be wrong, the newly added ones. **Law: a verification
    artifact must inherit the date of the EVIDENCE it checked, never the clock
    of the process that checked it; and the check must be able to fail on the
    rows nobody has seen before.** Fixed 2026-08-09 (A4): fallback mode
    inherits `rosters_official.json`'s own date, unmatched rows hard-fail, the
    build records a pool content hash, and the judgment layer is gated on
    matching the pull date.

16. **An append-only completeness law needs a retirement half.** The
    `MUST_HAVE` rule forces each June draft class INTO the pool and never
    retires the previous one. Six 2025-draftees still carried `rookie-proj`
    into their second season, applying a ×1.15 market-hype multiplier worth
    12–21 estimated-ADP slots — and nine of eleven 2025-class rows were still
    byte-identical to the pre-debut October-2025 snapshot, their actual rookie
    season never ingested. The owner found the instance (Dylan Harper); the
    class was six more. **Law: any rule that adds members on a schedule must
    state, in the same breath, what leaves and when — and enforce it
    mechanically, or the pool accretes stale labels one draft class per year.**

17. **Two surfaces with different objectives need a written precedence rule,
    or the draft decides it at 45 seconds.** The deck sorted by punt-blind
    blend50; `hoops.py` sorted by punt-aware `adj_value`; their #1s differed on
    **19 of 26 owner turns** (mean Top-5 overlap 1.8/5), and nothing anywhere
    said which governed a pick. The fix was not to sync them — it was to notice
    that the deck already parses feeds, carries the same halts, autosaves, and
    imports/exports the exact `draft_state.json` the CLI writes, i.e. it is a
    superset. **Corollary: before building a parity treadmill between two
    implementations, check whether one of them should stop having the
    responsibility at all.**

18. **A display that can only render one sign cannot report the opposite
    fact.** The card's row-1 figure was a percentile gap — "lead +X" — which is
    positive by construction. Replacing it with the margin in expected
    categories won per week revealed that on **4 of 13 owner turns in mock 34
    the card's #1 is WORSE than its own #2** on the weekly-categories metric,
    with the punt-blind value half carrying the ordering. The old display had
    not hidden this by accident; it was structurally incapable of showing it.
    The same pass found the median mid-round margin is 0.007 cats/wk — most
    turns are near-ties, which a 50–88% confidence band had obscured rather
    than reported. **Law: when choosing what a number on a card means, ask what
    it is incapable of saying. A quantity in real units can carry bad news; an
    index normalised for display often cannot.**

## 2026-08-10 — Round-4 audit: two lessons from 13 regressions

19. **A fix-batch is code like any other — it ships with its own defects, and
    the newest code is always the least-audited.** The 2026-08-09 batch that
    closed 20 audit findings introduced 13 new ones, including a critical:
    `resync`'s recovery promise was false (the one-generation `.bak` was
    overwritten by resync's own second save, so the "backup" held the wiped
    board), the degenerate-feed guard silently unmatched seven real players
    whose first names are two letters (CJ/GG/Ja/AJ/PJ/RJ/VJ), and two of the
    new publish gates had never been observed failing — one was a deadlock
    (its own prescribed bypass couldn't satisfy it), one was dead code (its
    regex could never match the file it inspected). **Laws: (a) every fix
    lands with a regression test that FAILED before the fix — red first, then
    green; (b) a gate is untested until it has been seen red — every gate
    suite must drive each gate to refusal AND acceptance
    (`scripts/test_gates.py`); (c) a fixture's expected values must be
    derived from intent, not recorded from the implementation — the parity
    fixture had enshrined the two-letter bug by recording `'aj' → []` as the
    expected answer.**

20. **Committed evidence needs overwrite guards in the tools, not discipline
    in the agents.** Three artifact-clobber incidents in two days, each by a
    process explicitly instructed read-only: a verifier re-dated
    `roster_verification.json` (round 3), an auditor's `--quick` run replaced
    the committed 18,000-season E24 evidence with a 4× noisier file at the
    same path, and a cadence run overwrote `cadence_intel.json` (round 4).
    All three were caught by `git status` before commit — but catching is not
    preventing. **Law: any tool that writes a committed evidence artifact
    refuses to overwrite a file whose recorded config differs from the run's
    (implemented in `bench_weight_study.py` 2026-08-10), and `git status`
    runs before EVERY commit, treating any unexpected modification as an
    incident to investigate, not noise to restore.**

## 2026-08-13 — The orphaned 8/10 republish (a third unlanded-work incident)

21. **A published artifact is a write path into production that git never
    sees.** The 2026-08-13 Fresh Deck Pull went to republish the deck and
    found the live artifact serving a **2026-08-10 build that existed nowhere
    in this repo's history**. It was not junk: it carried the daily-fill
    lineup model (`dailyFillWeights`, `DF_K = 32`) that replaced the static
    10-starters + 3-bench weighting, and the owner-requested Fit → ΔECW
    column. Its Python half never landed either, so the orphaned JS
    disagreed with `arena.team_week_model` by **20 card orderings** — while
    that same page's Logic paragraph still told the reader it was "verified
    against engine output at build time." The page had been lying about
    itself for three days, and no gate in either repo could have caught it,
    because every gate runs against the repo and the drift was *outside* it.

    This is the third instance of one failure mode: 7/24 (a pull that never
    landed, lesson 10), 7/27 (the deck serving a stale pool, lesson 11), and
    now a republish whose source never reached git. Lessons 10 and 11 both
    concluded "the repo is the only persistent layer." That was aspiration,
    not description: the artifact is *also* persistent, it is the surface the
    owner actually drafts from, and it can be written without the repo's
    knowledge. **Laws: (a) before republishing, FETCH the live artifact and
    diff it against the local build — if the published manifest is newer than
    the repo's, stop and reconcile before overwriting, because publishing is
    destructive to whatever is already there; (b) a republish is only done
    when the exact bytes published are committed; (c) when a cross-surface
    conflict has no safe default — here, regress the owner's model or ship an
    unverifiable one — it is an owner decision, not an agent's.**

22. **A "port of X" comment is a claim, and unclaimed claims rot.** The
    orphaned JS documented itself as a "Port of `arena.daily_fill_weights`;
    dfHash verified bit-identical to `arena.df_hash` (72/72 vectors)".
    Neither function existed in the repo — the comment described code that
    was never committed, so the strongest available evidence that the two
    halves agreed was a sentence. When the model was re-landed (2026-08-13),
    `df_hash`/`daily_fill_weights` went into `arena/arena.py` and the 72
    vectors became a real check in `check_parity.py`, driven red first by
    mutating one FNV constant (89 disagreements) before being accepted green
    — lesson 19(a)/(b) applied to a hash. The vectors are literal strings
    rather than pool members so roster churn cannot silently empty the check,
    and one is non-ASCII to exercise the UTF-16 path that a pure-ASCII pool
    would never reach. **Law: a cross-language port is verified by vectors in
    the gate, never by a comment asserting it was verified once.**
