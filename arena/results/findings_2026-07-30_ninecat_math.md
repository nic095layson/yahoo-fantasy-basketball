# The 9-CAT Math Dissertation — audit of the valuation engine and its measuring instrument (2026-07-30)

**Status: ANALYSIS ONLY. No engine, deck, or arena code was changed.** Every
proposal below is pre-registered and awaits (a) owner approval and (b) a
CRN-paired arena validation run, per the codification protocol.

**Method.** Five-agent workflow: line-by-line formula audit of
`scripts/hoops.py` + the deck JS port; instrument audit of
`arena/arena.py`'s season model; empirical structure analysis of the live
246-row pool; causal category-elasticity experiments (CRN-paired,
12,000 seasons per variant); one G-score draft pretest. A fifth
adversarial agent re-derived every load-bearing number with fresh code:
**all four majors CONFIRMED, one minor CORRECTED (definition caveat),
zero REFUTED.** All experimental code ran in the scratchpad; the repo was
read-only throughout. Companion chart artifact published alongside.

---

## 0. What the engine actually computes (verified inventory)

- **Percentage cats** are volume-weighted impact scores — already best
  practice: `imp = (pct − lg_pct) × attempts`, league baselines
  attempt-weighted (`hoops.py:231-235`); impacts sum to 0 by construction
  (verified 1.7e−13).
- **Counting cats**: population z over the pool; TO sign-inverted
  (`hoops.py:225-246`). Verified mean ≈ 0, std exactly 1 per cat.
- **Value**: `total_value = Σ z` over unpunted cats (hard exclusion);
  `adj_value = tv × availability` only when tv > 0 (0.78 risk haircut,
  0/1 otherwise) (`hoops.py:250-287`).
- **Deck parity**: JS z's are build-baked to 6 decimals; max deviation
  vs Python recompute = 0.0 over 246×9. `fitZ` is a reading lens only
  (retired from ranking 2026-07-28). `marketRanks` is a separate
  price model, shared verbatim with `arena.market_ranks`.
- **The league model** (`arena.simulate_seasons`): weekly H2H, 9 cats,
  Gaussian draws per cat from per-roster weekly mean/variance models,
  18-week season, top-6 playoff, fixed Yahoo bracket.

