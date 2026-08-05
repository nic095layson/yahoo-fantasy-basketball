# Scoring-model audit — how Yahoo H2H 9-cat actually scores, and where the system was wrong (2026-08-05)

**Owner-directed** ("research how fantasy basketball scoring works — provide
full understanding report, and that your system is calculating correctly…
for my real season winning production — and also season simulation for mock
drafts"), with two owner-supplied league facts treated as ground truth and
confirmed against Yahoo's documentation: (1) every filled starting slot
(PG, SG, G, SF, PF, F, C, C, Util, Util — Util is any position) contributes
100% of that day's stats to the weekly total; (2) BENCH is a pure holding
state — a monster game on the bench counts 0%.

Produced by an 8-agent research+audit workflow (3 web researchers on
primary Yahoo sources, 3 code auditors who re-ran the math in-repo, 1
daily-schedule Monte Carlo, 1 synthesis). Evidence: MC harness committed at
`arena/mocks/daily_lineup_mc.py` → `arena/results/daily_lineup_mc_out.json`
(deterministic, seed 20260805+mock).

## 0. The direct answer

**The system was NOT calculating the daily way. It froze ONE weekly
lineup: 10 starters counted 100% of all their games; the 3 bench players
counted at a flat 0.15 weight all week. There was no daily rotation and
no plug-in.** The measured reality (§3): a daily-managed 13-man roster
starts ~99.4% of ALL its played games — the effective "bench weight" is
≈0.975, not 0.15 — because on a typical night only ~5.3 of 13 rostered
players have a game, against 10 open slots. The schedule binds; the slots
almost never do.

## 1. How Yahoo H2H 9-cat scoring works (EVIDENCE, primary sources)

- **Weekly matchup**: each week you face one manager; EACH of the 9
  categories is one win/loss/tie decided by weekly team totals; the
  category record (e.g. 6-2-1) adds to season standings; standings rank
  by win% with ties worth half a win (Yahoo SLN6212, SLN35744).
- **FG%/FT%** are computed from weekly TEAM totals — makes ÷ attempts
  pooled across your started players, never an average of player
  percentages (SLN6920). **TO inverted**: fewer wins (Yahoo 9-cat guide).
- **Daily lineups**: default "Daily – Today"; each player locks at his
  game's tip-off; ONLY active-slot players earn stats; a bench player
  with a game fills any eligible open slot that day at full value
  (SLN22673/SLN6775, SLN28136). Exactly the owner's two ground-truth
  facts.
- **Playoffs** (public default): top 6 after week 21, weeks 22–24, top-2
  seeds byes, higher seed advances on ties (SLN6776, SLN6539).
- **No games-played caps in H2H** — the practical constraint is the adds
  limit (public default 4/week) (SLN6784, SLN6981).
- Schedule shape: NBA teams play 2–5 games/fantasy week, mostly 3–4
  (E[G]≈3.3), alternating heavy/light nights (verified-secondary).

## 2. What the system already gets RIGHT (audited, math re-run in repo)

- **hoops.py value engine**: exact Yahoo 9-cat set; TO inversion correct;
  **FG%/FT% volume-weighted impact exactly as Basketball Monster's
  standard** ((pct − league pct) × attempts); z-pool standardized over
  the draftable top-156; hand-recomputation matched the engine to 0.0
  across all 9 cats.
- **arena.py season sim**: category-record standings accumulation
  (18 wk × 9 = 162 cat-games); pooled weekly team percentages with a
  binomial variance floor; mu scales exactly as games × per-game rates;
  Yahoo's default top-6/byes bracket; TO inversion verified (P=0.999 for
  a 45-vs-83 TO gap); **the instrument is symmetric** — 12 identical
  rosters score champ% 7.8–9.2 vs 8.33 expected, no seat bias.
- **Deck weekly model**: a constant-for-constant exact port of the python
  reference, with the recorded 182/182 JS–python parity gate.

## 3. The central gap, quantified (EVIDENCE, committed MC)

Daily-schedule Monte Carlo on two real rosters (mock 39 slot 4; mock 34
slot 8 with six C-eligibles), 2,000 weeks each, deterministic:

| Readout | m39 roster | m34 roster |
|---|---|---|
| Fraction of ALL played games that got a slot | **0.9943** | **0.9942** |
| Top-10-value players | 1.0000 | 1.0000 |
| Bench-value trio | **0.9753** | 0.9751 |
| Worst single player | — | WCJ (C-only behind 5 C-eligibles) **0.945** |
| Static model's bench weight | 0.15 | 0.15 |

Weekly counting totals understated by the static model: **+8–23% raw
(+14–30% schedule-matched) per category**, skewed toward the bench trio's
signature stats (m39: BLK +19.9%; m34: 3PTM +23.0%). The static model
also understates TO by the same mechanism (+12–19%) — bench games carry
turnover cost too.

Why: 13 players × ~3.31 games × ~0.88 availability ≈ **5.3 candidates per
night for 10 slots**. A daily manager benches almost no one; only
same-day same-family collisions (mostly C on heavy nights) ever sit a
player, and even a 6th center starts 94.5% of his games.

## 4. Other confirmed gaps (registered, not all fixed today)

1. **Injury haircut is a verified no-op for most flagged players**
   (hoops.py): zero sits at the draftable-pool MEAN, not replacement, so
   `adj_value`'s multiply-if-positive guard leaves 19 of 30 risk-flagged
   players (LeBron, Embiid, Zion…) with exactly zero penalty in rounds
   ~6–13. Standard practice prices missed games as replacement-fill.
2. **Trade/matrix/vs ignore availability**: verified live — trading for
   0.0-availability Jimmy Butler reports "+3.03 you win on raw value"
   with no flag.
3. **No games-played/schedule dimension in the data**: flat 3.5
   games/week for everyone; 2-game and 5-game weeks are invisible, which
   practitioner consensus calls the single biggest weekly factor.
4. **No streaming/waivers/IL in the sim** (frozen rosters; public
   leagues default 4 adds/week), no NBA-team correlation, no per-category
   ties, random re-pairing instead of a round-robin (EV-neutral,
   verified), and the arena's own AI seats still draft with the old
   z-sum scorer rather than blend50 (grader/advice mismatch).
5. **Sum-of-z headline** is not the H2H objective (Rosenof's G-score
   critique) — mitigated in-tool by ECW/pwins, punts, and the vs views.

## 5. What this means

- **(a) Real-season weekly production**: do NOT read the old weekly mu,
  ECW levels, or trade net-z as absolute predictions — counting totals
  ran 8–23% low with roster-shape-dependent skew. The fix (instrument
  v2, shipped with this report) replaces static weights with measured
  daily-fill start rates.
- **(b) Mock-draft season sims**: all 12 seats shared the same error
  through one code path (symmetry verified), so RANKING conclusions
  between builds largely survive — with the registered exception that
  depth-vs-top-heavy comparisons were systematically distorted (the
  m34 six-center failure is this bias at its extreme), injury-heavy
  builds were graded too harshly while priced too generously at draft
  time, and stacking/streaming effects are invisible.

## 6. Bounds

- Yahoo help-page citations are the workflow researchers' verified-primary
  sources; schedule-shape and throughput figures are verified-secondary
  (practitioner data), and the MC's game-count distribution is an
  assumption stated in the harness docstring.
- The MC greedy-fills by season value daily — real managers are at least
  this good (they also stream), so 0.9943 is a floor-ish estimate for a
  managed roster, not a ceiling.
- Ordering/instrument consequences are measured separately (instrument
  v2 change note + panel re-derivation, same date).
