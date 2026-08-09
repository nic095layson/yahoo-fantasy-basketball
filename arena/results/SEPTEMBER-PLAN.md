# September recalibration plan — pre-registered 2026-07-31, owner-authorized

**Standing state until this plan executes:** FEATURE FREEZE. No engine or
judgment-layer changes ship before the September run. Allowed meanwhile:
display-only fixes, truth/reporting fixes, and anything the owner asks
for explicitly. Measure-only studies are always allowed.

**Authorization.** On 2026-07-31 the owner asked that the September work
happen systematically, without a prompt from him. A one-shot scheduled
Routine fires on **2026-09-01** and executes this file top to bottom in a
fresh session. This file is the single source of truth for that run —
the firing prompt carries authorization, the ship rule, and
delivery pointers but no experiment content, and states that where it and
this file disagree, this file wins (prompt/file reconciled 2026-08-04).

**Ship rule (the honest contract).** "Systematically installed" means
systematically *executed*. Each item below carries a pre-registered
acceptance bar. Data recalibrations ship when the build gates pass.
Engine/judgment changes ship **only if they beat the incumbent on the
arena instrument without regressing the winners** (mocks 21/24/25/26 as
replay baselines). Anything that fails its bar stays out and gets a
written negative result. This is the same standard that kept the
computational layer defect-free through two full audits — it does not
relax because the calendar turned.

**Bar-registry law (added 2026-08-04, from the independent system review
and LESSONS.md lesson 14):** the ship bars in this file are append-only. A
re-scope adds a dated line beside the original wording — it never edits
the registered text (the E18 ship commit edited its own bar in place; that
hole is closed). Two re-scopes of the same bar = the bar failed: write the
negative result and stop. A dropped or deferred pre-registered check is
disclosed in the ship note itself.

## 0. Read first (context recovery for the fresh session)

**`arena/results/league_intel_2025-26.md` — the owner's REAL league ground
truth (settings, standings, weekly data, draft board, room model). It
supersedes any assumption it contradicts and feeds E14–E17.** Then
**`arena/results/analysis_2026-08-09_self_critique_round3.md` and its companion
`analysis_2026-08-09_findings_table.md` (66 verified findings, F01–F66) and
`report_2026-08-09_bench_regrade_and_integrity.md` — the round-3 audit. It
re-scopes E22, adds §7 below, and several of its findings change what the items
already in this file mean.** Then
`LESSONS.md` (all lessons; data-pull countermeasures are lessons 8–10),
`REVERT-MAP.md` (kill switches), `arena/results/LEDGER.md` (derived
tallies + the no-remembered-tallies rule), the two 2026-07-31 audits,
`arena/results/findings_2026-07-31_tunnel_vision.md`, and the mock
debriefs for 22/23/24/25/26, and the 2026-08-03 debriefs for mocks 27
and 28 (they motivate E8/E9/E10 and LEDGER §5).

## 1. Data refresh (precondition for everything)

1. Fresh player-pool pull with per-player roster verification
   (`scripts/verify_rosters.py`, mechanical NBA/ESPN check) and a
   same-day freshness stamp (`docs/freshness.json`).
2. **September consensus ADP** replaces the July market board
   (`PRE_RANK` / `MKT_RANK` sources in the data block). This is the
   event the freeze was waiting for.
2b. **Projection synthesis (owner directive 2026-08-04, Q14):** the owner
   uploads multiple third-party ranking/projection datasets in September.
   Synthesize them into the tool's OWN projection set — cross-source
   blending, injury adjustments, rookie scaling, independent analysis —
   rather than adopting any single source. This synthesized set becomes
   `data/players.csv` for the October draft build. Document per-player
   provenance for anything that deviates >15 ranks from consensus.
3. Rebuild via `scripts/build_deck.py` — all fail-closed gates must
   pass; JS↔Python parity must print `PARITY: EXACT MATCH`.
4. Re-baseline the arena on the fresh pool before any experiment runs
   (all July numbers are stale the moment the pool changes).

## 2. Experiment queue (pre-registered bars)

