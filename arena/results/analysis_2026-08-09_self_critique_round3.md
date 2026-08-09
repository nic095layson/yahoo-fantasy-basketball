# Self-critique, round 3 — the domain-semantics audit (2026-08-09)

**Owner's request (2026-08-08):** "a system wide, self critical and analytical audit… we found
many gaps in your system knowledge of Fantasy basketball (such as not knowing bench players have
same impact of starter players), as well as Dylan Harper being listed as a rookie… I want for
your comprehension and the Draft Deck tool to be in pristine operational condition."

**Method.** Seven parallel domain audits — fantasy semantics, data layer, Python engine, Draft
Deck, skill/protocol, arena instrument, process/gates — each instructed to skip anything already
registered as E1–E23/E9b, T1–T7, N1–N7, or LESSONS 1–14. Every finding was then handed to an
**independent adversarial verifier instructed to refute it**, with instructions to default to
REFUTED on any evidence it could not personally reproduce, and to flag a registered item
reported as NEW as a defect in the finding. 79 agents (7 auditors + 72 verifiers). The repo was
not modified during the audit; all reproductions ran in `/tmp` scratch copies.

**Result.** 72 findings entered verification. **6 refuted. 66 survived** — 4 CONFIRMED outright,
62 PARTIALLY_CONFIRMED (real, but the verifier narrowed the claim; the narrowed wording is what
this report carries). 48 NEW, 18 exceeding the scope of an item already registered.
**6 high · 31 medium · 29 low.**

**Headline.** The previous two self-critiques (2026-08-04) found *modeling* weaknesses — the
objective, the room, the projections. This round found a different shape, and it is the shape
the owner pointed at: **the system is calibrated to a league it partly mis-describes, and the
mechanisms built to catch that certify dates rather than work.** The computational layer remains
clean; nothing in this audit contradicts a shipped validation number. What it contradicts is
several of the *premises* those numbers were computed under.

Claims are marked EVIDENCE (measured in this repo during the audit, reproduction cited) or
INFERENCE (reasoning on top). Every quoted number below is EVIDENCE unless marked otherwise.

---

## 1. The two owner-found defects, generalized

Both were domain-comprehension failures: internally consistent, confidently wrong. Both turned
out to be instances of a class, not one-offs.

### 1a. Bench value — and a correction to this session's own first answer

`BENCH_WEIGHT = 0.15` (`arena/arena.py:52`, `docs/draft-deck.html:830`) prices any player who
cannot claim one of the ten daily lineup slots at 15% of production. Under DAILY lineups that is
badly wrong, but **the first two derivations this session produced were also wrong**, and the
correction matters more than the original claim:

- **Withdrawn:** "your 41.7 games/week means you started 92% of everything you rostered." The
  41.7 figure is real (`arena/data/weekly_matchups_2025-26.csv`, weeks 1–18 excluding the
  All-Star double-week) but it is **confounded by streaming** — 64 in-season moves. A *static*
  13-man roster simulates to 36.0 games/week. The GP column is evidence the roster is dynamic
  (E16/N5), not evidence about bench weight.
- **Withdrawn:** "the correct weight is ~0.92." `team_week_model` already multiplies every
  player by `g = 3.5 × availability`, so `BENCH_WEIGHT` must carry **only** the slot-competition
  loss. 0.92 double-counted the injury haircut on exactly the last three picks.
- **What survives**, measured over the 144 rosters the system itself drafts, 18 weeks each, at
  the real NBA pace of 3.23 team-games/week (`arena/mocks/bench_share_fit.py`, committed with
  this report): start-share conditional on having a game is **0.997 for roster ranks 1–10 and
  0.953 for ranks 11–13** — a **relative weight of 0.956**, i.e. the shipped constant is
  **~6.4× too low**. An independent verifier measuring the same quantity with a different
  schedule generator got 0.998 / 0.971 → 0.973 (6.5×). Both land in the same place: slot
  competition costs the last three picks **4–5% of their games, not 85%.**

