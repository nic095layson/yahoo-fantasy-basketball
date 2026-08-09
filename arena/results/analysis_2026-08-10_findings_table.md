# Appendix B — the 41 verified round-4 findings (audit 2026-08-10)

Companion to `analysis_2026-08-10_self_critique_round4.md`. Round-4 was run under a stronger model with three targets: regressions in the 2026-08-09 commits, independent re-derivation of round-3's measurements, and the next layer of domain comprehension with F01–F66 as known baseline. Every finding below survived an independent adversarial verifier told to refute it; where the verifier narrowed the claim, the narrowed wording appears. `REGRESSION` = introduced by the 2026-08-09 commits (d3b4a49..e635809).

Reference items as `R4-F##`.

## Index

| # | Sev | Area | Status | Finding |
|---|---|---|---|---|
| R4-F01 | critical | regression | REGRESSION | resync's recovery promise is false: .bak holds the WIPED board, not the prior one; SKILL.md … |
| R4-F02 | high | deck | NEW | Published deck is 8 commits stale while yesterday's own doctrine makes that page the authoritative … |
| R4-F03 | high | domain2 | KNOWN-PARTIAL G1a / E20 / E23 / … | Punt-declaring cost (G1a) survives the bench-weight correction at -3.1 to -6.4pp — the owner's … |
| R4-F04 | high | domain2 | KNOWN-PARTIAL E17 / E18 | The hand-set market model misprices centers by ~2 rounds against the owner's real room — early … |
| R4-F05 | high | regression | REGRESSION | The new <3-char match guard kills real name tokens: 'CJ', 'GG', 'Ja', 'AJ', 'PJ', 'RJ', 'VJ' now … |
| R4-F06 | high | regression | REGRESSION | build_deck gate 1b deadlocks: its own prescribed bypass (--allow-unmatched) can never satisfy it |
| R4-F07 | high | reverify | KNOWN-PARTIAL E24 / … | m33's champ gain is ~74% a TEAM_WEEK_SHOCK x weight artifact ECW cannot see; mechanism E24 lacks is … |
| R4-F08 | high | skill | REGRESSION | Live-turn I/O channel undefined after A3: no written path for picks, deck Top-5, or margins to … |
| R4-F09 | high | skill | REGRESSION | The ~0.25 kept-z 'within noise' band is uncalibrated and fires at 12 of 13 board depths |
| R4-F10 | high | skill | REGRESSION | §3 format 'kept-z ±X.XX under the declared punt' is not producible from the one allowed command |
| R4-F11 | medium | deck | KNOWN-PARTIAL F18 (A10) | F18's colophon sentence is still in the source, but the action map records it under A10 which the … |
| R4-F12 | medium | deck | REGRESSION | Gate 4 (pool moved-or-explained) is silently inert for exactly the next build — the one that must … |
| R4-F13 | medium | deck | KNOWN-PARTIAL F15/F19 (A4) | Sochan/Mathurin JUDGMENT text still wrong in source AND published page; gate 5 now makes the fix … |
| R4-F14 | medium | domain2 | KNOWN-PARTIAL F24 / T4 / §7.5 … | A 3-vs-4-game playoff week for a single starter swings that round's win probability by ±6.4pp in … |
| R4-F15 | medium | domain2 | KNOWN-PARTIAL F26 / F37 / E15 … | In-season stash-vs-drop advice is contradictory across surfaces: a top-20-equivalent recovery … |
| R4-F16 | medium | october | KNOWN-PARTIAL E24/§7.2, §7.4 | E24 mechanism: three concrete September experiments, grounded in the three places BENCH_WEIGHT … |
| R4-F17 | medium | october | KNOWN-PARTIAL A20 (F33) | Nothing fires between Oct 12 and draft night, and the October prompt's self-reschedule clause is … |
| R4-F18 | medium | october | KNOWN-PARTIAL Q3-Q8 | Q3-Q8 ranked: the real deadline is Sept 1 (22 days), and Q4/Q3 must land before it |
| R4-F19 | medium | october | KNOWN-PARTIAL A19 (F56) | Republish is the definition of done for both Routines, but the Artifact tool grant is unconfirmed … |
| R4-F20 | medium | october | NEW | bench_weight_study.py --quick silently overwrites the committed E24 evidence artifact; runtime … |
| R4-F21 | medium | regression | REGRESSION | Gate 4's quiet-day bypass is substring matching: any note containing 'quiet' or 'no change' … |
| R4-F22 | medium | regression | REGRESSION | build_deck gate 5's JUDGMENT orphan check is dead code — its regex can never match the actual deck |
| R4-F23 | medium | reverify | KNOWN-PARTIAL E24 | 0.956 assumes 13 independent NBA schedules; real teammate stacking moves it to 0.940, absences to … |
| R4-F24 | medium | reverify | KNOWN-PARTIAL A17 / F16 | A17's leading-tag fix left 5 substring note-parsers alive: rec_ct, rec_compound x2, market 'risk', … |
| R4-F25 | medium | reverify | REGRESSION | bench_weight_study.py --quick silently overwrites the committed evidence JSON; I clobbered and … |
| R4-F26 | medium | skill | REGRESSION | Evals 4-6 predate the deck-surface doctrine and eval 4's premise contradicts its own expected output |
| R4-F27 | medium | skill | KNOWN-PARTIAL A19 / owner-law … | SKILL §3 describes deck features (cats/wk margin) that exist only in unpublished source; no gate … |
| R4-F28 | medium | skill | REGRESSION | draft-arena skill and arena README still mandate the retired 'confidence card' in practice drafts |
| R4-F29 | low | deck | KNOWN-PARTIAL F22 | Feed hint hand-lists 5 ambiguous surnames; the pool mechanically contains 18, including Johnson x4 |
| R4-F30 | low | deck | KNOWN F44 | Mobile/touch tooltip gap (F44) still open; the fix is ~12 display-only lines at one site |
| R4-F31 | low | domain2 | KNOWN-PARTIAL F12 / F14 / F25 | Hand-guessed rookie tail lines shape the z baseline (5 of 14 sit inside the top-156 fixed point) … |
| R4-F32 | low | domain2 | KNOWN report_2026-08-09 §9 / … | Round-3's repeat-target lead is already closed: 21 of 24 repeat targets are in profiles.json … |
| R4-F33 | low | october | KNOWN A15/A17; … | Feature-freeze inventory verified clean: zero ordering or availability-tier change on current data … |
| R4-F34 | low | october | NEW | Performance: every hot path measured — draft night runs at ~60ms/turn, and no code optimization is … |
| R4-F35 | low | october | NEW | SKILL.md's 'gitignored scratch artifacts' claim is false — both intel JSONs are git-tracked, and … |
| R4-F36 | low | regression | KNOWN-PARTIAL F52 | F52's end-of-draft guard shipped Python-only: the deck still shows a phantom 'your next: #164+' pick |
| R4-F37 | low | regression | NEW | test_draft.py certifies the recovery paths it does not test: resync .bak content, empty paste, and … |
| R4-F38 | low | reverify | KNOWN A17 | A17's 'ZERO rows change on today's pool' claim verified on both pools — confirmed accurate |
| R4-F39 | low | reverify | NEW | PARITY: EXACT MATCH covers 5 surfaces; teamWeekModel numerics, market model, and the hoops.py … |
| R4-F40 | low | reverify | NEW | Round-3's corroborating bench numbers (0.971/0.998 and 0.852) come from uncommitted /tmp harnesses |
| R4-F41 | low | skill | REGRESSION F58 … | SKILL claims the arena intel JSONs are 'gitignored scratch artifacts' — both are git-tracked; … |

---

## CRITICAL — Regressions in the 2026-08-09 commits

### R4-F01 · resync's recovery promise is false: .bak holds the WIPED board, not the prior one; SKILL.md codifies the lie

`REGRESSION` · verdict **CONFIRMED** · *measured*

draft resync (shipped in A5, hoops.py:705-712) prints 'draft_state.json.bak holds the prior board', and SKILL.md:58 instructs the live-draft session that 'the prior board is kept at draft_state.json.bak' — but resync calls save_state twice in one command (once to persist the wipe, once when the turn path saves the rebuilt feed), and the one-generation .bak is overwritten by the second save. By the time the command returns, .bak holds the CLEARED board. An empty or bad paste therefore destroys the prior board irrecoverably while printing a reassurance that it survives. A 3-correction halt mid-resync-paste has the same effect (snapshot is taken after the wipe, so rollback restores an empty board).

