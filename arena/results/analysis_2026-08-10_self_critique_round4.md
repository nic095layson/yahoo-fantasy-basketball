# Self-critique, round 4 — the regression audit (2026-08-10)

**Owner's request:** "conduct the same audit and system dial in and tune up performance
proposal" under the stronger model, with the standing instruction to "operate fully on
integrity guardrails. There were many issues from yesterday alone and that cannot happen."

**Method.** Identical architecture to round 3: six parallel domain auditors, every finding
handed to an independent adversarial verifier instructed to refute it. 48 agents. Three
deliberately different targets from round 3: (1) **regressions in the 2026-08-09 commits**
(`d3b4a49..e635809`) — the newest code is the least-audited code; (2) **independent
re-derivation of round-3's headline measurements** — a different model re-running the prior
session's numbers rather than trusting them; (3) the **next layer of domain comprehension**
with F01–F66 as the known baseline.

**Result: 42 findings raised → 1 refuted → 41 survived** (20 CONFIRMED outright, 21
narrowed). **13 are REGRESSIONS introduced by the 2026-08-09 commits** — 1 critical,
5 high. Full detail: `analysis_2026-08-10_findings_table.md` (R4-F01…R4-F41).

**The headline, stated against the author:** yesterday's fix-batches shipped with their own
defects, including one critical. The audit process caught its own author within 24 hours —
which is the process working, and also the reason it must keep running against every batch,
including the one that fixes these.

---

## 1. What re-verified clean (independent re-derivation, not trust)

- `bench_share_fit.py` → **0.997 / 0.953 / 0.956 exactly**.
- Lesson-13 integrity: **4/4** committed mock champ% regenerate at committed seeds.
- The 0-of-52 orderings control **reproduces** (both revisions node-executed).
- A17's "zero rows change" claim verified on **both** pools (live + frozen snapshot).
- Feature-freeze inventory verified clean: **zero ordering or availability-tier change** on
  current data from anything on `main`.
- Performance measured end to end: draft night ≈ **60 ms/turn**; no optimization warranted,
  none proposed (R4-F35 — a deliberate null result).

## 2. The E24 mechanism, solved (R4-F07)

Round 3 refused to ship the bench-weight correction because two proposed mechanisms were
refuted and the effect was unexplained. Round 4 found the mechanism: **`TEAM_WEEK_SHOCK`**
(the shared games-played shock, `arena.py` `simulate_seasons`) has a standard deviation that
scales **linearly** with the lineup weight while base weekly noise scales as **√w** — a
channel ECW is structurally blind to, because `pwins_total` uses only `team_week_model`
base variance. Decomposed at 2000×3 seeds, shock-on vs shock-off:

| Mock | Punt | Δchamp shock-on | Δchamp shock-off | Reading |
|---|---|---|---|---|
| 31 | yes | +7.28 | **+8.58** | real mean-level effect, shock partially masks it |
| 32 | yes | +1.70 | **+2.37** | same |
| 34 | yes | +6.53 | **+7.27** | same |
| 33 | **no** | +1.62 | **+0.42** | **~74% of the gain was the shock artifact** |

m33's fresh-seed "replication failure" (+1.17 → +0.48) matches its shock-free component —
the part that failed to replicate was the artifact part. Shock-off, the §7.4 punt
interaction **widens**: punted average +6.1pp vs unpunted +0.4pp. Per-category
decomposition concentrates the real gains in mid-probability contested categories (m34 REB,
m31 BLK/ST) while punted categories sit saturated near p≈0 where added μ changes nothing.

The round-3 no-ship call is vindicated, and E24 now has a measurable mechanism path
(registered as amendment G1 + experiments M1/M2/M3, §7 of SEPTEMBER-PLAN).

## 3. The regressions (all fixed in this batch, each with a red-first test)

| ID | Regression | Class |
|---|---|---|
| R4-F01 | **`resync`'s recovery promise is false** — it saves twice, so `.bak` holds the WIPED board; an empty paste destroys the live draft while printing a reassurance; SKILL.md codified the lie | **critical** |
| R4-F06 | The `<3-char` guard kills seven real name tokens — CJ, GG, Ja, AJ, PJ, RJ, VJ all log UNKNOWN; the parity fixture *blessed* the bug (`'aj' → []` as expected output) | high |
| R4-F05 | Gate 1b deadlocks: its own prescribed bypass (`--allow-unmatched`) only changes an exit code; the artifact still fails the gate — no sanctioned publish path for any rosterless pool row | high |
| R4-F21 | Gate 5's JUDGMENT orphan check is **dead code** — the regex can never match the actual deck; it shipped never having been seen to fire | medium |
| R4-F22 | Gate 4's quiet-day bypass is substring matching — any note containing "quiet" publishes an unchanged pool; and the gate is silently inert for exactly the next build (old manifest has no hash) | medium |
| R4-F24 | `--quick` silently overwrites the committed E24 evidence artifact — **a round-4 auditor did exactly this mid-audit** (restored); third occurrence of the artifact-protection failure class in two days | medium |
| R4-F23 | A17's leading-tag fix left **5 substring parsers alive** (`rec_ct`, `rec_compound`×2, market `risk`, deck mirrors) | medium |
| R4-F36 | F52's end-of-draft guard shipped Python-only — the deck still shows a phantom "your next: #164" | low |
| R4-F08/09/10 | The A3/A6 protocol surgery left seams: the live-turn I/O channel undefined; §3's "kept-z" not producible from the one allowed command (the card prints *adjusted* value — 22% off on risk rows); the ~0.25 near-tie band fires at 12 of 13 board depths (97% of adjacent pool gaps sit under it) | high |
| R4-F26/27 | draft-arena SKILL + arena README still mandate the retired "confidence card"; eval 4's premise contradicts its own expected output | medium |

