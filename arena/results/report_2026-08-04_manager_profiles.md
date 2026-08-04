# Manager profiles report — three real seasons, all 12 managers (2026-08-04)

**Owner's questions:** (1) which players did each manager draft repeatedly
across 2023-24 / 2024-25 / 2025-26 — "we seem to have a bias towards this";
(2) rank the managers on draft results and end-of-season finish; (3) full
profile per manager.

**Method.** All three owner-provided draft boards canonicalized into
`arena/draft_boards.json` (156 picks × 3 seasons, snake encoding verified
against the source team-per-pick columns; identity map from league_intel
§12). Repeats matched on normalized names. Rankings use regular-season
record rank (the draft's most direct output) and final placement, averaged
across seasons; composite = mean of the two averages. Chance baseline for
repeats derived from actual season-to-season pool overlaps (132 / 121 / 112
shared drafted players per season pair; 107 across all three).

## 1. The loyalty question — answered with a baseline

**League-wide, repetition is NOT above chance:** 28 same-manager pair
repeats observed vs ~30.4 expected if the 156 drafted players were dealt
randomly each season. Your league as a whole does not re-draft its guys.

**But the bias is real where it's concentrated:**

- **Three-peats run ~3× the league chance rate (2 vs 0.74) — and BOTH
  belong to Robby** (per-manager expectation ≈ 0.06; Robby has 2, ~30× his
  rate): **Jarrett Allen** (R6 → R5 → R4, earlier every year) and
  **Collin Sexton** (R12 → R7 → R12).
- **Repeats are round-sticky** — managers re-draft at nearly the same
  price: Siakam R4/R4 (Kevin), Quickley R6/R6 (Hegi), Mitchell R2/R2
  (Oblena), Ingram R5/R5 and Luka R1/R1 (Martin), OG R5/R5 and SGA R1/R1
  (David), Booker R2/R2 (Robby). Where loyalty exists, the *price* is
  predictable too.

### Repeats by manager (round in each season drafted)

| Manager | 3-peats | 2-peats |
|---|---|---|
| **Robby** | **Jarrett Allen** (R6/R5/R4), **Collin Sexton** (R12/R7/R12) | Booker (R2,R2), Vassell (R8,R7) |
| David (you) | — | SGA (R1,R1), OG Anunoby (R5,R5), Jamal Murray (R5,R4) |
| Martin | — | Luka (R1,R1), Ingram (R5,R5), Suggs (R7,R10) |
| John | — | Maxey (R3,R2), Poeltl (R8,R7), Sochan (R12,R11) |
| JCo | — | Haliburton (R1,R1), Butler (R2,R4), Claxton (R5,R9) |
| Hegi | — | Quickley (R6,R6), Wiggins (R6,R8) |
| Will | — | Okongwu (R9,R8), Ivey (R10,R9) |
| Noah | — | LaMelo (R1,R2), Naz Reid (R13,R8) — *autodraft: ADP artifacts, not loyalty* |
| Oblena | — | Mitchell (R2,R2) |
| Kevin | — | Siakam (R4,R4) |
| Cayas | — | **none** |
| Kyle | — | **none** |

**Draft-day use (feeds E18):** loyalty players get a probability boost in
each manager's pick projection *at their historical round*. Robby chasing
Jarrett Allen a round earlier each year (R6→R5→R4) is the single most
predictable non-autodraft pick in the league — if you want Allen in
October, you are bidding against Robby by R4. Cayas and Kyle carry no
loyalty signal; project them on tendencies alone.

## 2. Three-season rankings

Composite = mean(avg record rank, avg final placement); lower is better.

| # | Manager | Record ranks (23→26) | Avg | Finishes (23→26) | Avg | Composite |
|---|---|---|---|---|---|---|
| 1 | **Martin** | 5, 3, 7 | 5.00 | 5, 2, **1** | **2.67** | **3.83** |
| 2 | Will | 4, 6, 3 | 4.33 | 3, 6, 2 | 3.67 | 4.00 |
| 3 | John | 6, **1**, 5 | 4.00 | 2, 8, 5 | 5.00 | 4.50 |
| 4 | **David (you)** | 3, 8, **1** | **4.00** | 7, 3, 6 | 5.33 | 4.67 |
| 5 | JCo | 8, 5, 8 | 7.00 | 6, 4, 3 | 4.33 | 5.67 |
| 6t | Cayas | **1**, 11, 4 | 5.33 | 4, 11, 4 | 6.33 | 5.83 |
| 6t | Robby | 2, 7, 12 | 7.00 | **1, 1**, 12 | 4.67 | 5.83 |
| 8 | Oblena | 7, 2, 9 | 6.00 | 8, 5, 9 | 7.33 | 6.67 |
| 9 | Noah | 9, 4, 11 | 8.00 | 9, 7, 11 | 9.00 | 8.50 |
| 10 | Kevin | 11, 10, 2 | 7.67 | 11, 10, 8 | 9.67 | 8.67 |
| 11 | Kyle | 10, 12, 6 | 9.33 | 10, 12, 7 | 9.67 | 9.50 |
| 12 | Hegi | 12, 9, 10 | 10.33 | 12, 9, 10 | 10.33 | 10.33 |

Readings: **Martin converts** (worst avg record of the top four, best
finishes — the playoff riser). **You have the league's best regular-season
engine** (avg record rank 4.00, trending 3→8→1) and the league's worst
luck converting it. **Robby is pure variance** (two titles, then dead
last). **Will and John are the steady class.** The bottom four are stable:
Noah (autodraft), Kevin, Kyle, Hegi.

## 3. Twelve profiles

**Martin** (Martin you're him → Sales & Markkanen → HalleLuka Amen) —
Composite #1. 5th→2nd→champion, heavy streamer (36/87/50 moves), reaches
for his guys early (−14.8 early reach) and converts. Loyal to Luka (R1×2),
Ingram, Suggs. **The seat to fear in October.**

**Will** (MENISCUS TEAR → LAME TIME → Konclave) — #2. 3rd/6th/2nd, top-2
mover every season (87/70/83): drafts adequately, then out-works the
waiver wire. His draft is the least predictive part of his season.

**John** (Steph BoyArdee → Matchless → Cool Team) — #3. Steady, low-churn,
mild reacher; 24-25's #1 record that lost the QF. Loyal to Maxey/Poeltl/
Sochan at sticky rounds. Rarely surprising — easy to project.

**David — you** (LayBron → Demure → JAMAL AL-QUETA) — #4 composite,
**#1 regular-season engine** (record ranks 3→8→1). Value-anchored (+24.3
reach, best in room), risk-tolerant on price (Kawhi/KP as fallers), loyal
to SGA/OG/Murray at stable rounds. Three years, three playoff exits — the
format, not the drafting, has been the ceiling.

**JCo** (Beats by Dray → MOO DURANT → Wing Chun Wemby) — #5, quietly
6th→4th→3rd, ascending every year, value-anchored. Loyal to Haliburton.
The trend line says he's the next Martin.

**Cayas** (REBUILDING SZN → BALLSACK LAVINE → IM SO HORT) — #6t, maximum
volatility (record #1, then #11, then #4). Zero player loyalty — the least
projectable drafter in the room; model him wide.

**Robby** (Poole-ootan → Put Me in Coach → Bamonte) — #6t by composite,
but the tally hides the story: back-to-back titles, then a collapse. The
room's ONLY loyalty-heavy drafter (both 3-peats; Allen earlier each year,
Booker R2 twice). Low-churn. Expect reversion and expect him to chase his
guys — the most exploitable projection in the league.

**Oblena** (D.O.L.L.A. → Match My Freak → Itsy Bitsy Spida) — #8. One
genuinely strong year (24-25, record #2), value-early/hype-late pattern,
Mitchell R2 twice. Middle of everything.

**Noah** (Strokin my Saboner → Poop and Scoot → Devin Minutes) — #9.
**Autodrafts** (owner-confirmed): his board IS Yahoo ADP; his "loyalty"
(LaMelo, Naz Reid) is ranking-list residue. Deterministic seat — in
October, whatever ADP says he takes, he takes.

**Kevin** (Big Deuce → Day to Davis → All guards no defense) — #10.
Guard-heavy identity three straight years (Siakam R4×2 the lone big
loyalty); 25-26's record #2 shows the ceiling, playoffs show the floor.
Bigs are SAFE passing his seat; guards are not.

**Kyle** (HumilAyton → Jericho's → Anti-wan) — #11 but improving
(10th→12th→7th; engagement jump to 74 moves). Zero loyalty signal,
near-ADP drafter. Model as market with noise.

**Hegi** (Sing to me Paolo → Quickley Luk-a → Not hurt just SARR) — #12.
12th/9th/10th, low engagement, name reaches (Quickley R6 twice). Value
falls around his picks — draft-day gift dispenser to his neighbors.

## 4. Caveats

- Reach indices are quantitative for 2025-26 only (frozen Oct-2025 pool);
  older seasons are qualitative — no contemporaneous value reference.
- n=3 seasons; the rankings are honest arithmetic, not significance tests.
  Robby's variance and Cayas's volatility make their point estimates the
  least stable.
- 2023-24 was a 20-week season (rates normalized by using ranks only).
- Loyalty boosts in E18 must stay calibrated: league-wide repetition is at
  chance, so the boost applies ONLY to the named manager-player pairs
  above, not as a general behavior.

## 5. Correction (owner, 2026-08-04, post-publication)

**Noah autodrafted in 2025-26 ONLY; his 2023-24 and 2024-25 drafts were
manual.** Three downstream edits to this report's claims:

- §1/§3 called his LaMelo (R1, R2) and Naz Reid (R13, R8) repeats
  "autodraft ADP artifacts." Wrong on LaMelo: both LaMelo picks fell in
  the MANUAL seasons — that pair is genuine loyalty, modeled as such now.
  Naz Reid stays dropped (the R8 leg was the 25-26 autodraft).
- His 25-26 reach index (−43.5) is a pure reading of Yahoo's default
  board vs our value board — behaviorally uninformative for Noah, but
  the cleanest board-geometry reference the data contains. It is kept for
  exactly that purpose and excluded from his behavioral profile per the
  owner's instruction.
- His forward model (profiles.json + deck) is refit to the manual
  seasons: ADP-leaning manual drafter (adp_w 0.75, noise 9) with LaMelo
  loyalty — no longer a deterministic market bot. Whether he autodrafts
  again in October is unknown; if the owner learns he will, flip
  `autodraft` back and the model reverts to adp_w 1.0 / noise 2.
