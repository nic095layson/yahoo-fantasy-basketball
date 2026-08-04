# Tunnel-vision study — owner hypothesis, measure-only (2026-07-31)

**The hypothesis (owner, 2026-07-31):** when calculating fantasy synergy,
the system may unknowingly get "tunnel vision" and telescope too far down
the available player board, leaving value players on the table.

**Clarified scope (owner's answers):** test all four suspected mechanisms —
(1) Top-5 window too narrow, (2) synergy math myopic / one-pick-at-a-time,
(3) value-persona room model distorts, (4) composite flattens spiky
profiles. Miss metrics: players never shown; season-sim value regardless
of visibility; late-round specialists. **Scope: measure only — report, no
changes.** Nothing in this study modified the deck or engine.

## Instruments

All artifacts in the session scratchpad; sims are the standard arena
instrument (`arena.simulate_seasons`), 4,000 seasons × seeds [11, 23]
= 8,000 per arm. Sampling note: 95% CI ≈ ±1.0pp at champ% ≈ 25%,
≈ ±0.3pp at champ% ≈ 2%; deltas inside ±1.0pp are called washes.

| Instrument | What it does | Artifact |
|---|---|---|
| Full-board capture | Replay of mocks 21–26 through the shipped app block, hooked to dump the entire composite-ordered pool at each of 13 owner turns (not just the displayed 5) | `tv_boards.json` |
| T1 forced-window policies | Redraft each mock always taking composite rank 1 / rank 6 / rank 10 | `tv_window_out.json` |
| T2 invisible-value insertions | Top-5 *never-shown* candidates per mock (screened by final-roster weak-cat complement), inserted by legal pairwise swap at a real owner turn | `tv_invisible_out.json` |
| Shown-repair control | Same swap protocol applied to players that WERE shown at the critical turn | `tv_control_out.json` |
| Late-round specialist slice | Rounds 8–13, board top-40: shown-rate of spiky (max-cat z ≥ 1.5) vs balanced profiles | `tv_late_out.json` |

## Descriptive facts first

- The window is genuinely narrow: **38–52 distinct players ever shown per
  draft = 16.5–21.8% of the reachable pool.** The hypothesis's premise is
  factually right — most of the board is never displayed.
- But shown players are MORE spiky, not less: pooled max-cat z **+1.453
  shown vs +1.311 near-miss** (board ranks 6–15, never shown). The
  composite is not filtering out spiky profiles at the display margin.

## Mechanism 1 — window too narrow: REFUTED (strong form)

If value hid below the fold, drafting from deeper in the board would not
collapse. It collapses immediately:

| Policy | m21 | m24 | m26 |
|---|---|---|---|
| As drafted | 26.91 (1st) | 29.82 (1st) | 22.57 (1st) |
| Always board rank 1 | 28.80 (1st) | 18.23 (2nd) | 20.06 (1st) |
| Always board rank 6 | 0.73 (9th) | 0.54 (10th) | 1.15 (12th) |
| Always board rank 10 | 1.78 (8th) | 0.00 (11th) | 0.36 (12th) |

The ordering is steep: rank 6 is already ruinous. A narrow window over a
steep, accurate ordering loses nothing — the top of the board is where
the value actually is. (Side fact, consistent with the ledger: the owner
beat always-rank-1 in m24 by 11.6pp — owner judgment above the card is
real; see LEDGER §3.)

## Mechanism 2 / miss metrics 1+3 — invisible value: NONE FOUND THAT SURVIVES THE CONTROL

**Winning drafts (m21, m24, m26):** all 15 tested never-shown insertions
were negative — best case Alex Caruso at #117, **−0.51pp (wash)**. No
value was left on the table in any winner.

**The catastrophe (m23, 0.20% baseline)** produced the study's one
apparent hit: four never-shown interior bigs, inserted at pick #37 over
Jalen Brunson, each gain **+2.0 to +2.4pp** (Zubac +2.35, Kessler +2.34,
Clingan +2.32, Duren +1.97). For a few hours this looked like confirmed
tunnel vision.

**The control killed it.** At that same turn the card's Top-5 was
Giddey · Trey Murphy · Kawhi · **Okongwu** · **Porzingis** — two interior
repairs on screen. Same protocol:

| Candidate | Visible at #37? | Δ champ% |
|---|---|---|
| **Onyeka Okongwu** | **SHOWN (top-5)** | **+3.02** |
| Ivica Zubac | never shown (board rank 10) | +2.35 |
| Walker Kessler | never shown (board rank 8) | +2.34 |
| Donovan Clingan | never shown | +2.32 |
| Kristaps Porzingis | SHOWN (top-5) | +1.19 |
| Jalen Brunson (owner's pick) | composite rank 17 | baseline |

The **best measured repair in the entire pool was already on the card**.
The owner reached past both shown bigs to take Brunson. Even in the
worst draft ever graded, window width cost ≈ 0 measurable points —
adherence, not visibility, was the binding failure. (This also matches
the m23 debrief's CF2, +3.00pp, independently.)

Honest timing note: the drift latch shipped after m23 fires at pick #61 —
two rounds *after* this cheapest repair window. The alarm is late relative
to the best exit; but the exit was visible on the card at #37 regardless.

## Mechanism 2 proper — per-pick myopia: PARTIALLY SUPPORTED (n=1)

The one place a real crack shows: **m26's deviation bundle** (LEDGER §3,
DEVIATION WON). Three coordinated early reaches beat following the card
by **5.76pp** — a multi-pick *shape* that greedy one-pick-at-a-time
scoring would never propose, because no single pick in the bundle looked
best at its own turn. The card's fit weights adapt between picks, but it
has no lookahead over joint pick sequences. This is a genuine structural
limitation — but it is a *sequencing* blind spot, not a *board-depth*
blind spot, and it has exactly one confirmed instance.

## Mechanism 3 — value-persona room distortion: CONFIRMED, BUT CONTAINED

Code-verified separation (audit-grade, from the shipped app block):

- Composite ordering `fs = council score + judgment adj + board-slide
  bonus` — the slide bonus reads the *static* pre-season value board
  (`PRE_RANK`) against the pick number. **No persona-room term can
  reorder the Top-5.**
- The persona survival model (`survivalP`) is consumed at exactly three
  surfaces: verdict chips (BUY NOW/TOSS-UP), the wait/act ladder, and
  TARGET urgency.

So room distortion is real but only mistimes *urgency*, never *ordering*.
Its two measured distortions were already ledgered before this study:
punt-mode BUY NOW gone-rate 54% vs 83–91% normal (m22), and optimistic
quiet-chip survival in value rooms (September recalibration registered).

## Mechanism 4 / miss metric 4 — flattening & late-round specialists: NOT SUPPORTED

- Shown players are more spiky than near-misses (+1.453 vs +1.311 above).
- Late rounds (8–13), board top-40: specialists shown at **11.5%** of
  slot-appearances vs balanced **12.6%** — parity. Distinct near-miss
  specialists ever shown: 21.4% vs 25.0% balanced (n=28, gap within
  noise).
- Every tested late-round specialist insertion was negative or a wash
  (Caruso −0.51 at #117, Gobert −0.12 at #84, Camara/Coulibaly/Sarr
  −3.2 to −6.5 at #100).

The one *true* flattening instance on the books is not a display issue:
the r=0 gradient undervaluing extreme single-cat outliers (Wemby ×2,
LEDGER §4) — anchor-pick specific, already registered for the September
experiment.

## Verdict

**The hypothesis in its main form — "telescoping leaves value players on
the table" — is DISPROVED by direct measurement** across four drafts
including the catastrophe: every never-shown insertion in winning drafts
was negative, and the catastrophe's apparent invisible value was
dominated by a better repair already on screen at the same turn.

What the study did confirm, stated precisely:

1. **Per-pick myopia on multi-pick bundles** (m26, −5.76pp vs card,
   n=1) — the card cannot propose coordinated reach sequences.
2. **r=0 outlier flattening** (Wemby ×2, ledgered) — anchor-specific.
3. **Persona-room timing distortion** (ledgered, contained to
   chips/ladder/urgency; ordering is room-independent by construction).
4. Corollary worth keeping: in m23 the failure chain was
   owner-reach → structure death, with the correct repair visible and
   declined. The deck's leverage point remains adherence support
   (TARGET/latch), not window width.

## September candidates (registered, NOT shipped — measure-only mandate)

- **Bundle-lookahead probe:** score 2-pick joint sequences at reach
  turns; test whether m26-style bundles become proposable without
  wrecking single-pick accuracy.
- **Earlier structural sensitivity:** latch currently fires ~2 rounds
  after the cheapest repair; probe an R4–5 trigger against its false-
  positive cost (the current latch has 0 FPs — that bar must hold).
- Existing registrations unchanged: gradient outlier profiles,
  quiet-chip/punt-mode survival recalibration.

## Limits

Six boards from one player pool, all mock rooms; T2 candidate screening
is a weak-cat-complement heuristic (top 5 per mock), not exhaustive;
insertion arms are 8,000 seasons each; the myopia finding rests on one
bundle. No claim here is a cumulative tally; the tallies cited live in
`LEDGER.md`.