| # | Experiment | Origin | Ship bar |
|---|---|---|---|
| E1 | Empty-roster gradient across outlier profiles (r=0 anchor pick) | LEDGER §4: Wemby −14.1/−7.5pp, Luka +6.3pp | Any gradient change must improve ≥2 distinct outlier-anchor profiles by >1pp AND not regress conventional anchors (Luka-class) beyond −1pp |
| E2 | Quiet-chip survival + punt-mode chip recalibration on September ADP | m22: punt-mode BUY NOW gone-rate 54% vs 83–91% normal; quiet-survival optimistic | Replay calibration across ledger mocks: normal-mode BUY NOW gone-rate stays ≥80%; wheel-seat pair-boundary precision not below 17/17 (slot 12) and 15/17 (slot 1); punt-mode caveat replaced by measured curve |
| E3 | PCT_MIX_INFL re-estimate | registered 07-30 | Data-driven refresh; gates + parity only |
| E4 | Bundle-lookahead probe (2-pick joint scoring at reach turns) | findings_2026-07-31_tunnel_vision.md §mechanism-2; m26 bundle beat card by 5.76pp | Measure first. Ship only if it proposes m26-style bundles AND always-rank-1 replay results do not degrade on any winner |
| E5 | Earlier structural-drift sensitivity (latch currently fires ~2 rounds after cheapest repair) | findings file; m23 latch at #61 vs repair at #37 | Must keep **0 false positives** on all winning drafts (current bar); any earlier trigger that breaks this stays out |
| E6 | Slot-3 refinement + k-scheduling (GRAD_K) | registered 07-30/31 | Beat incumbent across gradient-seat replays (m24/m25/m26) beyond ±1pp; no regression elsewhere |
| E7 | `ar/fx/sy` (7.8KB) + `gradImpact` use-or-drop checkpoint | REVERT-MAP, owner instruction | If no shipped feature consumes them after E1–E6 and E8–E10 land, remove them (REVERT-MAP has the procedure) |
| E8 | Replace/augment "board rank" (kept-total) with **expected categories won per week** in debriefs + LEDGER; re-derive every retained mock | m27: corr +0.931 vs +0.828 (n=12). **m28 (controlled): kept-total correlates −0.293 *within* a room; a kept-total-maximizing oracle finished 11th while an ECW-maximizing oracle with identical hindsight finished 1st at 34.58%** (LEDGER §5) | Reporting-layer only — no engine change. Ship if the re-derivation reproduces every retained artifact and the new column explains m27 (board 1st, finish 4–7) |
| E9 | Test expected-cats-won as a **draft-time** signal (marginal Δ-cats-won per candidate **under a survival model**, not foresight). ~~extend the gradient gate past slot 3~~ — **REMOVED 2026-08-03, measured and rejected** (`findings_2026-08-03_gradient_gate.md`: widening the gate lost in 2 of 3 rooms) | m27 (slot 4) and m28 (slot 5) both sit outside the gradient gate and both produced the surplus-in-won-cats pathology. m28's controlled oracle pair shows the objective — not the hindsight — drives the 28pp gap (LEDGER §5). Honest prior: a realizable version captures far less than 28pp | Must beat the incumbent across ledger replays **without regressing m21/m24/m25/m26**. Measure first; ship only on a clean win |
| E10 | "Quiet zone" escalation: builds that are neither healthy nor drift-latched | m27 and m28 both finished mid-table with the drift latch correctly silent (each had <3 dead kept cats or ≥2 C-eligible). Nothing on the card marks this zone | Must preserve the latch's **0 false positives** on m21/m24/m25/m26; measure before proposing any UI |