## 4. New domain findings beyond regressions

- **Punt cost re-measured on the corrected instrument (R4-F03):** punt-declaring is still
  −EV at **−3.1 to −6.4pp** (t = −3.9 to −8.6, CRN-paired) — ~30% *less* than the
  "−5 to −11pp" the deck warns in four places. Direction survives, warning overstates.
- **Owner ruling registered same day:** the owner does not declare punts at all — "I only
  wait until the system calculates this and directs to full tilt when clear dominance over
  opponent rosters." The operative surface is concession *detection* (Soft Punt panel /
  drift latch), not declaration handling. E23's declaration-time framing is moot for this
  owner; the detect-and-direct path is the one that must be sharp.
- **The market model misprices centers ~2 rounds (R4-F04):** against the real 2025-26 board,
  C-eligible players go a mean **21.7 picks earlier in rounds 1–5** than `MKT_W` predicts
  (Jarrett Allen real #37 vs model #107). Draft-night survival chips inherit the optimism.
  Cross-validated refit direction: FG% weight up (0.5 → ~1.2–1.4), TO down (0.25 → ~0–0.4).
- **Playoff-week schedule density quantified (R4-F14):** a 3-vs-4-game week for one starter
  swings a 1-week playoff round's win probability by ±5.5–6.4pp in the sim's own model; a
  whole-team 3-vs-4 mismatch collapses it to ~0.11. Nothing in the October build can see
  weeks 19–21 density; the NBA schedule publishes mid-August and the schema window is
  September-only.
- **0.956 is a band, not a point (R4-F25):** teammate schedule correlation moves it to
  ~0.940, teammate absences to ~0.968. Every variant sits 6.2–6.5× above the shipped 0.15.
- **The published deck was 8 commits stale (R4-F02)** while the A3 doctrine names it the
  authoritative surface — resolved by this batch's republish ceremony.

## 5. Dispositions (owner-approved 2026-08-10, "approve all")

- **Batch R** (regression fixes R1–R8): fix + red-first regression test each.
- **Batch P** (protocol repairs): I/O contract per the owner's answer — *the owner feeds the
  pick stream to Claude pick-by-pick in addition to typing into the deck*; §3 quotes the
  card's adjusted value; the 0.25 band replaced by the measured interim (~0.03).
- **Batch D**: full legitimate refresh + republish to the standing artifact URL, through
  every gate.
- **Batch G**: registrations appended to SEPTEMBER-PLAN §7 (E24 shock arms + M1/M2/M3;
  E17/E18 center-bias prior; E23 corrected range + owner punt ruling; A19/A20 mechanization;
  playoff-density schema row; stash/IL+ truth lines; Q3 disposition; Q4 deadline).
- **Q3 (mock 10–30 states), owner delegated:** disposition = treat as lost. Mark LEDGER §5
  and the four `format_delta` states [UNREPRODUCIBLE]; September rewrites the E8/E9/E9b
  bars against the committed states (mocks 31–34 and any newer). Recorded in §7.
- **Q4 (projection source): still TBD** — must land before 2026-09-01 or the schema window
  closes with the synthesis unanchored.

## 6. Bounds

- Self-graded at the meta level, as every round: the same layer that shipped yesterday's
  regressions graded today's findings. The mitigations are the independent verifier layer
  (which killed 1 and narrowed 21) and the red-first test rule this batch executes under.
- The punt-cost re-measure ran at 500 seasons/cell on the 6-team bracket the instrument
  still ships; the full-scale re-run on the real bracket is registered, not done.
- The shock decomposition is at 2000×3 seeds; E24's re-baseline arms re-run it at full N.
- Two auditors modified committed artifacts during this audit (`bench_weight_study_out.json`
  via `--quick`, `cadence_intel.json` via a cadence run) despite read-only instructions —
  caught by `git status` and restored before any commit. Third occurrence of this class;
  R6's overwrite guard removes the sharpest instance.

## 7. Provenance

Produced 2026-08-10 on `claude/fantasy-basketball-audit-i9pio4` (restarted from merged
`main` at `e635809`). Harness: Workflow run `wf_0f20b710-830`, 48 agents, 874 tool calls.
Companion appendix: `analysis_2026-08-10_findings_table.md`. Re-verification numbers
regenerate via the same committed harnesses as round 3 (`bench_share_fit.py`,
`bench_weight_study.py`, `check_parity.py`, `test_draft.py`).
