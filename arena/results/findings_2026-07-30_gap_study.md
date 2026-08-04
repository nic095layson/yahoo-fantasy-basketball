# Gap study — punt advisor, majority-threshold gradient, archetypes (2026-07-30)

Pre-authorization study of the three ideology gaps. Four study agents +
adversarial gauntlet (fresh seeds, fresh code, one correction, zero
refutations). **Nothing implemented in the engine; one shipped tooltip
corrected as a truth fix** (see §1). ~1.5M season-sims across the
experiments; all artifacts in the session scratchpad
(`g1_punt_arms.json`, `g2_threshold.json`, `g1_advisor.json`,
`g3_archetypes.json`, verification `v_*.py`).

## 1. G1a — punt POLICIES are causally harmful (the study's headline)

CRN-paired, 36 cells (3 fresh seeds × 12 council slots), 2,000
seasons/arm-cell, 7 arms, base bit-verified:

| Punt policy (council seat) | Δchamp pp | t |
|---|---|---|
| adaptive-R4 (punt worst cat at R4) | −4.87 | −3.0 |
| punt FT% | −5.93 | −4.7 |
| punt TO | −6.49 | −4.4 |
| punt AST | −7.82 | −6.8 |
| punt {FG%, TO} ("Guard build") | −8.25 | −4.9 |
| punt {FT%, 3PTM} ("Big Man build") | **−11.22** | **−8.0** |

**Not declaring beats declaring, at every slot band, for every policy
tested.** The ideology's flagship Big-Man punt is the worst — and worst
exactly at slots 1–3 (−14.2pp) where the gradient already wins. The
verifier reproduced both extremes at an unused seed (−4.92 / −11.40).

**Interpretation and required correction.** The six-mock shape ledger
(flat loses, committed wins) stands as observation — but its
*prescription* ("declare the punt") is refuted: punting zero-weights
information a good drafter uses, and the old punt-persona room wins
were partly the retired %-determinism artifact (punt_ft: 33% old
instrument → 8.9% honest). Commitment means **coherent axis-building,
not conceding categories**. The ⚖ meter's tooltip has been corrected
accordingly (truth fix, shipped with this report); its diagnosis
(flat = losing) is unchanged. Consistency note: AST is the highest
elasticity (2.75) and punting it is the worst single punt (−7.8) —
the pieces agree.

One hypothesis survives, unproven: adaptive-R4 at slots 1–3 only
(+3.08pp, t=1.39, n=9) — registered, NOT recommended without its own
confirmatory run.

## 2. G1b — the punt ADVISOR: valid as a diagnostic, destructive as a policy

`puntFit(R,P) = cov_gain/0.0905 + rich/0.0403 − sunk/2.148` (terms:
elasticity-weighted kept-cat winnability gain, punt-conditional board
richness, roster value sunk in punted cats). Fully static — computable
live in the deck with zero sims.

- **Diagnostic validity: 6/6.** At every R4 state of mocks 11–16 the
  advisor's top-2 includes the debrief-verified weak family (m11 AST
  #1 exact; m14 FG%+TO #1 exact; m15 REB/ST = realized bottom-2
  exactly). Independent re-implementation reproduced both ranked
  tables to 3 decimals.
- **Policy validity: refuted.** Greedily completing the draft under the
  advisor's top punt collapsed champ% on both tested rosters (m11
  10.5% → 0.2%; m14 8.6% → 0.05%), reproduced at a fresh seed
  (−10.8pp); soft-punt (weight 0.35) also strictly worse; the
  within-roster ordering inverted on m14.
- Documented flaws if shipped as display: the `rich` term is a board
  prior (47× between-candidate vs within variance) needing demotion to
  tiebreaker; no "no-punt-needed" baseline row; R4 foresight limits.

**Proposal (awaiting authorization): ship as a display-only
"cheapest concessions" chip** — reframed per §1 as *concession
awareness* ("your cheapest cats to stop chasing"), never as weights,
never as a "declare this" instruction — with the rich-term demotion
and a no-punt baseline row, validated on states beyond these six mocks
before shipping.

## 3. G2 — majority-threshold gradient: SHELVED

Exact Poisson-binomial P(win ≥5 of 9) marginal scorer (DP verified vs
brute force <1e−12; concentration property mechanically confirmed —
it deepens the 5th-strongest cat where the current grad tops up the
weakest). Causally:

- vs the codified gradient at slots 1–3: −2.02pp, t=−1.29 (fresh-seed
  re-check −0.92, t=−0.35) — no improvement.
- vs the composite at mid slots: +1.92pp, t=0.88, cell sd 9.3pp —
  noise; the verifier showed the apparent "good slots" don't replicate
  (seed noise, CORRECTED).

Same fate as the G-score: theory attractive, mechanics verified, no
causal payoff at tested power. Shelved; revisit only with a much
larger run on September data if at all.

## 4. G3 — archetypes: the data endorses the ideology, package ready

- **PCA blind-reproduces the ideology's axes**: PC1 (42.3% var) =
  big-vs-guard style; PC2 (26.6%) = usage with TO loading against it
  ("TO = usage tax," measured). Position gradient monotone C +1.28 →
  PG −0.88.
- **Classifier** (quantile-rule based, all thresholds from measured
  distributions): 61 Traditional Big / 21 High-Usage Alpha / 36 Floor
  General / 19 3-and-D Wing / 104 Balanced. Every headline count
  verified exactly.
- **Ideology's scarcity claims confirmed in data**: 20/21 Alphas gone
  by R7; 10 Floor Generals + 14 Alphas in the top 36; 64% of elite-AST
  players in the top 36 (supply of the #1-elasticity cat dries first);
  Traditional Bigs plentiful late (23 in R8–13); 90% of Bigs are
  FT%-negative (mean −0.84).
- **Out-of-position honor roll** (position-anchored flags): Jokić AST
  +3.26, Dyson Daniels stocks +2.67, Markkanen FT +1.18, SGA, Giannis,
  Amen, Sabonis, Wemby, J-Will, Suggs; Şengün and D-White flagged —
  the ideology's own two examples, found blind.
- Honest surprises the UI must explain: Wemby and Jokić classify
  **Alpha**, not Big (their guard-side production is why they're picks
  1–2); 43% of the pool is Balanced → "no chip" default.

**Proposal (awaiting authorization): display-only package** — archetype
chip on Top-5 rows (BIG/ALPHA/GEN/3&D + cross-axis glyph), player
tooltip with profile-not-position note, roster "Build:" line with axis
lean, meter interaction reworded per §1 (name the *lean*, not a punt).
Baked at daily republish like the judgment layer; zero runtime cost;
never re-ranks.

## Authorization menu (recommendation order)

1. **A — Archetype display package (G3): RECOMMENDED.** Data verified,
   design anti-clutter-bounded, no engine risk.
2. **B — Concession-awareness chip (G1b advisor, reframed): RECOMMENDED
   WITH REFINEMENTS** (rich-term demotion, no-punt baseline row,
   validation beyond the six mocks).
3. **C — Threshold gradient (G2): DO NOT IMPLEMENT** (shelved).
4. **D — Adaptive-R4 punt at slots 1–3 (G1a residue): NOT NOW** —
   hypothesis only; would need its own fresh confirmatory experiment.
5. **Already shipped (truth fix, this commit): ⚖ meter tooltip no
   longer prescribes punt-declaring** — the one shipped claim the
   causal evidence contradicted.
