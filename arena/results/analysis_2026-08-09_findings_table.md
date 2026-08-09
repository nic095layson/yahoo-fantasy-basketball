# Appendix A — the 66 verified findings (audit 2026-08-09)

Companion to `analysis_2026-08-09_self_critique_round3.md`. Every finding below survived an independent adversarial verifier instructed to refute it; where the verifier narrowed the claim, **the narrowed wording is what appears here** — several originals were materially overstated. `STATUS` is novelty against E1–E23/E9b, T1–T7, N1–N7 and LESSONS 1–14. Claims are trimmed for length; the full text of any item is regenerable from the workflow run recorded in the report's provenance section.

**Read the body, not the title.** Titles are as-raised by the original auditor and several
overstate what survived — F10's title says "all 7 counting cats (1.25–2.07x)" where the verified
claim is 3 of 7 at 1.1–1.65×; F23's says "5.7x / ~0.85-1.0" where the measured relative weight is
0.956. The claim paragraph governs in every case.

Reference an item by its `F##`.

## Index

| # | Sev | Area | Status | Finding |
|---|---|---|---|---|
| F01 | high | data | NEW | verify_rosters.py in fallback-partial mode compares players.csv against a mirror of itself — 'checked: … |
| F02 | high | engine | NEW | draft turn logs a FABRICATED pick when a feed segment is a single character or punctuation |
| F03 | high | process | NEW | Draft night runs two different boards with two different orderings, and nothing written says which wins |
| F04 | high | process | NEW | The fail-closed publish gate certifies a date, not research — I passed all three gates with zero research |
| F05 | high | skill | NEW | Live-draft protocol commands hoops.py, which never received blend50 — the validated ordering exists only … |
| F06 | high | skill | NEW | The confidence-% format has no calibration, is arithmetically incoherent as specified, and contradicts a … |
| F07 | medium | arena | KNOWN-PARTIAL owner gap #1 / E22 | BENCH_WEIGHT=0.15 is falsified by the GP column of the owner's own weekly file, and flipping it changes … |
| F08 | medium | arena | KNOWN-PARTIAL lesson 13 | The LEDGER's own audit trail is not in the repo: 21 of 25 result rows, 5 of 5 interior-tally artifacts, … |
| F09 | medium | arena | NEW | The instrument's honesty rule targets the wrong error source: draft-to-draft sd is 8.4pp, Monte-Carlo sd … |
| F10 | medium | arena | KNOWN-PARTIAL N1 / T2 (also … | Weekly model under-disperses all 7 counting cats (1.25–2.07x) and models categories as independent; the … |
| F11 | medium | arena | NEW | `arena live` never passes the market board, so the practice room the draft-arena skill prescribes … |
| F12 | medium | data | NEW | Six second-year players still carry 'rookie-proj', applying a market-hype premium worth 12-21 draft … |
| F13 | medium | data | NEW | Team shot budgets are violated by up to 42% — per-player lines were never reconciled against the fixed … |
| F14 | medium | data | NEW T4/N3 (partial: they register … | The June-2025 draft class never had its rookie season ingested — 9 rows are byte-identical to the … |
| F15 | medium | data | NEW | The published deck's JUDGMENT layer is outside every build gate — and already contradicts the pool it … |
| F16 | medium | data | NEW | availability() note parsing: a season-ending injury written in plain English scores at FULL value, and … |
| F17 | medium | deck | NEW | Build-coherence strip reads "⚠ WRONG TARGETS" in 79% of punted states; its Retarget button implements … |
| F18 | medium | deck | NEW | Colophon describes a mock room the deck no longer runs, and states the star-fall property backwards vs … |
| F19 | medium | deck | KNOWN-PARTIAL T7 ("judgment layer … | Judgment layer is 11 days stale, contradicts the deck's own colophon and players.csv, and no build gate … |
| F20 | medium | deck | NEW | On pick #1 from slot 1 the card's headline number is off-scale by ~50×: it renders "lead +57.2 🚀" and a … |
| F21 | medium | deck | KNOWN-PARTIAL N1 (ECW validated … | The weekly model's percentage-category variance is refuted by the owner's own weekly data now committed … |
| F22 | medium | deck | NEW | Typo matching is dead for all 12 "Jr./suffix" players — and "jacksn" silently logs GG Jackson instead of … |
| F23 | medium | domain | KNOWN-PARTIAL E22 (+ … | BENCH_WEIGHT=0.15 is 5.7x too low: the real weight is ~0.85-1.0, and the repo's own Yahoo data proves it |
| F24 | medium | domain | NEW | Games-per-week is not modelled anywhere; players.csv has no games or minutes column at all |
| F25 | medium | domain | NEW | Six of the 2025 draft class are still tagged `rookie-proj` for 2026-27, and nothing in the refresh law … |
| F26 | medium | engine | NEW | Availability never reaches any category total: trade says you WIN by acquiring a player the engine … |
| F27 | medium | engine | NEW | No Unicode normalization: Jokić, Dončić, Şengün, Porziņģis all fail to match and become UNKNOWN |
| F28 | medium | engine | NEW | The 0.78 injury haircut switches off entirely below replacement level — from board rank 62 down, injury … |
| F29 | medium | engine | NEW | UNKNOWN placeholders silently corrupt roster count, remaining-picks arithmetic, the feasibility guard, … |
| F30 | medium | engine | NEW | draft fix --slot skips range validation on the UNKNOWN branch and bricks every roster command with an … |
| F31 | medium | engine | NEW | draft fix prints the NEW name on both sides of the arrow — the correction echo can never be verified |
| F32 | medium | engine | NEW | draft turn silently accepts a my: snake desync that draft pick --mine warns about |
| F33 | medium | process | KNOWN-PARTIAL N7 | No refresh is scheduled between the October Routine and draft night, and the Routine's self-reschedule … |
| F34 | medium | process | KNOWN-PARTIAL lesson13 / T7 | September's ship bars are unevaluable: the m21/m24/m25/m26 replay states do not exist anywhere |
| F35 | medium | process | KNOWN-PARTIAL T7 | The deck's JUDGMENT layer is 11 days stale, no gate sees it, and it is currently penalizing a player who … |
| F36 | medium | skill | NEW | Live-draft failure modes are unaddressed: state corruption crashes with a raw traceback, RESYNC has no … |
| F37 | medium | skill | KNOWN-PARTIAL N5 | The skill encodes none of the league settings that define this league — daily lineups, unlimited moves, … |
| F38 | low | arena | NEW | 13 personalities in 12 seats systematically denies each strategy one specific draft slot in tournament() … |
| F39 | low | arena | KNOWN-PARTIAL T2 / N1 / LEDGER §5 … | Circularity inventory: the objective, the grade, and the ship bar all read one model whose ~14 weekly … |
| F40 | low | arena | KNOWN-PARTIAL owner gap #2 | Dylan Harper is still priced as a hype rookie inside the arena's market model, which the September plan … |
| F41 | low | data | KNOWN-PARTIAL T4 / N3 (variance … | Schema has no minutes, no games-played, no age, no ADP and no variance — the four checks that would have … |
| F42 | low | data | KNOWN-PARTIAL E16 / N5 … | The pool is a draft board, not a season pool: 85 undrafted names for an 18-week season with unlimited … |
| F43 | low | deck | NEW | 16% of owner turns have an exact #1/#2 tie broken by reverse-alphabetical name, and the 🎯 "system pick" … |
| F44 | low | deck | NEW | Every tooltip in the deck is mouse-only: the entire explanation layer is unreachable on a phone or tablet |
| F45 | low | deck | NEW | Judgment layer is inert: `adj` never reaches the Top-5 sort key, but the card still prints "jdg −0.30" … |
| F46 | low | deck | NEW | No committed JS↔Python parity harness exists — the September/October Routine's `PARITY: EXACT MATCH` … |
| F47 | low | domain | NEW | Positional saturation is nearly free under daily lineups — the entire positional-need machinery is … |
| F48 | low | domain | KNOWN-PARTIAL E20/E23 | Punt doctrine is imported from most-categories/roto play; in an each-category league every punt is ~18 … |
| F49 | low | domain | NEW | The live skill instructs Claude to weight swing categories more heavily — the exact rule the arena … |
| F50 | low | domain | KNOWN-PARTIAL N1 | The season sim's weekly variance is ~half of reality in all 7 counting categories — and the aggregate … |
| F51 | low | domain | NEW | The two tools you use on draft night disagree about bench value by 5.7x |
| F52 | low | engine | KNOWN-PARTIAL lesson 7 | No end-of-draft guard: turn and pick keep logging picks 157, 158, 159 in a 156-pick league, and … |
| F53 | low | engine | NEW | One malformed cell in players.csv kills every command including draft turn — and SKILL.md tells the … |
| F54 | low | engine | NEW | The top-156 z-score fixed point can 2-cycle and can exceed its 5-iteration budget, silently and without … |
| F55 | low | engine | NEW | save_state is a truncating non-atomic overwrite with no backup; a corrupt state file gives a raw … |
| F56 | low | process | NEW | 'Republish to the artifact URL' is the definition of done, but nothing verifies it and the Routines' … |
| F57 | low | process | NEW | Documentation-truth cluster: RESEARCH.md, README.md and SKILL.md describe an engine and a pool that no … |
| F58 | low | process | NEW | Draft-night arena intel is computed on the frozen October-2025 pool, and the SKILL's skip rule … |
| F59 | low | process | NEW | REVERT-MAP's first kill switch is stale — GRAD_SLOTS=0 no longer turns off the deck's ordering |
| F60 | low | process | NEW | SEPTEMBER-PLAN §3's validation requirements name artifacts that do not exist as runnable code |
| F61 | low | skill | NEW | Adding a missing player's row mid-draft silently re-bases every value the tiebreak and the NN% are … |
| F62 | low | skill | NEW | Practice drafts are systematically distorted: 28 live-pool players — including the entire 2026 rookie … |
| F63 | low | skill | NEW | Pre-draft checklist timings are wrong in both directions and its skip-condition is unexecutable |
| F64 | low | skill | NEW | Protocol hygiene: dead skill reference, --expect contradicted by the tool's own prompt, and zero test … |
| F65 | low | skill | NEW | The turn card's "helps" annotation prints negative z as help, and targets the categories the same skill … |
| F66 | low | skill | KNOWN-PARTIAL T1 | §1 and §3 give flatly contradictory position rules for 120 of 156 picks, and the round-11 rule … |

---

## HIGH — Data layer

### F01 · verify_rosters.py in fallback-partial mode compares players.csv against a mirror of itself — 'checked: 246, mismatches: 0' is a tautology

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The roster-validation lock is inert as an independent check in the mode it actually runs in. ESPN direct mode is blocked here (403 tunnel), so verify_rosters.py runs fallback-partial against data/rosters_official.json — a hand-maintained file containing exactly the 237 non-FA (player, team) pairs players.csv already asserts (0 extra names, 0 disagreements, 6-11 players per team vs a real 15-man roster). It is not auto-derived from the pool, but it is updated in the same commits as the pool, so it can never disagree: 'checked: 246, mismatches: 0' revalidates a frozen 2026-07-23 verification snapshot under today's date rather than testing the pool against current reality — precisely the missed-quiet-transaction failure (Hachimura, LESSONS …

- **Evidence** — MIRROR PROVEN (script I ran over the two repo files): `evidence teams: 30, evidence player entries: 237 / pool rows: 246, pool non-FA: 237 / evidence names NOT in pool: 0 / pool non-FA names NOT in evidence: 0 / disagreements: 0`. TEST B (mutated COPY in /tmp, repo untouched): appended `Bronny James,ZZZ,PG,SG,...` to the copied players.csv and ran the copied verifier → `pool rows checked: 246/247 unmatched: 1` / `mismatches: 0` / `exit=0` — a player on team "ZZZ" passes the lock. TEST A (control): changing LeBron …
- **Cost** — The single mechanical defense against the exact defect that produced LESSONS #12 (39/220 stale team rows) is inert. Between now and October there will be training-camp trades, waivers, and camp cuts; …
- **Action** — (1) Make `unmatched_count > 0` a hard fail in both verify_rosters.py and the hoops.py stamp gate (or at minimum surface it in the deck manifest). (2) Rename the fallback-mode output so it cannot be read as verification: report `self_consistency_checked` rather than `checked`, and have build_deck.py stamp 'UNVERIFIED (fallback)' in the deck header when mode != direct-complete. (3) Either get site.api.espn.com …
- **Owner question** — Can you get site.api.espn.com (or any full-roster feed) allowlisted in the environment before October? If not, are you willing to hand-paste 30 full rosters once in early October so the fallback file becomes real evidence rather than a …


---

## HIGH — Python engine (hoops.py)

### F02 · draft turn logs a FABRICATED pick when a feed segment is a single character or punctuation

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`match_candidates` (scripts/hoops.py:365) applies a bare substring stage `q in p["player"].lower()` with no minimum-length or shape guard, and `draft turn` (hoops.py:787-797) resolves any non-empty candidate set by logging `max(cands, key=adj_value)` as a CONFIRMED ✓ pick with only an "(assumed over X, Y)" hedge naming 2 of N candidates. Verified on the live 246-row pool: a feed segment of '.' matches 10 players, '-' 5, "'" 7, 'j' 68, 'a' 195, and a bare `my:` (whose name is `body[3:].strip()` = "", hoops.py:725) matches all 246. Verified transcripts: `draft turn "Nikola Jokic; .; -"` logs Jaren Jackson Jr. to T2 and Shai Gilgeous-Alexander to T3; `draft turn "Nikola Jokic; my:; Victor Wembanyama"` logs Wembanyama to YOUR slot and then …

- **Evidence** — Repro (cwd /tmp/hoops, HOOPS_DRAFT_STATE=/tmp/hoops/ds2.json, after `draft init --teams 12 --size 13 --slot 4`): $ python3 scripts/hoops.py draft turn "Nikola Jokic; .; -" --top 1 ✓ #1 R1: Nikola Jokic → T1 ✓ #2 R1: Jaren Jackson Jr. → T2 (assumed over Wendell Carter Jr., Kevin Porter Jr.) ✓ #3 R1: Shai Gilgeous-Alexander → T3 (assumed over Karl-Anthony Towns, Nickeil Alexander-Walker) state file: [{'player': 'Nikola Jokic', 'slot': 1}, {'player': 'Jaren Jackson Jr.', 'slot': 2}, {'player': 'Shai …
- **Cost** — On draft night a stray hyphen, period, apostrophe, or truncated name in a semicolon feed — from voice dictation, a copy/paste artifact, or a fat-fingered `my:` — removes a top-20 player from the …
- **Action** — Add a minimum-length/shape guard to the substring stage of `match_candidates` (e.g. require len(q) >= 3 and at least one alphabetic character before the substring fallback fires) and make `draft turn` treat a zero-length or non-alphabetic segment as an UNKNOWN placeholder rather than a match. Separately, cap the auto-resolve: if len(cands) exceeds a small threshold (say 4), HALT the same way the surname collision …
- **Owner question** — Do you want an over-broad match to HALT the batch (safest, costs a resend) or to log UNKNOWN and keep going (preserves numbering, costs a later fix)?


---

## HIGH — Process & gates

### F03 · Draft night runs two different boards with two different orderings, and nothing written says which wins

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The two surfaces that could run on draft night order candidates by different objectives, and no session-facing document says which one governs a pick. The published Draft Deck sorts its Top-5 and its single 🎯 system pick by the punt-blind ΔECW blend50 score `ds` (draft-deck.html:2335, decwScores:1051-1059, DECW_ALPHA=0.5); scripts/hoops.py contains no ΔECW code and prints its numbered candidate list in punt-aware adj_value order (hoops.py:823, adj_value:314-318, card print:873). Reproduced on the owner's own uploaded mock states via the repo's validated reference construction: the two #1s differ on 19 of 26 owner turns, mean top-5 overlap 1.8/5, and the deck's #1 sits as deep as rank 39-41 on the hoops board in the declared-punt mock …

- **Evidence** — $ grep -c -i 'ecw|decw' scripts/hoops.py -> 0. hoops.py:823 'pool.sort(key=lambda p: -adj_value(p, override))'. draft-deck.html:2335 '.sort((a, b) => b.ds - a.ds || ...)' with the comment at 2314-2320 stating ds replaces the fs sort and the gradient gate. REVERT-MAP.md:73-77 ('decw-ordering (E9 blend50, shipped 2026-08-04)') lists the change as deck-only; findings_2026-08-04_decw_round2.md validated it on the deck. $ grep -c -i 'deck' .claude/skills/fantasy-basketball/SKILL.md -> 1 (line 14, the refresh …
- **Cost** — 45-second clock, owner staring at the deck's #1, Claude posting hoops.py's #1, and they are different players. The owner either loses seconds reconciling or takes the un-validated board — the deck's …
- **Action** — Add a 'Draft-night surface' section at the top of the SKILL's live-draft protocol: state that the published deck at the standing artifact URL is the authoritative board, that `draft turn` is the logging/bookkeeping surface and its candidate order is NOT the shipped ordering, and give the one-line reconciliation rule (read candidates off the deck; use the turn card only for the flags hoops.py has and the deck does …
- **Owner question** — On draft night, do you want Claude driving the deck in a browser, or you driving the deck while Claude only logs picks and adds flags? The written protocol currently assumes neither.

### F04 · The fail-closed publish gate certifies a date, not research — I passed all three gates with zero research

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The three-gate publish pipeline certifies dates the scripts stamp themselves, not research. verify_rosters.py writes datetime.date.today() unconditionally (verify_rosters.py:124) and in fallback mode never reads data/rosters_official.json's own `date` field (currently 2026-08-04); hoops.py's stamp gate and build_deck.py's gates 1-2 then check only that those self-written dates equal today, and gate 3 only that MUST_HAVE names exist. Nothing tests that players.csv changed or that any source was consulted. Reproduced end-to-end on 2026-08-09 with no network and a byte-identical CSV: three commands, three green lights, "safe to publish", a deck manifest carrying the note "AUDIT DRY RUN: I did zero research", and a header that renders "fresh …

- **Evidence** — Ran end-to-end in /tmp/fbaudit on 2026-08-08 with no web access and no CSV edit: $ python3 scripts/verify_rosters.py -> 'roster verification [fallback-partial] ... pool rows checked: 246/246 unmatched: 0 / mismatches: 0' EXIT=0 $ python3 scripts/hoops.py freshness --stamp --note 'AUDIT DRY RUN: I did zero research. No web search. No CSV edit.' -> 'Freshness stamped: 2026-08-08' EXIT=0 $ python3 scripts/build_deck.py -> 'deck built: 246 players · pull 2026-08-08 · verification fallback-partial (246/246 rows …
- **Cost** — This is the single load-bearing safety property of the whole October pipeline, and it is decorative in fallback mode. On 2026-10-12 a weaker model that skims the SKILL, runs the three commands, sees …
- **Action** — Two mechanical changes, both small: (1) in verify_rosters.py fallback mode, FAIL unless EVIDENCE['date'] == today — the evidence file must be re-authored by that day's pull, not re-dated by the script; (2) in build_deck.py, add a gate that data/players.csv's content hash differs from the hash recorded in the previous build manifest OR that freshness.json's note explicitly asserts 'no changes' with a source count, …
- **Owner question** — Can you allow site.api.espn.com in the environment network policy before October? Without it the roster lock is self-referential, and no amount of code fixes that.


---

## HIGH — Skill / live protocol

### F05 · Live-draft protocol commands hoops.py, which never received blend50 — the validated ordering exists only in the deck

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The live-draft protocol in .claude/skills/fantasy-basketball/SKILL.md is stale relative to the owner's confirmed draft-day workflow. §2 names `python3 scripts/hoops.py draft turn` as the one authoritative live command and §3 says to build the candidate card "straight from the `turn` card"; the word "deck" appears in SKILL.md only once, at line 14, inside the publish-gate paragraph. But the owner confirmed on 2026-08-04 (league_intel_2025-26.md §9 item 10) that draft-day use is the Draft Deck and "the mock workflow is the real workflow," and every mock 27-34 debrief replays through the deck's shipped UI handlers. Meanwhile the E9 blend50 ship landed only in docs/draft-deck.html (decwScores :1051, ordering :2314-2338); `grep -Ei …

- **Evidence** — scripts/hoops.py:823 `pool.sort(key=lambda p: -adj_value(p, override))` (the turn-card ordering) and :434 same for `best`. `grep -ni "decw|blend50|ecw|cats_won" scripts/hoops.py` → 0 matches; same grep on docs/draft-deck.html → decwScores present, line 2399 tooltip "top blend50 score: 50% marginal expected-cats-won vs this room + 50% balanced value". `grep -rn "draft-deck" .claude/skills/fantasy-basketball/SKILL.md` → only line 14 (publish gate). arena/results/findings_2026-08-04_decw_round2.md: "Where full …
- **Cost** — On October draft night, a session executing the written protocol produces recommendations from the objective the system measured as inferior by 7–23pp of championship probability on the only four …
- **Action** — Before October: either (a) port blend50 into `hoops.py draft turn` behind the existing `arena/mocks/decw_card_v2.py` reference implementation and re-run the parity gate, or (b) rewrite SKILL.md §2–3 to make the deck the authoritative live surface and demote hoops.py to logging/bookkeeping. Pick one and state explicitly in the skill which surface wins on disagreement. Do not leave both.
- **Owner question** — On draft night, which do you actually read off — the Draft Deck in the browser, or Claude's chat card? The protocol assumes the chat card; the engineering assumes the deck.

### F06 · The confidence-% format has no calibration, is arithmetically incoherent as specified, and contradicts a shipped-then-deleted measured version

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md:35 mandates `Name (POS, team) — NN%` as the ONLY permitted live-draft output format, with the percentage declared ABSOLUTE and council-ratified ("95% = no contest, 55% = coin flip — never normalize"). Three verified defects, none of them registered in SEPTEMBER-PLAN (E1-E23, E9b), the self-critiques (T1-T7, N1-N7), or LESSONS 1-14. (a) NO ANCHOR AND NO PROCEDURE. There is no reference table, no worked example, and no mapping from any card quantity to a percentage anywhere in the repo. Measured consequence across the only full transcript of the format (report_2026-07-12_live_arena_x3.md, three complete drafts, 45 cards): the top candidate lives in a narrow 50-88 band (mean 58.2), and the doc's "95% = no contest" anchor was reached …

- **Evidence** — Extracted all 45 confidence cards from arena/results/report_2026-07-12_live_arena_x3.md (the ×3 integrity run, three full drafts): top-candidate % min 50, max 88, mean 58.2; card sums min 149, max 272, mean 215.4; 45/45 cards sum >100%. Not one card in three full drafts reached the doc's "no contest" 95, and the median top-2 gap is 3 points. Skill coin-flip rule (top-2 within ~5) fires on 32/45 = 71% of turns. Deck's independent coin-flip: docs/draft-deck.html:2345 "coin-flip 0.011 preserves the old ~64% fire …
- **Cost** — The single most owner-visible output of the system is a number with no defined units, no anchor, and no procedure — 71% of picks come back labeled "coin flip" and the top number lives in a 50–88 band …
- **Action** — Replace the hand-authored NN% with a mechanical one before October: resurrect the deleted `share-of-best · ±X.XX cats/wk` layer (it is already council-ratified and has units), or define NN% as the blend50 percentile lead mapped through a published table, and delete the "ABSOLUTE / 95% = no contest" language which the record shows was never met. Whatever is chosen, one coin-flip rule, computed in one place.
- **Owner question** — When you read "72%" on a card, what do you believe it is the probability OF? Your answer determines whether it should be share-of-best (normalized) or a standalone win-probability delta.


---

## MEDIUM — Arena instrument

### F07 · BENCH_WEIGHT=0.15 is falsified by the GP column of the owner's own weekly file, and flipping it changes mock 34's headline finish from 4th to 2nd

`KNOWN-PARTIAL — owner gap #1 / E22` · verdict **PARTIALLY_CONFIRMED** · *measured*

BENCH_WEIGHT=0.15 is load-bearing on the arena's ranked outputs, not only on late-round card ordering: on mock 34 (seeds 11/23/47, 3,000 seasons/seed) raising it to 1.0 moves the owner seat from 9.30% to 16.00% champ and from 4th to 2nd, with room Spearman 0.916; the flip also appears at 0.75. No prior artifact quantified this. But the GP column does not falsify the constant or establish an effective weight >= 1.0: the same file's FGA and FTA columns imply ~0.79 and ~0.94 while GP implies ~1.33, and GP is confounded by the owner's 64 in-season moves on daily unlimited waivers (E16) and by the fixed weekly_availability=0.88 — sim FGA-per-player-game 13.5-14.0 vs a real 12.15 is the signature of streamed low-usage filler. The FT% …

- **Evidence** — Owner's observed player-games per week, 2025-26 regular season (arena/data/weekly_matchups_2025-26.csv, gp column): [32,44,46,43,44,43,46,21,38,41,45,48,43,43,46,45,56,41], mean 42.5, sd 7.1; all 36 team-weeks in the file mean 41.9. The simulator's effective weekly player-games for the 12 mock-34 rosters is 31.3 (range 29.8–32.2) — a 26% volume deficit. Even BENCH_WEIGHT=1.0 yields only ~40.0 (13 x 3.5 x 0.88), i.e. the real effective bench weight is >=1.0, not 0.15. Downstream: sim weekly FGA 438 vs real 525 …
- **Cost** — Every LEDGER champ%, every counterfactual arm, and every ECW figure is conditional on a constant the owner has already judged wrong, and the conditionality is large enough to change a mock's reported …
- **Action** — Treat the bench correction as a re-baseline item alongside E14 (playoff format) rather than only as a card-ordering item (E22): re-derive the four reproducible mocks under a fitted bench weight and dual-report, exactly as league_intel §4 does for the bracket. Fit the weight from the GP column rather than setting it to 1.0 by hand.
- **Owner question** — Should the bench weight be fit to your observed GP (which bakes in your 64 moves), or set to a static-roster value with streaming reported separately under E16?

### F08 · The LEDGER's own audit trail is not in the repo: 21 of 25 result rows, 5 of 5 interior-tally artifacts, and both of the controlled results that motivate E8/E9/E14 are unregenerable

`KNOWN-PARTIAL — lesson 13` · verdict **PARTIALLY_CONFIRMED** · *measured*

Lesson 13 and T7 (`analysis_2026-08-04_self_critique.md:156`) already register both the evidence-landing law and the unreproducible range as "mocks 10-26", with backfill queued for September. What is NOT registered is that the boundary runs past 26: `season_sim_mock27|28.py`, `mock28_cf.py:17` and `format_delta.py:23-27` also read states under the vanished `/root/.claude/uploads/58588377-.../` path, which places LEDGER §5 (the m28 ECW-vs-kept-total oracle pair, 34.58 / 0.28 / 6.50 — the sole cited basis for E8 and E9) and the four format_delta states (mocks 21/25/27/30 — the entire measured basis for E14) inside the unreproducible set while both are quoted as artifact-derived. Only 4 states (mocks 31-34), 5 season_sim out.json and 2 CF …

- **Evidence** — `grep -l 'uploads|scratchpad' arena/mocks/*.py` hits 35 of 42 harnesses; only build_boards.py, mock34_cf.py, room_model.py and season_sim_mock31–34.py are repo-relative. `arena/data/states/` contains exactly 4 states (mocks 31–34). mock28_cf.py:17 STATE='/root/.claude/uploads/58588377-.../4cb343cd-draft_state_17.json' — that is LEDGER §5, the ECW-vs-kept-total oracle pair (34.58 / 0.28 / 6.50) that T1, E8 and E9 all rest on. format_delta.py:22-27 reads four upload-path states — that is league_intel §4, the entire …
- **Cost** — On draft night nothing breaks. But every September ship decision is gated on 'beat the incumbent without regressing m21/m24/m25/m26' — and m21/m24/m25 states are exactly the ones that are not in the …
- **Action** — Before September: either commit the mock 10–30 draft states (they are small JSON) or downgrade every claim resting on them to [UNREPRODUCIBLE] per lesson 13 and rewrite the E8/E9/E9b ship bars against the four states that do exist. Highest priority: mock 28 (LEDGER §5) and the four format_delta states (E14) — those two carry the most downstream weight per byte.
- **Owner question** — Do you still have the mock 10–30 draft_state JSONs anywhere (an old upload, a chat attachment)? If not, the regression baselines have to be re-drafted from scratch and the ledger's history becomes descriptive only.

### F09 · The instrument's honesty rule targets the wrong error source: draft-to-draft sd is 8.4pp, Monte-Carlo sd is 0.22pp — and slot_intel.json, read live on draft day, has 3–5-draft cells and five zero-sample cells printed as 0.0%

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

slot_intel.json's per-(strategy, slot) cells are too noisy to support the best_per_slot line the live-draft prime checklist reads. Measured on 30 independent drafts per configuration: cross-draft sd is 6.89pp (council@S4) and 5.89pp (stars@S7), versus a Monte-Carlo-only sd of 1.05pp per 1500 seasons on a fixed roster -- the draft-realization term dominates by ~6.5x in SE at the operating point, not the ~38x claimed. The committed file was generated at --seasons 1500 --rotations 3 (verified: minimal common denominator 9000 = lcm(1500,3000,4500); specialist S4 = exactly 1 champ/4500), giving 2-3 draws and SE ~4pp per cell. Against that, the top-2 gap in the committed table is under 3pp at 10 of 12 slots (0.9pp at S4), so "best strategy for …

- **Evidence** — Monte-Carlo SE for champ%=9.52%: 0.379pp at N=6,000; 0.268pp at 12,000; 0.219pp at 18,000 — confirmed empirically against the committed mock34_cf_out.json champ_blocks (block sd 0.960 / sqrt(18) = 0.226pp). Cross-draft SE, measured: 7–8 independent drafts with the strategy pinned to a fixed slot, 1,200 seasons each — council@S4 champ% [10.6, 24.2, 13.8, 19.2, 13.2, 1.2, 1.8], sd 8.44pp; stars@S7 [6.8, 0.0, 13.4, 0.0, 13.8, 7.9, 25.1, 11.8], sd 8.21pp. That is ~38x the Monte-Carlo SE. A 5-draft cell therefore …
- **Cost** — On October draft night the prime checklist will hand the owner a 'best strategy for your slot' recommendation whose per-cell noise is roughly half the entire between-slot signal. It is a coin flip …
- **Action** — Either print per-cell n and a confidence interval in cmd_slots (and suppress zero-sample cells rather than printing 0.0), or drop the slot_intel read from the prime checklist and replace it with the cadence intel, which is a drain count and is far better estimated. Also correct the module docstring's rule to name draft variance as the binding term.
- **Owner question** — Do you actually use the best-strategy-per-slot line on draft day, or is cadence intel the part you rely on? If the former, it needs ~50 drafts/cell to mean anything.

### F10 · Weekly model under-disperses all 7 counting cats (1.25–2.07x) and models categories as independent; the real data that proves it is committed but read by zero lines of code

`KNOWN-PARTIAL — N1 / T2 (also league_intel §3)` · verdict **PARTIALLY_CONFIRMED** · *measured*

The weekly model's dispersion is modestly light in a subset of counting categories, and the real weekly data committed on 2026-08-04 is not yet read by any code — but the headline "1.25-2.07x under-dispersion in all 7 cats" and "categories modeled as independent" do not hold. (a) UNREAD DATA — CONFIRMED but expected: `arena/data/weekly_matchups_2025-26.csv` is referenced only by two debrief sentences and its own README. This is already registered as N1/T2 with the fit scheduled for September under the current feature freeze; it is not a new finding. (b) UNDER-DISPERSION — REAL BUT ~1.1-1.65x, NOT 1.25-2.07x, AND ONLY IN 3 OF 7 CATS. The raw-CV comparison conflates two things the arena's outputs are provably insensitive to: (i) week-length …

- **Evidence** — Ratio of real weekly team-total CV to simulator CV (real = owner's 18 regular-season weeks; sim = the 12 mock-34 rosters, arena/data/states/draft_state_mock34.json): 3PTM 1.25x (p=.065), PTS 1.50x (p=.0023), REB 2.07x (p=7e-9), AST 1.60x (p=.0004), ST 1.35x (p=.020), BLK 1.62x (p=.0003), TO 1.60x (p=.0004) — chi-square variance-ratio tests, 17 df, 7/7 in the same direction, 6/7 significant. Conditioned on observed player-games, real per-player-game dispersion k is 1.51–2.31x the sim's CV-only value …
- **Cost** — Every effect size in the LEDGER is inflated by roughly a third. The instrument makes strong rosters look ~35% safer than the real league treats them, which is precisely the anomaly the repo has …
- **Action** — Before the September re-baseline, fit CV, PCT_MIX_INFL and a cross-category correlation term to arena/data/weekly_matchups_2025-26.csv, and re-run the E9/blend50 validation on the refit model (SEPTEMBER-PLAN already makes E9b conditional on 'the refit weekly model if the weekly-record refit has landed' — this makes the refit the gating item, not an option). Add a committed fit script so the constants have …
- **Owner question** — Do you want the weekly constants fit to your own 18 weeks (n=18, one team, includes your streaming), or held back until a second season of weekly scoreboards is transcribed?

### F11 · `arena live` never passes the market board, so the practice room the draft-arena skill prescribes contains zero ADP drafters

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`pick_for` gates its ADP branch on `mkt is not None` (arena/arena.py:242). `run_draft` passes `mkt=mkt` (line 321-322), but BOTH `cmd_live` (line 540) and `run_draft_ordered` (line 564) omit it. `market` is the only `adp=True` persona, so in live practice drafts and in `cmd_cadence` (which generates the committed `arena/results/cadence_intel.json` that draft-arena/SKILL.md prescribes as draft-night intelligence) the ADP seat silently falls through to the generic path and becomes `sum(z) + gauss(0, 4.0)`, also skipping the ADP branch's -50 bench-bound penalty and +15 mid-round positional instinct. The seat is present in ~96% of live casts (11 of 12 non-council names are drawn per draft). The consequence is NOT that the room becomes more …

- **Evidence** — Code path: arena/arena.py:242 `if params.get("adp") and mkt is not None:` vs arena/arena.py:540 `pick_for(params, pool, rosters[slot], ranks, n // TEAMS + 1, rng)` (no mkt kwarg). Verified behaviorally — same persona, same rng seed, first 8 picks: WITH mkt -> Towns, Jokic, SGA, Edwards, Wembanyama, Doncic, Maxey, Harden; WITHOUT mkt -> Towns, Jokic, SGA, Mitchell, Wembanyama, Sexton, Daniels, Edwards. The bench-bound −50 penalty and the 'I still need a center' +15 mid-round instinct (arena.py:244-248) are also …
- **Cost** — Every rep the owner has taken in `arena live` trained him against a room strictly more value-disciplined than the arena cast was designed to be — and the arena cast is already known (league_intel §5) …
- **Action** — One-line fix (`mkt=market_ranks(pool_all)` computed once before the loop, passed at arena.py:540) — but it is an instrument change under the feature freeze, so register it with E17 and re-check whether any live-mode-derived calibration moves. Until then, disclose in the September report that live-mode reps have no ADP seat.
- **Owner question** — Do you want this fixed now as a truth/reporting fix (the freeze allows those) so your remaining practice reps are against a room with at least one real ADP drafter?


---

## MEDIUM — Data layer

### F12 · Six second-year players still carry 'rookie-proj', applying a market-hype premium worth 12-21 draft slots in the 2026-27 market model

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Six 2025-draft-class players (Khaman Maluach, Jeremiah Fears, Egor Demin, Tre Johnson, Cedric Coward, Nique Clifford) still carry the `rookie-proj` note in data/players.csv while entering year 2 for 2026-27. Their rows are byte-identical carry-forwards of arena/data/players_2025-10-21.csv — both the stale tag AND the original rookie stat projections survived the pool refresh; Harper's note was cleared but his line was not. The tag has exactly two consumers (arena/arena.py:189, docs/draft-deck.html:856), both applying the sign-aware `s*1.15 if s>0 else s/1.15` market-hype multiplier. Because all six have negative market z-sums, the division improves their Mkt rank by a measured 12-21 slots (Johnson 145→157, Coward 148→160, Demin 151→168, …

- **Evidence** — data/players.csv lines 72 (Khaman Maluach PHX), 113 (Jeremiah Fears NOP), 114 (Egor Demin BKN), 115 (Tre Johnson WAS), 148 (Cedric Coward MEM), 149 (Nique Clifford SAC) — all `rookie-proj`. Measured market-rank effect (ran arena.market_ranks on the live 246 pool with ARENA_DATA pointed at data/players.csv, current notes vs the same rows with the stale tag cleared): Tre Johnson Mkt 147→159 (−12), Cedric Coward 150→162 (−12), Egor Demin 153→170 (−17), Jeremiah Fears 160→181 (−21), Nique Clifford 165→182 (−17), …
- **Cost** — The deck's Mkt column is the slide/reach signal ('a player available well past Mkt is a room-wide slide' — docs/draft-deck.html:350) and feeds the survival/chip logic. Six players are being shown as …
- **Action** — Clear `rookie-proj` from those six rows (that alone removes the premium), and add a mechanical guard so the tag cannot survive a draft cycle: a check in validate_pool that fails the stamp if any `rookie-proj` row predates the most recent June draft. Add a `draft_year` column so class is data, not a note substring. Re-audit MKT_PIN: decide explicitly whether Harper's 60 is a year-2-leap pin (like Flagg's documented …
- **Owner question** — For the 2025 class specifically — do you want them treated as ordinary year-2 players (no premium) or do you want a separate, explicitly-named 'sophomore leap' pin distinct from rookie hype?

### F13 · Team shot budgets are violated by up to 42% — per-player lines were never reconciled against the fixed ~89 FGA a real NBA team has to give

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Per-team projection totals are never reconciled against any aggregate budget, and the error is concentrated in the deep tail of crowded rosters — not league-wide. Each additional row a team gets in the pool carries 9.30 FGA (OLS across 30 teams: sum = 20.6 + 9.30·n), while a real team's 9th-11th men take ~5/4/3.5. The pool's within-team FGA profile is well calibrated through rank 6 (cumulative 78.7) and inflates past rank 7 (8.7/8.5/7.6/6.8/6.5). The correct comparator is NOT a team's ~89 FGA/game: per-game averages are conditional on playing, so a partial roster's averages must sum higher. Real top-8 per-game FGA sums run 90-95 (BOS 94.5, DEN 90.9, GSW 90.6) against the pool's 95.8, so the LEAGUE MEAN (94.1 from 7.9 rows, 90.2 …

- **Evidence** — Script summing data/players.csv by team: `WAS 10 rows: 126.5 FGA, 158.5 PTS, 57.0 REB`; `MIL 11: 125.4 FGA, 158.3 PTS`; `HOU 11: 121.8 FGA, 158.6 PTS, 68.7 REB`; `ATL 10: 110.0 FGA`; league mean across 30 teams `94.1 FGA / 122.9 PTS / 44.1 REB` from 237 non-FA rows (7.9 per team). Concrete instance — Houston: Durant 16.8 + Sengun 16.0 + Amen Thompson 12.5 + VanVleet 12.5 + Sheppard 12.5 + Jabari Smith 11.5 + Bogdanovic 10.5 + Eason 10.0 + Smart 9.0 + Capela 6.0 + Adams 4.5. Reed Sheppard is projected for the same …
- **Cost** — Systematic over-ranking of the second and third tier on crowded rosters, and it is concentrated in the exact players who fill rounds 6-13 — Sheppard, Jabari Smith, Eason, Bogdanovic, Tre Johnson, Bub …
- **Action** — Add a `min` (projected minutes) column and a mechanical team-budget check that fails the pool if any team's summed FGA exceeds ~92 or summed minutes exceed 240. That single check turns this from invisible to blocking, and minutes is also the input a games-played model needs. Then do one October pass reconciling the worst offenders (WAS, MIL, HOU, ATL, PHI, ORL, POR, LAL, NOP all exceed 107 FGA) — the fix is …
- **Owner question** — Do you want me to build the team-budget check as a blocking gate in validate_pool (fails the stamp), or as an advisory report you review during the October pass?

### F14 · The June-2025 draft class never had its rookie season ingested — 9 rows are byte-identical to the pre-debut October-2025 snapshot

`NEW — T4/N3 (partial: they register 'hand-authored, no variance', not 'frozen across a …` · verdict **PARTIALLY_CONFIRMED** · *measured*

The arena's frozen "opening-night" board is not a no-hindsight reconstruction — it is a backdated copy of the post-season 2026-27 pool. arena/data/players_2025-10-21.csv was created 2026-07-12 (commit a59fb96) from the data/players.csv rebuilt one day earlier, which its own commit message describes as "2025-26 production, July 2026 rosters." At creation the snapshot was 211/219 (96%) byte-identical to that live pool and contained zero rows not already in it; only ~8 rows were hand-dampened (Wembanyama 26.5→24.5 pts, Flagg 17.8→16.5, Knueppel). arena/README.md:8-15 nonetheless guarantees the board was "reconstructed with no hindsight" with "entering-season projections (2024-25 production, hindsight breakouts dampened — see STAT_ADJ in the …

- **Evidence** — Script over data/players.csv vs arena/data/players_2025-10-21.csv comparing ['fg_pct','fga','ft_pct','fta','tpm','pts','reb','ast','stl','blk','tov']: `Dylan Harper yes True`, `VJ Edgecombe yes True`, `Ace Bailey yes True`, `Khaman Maluach yes True`, `Jeremiah Fears yes True`, `Egor Demin yes True`, `Tre Johnson yes True`, `Cedric Coward yes True`, `Nique Clifford yes True`. Pool-wide: `snapshot rows 220; shared with live 218; byte-identical statline 183 (84%)`. Only Flagg (pts 16.5→17.8, ast 3.5→4.2) and Knueppel …
- **Cost** — Every 2025-class player is priced on a guess made before he played a game, in the year the market prices him on a real season of tape. These are exactly the round 9-13 names the owner will be …
- **Action** — Before October: re-source per-game 2025-26 lines for the entire 2025 draft class from an actual box-score source and overwrite those nine rows; then re-derive, don't reuse, the arena snapshot with a committed generator so 'no hindsight' is reproducible. Separately, sample 20 non-rookie rows against a real source — if the 84% identity holds for veterans too, the whole pool needs a season re-ingest, not a patch. Add a …
- **Owner question** — Which projection source do you want as the October re-ingest baseline (Hashtag / BBM / Yahoo's own preseason page)? And do you want the arena re-baselined on a clean snapshot, or are you content to treat the existing LEDGER as historical …

### F15 · The published deck's JUDGMENT layer is outside every build gate — and already contradicts the pool it shipped with (Sochan)

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md §1d makes re-authoring the deck's JUDGMENT layer part of the publish gate, but build_deck.py enforces nothing about it: its three gates (roster verification, freshness, MUST_HAVE) and its injection/round-trip checks cover PLAYERS, BUILD_PULL, BUILD_NOTE and the footer date only. The 22 hand-written per-player entries ride along unchecked, and the block's own `date: "2026-07-28"` sits 8 days behind BUILD_PULL "2026-08-05" in the shipped file while no code ever reads it. One entry has already drifted inside a single certified build: the 2026-08-05 deck's JUDGMENT calls Jeremy Sochan "Unsigned after a limited NYK title-run role" while the same file's baked pool row says POR / "camp-deal non-gtd (agreed 8/1)" and the same file's Data …

- **Evidence** — docs/draft-deck.html:1219 → `"Jeremy Sochan": { adj: -0.15, why: "Unsigned after a limited NYK title-run role." }`. data/players.csv:202 → `Jeremy Sochan,POR,PF,0.535,9.5,0.720,2.8,0.5,12.0,6.8,3.2,1.1,0.6,1.9,camp-deal non-gtd (agreed 8/1)`. docs/draft-deck.html:403 (Data paragraph) → 'This refresh (8/3): Jeremy Sochan signs with Portland — one year at the veteran minimum, non-guaranteed, a camp deal (reported 8/1), so he moves FA→POR'. Deck build manifest (docs/draft-deck.html:1) → `{"built": "2026-08-05", ...}` …
- **Cost** — This is LESSONS #11's failure shape ('a published artifact whose content trails the data is a live defect') recurring one layer down, inside a build the pipeline certified. On draft night the owner …
- **Action** — Add gate 4 to build_deck.py: every JUDGMENT key must exist in the pool, and any entry whose text contains 'unsigned' must correspond to a row with team == 'FA' (and vice versa for the FA rows). Stamp each entry with an `as_of` date and have the deck grey out any entry older than the current BUILD_PULL. Fix the Sochan entry now — it is wrong in the artifact the owner will open.
- **Owner question** — Should a JUDGMENT entry older than N days block the build outright, or just render with a visible staleness badge on the card?

### F16 · availability() note parsing: a season-ending injury written in plain English scores at FULL value, and 'recovery' anywhere in a note silently deletes a player from every board

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`availability()` (scripts/hoops.py:304-311) resolves the free-text `note` column with three unordered substring tests — `startswith("out-")`, then `"recovery" in note`, then `"risk" in note` — with no validator anywhere in the repo (`validate_pool` checks only MUST_HAVE names; verify_rosters.py never reads `note`; evals/ and the repo contain no tests). Two latent failure modes, currently unexercised: (a) the season-ending tier keys on a leading `out-` token only, so any other phrasing scores 1.0 — the live instance is Jalen Brunson's `wrist-surgery-monitor`, which carries injury information and receives no haircut at all; (b) `"recovery"` is tested before `"risk"` and matches anywhere in the string, so a parenthetical such as …

- **Evidence** — Ran hoops.availability() directly on candidate note strings — `'ACL tear, out for season' → 1.0`; `'out for the season (achilles)' → 1.0`; `'out-achilles' → 0.0`; `'inj-achilles-risk (first season back)' → 0.78`; `'inj-achilles-risk (recovery on track)' → 0.0`; `'returned from recovery, cleared to play' → 0.0`; `'low-risk minutes cap' → 0.78`; `'no risk of missing camp' → 0.78`. Code: scripts/hoops.py:304-310. Silent-drop site: scripts/hoops.py:437. There are 29 distinct note values in the file and no controlled …
- **Cost** — On the highest-stakes day of the year, a single natural-language note written under time pressure either hands the owner a season-ended player at full value in round 2, or silently deletes …
- **Action** — Replace free-text parsing with a validated `status` column (one of: ok / risk / recovery / out) plus a free-text `note` for humans, and make validate_pool reject any unrecognized status — that alone kills both failure modes. Minimum viable version if the schema is frozen: match `out-` OR a leading token check, evaluate `risk` before `recovery`, require the recovery token to be a suffix of the leading tag …
- **Owner question** — Schema change (`status` column) or hardened parsing on the existing note column? The schema change is the real fix but touches hoops.py, build_deck.py, arena.py and the deck's baked rows, which is a feature-freeze question.


---

## MEDIUM — Draft Deck

### F17 · Build-coherence strip reads "⚠ WRONG TARGETS" in 79% of punted states; its Retarget button implements the tautology "punt your worst category"

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The build-coherence strip's "compare against every single-swap alternative" is a degenerate search: because `keptSum` is a raw z-sum over kept categories (docs/draft-deck.html:438-442, 1760-1770), its argmax is algebraically identical to "punt whichever category your roster's raw z-sum is lowest in". This makes the strip rank-blind — it never compares your roster to the field, unlike `puntPath`, the drift read, and every other punt surface in the same file. Two consequences reproduce independently: (a) the suggested replacement is TO in 40.7% of single-punt states (TO is the roster argmin in 43.9% of 132 market-order rosters) because elite high-usage players carry systematically negative TO z, so the strip has a standing structural bias …

- **Evidence** — docs/draft-deck.html:1760-1775 — `keptSum`, the single-swap loop `if (!best || v > best.v) best = {...}` (1770), `const state = delta > 2 ? "inverted" : delta > 0.75 ? "drifting" : "aligned"` (1773). Node harness over the extracted engine block, 1440 states: `{ 'ON TARGET': 183, 'OFF TARGET': 116, 'WRONG TARGETS': 1141 }`. Per-round trace, slot 4, punt FT%: roster 3 → delta 7.20 (suggests "punt TO instead"); rosters 7-13 → delta 8.2-11.6, all suggesting "punt BLK instead". `puntPath` (line 488) is referenced only …
- **Cost** — An alarm that fires 79% of the time is noise, and this one fires in the loudest state the strip has. Under 45 seconds the owner either learns to ignore it — losing the genuine mock-32 inversion case …
- **Action** — Two display-only fixes, both allowed under the freeze: (1) normalize the delta by roster size (per-player z, or percent of kept-total) before applying thresholds, and re-fit the two cutoffs against the punted mocks (22/31/32/34) per E21; (2) gate the Retarget button behind `puntPath(...).clear`, matching the pivot button in `renderPuntAnalyzer`. Until then, consider suppressing the strip — 79% false-alarm is worse …
- **Owner question** — You approved this strip three days ago after mock 32 — has it ever shown you "ON TARGET"? If not, that's the symptom, and I'd rather re-fit the thresholds than have you learn to ignore the box.

### F18 · Colophon describes a mock room the deck no longer runs, and states the star-fall property backwards vs the measured E18/N2 result

`NEW` · verdict **CONFIRMED** · *measured*

The Logic colophon (docs/draft-deck.html:404) tells the owner "Mock opponents are 9 value-drafters + 2 market seats, so discounted vets leave mock boards early and stars fall further than real rooms." Both halves are wrong as shipped. (1) Since E18 (2026-08-04) every newly started mock seats the 11 named league-mates: deck.state.cast is set unconditionally from Object.keys(MANAGERS) at :1352-1369 and advanceAI routes through managerScores at :1430-1432, leaving MOCK_CAST reachable only for drafts saved before E18 (:1402-1404 comment). The deck's own mode button (:266) and start log (:1374) already say "11 league-mates", so the colophon contradicts the shipped UI; the drift is material, since mean adp_w across MANAGERS is 0.518 versus the …

- **Evidence** — docs/draft-deck.html:404 (colophon Logic paragraph, verbatim sentence). Shipped behaviour: :1352-1372 seats `Object.keys(MANAGERS)` shuffled per draft into `deck.state.cast`; :1417-1436 `advanceAI` calls `managerScores(name, …)` when `MANAGERS[name]` exists; :1404 comment on `mockCastFor` — "legacy: drafts saved before the named room (E18) keep the old cast". Contradicting measurement: arena/results/analysis_2026-08-04_self_critique_round2.md N2 ("The market geometry is 0.45× reality … the real room produced …
- **Cost** — The owner practises against the deck's mock mode and calibrates his real-draft instincts on it. A stale, backwards sentence teaches him to expect mocks to over-state falls when they under-state them …
- **Action** — Rewrite the sentence to describe the named room and state the measured direction and its asterisk: mock opponents are the 11 named league-mates (profiles.json, three seasons), and the synthetic market carries ~0.45× the real board's divergence, so expect REAL rooms to produce deeper star falls than mocks until October ADP lands. Display-only, allowed under the freeze.

### F19 · Judgment layer is 11 days stale, contradicts the deck's own colophon and players.csv, and no build gate checks it

`KNOWN-PARTIAL — T7 ("judgment layer is staleness-prone by design")` · verdict **PARTIALLY_CONFIRMED** · *measured*

The deck's `JUDGMENT` layer is dated 2026-07-28 and is byte-identical across every deck commit in repo history (7/31 through 8/5): it has not been re-authored across 4 stamped data pulls and ~11 deck republishes, despite SKILL.md §1d requiring re-authoring in the same pass as each republish. scripts/build_deck.py has no gate on it (zero JUDGMENT references anywhere in scripts/ or arena/), and `JUDGMENT.date` is never rendered in the page, so divergence is invisible without reading source. The live consequence today is ONE contradicted entry of 22: Jeremy Sochan is still described as "Unsigned after a limited NYK title-run role" while players.csv has him at POR ("camp-deal non-gtd (agreed 8/1)") and the colophon announces the FA→POR move — …

- **Evidence** — docs/draft-deck.html:1193 `date: "2026-07-28"`; :1240 `const BUILD_PULL = "2026-08-05"`; :1219 Sochan "Unsigned after a limited NYK title-run role"; :1224 Mathurin "RFA frozen by the Kawhi investigation"; :402 colophon "This refresh (8/3): Jeremy Sochan signs with Portland". data/players.csv: `Jeremy Sochan,POR,…,camp-deal non-gtd (agreed 8/1)` and `Bennedict Mathurin,LAC,…,` (verified by cross-joining all 22 judgment keys against the CSV: 22/22 in pool, 2 contradicted, 0 orphans). `git log --oneline -- …
- **Cost** — The judgment layer is the deck's only channel for "directional-but-uncertain reads" per owner law 1e. Two of its 22 entries currently assert facts the same page contradicts one screen lower. In …
- **Action** — Add a fail-closed gate to build_deck.py: refuse the build unless `JUDGMENT.date == fresh["date"]` (the same fail-closed treatment BUILD_PULL already gets, with the same post-write verification). Surface `JUDGMENT.date` in the header stamp beside the pool date so a divergence is visible without reading source. Clear the Sochan and Mathurin entries in the next pass.
- **Owner question** — Should a stale judgment date HARD-FAIL the build (my recommendation, matching how you treat stale roster verification), or warn and stamp the header "judgment N days behind pool"?

### F20 · On pick #1 from slot 1 the card's headline number is off-scale by ~50×: it renders "lead +57.2 🚀" and a tooltip reading "ΔECW-blend 1100.3 … as pool percentiles"

`NEW` · verdict **CONFIRMED** · *measured*

On the empty board, `decwScores` (docs/draft-deck.html:1053-1054) returns raw `adjValue` as `ds`, while every downstream consumer assumes the [0,1] percentile scale the non-empty branch produces via `pctRanks`. Verified by running the shipped engine: `decwScores(PLAYERS, [], [])` gives Wembanyama 11.0025 / Jokic 10.4308, so the row-1 chip renders "lead +57.2 🚀" and the tooltip reads "ΔECW-blend 1100.3 … both as pool percentiles" — a value 11× above the top of its own declared 0-100 scale. The standout threshold (0.035) fires unconditionally and the coin-flip threshold (0.011) can never fire, since both were rate-matched to blend units. Scope is BROADER than the original finding states: `renderDecision` has no empty-board gate, `deck.state` …

- **Evidence** — docs/draft-deck.html:1053-1055 — `const opp = oppRosters.filter(r => r.length)…; if (!opp.length) return vals.map((v,i) => ({p: pool[i], ds: v}));`. Display: :2411-2416 `lead = (scored[0].ds - scored[1].ds) * 100`, tooltip `\`ΔECW-blend ${(scored[i].ds*100).toFixed(1)} — … both as pool percentiles\``. Thresholds :2347 (`<= 0.011`) and :2357 (`>= 0.035`). Node run of `decwScores(pool, [], [])`: Wembanyama ds 11.0025, Jokic 10.4308 → chip "lead +57.2", tooltip "blend 1100.3", standout=true, coinFlip=false. Contrast: …
- **Cost** — Small blast radius (one turn, and the #1 overall pick is not a close call) but it is a live units error on the deck's single most prominent number, and it disables the coin-flip/standout calibration …
- **Action** — At the empty-board fallback, percentile-rank the adjValue vector before returning (`pctRanks(vals)`), so `ds` is on the same [0,1] scale at every turn. One line, display-consistent, no ordering change (percentile rank is monotone in adjValue). Re-run the render gauntlet.

### F21 · The weekly model's percentage-category variance is refuted by the owner's own weekly data now committed in the repo; recalibrating flips the card's #1 at 10% of turns

`KNOWN-PARTIAL — N1 (ECW validated at season grain, never weekly)` · verdict **PARTIALLY_CONFIRMED** · *measured*

The weekly model's percentage-category sigma as built is too large relative to the owner's newly committed weekly data, but the cause is mostly the already-known bench-weight defect, not PCT_MIX_INFL. E3 (registered 2026-07-30) already names the PCT_MIX_INFL re-estimate; what is new here is the first measurement against real weeks. MEASURED (arena/data/weekly_matchups_2025-26.csv, David rows, independently re-derived; the file's 22/22 reconciliation claim verified): at the owner's real weekly volume, FG% is well calibrated — implied inflation 1.08-1.11 against PCT_MIX_INFL=1.15, chi-square p=0.40-0.46, no evidence of misspecification. FT% is directionally lower than 1.15 — point estimate 0.86-0.94 depending on whether week 8 is dropped or …

- **Evidence** — Observed (arena/data/weekly_matchups_2025-26.csv, David rows, weeks 1-18 excluding wk8 [gp 21] and wk17 [2-week All-Star span], n=16): FG% mean 0.4836 sd 0.0240 at 533 FGA/wk; FT% mean 0.8358 sd 0.0267 at 145 FTA/wk. Binomial floors sqrt(p(1-p)/att): FG% 0.0216 → implied infl 1.109; FT% 0.0308 → implied infl 0.865. Model (arena.team_week_model / docs/draft-deck.html:1007-1030, snake-drafted 13-man rosters from data/players.csv): FT% sd 0.0455 / 0.0410 / 0.0501 for teams 1/6/12; FG% sd 0.0282-0.0292. Chi-square …
- **Cost** — Half of the shipped ordering rides on a variance model that the owner's own league data rejects for FT%, and correcting it moves the top recommendation at one turn in ten. Every ECW number in the …
- **Action** — This is a measure-only study, allowed under the freeze: fit DECW_CV, PCT_MIX_INFL (per-category, not shared) and the attempt-volume scale to `weekly_matchups_2025-26.csv`, then re-run the E9 blend50 validation on the refit model before September. Register it as the N1 close-out with its own ship bar. Caveat to carry: n=16 team-weeks from one team; the FT% CI on sd is [0.017, 0.036], which excludes the model but is …
- **Owner question** — Do you have (or can you screenshot) weekly scoreboards from a second season? n=16 from one team is enough to reject the FT% constant but not enough to fit nine of them well.

### F22 · Typo matching is dead for all 12 "Jr./suffix" players — and "jacksn" silently logs GG Jackson instead of Jaren Jackson Jr.

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The fuzzy-typo branch keys on the last whitespace token (docs/draft-deck.html:676, scripts/hoops.py:370), which is the suffix for the pool's 14 suffixed players (12 "Jr", plus Dereck Lively II and Trey Murphy III), so typo tolerance is dead for all of them in both the deck and the CLI. Verified in both engines against the live 246-row pool. Consequences split: (a) for 11 of the 14, a fuzzy typo (porrter, carterr, smiith, jaquezz, oubrre, trentt, livley, murphey...) returns NO MATCH and lands in the UNKNOWN quarantine — which is the system's designed countermeasure and it works: a per-pick warn line plus a persistent `unknownCount` banner on every rank consumer (deck:478, 1821, 2121, 2807) tells the owner ranks exclude it and how to fix it. …

- **Evidence** — docs/draft-deck.html:676 `const last = parts[parts.length - 1];` (fuzzy branch of matchCandidates, 662-681); scripts/hoops.py:370 `last = p["player"].lower().replace(".", "").split()[-1]`. Node run against the extracted engine: `"jacksn" -> GG Jackson`; `"porrter" -> NO MATCH`; `"carterr" -> NO MATCH`; `"smiith" -> NO MATCH`; `"jaquezz" -> NO MATCH`. Python run of `hoops.match_candidates` reproduces exactly: `jacksn -> ['GG Jackson']`, `porrter -> NO MATCH`. Surname census of the live pool: the "jr" bucket holds …
- **Cost** — Mis-logged picks are the documented #1 live-draft failure mode (lesson 1 cost two undos and two fixes mid-draft). This one is silent: no warning, no halt, no UNKNOWN. A single fast-typed "jacksn" or …
- **Action** — Strip a trailing `jr|sr|ii|iii|iv` token before taking the surname, in BOTH docs/draft-deck.html:676 and scripts/hoops.py:370 (truth/robustness fix, allowed under the freeze), and re-run the 130-state gauntlet. Regenerate the feed hint's ambiguous-surname list mechanically from the pool at build time instead of hand-listing five names.
- **Owner question** — On draft night do you type surname-only for speed? If so I'd also add a "one candidate but fuzzy-matched" warning line, so a silent single-match never passes without you seeing the name it chose.


---

## MEDIUM — Fantasy-domain semantics

### F23 · BENCH_WEIGHT=0.15 is 5.7x too low: the real weight is ~0.85-1.0, and the repo's own Yahoo data proves it

`KNOWN-PARTIAL — E22 (+ owner-reported 2026-08-08)` · verdict **PARTIALLY_CONFIRMED** · *measured*

BENCH_WEIGHT=0.15 (arena/arena.py:52, docs/draft-deck.html:830) is far too low for a DAILY-lineup league, and the error is large enough to matter: flipping it 0.15->0.85 changes 461/1872 arena picks (24.6%), 243/432 rounds-11-13 picks (56.2%), moves team_week_model PTS mu from 563.9 to 663.1 against a best-to-worst spread of 207.0, and reorders the 12-team PTS ranking in 12/12 test drafts, so it is not a common-mode shift. But the finding's magnitude and prescription do not survive checking. (a) The correct constant is NOT 0.85-1.0: team_week_model already multiplies every player by g = 3.5*availability, so BENCH_WEIGHT must carry only the slot-competition loss, which I measure at 0.971 for ranks 11-13 versus 0.998 for ranks 1-10 (relative …

- **Evidence** — (1) Simulation on 144 rosters the SYSTEM ITSELF drafts (arena.run_draft, 165 days, realistic NBA slate at 44.7% team game-days), /tmp/bench_sim2.py: start-share by roster rank #11 0.887, #12 0.851, #13 0.817; ranks 11-13 mean = 0.852; whole-roster games-used 0.969. (2) REAL DATA already in this repo — arena/data/weekly_matchups_2025-26.csv, the owner's Yahoo `gp` column, 32 clean regular-season team-weeks (excl. wk1 partial, wk17 All-Star double): GP mean 41.75, sd 5.94, range 21-48. Model-implied weekly …
- **Cost** — Every artifact that touches a full 13-man roster is wrong: teamWeekModel mu is ~18% low and the shortfall is concentrated entirely in the last 3 picks, so ΔECW (deck decwScores, hoops-side blend50) …
- **Action** — Do not hand-tune 0.15 upward. Replace the scalar with a measured start-share: (a) re-derive per-roster-rank weights from a daily-lineup fill (the /tmp harness is 60 lines and reproduces the observed 41.75 GP), or (b) as an interim, set BENCH_WEIGHT=0.85 and re-baseline. Because this moves 25% of all picks it invalidates ledger comparability — it belongs in the September E14 re-baseline alongside the bracket change, …

### F24 · Games-per-week is not modelled anywhere; players.csv has no games or minutes column at all

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Games are modelled coarsely and are unfit, not absent. Weekly games enter as g = 3.5 * weekly_availability(p) with a 3-tier per-player multiplier (0.88/0.75/0.60), plus a games-count variance term g_var = 3.5*a*(1-a) and a per-team-week shared games shock TEAM_WEEK_SHOCK = 0.06 (arena.py:71,332-358,384-386; draft-deck.html:1001-1016). Durability is likewise priced on the board, by hand-tagged injury note (hoops.py availability(): 0.78 for risk, exclusion for recovery, explicitly calibrated against real 2025-26 games played) rather than by a projected-games column. Three specific gaps remain: (1) SCHEMA — data/players.csv (verified: 14 columns, no gp/games/minutes) and hoops.py load_players (lines 215-217) carry no per-player projected …

- **Evidence** — Schema: `head -1 data/players.csv` → 14 columns, none of them games or minutes. `grep -c 'schedule\|games per week\|back-to-back' docs/draft-deck.html` → 1 (a prose mention). Magnitude, from the owner's real weekly data (arena/data/weekly_matchups_2025-26.csv, 32 clean team-weeks): corr(gp, pts)=+0.744 (r2=0.55), gp-vs-reb +0.676 (r2=0.46), ast +0.727 (0.53), tpm +0.726 (0.53), stl +0.621 (0.39), blk +0.569 (0.32), tov +0.576 (0.33), fga +0.754 (0.57). Dividing each week's totals by that week's gp collapses the …
- **Cost** — Three separate costs. (1) Valuation: per-game z is the only currency, so the board cannot distinguish durability, and it cannot express the 4-game-week / light-week effect that, with daily lineups …
- **Action** — Add a `gp` (projected games) column to players.csv in the September multi-source synthesis (Q14 already authorizes re-deriving the projection set — this is the moment to widen the schema), and make the weekly model consume per-player games rather than the 3.5 constant. Separately, decide whether the October build ingests the published NBA schedule to score weeks 19-21 density per player; that is a scope call, but …
- **Owner question** — Do you want the October board to carry a weeks-19-21 schedule-density column (i.e. price the fantasy playoff weeks explicitly), or keep the draft schedule-blind and handle it with in-season streaming?

### F25 · Six of the 2025 draft class are still tagged `rookie-proj` for 2026-27, and nothing in the refresh law ever retires a rookie tag

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The MUST_HAVE pool-completeness law (SKILL.md:14, hoops.py:124-135) is append-only: it forces each June class INTO the pool but never retires the prior class or requires re-projection off its real season. The visible consequence is that nine of the eleven 2025-class rows in data/players.csv still carry their byte-identical October-2025 pre-season projection lines — only Flagg and Knueppel were ever re-projected. Six of those nine still carry `rookie-proj` (Maluach, Fears, Demin, Tre Johnson, Coward, Clifford); on those the tag is ACCURATE, and its only real cost is the x1.15 market-hype multiplier (arena.py:190-191, deck:855) still firing on second-year players — worth +12 to +21 estimated-ADP places, 52 of 241 rows moving, total |shift| …

- **Evidence** — players.csv line numbers above; `grep -c rookie data/players.csv` → 14 rows, of which 6 are 2025 draftees and 8 are 2026 draftees. Downstream magnitude, measured by clearing the note on those six and re-running arena.market_ranks: Tre Johnson 145→157 (+12), Cedric Coward 148→160 (+12), Egor Demin 151→168 (+17), Jeremiah Fears 158→179 (+21), Nique Clifford 163→180 (+17), Khaman Maluach 220→235 (+15); 52 of 241 estimated ADPs move, total |rank shift| 188. The system already knows better in one place and not the …
- **Cost** — Two costs. The smaller one is ADP: six names get a phantom 12-21 pick hype boost in exactly the rank-145-to-220 band where the owner's rounds 12-13 picks and the BUY-NOW/survival chips operate. The …
- **Action** — Two fixes, both cheap and both inside the freeze's 'truth fix' allowance. (1) Data: clear `rookie-proj` from the six 2025 draftees and re-project their lines from actual 2025-26 production during the September synthesis; drop Dylan Harper out of the rookie-hype MKT_PIN grouping or re-comment it honestly. (2) Law: make the MUST_HAVE rule in SKILL.md symmetric — every June class added must also retire the prior …


---

## MEDIUM — Python engine (hoops.py)

### F26 · Availability never reaches any category total: trade says you WIN by acquiring a player the engine values at +0.00

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`availability()` gates rankings and board membership but never enters any category-summing code path. `cmd_trade` (hoops.py:449-465) sums raw `p["z"][cat]` with no availability term, so Jimmy Butler — availability 0.00, excluded from every board, printed as "val +0.00*" by `find` — trades at his full raw +2.77, and `trade --send "Derrick White" --get "Jimmy Butler"` reports "net value: +0.57 (you win on raw value)". SKILL.md's recovery-exclusion rule is scoped to draft candidates only and its trade guidance (line 47) never mentions availability, so nothing in the judgment layer catches this. `print_profile` (411) additionally prints a season-out player's full category line while suppressing the injury note that `fmt_row` displays. …

- **Evidence** — $ python3 scripts/hoops.py trade --send "Derrick White" --get "Jimmy Butler" net value: +0.57 (you win on raw value; ...) $ python3 scripts/hoops.py rank --top 200 | grep -i butler → (no output — excluded from every board) $ python3 scripts/hoops.py find "Butler" Jimmy Butler GSW SF val +0.00* ... [acl-recovery-jan26 (return ~2027)] Roster-total leg, live draft state (slot 1, my only pick = Anthony Davis, board value +4.29): $ python3 scripts/hoops.py draft status Your build — 1 players; category z totals FG% …
- **Cost** — Trade is a decision surface the owner uses in-season, and it currently recommends acquiring exactly the players the injury rule was written to exclude (LESSONS.md lesson 6 — the …
- **Action** — Give `cmd_trade` an availability-aware net (or at minimum refuse/flag a trade involving an availability==0 player with the same language the board uses), and add an availability-weighted variant of `roster_totals` for the vs-field/matrix/status surfaces — or, if raw totals are deliberate, label them 'raw, not injury-adjusted' everywhere they print.
- **Owner question** — Should category totals be availability-weighted (an injured star contributes 78% of his z to your projected category standing), or is the current raw total the intended 'if healthy' reading?

### F27 · No Unicode normalization: Jokić, Dončić, Şengün, Porziņģis all fail to match and become UNKNOWN

`NEW` · verdict **CONFIRMED** · *measured*

No Unicode normalization anywhere on the name-matching path: Jokić, Dončić, Şengün, Porziņģis all fail to match and become UNKNOWN — in BOTH the engine and the published draft deck. `match_candidates` (hoops.py:352-375) compares raw lowercased strings with no NFKD/ASCII folding, and docs/draft-deck.html:663-679 is a line-for-line JS port with the same defect. Both pools are 100% ASCII (246 rows each), so any feed carrying the diacritics that Yahoo, ESPN and NBA.com render fails the exact, word, and substring stages. The fuzzy fallback cannot rescue it: it is surname-only and compares the FULL query against the surname ("nikola jokić" vs "jokic" = 0.471), and it gates on q[:1] == last[:1], which a leading diacritic ('Ş' vs 's') fails by …

- **Evidence** — $ python3 scripts/hoops.py draft turn "Nikola Jokić; Luka Dončić; De'Aaron Fox" --top 1 ✓ #3 R1: De'Aaron Fox → T3 ⚠ #1 logged as UNKNOWN ('Nikola Jokić': no match) — fix with: draft fix 1 "Name" ⚠ #2 logged as UNKNOWN ('Luka Dončić': no match) — fix with: draft fix 2 "Name" $ python3 scripts/hoops.py draft turn "Jokić; Dončić; Şengün" --top 1 ✓ #1 R1: Nikola Jokic → T1 ⚠ #2 logged as UNKNOWN ('Dončić': no match) ⚠ #3 logged as UNKNOWN ('Şengün': no match) Swept against the live pool: 8 of 8 accented FULL names …
- **Cost** — Any pick copy-pasted out of the Yahoo draft room chat, or typed by anyone who spells these names correctly, quarantines a first-round player as UNKNOWN — which then triggers the …
- **Action** — ASCII-fold both sides before matching: `unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()` applied to the query and to `p['player']` at the top of `match_candidates`. Zero risk to existing ASCII behaviour and it fixes the first-letter guard in the fuzzy stage too.

### F28 · The 0.78 injury haircut switches off entirely below replacement level — from board rank 62 down, injury risk is free

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`adj_value` (hoops.py:318, mirrored as `adjValue` at docs/draft-deck.html:445) applies the 0.78 risk haircut only when total_value > 0. Because z-sums are centred on the top-156 draftable pool, board value crosses zero at rank 62, so from there down the multiplier is a no-op: 15 risk-flagged players inside the 156-player draftable universe (Dejounte Murray 67, VanVleet 70, Paul George 72, LeBron 73, Embiid 78, Mark Williams 80, Edey 92, Keegan Murray 103, Sarr 108, Zion 109, Lonzo 119, Beal 127, Lively 131, M. Robinson 133, Melton 139) receive adj_value == total_value exactly. The defect is real but narrow: it is an incomplete propagation of a fix the repo already made. draft-deck.html:857 carries the comment "sign-aware (2026-07-30): …

- **Evidence** — $ python3 scripts/hoops.py rank --top 130 (excerpt) 5. Anthony Davis WAS PF,C val +4.29* [inj-risk] 32. Kawhi Leonard LAC SF val +1.72* [inj-risk; ...] 67. Dejounte Murray NOP PG val -0.14 [inj-achilles-risk (14 games last season)] 72. Paul George BOS SF,PF val -0.21 [inj-risk] 78. Joel Embiid PHI C val -0.37 [inj-risk] 109. Zion Williamson NOP PF val -1.59 [inj-risk] Note the `*` present at ranks 5 and 32 and absent from rank 67 onward. Computed over the live pool: first board rank with total_value <= 0 is 62 of …
- **Cost** — Rounds 6-13 are where the owner chooses between a healthy bench piece and an injury-flagged upside swing — and in a DAILY-lineup league with unlimited moves, that bench piece plays most days, so the …
- **Action** — Decide the intended semantics and make them explicit. If the goal is only "never let the multiplier turn a negative into a better number," then apply the haircut as a penalty on the distance from replacement rather than a multiplier on a signed sum (e.g. `av*tv - (1-av)*PENALTY`), or shift the value scale so it is non-negative over the draftable pool before multiplying. Separately, make the `*` marker key on …
- **Owner question** — Below replacement level, do you want an injury-risk player priced WORSE than an equivalent healthy player (a real penalty), or merely not better? The current code does neither — it prices them identically.

### F29 · UNKNOWN placeholders silently corrupt roster count, remaining-picks arithmetic, the feasibility guard, and every category rank for the rest of the draft

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

When one of the OWNER'S OWN picks is logged as an UNKNOWN placeholder, `build_rosters` (hoops.py:530) drops it, and every roster-derived number silently under-counts for the rest of the draft: the card's `roster N/size` (hoops.py:825), `draft status` / `rosters` / `matrix`, the weakest-category annotation, and the vs-field ranks (hoops.py:540-547). Verified: 7 real picks, card says "roster 3/13", status says "Your roster (3)", and FG%/REB read 12/12 purely because 4 players are invisible. The UNKNOWN warning prints once in the batch where it happened and never reappears on any later card or command, so the phantom spots are invisible from then on. The feasibility guard's `remaining` (hoops.py:856) is likewise inflated, and it prints a …

- **Evidence** — Repro: 12-team/13-round/slot-4 draft, 80 picks fed, 4 of my 7 own picks announced with an unmatchable name. my logged picks: ['UNKNOWN #4', 'Ja Morant', 'UNKNOWN #28', 'Dyson Daniels', 'UNKNOWN #52', 'Alex Sarr', 'UNKNOWN #76'] $ python3 scripts/hoops.py draft turn "" --top 3 YOUR PICK: #93 | roster 3/13 | weakest: FT%, FG% your positions: C:1 PF:1 PG:1 SG:1 vs field: FG%:12 FT%:8 3PTM:5 PTS:10 REB:12 AST:4 ST:1 BLK:9 TO:8 $ python3 scripts/hoops.py draft status Your roster (3): Ja Morant, Dyson Daniels, Alex Sarr …
- **Cost** — Every UNKNOWN — from a rookie not yet in the CSV, an accented name (see the Unicode finding), or a mis-heard call — makes the card understate the owner's roster and overstate his remaining picks. The …
- **Action** — Count UNKNOWN picks per slot separately and (a) print a persistent banner on every card — e.g. `⚠ 4 UNKNOWN picks on your roster (#4, #28, #52, #76) — counts and ranks below exclude them`; (b) use the true pick count (`sum(1 for pk in picks if pk['slot']==myslot)`) for `roster N/size` and for `remaining` in the feasibility guard.
- **Owner question** — Would you rather the card refuse to print category ranks at all while any of YOUR picks is UNKNOWN, or print them with a loud caveat?

### F30 · draft fix --slot skips range validation on the UNKNOWN branch and bricks every roster command with an unhandled KeyError

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`draft fix`'s UNKNOWN branch (hoops.py:610-618) is the one slot-writing path that omits the `1 <= slot <= teams` range check that both `draft pick` (hoops.py:577) and the non-UNKNOWN fix branch (hoops.py:622-624) enforce. An operator who volunteers `--slot` on an UNKNOWN fix (a keeper/trade-style correction per SKILL.md §8, not the §9 out-of-pool flow, which passes no `--slot`) and mistypes it out of range gets it silently persisted. The bad slot is latent while the pick stays an UNKNOWN, then detonates when the placeholder is fixed to a real player: `build_rosters` does `rosters[pk["slot"]].append(p)` (hoops.py:532) against a dict keyed 1..teams and raises an unhandled KeyError, killing `turn`, `status`, `rosters`, `matrix`, `vs`, and …

- **Evidence** — Repro with `--slot 13` — a one-key-off typo in a 12-team, 13-ROUND league: $ python3 scripts/hoops.py draft init --teams 12 --size 13 --slot 4 $ python3 scripts/hoops.py draft turn "Nikola Jokic; Victor Wembanyama" --top 1 ✓ #1 R1: Nikola Jokic → T1 ✓ #2 R1: Victor Wembanyama → T2 $ python3 scripts/hoops.py draft fix 2 "UNKNOWN euro guy" --slot 13 ✎ #2: UNKNOWN euro guy → UNKNOWN euro guy (T13, out-of-pool placeholder) $ python3 scripts/hoops.py draft fix 2 "Alperen Sengun" # SKILL.md §9 step ✎ #2: Alperen Sengun …
- **Cost** — A single mistyped `--slot` on the documented out-of-pool workflow leaves the live draft tool raising a traceback on every invocation, mid-clock. The state file is gitignored and has no backup, so the …
- **Action** — Move the `1 <= args.slot <= teams` check above the UNKNOWN branch so it guards both paths, and make `build_rosters` use `rosters.setdefault(...)` or skip/warn on out-of-range slots so a bad state degrades instead of crashing.

### F31 · draft fix prints the NEW name on both sides of the arrow — the correction echo can never be verified

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

In `cmd_draft`'s fix branch, `old = picks[idx]` (hoops.py:609) binds a reference to the pick dict, which is then mutated at :612 and :621 before `old['player']` is printed at :616 and :627. Both `draft fix` print sites therefore show the NEW name on both sides of the arrow, in the normal and the UNKNOWN branches alike — reproduced verbatim. SKILL.md §5 mandates corrections be "echoed before/after", so `draft fix` cannot serve that verification: if the operator types the wrong pick number, the echo looks identical to a correct fix. The sharpest real case is SKILL.md §9's UNKNOWN-backfill workflow, where a correct echo would show `UNKNOWN #N` on the left and a mistyped number would be caught instantly. This is display-only: state is written …

- **Evidence** — Repro (state has #1 Jokic, #2 Wembanyama, #3 Shai Gilgeous-Alexander): $ python3 scripts/hoops.py draft fix 3 "Luka Doncic" ✎ #3: Luka Doncic → Luka Doncic (T3) (correct output would be: ✎ #3: Shai Gilgeous-Alexander → Luka Doncic) Contrast, same state, via turn: $ python3 scripts/hoops.py draft turn "3- Anthony Edwards" --top 1 ✎ #3 corrected: Luka Doncic → Anthony Edwards And the UNKNOWN branch does it too: $ python3 scripts/hoops.py draft fix 2 "UNKNOWN mystery guy" --slot 99 ✎ #2: UNKNOWN mystery guy → UNKNOWN …
- **Cost** — SKILL.md §5 mandates that corrections be "echoed before/after" as the operator's verification step. That verification is impossible through `draft fix`. If the wrong pick number is typed under the …
- **Action** — Change hoops.py:609 to `old = dict(picks[idx])` (or capture `old_name = picks[idx]["player"]` before mutation) so both print sites report the true prior value. One-line fix, display-only, allowed under the feature freeze.

### F32 · draft turn silently accepts a my: snake desync that draft pick --mine warns about

`NEW` · verdict **CONFIRMED** · *measured*

`cmd_draft`'s `pick` branch derives the snake slot, compares it to `myslot`, and prints a non-blocking note when `--mine` contradicts snake order (hoops.py:585-590). The `turn` branch does not: `slot = myslot if mine else team_of_pick(n, teams)` (hoops.py:767) with no comparison and no warning. The detection therefore lives only on the between-turns command and is absent from the one-command-per-turn live workflow SKILL.md §4 makes non-negotiable. `--expect` does not cover the gap — it is a pick-count handshake and a misattributed `my:` leaves the count correct (verified). Because `build_rosters` keys on `slot`, a `my:` landing one segment early or late permanently transfers one pick from a rival to the owner and corrupts both rosters plus …

- **Evidence** — Same situation, two commands, 12 teams / slot 4: $ python3 scripts/hoops.py draft turn "Nikola Jokic; my:Victor Wembanyama" --top 1 ✓ #1 R1: Nikola Jokic → T1 ✓ #2 R1: Victor Wembanyama → T4 (YOU) ← no warning $ python3 scripts/hoops.py draft pick "Nikola Jokic"; python3 scripts/hoops.py draft pick "Victor Wembanyama" --mine note: snake order says pick 2 belongs to Team 2; logging to you (Team 4) anyway. Use --slot for other out-of-order picks (keepers, trades). Pick 2 (round 1): Victor Wembanyama → Team 4 (YOU).
- **Cost** — A `my:` prefix landing one segment early or late — the single most likely feed error after surname collisions — silently gives the owner a pick that belongs to a rival and leaves that rival a player …
- **Action** — Port the hoops.py:587-590 note into the `turn` loop: when `mine` is true and `team_of_pick(n, teams) != myslot`, print a `⚠ my: at #N — snake says Team K` line alongside the ✓.


---

## MEDIUM — Process & gates

### F33 · No refresh is scheduled between the October Routine and draft night, and the Routine's self-reschedule depends on a date the repo records as TBD

`KNOWN-PARTIAL — N7` · verdict **PARTIALLY_CONFIRMED** · *measured*

The account holds exactly two enabled Routines (verified across all 205 triggers, three pages), both one-shot with no cron: 2026-09-01T14:00Z September recalibration and 2026-10-12T14:00Z October pre-draft refresh. There is no recurring refresh Routine and no draft-night Routine, and the "mandatory daily refresh" law (SKILL.md:14) has no scheduler — it fires only when the owner opens a session. That practice has already slipped four days: data/freshness.json and docs/draft-deck.html BUILD_PULL both read 2026-08-05, last commit 2026-08-05, so as of 2026-08-09 the deck renders "4 days old" in the red staleness color. The supported risk is the missing daily cadence, not an October gap: the repo's own record (arena/arena.py:6, …

- **Evidence** — list_triggers (50 rows, full account): the only non-send_later entries are trig_01DDZDEUyLJnmeU4mGWtnGWA 'September Draft Deck recalibration (one-shot)' next_run 2026-09-01T14:00:00Z enabled True, and trig_0146xxp4wAt4uHQypXLxjNZ1 'October pre-draft final refresh (one-shot)' next_run 2026-10-12T14:00:00Z enabled True. Every other trigger is a fired send_later. No cron_expression anywhere. October prompt text (verbatim): '...if a firm date exists and this firing is more than ~10 days before it, reschedule yourself …
- **Cost** — The most likely October outcome is a deck last refreshed ~10 days before the draft, missing preseason injuries and final roster cuts — precisely what §6 item 1 says the October run is for …
- **Action** — Three things, all doable now: (1) get the draft date from Yahoo the moment it is set and write it into league_intel_2025-26.md §9 item 8; (2) replace the fragile self-reschedule with a second standing Routine fixed at 'draft date minus 1 day' as soon as the date is known, and leave the Oct-12 one in place as the ADP/EDGE run; (3) add a recurring daily or every-other-day refresh Routine now rather than relying on the …
- **Owner question** — What is the actual draft date and time, and once Yahoo assigns your slot, will you send it? Both are TBD in the repo and both are inputs the October and draft-night runs need.

### F34 · September's ship bars are unevaluable: the m21/m24/m25/m26 replay states do not exist anywhere

`KNOWN-PARTIAL — lesson13 / T7` · verdict **PARTIALLY_CONFIRMED** · *measured*

The mock draft states under /root/.claude/uploads/ are gone and unrecoverable -- this is already registered as LESSONS.md lesson 13 and self-critique T7 ("Backfill is an open owner decision"), so it is not a new finding. What is new and unregistered is a two-line documentation gap around it: (a) lesson 13 asserts "Backfill of the existing mock states/results is queued for the September run (see SEPTEMBER-PLAN)", but SEPTEMBER-PLAN.md contains zero occurrences of "backfill" and no backfill row -- the lesson points at a queue item that does not exist; (b) T7 scopes the loss to "mocks 10-26", but season_sim_mock27-30.py also hardcode the uploads path, so the headline mock 27 simulation is unreproducible as well; and (c) …

- **Evidence** — $ ls /root/.claude/uploads/ -> 'No such file or directory'. `grep -rln '/root/.claude/uploads' .` -> 36 files. Fresh clone (/tmp/freshclone, cloned from the repo): $ python3 arena/mocks/season_sim_mock21.py -> FileNotFoundError: '/root/.claude/uploads/58588377-.../773c5fc1-draft_state_10.json' $ DECW_OUT=/tmp/decwout python3 arena/mocks/decw_card_v2.py 0.5 1 21 -> same FileNotFoundError (decw_card_v2.py:71) — this is the Python reference for the JS↔Python parity gate. Control: $ python3 …
- **Cost** — On 2026-09-01 the fired session cannot grade a single bar that names m21/m24/m25/m26. Two outcomes, both bad: the honest weaker model reports 'cannot evaluate' and September ships nothing except the …
- **Action** — Before top-model access ends: reconstruct and commit the mock 16-30 draft states under arena/data/states/ (the debriefs contain the pick lists; if any cannot be reconstructed, delete the corresponding harness and strike those mocks from every ship bar), repoint the STATE/UP constants at the committed path, and correct arena/mocks/README.md. If states cannot be recovered, rewrite the affected bars in SEPTEMBER-PLAN …
- **Owner question** — If the m16-30 states are unrecoverable, do you want September's engine experiments graded on the 4 surviving mocks, or deferred to October with no engine change at all?

### F35 · The deck's JUDGMENT layer is 11 days stale, no gate sees it, and it is currently penalizing a player who signed a week ago

`KNOWN-PARTIAL — T7` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL law 1d requires the deck's JUDGMENT layer to be re-authored in the same pass as any rebuild, but build_deck.py has no gate for it: gates 1-3 cover roster verification, freshness and pool completeness, and the injector touches only PLAYERS, BUILD_PULL, BUILD_NOTE and the footer prose. Nothing in the repo reads JUDGMENT.date, which still says "2026-07-28" against a manifest built 2026-08-05 and a freshness stamp of 2026-08-05. One live contradiction is measurable today: Jeremy Sochan signed with POR on 8/1 — recorded in players.csv:202, in the deck's own embedded PLAYERS row, in the deck's colophon prose at :403, and in rosters_official.json — while JUDGMENT:1219 still carries {adj: -0.15, why: "Unsigned after a limited NYK title-run …

- **Evidence** — draft-deck.html:1191-1193: comment 'Grounded in the 2026-07-28 refresh research (re-dated at each republish alongside JUDGMENT.date)' then 'const JUDGMENT = { date: "2026-07-28",'. $ grep -n 'JUDGMENT.date' docs/draft-deck.html -> only the comment at 1191; no code reads it. build_deck.py:92-114 touches only PLAYERS, BUILD_PULL, BUILD_NOTE, 'Pool refreshed' prose. draft-deck.html JUDGMENT.players: '"Jeremy Sochan": { adj: -0.15, why: "Unsigned after a limited NYK title-run role." }' and '"Bennedict Mathurin": { …
- **Cost** — On draft night the card silently marks down a player for a condition that resolved, and shows the owner a rationale naming the wrong team — the tooltip is the thing he trusts to explain a demotion. …
- **Action** — Add gate 4 to build_deck.py: parse JUDGMENT.date out of the deck and FAIL unless it equals freshness['date'] — same fail-closed shape as the other gates, ~6 lines. Add a second cheap check: any player carrying an unsigned-FA judgment whose players.csv team is not 'FA' is a hard error. Then re-author the layer against today's news before October.


---

## MEDIUM — Skill / live protocol

### F36 · Live-draft failure modes are unaddressed: state corruption crashes with a raw traceback, RESYNC has no mechanism, SYNC needs two commands

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The live-draft protocol names two recovery keywords whose mechanics are undocumented and partly unserved by the engine. Verified: (a) `load_state` (scripts/hoops.py:486-488) parses the state file with an unguarded `json.load`, and `main()` catches only BrokenPipeError (line 1033), so a truncated or corrupt `draft_state.json` prints a raw JSONDecodeError traceback from every draft subcommand except `init` — with no recovery instruction anywhere in the skill; (b) `save_state` (490-492) truncates and rewrites the single state file with no temp-and-rename and no backup, so an interrupted write is the one way to produce that corrupt file; (c) RESYNC has no `resync` subcommand and no written command sequence — it is achievable today with `draft …

- **Evidence** — Truncated draft_state.json to `{"teams":12,"slot":5,` and ran `draft turn "Naz Reid" --expect 55` → full Python traceback ending `json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 22`. scripts/hoops.py:490-492 `def save_state(state): with open(STATE_PATH,"w") as f: json.dump(...)` — non-atomic, no backup. Subcommand list (scripts/hoops.py:954-998): init/pick/undo/fix/best/turn/status/rosters/matrix/vs — no resync. `draft status` output on a 55-pick state: "Draft: 55 …
- **Cost** — The draft runs exactly once, with no rehearsal, on a 45-second clock. Any of these events converts the session from an advisor into a debugger mid-draft. State loss is the worst case: the designated …
- **Action** — Add `draft resync` (accepts a pasted pick list plus the owner's slot, rebuilds the board, echoes the reconciliation) and `draft status --tail N`; make `save_state` write-temp-then-rename and keep a `.bak`; wrap state loads so a corrupt file prints a recovery instruction instead of a traceback. In the skill, add a short numbered "if X happens live, do Y" block covering crash, silence, out-of-order picks, and …
- **Owner question** — If Yahoo autodrafts for you because the clock expired, do you want the session to log it silently and move on, or to flag the damage and re-plan the build?

### F37 · The skill encodes none of the league settings that define this league — daily lineups, unlimited moves, waivers, playoff format

`KNOWN-PARTIAL — N5` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md — the protocol a draft-night session auto-loads — states only 12 teams, 13 roster slots, the eight positional slots, and 156 picks (line 31). It never states that lineups are DAILY, that moves are UNLIMITED, that waivers are daily FFA with game-time locks, that the season is 18 weeks, or that 8 of 12 make the playoffs in three 1-week rounds. Its only adjacent line (48) is generic H2H advice with no mechanism, and it contains no pointer to arena/results/league_intel_2025-26.md, where those facts live. docs/draft-deck.html and README.md carry them no better — the deck's 13 "streamer" hits are rival-manager attributes, not the owner's chassis. This is a propagation gap, not a knowledge gap: round-2's scorecard marks the settings item …

- **Evidence** — `grep -ni "daily|unlimited|waiver|stream|18-week|playoff" .claude/skills/fantasy-basketball/SKILL.md` returns only the frontmatter description (which says "waiver wire" as a trigger phrase) and line 48's generic H2H sentence. League ground truth in arena/results/league_intel_2025-26.md §9 (Q3–Q6): daily lineups, unlimited moves, daily FFA waivers with game-time locks, 8/12 playoffs, three 1-week rounds weeks 19–21, IL+ never drafted for. analysis_2026-08-04_self_critique_round2.md N5: "the card's draft-night …
- **Cost** — Late-round advice is the part of the draft most changed by daily lineups and unlimited moves (bench spots are streaming slots, games-played density and positional flexibility matter more than …
- **Action** — Add a short "League facts (ground truth)" block at the top of the live-draft protocol restating Q1–Q9 from league_intel_2025-26.md verbatim, and state the one consequence explicitly: bench spots are streaming slots — value flexibility and games played over marginal z there.
- **Owner question** — How many of your 3 bench spots do you actually intend to churn weekly? That sets whether the last rounds should target upside stashes or high-games-played fillers.


---

## LOW — Arena instrument

### F38 · 13 personalities in 12 seats systematically denies each strategy one specific draft slot in tournament() and slots(), while the slot effect spans 13.5pp

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Known-but-unregistered instrument blemish: with 13 personalities and 12 seats, tournament()/slots() score only order[:TEAMS], so in the unshuffled first rotation round each strategy is denied one fixed slot (council S2, bpa_pure S3, ... specialist S12, points_chaser S1) while market takes a 12th seat with full slot coverage. The tournament docstring at arena.py:430-433 still claims every strategy sees every slot once per round and is false. Because a strategy's reported mean averages its 11 seated slots, the induced bias is (grand_mean - denied_slot_mean)/11: at most 1.23pp spread at rotations=1 and ~0.41pp at the shipped defaults (council -0.28pp, points_chaser -0.21pp, stars +0.13pp) — below the repo's own ~2pp trust floor and below …

- **Evidence** — Replayed the rotation logic directly for an unshuffled round: council seated 11, never drafts from slot 2; bpa_pure never slot 3; punt_ft never slot 4; ... specialist never slot 12; points_chaser never slot 1; market seated 12 with all 12 slots. Confirmed in the committed artifact — tournament_seed1.json's champ% values are exact multiples of 100/11 (9.0909…), i.e. seated=11. Magnitude of the confound, from the committed slot_intel.json: mean champ% by slot runs S2 17.62, S1 15.42, S3 12.29 … S7 4.08, S11 4.97 — …
- **Action** — Either drop one personality so the cast is 12, or run 13 rotations per round instead of 12 so every name sits out exactly once per slot-complete cycle. Fix the docstring either way. Both are instrument changes — register with the September re-baseline.

### F39 · Circularity inventory: the objective, the grade, and the ship bar all read one model whose ~14 weekly constants are entirely hand-set

`KNOWN-PARTIAL — T2 / N1 / LEDGER §5 bound` · verdict **PARTIALLY_CONFIRMED** · *reasoned*

The circularity itself is fully KNOWN, not KNOWN-PARTIAL: T2, N1, and LEDGER §5's Bound each state that ECW is computed from team_week_model and therefore reads the instrument rather than reality, and N1 already prescribes the finding's action verbatim ("fit CV constants to reality -> re-run the E9 validation on the refit model"). The claimed novelty — that the arrival of weekly_matchups_2025-26.csv makes the circularity a choice "since N1 was written" — is refuted: that CSV's own README, dated the same day as N1, registers it as the fit data for R7/N1 and names the exact constants to be re-estimated. The parameter inventory is accurate for the six weekly-model constants (BENCH_WEIGHT, 7 CVs, PCT_MIX_INFL, TEAM_WEEK_SHOCK, 3 availability …

- **Evidence** — Free parameters of the weekly model, all hand-set with no fit: 7 CV constants (arena.py:54-55), PCT_MIX_INFL, TEAM_WEEK_SHOCK, 3 availability tiers (arena.py:332-338), BENCH_WEIGHT, the 3.5 games/week constant, GRAD_DEFL's 9 deflators — and docs/draft-deck.html:998-1026 ports them verbatim. Claims genuinely anchored to real-world data: league_intel §2/§10/§11 standings and the three-season 'the #1 record has never won' signature; §5's reach index (room_model.py, 148/156 picks matched against a real draft board) — …
- **Action** — State in the September report which claims are instrument-internal and which are anchored, using the two lists above, and make the weekly refit a precondition for re-quoting any of the instrument-internal ones — rather than a parallel workstream.

### F40 · Dylan Harper is still priced as a hype rookie inside the arena's market model, which the September plan will re-point at the 2026-27 pool

`KNOWN-PARTIAL — owner gap #2` · verdict **PARTIALLY_CONFIRMED** · *measured*

MKT_PIN (arena/arena.py:175-177) is keyed on player name with no note or eligibility guard, so its hand-set July pins survive a pool swap untouched. Measured on the live data/players.csv pool, the "Dylan Harper": 60 pin lifts him from market-model rank 114 to 63 — a ~51-rank hype premium that fully overrides the data-plane fix (his rookie-proj note is already cleared in data/players.csv:106). Impact is zero today because arena.py:39 pins the arena to the frozen October-2025 snapshot, where Harper genuinely was a rookie. The exposure opens at SEPTEMBER-PLAN §1.4 ("re-baseline the arena on the fresh pool"), which would apply lottery-rookie name-value hype to a SECOND-YEAR guard (Harper: June 2025 draftee, rookie season 2025-26, year 2 in …

- **Evidence** — arena/arena.py:175-177 `MKT_PIN = {"Cooper Flagg": 18, "AJ Dybantsa": 30, "Darryn Peterson": 55, "Dylan Harper": 60, "Cameron Boozer": 70, "Caleb Wilson": 90, "Mikel Brown Jr.": 95}` with the comment block at 173-174. data/players.csv:106 Dylan Harper row ends with an empty note field; data/players.csv:26 Cooper Flagg likewise; data/players.csv:222 AJ Dybantsa still carries `rookie-proj` (correct — he is a 2026 draftee). arena/data/players_2025-10-21.csv:26 and :106 still tag both as rookie-proj, which is correct …
- **Action** — At the September re-baseline, rebuild MKT_PIN from the September consensus ADP rather than carrying the July hand-pins forward, and add a build-time assertion that every MKT_PIN name whose pin is justified by rookie hype still carries a rookie-proj note in the loaded pool.


---

## LOW — Data layer

### F41 · Schema has no minutes, no games-played, no age, no ADP and no variance — the four checks that would have caught the other findings are all unbuildable

`KNOWN-PARTIAL — T4 / N3 (variance and market rank registered; minutes, GP and age are not)` · verdict **PARTIALLY_CONFIRMED** · *reasoned*

data/players.csv carries 15 columns (player, team, pos, fg_pct, fga, ft_pct, fta, tpm, pts, reb, ast, stl, blk, tov, note) and has no per-player minutes field. Minutes is the only one of the finding's four proposed columns not already registered: GP/flat-availability-tiers is T4 verbatim (including the 0.88/0.75/0.60 triple), age-conditioning is E19 by name with the same Lillard-vs-Haliburton example, variance is T4/N3, and real ADP is scheduled at three separate points in SEPTEMBER-PLAN (§2, §6.2, §6.3) plus E18's bar. Adding `min` at the October re-ingest is cheap and would make role repricing a one-cell edit instead of an eleven-cell one. The finding's claim that the team-budget defect is "impossible to detect without a minutes column" …

- **Evidence** — Header of data/players.csv line 1: `player,team,pos,fg_pct,fga,ft_pct,fta,tpm,pts,reb,ast,stl,blk,tov,note` — 15 columns, confirmed by csv.DictReader keys. Flat availability tiers: scripts/hoops.py:304-310. Arena/deck weekly tiers unchanged from the values LESSONS.md:36-40 says were wrong: arena/arena.py:332-338 (`0.60 / 0.75 / 0.88`) and docs/draft-deck.html:1001-1005 (`if (note.includes("recovery")) return 0.60; if (note.includes("risk")) return 0.75; return 0.88;`). Market model with no ADP input: …
- **Action** — Add `min` and `gp` in the October re-ingest (both come free with any real projection source) and derive availability from `gp` instead of note substrings. Add `age` (one number per row, zero maintenance, resolves the Lillard-vs-Haliburton problem N3 raises). Add an `adp` column at the October real-ADP sync that E18's re-armed ±8 bar already depends on. Variance stays the September/E-item it already is.
- **Owner question** — Are you willing to take a schema change during the freeze, or should all five columns land as one batch at the October re-ingest? Adding `min` alone unblocks the team-budget gate and is the cheapest single win here.

### F42 · The pool is a draft board, not a season pool: 85 undrafted names for an 18-week season with unlimited daily moves

`KNOWN-PARTIAL — E16 / N5 (registered as the arena's streaming gap; the data-layer …` · verdict **PARTIALLY_CONFIRMED** · *measured*

The pool's inclusion rule is pegged to draft relevance ("top-200 relevance" per the SKILL.md completeness sweep), so after 156 of 241 available rows are drafted only 85 names remain for an 18-week season of daily free-for-all waivers with unlimited moves — and streaming-tier players (roughly ranks 160-350) are structurally out of scope by design, not by oversight. Arithmetic verified: 246 rows, 5 recovery/retired exclusions, DRAFTABLE=156 at scripts/hoops.py:220, 85 remaining, of which 12 are C-eligible. This is a scope question rather than a defect: the system already labels the file a "top-210 draft baseline" (data/RESEARCH.md:1,4), already tells the user to add rows when find misses (scripts/hoops.py:472-473 and SKILL.md:53), and …

- **Evidence** — Engine run over data/players.csv: `available: 241 of 246` (excluded: Malcolm Brogdon out-retired; Jimmy Butler acl-recovery; Steven Adams ankle-recovery; Moses Moody patellar-recovery; Donte DiVincenzo achilles-recovery). DRAFTABLE = 156 at scripts/hoops.py:220. 241 − 156 = 85. Positional supply within the draftable 156 is comfortable (PG 44, SG 48, SF 40, PF 42, C 46 eligible against a 12×[1 PG,1 SG,1 G,1 SF,1 PF,1 F,2 C] requirement), so depth is a season-pool problem, not a draft-feasibility problem. Doc counts …
- **Action** — Decide the pool's purpose explicitly. If it stays a draft board, say so in README/SKILL and route in-season waiver questions to web search rather than `find`. If it should serve the season, the October build needs ~350-400 rows (the marginal rows are cheap — they only need to beat replacement level to be useful) and the z-standardization already handles it correctly via the top-156 fixed point. Fix the ~210/~250/246 …
- **Owner question** — Is this tool meant to help you on waiver days too, or is draft night the whole job? That answer decides whether the October pool is 246 rows or 400.


---

## LOW — Draft Deck

### F43 · 16% of owner turns have an exact #1/#2 tie broken by reverse-alphabetical name, and the 🎯 "system pick" marks the winner

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

On a market-order board, 16.0% of the owner's 144 turn-states (23) have an exact `scored[0].ds === scored[1].ds` tie and 41.0% (59) have a tie somewhere in the Top 5, because blend50 is the mean of two r/(n−1) percentile ranks and is therefore quantized. The tie is broken by `(a.p.n < b.p.n ? 1 : -1)` at docs/draft-deck.html:2335 — descending on the FULL display name (first name first, not surname) — and the 🎯 "system pick" marker plus the advice line's imperative `Take {name} — coin flip with #2, either is fine.` (:2519) both land on that arbitrarily selected player, with #2 never named in the advice line. The exact-tie rate is board-dependent: 16.0% market-order, 11.1% value-order, 5.6% mixed (the mixed board being closest to the deck's …

- **Evidence** — docs/draft-deck.html:2335-2338 — `.sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0))` with the comment "tie-break = name DESCENDING, matching the validated python reference". `pctRanks` at :1041-1048 (rank/(n−1) quantization). Node harness, 144 states (12 slots × rounds 2-13, market-order board): exact top-2 ties 23; top-5 containing a tie 59; coin-flip fires 87 (60.4%, consistent with the "~64%" calibration claim at :2350); standout fires 7 (4.9%). Example ties observed: slot 4 R3 …
- **Action** — When `scored[0].ds === scored[1].ds`, break the tie on a stated substantive criterion rather than name (candidates: higher `adjValue`, or the scarcer positional family, or lower market rank), and render both names under one 🎯 with "tied — [criterion] breaks it". Keep a deterministic final fallback for parity. Display + tiebreak only; needs the 130-state gauntlet re-run.
- **Owner question** — When the card says coin flip, what do you actually want it to break on — scarcity at the position, or the player likelier to be gone at your next turn?

### F44 · Every tooltip in the deck is mouse-only: the entire explanation layer is unreachable on a phone or tablet

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The deck's tooltip layer has no touch-, focus-, or keyboard-specific affordance: all 25 `dataset.tip` tooltips hang off one delegated `document` `mousemove` handler (docs/draft-deck.html:1584-1587), and 8 native `title` tooltips (6 in markup at :313, :316, :343, :350, :353, :354; 2 assigned in JS at :2671, :2737) have no scripted path at all. Consequences split. The 8 `title` tooltips ARE unreachable on touch — no mobile browser surfaces `title` — and they cover the two zone lines and the Mkt/Val/Fit column-header definitions, which is where the "display lens only / build-agnostic by design" disclaimers live. The 25 JS tooltips are NOT unreachable: mobile browsers fire compatibility mouse events (mousemove → mousedown → mouseup → click) on …

- **Evidence** — docs/draft-deck.html:1584-1587 — `document.addEventListener("mousemove", e => { const td = e.target.closest && e.target.closest("[data-tip]"); if (td) showTip(...) else hideTip(); })`; no `touchstart`/`click`/`focusin` listener anywhere (`grep -n "addEventListener" ` over the app block). Counts: 25 `dataset.tip` assignments, 6 `title=` attributes. Responsive surface: `<meta name="viewport">` at :3, one `@media (max-width: 960px)` at :100, `.tablewrap { overflow: auto }` at :209. Visible ranks confirmed at …
- **Action** — Add `click`/`touchstart` to the same delegated handler with a tap-to-dismiss, and mirror the `title=` attributes onto `data-tip`. Small, display-only.
- **Owner question** — Will you have the deck open on a phone or tablet on draft night, or laptop only? If laptop only this is not worth spending the freeze window on.

### F45 · Judgment layer is inert: `adj` never reaches the Top-5 sort key, but the card still prints "jdg −0.30" chips

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Post-E9 the Top-5 order and membership are `ds`-only, so judgment `adj` and the board-slide bonus do not reorder the card — but this is the documented, pre-registered E9/blend50 ship decision (findings_2026-08-04_decw_round2.md "they no longer reorder"; REVERT-MAP.md §decw-ordering kill switch; in-code comments 2313-2319), not an unregistered inertness, and the primary surface already labels it ("Informational: council … · judgment …", line 2417). What actually remains is stale prose in three places that still implies the old coupling: the colophon's "Every layer beyond the composite ranking is display-only" (line 404, the ranking is no longer the composite, and the judgment sentence never states it does not reorder), the comment at …

- **Evidence** — docs/draft-deck.html:2331-2336 builds `{adj, slide, vbonus, fs}` then `.sort((a, b) => b.ds - a.ds || <name tiebreak>)` — `fs` is not in the comparator. Grep of every `fs` reference in the file (lines 2319, 2334, 2551) shows the only non-comment consumers are `el("span","sc", row.ds >= 0 ? ... : fmtZ(row.fs,2))` (2551, a fallback that fires only when ds<0) and the tooltip at 2417. `scoredAll` is derived from `councilTop` = the whole scored pool, so Top-5 membership is `ds`-ranked too. Rendered chips: line 2427 …
- **Action** — Before October: either (a) re-couple judgment as a term inside the blend in percentile units (e.g. convert `adj` to a rank shift on `pv`, then re-run the ledger replays under E21's punted-mock screening), or (b) if it stays display-only under the freeze, relabel every judgment/slide chip and the colophon sentence as informational — the same display-only truth fix E20 registered for the punt box. Do not ship (a) …
- **Owner question** — When you look at the Top 5 on draft night, do you expect the judgment notes to have already moved the order, or do you read them as context you apply yourself? The fix is different in each case.

### F46 · No committed JS↔Python parity harness exists — the September/October Routine's `PARITY: EXACT MATCH` gate is unexecutable from a fresh clone

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SEPTEMBER-PLAN §1.3 gates the 2026-09-01 Routine on build_deck.py printing `PARITY: EXACT MATCH`, and §6 item 5 repeats "all gates + parity" for the October refresh, but no committed command emits that string or performs any parity check: build_deck.py's four checks are roster-verification-today, freshness-today, pool completeness, and an injection round-trip; scripts/ contains no parity harness and no .py file in the repo invokes node against the deck engine. This is a narrow instance of an ALREADY-REGISTERED problem, not a new one — LESSONS.md lesson 13 explicitly names "parity counts" among the sim-side numbers that rest on records rather than re-derivable artifacts, and arena/results/findings_2026-08-04_decw_round2.md item 3 already …

- **Evidence** — scripts/build_deck.py:1-150 (full file, 150 lines) — gates at 42-70, injections at 93-107, post-write checks at 134-143, final print at 145-146; no parity step. `grep -rn "PARITY" .` returns only arena/results/SEPTEMBER-PLAN.md (lines in §1.3 and §6.5). Data-parity re-verified independently today: deck PLAYERS block (246 rows, extracted from docs/draft-deck.html:1183) vs `hoops.zscores(hoops.load_players())` — max z delta 4.995e-07 (Julius Randle FT%, pure 6-dp rounding), av mismatches 0/246, 0 names missing in …
- **Action** — Commit a `scripts/check_parity.py` that node-executes the extracted `<script id="engine">` block against the Python engine on a fixed set of states (pool z/av rows, plus `decwScores`, `strategyScores`, `managerScores`, and `matchCandidates` on a seeded fixture set) and prints `PARITY: EXACT MATCH` or a diff; call it from build_deck.py as gate 4, fail-closed. This is process/tooling, not an engine change.


---

## LOW — Fantasy-domain semantics

### F47 · Positional saturation is nearly free under daily lineups — the entire positional-need machinery is calibrated for a weekly-lineup league

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Under daily lineups the SLOT-FEASIBILITY cost of positional saturation is small and independently reproducible (4C->6C ~0.4-0.5% of rostered player-games lost; 4C->8C ~2-3%; only past ~9-10 C-eligible does it reach 5-10%), so the LINEUP_SLOTS comment at arena/arena.py:133-139 and docs/draft-deck.html:823-829 states a WEEKLY-lineup rationale ("caps startable bigs at C,C,Util,Util") that overstates the slot penalty in this daily league. That is a real doc/model framing defect — but it is the same lineup_weights/BENCH_WEIGHT weekly mis-specification the owner already found (KNOWN gap 1), and it does NOT invalidate E22: E22's registered evidence is a CATEGORY consequence (AST kept-cat win probability 0.202), and I measured that going 4C->6C …

- **Evidence** — Daily-lineup fill over 165 days x 60 rosters per cell, share of rostered player-games actually started, as a function of C-eligible count on a 13-man roster: 2C 0.965, 3C 0.973, 4C 0.974, 5C 0.971, 6C 0.969, 7C 0.959, 8C 0.942, 9C 0.926, 10C 0.899. Going from a balanced 4C roster to the mock-34 shape of 6C costs 0.5% of games; 8C costs 3.2%. Multi-position eligibility is worth almost as little: stripping every player to his PRIMARY position only moves games-started share 0.9612 → 0.9373, i.e. 2.4%. Corroborating …
- **Action** — Before building E22's saturation term, re-run its motivating measurement under a daily-lineup fill. My prediction, pre-registered here: the saturation term will not clear its bar, because the effect it is designed to capture is 0.5-3% of games. Reframe the positional layer as a hard feasibility check only (never leave PG/SG/SF/PF/C unfillable) and drop the soft need/scarcity/LEAN weighting from the value path. Also …

### F48 · Punt doctrine is imported from most-categories/roto play; in an each-category league every punt is ~18 guaranteed losses of 162

`KNOWN-PARTIAL — E20/E23` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md:33/:46 and hoops.py's punt surfaces (`rank --punt`, `draft init --punt`, total_value at 281-282) present punting as a neutral, unqualified build mode with no pointer to the measured G1a cost, so a session working only from the skill and CLI re-derives generic punt doctrine that the deck and arena results already contradict. This is a documentation-surface gap, not a domain-comprehension failure: the each-category vs most-category distinction is already codified in arena.py:404-407 with a measured +-29pp impact ("9-CAT math audit", 2026-07-30), the 5-of-9 concentration model was explicitly built and shelved as G2 (-2.02pp, findings_2026-07-30_gap_study.md), the deck's Top-5 is punt-blind by design and fires a warning citing G1a on …

- **Evidence** — hoops.py:281-282 and SKILL.md:46 as quoted; league_intel_2025-26.md:13 confirms 'H2H each-category, 9-cat (162 = 18 wk x 9 cats, verified)'. Real-league counter-example, computed from arena/data/weekly_matchups_2025-26.csv (owner vs opponent, 18 regular-season weeks): the owner's best-record season was a ZERO-punt build that finished above 50% in all nine categories — ST 14/18, FT% 12/18, 3PTM 12/18, TO 12/18, FG% 11/18, PTS 11/18, AST 11/18, BLK 11/18, REB 9/18, total 103 of 162, the league's best record. His …
- **Action** — Add the format arithmetic to the punt surfaces as a display-only truth fix (allowed under the freeze): when a punt is declared, show the guaranteed record cost (n_punted x 18 of 162) and the resulting playoff bar (5 of 9-n). Fold it into E23's wording. Separately, add one line to SKILL.md's punt-coherence rule naming why punting is weaker in each-category than the generic 9-cat literature assumes, with the G1a -5 to …

### F49 · The live skill instructs Claude to weight swing categories more heavily — the exact rule the arena measured at -3.78pp and removed

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md has not been updated for the 2026-07-28 locked/lost neutralization (re-quoted at +5.59pp, t=7.18 on the fixed instrument). It contains no reference to that codification, to blend50/punt-blind ordering, or to the Draft Deck at all. The clearest surviving instance of the retired doctrine is live-protocol rule 3 ("Marginal value in already-locked categories counts for little; say so when it drives a demotion", dated 2026-07-11), not the analysis-rules bullet at line 48 — line 48 bundles swing-weighting with streaming flexibility, an in-season concept the arena never tested. The stated harm mechanism is wrong: scripts/hoops.py, the engine SKILL.md actually drives, contains no ECW/blend50/locked-weight logic, so a session cannot be …

- **Evidence** — SKILL.md:48 verbatim above. arena.py:99-102 sets council locked_w=1.0, lost_w=1.0 (neutral) with that comment, while DEFAULT (arena.py:89-92) keeps the field seats at 0.35/0.45 'so baselines stay comparable' — i.e. the swing weighting survives only as a control arm. The deck carries the same note at draft-deck.html:862-865. The record is genuinely two-sided, which is why this is a doctrine defect and not a math defect: the later ΔECW/blend50 objective does saturate (marginal value →0 in won and lost cats) and …
- **Action** — Rewrite SKILL.md:48 to state the measured position: category saturation is handled inside the shipped ΔECW ordering; do not additionally hand-reweight swing categories on top of the card. Add the -3.78pp citation so the next session cannot re-derive the old rule from first principles. Display/doc-only, allowed under the freeze.

### F50 · The season sim's weekly variance is ~half of reality in all 7 counting categories — and the aggregate check that 'validated' it cannot see this

`KNOWN-PARTIAL — N1` · verdict **PARTIALLY_CONFIRMED** · *measured*

The weekly model is NOT ~2x too tight in the counting categories. The 2x gap is an artifact of comparing a within-roster model CV against pooled team-week totals that carry league-wide schedule variance: of the observed 14.2% GP CV, 13.2% is common to both teams in a matchup (and therefore cancels in every category decision) and only 5.2% is independent. Excluding week 8 alone (NBA Cup knockout week, 21 and 27 team-games vs a ~44 norm) under the finding's own exclusion rule takes the PTS ratio from 0.60 to 0.97. On the matchup-relevant independent component, measured two independent ways, the shipped model is within about +/-15% for PTS, REB, AST, ST, 3PTM and TO. The named mechanism is also incorrect: team_week_model already carries …

- **Evidence** — Model team-week CV computed from arena.team_week_model over 72 arena-drafted rosters vs observed CV from the owner's 32 clean team-weeks — PTS 8.9% vs 18.0% (ratio 0.49); REB 9.8% vs 21.2% (0.46); AST 10.6% vs 20.5% (0.52); ST 14.9% vs 27.1% (0.55); BLK 17.8% vs 29.1% (0.61); 3PTM 13.6% vs 23.4% (0.58); TO 11.7% vs 23.5% (0.50). Even adding TEAM_WEEK_SHOCK=0.06 in quadrature (arena.py:71, applied at arena.py:385-387) only takes PTS to 10.7% vs 18.0%. Mechanism: observed GP CV is 14.2% (mean 41.75, sd 5.94) while …
- **Action** — Fit CV, TEAM_WEEK_SHOCK, and the games term to arena/data/weekly_matchups_2025-26.csv as the September N1 refit — but fit games first, not the CV constants, since ~half the missing variance is the constant-3.5 assumption rather than per-game noise. Then re-run the E9/blend50 validation on the refit model, because every effect size in findings_2026-08-04_decw_round2.md was measured on the tight model.

### F51 · The two tools you use on draft night disagree about bench value by 5.7x

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The deck's validated Top-5 ordering (blend50 `ds` from decwScores, which bench-discounts unslotted players at 0.15 inside teamWeekModel, deck:1010-1020, 2327-2336) never shipped to scripts/hoops.py, the engine behind the SKILL-mandated one-command `draft turn` (SKILL.md:34). The CLI orders its board by adj_value alone — no roster-composition or lineup term — so from roughly round 11, when rosters exceed the ten daily slots, the CLI's candidate order and the deck's Top-5 can disagree, and neither tool notes the other exists. This is a board-ORDERING gap, not a bench-weight disagreement: the two tools' operator-facing "vs field" category ranks are computed by the same flat unweighted sum (hoops.py:536-537 and its JS twin at …

- **Evidence** — hoops.py:536-537 `def roster_totals(roster): return {cat: sum(p['z'][cat] for p in roster) for cat in CATS}` — no lineup_weights call anywhere in hoops.py (`grep -n BENCH_WEIGHT scripts/hoops.py` returns nothing; the constant exists only in arena/arena.py:52 and docs/draft-deck.html:830). Deck path: lineupWeights (deck:831-846) returns 0.15 for the three unslotted players, teamWeekModel multiplies mu and var by it (deck:1013-1020), decwScores calls teamWeekModel per candidate (deck:1056). Measured consequence of …
- **Action** — Pick one weighting and make it the single source of truth. Given findings 1 and 5, that should be a measured start-share (~0.85, or per-rank), applied identically in hoops.py roster_totals, arena.lineup_weights, and deck lineupWeights, with the JS-Python parity gate extended to cover it. This is a truth/consistency fix, but it changes rankings, so it needs the September ship bar rather than an in-freeze patch.


---

## LOW — Python engine (hoops.py)

### F52 · No end-of-draft guard: turn and pick keep logging picks 157, 158, 159 in a 156-pick league, and my_next_pick advertises a pick that cannot exist

`KNOWN-PARTIAL — lesson 7` · verdict **PARTIALLY_CONFIRMED** · *measured*

`my_next_pick` (hoops.py:511-518) is an unbounded `while True` loop, so once the owner's final pick is logged it returns a pick number past the end of the draft. Reproduced at 12 teams x 13 rounds, slot 4: `draft status`, `draft best`, and the `draft turn` card all print "#165" although the draft ends at #156 and his last pick was #148. Exposure is bounded — it appears for (12 - slot) remaining picks (11 for slot 1, 8 for slot 4, none for slot 12), i.e. at most the tail of the final round, not "the last two rounds" — and the same line prints "roster 13/13" alongside it. Separately, neither `draft pick` (hoops.py:590) nor the plain-append path in `draft turn` (hoops.py:785, 801) bounds `len(picks)` against `teams * size`, though …

- **Evidence** — 150-pick state, 12 teams x 13 rounds: $ python3 scripts/hoops.py draft status Draft: 150 picks made (round 13 of 13), your next pick: #165 ← #165 > 156, and my last pick was #148 $ python3 scripts/hoops.py draft pick "Jerami Grant" Pick 157 (round 14): Jerami Grant → Team 12. Your next pick: #165 $ python3 scripts/hoops.py draft turn "Kyle Filipowski; Ayo Dosunmu" --top 1 ✓ #158 R14: Kyle Filipowski → T11 ✓ #159 R14: Ayo Dosunmu → T10 picks now 159 / max legal 156
- **Action** — Refuse (or loudly warn on) any append once `len(picks) >= teams * size`, and have `my_next_pick` return None past the owner's last pick so the card prints 'no picks remaining' instead of a fictional number.

### F53 · One malformed cell in players.csv kills every command including draft turn — and SKILL.md tells the operator to edit that CSV mid-draft

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`load_players` (hoops.py:211-218) coerces eleven columns with a bare `float(r[k])` and no try/except, so a hand-edited row with a blank numeric cell or too few columns aborts every hoops.py entry point with a raw traceback that names hoops.py:217 and the bad value but not the offending row or player. Reproduced for both a blank cell (ValueError) and a short row (TypeError). This is an error-message/ergonomics defect, not a missing gate: `validate` (hoops.py:1009) and build_deck.py's gate 3 (line 68) both call `load_players()`, so a malformed CSV already fails loud at the pre-draft gate and fail-closed at the publish gate before it can reach a draft or the published deck. SKILL.md §9 additionally forbids editing the CSV while on the clock …

- **Evidence** — Blanking one stat cell in a copy of players.csv (HOOPS_DATA override): edited row: Giannis Antetokounmpo,MIA,"PF,C",0.598,19.2,0.630,,0.3,30.8,11.7,6.3,0.9,1.1,3.2, $ python3 scripts/hoops.py draft turn "Nikola Jokic" File ".../scripts/hoops.py", line 217, in load_players r[k] = float(r[k]) ValueError: could not convert string to float: '' Appending a short row ('Some Newguy,BOS,SF') produces the same class of failure — DictReader yields None for the eleven numeric fields.
- **Action** — Wrap the coercion in a per-row try/except that reports `row N ('<player>') column '<col>' is not a number` and exits with that message; extend `validate` to run the same numeric check so a bad row is caught by the pre-draft gate rather than by `draft turn`.
- **Owner question** — Should a bad row abort, or be dropped with a warning so the draft can continue on a 245-player pool?

### F54 · The top-156 z-score fixed point can 2-cycle and can exceed its 5-iteration budget, silently and without a convergence check

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`zscores` (hoops.py:266-278) iterates the top-156 standardization set at most 5 times and breaks when the current top-156 set matches ANY previously seen set, so it cannot distinguish a true fixed point from a cycle of length >1, and it emits no warning on either exit path. The docstring's "audit: converges in one step" is a verified property of the CURRENT data, not of the algorithm — reproduced: the committed pool detects a repeat at iteration 2 with cycle length 1. Over 300 pools formed by scaling every counting stat by U(0.6,1.4), 11 of 300 (~4%) land on a multi-step cycle instead of a fixed point, and detection took up to 6 iterations vs the budget of 5; at wider perturbations, cycles of length 3 and 4 also occur and detection reached …

- **Evidence** — Reimplemented the hoops.py loop verbatim and ran it over 300 pools formed by scaling every counting stat by U(0.6, 1.4): max iterations to detect a repeat: 6 (hoops.py budget = 5) cycle-length histogram: {1: 293, 2: 7} (1 = true fixed point, 2 = oscillation) On the CURRENT committed pool it converges in one step exactly as documented (symmetric difference 0 at iteration 1). Impact measured on one oscillating pool by running the loop to parity A vs parity B: 48 of the top-156 board ranks move, largest move ±2 …
- **Action** — Track the cycle length: break only on cycle length 1, raise the budget (10 is still sub-millisecond), and print a stderr warning naming the cycle length if the loop exits without a true fixed point. Measure-only until then; a warning is a truth/reporting fix and is allowed under the freeze.

### F55 · save_state is a truncating non-atomic overwrite with no backup; a corrupt state file gives a raw traceback and no recovery path

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

save_state (hoops.py:490-492) is a non-atomic truncating overwrite — open(path,"w") then json.dump, with no temp-file-plus-os.replace, no fsync, and no rotation — and load_state (483-487) checks only os.path.isfile and lets json.load raise, so a truncated or empty state file surfaces as an unhandled JSONDecodeError (main() guards only BrokenPipeError). draft_state.json is gitignored, and a repo-wide search finds no backup or recovery routine. A process kill, Ctrl-C, or full disk during the dump therefore leaves an unreadable (at typical draft sizes, empty) state file. This is a hardening gap, not loss of the draft record: the Yahoo draft room and the conversation's per-pick mirror lines remain authoritative, and SKILL.md §4 RESYNC exists …

- **Evidence** — $ python3 scripts/hoops.py draft turn "Nikola Jokic; Victor Wembanyama" --top 1 # 2 picks logged $ python3 -c "d=open('ds.json').read(); open('ds.json','w').write(d[:len(d)//2])" # simulate an interrupted write $ python3 scripts/hoops.py draft turn "Shai Gilgeous-Alexander" --top 1 File "/usr/lib/python3.11/json/decoder.py", line 353, in raw_decode obj, end = self.scan_once(s, idx) json.decoder.JSONDecodeError: Unterminated string starting at: line 8 column 17 (char 93) $ ls -la | grep ds → one file, no backup …
- **Action** — Write to `STATE_PATH + '.tmp'`, fsync, then `os.replace` onto the real path (atomic on POSIX); keep the previous version as `STATE_PATH + '.bak'` before each replace; and catch ValueError in `load_state` to print 'draft state is corrupt — restore from draft_state.json.bak or use RESYNC' instead of a traceback.
- **Owner question** — Should the tracker also append a plain-text one-line-per-pick journal alongside the JSON, so a corrupt state can be replayed without needing the draft room open?


---

## LOW — Process & gates

### F56 · 'Republish to the artifact URL' is the definition of done, but nothing verifies it and the Routines' tool grant does not list the publishing tool

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

The republish close-out is written but never mechanized, and it is asymmetric between the two Routines. SEPTEMBER-PLAN §6.5 (October) and SKILL law 1d both instruct a session to confirm the published header reads fresh-today, but §4 (September) has no such line, and nowhere in the system is the confirmation an assertion: build_deck.py ends at "safe to publish" (line 146) and no code or prompt re-reads the artifact and compares its build-manifest `built` date to today. Separately, both Routines fire fresh sessions in env_0125yK1hVXJZsPssmPjhED1r whose stored session_context.allowed_tools (an auto-captured list identical across all ~40 triggers in the account, led by "preset:default") does not name Artifact; whether preset:default supplies …

- **Evidence** — SEPTEMBER-PLAN.md:100-102 and :151-154 ('republish the deck artifact to the EXISTING URL ... pass it as `url`; republish is part of the definition of done'). list_triggers job_config for both Routines: session_context.allowed_tools = ['preset:default','Task','Bash','Glob','Grep','Read','Edit','MultiEdit','Write','NotebookEdit','WebFetch','TodoWrite','WebSearch','BashOutput','KillBash','Skill','Tmux','Monitor','SendUserFile','REPL'] — no 'Artifact'. Artifact action:list confirms the target is live and owned: 'Draft …
- **Action** — Add a mechanical close-out to both Routine prompts and to §4/§6: after republishing, WebFetch the artifact URL and assert the returned HTML's build-manifest `built` date equals today, then paste that assertion into the owner report. Also confirm now that the Artifact tool is available in env_0125yK1hVXJZsPssmPjhED1r, and if it is not, write the fallback (send the owner the file via SendUserFile plus explicit …
- **Owner question** — Do you want a hard rule that if republish fails, the session pushes a notification saying the deck is STALE — rather than reporting the run as complete?

### F57 · Documentation-truth cluster: RESEARCH.md, README.md and SKILL.md describe an engine and a pool that no longer exist

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

data/RESEARCH.md is stale against the 2026-07-12 owner ruling and against the current pool. RESEARCH.md:7 states "*-recovery = 0.7x, *-risk = 0.85x" where hoops.py:284-310 applies 0.0 (full exclusion from every board) and 0.78; RESEARCH.md:26-28 lists Tatum, Haliburton, Kyrie, VanVleet and Lillard as "discounted 0.7x by the engine" when all five are now tagged *-risk in players.csv:79-83; and RESEARCH.md:1,4 call the pool "top-210 / ~210" against 246 rows. Because SKILL.md:12 cites RESEARCH.md as the method-of-record, a session that reads the cited source rather than the SKILL body could describe the recovery rule to the owner backwards. Scope corrections to the original finding: SKILL.md and docs/draft-deck.html:363 both state the engine …

- **Evidence** — data/RESEARCH.md:1,4,7 ('top-210', '~210 fantasy-relevant players', "'out-*' = excluded, '*-recovery' = 0.7x, '*-risk' = 0.85x") and :26-28 vs scripts/hoops.py:289-310 ('*recovery* -> 0.0: serious-injury recovery; excluded from all boards', '*risk* -> 0.78', 'recovery-flagged players are REMOVED from the pool, not priced'). $ wc -l data/players.csv -> 247 (246 rows + header). README.md:42 'draft init --teams 12 --size 15 --slot 4' vs SKILL.md:31 '13-player rosters ... 156 total picks'; measured $ hoops.py draft …
- **Action** — One editing pass before access ends: correct RESEARCH.md's pool size, multipliers, and the recovery paragraph to match hoops.py:289-310; change README's draft init example to --size 13 and state 156 picks; unify the pool-size wording (say 'the pool is whatever players.csv holds — currently 246' rather than a number that rots). Optionally have build_deck.py assert that RESEARCH.md's stated multipliers match the …

### F58 · Draft-night arena intel is computed on the frozen October-2025 pool, and the SKILL's skip rule references a timestamp the files do not contain

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md:33's "Consult arena intel" step contains three false provenance statements, but the intel it produces is not materially wrong. Confirmed: (a) arena.py:39 hard-defaults to the frozen arena/data/players_2025-10-21.csv, so the artifacts never track the live pool — SKILL.md's stated rationale "go stale with every pool refresh" is false for the pool half (true for the engine half); (b) both JSONs are git-tracked committed evidence, not "gitignored scratch artifacts" — .gitignore's own comment says so, citing LESSONS lesson 13, and arena/README.md:16 repeats the same stale claim; (c) the "~10 min" budget is ~75s measured (slots 67s + cadence 7.5s). Two corrections to the original finding: the skip rule does NOT resolve to "always skip" …

- **Evidence** — arena/arena.py:39 default data path 'os.path.join(ARENA_DIR, "data", "players_2025-10-21.csv")'; arena/README.md: 'Own frozen dataset ... the 2025 rookie class (Flagg, Edgecombe, Harper, Bailey, ...) and no 2026 rookies.' $ python3 -c "json.load(...)" -> slot_intel.json top keys ['champ_pct','best_per_slot']; cadence_intel.json top keys ['drafts','seed','slots'] — no date/stamp field in either. $ git ls-files arena/results/ | grep json -> both files are tracked (SKILL.md:33 calls them 'gitignored scratch …
- **Action** — Either (a) stamp both JSONs with the snapshot date and the engine SHA at write time and have the SKILL check that field, or (b) simpler and more honest: rewrite SKILL step 1 to say these are 2025-snapshot structural intel (snake rhythm, slot shape) that does NOT track the live pool, drop the regeneration from the pre-draft checklist entirely, and read the committed files. Fix the 'gitignored' claim either way.

### F59 · REVERT-MAP's first kill switch is stale — GRAD_SLOTS=0 no longer turns off the deck's ordering

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

REVERT-MAP's front kill-switch table is stale on its deck half: the row "Slot-gated gradient ordering | set GRAD_SLOTS = 0 in arena/arena.py AND docs/draft-deck.html | gradient ordering off everywhere" still reaches its advertised end state, but for the wrong reason on the deck side. The 2026-08-04 decw ship (d5ac587) made the deck's Top-5 order `ds` alone (draft-deck.html:2335), so GRAD_SLOTS has exactly one reader left in the deck (2309) and it feeds only the council score that becomes `fs` — whose sole consumer is the display span at 2551. Since strategyScores returns the full pool regardless of gradK, GRAD_SLOTS=0 changes neither Top-5 order nor membership in the deck; it remains fully live in the arena (arena.py:317,560). The table …

- **Evidence** — REVERT-MAP.md:13 (kill-switch table row) vs draft-deck.html:2314-2320 comment ('the Top-5 ORDER is the validated blend50 score at every seat — replacing the composite fs sort AND the slot-1-3 gradient gate ... fs is retained on rows for tooltips and REVERT-MAP rollback') and :2335 '.sort((a, b) => b.ds - a.ds || ...)'. GRAD_SLOTS survives at arena.py:65,317,560 and draft-deck.html:988,2309 — in the deck its only reader is the councilTop scoring call at 2309. One real snag in the accurate switch: reverting to …
- **Action** — Update the REVERT-MAP kill-switch table row to say GRAD_SLOTS=0 affects the arena and the deck's fs/tooltip metadata only, and that the deck's Top-5 ordering is governed solely by the decw kill switch below. Add the name tiebreak to the decw revert recipe so a rollback does not break parity determinism.

### F60 · SEPTEMBER-PLAN §3's validation requirements name artifacts that do not exist as runnable code

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

SEPTEMBER-PLAN §3 restates the gauntlet/mutation-suite requirement as an imperative without carrying lesson 13's [UNREPRODUCIBLE] tag, so a September session reading §3 alone would not learn the harness is un-backfilled. The underlying gap — uncommitted validation harnesses whose input states live at a dead /root/.claude/uploads path and whose runners hardcode os.chdir — is ALREADY REGISTERED as LESSONS.md lesson 13 and T7, with backfill explicitly queued for the September run. The parity half of the claim does not hold: parity here means deck-baked JS z-values vs the Python engine (findings_2026-07-30_ninecat_math.md:30-31), it reproduces exactly from committed artifacts alone (246 rows / 2214 cells / 0 mismatches), and build_deck.py …

- **Evidence** — $ grep -rn 'PARITY' /tmp/freshclone -> exactly one hit: arena/results/SEPTEMBER-PLAN.md:62. build_deck.py's only outputs are the 'deck built:' and 'safe to publish' lines (build_deck.py:143-146). $ ls arena/mocks | grep -i 'gaunt|mut|render' -> nothing. audit_2026-07-31b_deck_integrity.md:43-45: 'Render gauntlet — 130 states, 10 invariants ... Every owner-turn state of mocks 16-25 (10 drafts x 13 rounds), booted through the shipped app block' — the states from finding #2.
- **Action** — Commit two runnable scripts before access ends — scripts/parity_check.py (loads the deck's PLAYERS + a Python reimplementation of decwScores over committed states, exits non-zero on any ordering disagreement, prints exactly 'PARITY: EXACT MATCH') and arena/mocks/render_gauntlet.py — and make build_deck.py invoke the parity check as gate 4 so it cannot be skipped by omission. If they cannot be built in the time left, …


---

## LOW — Skill / live protocol

### F61 · Adding a missing player's row mid-draft silently re-bases every value the tiebreak and the NN% are computed against

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Because z-scores are standardized over the top-156 draftable fixed point (scripts/hoops.py:272), the §9 remedy of adding a missing player's row to data/players.csv between turns re-bases every value on the board. Measured: adding two starter-quality rows at overall ranks 36/37 changed 245/246 existing values (max |Δ| 0.161z, mean 0.058z) and produced 12 genuine reorderings of ≥3 slots (the "48-52 moved ≥3 ranks" figure is inflated by the mechanical 2-slot insertion offset and is not evidence of distortion). Adding sub-replacement rows changes nothing, so the effect is confined to genuinely draftable additions. The decision-relevant consequence is narrower than a value-level shift implies: the healthy-vs-risk tiebreak compares two …

- **Evidence** — Loaded scripts/hoops.py as a module, built the board from `data/players.csv`, then from a copy with two added draftable rows (a 16/10.5/1.9blk big and a 19/6ast guard, landing at overall ranks 40 and 37). Result: 241/241 players changed value; max |Δvalue| 0.1394, mean 0.0548; 48 players moved ≥3 ranks; top-8 order unchanged. Control: adding three sub-replacement rows changed nothing (max |Δ| 0.0) — confirming the effect only appears when the added player is inside the replacement-anchored draftable set, which is …
- **Action** — State the bound in §9 ("adding a draftable row shifts all values by up to ~0.14z; treat pre-edit and post-edit numbers as different scales"), or better, add a `draft turn --add "Name"` path that logs the pick as a named UNKNOWN with a placeholder value and defers the CSV edit to after the draft.

### F62 · Practice drafts are systematically distorted: 28 live-pool players — including the entire 2026 rookie class — can never be drafted by the bots

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

`arena.py live` runs a mixed pool: bots draft from the frozen 2025-10-21 snapshot (213 players after the recovery exclusion) while the owner's card prices from the live CSV (241 draftable), and the cross-pool guard at arena/arena.py:505-519 checks only the snapshot-minus-live direction. 34 draftable live-pool players therefore can never be taken by a bot. The consequential ones are not the rookies but six elites healthy in 2026 and `*-recovery` in the snapshot — Haliburton (#6), Kyrie (#9), Tatum (#15), Lillard (#22), Dejounte Murray (#67), VanVleet (#70) — which sit on the owner's board at every turn of every practice draft; the recovery half of this is already registered as a realism caveat in arena/README.md:95-103. Of the 2026 rookie …

- **Evidence** — arena/arena.py:505-519: the guard computes `missing = [p for p in pool_all if p['player'] not in live_names]` — snapshot-minus-live only. Set difference computed directly: live pool 246, snapshot 220; |live − snapshot| = 28 (list above), |snapshot − live| = 2 (Jamie Jaquez Jr., Jonas Valanciunas). arena/arena.py:43-45 pins the bot pool to `data/players_2025-10-21.csv`; the user's card comes from `scripts/hoops.py draft turn`, which reads `data/players.csv`.
- **Action** — Extend the cross-pool guard to warn in both directions and print the count of live-only players, and either map live-only players onto the snapshot for bot consideration or make the skill state plainly that practice drafts under-draft the live-only set (naming the rookie class).

### F63 · Pre-draft checklist timings are wrong in both directions and its skip-condition is unexecutable

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Three arena runtime figures in the docs are wrong by roughly an order of magnitude, in both directions, and reproduce on demand. fantasy-basketball SKILL.md:33 tells the pre-draft checklist that regenerating arena intel takes "~10 min — launch in the background"; measured end-to-end it is 73.6s (slots --seasons 1500 --rotations 3 = 66.7s; cadence --drafts 60 = 6.9s), so the background-launch instruction buys nothing. In the other direction, draft-arena SKILL.md calls `tournament --seasons 200 --seed <n>` "~2s" and big runs "cheap (~2s per tournament)", and tells the maintainer to re-verify with `--seasons 100 --seed 1` "in ~2s"; measured 38.8s and 26.0s. arena/README.md:34 repeats "~2 seconds" for a 1-rotation/1-seed board that measures …

- **Evidence** — Timed on this machine: `arena/arena.py slots --seasons 1500 --rotations 3` → 69.2s rc=0; `cadence --drafts 60` → 7.2s rc=0; total 76.4s vs "~10 min". `tournament --seasons 200 --seed 1` (defaults --seeds 3 --rotations 3) → 38.8s; `--seasons 100 --seed 1` → 25.7s; the "~2s" figure corresponds to a single 1×1 cell (measured 4.4s with `--seeds 1 --rotations 1`), not to the command as written. JSON contents: `slot_intel.json` keys = ['champ_pct','best_per_slot']; `cadence_intel.json` keys = ['drafts','seed','slots'] — …
- **Action** — Correct all three timing claims to measured values, drop the background-launch instruction (run it inline, it is 76s), and have `slots`/`cadence` stamp `generated_at` plus the pool file's mtime/hash into their JSON so the skip-condition becomes checkable.

### F64 · Protocol hygiene: dead skill reference, --expect contradicted by the tool's own prompt, and zero test coverage of the live-draft protocol

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

Three cosmetic-to-minor hygiene gaps in the instruction set, all reproduced but none load-bearing. (a) /home/user/yahoo-fantasy-basketball/.claude/skills/fantasy-basketball/SKILL.md:60 points at "the claude-council skill"; the installed skill is `council` — a stale name carried since the initial-release commit, resolvable in one step because `council`'s own description lists "claude council" as a trigger phrase. (b) /home/user/yahoo-fantasy-basketball/arena/arena.py:527-529's practice-mode pause banner and .claude/skills/draft-arena/SKILL.md:12 both state the two-call turn without `--expect`, so the banner is weaker than the rule it echoes. This is a missed redundancy, not an open hazard: the banner never appears in the real draft (which …

- **Evidence** — .claude/skills/fantasy-basketball/SKILL.md:60 "the claude-council skill owns the deliberation"; `ls ~/.claude/skills` → `council` (no claude-council). arena/arena.py:527-529 prints `⏸ pick #N is YOURS — get the card with: python3 scripts/hoops.py draft turn "" then log with draft turn "my:Name"; re-run live after.` — no `--expect`; .claude/skills/draft-arena/SKILL.md:12 likewise. LESSONS.md lesson 1 is the incident that made `--expect` mandatory. evals/evals.json: `{"skill_name":"fantasy-basketball","evals":[3 …
- **Action** — Fix the skill name to `council`; add `--expect <n>` to arena.py's printed prompt and to draft-arena step 0; add three live-draft evals (a turn feed producing a correctly formatted card, a SYNC request, a RESYNC from a pasted list) so the protocol has at least smoke coverage before October.

### F65 · The turn card's "helps" annotation prints negative z as help, and targets the categories the same skill says count for little

`NEW` · verdict **PARTIALLY_CONFIRMED** · *measured*

In scripts/hoops.py only (both `draft best` at :649-654 and the `draft turn` card at :875-879), the two weakest kept categories are annotated with the literal word "helps" followed by the candidate's raw signed z, so a candidate who hurts the category is labeled as helping it (reproduced: "helps 3PTM:-1.8 ST:-0.5" on a card whose owner ranked 12th in 3PTM). The mislabel is cosmetic rather than informational: fmt_row prints the same signed z for those exact categories earlier on the same row, so the annotation is always a verbatim duplicate of visible, correctly signed data, and the card carries several other fit signals (full z vector, vs-field ranks, feasibility, LEAN, stack tags). Separately, "weakest" is chosen by lowest own-roster …

- **Evidence** — scripts/hoops.py:876-879 `if weakest: line += " helps " + " ".join(f"{c}:{p['z'][c]:+.1f}" for c in weakest)` — no sign or threshold filter; identical code at :650-653 for `draft best`. Live card from a 55-pick slot-5 draft, my next pick #68, weakest TO/FT%: "3. Jayson Tatum … helps TO:-1.1 FT%:+0.3", "4. Austin Reaves … helps TO:-1.2 FT%:+1.9", "6. Damian Lillard … helps TO:-1.1 FT%:+2.7". Same card's `vs field:` line: FT% 12, TO 12 — both categories already last of 12. `grep -rn "helps" arena/results/*.md …
- **Action** — Filter to positive z (or print `hurts` for negatives) and pick the annotated categories by contestedness (rank 4–9 vs the field) rather than by lowest z-total. Both are one-line changes; the second is a display-only fix and allowed under the freeze.

### F66 · §1 and §3 give flatly contradictory position rules for 120 of 156 picks, and the round-11 rule prescribes the measured losing pathology

`KNOWN-PARTIAL — T1` · verdict **PARTIALLY_CONFIRMED** · *measured*

SKILL.md §1 (line 31) tells the executor to "weigh position need heavily" through rounds 1-10, while §3 (line 35) says "Position enters the call only as (1) a hard feasibility check ... and (2) a tiebreaker between near-equal candidates." §3 states the general direction ("Winning potential overrides position balance," council-ratified 5-0; echoed in §6), but §1's deep-draft rule is not named inside that ordering, so the two paragraphs read in tension and a one-line cross-reference in §1 would remove it. The finding's stronger claims do not hold: (a) §1's round-11 clause actually reads "extend the user's leads OR RESCUE WINNABLE CATEGORIES" — the finding truncated it and then proposed adding language already present, so the clause does not …

- **Evidence** — .claude/skills/fantasy-basketball/SKILL.md line 31 (§1 deep-draft dynamics) vs line 35 (§3 winning-potential rule). Reconstructed precedence, with the undefined links marked: recovery exclusion (absolute, engine-enforced) > feasibility guard ("hard") > [UNDEFINED: healthy tiebreak vs winning potential — §6 says soft rules are "subordinate to winning potential" but §3's tiebreak explicitly overrides a flagged player who wins on category fit, so inside the ~5% band the tiebreak in fact outranks winning potential] > …
- **Action** — Add an explicit numbered precedence list to §3 covering all seven rules including §1's deep-draft dynamics, and rewrite §1's round-11 clause from "extend the user's leads" to "rescue winnable categories and add flexibility; surplus in categories already won ~75% of weeks counts for little" (which is what the measurement supports). Resolve the healthy-tiebreak-vs-winning-potential link explicitly.
- **Owner question** — Do you want position need weighted through round 10 at all, or was that superseded when the council ratified 'winning potential overrides position balance'?


---

## Refuted on verification — do not re-raise

- **[domain] The injury haircut and recovery exclusion were calibrated on a zero-streaming instrument and applied to an …** — I reproduced every mechanical citation, then found the finding's two load-bearing assertions — its novelty claim and its impact direction — are contradicted by the repo's own registered evidence. WHAT REPRODUCES (all true, none novel): - hoops.py:285-311 availability() is exactly as described: `out-*`->0.0, `*recovery*`->0.0, `*risk*`->0.78, with the streaming sentence in the docstring. - arena.py:332-338 …

- **[data] The 'unsigned-fa-monitor' convention is dead: 8 free agents on the board, zero flagged, and James Harden …** — Reproduced the raw evidence, then refuted the thesis on four independent grounds. VERIFIED TRUE: `grep -rn "unsigned-fa-monitor"` returns only .claude/skills/fantasy-basketball/SKILL.md:35, data/RESEARCH.md:25, arena/results/report_2026-07-12_live_arena_x3.md:79/105/184 — no CSV row, no consuming code; `python3 scripts/hoops.py rank --top 260` reproduces all 8 FA board ranks verbatim (Brogdon is a 9th FA row, …

- **[data] A second published board (docs/cowork-vs-artifact.html) ships a 220-row pre-June-2026-draft pool outside …** — The mechanical evidence reproduces exactly, but the defect it is offered as proof of does not exist. I parsed the embedded array at docs/cowork-vs-artifact.html:597: 220 rows, Dybantsa absent, Jokic FG% z=3.060917 vs 2.55981 at docs/draft-deck.html:1183. Diffing against data/players.csv (246 rows) confirms the whole 2026 class is missing (Dybantsa, Peterson, Boozer, Caleb Wilson, Queen, Acuff, Steinbach, Jakucionis, …

- **[deck] teamWeekModel weights category variance linearly in the lineup weight, where the mean's weighting implies w²** — Read the cited lines (arena/arena.py:357-358 exact; deck mean line is 1018, not 1017) — the code fact that mean uses w and variance uses w is real and parity is exact. But the substantive defect claim fails three independent checks I ran. (1) Magnitude: I loaded arena.py, ran run_draft over 5 seeds x 12 teams and recomputed team_week_model with `w*w` substituted. Mean team-sd ratio code/w-squared = 1.0149 (p95 …

- **[arena] The shipped slot-gated gradient (+12.67pp, live in arena.py AND the deck) reverses sign to −7.19pp in a room …** — I re-ran the described design against the unmodified engine and could not reproduce either the sign inversion or the impact mechanism. 1) SIGN INVERSION NOT REPRODUCIBLE — IT GOES THE OTHER WAY. Own harness importing arena/arena.py unmodified; CRN-paired (identical draft rng and identical season rng per cell, arms differing ONLY in the council seat's grad_k via param_overrides); 6 seeds x 3 slots = 18 cells; 1,500 …

- **[arena] 'CRN-paired' overstates the precision actually gained — the repo's own paired SE equals its unpaired SE — and …** — Recomputed every cited SE from mock34_cf_out.json champ_blocks — all reproduce (ARM0 sd 0.9603/SE 0.2264; ARM1 paired SE 0.2278; ARM3 paired SE 0.2264; ARM2 block SE 0.0959), and arena.py:375 simulate_seasons does draw a roster-independent stream, so the CRN label is literally true. But the finding's central computation mixes arms: sqrt(0.960^2+0.407^2)=1.043 pairs ARM0's sd with ARM2's sd and then compares it to …

