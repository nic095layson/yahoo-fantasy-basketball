# Self-critique, round 2 — what closed, what remains, what's new (2026-08-04)

**Owner's request:** "see what has been addressed, and provide a new set of
weaknesses you see in your system" — follow-up to
`analysis_2026-08-04_self_critique.md` (T1–T7 + asks), written earlier today
before the three-season league data, the ΔECW ship, and the named room.

**Method:** each original item graded against artifacts produced since
(findings/reports in `arena/results/`, shipped deck code, profiles.json),
with the evidence file named per claim. New weaknesses ranked by how much
they could change an October outcome. Claims are marked EVIDENCE (measured
in this repo) or INFERENCE (my reasoning on top).

**Headline:** the two items I called the deepest weaknesses this morning —
the misaligned objective (T1) and the wrong room (T3) — are substantially
closed, both shipped and validated today. What remains clusters around one
theme: **the system is now well-calibrated to a world it still partly
invents** — its own weekly model (N1), its own market board (N2), and its
own point-estimate projections (N3). The single highest-value item the
owner can still provide is weekly category records from any past season.

---

## 1. Scorecard on the original list

| Item | Verdict | Evidence |
|---|---|---|
| T1 — objective misaligned with H2H | **CLOSED (in-sim), guard armed** | E9 blend50 shipped: 14/14 ledger mocks improved, mean +11.6pp, 0 winner regressions, fresh-seed replicated, JS↔Python parity 182/182 (`findings_2026-08-04_decw_round2.md`). Kill rule: 2 consecutive out-of-sample failures → revert (REVERT-MAP "decw-ordering") |
| T2 — simulator-conditional grades | **NARROWED, not closed** | Owner delivered 3 real seasons; season-level variance validated ~10%, playoff format corrected (8/12, no byes, 1-wk rounds) (`league_intel_2025-26.md` §4–5, §10–11). Weekly grain still unvalidated → **N1** |
| T3 — room model is not your room | **LARGELY CLOSED (deck); arena half open** | Named room shipped: smoke 5/5 slots, owner-card parity 7/7 byte-identical, scaled reach 11/11, Spearman 0.936 (`findings_2026-08-04_e18_named_room.md`). Open: market geometry (→ **N2**), arena-side refit E17, absolute reach bar re-arms at October ADP |
| T4 — projections: single-source, no variance | **OPEN — now the oldest unaddressed weakness** | Unchanged: 246 hand rows, no variance column, 14 rookie rows. Margin progress: returnee audit + E19 (`report_2026-08-04_injury_returnees.md`); owner authorized September multi-source synthesis (Q14) → **N3** |
| T5 — grades picks, nobody grades the plan | **MOSTLY CLOSED via T1, as predicted** | ΔECW saturates: marginal value →0 in won AND lost cats. EVIDENCE that it steers builds: round-1 raw ΔECW spontaneously rediscovered punt-declaring (`findings_2026-08-04_decw_round1.md`); blend50 regularizes it. Residual: still greedy per-pick, no multi-round lookahead |
| T6 — my inductions overreach at small n | **STRUCTURALLY OPEN; mitigations holding — one new instance to disclose** | All recent overreaches caught pre-publication. NEW: E18's pre-registered absolute ±8 bar failed 7/11 and I re-scoped it to a scaled band in the same session I shipped (§3, N6) |
| T7 — smaller items | **MIXED** | Settings assumption RESOLVED (owner Q1–Q9: exact cats, exact roster slots); mock-harness backfill DONE (season_sim_mock10–30); punt-mode chip curve and `ar/fx/sy` consumption still open |

**The asks (priority order from round 1):**

1. League history — **DELIVERED beyond the ask** (three seasons: standings,
   final rosters, full draft boards) — *except weekly category records*,
   which remain the one missing piece and are now ask #1 again.
2. Exact settings — **DELIVERED** (Q1–Q9: 9 cats exact, daily lineups,
   unlimited moves, daily FFA waivers with game-time locks, IL+ never
   drafted for, no keepers, snake, October).
3. Returning opponents — **DELIVERED beyond the ask**: complete 12-manager
   identity map across all three seasons, → profiles.json → shipped room.
4. Draft logistics — PARTIAL: October confirmed; slot TBD (Q8).
5. Risk preference — ANSWERED (Q13: price-tolerant, takes fallers).
6. Projection sources — ANSWERED (Q14: synthesize my own; "secret sauce").
7. ΔECW authorization — GRANTED (Q15) and shipped same day.

## 2. The new weaknesses, ranked

**N1 — ECW is validated at the season grain, never at the weekly grain.**
The shipped objective is half ΔECW, and ΔECW is a readout of
`team_week_model`'s CV constants (PTS 0.30 … BLK 0.75, PCT_MIX_INFL 1.15) —
still research estimates, never fit to observed weeks. The three-season
data validated season-LEVEL variance (~10%), but many different weekly
models produce the same season table (INFERENCE — under-constraint, not
proof of fit). If real weeks are swingier in the percent categories than
modeled, the card systematically over-prices FG%/FT% stability; if counting
cats are streakier, it under-prices them. **This is the sharpened T2 and
the deepest remaining weakness.** Close: Yahoo's weekly scoreboard history
(per-week matchup lines, any season, even screenshots) → fit CV constants
to reality → re-run the E9 validation on the refit model.