- **Evidence** — Reproduced in scratch clone: built a 6-pick board, ran `draft resync "<7-name paste>"` — output printed '...json.bak holds the prior board' but `draft_state.json.bak` contained [] (0 picks). Empty-paste case: 7-pick board, `draft resync ""` → state=0 picks AND .bak=0 picks immediately after the single command; the 7-pick board is gone with no artifact anywhere. Code: scripts/hoops.py:705-712 (resync → save_state → args.draft_cmd='turn' → turn's save_state), save_state one-generation backup at …
- **Cost** — Draft night, the exact moment resync exists for (board glitch, owner pastes the room's pick list): a truncated/empty paste wipes the live board; the future Claude session, following SKILL.md, runs …
- **Action** — Have resync copy the pre-wipe state to a dedicated one-shot file (e.g. draft_state.json.pre-resync) before clearing, print THAT path, refuse an empty/zero-name paste outright ('resync with 0 parsed names — nothing cleared'), take the correction snapshot before the wipe, and correct SKILL.md:58. Add test_draft cases asserting the recovery file's CONTENT equals the prior board.


---

## HIGH — Published artifact & deck truth

### R4-F02 · Published deck is 8 commits stale while yesterday's own doctrine makes that page the authoritative draft-night surface

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL (LESSONS #11 class, F56/A19 process gap, SEPTEMBER-PLAN §4/§6 remedy timing — the registered baseline covers the drift class, the missing republish verification, and the planned September republish; it does not cover this instance or the doctrine conflict). What exceeds the registered scope, all reproduced: the published deck (built 2026-08-05, 8 commits behind HEAD) still runs pre-A5/A6/A7 code whose live hazards I executed — '.' logs a fabricated ✓ pick (best of 10 dot-containing names), bare 'my:' logs the best remaining player (Wembanyama) to the owner's team, Şengün/Dončić quarantine as UNKNOWN (Jokić survives only at fuzzy ratio exactly 0.8), 'jacksn' silently resolves to GG Jackson, an empty LIVE board renders 'lead +57.2 🚀' …

- **Evidence** — git diff ac197ce..e635809 -- docs/draft-deck.html (140 lines, all five behavioral regions enumerated). Node execution of BOTH revisions' extracted <script id=data>+<script id=engine>: PUBLISHED match('.')→'Jaren Jackson Jr.|Wendell Carter Jr.|Kevin Porter Jr. (+7)', match('')→246 candidates, match('Şengün')→NO MATCH, match('jacksn')→'GG Jackson'; SOURCE: all degenerate→NO MATCH, Şengün→Alperen Sengun, jacksn→2 candidates. Published decwScores(pool,[],[]) → 'rendered row-1: lead +57.2 | standout …
- **Cost** — On draft night the owner's fingers are on the OLD page: one stray '.', a bare 'my:', or a pasted 'Dončić' corrupts draft state mid-round (lesson-1's documented #1 failure mode), while the protocol …
- **Action** — Run the legitimate refresh + republish ceremony now (checklist in the Sochan finding) rather than waiting for September; then add one line to SKILL.md's pre-draft checklist: assert the artifact's build-manifest 'built' date is >= the date of the last deck-source commit before declaring the deck primary.
- **Owner question** — Approve an immediate refresh + republish to the existing artifact URL (all changes since 8/5 are shipped audit fixes, not new features — freeze-compatible)?


---

## HIGH — Fantasy-domain comprehension, round 2

### R4-F03 · Punt-declaring cost (G1a) survives the bench-weight correction at -3.1 to -6.4pp — the owner's 3-cat punt habit is still -EV on the corrected instrument, but E23's planned warning would overstate the cost ~30%

`KNOWN-PARTIAL — G1a / E20 / E23 / SEPTEMBER-PLAN §7.4` · verdict **PARTIALLY_CONFIRMED** · *measured*

On the corrected bench weight (0.956), CRN-paired G1a-style policy arms (500 seasons/cell, n=36, 6-team bracket) still measure punt-declaring as -EV: punt FT% -3.09pp (t=-3.93), punt {FT%,3PTM} -6.43pp (t=-8.55), attenuated ~26-31% from the same-instrument BW=0.15 run — direction survives, magnitude shrinks. The measured arms are 1- and 2-cat punts; the owner's actual 3-cat punt habit (m31/m32/m34, 3 of his last 4 declared mocks) is supported only by extrapolation plus one same-slot mock pair (m32 6.18/5.92 vs m33 12.54/12.38 corrected). The deck ALREADY ships the '-5 to -11pp (G1a, CRN)' warning in 4 places and E23 cites the G1a cost unqualified; those figures are 43-48% above the corrected-instrument point estimates. Not covered by par.7.4 …

- **Evidence** — My run: scratchpad/g1a_bw.py, output g1a_bw_out.json — summary {0.15: punt_ft -4.17 sd 8.42 t -2.97 n=36; punt_big -9.27 t -9.45} {0.956: punt_ft -3.09 t -3.93; punt_big -6.43 t -8.55}. Same-slot mock pair reproduced by reading arena/results/bench_weight_study_out.json and _seeds101-202-303_out.json (m32 slot10 punt 6.18/5.92 vs m33 slot10 no-punt 12.54/12.38). Original G1a: arena/results/findings_2026-07-30_gap_study.md §1 (-5.93/-11.22 at BW=0.15). Declaration guidance: …
- **Cost** — On draft night the owner will likely declare a 3-cat punt (3 of his last 4 declared drafts). By the system's own corrected instrument that policy costs him ~3-6.4pp champ. If E23 ships quoting G1a's …
- **Action** — 1) Amend E23's wording source: quote the corrected-instrument range (-3 to -6.5pp, n=36 cells, directional) alongside G1a, and add one declaration-time line to SKILL.md (display-only truth fix, allowed under the freeze). 2) At the E14/E24 re-baseline, re-run G1a at full 2000-season scale on the real bracket before E20's punt-aware-ordering decision — my run is on the 6-team bracket the instrument still ships.
- **Owner question** — When you declare a 3-cat punt on draft night, do you want the system to actively argue against it with the measured cost, or display the number once and then optimize inside your declared frame?

### R4-F04 · The hand-set market model misprices centers by ~2 rounds against the owner's real room — early C-eligible players go 21.7 picks earlier than MKT_W predicts

`KNOWN-PARTIAL — E17 / E18` · verdict **PARTIALLY_CONFIRMED** · *measured*

Graded arena.market_ranks (MKT_W, arena/arena.py:87-88) against the real 2025-26 board (arena/draft_boards.json, 146-148/156 picks matched via fold/suffix normalization): Spearman ~0.81-0.82, MAE ~22 picks, beating the value-board baseline (~0.78/26). The miss is systematically positional and exactly reproducible: C-eligible players go a mean 19.0 picks earlier than the model predicts (+21.7 in rounds 1-5, n=17), guards 7.5 picks later — e.g. Jarrett Allen real #37 vs model #107, Jalen Duren #46 vs #109, Deandre Ayton #49 vs #108. A split-half CV coordinate-descent refit lifts held-out Spearman by ~+0.05 in both folds; both folds agree FG% should rise (0.5 -> 1.2-1.4) and TO should fall (0.25 -> 0.0-0.4), but the REB-up and FT%-down directions are …

- **Evidence** — Ran in-session against arena/draft_boards.json '2025-26' with arena.market_ranks on the frozen Oct-2025 pool: shipped Spearman 0.820 / MAE 23.9; value-board baseline 0.789 / 27.5; positional signed miss C-eligible +19.0 (n=39), guards -7.5 (n=63), rounds 1-5 C +21.7 vs others +1.2. CV: fit on even picks -> odd-half 0.873 vs shipped 0.835; fit on odd -> even 0.883 vs 0.803. MKT_W definition arena/arena.py:87-88; consumers: pick_for ADP branch arena.py:244, market persona, deck manager model.
- **Cost** — Every survival estimate on draft night — BUY NOW chips, 'will that center last to my next pick', the E18 per-seat projection — inherits a ~2-round optimism on centers in a room that demonstrably …
- **Action** — Fold this into the E17/E18 September refit as a measured prior: calibrate MKT_W (or the per-manager adp/val blend) on the owner's own three boards with the CV procedure above, not national-ADP intuition; at minimum raise FG%/REB and cut FT%/TO. Re-run chip calibration afterward per E17's bar. Keep refit weights out of the engine until the September window (freeze).


---

## HIGH — Regressions in the 2026-08-09 commits

### R4-F05 · The new <3-char match guard kills real name tokens: 'CJ', 'GG', 'Ja', 'AJ', 'PJ', 'RJ', 'VJ' now log UNKNOWN

`REGRESSION` · verdict **CONFIRMED** · *measured*

The F02 degenerate-segment guard (scripts/hoops.py:426, mirrored in the deck at draft-deck.html matchCandidates 'q.length < 3') rejects every query under 3 characters unless it is in NICKNAMES — but seven pool players' REAL first-name tokens are two characters (CJ McCollum, GG Jackson, Ja Morant, AJ Dybantsa, PJ Washington, RJ Barrett, VJ Edgecombe) and none are in NICKNAMES (hoops.py:366-380). At ac197ce each of these resolved uniquely via the exact-word stage; at HEAD they return [] and a live feed logs them as UNKNOWN placeholders while the player stays on the available board. The check_parity fixture actively blesses the regression: QUERIES includes 'aj' (check_parity.py:57) with the Python result — [] — as the expected answer.

- **Evidence** — Corpus diff (1,550 queries: every pool-name word, truncations, hyphen segments, nicknames) between ac197ce and HEAD: 107 result changes, most intended (broad prefixes now []), but 'CJ' OLD=['CJ McCollum'] NEW=[], 'GG'/'gg' OLD=['GG Jackson'] NEW=[], 'Ja' OLD=['Ja Morant'] NEW=[], 'AJ' OLD=['AJ Dybantsa'] NEW=[], plus PJ/RJ/VJ. End-to-end: `draft turn "CJ; GG; Ja"` at HEAD → three '⚠ logged as UNKNOWN (no match)' lines; at ac197ce → '✓ #1 CJ McCollum → T1, ✓ #2 GG Jackson → T2, ✓ #3 Ja Morant → …
- **Cost** — Live-draft feeds routinely carry short first-name announcements ('CJ', 'Ja'). Each becomes an UNKNOWN placeholder: the owner's roster counts exclude it, and the actually-drafted player keeps …
- **Action** — Before the length guard, check q against a set of legitimate pool name tokens (built at load: every whitespace token of every pool name that is >=2 chars and alphabetic), or add the seven tokens to NICKNAMES; port identically to the deck's matchCandidates; replace check_parity's 'aj'→[] expectation with 'aj'→['AJ Dybantsa']; add a test_draft case for the two-letter first names.

### R4-F06 · build_deck gate 1b deadlocks: its own prescribed bypass (--allow-unmatched) can never satisfy it

`REGRESSION` · verdict **CONFIRMED** · *measured*

A4's gate 1b (scripts/build_deck.py:56-61) hard-fails on ver['unmatched_count'] > 0 and tells the operator to 're-run verify_rosters.py --allow-unmatched and state the reason in the freshness note'. But --allow-unmatched (scripts/verify_rosters.py:94) only changes verify_rosters' EXIT CODE — the artifact still records unmatched_count > 0 and records no allow/reason flag — so build_deck fails again with the identical message. There is no path through the sanctioned pipeline for a pool containing any legitimately rosterless non-FA player; the only escapes are hand-editing data/roster_verification.json or deleting the row.

- **Evidence** — Reproduced end-to-end in scratch clone: appended a pool row on no official roster, re-dated the evidence file to today, stamped freshness with a stated reason, ran `verify_rosters.py --allow-unmatched` (exit 0, 'UNMATCHED (1): Testy McTest'), then `build_deck.py` → 'BUILD REFUSED — roster verification has 1 unmatched row(s) (Testy McTest) — ... re-run verify_rosters.py --allow-unmatched and state the reason in the freshness note' (exit 1) — the exact instruction already followed. …
- **Cost** — October rebuild eve: a two-way stash, an unsigned FA carried under a projected team code, or a player traded after the evidence pull makes the deck unrebuildable through the SLA pipeline. Under …
- **Action** — Record the bypass in the artifact (e.g. "allow_unmatched": true plus the unmatched list) when the flag is passed, and have gate 1b accept unmatched_count>0 only when that field is present, echoing the unmatched names into the build output and manifest so the exemption is loud and auditable.
- **Owner question** — When a pool row legitimately sits on no official roster (unsigned FA projected to a team, two-way stash), what should the sanctioned publish path be — artifact-recorded bypass as proposed, or reclassifying such rows to …


---

## HIGH — Re-verification of round-3 measurements

### R4-F07 · m33's champ gain is ~74% a TEAM_WEEK_SHOCK x weight artifact ECW cannot see; mechanism E24 lacks is now measurable

`KNOWN-PARTIAL — E24 / SEPTEMBER-PLAN §7.4` · verdict **CONFIRMED** · *measured*

The report's unresolved ECW-vs-champ incoherence (m33: ECW +0.002 but champ +1.17) is real and now explained: ECW (pwins_total in bench_weight_study.py, check_parity's _pwins, and the deck's pwinsTotal behind the A6 cats/wk margin) uses only team_week_model base variance, while simulate_seasons additionally applies a multiplicative TEAM_WEEK_SHOCK=0.06 to counting-cat means (arena/arena.py:394-395) whose sd scales linearly with BENCH_WEIGHT while base sd scales as sqrt(w). Re-running the four mocks at 2000x3 seeds with shock on vs 0: m33 (unpunted) delta +1.62 -> +0.42 (~74% of the gain is the shock channel); the three punted mocks move the OPPOSITE way (m31 +7.28 -> +8.58, m32 +1.70 -> +2.37, m34 +6.53 -> +7.27). So the punt interaction registered …

- **Evidence** — Ran /tmp scratch shock_all.py and mechanism.py against committed states arena/data/states/draft_state_mock31-34.json. Verbatim: 'mock 33 punt=none delta shock-on +1.62 shock-off +0.42 shock share 74%'; 'mock 31 ... shock-on +7.28 shock-off +8.58 shock share -18%'; 'mock 32 ... +1.70/+2.37 -39%'; 'mock 34 ... +6.53/+7.27 -11%'. Per-cat table (mechanism.py): m33 ECW 4.650->4.652 (+0.002) exactly reproducing the report while per-cat p's move up to +-0.099. Code: arena/arena.py:392-404 (shock …
- **Cost** — E24's ship bar says 'a mechanism must be identified before it ships.' Without this decomposition the September session would either not ship a correction that is real for punt builds, or ship one …
- **Action** — Append to E24: (1) require shock-on AND shock-off arms in the re-baseline re-grade so the mean-level effect is separated from the shock artifact; (2) test §7.4's punt hypothesis on the shock-off arm (pre-registered prediction from this session, dated 2026-08-10: punted-vs-unpunted gap WIDENS with shock off); (3) document that ECW excludes TEAM_WEEK_SHOCK wherever ECW is displayed next to champ%, or add a shock-aware …


---

## HIGH — Skill / protocol coherence

### R4-F08 · Live-turn I/O channel undefined after A3: no written path for picks, deck Top-5, or margins to reach the session

`REGRESSION` · verdict **PARTIALLY_CONFIRMED** · *reasoned*

A3 introduced a one-way dependency without a channel: SKILL.md §3 (lines 51, 55) defines the owner's-turn candidate list as "the deck's Top-5" and breaks kept-z ties on "the deck's margin," but no sentence says how the session obtains those names or that margin — the deck runs in the owner's browser, hoops.py contains no blend50/decw code, check_parity.py is a pre-flight gate not usable under the one-command SPEED RULE, and line 55's fallback keys on "the deck is unreachable," a condition the session cannot evaluate. Line 41's Export/Import reconciliation names the buttons but no cadence or file-transfer step. The pick-input path itself IS written (owner feeds per §1/§2/§4, with RESYNC-by-paste as the file-free recovery), but its now-implied cost — …

- **Evidence** — /home/user/yahoo-fantasy-basketball/.claude/skills/fantasy-basketball/SKILL.md lines 33, 41, 43, 48, 51, 55 (read in full this session). Walked the turn mechanically in a scratch draft: with no feed from the owner, hoops state stays empty, `--expect N` is meaningless, and the punt-coherence layer (the SKILL's own 'single most valuable thing you add', line 38) has nothing to annotate. Round-3's registered finding (analysis_2026-08-09_findings_table.md line 123) covered only 'which surface …
- **Cost** — On draft night the executing session must improvise the entire I/O protocol at a 45-second clock: either the owner double-enters every pick (the exact burden the deck doctrine was meant to remove) or …
- **Action** — Add an explicit I/O contract to §2/§3: (a) whether the owner pastes each pick run to Claude in addition to typing it into the deck, or only engages Claude at his own turns; (b) at the owner's turn, he pastes the deck's Top-5 names + margin (one line) OR Claude annotates its own fallback order and says so; (c) export/import cadence — e.g. deck Export → file dropped in cwd at each SYNC, never mid-clock.
- **Owner question** — On draft night, will you paste the pick feed to Claude as well as typing it into the deck, or do you want Claude consulted only at your turns (and if so, will you paste the deck's Top-5 line)?

### R4-F09 · The ~0.25 kept-z 'within noise' band is uncalibrated and fires at 12 of 13 board depths

`REGRESSION` · verdict **CONFIRMED** · *measured*

SKILL §3's near-tie rule ('two candidates within ~0.25 kept-z … within noise') has no provenance on the kept-z scale — the 0.25 figure is transplanted from the deck's retired coin-flip threshold, which was defined on the composite blend score ('top two within 0.25z of composite score'), a different unit, and the same A6 commit that retired it explicitly deferred re-deriving any threshold to September. Measured against the actual pool, the band is far too wide to be a tiebreak: the top-2 punt-aware gap is under 0.25 kept-z at 12 of 13 round-representative board states, and 97% of all adjacent-pair gaps in the pool are under 0.25 (median 0.027). So the clause declares essentially every turn a near-tie, colliding with the same paragraph's 'one …

- **Evidence** — git show e944015: removed deck comment '/* Coin-flip tag: top two within 0.25z of composite score */' and commit text 'Re-deriving a threshold on the cats/wk scale is a September item'. Grep of LESSONS.md, SEPTEMBER-PLAN.md, both analysis_2026-08-09 files: no 0.25-kept-z calibration anywhere. Measured this session (python over hoops.zscores, punt FT%): top-2 gaps after removing 0/12/24/…/144 top players = 0.162, 0.501, 0.000, 0.057, 0.113, 0.064, 0.020, 0.006, 0.009, 0.115, 0.015, 0.014, 0.043 …
- **Cost** — In October the rule as written makes 'within noise on kept-z' the correct utterance on nearly every pick from round 2 on, hollowing out the commit-to-one-pick doctrine — exactly the confidently-wrong …
- **Action** — Strike the number until the September recalibration the A6 commit already promised, or set the band from data (e.g. the kept-z gap below which replayed mock outcomes are order-invariant); interim wording: near-tie only when the top-2 gap is within the median adjacent-pool gap (~0.03), not 0.25.

### R4-F10 · §3 format 'kept-z ±X.XX under the declared punt' is not producible from the one allowed command

`REGRESSION` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md §3's new output format (e944015) mandates quoting 'kept-z ±X.XX' but the one-command `draft turn` card headlines adj_value, which for *-risk rows is 0.78 × kept-z (AD under punt FT%: kept-z 6.00, card 'val +4.68*' — a 22% mismatch, and the same section's healthy-tiebreak names the adjusted number as 'the reference'). Because the deck's Top-5 is punt-blind and the card's default --top is 8, deck candidates can rank off the punt-aware card entirely (reproduced: Maxey 15th, Edwards 11th under punt FT% after 8 picks); their kept-z is then only reachable by preemptively raising --top on the same command or summing the row's printed per-category z's — neither of which §3 instructs, and both impractical on a 45-second clock. The ± sign semantics …

- **Evidence** — Reproduced this session in a scratch draft (draft init --punt FT%, 8-pick feed): card row 'Anthony Davis … val +4.68*' vs hoops.total_value(AD, ('FT%',)) = 6.00 (hoops.py:345-349 applies the 0.78 haircut; fmt_row hoops.py:463-471 prints the adjusted number). Python repro over the same state: punt-blind value top-5 = [Davis, Haliburton, Maxey, Edwards, Holmgren]; punt-aware card top-8 omits Maxey and Edwards. Card default --top is 8 (hoops.py:1201). SKILL.md lines 53-55.
- **Cost** — Every October turn where the deck's Top-5 diverges from the punt board (the exact situation the punt-coherence layer exists for), the session must either break the SPEED RULE, report an adjusted …
- **Action** — Define the quoted number as the card's val (adjusted, with * relayed) and rename the format token; or add a one-command flag `draft turn "..." --card "A,B,C,D,E"` that prints raw kept-z + adjusted for exactly the named candidates; state that ±X.XX is the signed kept-z level.


---

## MEDIUM — Published artifact & deck truth

### R4-F11 · F18's colophon sentence is still in the source, but the action map records it under A10 which the commit declares fixed

`KNOWN-PARTIAL — F18 (A10)` · verdict **CONFIRMED** · *measured*

docs/draft-deck.html:404 still ends with the exact sentence F18 confirmed false in both halves: 'Mock opponents are 9 value-drafters + 2 market seats, so discounted vets leave mock boards early and stars fall further than real rooms' — the deck has seated the 11 named league-mates since E18, and the measured direction is the reverse (synthetic market ~0.45x real divergence, so real rooms produce DEEPER falls). What exceeds the registered scope is the accounting defect: the round-3 action map assigns F18 to A10, commit 25f41bc declares A10 'Fixed', but its only deck change was weeklyAvail — so the September session reading the map will believe F18 is closed and never touch it. Same paragraph, second false claim: 'The judgment layer … is authored …

- **Evidence** — docs/draft-deck.html:404 (verbatim, read this session). git show 25f41bc -- docs/draft-deck.html: sole hunk is weeklyAvail (F16 mirror); commit message's A10 paragraph names RESEARCH.md/README/REVERT-MAP/SKILL.md only. analysis_2026-08-09_self_critique_round3.md:265 '| A10 documentation truth | F18, F57, F58, F59, F63 |'. JUDGMENT byte-stability: F19 evidence + JUDGMENT.date still 2026-07-28 at :1234.
- **Cost** — The owner calibrates his real-draft instincts in mock mode against a colophon that teaches him the backwards expectation about star falls, and the tracking system's own ledger says the teaching was …
- **Action** — Include F18's rewrite (named 11-league-mate room; measured 0.45x direction with its asterisk; drop or past-tense the 'authored fresh' claim, or point it at gate 5) in the same republish commit as the Sochan fix; add a one-line correction to the action map or SEPTEMBER-PLAN noting A10 shipped without its F18 component.

### R4-F12 · Gate 4 (pool moved-or-explained) is silently inert for exactly the next build — the one that must fix Sochan

`REGRESSION` · verdict **PARTIALLY_CONFIRMED** · *measured*

A4's gate 4 reads the previous build's pool_sha256 from the deck's build-manifest comment, but the shipped deck's manifest was written by the OLD build_deck.py (2026-08-05) whose schema has no pool_sha256 key, so prev_hash is None and the check is skipped without a word — and commit 1cc113e touched no deck file, so nothing armed it retroactively. Reproduced: in a scratch copy with byte-identical players.csv and a freshness note containing none of the quiet keywords, the first build succeeded ("safe to publish"); only the second build refused ("byte-identical"). Two lesser brittlenesses in the armed gate, both reproduced: an honest quiet note that avoids the four magic substrings is refused, while any note containing the bare word "quiet" passes as a …

- **Evidence** — scripts/build_deck.py:89-100 (`prev_hash = json.loads(prev.group(1)).get("pool_sha256") if prev else None`; keyword list :92-93). docs/draft-deck.html line 1: manifest has keys built/pool/verification/freshness_note only — no pool_sha256 (current players.csv sha ea38250b7a27). git show 1cc113e touched no deck file (retro-arming impossible). Simulation transcript: build 1 'safe to publish' with unchanged pool + non-keyword note; build 2 'BUILD REFUSED — byte-identical'.
- **Cost** — The very republish that closes findings 1-2 — the highest-stakes build between now and October — runs with the no-research-republish gate disarmed, the precise failure class (gates certify a date, …
- **Action** — One-commit fix, freeze-compatible: (a) have build_deck.py FAIL (not skip) when the manifest exists but lacks pool_sha256, with a message naming the quiet-note escape hatch, or retro-stamp the current deck's manifest with players.csv's real hash; (b) require the quiet-note keyword check to also demand a digit (source/query count) so a bare copied 'quiet' can't satisfy it.

### R4-F13 · Sochan/Mathurin JUDGMENT text still wrong in source AND published page; gate 5 now makes the fix cost a full refresh ceremony

`KNOWN-PARTIAL — F15/F19 (A4)` · verdict **PARTIALLY_CONFIRMED** · *measured*

Round 3 ordered the Sochan fix (F15 action) and the Sochan+Mathurin clear (F19 action); yesterday's A4 commit (1cc113e) shipped gate 5 but no commit in d3b4a49..e635809 touched the JUDGMENT text or date, and no A-item or September-plan entry owns the text fix. docs/draft-deck.html still ships Sochan "Unsigned after a limited NYK title-run role" (:1260) against POR/camp-deal in players.csv:202 and the same page's own FA→POR colophon, Mathurin "RFA frozen by the Kawhi investigation" (:1265) against LAC in players.csv:160, and JUDGMENT.date "2026-07-28" (:1234) — and the published artifact, built from the 2026-08-05 source whose JUDGMENT block is byte-identical, renders the same wrong prose. Gate 5 plus A4's evidence-date inheritance now (by design) …

- **Evidence** — docs/draft-deck.html:1234,:1260,:1265; data/players.csv:160,:202. Full gate simulation in /tmp scratch copy (repo untouched): build refusals in order — 'roster verification is stale (2026-08-05)' → after verify: 'stale (2026-08-04)' (evidence-date inheritance working) → after evidence re-date + stamp: 'JUDGMENT layer is dated 2026-07-28 but the pool is 2026-08-09' → after date bump: 'deck built: 246 players … safe to publish'. check_parity.py on real repo: 'PARITY: EXACT MATCH' exit 0.
- **Cost** — Until the ceremony runs, the owner's page fades Sochan for a reason the same page's colophon refutes — the exact confidently-wrong-prose class he caught himself twice — and every day it isn't run, …
- **Action** — Execute the nine-step ceremony above once, now; register 'JUDGMENT re-author' as an explicit named step in SKILL.md's refresh procedure so gate 5's refusal message is expected rather than a draft-week surprise.


---

## MEDIUM — Fantasy-domain comprehension, round 2

### R4-F14 · A 3-vs-4-game playoff week for a single starter swings that round's win probability by ±6.4pp in the sim's own weekly model — and nothing in the October build can see weeks 19-21 schedule density

`KNOWN-PARTIAL — F24 / T4 / §7.5 schema window` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL over F24/Q4/§7.5 — new contribution is the win-probability quantification, at corrected magnitudes. The sim (arena.py:362) and deck (draft-deck.html:1039) hard-code 3.5 games/wk for every player in every week, and players.csv carries no team-schedule linkage, so the October build cannot price weeks-19-21 density for the three 1-week playoff rounds (league_intel §1/§9). Reproduced with the arena's own week mechanics parameterized on games (seed-5 run_draft rosters, adjacent playoff-tier pair, baseline P(win wk)=0.586, 60k draws): a whole-team 3-game week vs an opponent 4-game week collapses P(win) to ~0.11 (~0.29 vs an ordinary 3.5 opponent); one ±1-game week for the roster's TOP starter swings ±5.5-6pp, for a typical starter …

- **Evidence** — Ran in-session: reimplemented team_week_model with games/week as a parameter, P(win week) via the arena's own week_result mechanics at 60,000 draws, on rosters drafted by arena.run_draft(seed 5), adjacent-strength pair. Results: 3.5v3.5=0.611; 3v3.5=0.270; 4v3.5=0.859; 3v4=0.075; single-player ±1 game: starters ±6.3-6.4pp, bench (w=0.15) ±0.7-0.8pp. Format ground truth: league_intel_2025-26.md §9 Q2 (playoffs weeks 19-21, three 1-week rounds). Schema: data/players.csv 15 cols, no …
- **Cost** — The owner's three-season failure mode is precisely the 3-week bracket (record ranks 3/8/1, never champion). A late-round pick or playoff-week stream chosen blind to weeks 19-21 density forfeits an …
- **Action** — At the September schema window (§7.5 already reserves it), add per-player weeks-19-21 game counts once the 2026-27 NBA schedule publishes (mid-August); have the October build surface a playoff-density column on the card and the E9 playoff-tier objective consume it. This finding supplies the quantified basis the round-3 owner question lacked.

### R4-F15 · In-season stash-vs-drop advice is contradictory across surfaces: a top-20-equivalent recovery player is invisible to rank/best but counted at full value by trade, and no surface knows the 2 IL+ slots make stashes roster-free

`KNOWN-PARTIAL — F26 / F37 / E15 (closed for drafts only)` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL (F26/F37/E15), correctly labeled. Fully registered already: cmd_trade's raw-z sum with no availability term and the resulting board-invisible-but-trades-at-+2.77 Butler contradiction is F26 verbatim, with the availability-adjusted trade fix already F26's registered action. Genuinely beyond the baseline: (1) E15 was closed by owner rule Q6 for DRAFTS only ("no stash-drafting logic will be added"), yet SKILL.md triggers route in-season stash/drop/waiver/trade questions into the same tools, and SKILL.md line 57's "never recommend one" plus board invisibility create an unregistered drop-side failure mode — treating a free-to-hold, IL+-eligible, top-20-equivalent recovery asset (Butler, raw z +2.77, healthy-equivalent rank #20) as …

- **Evidence** — Measured in-session on live data/players.csv: 5 availability-0 rows; Jimmy Butler note 'acl-recovery-jan26 (return ~2027)' raw z +2.77 = healthy-equivalent rank ~#20; DiVincenzo -1.60 (~#110). Code: hoops.py availability() 301-342 (recovery -> 0.0), cmd_rank 498-508 (excludes), cmd_trade 517-534 (raw z, no availability — F26). League: league_intel_2025-26.md §1 (2 IL+), §9 Q6. SKILL.md:3 triggers on 'waiver wire'; grep of SKILL.md finds no in-season/IL+ rule.
- **Cost** — First serious injury to an October-drafted player (the owner is risk-tolerant: Kawhi/KP/Murray class) produces either a mistaken drop of a free-to-hold top-20 asset or a trade evaluation pricing a …
- **Action** — Two cheap truth fixes: (1) one SKILL.md line: in-season stash/drop/trade questions must state IL+ economics (recovery players cost 0 active slots if IL-eligible) and never read board absence as droppability; (2) implement F26's already-registered action (availability-adjusted trade delta) before the season starts.
- **Owner question** — In-season, do you want hoops.py to grow a real waiver/stash surface (rank including IL-stashable players with a stash tag), or keep the engine draft-only and handle waivers as judgment?


---

## MEDIUM — October readiness & performance

### R4-F16 · E24 mechanism: three concrete September experiments, grounded in the three places BENCH_WEIGHT actually enters team_week_model

`KNOWN-PARTIAL — E24/§7.2, §7.4` · verdict **CONFIRMED** · *measured*

Code reading pins where the constant acts — arena/arena.py team_week_model (line ~350) applies the lineup weight w in three separable channels: (a) counting-cat mu (mu[c] += w*x*g), (b) counting-cat variance (var[c] += w*(...)), and (c) the FG%/FT% attempt pools (fg_at/ft_at scale with w, moving BOTH the %-mix mean and the binomial variance floor, which is ∝1/attempts). Channel (c) is unregistered anywhere and is a live candidate for the §7.4 punt-interaction pattern, since all three punted study mocks punt a % category. Proposed designs: M1 — channel ablation: 8 CRN arms {0.15,0.956}^3 over (mu, var, pct) on mocks 31-34, seeds 11/23/47 at N=6000; bar: one named channel (or pair) reproduces the sign and ≥70% of the full-correction Δchamp% in ≥3/4 …

- **Evidence** — arena/arena.py:350-382 (team_week_model, w in all three channels — read verbatim this session); arena/arena.py:143-166 (lineup_weights/BENCH_WEIGHT); my --quick replication (direction 4/4, m33 smallest — consistent with §7.4's punted-vs-unpunted split); pwins_total closed form in arena/mocks/bench_weight_study.py:46-55.
- **Cost** — Without a mechanism E24 stays unshippable by its own registered bar, and every LEDGER champ% stays conditional on a constant known to be ~6.4x wrong. M2 costs minutes and could settle §7.4 before the …
- **Action** — Queue M2 (cheap, closed-form) first, M1 second, M3 as the tiebreaker, into the September session's E24 block; pre-register the M2 prediction above with today's date before any of them runs.

### R4-F17 · Nothing fires between Oct 12 and draft night, and the October prompt's self-reschedule clause is doubly inert

`KNOWN-PARTIAL — A20 (F33)` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL F33/A20, with one genuinely new increment. Confirmed and already registered in F33: only two enabled triggers exist (Sept 1, Oct 12 2026-10-12T14:00Z), nothing fires after Oct 12, no firm draft date is recorded (league_intel:142 "date TBD"), and the cost — a deck up to ~7-10 days stale through final-cuts week — plus the remedies (record the date; add a draft-eve T-1 Routine) are all in F33's registered text. The new increment beyond F33: the October prompt's self-reschedule clause is inert by construction, not merely blocked on the missing date — any draft date consistent with the recorded "week before the NBA season opens" (~Oct 13-20) is within the clause's ~10-day threshold of the Oct 12 firing, so the clause can never trigger even …

- **Evidence** — list_triggers pages 1-2 (120 entries, newest-first; every entry after 2026-10-12 is nonexistent, all other entries are ended send_later one-shots). October Routine prompt quoted in this session. arena/results/league_intel_2025-26.md:142,165.
- **Cost** — The deck the owner drafts from can be up to ~7 days stale through the highest-churn week of the NBA calendar (final cuts, camp injuries, opening-night rotations) — the same class of gap as the two …
- **Action** — Mechanize in two parts: (1) append to §6 a final step — 'before closing, create a one-shot draft-eve Routine (T-1 day, or T-0 morning) that executes §6 steps 1 and 5 only: pool pull + verify_rosters + freshness stamp + build_deck + republish + WebFetch built-date assert' — so the October session schedules its own follow-up with the date it will by then know; (2) record the firm draft date in league_intel the moment …
- **Owner question** — What is the actual draft date/time once your league schedules it on Yahoo? (One line in league_intel unblocks the whole chain.)

### R4-F18 · Q3-Q8 ranked: the real deadline is Sept 1 (22 days), and Q4/Q3 must land before it

`KNOWN-PARTIAL — Q3-Q8` · verdict **CONFIRMED** · *measured*

The binding date for the open questions is not October — it is the September Routine firing 2026-09-01T14:00Z, because that session executes the plan whose shape the answers determine. Ranked by cost of silence: 1) Q4 (projection source) — gates §1.2b multi-source synthesis AND the §7.5/A14 schema window (gp/min/age/adp/uncertainty 'cannot be retrofitted after October'); unanswered, the September session either picks the anchor itself (a domain judgment the owner reserved) or defers and the schema window closes. 2) Q3 (mock 10-30 states) — gates the §7.5 backfill fork; unanswered, September must mark LEDGER §5 and all format_delta states [UNREPRODUCIBLE] and rewrite the E8/E9/E9b bars against mocks 31-34, a bar rewrite performed under time pressure …

- **Evidence** — SEPTEMBER-PLAN.md:59-65 (§1.2b), 249-263 (§7.5 backfill + schema window); round3 §4 Q-texts (analysis_2026-08-09_self_critique_round3.md:290-309); docs/draft-deck.html build-manifest '"mode": "fallback-partial"' (read this session); September Routine firing time from list_triggers.
- **Cost** — Concretely in October: an unanchored projection synthesis (Q4), regression bars rewritten mid-run (Q3), and a roster lock blind to camp trades during cut week (Q6) — each individually the kind of …
- **Action** — Send the owner a six-line answer sheet ordered as above, with the header 'Q4 and Q3 need answers before Sept 1; the rest before Oct 1.' Q8 can even be answered by pasting a screenshot of the league settings page.
- **Owner question** — Q4 first: which projection source anchors October, and do you want the weeks-19-21 schedule-density column? Q3 second: do the mock 10-30 draft_state JSONs still exist anywhere?

### R4-F19 · Republish is the definition of done for both Routines, but the Artifact tool grant is unconfirmed and absent from their stored tool lists

`KNOWN-PARTIAL — A19 (F56)` · verdict **PARTIALLY_CONFIRMED** · *measured*

Both Routines exist, are enabled, fire 2026-09-01T14:00Z and 2026-10-12T14:00Z, command republish to the standing artifact URL, and their stored allowed_tools lists (verbatim as quoted) contain no 'Artifact' entry — all reproduced this session. A19's grant-confirmation step remains undone as of 2026-08-10, and the stored grant is immutable via update_trigger (schema exposes only name/cron/enabled/model/prompt/run_once_at), so any fix requires delete+recreate from a session holding the tool — this immutability point and the still-undone re-verification are the only elements exceeding registered F56/A19. However, absence from allowed_tools does not prove the tool is unavailable: this session's own stored trigger carries the identical Artifact-less …

- **Evidence** — list_triggers (this session, 2026-08-10): full trigger objects for trig_01DDZDEUyLJnmeU4mGWtnGWA and trig_0146xxp4wAt4uHQypXLxjNZ1 — enabled=True, run_once_at as stated, prompts quoted, allowed_tools lists quoted verbatim (no Artifact). arena/results/SEPTEMBER-PLAN.md:105-107, 156-159, 245-247. analysis_2026-08-09_self_critique_round3.md:246 (A19 text).
- **Cost** — If the fired session cannot invoke Artifact (or stalls on a permission prompt with no human at 14:00Z), the October refresh builds a perfect deck that never reaches the page the owner opens on draft …
- **Action** — Before 2026-09-01: from a session that demonstrably holds the Artifact tool, publish a no-op redeploy of the artifact URL to prove the grant, then either (a) confirm preset:default includes Artifact for fired sessions, or (b) delete+recreate both Routines from that session so the grant is captured. Add one sentence to §6.5: 'If the Artifact tool is unavailable at republish time, STOP, SendUserFile the built …

### R4-F20 · bench_weight_study.py --quick silently overwrites the committed E24 evidence artifact; runtime claims off ~4x

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

arena/mocks/bench_weight_study.py writes arena/results/bench_weight_study_out.json whenever --seeds is not passed (no --out flag; --seeds retags the filename but a plain --quick run clobbers the committed 18,000-seasons/arm E24 evidence in place, recoverable only via git checkout if someone notices git status). Nothing in the repo validates the artifact's seasons_per_seed, so a September "--quick sanity check" silently replaces E24's quantitative basis with an N=4500/arm rerun. The docstring's "--quick ~40s" is wrong by several-fold: Phase 1 alone re-runs the committed 6000x3-season integrity check regardless of --quick, and a timed quick run here was still mid-Phase-1 well past the 40s mark (finder measured 2m30s total; not fully re-timed in this …

- **Evidence** — Ran `time python3 arena/mocks/bench_weight_study.py --quick` (real 2m30.4s); output tail quoted in session; `git status --porcelain` → ' M arena/results/bench_weight_study_out.json', restored. Script header lines 4-5 (~40s/~5min claims); line ~132 writes the fixed path.
- **Cost** — A September session told to 'sanity-check E24 first' with --quick destroys the committed full-run evidence in place; the JSON's seasons_per_seed field is the only tell, and nothing checks it. E24's …
- **Action** — September (or now, as a truth fix under the freeze's tooling allowance): give the script an --out defaulting to a dated scratch filename, refuse to overwrite an existing results file whose seasons_per_seed differs, and correct the docstring runtimes to measured values.


---

## MEDIUM — Regressions in the 2026-08-09 commits

### R4-F21 · Gate 4's quiet-day bypass is substring matching: any note containing 'quiet' or 'no change' publishes an unchanged pool

`REGRESSION` · verdict **CONFIRMED** · *measured*

Gate 4 (scripts/build_deck.py:91-94) exists to catch 'a build that republishes an unchanged pool under a fresh date', but its escape valve is `any(k in note_l for k in ('no change','zero confirmed','zero pool','quiet'))` over the whole freshness note. A note that admits pending work while containing one of those substrings passes: 'quiet on injuries; MAJOR: Giannis traded to HOU, pool update pending' → quiet_ok=True, unchanged pool publishes. Since the note author is the same agent whose diligence the gate distrusts (the F04 lesson), keyword presence is not evidence the sweep found nothing — the gate re-admits the self-attestation A4 was built to remove. Note also gate 4 is inert on the first post-A4 build: the current deck manifest has no …

- **Evidence** — Ran the exact predicate from build_deck.py:92-93 against four notes: 'no changes to speak of, but the Porzingis trade reshuffled three rotations' → True; 'quiet on injuries; MAJOR: Giannis traded to HOU, pool update pending' → True; 'swept ESPN + Rotowire, zero confirmed roster changes' → True (intended); 'minor stat corrections applied to 3 rows' → False (correctly fails when the claimed corrections didn't land). Manifest check on docs/draft-deck.html: regex matches, json parses, pool_sha256 …
- **Cost** — The gate's core scenario — a sweep that found a pool-moving event but didn't apply it — publishes anyway whenever the note ALSO says the injury front was quiet, which is the natural phrasing of …
- **Action** — Require an explicit structured assertion instead of substrings: e.g. the freshness stamp gains a boolean field (--no-pool-changes) that the stamp command only sets when passed deliberately, and gate 4 checks that field; keep the keyword scan only as a hint in the refusal message.

### R4-F22 · build_deck gate 5's JUDGMENT orphan check is dead code — its regex can never match the actual deck

`REGRESSION` · verdict **CONFIRMED** · *measured*

Gate 5's players-block regex (scripts/build_deck.py:123, r"\n players: \{(.*?)\n \},?\n") requires a newline AFTER the block's closing ' },' — but `players:` is the LAST key of the JUDGMENT object, so inside the captured JUDGMENT body (which the outer regex truncates at '\n};') the closing ' },' is the final characters with no trailing newline. pmatch is always None, the orphan check (a JUDGMENT entry naming a player absent from the pool) is silently skipped, and gate 5 reports only the date check it did run. The gate shipped never having been seen to fire on the defect it was written for.

- **Evidence** — Reproduced against the real deck: JUDGMENT body found, date parsed (2026-07-28), 'players sub-block found: False'; body tail is '...durability." },\n },' — ends at ' },' with no trailing newline. Injected '"Zzz Fakeplayer": { adj: 0.9 ... }' into a scratch copy's players block and ran gate 5's exact code: 'orphan check SKIPPED (pmatch=None) — Zzz Fakeplayer sails through gate 5'. The line-count check confirms exactly one ' },' line exists in the body and it is terminal.
- **Cost** — The certification A4 claims — 'an entry for an undraftable player renders a rationale for a row that does not exist' is caught — is not provided. A JUDGMENT fade/boost entry for a player later …
- **Action** — Change the pattern to tolerate end-of-body (e.g. r"\n players: \{(.*?)\n \}" with re.S, or parse to the outer close), and make gate 5 FAIL when the players block cannot be located rather than silently skipping — the block's absence is markup drift, which gate 5 already treats as fatal one regex earlier. Add a mutation test (fake JUDGMENT name → build must refuse) alongside check_parity in the pre-publish checklist.


---

## MEDIUM — Re-verification of round-3 measurements

### R4-F23 · 0.956 assumes 13 independent NBA schedules; real teammate stacking moves it to 0.940, absences to 0.968

`KNOWN-PARTIAL — E24` · verdict **CONFIRMED** · *measured*

bench_share_fit.py draws an independent team_week() schedule for every rostered player, but the 144 arena rosters it measures naturally stack teammates: mean 2.18 shared-NBA-team pairs per roster (max 9; only 8 of 144 rosters have zero). Sharing schedules among same-team players (which correlates their game days and sharpens slot competition) moves the relative weight 0.956 -> 0.940. Adding the other realism the fit excludes — teammates missing 12%+ of games at their availability tiers, which frees slots — moves it to 0.968. The wide 2/3/4-game-week variance mix changes nothing (0.955). So the headline is robust in class (every variant sits 6.2-6.5x above the shipped 0.15) but 0.956 is a point inside a ~0.94-0.97 model band, and §7's bounds list …

- **Evidence** — Baseline reproduced exactly: 'ranks 1-10 start-share : 0.997 / ranks 11-13 : 0.953 / RELATIVE WEIGHT: 0.956' (arena/mocks/bench_share_fit.py, this session). My variant harness (scratchpad bench_fit_variants.py, same 144 rosters, same fill(), seed 99): 'A independent 0.956; B shared-team schedules 0.940; C wide variance 0.955; E shared-team + teammate absences 0.968'. Stacking count: '144 rosters; shared-NBA-team pairs per roster: mean 2.18 min 0 max 9'. Independence assumption: …
- **Cost** — If September adopts 0.956 as a point constant it inherits ~+-0.015 of schedule-model error — immaterial next to the 0.15 correction, but the report's error-analysis section presents the number with …
- **Action** — Add the two bounds to E24's row (independence of teammate schedules: -0.016; teammate absences: +0.028 on top of correlation) and have the re-baseline fit use team-shared schedules via p['team'] — a 6-line change to the committed harness.

### R4-F24 · A17's leading-tag fix left 5 substring note-parsers alive: rec_ct, rec_compound x2, market 'risk', deck recCt

`KNOWN-PARTIAL — A17 / F16` · verdict **CONFIRMED** · *measured*

A17's leading-tag fix covered only the three availability-tier functions (hoops.availability, arena.weekly_availability, deck weeklyAvail). Six consumers still substring-match the WHOLE note: arena/arena.py:211 (rec_ct), :272 (rec_compound compounding), :192 (market 'risk' multiplier), and their deck mirrors docs/draft-deck.html:1120 (recCt), :1174 (rec_compound), :874 (marketRanks 'risk'). JS<->Python parity still holds for these — both sides are identically unpatched — but the F16 landmine class survives in all six: the documented re-entry convention ('inj-<reason>-risk' tag plus explanatory prose, blessed by SKILL.md's 'tag first, commentary after' rule) means a returnee whose refresh note gains '(recovery on track)' is silently extra-discounted …

- **Evidence** — grep verbatim: arena/arena.py:211 'if "recovery" in (p.get("note") or "").lower():'; :272 'if params["rec_compound"] and "recovery" in note:'; :192 'if "risk" in note:'; docs/draft-deck.html:1120 'if ((p.note || "").toLowerCase().includes("recovery")) recCt++;'; :1174 'if (params.rec_compound && note.includes("recovery"))'. Verified today's exposure is zero on both pools: my scratch scan found 0 rows in data/players.csv and arena/data/players_2025-10-21.csv with 'risk'/'recovery' in prose after …
- **Cost** — Zero rows affected today (verified), so this is latent — but the October daily-refresh loop is precisely what writes new prose into notes, and the four re-entered returnees (Haliburton ~top-12 by …
- **Action** — Register an A17b: route all five consumers through one shared leading-tag helper (hoops-side tag(), deck-side tagOf()), and add the 'prose must never contain risk/recovery' rule as a validate/freshness-gate check rather than a documentation promise. Small, freeze-compatible as a gate; the parser unification can wait for September.

### R4-F25 · bench_weight_study.py --quick silently overwrites the committed evidence JSON; I clobbered and restored it

`REGRESSION` · verdict **CONFIRMED** · *measured*

Running the study with --quick (the mode its own docstring advertises, '~40s, N=1500') writes its low-N output to arena/results/bench_weight_study_out.json — the SAME path as the committed 18,000-season evidence artifact the report's §10 cites. There is no tag distinguishing quick output (only --seeds gets a filename tag, bench_weight_study.py:99,160). Any future session that follows the report's 'regenerate' instructions with --quick destroys the committed evidence and leaves a plausible-looking but 4x-noisier file in its place — the exact failure mode lesson 13 exists to prevent, introduced by the commit that created the lesson-13 harness.

- **Evidence** — I reproduced it in this session: after 'python3 arena/mocks/bench_weight_study.py --quick', 'git status --porcelain' showed 'M arena/results/bench_weight_study_out.json' (header printed 'seasons_per_seed'=1500 into the JSON); restored via git checkout. Code: arena/mocks/bench_weight_study.py:99 'tag = "" if not args.seeds else ...' and :160 'dest = f"arena/results/bench_weight_study{tag}_out.json"' — args.quick never reaches the filename. Introduced in commit c03349f (2026-08-09).
- **Cost** — The re-grade's headline numbers (+7.01/+2.08/+1.17/+5.96) live in that JSON; the September Routine session, primed to 'regenerate' evidence, can silently replace them with N=1500 values that differ …
- **Action** — One-line fix when the freeze allows: include a '_quick' tag in dest when args.quick (or refuse to overwrite an existing file whose seasons_per_seed differs). Until then, add a warning line to the report §10 / SEPTEMBER-PLAN 7.5 that --quick must not be run from a clean checkout without reverting the JSON afterwards.


---

## MEDIUM — Skill / protocol coherence

### R4-F26 · Evals 4-6 predate the deck-surface doctrine and eval 4's premise contradicts its own expected output

`REGRESSION` · verdict **PARTIALLY_CONFIRMED** · *measured*

The live-draft evals (4-6) were added in 8bd32e1 (2026-08-09 04:20), ~2.5h before the deck-surface doctrine landed in e944015 (06:53, which touched only SKILL.md and draft-deck.html), and were never revisited: the suite contains zero references to deck-governs, the deck Top-5 candidate list, kept-z output format, or the fallback disclosure, so the skill's only regression suite has no coverage of the doctrine layer — though the commands it does test (draft turn feed, SYNC, RESYNC) remain protocol-mandated as hoops.py's state-integrity role, so the suite is incomplete rather than certifying a wrong path. Separately, eval 4 is internally contradictory as written: its prompt tag "[mid-draft, user is on the clock]" is false for its own feed (after the …

- **Evidence** — evals/evals.json lines 24-38 (read in full); git log --oneline -- evals/evals.json shows the file's only 2026-08-09 change is 8bd32e1; e944015 (A3 doctrine) touched only SKILL.md and draft-deck.html. Runtime behavior of the three commands themselves verified this session: draft status --tail 6 and draft resync outputs match evals 5-6 exactly.
- **Cost** — The skill's only regression suite for the October protocol passes a session that ignores the deck doctrine entirely; eval 4 cannot be graded consistently as written.
- **Action** — Fix eval 4's bracket to '[mid-draft, user NOT on the clock after this feed]'; add one eval where the user IS on the clock expecting deck-Top-5 annotation + kept-z lines + fallback wording when the deck is unreachable.

### R4-F27 · SKILL §3 describes deck features (cats/wk margin) that exist only in unpublished source; no gate forces a code republish

`KNOWN-PARTIAL — A19 / owner-law 1d (republish freshness)` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL §3's tiebreak depends on the deck's cats/wk margin display, which exists only in unpublished source: the published artifact (built from the 2026-08-05 source, ac197ce) still renders the coin-flip/confidence output A6 retired, so until the next rebuild the owner's screen shows banned output and lacks the margin the protocol cites — live now for any mock/practice draft. Structurally, nothing detects source-vs-published code divergence: law 1d and A19/F56 key on data refreshes, build gates fire only when a rebuild runs, and the Prime checklist has no artifact-parity step. However, two registered mechanisms already mandate republish before draft night (SEPTEMBER-PLAN §4 definition-of-done at the ~09-01 run, which also ends the feature freeze, and …

- **Evidence** — SKILL.md:51; git show ac197ce:docs/draft-deck.html contains BUILD_PULL = "2026-08-05" and live rendering code `sc.textContent = \`coin flip (+${lead.toFixed(1)})\`` (line 2414 of that revision); 8bd32e1 commit message: 'The deck source is now ahead of the published artifact… ships with the next legitimate rebuild'; e944015: 'no rebuild was run, because none was earned'; SKILL §1 Prime checklist (line 47) contains no artifact-parity step.
- **Cost** — If no data-triggered rebuild happens before October (feature freeze makes that plausible), draft night runs with the deck displaying banned coin-flip/confidence output while the session is forbidden …
- **Action** — Extend owner-law 1d to code changes (any commit touching docs/draft-deck.html starts the republish clock) and add to the Prime checklist: fetch the artifact URL, assert the build manifest matches the source's engine hash/date (implements A19).

### R4-F28 · draft-arena skill and arena README still mandate the retired 'confidence card' in practice drafts

`REGRESSION` · verdict **CONFIRMED** · *measured*

A6 retired the confidence-% format in fantasy-basketball SKILL.md and the deck source, but three surfaces untouched since before A6 (last commits 2c87c51, bf99dce, 064b9ce — none touched by e944015 or the 25f41bc doc pass) still use the retired vocabulary: draft-arena/SKILL.md:12 instructs practice-draft sessions to 'present the standard confidence card'; arena/README.md:29 promises 'the normal draft turn confidence cards'; docs/cowork-vs-artifact.html:347/375/426 describe confidence percentages/cards as the system's current judgment layer. draft-arena step 0 does delegate to 'production draft turn flow... all owner rules' — which now carries the explicit dated ban — so a session that opens the fantasy-basketball skill resolves correctly; but the …

- **Evidence** — Grep this session: draft-arena/SKILL.md:12, arena/README.md:29, docs/cowork-vs-artifact.html:347/375/426/521. git log shows all three files last touched at 064b9ce, before e944015 (A6) — the doc-truth pass (25f41bc) did not touch them.
- **Cost** — Practice drafts between now and October — the main rehearsal channel — train the owner on a banned output format, and two skills give a session directly contradictory orders in the same turn.
- **Action** — One-line sweep: replace 'standard confidence card' / 'confidence cards' with 'the §3 calculated card (fantasy-basketball SKILL)' in draft-arena/SKILL.md and arena/README.md; mark cowork-vs-artifact.html's confidence references as historical or update them.


---

## LOW — Published artifact & deck truth

### R4-F29 · Feed hint hand-lists 5 ambiguous surnames; the pool mechanically contains 18, including Johnson x4

`KNOWN-PARTIAL — F22` · verdict **CONFIRMED** · *measured*

The feed hint (docs/draft-deck.html:306, identical on the published page) tells the owner to type 'first initial + surname' for '(White, Murray, Ball, Bridges, Sharpe…)'. Running the deck's own surnameKey logic over the live 246-row pool yields 18 ambiguous surnames; 13 are missing from the hint: johnson(4), williams(3), thompson(3), george(3), mitchell, jackson, brown, allen, robinson, green, porter, jones, wilson (murray is also 3-way, listed as if 2-way). F22's action already ordered mechanical regeneration at build time — what exceeds the registered scope: no shipped commit, no A-item component, and no September entry owns that sub-action (A5's shipped list covers fold/suffix/guards only), and this census quantifying the miss (5 of 18) did not …

- **Evidence** — docs/draft-deck.html:306 verbatim. Python census I ran over data/players.csv with the shipped surname_key semantics (NFKD fold, suffix strip): 'ambiguous surnames (mechanical): johnson 4, williams 3, thompson 3, murray 3, george 3, …18 total'; 'missing from hand list: allen, brown, george, green, jackson, johnson, jones, mitchell, porter, robinson, thompson, williams, wilson'.
- **Action** — Make build_deck.py regenerate the hint's parenthetical from the pool at inject time (it already rewrites three anchors); ship in the same republish.

### R4-F30 · Mobile/touch tooltip gap (F44) still open; the fix is ~12 display-only lines at one site

`KNOWN — F44` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN F44, still open at HEAD e635809: the tooltip layer remains mousemove-only (docs/draft-deck.html:1625-1628, plus scroll→hideTip at :1629) with no touch/click/focus path. 24 dataset.tip assignment sites plus 8 native title tooltips — 6 in markup (:313,:316,:343,:350,:353,:354, including the load-bearing build-agnostic/punt-blind disclosure at :316 and the Mkt/Val/Fit column definitions) and 2 assigned in JS (:2725 cat-drill instructions, :2791 chip-removal hint). The 8 title tooltips are unreachable on touch browsers; the 24 data-tip tooltips are degraded but partially reachable via tap-generated compatibility mouse events (no dismiss affordance), per the registered F44 verdict. Cheap fix is real but slightly larger than claimed: one delegated …

- **Evidence** — docs/draft-deck.html:1625-1628 (verbatim handler, read this session); counts I ran: 25 dataset.tip assignments, 6 title= attributes (:306 hint excluded, :316, :350, :353, :354, :364 region). No other addEventListener touches the tip layer (full listener grep this session).
- **Action** — Bundle the ~12-line handler + title mirroring into the same republish commit if the owner will use a touch device; skip otherwise.
- **Owner question** — Draft night device: laptop only, or possibly phone/tablet? (Registered as F44's open question — still unanswered and it gates whether this is worth the freeze window.)


---

## LOW — Fantasy-domain comprehension, round 2

### R4-F31 · Hand-guessed rookie tail lines shape the z baseline (5 of 14 sit inside the top-156 fixed point) but the exposure is bounded: a ±25% mis-guess moves veteran board ranks ≤7 spots, mean <1

`KNOWN-PARTIAL — F12 / F14 / F25` · verdict **CONFIRMED** · *measured*

F12/F14/F25 registered the stale tags and the market-hype premium (12-21 slots). The unmeasured half was the z-plane: rookie-proj rows feed zscores()' top-156 fixed point, so guessed stat lines move real players' values. Measured: 5 of the 14 rookie-proj rows (Coward, Dybantsa, Peterson, Boozer, Lendeborg) are inside the top-156 fixed point and therefore shape every league baseline. Scaling all 14 rookie stat lines ±25% and isolating the baseline effect (vet-vs-vet ranks, mechanical displacement excluded): mean |rank shift| 0.37-0.72 among the top 156 vets, max 7 (Jalen Duren 68->75 at x1.25); Jokic's z-sum moves 10.431->10.321. Real but bounded — an order of magnitude smaller than the same rows' market-model effect.

- **Evidence** — Ran in-session on live data/players.csv via hoops.zscores: rookie-proj rows n=14; top-156 membership 5; x0.75 vet-vs-vet moved 48/156 max 3 mean 0.37; x1.25 moved 71/156 max 7 mean 0.72; Jokic total_value 10.431->10.362/10.321. Fixed-point code: scripts/hoops.py:240-294.
- **Action** — Register this bound so September doesn't spend effort 'fixing' the z-plane exposure: the F25 action (retire stale tags, re-project the 2025 class from real production) already covers everything material. No additional guard needed.

### R4-F32 · Round-3's repeat-target lead is already closed: 21 of 24 repeat targets are in profiles.json loyalty and consumed by the deck; the 3 uncovered are the owner's own

`KNOWN — report_2026-08-09 §9 / E18a` · verdict **PARTIALLY_CONFIRMED** · *measured*

The candidate lead 'repeat-target intel is stored in a report, not consumed by any surface' is false on measurement. Of the 24 repeat targets in report §9, 20 are present in arena/profiles.json loyalty entries (incl. Robby's Sexton/Allen 3-peats, JCo's Jimmy Butler via suffix fold-match). The 4 absences all have documented justification: David's 3 (OG Anunoby, SGA, Jamal Murray) are correctly absent because the owner is not an opponent seat in the manager model, and Noah's Naz Reid is deliberately dropped with an in-file reason (the R8 leg was the 2025-26 autodraft). The deck consumes loyalty as flat rank discounts (draft-deck.html:922, applied at :977, names matching players.csv), and E18 calibration measured P(Robby drafts Jarrett Allen)=0.77. …

- **Evidence** — Ran the cross-reference in-session: covered 21/24; missing = David x3 only. arena/profiles.json managers.*.loyalty (entries printed verbatim); _meta loyalty policy; docs/draft-deck.html:922 'loyalty pulls as flat rank discounts'; report_2026-08-09_bench_regrade_and_integrity.md §9 table.
- **Action** — Mark the §9 lead consumed in the September report. Optionally add the owner's own repeat targets to the pre-draft brief as a 'your habits' line.


---

## LOW — October readiness & performance

### R4-F33 · Feature-freeze inventory verified clean: zero ordering or availability-tier change on current data from yesterday's commits

`KNOWN — A15/A17; report_2026-08-09 0-of-52 control` · verdict **CONFIRMED** · *measured*

Direct before/after measurement, ac197ce vs HEAD: (1) `hoops.py rank --top 200` byte-identical except the freshness header line (old script lacked a freshness.json beside it). (2) The availability() / weekly_availability() / weeklyAvail() leading-tag rewrites change ZERO rows on current data — I re-implemented old and new semantics side by side and swept both pools: live players.csv 246 rows, 0 tier changes; arena frozen pool 220 rows, 0 changes. The F16 fix is purely latent protection for future note shapes ('...-risk (recovery on track)'). (3) The deck's only ordering-adjacent change (empty-board pctRanks fallback) is monotone by construction and covered by the registered 0-of-52 orderings control; HEAD deck-vs-Python parity is EXACT MATCH on …

- **Evidence** — diff of rank_old.txt/rank_new.txt (only line 2 differs, quoted in session); availability sweep script output: 'availability changed: 0', 'weekly tier changed (live pool): 0', 'arena frozen pool rows: 220 weekly tier changed: 0'; `python3 scripts/check_parity.py` → PARITY: EXACT MATCH (1.36s); git diff ac197ce..e635809 for hoops.py/arena/arena.py/docs/draft-deck.html read in full for the engine-touching hunks.
- **Action** — Record this before/after check as a standing pre-merge step for any 'robustness-allowance' ship: `rank --top 200` diff + the two-pool availability sweep takes under a minute and would have been the first thing to catch a freeze violation.

### R4-F34 · Performance: every hot path measured — draft night runs at ~60ms/turn, and no code optimization is warranted

`NEW` · verdict **CONFIRMED** · *measured*

As stated, with two precision corrections: the A15 per-draft cost measured here is 129ms→172ms (+~33%, ~2.6s over a 60-draft cadence run) rather than +~12%/~1s — still trivial; and the bench_weight_study full-run '~10min' is an extrapolation from the measured 161s quick run, not a direct measurement.

- **Evidence** — All numbers from commands run this session and quoted in transcript: timing harness over ds_0/ds_50/ds_155 states built via `draft pick`; cProfile output (zscores 0.009s cum); `time` on check_parity.py, test_draft.py, arena cadence/slots, bench_weight_study --quick; old-vs-new run_draft_ordered timed against the ac197ce tree extracted via `git archive` to scratch.
- **Action** — Close the 'performance tune-up' half of the owner's ask with this table and no code changes; fold the docstring runtime corrections into the bench-study fix.

### R4-F35 · SKILL.md's 'gitignored scratch artifacts' claim is false — both intel JSONs are git-tracked, and the tracked cadence_intel.json is still the pre-A15 zero-ADP artifact

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL (F58, F11/A15): the false "gitignored scratch artifacts" sentence and the zero-ADP committed cadence_intel.json are both registered (F58's action explicitly says to fix the gitignored claim; A15's text names the committed artifact). What exceeds the registered scope: (1) yesterday's A10 doc-truth pass (25f41bc) edited that exact SKILL.md sentence — fixing the ~10-min runtime and adding the F58 staleness caveat — but left the F58-flagged "gitignored" falsehood standing, so a registered fix shipped incomplete on its own target line; (2) A15's code fix landed without regenerating the tracked cadence_intel.json, so the committed copy (a411e13) still embodies the exact defect the fix comment describes; (3) because the paths are tracked, the …

- **Evidence** — SKILL.md:47 (quoted); `git ls-files arena/results` output listing both JSONs; `git log --oneline -1 -- arena/results/cadence_intel.json` → a411e13 (pre-d3b4a49); `git log -S "gitignored scratch artifacts"` → 064b9ce; git diff ac197ce..e635809 SKILL.md shows the sentence retained through the doc-truth edit.
- **Action** — Pick one and make the sentence true: (a) add both intel JSONs to .gitignore and `git rm --cached` them (my recommendation — the skill already treats them as disposable), or (b) regenerate both post-A15 and commit with a generated_at stamp (the skill itself notes the stamp is missing). Either is a truth/tooling fix allowed under the freeze.


---

## LOW — Regressions in the 2026-08-09 commits

### R4-F36 · F52's end-of-draft guard shipped Python-only: the deck still shows a phantom 'your next: #164+' pick

`KNOWN-PARTIAL — F52` · verdict **CONFIRMED** · *measured*

F52's registered fix (A5) gave hoops.my_next_pick a None return past the owner's last pick, and hoops now prints '— none left, draft complete' (verified). But the deck's myNextPick (docs/draft-deck.html:621-625) is still the unbounded `while (teamOfPick(n, teams) !== slot) n++`, and renderStrip's draftDone() guard (line 2136) only covers picks==156: for the whole tail of the final round after the owner's roster completes, the deck renders 'your next: #164'-class fictional picks (line 2155) and computes a fictional countdown (line 2146). This exceeds F52's registered scope, which named and fixed only hoops.py — and it is a deck=board (A3) parity breach that check_parity cannot see, since my_next_pick is outside the gate's five checks.

- **Evidence** — node repro of the deck's exact functions: {teams:12, size:13, slot:1, picks:150} → myNextPick = 168 (draft ends at 156); {slot:5, picks:153} → 164. Same state in Python HEAD: `draft status` prints 'your next pick: — none left, draft complete'. Guard audit: draft-deck.html:2136 (draftDone early return, fires only at 156 picks), 2146/2155 unguarded calls; F52's text in analysis_2026-08-09_findings_table.md:691-698 cites hoops.py lines only.
- **Action** — Port the guard: myNextPick returns null once n reaches teams*size with no owner slot found, render 'none left' in the strip, and guard the countdown. Optionally extend check_parity with a next-pick fixture over the committed states.

### R4-F37 · test_draft.py certifies the recovery paths it does not test: resync .bak content, empty paste, and short tokens are uncovered

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The 23-case suite (shipped yesterday, 'run before every draft') passes at HEAD while three reproduced defects sit inside its named scope: (a) its F36 resync case (test_draft.py:143-152) checks the rebuild banner and last pick but never inspects .bak content, so the false '.bak holds the prior board' promise is invisible to it; (b) no case feeds resync an empty paste, so silent full-board destruction on empty input passes; (c) its F55 case (154-165) checks only that .bak is loadable, not what it holds. On short tokens the suite DOES cover two-letter nicknames (KD/AD/OG/Zu, lines 79-84), but those resolve via the hardcoded nickname map checked before the length guard; two-letter given names outside the map (CJ/GG/Ja — real pool players) hit the len<3 …

- **Evidence** — Ran the suite at HEAD: 'all 23 cases passed' (exit 0) in the same session in which the resync .bak wipe, empty-paste destruction, and CJ/GG/Ja UNKNOWNs were reproduced against the same binary. Case inventory read from scripts/test_draft.py:63-215: resync case at lines 143-152 asserts 'RESYNC: cleared 2' and '#5 R1: Cade Cunningham' only; F55 case at 154-166 asserts loadability only; no short-token case exists; check_parity.py:57 lists 'aj' among degenerate fixtures.
- **Action** — Add cases: resync then assert .bak equals the pre-resync board pick-for-pick; resync with empty/garbage paste must refuse; 'CJ; GG; Ja' must log three real players; and fix the check_parity 'aj' expectation when finding 3 ships.


---

## LOW — Re-verification of round-3 measurements

### R4-F38 · A17's 'ZERO rows change on today's pool' claim verified on both pools — confirmed accurate

`KNOWN — A17` · verdict **CONFIRMED** · *measured*

A17's "ZERO rows change" claim reproduces exactly: applying pre-A17 (d3b4a49) and post-A17 availability() and weekly_availability() semantics to all 246 rows of data/players.csv and all 220 rows of arena/data/players_2025-10-21.csv changes 0 rows' tiers under either function on either pool. Correction to the finding's detail: data/players.csv carries 25 (not 22) notes with parentheticals; none contains "risk"/"recovery" in the prose portion, and the two structurally divergent tags ("inj-risk;" and "acl-recovery-jan26") land in the same tier via the new code's in-tag fallback checks.

- **Evidence** — Scratch a17_check.py output: 'data/players.csv rows changed: 0' / 'arena/data/players_2025-10-21.csv rows changed: 0'; 'notes containing space/paren: 22' (listed). Old semantics taken verbatim from 'git show d3b4a49:scripts/hoops.py' availability(); new from scripts/hoops.py:331-342 and arena/arena.py:337-347.
- **Action** — None.

### R4-F39 · PARITY: EXACT MATCH covers 5 surfaces; teamWeekModel numerics, market model, and the hoops.py fallback board are outside it

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL (F05/A3, F46, F50). The gate reproduces (EXACT MATCH, 246/2214/39/52) and the 52-turn ordering check genuinely exercises teamWeekModel/lineupWeights/pwins end-to-end — but only the blended branch: the committed states are slots 8-10, so the turn-1 empty-room percentile fallback (the A7/F20 fix) is never executed by the gate at all. Coverage gaps that exceed registration: numeric teamWeekModel (mu/var), lineupWeights maps, marketRanks/MKT_PIN, fitWeights, strategyScores/managerScores and advice/margin display paths are compared nowhere (driver exports only PLAYERS/matchCandidates/decwScores/adjValue/CATS, check_parity.py:81) — a drift there passes unless it flips a Top-5 on 52 specific turns; adjValue is checked for exactly one punt set …

- **Evidence** — Ran scripts/check_parity.py: 'PARITY: EXACT MATCH' with counts matching report §2b verbatim. Ran my scratch orderings_control.py (independent driver, both engines under node): '52 owner turns compared; orderings changed d3b4a49 -> HEAD: 0; top-1 changes: 0'. 'git diff --stat ac197ce..d3b4a49 -- docs/draft-deck.html' is empty. Gap cites: check_parity.py:52-58 (single punt fixture), :185-233 (bespoke _pwins/_pct reference); grep 'decw' scripts/hoops.py returns nothing; deck app path verified …
- **Action** — September: extend the gate to assert numeric equality on teamWeekModel (mu,var) and lineupWeights over the committed rosters plus 2-3 more punt sets (cheap — the harness already runs node), and add one line to SKILL.md's live-draft protocol stating explicitly that the hoops fallback board is a DIFFERENT ordering (adj-value-based) than the deck card, so a mid-draft fallback is a known instrument change, not a silent …

### R4-F40 · Round-3's corroborating bench numbers (0.971/0.998 and 0.852) come from uncommitted /tmp harnesses

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Round-3 quotes two corroboration figures with uncommitted provenance, violating the existing lesson-13 law ('no shipped number is quotable unless a fresh clone plus one committed command regenerates it'): §1a's verifier figures 0.998/0.971→0.973 have no surviving harness anywhere and are unregenerable; F23's 0.887/0.851/0.817→0.852 regenerates exactly today but only from uncommitted /tmp/bench_sim2.py, which lesson 3 says will die with the session. The figures also conflate definitions — 0.852 is a raw ranks-11-13 start-share while 0.956/0.973 are relative weights, and the true undiagnosed generator gap is raw 0.953 (committed bench_share_fit.py) vs 0.852 (bench_sim2), ~10 points, not a denominator difference (bench_sim2 divides by own game days, …

- **Evidence** — arena/results/analysis_2026-08-09_self_critique_round3.md:57-58 ('An independent verifier ... got 0.998 / 0.971 -> 0.973'); analysis_2026-08-09_findings_table.md F23 evidence ('/tmp/bench_sim2.py: start-share by roster rank #11 0.887, #12 0.851, #13 0.817'; action row: 'the /tmp harness is 60 lines'). Repo grep confirms no committed script reproduces 0.971 or 0.852. My sweep (this session): plausible variants span 0.930 (pace 3.5) to 0.968 (shared-team + absences).
- **Action** — Either strike the uncommitted figures from the round-3 record with a dated correction note, or commit a regenerator for them; make 'no number enters a results doc from an uncommitted harness' an explicit lesson (it is currently only implied by lesson 13's mock-state framing).


---

## LOW — Skill / protocol coherence

### R4-F41 · SKILL claims the arena intel JSONs are 'gitignored scratch artifacts' — both are git-tracked; priming dirties committed evidence

`REGRESSION — F58 (frozen-pool/timestamp scope only)` · verdict **PARTIALLY_CONFIRMED** · *measured*

KNOWN-PARTIAL F58 (incomplete fix, not new): F58 already registered that SKILL.md's 'gitignored scratch artifacts' statement is false (both intel JSONs are git-tracked; .gitignore cites lesson 13) and its action said to fix that claim. What exceeds the registered scope: yesterday's doc-truth rewrite (25f41bc) edited this exact sentence — correcting ~10min to ~76s, deleting the unexecutable skip rule, adding the F58 frozen-pool caveat — yet retained the F58-flagged falsehood and the regenerate directive, so F58 remains open on its own sentence after its fix pass. Reproduced consequence: executing the checklist's cadence command mutates committed cadence_intel.json (869-line diff, deterministic — the committed file predates the A15 mkt fix per …

- **Evidence** — Ran both commands this session from the checklist verbatim; git status showed 'M arena/results/cadence_intel.json' (restored via git checkout -- afterward; tree left clean); git ls-files arena/results/ lists both intel JSONs; .gitignore lines: 'results JSONs are committed evidence per LESSONS.md lesson 13'; git log -S 'gitignored' → d3b4a49. F58's registered scope was the frozen-pool caveat and the missing generated_at stamp (which I confirmed: neither file carries one), not the tracking claim.
- **Action** — Either gitignore the two intel JSONs (they are regenerated scratch by doctrine) or reword to 'tracked but regenerate-and-discard' with an explicit git-restore step; update ~76s to ~100s or re-measure.
- **Owner question** — Should regenerated intel JSONs ever be committed, or are the checked-in copies frozen evidence?


---

## Refuted on verification — do not re-raise

- **[skill] arena live's pause message tells the session to run `draft turn ""` without --expect, contradicting the …** — Reproduced both anchors: arena/arena.py:537-539 prints the pause banner commands without --expect, and SKILL.md:48's arena carve-out mandates --expect on both calls. But the status claim is wrong: this is registered finding F64(b) in arena/results/analysis_2026-08-09_findings_table.md (lines 812-819), which quotes the identical banner text, names the identical SKILL …


## Coverage notes (what each auditor did and could not do)

- **regression** — Examined and personally reproduced against: the full ac197ce..e635809 diff for scripts/, arena/arena.py, docs/draft-deck.html, .claude/; a 1,550-query match-corpus A/B between ac197ce and HEAD (both clones, same pool); availability/weekly_availability old-vs-new on BOTH data/players.csv and the frozen arena/data/players_2025-10-21.csv — ZERO rows change on either file, so E24/ledger comparability survives A17 (verified clean, not a finding); …
- **reverify** — Reproduced in this session (all solid, no finding filed): (1) bench_share_fit.py -> 0.997/0.953/0.956 exactly; (2) bench_weight_study Phase 1 lesson-13 integrity 4/4 EXACT at committed seeds/N (6.16/4.11/11.37/9.52); (3) Phase 2 --quick (N=1500x3) deltas +7.91/+1.84/+1.73/+6.49 — direction 4/4 and magnitudes consistent with the report's N=6000 values within MC error; (4) both committed JSONs (seeds 11/23/47 and 101/202/303) match every number in …
- **domain2** — Examined and reproduced in-session (repo untouched, all scripts in the session scratchpad): (1) a fresh CRN-paired G1a replication at BENCH_WEIGHT 0.15 vs 0.956 — 216 draft+sim runs, seeds 107/211/331, 500 seasons/cell (scratchpad/g1a_bw.py + g1a_bw_out.json); (2) MKT_W graded and split-half cross-validated against the real 2025-26 board (148/156 picks matched); (3) playoff-week games sensitivity through a parameterized team_week_model at 60k …
- **skill** — Examined line-by-line: .claude/skills/fantasy-basketball/SKILL.md (all 87 lines), .claude/skills/draft-arena/SKILL.md, evals/evals.json; hoops.py draft-loop code (turn card, status, resync, freshness gate, adj_value/fmt_row), check_parity.py header/structure, and yesterday's commits (8bd32e1, e944015, 1cc113e, 25f41bc) via git show. Ran mechanically in scratch: a punted scratch draft (init/turn/status/resync), a full arena live session at slot 5 …
- **deck** — Examined: full git diff ac197ce..e635809 of docs/draft-deck.html plus per-commit deck diffs (8bd32e1, e944015, 1cc113e, 25f41bc); executed BOTH revisions' deck engines (extracted data+engine scripts) under node to measure matching, weeklyAvail tiering over every baked note, and empty-board decwScores; simulated the complete refresh/build gate sequence on a /tmp scratch copy (repo untouched — git status clean), observing every refusal message in …
- **october** — Examined and personally reproduced: live Routine/trigger inventory via list_triggers (2 pages, 120 entries — both named Routines found with full prompts and tool lists; remaining unpaged entries are older ended send_later one-shots, so a third undiscovered draft-related Routine is unlikely but not strictly excluded); full ac197ce..e635809 diffs for hoops.py, arena/arena.py, docs/draft-deck.html, SKILL.md; before/after rank --top 200 diff …