The consequence is not cosmetic. EVIDENCE, reproduced by the verifier at 12 seeds × 12 teams ×
13 rounds:

| Measurement | 0.15 (shipped) | 0.85 (test) |
|---|---|---|
| Arena picks changed | — | **461 / 1872 (24.6%)** |
| Rounds 11–13 picks changed | — | **243 / 432 (56.2%)** |
| `team_week_model` PTS μ | 563.9 | 663.1 |
| Best-to-worst room PTS spread | 207.0 | — |
| 12-team PTS ranking reordered | — | **12 / 12 drafts** |

The mis-weight is worth ~99 PTS/week against a best-to-worst roster gap of 207 — roughly **half
the signal the season simulator exists to resolve**. On mock 34 at 3 seeds × 3,000 seasons,
raising it moves the owner seat from **9.30% → 16.00% champ, 4th → 2nd** (room Spearman 0.916).
This is not a common-mode shift that cancels across teams.

**It also inverts a registered experiment.** E22 is registered to *add* a positional-saturation
term to `decwScores`, on the premise that the bench discount is correct and under-applied. Under
daily lineups, positional saturation costs **0.5–3% of games** — a 13-man roster fills only
~6.5 of its 10 daily slots, so the constraint the machinery prices barely binds. INFERENCE: the
saturation term will not clear its bar. That prediction is pre-registered here, dated, before
the measurement.

### 1b. Rookie tags — an append-only law with no retirement half

The `MUST_HAVE` completeness law (`SKILL.md:14`, `hoops.py:124-135`) forces each June class INTO
the pool and never retires the prior class or requires re-projection off its real season.

- Six 2025-draftees still carry `rookie-proj` for 2026-27: **Maluach, Fears, Demin, Tre Johnson,
  Coward, Clifford.** The tag's only consumers (`arena.py:189`, `deck:856`) apply a sign-aware
  ×1.15 market-hype multiplier; because all six carry negative market z-sums the division
  *improves* their estimated ADP by **12–21 slots** (Johnson 145→157, Coward 148→160, Demin
  151→168, Fears 158→179, Clifford 163→180, Maluach 220→235). Three land inside the 156-pick
  universe.
- **The sharper defect:** nine of eleven 2025-class rows are **byte-identical to the pre-debut
  October-2025 snapshot**. Their actual rookie season was never ingested. Harper's tag was
  cleared; his projection line was not. `MKT_PIN` still pins Flagg 18 / Harper 60 under a
  comment describing lottery-rookie name value.

---

## 2. The four failure classes

### Class 1 — Domain semantics: constants encoding a wrong belief about *this* league