| E20 | **Punt-box truth (owner-reported 2026-08-04, mock 34 slot 8).** The shipped `ds` ordering is punt-blind: `decwScores` uses `adjValue(p, new Set())` and `pwinsTotal` over all 9 cats. Control-measured: Top-5 byte-identical 26/26 with the punt declared vs cleared — `state.punt` reaches only display metadata. A punt-aware blend changes #1 at 21/26 turns (mean shipped rank of the punt-aware #1 = 11.73, max 40). Mock 22 is the visible case: punt = REB/BLK/FG%, shipped #1 was a center at 8/13, punt-aware at 0/13 | `debrief_2026-08-04_mock34_slot8.md`. NOTE the counterweight: the punt-blind VALUE half is the documented regularizer against round-1's concession spiral (`findings_2026-08-04_decw_round1.md`) and punt-DECLARING measured −5 to −11pp (G1a). The 9-cat `pwinsTotal` half has no documented rationale | Measure both cards on EVERY punted draft in the ledger — mock 22, mock 31 (slot 9), mock 32 (slot 10), mock 34 (slot 8) — under the season-sim harness BEFORE any ordering change. A punt-aware ordering ships only if it beats the incumbent on the punted mocks without regressing m21/m24/m25/m26. If it does not ship, the UI must stop implying the punt box affects recommendations (display-only truth fix, allowed under the freeze) |
| E21 | **Punted-draft screening becomes mandatory** for any future Top-5 ordering change | E9's 14-mock panel spanned mocks 16–21 and 23–30 — **mock 22, the only punted mock in existence AT THAT TIME, is the one number skipped in that range** (mocks 31/32/33 all postdate the ship), and `findings_2026-08-04_decw_round2.md` contains zero occurrences of "punt". That is how the punt box became inert without any gate firing | Process rule, not an experiment: no ordering change is quotable or shippable without per-turn results on every punted mock in the ledger |
| E22 | **Positional-saturation term in `decwScores`** — it currently has none (confirmed: never calls `benchBound`; relabelling every center to PG leaves ECW bit-identical at 4.041857269). Measured amplifier: ablating the candidate bench discount at mock-34 round 13 moves the Top-5 from 5/5 C-eligible to 2/5, so `BENCH_WEIGHT` inside `teamWeekModel` drives the late-round all-big card | mock 34: 6 C-eligible of 13; AST fell to a kept-cat win probability of 0.202, clustered with the punted cats — an undeclared 4th punt | Measure first. Any term must not regress m21/m24/m25/m26 and must be screened on the punted mocks per E21 |
| E23 | **Punt-implication warning (display-only).** **Scope addendum 2026-08-05 (3PTM integrity defense, Council 5-0, `integrity_2026-08-05_3ptm_rank_defense.md`):** category rank chips gain (a) gap-to-pack context ("10th, −1.3/g to 4th" — bare ranks on compressed distributions read as holes) and (b) a per-category boost/drag readout (+6.93/−6.64 answered the owner's 3PTM challenge at a glance) with a stars-vs-breadth composition warning.  Must also cover the INVERTED-punt case measured in mock 32 (declared punt conceded a rank-3 strength and kept a rank-11 weakness; inverting it was worth +6.5z) — At declaration time, state what the punt set leaves: which categories remain, which archetype they imply, and which kept cat is most at risk of dying with them | Owner declared FT%+3PTM+PTS and was surprised the card proposed only centers; the existing warning cites the G1a cost but never the positional consequence | Display-only; no engine change. Ships when the wording is checked against the punted mocks |

## 3. Validation before anything merges

Parity EXACT; build gates; the 130-state render gauntlet + mutation
suite (harness described in `audit_2026-07-31b_deck_integrity.md`);
replay of ledger mocks as regression fixtures; `LEDGER.md` updated per
its standing rule — plus the audit's grep sweep for unbacked derived
claims in any new prose.

## 4. Delivery

Branch `claude/2026-09-01-september-recal` off the default branch — and
verify first that the branched tree contains `docs/draft-deck.html` and
this file; if either is absent, the default branch is stale (unmerged
work) — stop, fetch `claude/2026-07-27-data-pull-kxzden`, and report
before proceeding. Draft PR; subscribe to PR activity. Rebuild and **republish the deck artifact
to the existing URL** (https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0
— pass it as `url`; republish is part of the definition of done).
Report to the owner: per-experiment verdict table (shipped / rejected,
with numbers), what changed in the deck, and anything genuinely
requiring his judgment.

## 5. Added 2026-08-03 (from mocks 27–29 and an owner-reported defect)

| # | Experiment | Origin | Ship bar |
|---|---|---|---|
| E11 | Any future card-vs-card counterfactual must carry a **perturbation-matched placebo arm** (N random legal swaps) and report per-arm field-strength delta | Gradient-gate verifiers showed arms differing in swap count, reach distance, and z removed from rivals — "better card" was confounded with "more disturbance" | Methodological requirement, not an experiment: no card-comparison result is quotable without it |
| E12 | TARGET family-need gate — **Option A (BOARD LEAN relabel) SHIPPED 2026-08-04**; this item is now Option B only (suppress the family when covered) | `findings_2026-08-03_target_family_defect.md`: 12 of 32 TARGET lines across mocks 27–29 name a family already at/above its startable floor with no open lineup slot | Must not silence any TARGET line that was load-bearing (m22 Markkanen structural transfer, m23 repair pleas); re-run the 130-state gauntlet and ledger replays |

**Superseded within the plan:** the "extend the gradient gate past slot 3"
half of E9 is closed as a measured negative result. Do not re-open it without
new evidence of a different kind.
| E13 | ~~Quiet-chip suppression or recalibration~~ — **SHIPPED 2026-08-04** (`after_2026-08-04_fixes_recalibration.md`): room-mix survival blend (9 value + 2 market seats), thresholds re-fit; quiet survival 58%→89%, BUY precision 94% look-through / 82% conservative, wheel bars exceeded | was: quiet 50→37→22→0% across m27–30 | Bar was met before shipping. September E2 narrows to the punt-mode curve + ADP re-fit of the market weight |

**Priority note resolved 2026-08-04:** both owner-visible defects (E13 quiet
chip, E12 TARGET label) were fixed, calibrated, validated, and shipped on
owner instruction — see `after_2026-08-04_fixes_recalibration.md`.
| E14 | **Adopt the real playoff format** in the arena (8 of 12, NO byes, **three 1-week rounds, weeks 19–21 — spec completed by owner Q2**) at the re-baseline | league_intel §9; measured deltas −4 to −6pp champ for elite rosters (`arena/mocks/format_delta.py`) | Instrument change at re-baseline only; dual-report one mock both formats for continuity |
| E15 | ~~IL+ stash revaluation~~ **CLOSED 2026-08-04 by owner rule (Q6): drafts target active roster + bench only, never IL+ stashes.** The recovery-exclusion rule stands as shipped | league_intel §9 | No work |
| E16 | Streaming gap: real league runs 27–83 moves/team vs arena's zero — now known to be **daily lineups, unlimited moves, daily FFA waivers with game-time locks (Q3–Q5)** | league_intel §9 | At minimum, report champ% as a no-streaming bound and tilt bench value toward flexibility; full streaming model is a scope decision, not a default |
| E17 | Refit the arena room (`MOCK_CAST`) + survival blend to the MEASURED reach profiles of the 11 returning managers | league_intel §5: 8–9 of 11 opponents reach past value early — the real room is market/name-shaped, not value-bot-shaped | Chip calibration must be re-run on the refit room; BUY NOW ≥80% precision bar unchanged. The deck side shipped 2026-08-04 (E18a); this item now covers the ARENA cast + survival refit to the same profiles |
| E19 | **Returnee repricing wave (owner directive 2026-08-04):** per-returnee camp verification (minutes restrictions, preseason usage, beat reports) → re-tag notes (clear / keep 0.78 / deepen); evaluate an age-conditioned Achilles tier in the arena (36yo Lillard ≠ 26yo Haliburton at a flat 0.78) before any engine change | `report_2026-08-04_injury_returnees.md`: five named returnees priced at last-healthy 24-25 rates ×0.78; Haliburton ranks ~top-12 by value even after the haircut — right if fully ramped, overpriced if capped | Any tier change validates in the arena first (feature freeze); October ADP sync adds per-returnee EDGE (our rank vs market) to the card |
| E18 | **Named manager profiles (owner directive 2026-08-04):** (a) ~~deck MOCK mode fields the 11 real managers~~ **SHIPPED 2026-08-04** (`findings_2026-08-04_e18_named_room.md`): MANAGERS + managerScores in the engine, per-draft seat shuffle stored on state, Robby adp_w refit 0.55→0.7; smoke 5/5 slots, owner-card parity 7/7 byte-identical, scaled reach band pass, Spearman 0.952 — **noise model corrected same day (E18b, owner-reported: log-normal rank noise, proportional availability, Noah manual refit per owner correction, Kyle refit; `findings_2026-08-04_e18b_noise_model.md`)**; (b) LIVE mode with named seats replaces the generic room-mix survival with **per-seat pick projection**: P(manager m takes player p before my next turn), chained across the actual managers sitting between my picks, feeding BUY NOW/quiet and a pre-draft per-round target sheet per rival — still open for September | Three-season boards + complete identity map (league_intel §12); profiles.json committed 2026-08-04 | **Absolute ±8 reach bar re-arms at the October real-ADP sync** — the synthetic market carries only ~0.45 of real Yahoo's divergence from the value board (Noah anchors the scale), so until real ADP replaces the proxy geometry the binding bar is the Noah-anchored scaled band (passed 11/11). Survival: BUY NOW precision ≥80% maintained; October brief consumes the projection sheet |
| E9b | **Single regularized draft objective (registered 2026-08-04, owner-authorized via the independent system review; N4 disposition — measure-only):** move blend50's regularization *inside* the objective (concession floor on per-category marginal weight, or a concave per-category utility) and retire the two-proxy percentile mix | `analysis_2026-08-04_self_critique_round2.md` N4 (α=0.5 knife-edge: 0.4 craters m29, 0.6 regresses m25); `findings_2026-08-04_decw_round1.md` (concession spiral); the review's finding that raw ΔECW is not a coherent utility | Measure-only until it beats blend50 on the full ledger + fresh seeds with **zero winner regressions** AND stays clean under **±0.1 perturbation of its own hyperparameters** (the robustness property blend50 lacks); runs on the E14 real bracket, and on the refit weekly model if the weekly-record refit has landed; must include held-out states beyond the 14-mock tuning panel |


## 6. October final refresh (executed by the October Routine, ~2026-10-12)

The October Routine executes THIS section in a fresh session. Same branch
guard as §4: branch `claude/2026-10-12-october-refresh` off the default
branch, verify the tree contains `docs/draft-deck.html` and this file
(if absent: stop, fetch the newest `claude/*` branch, report).

1. **Fresh pool pull** with per-player roster verification
   (`scripts/verify_rosters.py`) and a same-day `data/freshness.json`
   stamp — opening-night rosters, late cuts, camp injuries.
2. **Real October ADP replaces all synthetic market geometry** in
   `PRE_RANK` / `MKT_RANK`. This gate is artifact-bound: the build must
   FAIL, not warn, if the market source is still the synthetic proxy
   after real ADP has published (the ~0.45× divergence measurement is the
   reason — see E18's bar and the 2026-08-04 system review N2).
3. **Re-arm and grade the E18 absolute ±8 reach bar** on the real-ADP
   room, exactly as originally registered (LESSONS.md lesson 14: the
   original wording binds; a second re-scope = the bar failed).
4. **Per-returnee EDGE columns** (our rank vs market) land on the card
   per E19; re-verify each returnee's camp status the same day.
5. Rebuild via `scripts/build_deck.py` (all gates + parity), **republish
   the deck artifact to the existing URL**
   (https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0,
   passed as `url`), confirm the page header reads fresh-today.
6. Sync the same window's news to `fantasy-basketball-2026-27` per its
   DATA-PULL.md (both planes, one window), and report to the owner:
   what moved on the board, which bars passed/failed, and the per-rival
   target sheet if E18(b) shipped.

## 7. Added 2026-08-09 — round-3 audit registrations (APPEND-ONLY, lesson 14)

Source: `analysis_2026-08-09_self_critique_round3.md` (66 verified findings) and
`report_2026-08-09_bench_regrade_and_integrity.md` (the measured study). No bar
above is edited; re-scopes are dated rows beside the original wording.

### 7.1 E22 — RE-SCOPE (original wording in §2 stands untouched)

**Registered 2026-08-09.** E22 asks for a positional-saturation term in
`decwScores`, on the premise that the bench discount is right and
under-applied. The audit measured the opposite premise. Under the owner's
DAILY-lineup format a 13-man roster has ~6.5 players with a game on a typical
day against 10 startable slots, so positional saturation costs **0.5–3% of
games**, not 85%. `BENCH_WEIGHT = 0.15` is ~6.4× too low
(`arena/mocks/bench_share_fit.py`: ranks 11–13 start 0.953 of their own games,
ranks 1–10 start 0.997).

**Pre-registered prediction, dated 2026-08-09, before the measurement:** a
positional-saturation term will NOT clear its bar, because the effect it is
built to capture is near zero in this format. **Order of work is therefore
reversed: fix the bench weight first (7.2), then re-run E22's motivating
measurement on the corrected instrument. Do not build the term first.**
If the corrected measurement still shows the late-round all-big card, the cause
is elsewhere and E22 needs a new mechanism, not a new constant.

### 7.2 E24 (NEW) — bench-weight correction, at the E14 re-baseline

| Item | Detail |
|---|---|
| Change | `BENCH_WEIGHT` 0.15 → a measured start-share (0.956 flat, or the per-rank curve from `bench_share_fit.py`), applied identically in `arena.lineup_weights`, the deck's `lineupWeights`, and the ADP bot's −50 bench-bound penalty |
| Measured effect | Owner champ% rises in 4/4 reproducible mocks: m31 +7.01, m32 +2.08, m33 +1.17, m34 +5.96 (18,000 seasons/arm, rosters fixed). 5–8 of 12 seats reorder per mock — not a common-mode rescale |
| Replication | Unseen seeds 101/202/303: direction 4/4; magnitude within 0.63/0.31/0.12pp on m31/m32/m34; **m33 halves (+1.17 → +0.48)** |
| Mechanism | **UNEXPLAINED.** Two hypotheses tested and refuted: "owner's bench is stronger" (corr −0.515, wrong sign) and "variance compression favours strong rosters" (corr +0.206 across 48 team-observations, wrong sign; top-3 ECW rosters lose) |
| Ship bar | Runs at the E14 re-baseline ONLY, dual-reported old-vs-new exactly as `league_intel §4` dual-reported the bracket. Must not regress m21/m24/m25/m26 once their states exist (see 7.5). A mechanism must be identified before it ships — a large consistent effect nobody can explain is not a finding, it is a lead |
| Do NOT | ship it standalone, or hand-tune the constant upward. It re-grades every historical champ% at once; every number in `LEDGER.md` is conditional on it |

### 7.3 E25 (NEW) — close N1 with the data already in the repo

`arena/data/weekly_matchups_2025-26.csv` — the owner's real per-category weekly
totals, 45 rows including the champion's playoff run — is read by **zero lines
of code**. N1 has been called the deepest remaining weakness since 2026-08-04
while its closing data sat committed and unused.

First measurement against it (audit F10/F21/F50): FG% is well calibrated
(implied inflation 1.08–1.11 vs `PCT_MIX_INFL = 1.15`, χ² p≈0.40); FT% is
directionally lower (0.86–0.94) but does **not** reject at the owner's attempt
volume (p = 0.077–0.106, n=16–18); counting-cat dispersion is light by
~1.1–1.65× in 3 of 7 categories once week 17 (All-Star double week) and week 8
(21-game short week) are excluded.

**Fit games BEFORE the CV constants** — roughly half the missing variance is
the constant `3.5` games-per-week assumption, not per-game noise.

**Ship bar:** E25 is a PRECONDITION of E9b, not a parallel workstream. E9b's
registered bar already says "runs on the refit weekly model if the weekly-record
refit has landed"; this makes the refit the gating item. Carry the bound: n=16–18
team-weeks from one team, enough to move a hand-set constant, not enough to fit
nine of them well.

### 7.4 Pre-registered hypothesis (dated 2026-08-09) — punt interaction

Across both seed sets, the three **punted** mocks average **+4.7pp** under the
bench correction and the single **unpunted** mock **+0.8pp** (n=3 vs 1). The
only mock whose magnitude failed to replicate (m33, +1.17 → +0.48) is the
unpunted one.

**Hypothesis, registered before the test exists:** the bench-weight correction
matters chiefly in punt builds, where a roster deliberately concedes categories
and the last three spots carry more of what remains. Test it on the wider panel
at the re-baseline. n=3 vs 1 today — a hypothesis, not a finding.

### 7.5 Process corrections to items already in this file

- **§3's `PARITY: EXACT MATCH` gate now exists.** `scripts/check_parity.py`
  (added 2026-08-09) compares the deck's engine against the Python engine on
  246 pool rows, 2,214 z cells, 39 name fixtures and 52 card orderings across
  every committed mock state. Until today this file gated on a script that did
  not exist (F46/F60). The "130-state render gauntlet + mutation suite" §3 also
  cites still exists only as prose in an audit document — either build it or
  strike the reference.
- **§4/§6 republish is now checkable.** After republishing, WebFetch the
  artifact URL and assert the returned build-manifest `built` date equals today;
  paste that assertion into the owner report. "Republish" was the definition of
  done with nothing verifying it (F56).
- **Backfill.** Lesson 13 says mock-state backfill is "queued for the September
  run"; this file contained zero occurrences of "backfill" (F34). It is queued
  HERE, now: the unreproducible boundary runs **past** mock 26 —
  `season_sim_mock27|28.py`, `mock28_cf.py:17` and `format_delta.py:23-27` all
  read the vanished uploads path, which places **LEDGER §5** (sole cited basis
  for E8 and E9) and **all four `format_delta` states** (entire measured basis
  for E14) inside the unreproducible set while both are quoted as
  artifact-derived. Either the states are recovered, or every dependent claim is
  marked [UNREPRODUCIBLE] and the E8/E9/E9b bars are rewritten against mocks
  31–34, the only states that exist.
- **Schema widening is a September-only window (F24/F41).** `gp` (projected
  games), `min`, `age`, `adp` and an uncertainty column must land in the Q14
  multi-source synthesis, before the pool freezes. `gp` is the input both the
  weekly model (7.3) and any real availability model need; it cannot be
  retrofitted after October.

## 8. Added 2026-08-10 — round-4 registrations (APPEND-ONLY, lesson 14)

Source: `analysis_2026-08-10_self_critique_round4.md` (41 verified findings,
R4-F01…R4-F41) and the owner's same-day rulings. No bar above is edited.

### 8.1 E24 amendment — the mechanism is found; the re-baseline design changes

**Registered 2026-08-10 (R4-F07).** `TEAM_WEEK_SHOCK`'s sd scales linearly with
the lineup weight while `team_week_model` base noise scales as √w — a channel
ECW is structurally blind to (`pwins_total` uses base variance only). Measured
at 2000×3 seeds: m33's gain decomposes +1.62 shock-on → **+0.42 shock-off**
(~74% artifact — and the artifact component is exactly what failed fresh-seed
replication); the three punted mocks move the OPPOSITE way (m31 +7.28→+8.58,
m32 +1.70→+2.37, m34 +6.53→+7.27). Shock-off, §7.4's punt gap **widens**:
punted average +6.1pp vs unpunted +0.4pp.

E24's bar therefore gains: **(a)** the re-baseline re-grade runs shock-on AND
shock-off arms so the mean-level effect is separated from the shock artifact;
**(b)** §7.4's punt hypothesis is graded on the shock-off arm — pre-registered
prediction, dated 2026-08-10, before the wider panel exists: *the punted-vs-
unpunted gap widens with shock off*; **(c)** wherever ECW is displayed beside
champ%, the display must state that ECW excludes TEAM_WEEK_SHOCK; **(d)** the
0.956 constant is quoted as a **0.940–0.968 band** (teammate schedule
correlation −0.016; teammate absences +0.028 — R4-F25), and the re-baseline
fit uses team-shared schedules via `p["team"]` (≈6-line harness change);
**(e)** mechanism experiments M1 (channel ablation: {0.15, 0.956}³ over
μ/var/%-attempt-pools, CRN, mocks 31–34), M2 (closed-form per-category
win-prob decomposition — run FIRST, it is cheap), M3 (variance-only vs
mean-only tiebreaker) are the September queue, M2's prediction pre-registered
before any of them runs. The %-attempt-pool channel (fg_at/ft_at scale with w,
moving both the %-mix mean AND the binomial variance floor) is a live
candidate for the punt interaction since all three punted study mocks punt a
% category.

### 8.2 E17/E18 amendment — measured market-model prior (R4-F04)

Graded against the real 2025-26 board (146–148/156 picks matched): Spearman
≈0.81, MAE ≈22 picks — but the miss is systematically positional: C-eligible
players go a mean **21.7 picks earlier in rounds 1–5** than `MKT_W` predicts
(Allen #37 vs #107, Duren #46 vs #109, Ayton #49 vs #108); guards ~7.5 picks
later. Split-half CV refit: both folds raise FG% (0.5 → 1.2–1.4) and cut TO
(0.25 → 0.0–0.4); REB/FT% directions are fold-dependent — not settled. The
September refit calibrates on the owner's three boards with this CV procedure,
not national-ADP intuition, and re-runs chip calibration per E17's bar. The
deck's survival chips inherit the ~2-round center optimism until then.

### 8.3 E23 amendment + owner punt ruling (2026-08-10)

Corrected-instrument punt-declaring cost: **−3.09pp** (1-cat, t=−3.93) to
**−6.43pp** (2-cat, t=−8.55), CRN-paired, n=36 cells at 500 seasons/cell on
the shipped 6-team bracket — ~26–31% attenuated from the −5 to −11pp the deck
quotes in four places. E23's wording quotes both ranges with their
instruments. Full-scale re-run (2000 seasons/cell, real bracket) precedes any
E20 punt-aware-ordering decision.

**Owner ruling (supersedes E23's declaration-time framing for this owner):**
he will not declare punts — *"I only wait until the system calculates this and
directs to full tilt when clear dominance over opponent rosters."* The
operative surface is concession DETECTION and full-tilt direction (SKILL.md
Analysis rules, "Full-tilt doctrine"), not declaration warnings. E23's
display work re-scopes to sharpening the detect-and-direct path: the Soft
Punt panel, the drift latch, and the card's dead-category signal.

### 8.4 Q3 disposition (owner delegated 2026-08-10) and Q4 deadline

**Q3:** mock 10–30 draft states are treated as LOST. LEDGER §5 (the m28
oracle pair) and the four `format_delta` states are marked [UNREPRODUCIBLE];
the September session rewrites the E8/E9/E9b regression bars against the
committed states (mocks 31–34 and anything newer) BEFORE running those
experiments, and the LEDGER gains a one-line header noting which rows are
historical record vs re-derivable evidence.

**Q4 (projection source): still TBD as of 2026-08-10.** Hard deadline
2026-09-01: if unanswered when the Routine fires, the September session must
NOT pick an anchor source itself (a domain judgment the owner reserved) —
it proceeds with the schema widening (§7.5) on the existing pool, marks the
synthesis blocked-on-owner, and says so in its report.

### 8.5 A19/A20 mechanization (R4-F16/17)

Before 2026-09-01, from a session that demonstrably holds the Artifact tool:
publish a no-op redeploy of the standing artifact URL to prove the grant
survives into fired sessions, or delete+recreate both Routines from such a
session. §6 gains a final step: *before closing, the October session creates
a one-shot draft-eve Routine (T-1) that executes §6 steps 1 and 5 only (pool
pull → verify → stamp → build → republish → WebFetch built-date assert)* —
the existing self-reschedule clause is inert by construction (any plausible
draft date sits within its ~10-day threshold of Oct 12). Fallback wording if
the Artifact tool is unavailable at republish time: STOP, SendUserFile the
built deck, tell the owner the page is stale. Record the firm draft date in
league_intel the moment Yahoo schedules it.

### 8.6 Schema window addendum (R4-F14)

The weeks-19–21 playoff-density quantification: a ±1-game week for a single
top starter swings a 1-week playoff round's win probability ±5.5–6.4pp in the
sim's own model; a whole-team 3-vs-4 mismatch collapses it to ~0.11. The §7.5
schema widening adds per-player weeks-19–21 game counts when the 2026-27 NBA
schedule publishes (mid-August); the October build surfaces a playoff-density
column and the E9 playoff-tier objective consumes it.

### 8.7 In-season surfaces (R4-F15)

Two truth rules added to SKILL.md territory in September: (1) in-season
stash/drop/trade questions must state IL+ economics — a recovery player
eligible for the 2 IL+ slots costs zero active spots, so board absence is
never droppability; (2) F26's availability-adjusted trade delta ships before
the season starts (engine change: September window).
