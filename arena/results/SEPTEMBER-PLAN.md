# September recalibration plan — pre-registered 2026-07-31, owner-authorized

**Standing state until this plan executes:** FEATURE FREEZE. No engine or
judgment-layer changes ship before the September run. Allowed meanwhile:
display-only fixes, truth/reporting fixes, and anything the owner asks
for explicitly. Measure-only studies are always allowed.

**Authorization.** On 2026-07-31 the owner asked that the September work
happen systematically, without a prompt from him. A one-shot scheduled
Routine fires on **2026-09-01** and executes this file top to bottom in a
fresh session. This file is the single source of truth for that run —
the firing prompt intentionally contains no details beyond "execute
SEPTEMBER-PLAN.md".

**Ship rule (the honest contract).** "Systematically installed" means
systematically *executed*. Each item below carries a pre-registered
acceptance bar. Data recalibrations ship when the build gates pass.
Engine/judgment changes ship **only if they beat the incumbent on the
arena instrument without regressing the winners** (mocks 21/24/25/26 as
replay baselines). Anything that fails its bar stays out and gets a
written negative result. This is the same standard that kept the
computational layer defect-free through two full audits — it does not
relax because the calendar turned.

## 0. Read first (context recovery for the fresh session)

**`arena/results/league_intel_2025-26.md` — the owner's REAL league ground
truth (settings, standings, weekly data, draft board, room model). It
supersedes any assumption it contradicts and feeds E14–E17.** Then
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

## 3. Validation before anything merges

Parity EXACT; build gates; the 130-state render gauntlet + mutation
suite (harness described in `audit_2026-07-31b_deck_integrity.md`);
replay of ledger mocks as regression fixtures; `LEDGER.md` updated per
its standing rule — plus the audit's grep sweep for unbacked derived
claims in any new prose.

## 4. Delivery

Branch `claude/2026-09-01-september-recal` off the default branch; draft
PR; subscribe to PR activity. Rebuild and **republish the deck artifact
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
| E18 | **Named manager profiles (owner directive 2026-08-04):** (a) ~~deck MOCK mode fields the 11 real managers~~ **SHIPPED 2026-08-04** (`findings_2026-08-04_e18_named_room.md`): MANAGERS + managerScores in the engine, per-draft seat shuffle stored on state, Robby adp_w refit 0.55→0.7; smoke 5/5 slots, owner-card parity 7/7 byte-identical, scaled reach band 11/11 pass, Spearman 0.936; (b) LIVE mode with named seats replaces the generic room-mix survival with **per-seat pick projection**: P(manager m takes player p before my next turn), chained across the actual managers sitting between my picks, feeding BUY NOW/quiet and a pre-draft per-round target sheet per rival — still open for September | Three-season boards + complete identity map (league_intel §12); profiles.json committed 2026-08-04 | **Absolute ±8 reach bar re-arms at the October real-ADP sync** — the synthetic market carries only ~0.45 of real Yahoo's divergence from the value board (Noah anchors the scale), so until real ADP replaces the proxy geometry the binding bar is the Noah-anchored scaled band (passed 11/11). Survival: BUY NOW precision ≥80% maintained; October brief consumes the projection sheet |