Beyond 1a/1b: `SKILL.md:48` instructs the session to hand-weight swing categories, **the exact
rule the arena measured at −3.78pp**. Punt doctrine is imported from roto play — in an
each-category league every punted category is ~18 guaranteed losses of 162 and you need 5 of 9;
no punt surface states that arithmetic. `availability()` resolves free-text notes by unordered
substring: `"recovery"` is tested before `"risk"` and matches anywhere, so
`inj-achilles-risk (recovery on track)` silently deletes a player from every board — **and all
four re-entered returnees carry exactly that parenthetical shape**; conversely a season-ending
injury written in plain English (Brunson's `wrist-surgery-monitor`) gets no haircut at all.

### Class 2 — Gates that certify a date, not the work

The most dangerous class for October, because a weaker model will run the pipeline.

EVIDENCE, reproduced end-to-end on a scratch copy with no network and a byte-identical CSV:

```
$ python3 scripts/verify_rosters.py        → 246/246 checked, 0 mismatches   EXIT 0
$ python3 scripts/hoops.py freshness --stamp \
      --note 'AUDIT DRY RUN: I did zero research. No web search. No CSV edit.'
                                           → Freshness stamped: 2026-08-09   EXIT 0
$ python3 scripts/build_deck.py            → "safe to publish"               EXIT 0
```

The deck header then renders **"fresh today."** `verify_rosters.py:124` writes
`date.today()` unconditionally and, in fallback mode, never reads the evidence file's own `date`
(currently 2026-08-04). All three gates bottom out on a date the scripts stamp themselves.

Compounding holes: a pool row absent from the evidence file lands in `unmatched`, which is
**never** a mismatch — `Bronny James,ZZZ` exits 0 and passes both gates (`verify_rosters.py:115-117`;
`hoops.py:168` and `build_deck.py:52` read only `mismatches`), so **the rows most likely to be
wrong in October — newly added ones — are the exempt ones**. An unwired `--strict` flag already
exists at `verify_rosters.py:149-150`. `try_direct()` swallows every exception
(`verify_rosters.py:58-61`), making a transient network blip indistinguishable from a policy
block. And the deck's `JUDGMENT` layer sits outside every gate: byte-identical across 4 stamped
pulls and ~11 republishes, its `date: "2026-07-28"` never rendered, with one entry already
self-contradicting *inside a certified build* — Sochan reads "Unsigned after a limited NYK
title-run role" while the same file's pool row says POR.

**The defect demonstrated itself during this audit.** One auditor ran `verify_rosters.py` against
the working tree instead of its scratch copy. The only trace it left was
`data/roster_verification.json`'s `date` advancing **2026-08-05 → 2026-08-08** — a fresh
verification stamp produced by a process that consulted no source and changed no row. Nothing
warned; the file simply became a day's worth of "verified." Reverted before commit
(`git checkout -- data/roster_verification.json`), and recorded here because it is the exact
October failure mode: the artifact that certifies research is writable by anything that runs the
script.

The control worked where it was designed to: changing Jokic DEN→BOS in a scratch copy **is**
caught (`pool=BOS official=DEN`, exit 1). The evidence file carries real team assignments and
catches pool-side drift. What it cannot do is detect a real-world change after the day it was
last re-authored — and nothing forces re-authoring.

### Class 3 — Two boards, one draft, no precedence

- `docs/draft-deck.html:2335` sorts by punt-blind ΔECW `blend50`; `scripts/hoops.py:823` sorts
  by punt-aware `adj_value`. `grep -ci "decw|blend50|ecw" scripts/hoops.py` → **0**.
- Reproduced on the owner's own mock states via the repo's certified reference construction
  (`decw_card_v2.py`'s `pwins_total` + `team_week_model` + `pct_ranks`): **the two #1s differ on
  19 of 26 owner turns; mean Top-5 overlap 1.8/5**; on the declared-punt mock the deck's #1 sits
  as deep as **rank 39–41** on the hoops board.
- SKILL.md's live protocol commands `hoops.py draft turn` and says present candidates "straight
  from the `turn` card." The word "deck" appears **once** in SKILL.md, inside the publish-gate
  paragraph. README.md never mentions the deck or its URL. The owner confirmed on 2026-08-04
  that draft-day use is the deck.

45-second clock, the owner's screen showing one name and the chat another, and nothing written
anywhere resolves it.

### Class 4 — The live engine has never been stress-tested

Zero tests exist for the draft loop. EVIDENCE, all reproduced verbatim by the verifier:

- A feed segment of `.`, `-`, `'`, or a bare `my:` logs a **fabricated confirmed pick**:
  `draft turn "Nikola Jokic; .; -"` logs Jaren Jackson Jr. to T2 and SGA to T3 with a normal ✓
  mirror line. `my:` strips to `""`, which is a substring of all 246 names. Two existing guards
  (the surname-collision HALT and `--expect`) cover part of this, but any degenerate segment
  whose own top candidate is still on the board logs unwarned.
- **No Unicode normalization anywhere**: `Jokić`, `Dončić`, `Şengün`, `Porziņģis` fail every
  match stage in both the CLI and the deck and become UNKNOWN — after which `draft best` still
  recommends "Nikola Jokic" at #2.
- The fuzzy stage keys on the last whitespace token, which is the **suffix** for 14 players, so
  typo tolerance is dead for all of them — and `jacksn` resolves to a single candidate,
  **GG Jackson**, logged silently as a normal pick instead of Jaren Jackson Jr.
- `draft fix` prints the **new** name on both sides of the arrow (`old` binds a reference that
  is then mutated), so the correction echo SKILL.md §5 mandates can never verify anything.
- One of the owner's own picks logged as UNKNOWN silently under-counts `roster N/size`, the
  feasibility guard's `remaining`, and every category rank for the rest of the draft — observed
  "roster 3/13" on a 7-pick roster and "6 picks left" when 2 remained.
- `save_state` is a truncating non-atomic overwrite with no backup; the resulting corrupt file
  gives a raw `JSONDecodeError` traceback from every subcommand, and RESYNC has no mechanism.

### And the most owner-visible output has no calibration

Across the only full transcript of the confidence format (`report_2026-07-12_live_arena_x3.md`,
three complete drafts, 45 cards): the top candidate lives in a **50–88 band, mean 58.2**; the
spec's "95% = no contest" anchor was reached **0/45 times** — including pick #1 overall, where
Wembanyama at +13.00z with a >4z gap drew 88. Cards sum to 149–272 (45/45 over 100). The skill's
own ~5-point coin-flip rule fires on 32/45 turns and **8 of those 32 are missing the mandated
"(coin flip)" annotation — 75% compliance, by the strongest executor the system has run.**
Meanwhile the deck runs a second, unrelated coin-flip rule (`ds` gap ≤ 0.011, ~64% fire rate)
computed from a different quantity. Both surfaces are open in front of the owner on draft day.

---

## 3. Action items

Full evidence for every item is in Appendix A. Tiered by deadline, worked one at a time.

### P0 — while top-model access lasts

| # | Item |
|---|---|
| **A1** | **Fit the bench weight; do not hand-tune it.** Measured start-share (~0.96 flat, or the per-rank curve from `bench_share_fit.py`) applied identically in `arena.lineup_weights`, deck `lineupWeights`, and the ADP bot's −50 penalty. Moves ~25% of picks → belongs in the **September E14 re-baseline**, dual-reported exactly as `league_intel §4` dual-reported the bracket. Also fix `arena.py:236-239`: `bench_bound` short-circuits to False once 10 startable players exist, so the penalty fires only in an arbitrary middle-round window. |
| **A2** | **Make the rookie law symmetric.** Clear the six tags; re-project all nine frozen 2025-class rows from real 2025-26 production; add a `draft_year` column; add a `validate_pool` check that **fails the stamp if any `rookie-proj` row predates the most recent June draft**; rebuild `MKT_PIN` from consensus ADP with a build-time assertion that every hype-justified pin still carries a rookie note. |
| **A3** | **Name the authoritative draft-night surface** at the top of SKILL.md's live protocol, with the reconciliation rule; put the artifact URL in README.md. Doc-only. **Blocked on Q1.** |
| **A4** | **Make the gates certify work.** (a) fallback mode FAILS unless `EVIDENCE['date'] == today`; (b) wire `--strict` so `unmatched_count > 0` hard-fails; (c) record `players.csv`'s content hash in the manifest and fail unless it changed or the note asserts "no changes" with a source count; (d) gate 4 on `JUDGMENT` (keys exist in pool, `as_of` per entry, `JUDGMENT.date == fresh["date"]`); (e) log the `try_direct` exception; (f) print `PARTIAL VERIFICATION — evidence file, not an independent source` and stamp it in the deck header when `mode != direct-complete`. |
| **A5** | **Live-draft robustness pack** — twelve fixes in one commit, each independently revertable: substring-stage guard + HALT on >4 candidates; NFKD/ASCII fold; strip `jr\|sr\|ii\|iii\|iv` before the fuzzy surname; `old = dict(picks[idx])`; `--slot` range check above the UNKNOWN branch + `build_rosters` degrades instead of `KeyError`; persistent UNKNOWN banner + true pick count in `roster N/size` and `remaining`; `my:` snake-desync warning in `turn`; atomic `save_state` + `.bak` + a recovery message instead of a traceback; refuse appends past `teams × size`; per-row CSV coercion errors naming row and column; `draft resync` and `draft status --tail N`; **three live-draft evals — there are currently zero.** |
| **A6** | **Replace the hand-authored NN%** with the retired council-ratified `share-of-best · ±X.XX cats/wk` readout, or the blend50 percentile lead through a published table. Delete the "95% = no contest" language the record shows was never met. One coin-flip rule, one place. **Blocked on Q2.** |
| **A7** | **Deck empty-board scale bug.** `decwScores` returns raw `adjValue` on an empty board while consumers assume [0,1] percentiles → pick #1 renders **"lead +57.2 🚀"** and a tooltip reading **"ΔECW-blend 1100.3 … as pool percentiles."** In LIVE mode this renders for all twelve seats until the first opponent pick. One line: `pctRanks(vals)` in the fallback. Monotone; no ordering change. |
| **A8** | **Build-coherence strip.** Its `keptSum` argmax is algebraically "punt your lowest raw z-sum category" — rank-blind, suggests TO in 40.7% of single-punt states, reads **"⚠ WRONG TARGETS" in 79% of punted states**. Normalize by roster size, re-fit both cutoffs against the punted mocks per E21, gate Retarget behind `puntPath(...).clear`. |
| **A9** | **Commit a real parity harness.** SEPTEMBER-PLAN §3 and §6 both gate on `PARITY: EXACT MATCH` and **no such script exists**; the "130-state render gauntlet + mutation suite" exists only as prose. Commit `scripts/check_parity.py`, call it from `build_deck.py`. |
| **A10** | **Documentation-truth pass.** `RESEARCH.md` still documents the 0.7× recovery discount the engine replaced with exclusion; README's `draft init` example uses `--size 15` against a 13-slot league; REVERT-MAP's first kill switch no longer turns off the deck's ordering; the pre-draft checklist mis-states three timings and its skip-condition is unexecutable (the intel JSONs carry no `generated_at`). |

### P1 — September recalibration

| # | Item |
|---|---|
| **A11** | **Close N1 with the data already delivered.** `weekly_matchups_2025-26.csv` is read by **zero lines of code**. First measurement: FG% well calibrated (implied 1.08–1.11 vs `PCT_MIX_INFL = 1.15`, p ≈ 0.40); FT% directionally lower (0.86–0.94) but not rejected at the owner's attempt volume (p = 0.077–0.106, n=16–18); counting-cat dispersion light by ~1.1–1.65× in 3 of 7 cats once the two irregular weeks are excluded — **and roughly half the missing variance is the constant-3.5-games assumption, so fit games first.** Make it gate E9b rather than run parallel. |
| **A12** | **Re-scope E22 before building it** (see §1a). Reframe the positional layer as a hard feasibility check only. |
| **A13** | **Ledger reproducibility.** The unreproducible boundary runs **past** mock 26: `season_sim_mock27\|28.py`, `mock28_cf.py:17` and `format_delta.py:23-27` all read the vanished uploads path — which puts **LEDGER §5** (the m28 oracle pair, sole cited basis for E8 and E9) and **all four `format_delta` states** (entire measured basis for E14) inside the unreproducible set while both are quoted as artifact-derived. Also: lesson 13 says backfill is "queued for the September run"; SEPTEMBER-PLAN contains **zero occurrences of "backfill."** **Blocked on Q3.** |
| **A14** | **Widen the schema before the pool freezes** — `gp`, `min`, `age`, `adp`, variance. Derive availability from `gp` instead of note substrings. Add a team-budget check (fail if a team's summed FGA > ~92 or minutes > 240): the pool is well calibrated through roster rank 6 and inflates past rank 7 — MIL 125.4 FGA across 11 rows, WAS 126.5, HOU 121.8. **Blocked on Q4.** |
| **A15** | **Fix the practice room.** `cmd_live` and `run_draft_ordered` never pass `mkt`, so the only ADP persona degrades to `sum(z) + gauss(0, 4.0)` — **practice drafts and the committed `cadence_intel.json` contain zero ADP drafters**, and the degraded seat is the loosest bot in the cast (passes 18.4 board slots vs 6.4). Register with E17. Separately, 28 live-pool players including the entire 2026 rookie class cannot be drafted by bots in practice. |
| **A16** | **Retire or annotate `slot_intel`.** Cross-draft sd 6.89pp vs Monte-Carlo sd 1.05pp; 2–3 draws per cell (SE ~4pp), five zero-sample cells printed as `0.0%`, top-2 gap under 3pp at 10 of 12 slots. The console table carries the caveat; the JSON the skill reads does not. **Blocked on Q5.** |
| **A17** | **Harden `availability()` note parsing** — validated `status` column, or at minimum re-order the tests and require `-recovery` as a suffix. Print excluded players by **name**, not count. |

### P2 — October refresh and draft night

| # | Item |
|---|---|
| **A18** | **Allowlist `site.api.espn.com`, or hand-paste 30 full rosters once.** Until then the lock cannot detect a camp trade, waiver, or cut. **Blocked on Q6.** |
| **A19** | **Mechanical republish close-out:** WebFetch the artifact URL after republishing, assert the manifest's `built` date is today, paste the assertion into the owner report. Confirm the Artifact tool is granted to the Routine's environment. |
| **A20** | **No refresh is scheduled between the October Routine (~10-12) and draft night.** Add one. |

### Action item → finding map

Every action item traces to numbered findings in
`analysis_2026-08-09_findings_table.md`. Working an item means working its findings.

| Item | Findings |
|---|---|
| A1 bench weight | F07, F23, F47, F51 |
| A2 rookie law | F12, F14, F25, F40 |
| A3 draft-night surface | F03, F05, F37 |
| A4 gates | F01, F04, F15, F19, F35 |
| A5 live robustness | F02, F22, F26, F27, F29, F30, F31, F32, F36, F52, F53, F55, F61, F64 |
| A6 confidence % | F06 |
| A7 empty-board scale | F20 |
| A8 coherence strip | F17 |
| A9 parity harness | F46, F60 |
| A10 documentation truth | F18, F57, F58, F59, F63 |
| A11 weekly refit (N1) | F10, F21, F39, F50 |
| A12 E22 re-scope | F47 |
| A13 ledger reproducibility | F08, F34 |
| A14 schema | F13, F24, F41, F42 |
| A15 practice room | F11, F62 |
| A16 slot_intel | F09 |
| A17 note parsing | F16, F28 |
| A18 roster source | F01 |
| A19 republish close-out | F56 |
| A20 pre-draft refresh | F33 |
| P3 backlog | F38, F43, F44, F45, F49, F54, F65, F66 |

### P3 — 29 low-severity findings

Judgment layer inert while still printing `jdg −0.30` chips · 16% of turns have an exact #1/#2
tie broken by **reverse-alphabetical name** under the 🎯 marker · every deck tooltip is
mouse-only · the `helps` annotation prints negative z as help and targets the wrong categories ·
13 personalities in 12 seats denies each strategy one slot in every tournament · the z-score
fixed point can 2-cycle without warning · the injury haircut is a no-op below board rank 62 ·
`cmd_trade` ignores availability entirely (reports you *win* by acquiring a player valued at
+0.00) · SKILL.md §1 and §3 give contradictory position rules for 120 of 156 picks · adding a
player mid-draft re-bases every value by up to ~0.14z · dead `claude-council` skill reference.
All 29 with evidence in Appendix A.

---

## 4. Decision sheet (owner disposes)

1. **Q1 — On draft night, what do you read off:** the Draft Deck in the browser, or Claude's
   chat card? The protocol assumes the chat card; the engineering assumes the deck. Decides A3.
2. **Q2 — When you read "72%", what do you believe it is the probability of?** Decides whether
   NN% becomes share-of-best (normalized) or a standalone win-probability delta. Decides A6.
3. **Q3 — Do you still have the mock 10–30 `draft_state` JSONs?** If not, the September
   regression baselines must be re-drafted and the ledger becomes descriptive history.
4. **Q4 — Which projection source anchors the October re-ingest** (Hashtag / Basketball Monster
   / Yahoo preseason), and do you want a weeks-19–21 schedule-density column?
5. **Q5 — Do you use "best strategy for your slot" on draft day, or only cadence intel?** The
   former needs ~50 drafts/cell to mean anything.
6. **Q6 — Can `site.api.espn.com` be allowlisted before October?** If not, will you hand-paste
   30 full rosters once in early October?
7. **Q7 — How many of your 3 bench spots do you intend to churn weekly?** Decides whether the
   last rounds target upside stashes or high-games fillers; an input to A1.
8. **Q8 — Does the league have a Yahoo "max games played per position" cap?** Nothing in the
   repo records one. If it exists it changes the streaming math and A1's ceiling.

---

## 5. Refuted — do not re-raise

Six findings died on verification and are **not** claims against this system: the injury haircut
being mis-calibrated by the zero-streaming instrument; `unsigned-fa-monitor` being a dead
convention; `docs/cowork-vs-artifact.html` shipping a stale second board; `teamWeekModel`
weighting category variance incorrectly relative to the mean; the slot-gated gradient reversing
sign out of sample; and "CRN-paired" overstating the precision actually gained.

---

## 6. Bounds

- Self-graded, like rounds 1 and 2 — T6 applies to this document. The adversarial-verifier layer
  narrows that exposure (it killed 6 findings and corrected 62, including both of this session's
  own bench-weight derivations) but does not remove it.
- **Nothing here re-derives the shipped blend50 or E18 validation numbers.** Those remain
  [UNREPRODUCIBLE] per lesson 13, and A13 shows the unreproducible set is larger than lesson 13
  records.
- ESPN direct mode is network-blocked in this environment (`Tunnel connection failed: 403`), so
  every roster-verification claim describes fallback mode.
- The bench-weight measurements are static-roster simulations on the system's own drafted
  rosters. They deliberately exclude streaming, which is E16/N5's territory and would raise the
  effective weight further, not lower it.
- Severity tiers are my judgment of October cost, not a measured quantity.
- The N1 weekly-fit numbers rest on n=16–18 team-weeks from one team. Enough to move
  `PCT_MIX_INFL` off its hand-set value; not enough to fit nine constants well.

## 7. Provenance

Produced 2026-08-09 by a Claude Code cloud session on branch
`claude/fantasy-basketball-audit-i9pio4`. Harness: `Workflow` run `wf_aebf396a-35d`, 79 agents,
1,915 tool calls. The bench start-share measurement is regenerable from
`arena/mocks/bench_share_fit.py` (committed with this report per lesson 13). Volatile claims
re-verify via: bench weight — `arena/mocks/bench_share_fit.py` and `arena/arena.py:52`;
gate behavior — the three-command sequence in §2 Class 2; board divergence —
`scripts/hoops.py:823` vs `docs/draft-deck.html:2335`; confidence band —
`arena/results/report_2026-07-12_live_arena_x3.md`; weekly fit —
`arena/data/weekly_matchups_2025-26.csv`.
