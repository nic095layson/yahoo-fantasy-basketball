# REVERT-MAP — rollback recipes per layer (2026-07-30)

Every codified change in this repo is an atomic, documented commit with
its validation evidence in `arena/results/`. Any layer can be reverted
independently in minutes without touching the others. The deck rebuilds
from any commit (`python3 scripts/build_deck.py` after checkout of the
relevant files) and republishes to the standing artifact URL.

## Kill switches (no revert needed)

| Layer | Switch | Effect |
|---|---|---|
| Slot-gated gradient ordering | set `GRAD_SLOTS = 0` in `arena/arena.py` AND `docs/draft-deck.html` (one constant each) | **STALE, corrected 2026-08-09 (audit F59):** since the E9 blend50 ship the deck's Top-5 ordering is governed solely by `ds` — `GRAD_SLOTS = 0` now affects the ARENA and the deck's `fs`/tooltip metadata only, NOT the shipped card order. To change the card order use the decw-ordering kill switch below. |
| Single-🎯 system-pick marker | remove the `isRec`/`tgOnPin` marks in the Top-5 loop + pinned row | marker gone; ordering untouched |
| Strengths/Weaknesses header | remove the `#swline` render block in renderDecision | header gone |
| Market-timing chips / ladder | display blocks in the app script, all marked | display-only by construction |
| Survival chips + 🚌 wait-chain, RE-ENABLED 2026-09-22 on the price-only refit (D51R-1R; suspended 2026-09-21 between fits) | `SURVIVAL_DISPLAY = false` in the deck's engine block (one constant) | chips and wait-chain vanish; survivalProb stays defined |
| Price-only survival model (D51R-1R, 2026-09-22): engine `survivalProb` (`SURV_K` 0.30, `SURV_FLOOR` 8 — Φ((price − N)/max(8, 0.30·price)) on the baked Yahoo price, else the market-rank position) + app `survivalP` wrapper; twin `hoops.survival_prob`, parity item 7 | `git revert` the refit commit (restores the 2026-08-03 room-mix blend: `VAL_RANK`, `survPhi`, `SURV_W_VAL/MKT` in the app block) | back to Brier 0.651 on the two live rooms (`arena/results/survival_refit_2026-09-22.json`) |
| Clock read (M53, 2026-09-22): engine `clockRead(state)` — phase done / you / none-left / wait — renders the feed-title countdown and the strip's "your next"; twin `hoops.clock_read`, parity item 8 | restore the countdown's `until = nxt === null ? 0 : nxt - (n + 1)` and its `until === 0` branch in `renderStrip` (app block) | the mock-53 bug returns: "(you're on the clock)" for every pick after the owner's 13th |
| Refused Insert-at-# re-renders the log (M53, 2026-09-22) | delete the `else { save(); renderMirror(); }` branch in `runInsert` (app block) | an ambiguous-name warning surfaces only on the next action |
| Owner veto list (VETO, 2026-09-28): `JUDGMENT.doNotDraft` (judgment block; Kristaps Porziņģis) — the app builds YOUR candidates from `ownerPool(st)` = `availablePool` minus the list at the decision card and the TARGET read; Best-available keeps the row marked ⛔ DO NOT DRAFT; a `my:` pick of a listed name logs a warning; `hoops.do_not_draft()` / `owner_pool()` twin for `draft best` / `turn`; `live_deckcard.py` applies the replayed deck's list, `live_retro.py` only for `MOCKS[...]['veto']`; no engine function changed, parity EXACT; evidence `test_card` VETO cases, `test_draft` VETO cases, `arena/results/veto_dom_check_2026-09-28.json` | set `doNotDraft: []` (every reader treats an empty list as no veto; the plumbing becomes a no-op). Full removal: restore `const pool = availablePool(st, PLAYERS);` at the card and in the TARGET read, delete `VETO` / `ownerPool`, the Best-available marker block and the runFeed warning loop, `do_not_draft` / `owner_pool` in hoops.py (restore the two `availability(p) > 0` comprehensions) and the harness `veto` plumbing; drop the VETO cases | Porziņģis returns to the card wherever blend50 ranks him (rounds 6–8 in the three recorded rooms, never #1); the room-facing surfaces never changed |
| Card-gap echo (D54-1, 2026-09-28): app `LAST_CARD` (the card as last rendered) + `cardGapText(name)`; `feedHint()` on the feed's `input` event writes the staged my: pick's card rank and blend gap under the feed (`#feedHint`), and `runFeed` logs the same line for every new owner pick that is not the 🎯; a round-9+ suffix names the owner's rule (arena arms, mocks 51–54: the card beat late deviations 15 of 16) | delete the `#feedHint` element, the `LAST_CARD` / `cardGapText` / `feedHint` block, the `input` listener and the gap loop in `runFeed`; the `LAST_CARD =` line in `renderDecision` | the log and the feed go back to showing the pick with no card context |
| UNKNOWN follow-up (D54-2, 2026-09-28): engine `processFeed` keeps the raw text on a no-match UNKNOWN (`raw`), and the next un-numbered feed that resolves to a name matching that text (`unknownMatches`: 3-letter token prefix or containment) FIXES the UNKNOWN in place ("✎ #k fixed: UNKNOWN (…) → Name"); a non-matching name logs as usual plus "⚠ #k is still UNKNOWN"; gap placeholders never auto-fix; numbered feeds are literal; explicit fixes drop `raw`. Twin: `hoops.unknown_matches` + the same branch in `draft turn`. App: `unknownBadge(st)` names every open UNKNOWN in the strip, draft complete included. Evidence: `test_card` D54-2 cases, `test_draft` D54-2 cases, `arena/results/d54_dom_check_2026-09-28.json` (the mock-54 tool log replayed through the real page: 13 drifted positions → 1, the never-fixed #97) | engine: drop `raw:` from the no-match push and delete the `prevOpen` block (auto-fix + warning) in the resolved branch, and the `delete picks[idx].raw` in the correction branch; hoops.py: mirror (remove `unknown_matches`, the `prev_open` block, the `raw` key and the two `pop("raw")`); app: restore the previous strip block in place of `unknownBadge` | a name typed after an UNKNOWN logs as the next pick again and the board shifts one seat until a numbered fix (mock 54 #118–#129) |
| Dead-category trap line (D54-3, 2026-09-28): `renderDecision` keeps the advised read (`advisorLine`) and, once the 🎯 is known, appends "C is dead — don't reach: X (best C left, card #k) does not beat 🎯 Y; the card already prices C." Advice text only; measured before shipping: a punt-STEERED card from #63 on the mock-54 room scored 52.49% vs 59.27% unsteered (−6.8 pp, 0 of 3 seeds met the ≥2 pp bar; `arena/mocks/punt_arms.py`, `arena/results/m54_punt_arms.json`) — the advisor stays advice-only | delete the `advisorLine` declaration, its assignment after `meta.append(p)` and the D54-3 block after `LAST_CARD =` | the advisor line reads as before (lean / advise / clear path) without naming the reach |
| Empty-input guards + sweep count (V-D1/V-D2, 2026-09-29, system-validation decisions D1/D2): `runInsert`'s empty-input guard and `runResync`'s empty-paste guard call `save(); renderMirror();` before returning (the 127-assertion Chromium drive found both paths silent until the next action); the Daily-sweep panel's step text counts `PLAYERS.length` instead of the July literal 246; evidence `test_card` V-D1/V-D2 cases (red on v30, green after), `arena/results/full_dom_check_2026-09-29_fixed.json` (127/127, exit 0) | delete the two `save(); renderMirror();` lines and restore the literal | pre-2026-09-29 behaviour: an empty Insert / Rebuild click shows nothing until the next action; the panel says 246 |
| Dot-folding in the feed resolver (D53-4, mock 53 ask 2026-09-22, executed 2026-09-29): `fold()` in the engine block and `hoops.fold` strip `.` along with apostrophes and diacritics, so Yahoo's "P.J. Washington" meets the pool's "PJ Washington" and a typed "TJ McConnell" meets the pool's "T.J. McConnell" (both failed every resolver stage before); the downstream `replace(/\./g, "")` calls are now no-ops kept for symmetry; evidence `test_card` D53-4 cases (2 of 59 red on v31, 59/59 green after), `test_draft` 62/62, `test_gates` 34/34, parity EXACT, `arena/results/full_dom_check_2026-09-29_v32.json` (127/127, exit 0, two runs) | remove the `.` from the two fold character classes (`/['’`.]/g` and `"'’`."`) | pre-2026-09-29 behaviour: a pasted "P.J. Washington" or typed "TJ McConnell" logs UNKNOWN |
| Concise decision card, Option A (D57-1, owner 2026-09-29: "When I have a 60 second pick clock, this is a lot of information to digest"): in `renderDecision` (app block) the advisor read is one plain-words line (`Losing … to most of the room, 2 picks running (you beat …). Don't punt them: you'd be winning only w of the other k categories (need n). Keep taking the best player.`), the D54-3 trap is a second line (`Don't reach for a lost category: X (C, card #k) · … — none beats 🎯 T`), and the `#swline` panel is one `p.swone` row (Strong · Winnable · Soft punt; weaknesses dropped, the chip strip shows them); the two `p.zoneline` labels are removed from the markup. Mockups: artifact FTHDzNSqdqXSfsEgheHMiB. Evidence: `test_card` D54-3 reworded (1 of 61 red on v33, green after), `full_dom_check` `turn.concise` at all 13 owner turns. | restore the pre-v34 `puntread` texts, the per-category `textContent +=` trap loop, the two-column `swL`/`swR` build and the two `zoneline` paragraphs (`git show 793a92c:docs/draft-deck.html`); revert `test_card.py`'s D54-3 case and the `turn.concise` assertion in `full_dom_check.mjs` | the sixteen-line card |
| Owner's turn made unmistakable (D57-2, owner 2026-09-29: "I sometimes don't realize it is my turn and lose seconds off my pick clock"): `setOwnerTurn(on, pickNo)` in the app block shows `#youBanner` (accent-fill "▶ YOUR PICK — #n", two brightness pulses unless reduced motion) and marks `.feedcard.onclock` (accent border, glow, tinted thick-bordered `#feed`) whenever `clockRead` says phase `you`; the strip's "YOU are on the clock" and the countdown's `onclocknow` line are unchanged. Evidence: `full_dom_check` `turn.banner` at all 13 owner turns and `S2.banner-hidden-when-not-you`. | remove the `#youBanner` div, the `.youbanner` / `.feedcard.onclock` CSS and the `setOwnerTurn` calls in `renderStrip`; revert the `turn.banner` and `S2.banner-hidden-when-not-you` assertions in `full_dom_check.mjs` | the v33 state: bold strip line and accent countdown only |
| Urgent-TARGET 🎯 gate (D51R-4) | `PIN_MAX_GAP = Infinity` and delete the `pin.av < 1` line in `pinDecision` (engine block) | pre-2026-09-21 behaviour: any urgent read takes the 🎯 |
| ΔECW tie-break (D51R-2) | remove the middle clause of `rankCard` (engine block) AND the middle key of the ordering in `scripts/check_parity.py` — both, or parity fails | name-only tie-break |
| Punt advisor advice-only + room-relative read (D51R-3, 2026-09-21) | `PUNT_BUTTONS = true` in the deck's engine block restores the FULL TILT / Adopt / Retarget buttons (every write routes through `adoptPunt` in the app block, dead while the switch is false); the room-relative read (catWinProb / puntRead / coherenceRead) has no switch — revert the introducing commit to get the 13-man z-sum drift and coherence back | buttons back, advice text stays; measured on the 8 committed states (`arena/results/m51_punt_advice_effect.json`): the old advisor proposed punting a category the roster was beating ≥50% of the room in on 7 turns (all TO, state 50, 55–80%), the new one on 0 |
| Yahoo prices in the Mkt rank (F8, 2026-09-22) | remove the kit's `report/market/yahoo-*.csv` (or build with an empty kit market dir) and rebuild — the build drops `data/market-snapshot.csv` and both engines fall back to the internal model together | pre-F8 Mkt: the points-volume proxy + rookie pins |

**Display surfaces RETIRED 2026-07-30 (owner: noise)** — all removed in
commits `d2e930d` (archetype tags + roster census) and the simplification
commit after it (🧭 compass line, 🎯 NN% confidence spans, Value/Market
strips, composite title line). The underlying layers stay internal:
`ar/fx/sy` still bake into PLAYERS (currently UNCONSUMED by the live app —
audit 2026-07-31; September checkpoint to drop or re-use), `gradImpact`
remains defined for harnesses/future surfaces, and `cheapestConcessions`
is LOAD-BEARING again — the Soft Punt panel line consumes it (punt-aware
since the 2026-07-31 audit fix). To restore any retired surface,
`git revert` the removing commit (each is atomic and display-only).

## Full-layer reverts (git)

Ordered newest-first; each SHA is the commit that INTRODUCED the layer.
`git revert <sha>` (or checkout the prior SHA's versions of the listed
files), rebuild deck, run gates (verify_rosters, build round-trip,
parity), republish.

| Layer | Introduced | Files | Known-good prior state |
|---|---|---|---|
| Commitment meter + 🎯 boundary copy | `d9e1c80`+ | deck | `a1d01cd` |
| Gradient ordering + 🎯 display | `a1d01cd` | deck, arena | `b7ea017` |
| 9-CAT codification (P1 %-variance, P2 seeding, P3 draftable-156 z, market-mult hygiene) | `b328ef7` | arena, hoops, deck | `1ae3693` — NOTE: reverting this restores the four confirmed instrument/engine defects; do not revert below this line without re-reading `findings_2026-07-30_ninecat_math.md` |
| Market-timing layer + scarcity fix | `fd4edbc`, `0866df1` | deck | `beb2c72` |
| Buckets 1+2 (neutral weights, deck UI) | `8c65750`, `201c23c` | arena, deck | pre-7/28 history |

## What each layer's evidence says (why reverting is NOT currently indicated)

- Neutral weights: +5.59pp t=7.18 (re-quoted on the fixed instrument).
- P1–P3 instrument/engine fixes: anchored to external facts (binomial
  floors, Yahoo's seeding rule, the draftable universe); council
  tournament 4th→2nd; all-pass integrity suite.
- Slot-gated gradient: +12.67pp t=4.63 at 18 virgin-seed CRN cells;
  gated precisely because the global test was inconclusive and the
  mock-15 counterfactual confirmed mid-seat greedy-following hurts.
- Display layers (chips, 🎯, ⚖): never re-rank anything; each carries
  its evidence and its limits in its own tooltip.

Reproducibility: historical experiment harnesses pin their engines
(scratch copies or the 0.35/0.45 field pins) and reproduce against the
SHAs noted in their findings files. Arena numbers before `b328ef7` are
old-instrument and not comparable to current runs.

## 2026-08-04 — owner-directed display fixes (both single-site reverts)

- **Room-mix survival model** (`docs/draft-deck.html`, app block): constants
  `SURV_K/SURV_FLOOR/SURV_W_VAL/SURV_W_MKT`, `VAL_RANK`, `survPhi`, and the
  blended `survivalP(name, pickN)`; chip thresholds BUY ≤0.20 / TOSS <0.40.
  REVERT: restore `survivalP(mkt, pickN)` with Φ((mkt−N)/max(6,0.15·mkt)) and
  thresholds 0.40/0.60, and re-point the three call sites at `MKT_RANK.get`.
  Calibration record: `arena/results/after_2026-08-04_fixes_recalibration.md`.
- **TARGET/BOARD LEAN provenance** (`engine` block `archetypeRead` returns
  `boardOnly`; app block label template). REVERT: drop the `boardOnly` const +
  tip line and restore the fixed `TARGET:` prefix.

## decw-ordering (E9 blend50, shipped 2026-08-04)

The Top-5 ORDER at every seat is the ΔECW blend50 score (`ds`), replacing
the composite `fs` sort and the slot-1–3 gradient gate. Validation:
`arena/results/findings_2026-08-04_decw_round2.md` (14/14 improved, 0
winner regressions, fresh-seed replicated; JS↔Python ordering parity
182/182 EXACT). **Kill switch:** in the app block, change the scoredAll
sort back to `.sort((a, b) => b.fs - a.fs)` (one line; `fs` is still
computed on every row), restore the fs-unit coin-flip/standout thresholds
(0.25 / 1.5), and revert the score display spans from `ds * 100` to
`fmtZ(fs, 2)`. The engine-block ΔECW section (RAW_COLS … decwScores) and
the `r` array in PLAYERS are inert once the sort reverts — safe to leave.
**Standing kill RULE:** two consecutive out-of-sample mocks where
blend50-follow measures worse than composite-follow beyond noise trigger
this revert plus a written post-mortem (findings file, §Standing caveats).


## named-room (E18 mock cast, shipped 2026-08-04)

Mock seats are held by the 11 named league-mates (`MANAGERS` +
`managerScores` in the engine block; per-draft seat shuffle stored as
`state.cast` in the app's start handler). Validation:
`arena/results/findings_2026-08-04_e18_named_room.md` (smoke 5/5 owner
slots, owner-card parity 7/7 byte-identical, scaled reach band 11/11,
Spearman 0.936; noise model corrected same day by E18b — see below). **Kill switch:** in the app block's start handler, delete
the `if (mockMode) { ... deck.state.cast = cast; }` block — `mockCastFor()`
already falls back to the legacy `MOCK_CAST` persona cast when no cast is
stored, and `advanceAI` dispatches non-manager names through
`strategyScores` unchanged. The engine-block `MANAGERS`/`managerScores`
section is inert once no cast references it — safe to leave. The owner's
ΔECW blend50 card is independent of this ship (parity-proven) and keeps
its own kill switch above.

### E18b amendment (noise model, shipped 2026-08-04)

Owner-reported realism defect (SGA alive at pick 8) fixed:
`managerScores` noise became log-normal on rank (`r *= exp(N(0, noise/
MGR_NOISE_DIV))`, `MGR_NOISE_DIV = 50`), availability became proportional
(`r *= 1 + (1-av)*0.35`, streamers `0.15`), loyalty discount floored at 1;
Noah refit to manual drafter (owner correction: autodraft was 2025-26
only) and Kyle refit to his measured mild reach. Validation:
`arena/results/findings_2026-08-04_e18b_noise_model.md` (all six gates
pass; owner-card parity 7/7 byte-identical). **Narrow revert** (noise
model only, keeps the named room): restore the three lines in `score()` —
`r -= m.loyal[p.n]` un-floored, `r += (1-av)*(streamer?15:40)`, and the
additive `s += rng.gauss(0, m.noise)` after the need bonus — and restore
Noah/Kyle's prior MANAGERS entries. The full named-room kill switch above
also covers this.