The foundation is sound: the two most common 9-cat valuation mistakes
(raw-percentage z's, no TO inversion) are **not** present. The four
majors below are one level deeper.

---

## 1. MAJOR — the z pool includes ~90 players who can never be drafted

z-scores are standardized over **all 246 rows** (`hoops.py:988`),
including 5 `av=0` stat lines and ~90 sub-replacement players; boards
filter to the 241 available only afterwards (`hoops.py:399`). The
draftable universe is ~156 (13 rounds × 12 teams). Standardizing over
non-draftable players shifts every category's mean and std by
+0.16–0.40σ (PTS mean 15.60 → 17.69 between pools).

**Effect (executed, confirmed independently):** re-standardizing over
the top-156 fixed-point pool (membership converges in one iteration,
zero top-100 membership flips, Spearman 0.998) reorders the **top-100 by
up to 14 ranks**: FVV 84→70, Dejounte Murray 80→67, Kessler 54→44,
Paul George 81→72, Tatum 25→20 rise; Poole 74→82, Morant 69→75, Jaylen
Brown 77→83, KD 16→21 fall. Mean |shift| 2.18 (top-100); 7 players move
≥ 6 ranks — more than half a draft round.

**ELI5:** the engine grades on a curve that includes ~90 students who
aren't in the class. Everyone's grade is measured against a fake
average, so mid-round players get mispriced by half a round.

## 2. MAJOR — the injury haircut taxes a number whose zero line is arbitrary

`adj_value = 0.78 × tv` costs a risk player `0.22 × tv` — and `tv`'s
level depends on the pool cut (over the 246 pool it's inflated; over
the top-156 pool the mean is ~0 by construction). FVV's total value is
**+1.17 in the 246 pool and −0.20 in the 156 pool** — same player, the
haircut flips from a real cost to nothing. Diagnostic: in the re-z
experiment, **every top-100 riser is risk-tagged and every faller is
healthy** — the current pool inflates the haircut for exactly the
discounted-vet cluster the timing layer works hardest to exploit.
Best practice applies risk multipliers to replacement-anchored value.
Fixing §1 largely fixes this for free (the 156-pool zero *is*
replacement level); it should be re-audited after.

**ELI5:** a 22% tax hurts more when the price tag was drawn against an
inflated baseline. The tax rate is fine; the price it taxes is wrong.

## 3. MAJOR (instrument) — the sim's FG%/FT% dice barely wobble

`PCT_WEEK_SD = 0.012` for both percentage cats (`arena.py:56,329-330`),
roster-independent. In-sim weekly attempt volumes (FGA 312–509, FTA
81–161) imply **binomial floors alone** of sd(FG%) 0.022–0.028 and
sd(FT%) 0.032–0.047 — 2–4× the modeled noise, before shot-mix variance.
Measured consequence: the better team wins FT% in a **median 99.4%** of
weeks (FG% 90.3%); a 0.043 FT% edge wins 99.4% in-sim vs ~78% at a
realistic sd. Percentage categories are near-deterministic coins.

**Downstream taint:** every %-cat conclusion the arena has ever
produced — FG%/FT% elasticities below, punt-% build grades, and part of
the neutral-weights +3.78pp headline — inherits this. Direction of past
results likely survives (they route mostly through counting cats);
magnitudes should be re-quoted after the fix.

**ELI5:** the sim flips a nearly two-headed coin for FT% every week.
Real leagues flip a much fairer coin — being slightly better at FT%
should win you *most* weeks, not *all* of them.

## 4. MAJOR (instrument) — the sim seeds playoffs by the wrong record

`simulate_seasons` accumulates a **weekly binary W/L record**
(`arena.py:363-368`); Yahoo H2H-each-cat standings accumulate the
**cumulative category record** (a 6–3 week adds 6 wins, not 1). CRN
experiment on identical rosters, identical regular-season draws, 20,000
seasons: swapping the seeding rule shifts playoff% by **+13pp
(safe_floor) to −29pp (specialist)** and champ% by ±4.5pp. Narrow builds
that squeak 5–4 weeks are over-seeded; broad builds that win 7–2 are
under-seeded. This is the same order of magnitude as the largest
strategy effect ever codified from the arena.

**ELI5:** the sim ranks teams like chess match points (win the week =
1 point, whether 5–4 or 9–0). Yahoo ranks by total categories won all
season — closer to goal difference. Different teams make the playoffs
under the two rules, and it's ±29pp different, not a rounding error.

---

## 5. Structure of the 9 categories (what the pool actually looks like)

- **Two opposed axes**: big axis FG%–REB +0.72, REB–BLK +0.69,
  FG%–BLK +0.53 vs guard axis FT%–3PTM +0.71, PTS–AST +0.64; cross-axis
  FG%–3PTM −0.63. **TO is a usage tax**, not a skill: corr(TO z, AST)
  −0.83, (TO z, usage proxy) −0.86.
- **Heavy tails**: BLK skew +2.42 / kurtosis +10.3, ST +1.36 / +4.4;
  FT% impact is the hidden tail (skew −0.65, kurt +5.7 — big-man FT
  drag). **3PTM is Gaussian** (skew +0.03) — the "scarce threes"
  intuition is not in this pool.
- **Replacement-level subtraction is rank-neutral** (a per-cat constant
  can't reorder a sum); the z-sum board is *structurally* robust to VOR
  correction — the pool fix (§1) is the real lever, worth ≤3 spots in
  the top 30 and up to 14 in the top 100.
- **TO column oddities (minor)**: two top-100 players sit there on the
  TO column alone (Cason Wallace #79, Gafford #94, TO z +1.15 each);
  all top-20 TO-z players are low-usage bench pieces. Contained, but a
  TO-weight sweep is a legitimate candidate (weight 0 moves Cade 14→6,
  Chet 11→30).

## 6. Category win-elasticity (what a +1z actually buys)

CRN-paired, mock-12 room, owner seat, +1 pooled player-σ per cat,
12,000 seasons per variant (verified at a fresh seed, all within 1.4×):

| Cat | Δchamp pp | Δplayoff pp | Note |
|---|---|---|---|
| AST | **+1.82** | +6.70 | most valuable z in the room |
| BLK | **+1.55** | +6.63 | |
| FG% | +1.25 | +4.84 | ⚠ inflated by §3 — re-measure |
| PTS | +1.20 | +6.23 | |
| REB | +1.09 | +4.28 | |
| TO | +1.08 | +4.77 | |
| ST | +0.89 | +5.07 | weekly-noise victim (see §7) |
| 3PTM | +0.88 | +5.43 | |
| FT% | +0.78 | +4.53 | ⚠ inflated by §3 — re-measure |

Max/min ratio **2.32** — the flat z-sum treats these as equal. The
counting-cat ordering (AST, BLK high; ST, 3PTM low) is instrument-clean;
the %-cat rows must be re-measured after the §3 fix before anything is
tuned to them.

## 7. G-score (weekly-variance-aware value): theory strong, causal proof absent

Re-pricing each cat by `impact / √(σ²_between + σ²_week)` (σ_week from
the arena's own week model) deflates **ST hardest (×0.580)** — the only
cat whose weekly noise exceeds its between-player spread — then TO
×0.705, FG% ×0.736; FT% least (×0.862). Rank effects: Dyson Daniels
16→33 (his +6.0 ST z is worth ~+3.5 in weekly currency), Curry 13→8,
Cade 14→9; **top 7 identical**. But the CRN draft pretest (24 paired
cells) was **inconclusive** (+0.42pp, t = 0.32; verifier's fresh seed
−2.68pp, t = −1.38): draft-path divergence noise (±14pp/cell) dwarfs
the signal at this N. **Shelved** — do not codify without a far larger
paired run, after the instrument fixes.

**ELI5:** a steals specialist's season average is real, but his weekly
edge rides a coin that flips wildly. z prices the season; the matchup is
played weekly. In weekly currency his steals are worth ~58 cents on the
dollar — yet proving that changes *championships* needs more data than
one pretest.

## 8. Minor findings (hygiene ledger)

1. `marketRanks` note-multipliers invert for negative scores: ×1.15
   rookie hype makes negative-mscore rookies *lower*, ×0.95 risk makes
   negative-mscore vets *higher* (Maluach −4.65→−5.35; Lively
   −3.31→−3.15). Shared by deck + arena (`draft-deck.html:804-817`,
   `arena.py:166-180`).
2. Dead code: recovery (0.60) branch of `weekly_availability` and the
   council's `rec_compound` knob are unreachable — recovery players are
   pool-excluded (0 of 213 in the arena pool).
3. Risk price/world mismatch: drafters price risk at ×0.78; the arena
   world delivers 0.75/0.88 = ×0.852 — risk players ~9% underpriced in
   the arena's own reality (streaming, which justified 0.78, doesn't
   exist in-sim).
4. %-cat weekly variance is roster-independent (a 89-FTA/wk punt team
   gets the same 0.012 as a 161-FTA/wk team) and decoupled from the
   games shock; ties impossible (continuous draws); schedule is random
   weekly pairing vs Yahoo's fixed schedule (unbiased for CRN
   comparisons); WEEKS=18 vs Yahoo ~19-20.
5. Verifier caveat (CORRECTED): the "top-30 moves ≤2 under
   re-standardization" figure holds for the partial re-standardization
   keeping 246-pool % baselines; a full re-derivation gives ≤3.

## 9. Pre-registered tuning proposals (ranked; NONE implemented)

**Instrument first — measure with a straight ruler before re-tuning:**

- **P1. Fix %-cat weekly variance** (arena): split FG/FT, raise to
  ~0.025/0.040 — or attempt-based binomial + mix inflation per roster
  (also fixes minor 4). *Prediction: FG%/FT% elasticities fall toward
  the pack; punt-% builds regrade upward; % cats stop being
  deterministic.*
- **P2. Seed by cumulative category record** (arena): one-line change in
  `simulate_seasons`. *Prediction: broad builds' playoff% rises,
  specialist builds' falls (≈ the ±13/−29pp CRN result); the
  neutral-weights headline re-quotes at a different magnitude, same
  sign.*

**Engine, validated on the fixed instrument:**

- **P3. Standardize z over the top-156 fixed-point pool** (hoops +
  rebuilt deck). *Prediction: risk-vet cluster rises (FVV +14 class),
  KD/Morant/Poole class falls ~5-8; arena CRN test on the council seat
  expected positive but modest; top-7 unchanged.*
- **P4. Re-audit the 0.78 haircut on the replacement-anchored scale**
  (mostly subsumed by P3; align or document the 0.78↔0.852 constant
  pair — minor 3).

**Candidates, only after P1+P2 (they change the answer):**

- **P5. TO down-weight sweep** (0.5 / 0.25) — elasticity says TO is
  mid-pack, structure says the column pays low-usage bench pieces.
- **P6. Elasticity-weighted council weights** (AST/BLK premium) —
  re-measure elasticities on the fixed instrument first; the current
  AST 1.82 / FT% 0.78 spread is 2.3× and worth chasing if it survives.
- **P7. G-score value** — SHELVED pending a much larger paired run.

**Hygiene (no measurement needed):** marketRanks negative-branch fix
(minor 1), dead-code removal (minor 2).

---

*Verification: 5-agent workflow, gauntlet re-derivation with fresh code
at fresh seeds; scratchpad artifacts: `audit.py`, `fixedpoint.py`,
`audit_week_model.py`, `audit_seeding.py`, `ninecat_structure.py`,
`elasticity_exp.py`, `gscore_pretest.py`, `V_pool.py`, `V_pct.py`,
`V_seeding.py`, `V_elast.py`, `V_gpre.py`, `V_misc.py`; data:
`ninecat_chartdata.json`, `ninecat_elasticity.json`.*