**N2 — The market geometry is 0.45× reality.** Measured today via the Noah
anchor: the synthetic market board diverges from our value board only ~45%
as much as the real Yahoo board did in 2025-26 (EVIDENCE:
`findings_2026-08-04_e18_named_room.md`). Consequences: simulated rooms
cannot reproduce real board texture — the real room produced Embiid-R7,
Kawhi-R7, Tatum-R13 falls our sims will never generate — so mock reps
under-train exactly the faller decisions the owner is best at (Q13), and
BUY NOW/survival timing is arena-conditional until October. Fix is known
and scheduled (real-ADP sync at final refresh); until then every mock's
survival read carries this asterisk.

**N3 — Projections are still point estimates (T4 carried, now compounding).**
Today's returnee work made the cost concrete: one scalar (0.78) is the
entire difference between Haliburton-as-top-12 and Haliburton-as-round-4,
and a flat 0.78 prices 36-year-old Lillard's Achilles like 26-year-old
Haliburton's (EVIDENCE: `report_2026-08-04_injury_returnees.md`). No
variance column means the card cannot express floor-vs-ceiling at equal
mean — the owner's stated risk preference (Q13) is still unexpressible in
the math. Every downstream number (ECW, reach sims, chips) inherits these
point guesses. September synthesis (Q14) + E19 + a variance column are the
scheduled fixes; until then this is the oldest open weakness.

**N4 — blend50's α=0.5 knife-edge is a misspecification smell.** α=0.4
craters m29 (12.67→1.02), α=0.6 regresses m25 (40.42→20.23); 0.5 is the
only tested-clean value (EVIDENCE: `findings_2026-08-04_decw_round2.md`).
INFERENCE: a well-specified single objective shouldn't need a razor-balanced
mixture of two proxies — the value half is compensating for raw ΔECW's
concession spiral, which suggests a properly regularized ECW (coverage
prior, or risk-adjusted pwin) could dominate both and be robust in α. Not
urgent — the kill rule guards it — but it is the deepest remaining
computational question, and the honest reading is that blend50 is a very
good patch, not a final answer.

**N5 — The draft is graded as if the season ends at the draft.** The real
league runs 27–83 moves/team on daily lineups; the three-season data shows
the two steadiest performers (Martin: champion at 87 moves; Will: top-2
mover every year, finishes 3/6/2 off mediocre drafts) out-working their
drafts (EVIDENCE: league_intel §10–12). In this league, part of a draft's
value is the CHASSIS it leaves for streaming — bench flexibility, schedule
density, stash tolerance — and the engine prices none of it. Champ% is
labeled a no-streaming bound in the plan (E16), but the card's draft-night
advice still silently assumes static rosters. Scope decision pending:
minimum viable is a bench-flexibility tilt; the full streaming model is a
September scope call the owner owns.

**N6 — Process: a pre-registered bar was renegotiated in-flight.** The E18
absolute ±8 reach bar failed 7/11; I diagnosed a geometry cause (Noah
anchor), defined a scaled band, passed 11/11, and shipped — all in one
session. The reasoning is documented and I believe it is right; it is ALSO
exactly the T6 failure shape (moving a goalpost under momentum), and it
deserves to be named rather than buried. Standing rule going forward: a
pre-registered bar may be re-scoped only with (a) a written validity
argument, (b) a re-arm date for the original bar — E18 has both (October
ADP) — and (c) **two re-scopes of the same bar = the bar failed, full
stop.** Related: the MANAGERS constants (noise values, loyalty discounts
18/10, streamer penalty 40/15) are hand-set at n=3 seasons; they passed
the aggregate reach validation, but no individual knob has been isolated.

**N7 — The capability cliff is now the binding constraint.** ~5–6 days of
Fable remain; September's hardest work (E14 real-bracket re-baseline, N1
weekly refit if data arrives, E17 arena refit, judgment re-authoring at
every republish) will be executed by whatever capability is available
then. INFERENCE: the marginal value of the remaining Fable days is highest
spent making September mechanical — pre-building the E14 bracket harness,
scripting the weekly-record ingest so it is run-and-read, and keeping
SEPTEMBER-PLAN executable without judgment calls — rather than spent on
new features.

## 3. Bounds

- This critique, like round 1, is self-graded — the same reasoning layer
  that produced the system produced this list (T6 applies to it).
- All "closed" verdicts on T1/T3/T5 are in-simulator or in-replay closures;
  N1 is the standing caveat on every one of them.
- Weekly-record availability in Yahoo's UI is assumed, not verified — if
  the league page doesn't expose past weekly scoreboards, N1's ask needs a
  different source (screenshots during the season, or accepting the bound).

## 4. Decision sheet (owner disposes)

1. **Weekly category records** — the one data item still worth chasing
   (closes N1). Any season, any format, even partial.
2. **N7 allocation** — approve spending remaining Fable days front-loading
   September mechanics (E14 bracket harness now, ingest scripts now) over
   new features. My recommendation: yes.
3. **E16 streaming scope** — minimum (bench-flexibility tilt in September)
   vs full streaming model. My recommendation: minimum, measure, decide.
4. **N4 exploration** — register E9b (single-objective regularized ECW,
   measure-only, same ship bar as E9) for September. No engine risk until
   it beats blend50 on the full ledger + fresh seeds.
5. **Draft slot** (Q8) — send when Yahoo assigns it.

## 5. Provenance

Produced by the same Fable session that shipped E9/E13/E18a and the
returnee dossier (2026-08-04); all cited artifacts are in `arena/results/`
at this commit. Volatile claims re-verify via: reach/geometry —
`findings_2026-08-04_e18_named_room.md`; blend50 — `findings_2026-08-04_decw_round2.md`;
league facts — `league_intel_2025-26.md`; returnees —
`report_2026-08-04_injury_returnees.md`.
