# E22 measurement — lineup-resilience (SLF) ordering: right diagnosis, wrong knife (2026-08-05)

**Owner-directed study** ("come up with a computative, data researched
formula… to strengthen fantasy model", 2026-08-05), executed measure-first
under the freeze and the E21 screening law. The owner's hypothesis: build
rosters that BEST fill the weekly starting lineup — positional balance plus
productive plug-in depth for when starters miss games.

Regenerate: `python3 arena/mocks/e22_measurement.py` →
`arena/results/e22_measurement_out.json` (per-mock partials committed);
seed-robustness: `python3 arena/mocks/e22_seedcheck.py`. Per-turn cards:
`arena/results/e22_replay_m{21,22,24,25,26,31,32,34,35,36,37,38,39}.json`
(current deck blocks + the E22 SLF driver; formula in the harness
docstring, registered before any simulation ran).

## 0. What the system already models, and what it did not (EVIDENCE)

- The weekly lineup model — 10 slots (PG SG G SF PF F C C U U), bench at
  0.15, per-player availability tiers (0.88 / 0.75 risk / 0.60 recovery)
  in both mean and variance — has been in the season sim
  (`arena.team_week_model`) and the deck engine since 2026-07-23; the
  deck's ΔECW ordering half has consumed it since blend50 shipped
  (2026-08-04).
- NOT modeled anywhere before today: **replacement dynamics** — when a
  starter misses games, his production is simply lost; the bench player
  who would start those nights stays at 0.15. Plug-in depth had no
  channel to be priced. The owner's hypothesis names a real gap.

## 1. The formula measured (SLF — stochastic lineup fill)

```
a_p = weekly availability;  K = 128 deterministic CRN draws
draw k: p active iff hash(name_p, k) < a_p
        greedy-fill the 10 slots among ACTIVE players (same order/priority)
s_p = P(p starts | p active)          w_p = s_p + (1 − s_p) · 0.15
```
`w_p` replaces the static weight inside the ΔECW half only; the value
half and blend are untouched. A bench guard behind an injury-flagged
starter gains weight; a 4th center behind healthy centers keeps ~0.15.

## 2. Result vs the registered bar: DO NOT SHIP — incumbent stands

Arms per mock, one CRN-paired 18,000-season set each (seeds 11/23/47 ×
6,000): baseline (as drafted) / shipped-follow / resil-follow.

| Mock | Punt | Baseline | Shipped | Resil | Δ (resil−shipped) |
|---|---|---|---|---|---|
| 22 | REB/BLK/FG% | 0.22 | 6.14 | 6.14 | 0.00 (#1 never diverges; identical rosters) |
| 31 | FT%/3PTM/TO | 6.16 | 15.87 | 15.87 | 0.00 |
| 32 | FT%/3PTM/ST | 4.11 | 0.01 | 0.01 | 0.00 |
| 34 | FT%/3PTM/PTS | 9.52 | 0.00 | **10.07** | **+10.07** |
| 35 | FT%/AST/3PTM | 7.11 | 7.71 | 6.87 | −0.83 |
| 36 | FT%/3PTM/TO | 31.18 | 27.66 | 27.31 | −0.36 |
| 37 | FT%/TO/3PTM | 19.04 | 11.84 | 12.52 | +0.68 |
| 38 | FT%/3PTM/PTS | 16.46 | 29.46 | **34.24** | **+4.79** |
| 39 | FT%/3PTM/TO | 33.98 | 6.45 | **30.53** | **+24.08** |
| 21 | — | 26.73 | 45.04 | 18.90 | **−26.14** |
| 24 | — | 29.66 | 32.15 | 8.41 | **−23.74** |
| 25 | — | 29.00 | 44.88 | 44.88 | 0.00 |
| 26 | — | 22.61 | 29.58 | 29.83 | +0.25 |

Registered bar (harness docstring, written before the run):
- **(a) non-regression on m21/24/25/26 (tolerance −1.5pp): FAIL** —
  m21 −26.14, m24 −23.74.
- **(b) punted-set win (≥5 of 9 AND mean > +1.0pp): FAIL** — wins 4 of 9
  (m34, m37, m38, m39); mean +4.27 passes, the count does not.

Per the bar: the incumbent static-fill ordering stands. No engine change
ships from this study.

## 3. Where the two orderings actually differ (EVIDENCE)

The #1 recommendation diverges ONLY in rounds 11–13, at 24 of 169
replayed turns across the 13 mocks — never earlier. SLF is inert until
bench competition exists. Every large champ% swing above traces to one
to three late-round player substitutions:

- **m39 (+24.08):** ONE player — resil takes Aaron Nesmith at pick 124
  where shipped ends up with Tobias Harris. (Shipped-follow collapses
  far below the owner's real 33.98, to 6.45; resil-follow lands 3.45pp
  below it — within the noise band — the m37/m39 lesson that full-follow
  autopilot ≠ advice.)
- **m34 (+10.07):** the measured mechanism is two substitutions — resil
  takes Brandin Podziemski over Wendell Carter Jr. at 137 and keeps
  Jalen Green where shipped adds Jusuf Nurkic at 152 — and the result
  beats BOTH shipped (0.00) and the as-drafted baseline (9.52).
  Separately, at turn 152 the resil CARD's top-2 (Anthony Black, Alex
  Caruso — the registered smoke case, vs shipped's 5/5-C-eligible Top-5)
  confirm the card-level fix, though neither player enters any arm's
  roster.
- **m21 (−26.14):** resil swaps Lendeborg → Ryan Rollins (124), Wendell
  Carter Jr. → Ayo Dosunmu (141), Sochan → Kelly Oubre Jr. (148) —
  three frontcourt pieces become guards/wings on a roster whose lineup
  needed the frontcourt.
- **m24 (−23.74):** resil swaps Kyle Filipowski → Andrew Nembhard (121)
  and takes Kelly Oubre Jr. at 145; shipped's Sochan/Harris path keeps
  the balance.

**The dual-instrument readout settles the pre-flagged caveat: the
collapses are not an artifact of the static-fill grader specifically —
both week models score the m21/m24 resil rosters as worse.** (A
misspecification SHARED by both fill models — they differ only in the
weights — would fool both together; E22c's real-data calibration is the
arbiter for that residual.) Scoring every final roster's ECW under BOTH
week models (static fill and SLF fill):

| Roster | ECW static (ship/resil) | ECW SLF (ship/resil) | agree? |
|---|---|---|---|
| m34 | 3.950 / **4.699** | 3.869 / **4.428** | both say resil better |
| m39 | 4.463 / **4.958** | 4.385 / **4.711** | both say resil better |
| m21 | **5.548** / 4.946 | **5.398** / 4.870 | both say resil WORSE |
| m24 | **5.130** / 4.641 | **5.008** / 4.496 | both say resil WORSE |

The pre-flagged caveat ("the static-fill grader may under-reward
resilience") is REFUTED for these four rosters: even the SLF instrument
scores the m21/m24 resil picks as worse. The resil ordering made
genuinely bad calls there, not differently-graded good ones.

## 4. Seed robustness of the four big swings (EVIDENCE)

Re-simulated on a disjoint seed set (101/103/107 × 6,000):

| Mock | Arm | seeds 11/23/47 | seeds 101/103/107 |
|---|---|---|---|
| 21 | shipped / resil | 45.04 / 18.90 | 45.86 / 18.54 |
| 24 | shipped / resil | 32.15 / 8.41 | 32.03 / 8.86 |
| 34 | shipped / resil | 0.00 / 10.07 | 0.02 / 9.68 |
| 39 | shipped / resil | 6.45 / 30.53 | 6.47 / 31.12 |

Every gap reproduces within ~1.2pp (max: m21 at 1.17pp) on seeds the
original run never saw (regenerate: `python3 arena/mocks/e22_seedcheck.py`
→ `arena/results/e22_seedcheck_out.json`). The four big swings are real
properties of those rosters under the instrument, not CRN artifacts —
one late-round player really is worth ±24pp to this simulator in these
rooms (a statement about the instrument's tail sensitivity as much as
about the players; see §6).

## 5. Reading (INFERENCE, marked as such)

The static greedy fill is a SHARP slot-scarcity signal: a candidate who
cannot start scores 0.15, one who fills a hole scores 1.0. SLF smooths
that signal with injury draws — which is exactly right at the saturation
extreme (m34's sixth center, m39's tail) and exactly wrong where the
roster still has a REAL hole: injury draws let redundant guards borrow
partial starts, the Δ gap between "fills the hole" and "5th guard"
shrinks, and the position-blind value half tips the blend toward the
redundant pick (m21, m24). Bias–variance in one sentence: SLF fixes the
knife-edge's catastrophes and blunts the knife everywhere else.

Two consequences worth registering, neither shippable today:

- **E22b (September candidate): penalty-only / guard-rail SLF.** Apply
  SLF as a saturation CHECK, not a re-ranking: keep the static ordering
  unless the static Top-5 is ≥4/5 one position family in R10+, and only
  then re-rank those five by SLF. Precision note (verified 2026-08-05):
  that signature is the measured **m34** signature only (turn 152 is
  5/5 C-eligible); m39's rescue turn (pick 124: Gafford/Lendeborg/
  Nembhard/Buzelis/Coulibaly) does NOT match it, and no trigger
  condition capturing m39 is currently known. Must re-clear this
  study's full 13-mock panel. *Postscript, same day:* E22b was
  owner-directed and measured immediately — it FAILED its bar
  (`e22b_measurement_out.json`: captures only +1.28 of m34's rescue,
  fires on m21's poison turn for −24.96, wins 1/9); the shipped answer
  became the display-only LINEUP CAP warning. See the SEPTEMBER-PLAN
  E22b resolution line.
- **E22c (September, data): calibrate the fill model against reality.**
  The owner's uploaded weekly breakdowns (games played per week) are
  ground truth for how his lineups actually filled. Fitting BENCH_WEIGHT
  and the availability tiers to that data decides which week model is
  closer to the world — the correct arbiter between the two instruments,
  and a better use of the hypothesis than any untested re-ranking.

## 6. Bounds

- Full-follow arms measure each ordering as an autopilot; the owner's
  real drafts beat both arms on m32, m36, m37, m39. Advice ≠ policy.
- Single-player champ% swings of ±24pp under CRN pairs confirm the
  ledger's standing lesson on tail sensitivity. Single-mock deltas at
  the ~1–3pp placebo scale (the bar's registered design assumption)
  should never drive ship decisions — and this author's wider judgment
  (marked as such, post-hoc) is to distrust anything under ~5pp on a
  single mock; the count criterion exists for exactly this reason.
- The grading instrument still carries the static-bench blind spot for
  ROSTERS NOT IN THIS PANEL; §3's dual readout settles the four big
  cases only. E22c is the principled fix.
- Convergence detail on the three 0.00-delta punted mocks (corrected
  after adversarial verification — an earlier draft called all three
  "byte-identical cards", which the replays refute): m22 — the #1 never
  diverged (lower card ranks differ at picks 107/110) and both arms
  drafted identical rosters; m31 — the #1 diverged once (pick 153) but
  both follow arms still drafted the same roster; m32 — the arms drafted
  rosters differing by one player (Lendeborg vs D'Angelo Russell at pick
  135) that TIED at 0.006% champ, a decided comparison that dead-heated.
  The win-count sample is therefore seven decided comparisons (one a
  tie) plus two convergent mocks. Recorded as-is; the bar was registered
  on all nine and is applied as registered.
