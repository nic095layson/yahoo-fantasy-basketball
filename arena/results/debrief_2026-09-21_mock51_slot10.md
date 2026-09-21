# Mock 51 debrief — slot 10, no punt declared, first LIVE public room from the real seat (2026-09-21)

**Fingerprint:** owner slot 10, 156 picks, Yahoo public mock (random humans,
not the cast), state `arena/data/states/draft_state_51.json` (md5 `ece1e7f3b92882aac5170e9fb7771c8c`,
verified against the Yahoo recap 2026-09-21). No punt before pick 1; the
advisor's FULL TILT (AST+FT%) was taken after #46 and retargeted three times
(FT%+TO at #52, TO+FG% at #63, TO+AST at #111). Two live-drafted names were
poolless on the deck the owner used (v22, pool 255): Tre Jones, Julian
Champagnie — fixed in the 9/21 tune-up (v23, pool 264).

**Owner request:** a dissertation-style retro — defend or refute each card
recommendation at each moment, name any better player visible in hindsight,
and identify where the calculations can be tightened. The owner-facing
report is the kit's `after-report-2026-09-21-draft51-retro.md`; this file is
the technical landing (lesson 13).

**Method.** Card reconstructed two ways at all 13 owner turns — the Python
port `check_parity.py` certifies as EXACT on this state, and the deck's own
JS under node (`mock51_deckcard.py`, which also reproduces the DOM-side
survival chips, MKT_RANK and the 🎯 pin from source) — on both v22 (the deck
drafted against; `docs/draft-deck.html` at `e7aac6b`, data and engine blocks
identical to the published artifact v22) and v23 (current). Grading on
current lines: ECW (cats/week vs the average opponent, arena weekly model),
season-shape H2H (draft_50/51 method), championships (18,000 seasons, seeds
11/23/47, CRN). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`,
owner's own later picks screened as degenerate, undrafted alternatives in
release mode.

## Headline

| Readout | Value |
|---|---|
| Championship rate (18,000 seasons) | **55.03%** (rank 1 of 12; next seat dnd 11.58%) |
| Playoff rate | 99.82% |
| ECW | **5.610** cats/week (rank 1; next 4.769) — favored in 11/11 head-to-heads |
| Board rank (kept-total z-sum) | **1** (+19.88; next +2.33) |
| Category rank, weekly model | FG% 3 · FT% 2 · 3PTM 3 · PTS 3 · REB 5 · AST **12** · ST **1** · BLK 3 · TO **2** |

First mock in the ledger where board rank, ECW rank and champ rank all read
1. Excluded from the ledger superlatives: random public room (owner directive
2026-08-25); the 55% carries the room's weakness in its denominator.

Cross-plane: on v22 lines (12-man roster — Champagnie had no row) ECW 5.299,
season-shape 9/11 with the same two losers the kit's draft_51 report named
(Bonani, dnd). The v23 jump to 11/11 is bookkeeping (13th man now exists;
Sheppard synced down), not a better draft.

## Decision ledger — card vs owner vs hindsight

Card 🎯 = v22 blend50 #1 (no TARGET pin fired on v22). Hindsight = best legal
single-swap alternative on v23 lines, ECW gain in cats/week.

| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts |
|---|---|---|---|---|---|
| 10 | Towns | Edwards | 2 | none (Towns returned at 15) | 0/234 |
| 15 | Towns | Towns | 1 | none | 0/230 |
| 34 | Davis | Davis | 1 | none | 0/212 |
| 39 | D. White | Daniels | 3 | D. White +0.055 | 4/208 |
| 58 | Anunoby | Anunoby | 1 | Turner +0.007 | 1/190 |
| 63 | Pritchard (= Lillard, tie) | Lillard | 2 | Pritchard +0.066 | 4/186 |
| 82 | Turner | Sheppard | 5 (v23: 36) | Turner +0.182 | 34/168 |
| 87 | Turner | Porziņģis | 2 | Turner +0.076 | 2/164 |
| 106 | C. Johnson | C. Johnson | 1 | Lopez +0.021 | 1/146 |
| 111 | Poeltl | Poeltl | 1 | Lopez +0.021 | 1/142 |
| 130 | Braun (= Lopez, tie) | Eason | 3 | Lopez +0.074 | 1/124 |
| 135 | Lopez | Braun | 2 | Lopez +0.061 | 1/120 |
| 154 | Lopez | Champagnie | — (no v22 row; v23: 24) | Lopez +0.223 | 33/103 |

The 🎯 was the hindsight-best legal choice, or within 0.02 of it, at 12/13
turns; the exception (#130) is a tie the name tie-break resolved the wrong
way. The owner was hindsight-optimal (≤1 better alternative) at 8/13; all five
material deviations were from a correct card. Brook Lopez sat in the Top-5 at
seven consecutive turns (82–154), tied/outright #1 at three, and went
undrafted by the room.

## Counterfactual arms (CRN-paired; SE ≈ 0.4pp at these rates)

| arm | champ % | playoff % |
|---|---|---|
| as drafted | 55.03 | 99.82 |
| D. White at 39 | 56.06 | 99.93 |
| Turner at 58 | 55.98 | 99.88 |
| Pritchard at 63 | 57.85 | 99.90 |
| Turner at 82 | **62.34** | 99.99 |
| Turner at 87 | 58.14 | 99.94 |
| Lopez at 106 / 111 / 130 / 135 | 57.18 / 56.43 / 57.41 / 58.11 | ~99.9 |
| Lopez at 154 | **63.42** | 99.98 |
| follow card #1 every turn (self-consistent, strict pairwise: 39 White, 63 Pritchard, 82 Turner, 87 Hart) | 63.47 | 100.00 |
| Turner 82 + Lopez 154 | 67.38 | 100.00 |
| + Pritchard 63 | 69.66 | 100.00 |

Contrast with m34 (full card-follow 0.008% vs owner 9.52%): there the card
was punt-blind against a declared punt; here no punt preceded pick 1 and the
punt-blind ordering matched the roster that emerged. The two results bracket
the card — a strong value-first drafter, a poor punt-drafter, by design.

## Instrument findings (measured here; decisions in the kit report)

- **Survival chips (T1).** 46/48 scored v22 Top-5 rows read BUY NOW at mean
  predicted survival 2.8%; 32/46 survived to the owner's next turn. Brier
  **0.646**. Cause: the 9/11-value / 2/11-market room mix was fit on arena
  bot rooms; this human room drafted by ADP. Internal value rank vs actual
  pick: sd 41 picks (MAE 32); internal Mkt proxy sd 41 (MAE 30); Yahoo ADP
  9/15 sd 17 (MAE 12). ADP-only survival on the same rows (deck's own σ
  rule): Brier 0.260, quiet 22/28 alive, BUY 6/13 gone.
- **Exact blend ties (T2).** Percentile quantization: ties at #1 at 2/13
  turns on v22 (#63 Pritchard=Lillard, #130 Braun=Lopez) and 6/13 on v23
  (#15, #63, #82, #87, #130, #135); name-descending tie-break decided the 🎯.
- **Punt advisor (T3, root cause of S4).** Coherence "fit" is absolute kept-z;
  a star-heavy roster is always TO-negative on that scale, so punting TO
  always raises fit. Room-relative weekly P(win TO) was 0.62–0.77 at every
  turn from #58 (finished 2nd); FG% 0.43–0.56 when proposed (finished 3rd);
  FT% finished 2nd. Right about AST only (P(win) 0.04–0.30).
- **Urgent TARGET pin (T4).** v23 at #58 pins Joel Embiid (C shelf ≤2 in the
  price window) over Anunoby: −0.171 cats/week in hindsight, availability
  0.78. Latent on v22, live on the current deck.
- **Room forecast (T5, negative).** ΔECW vs forecast final rosters (K=12
  market-persona rollouts) and vs the actual final rosters both grade WORSE
  than the shipped partial-roster ΔECW by Spearman with hindsight gain (mean
  ρ 0.77 shipped, 0.59 forecast, 0.59 oracle, 0.58 value-only; shipped
  best/tied at 11/13 turns). Stage mismatch: a 3-man roster vs 13-man
  opponents has a flat, noisy gradient. Both-sides rollouts untested.

## Lessons

- **L-m51a:** the ordering held under every test including hindsight; the
  readouts around it (chips, punt fit, TARGET shelf) are the miscalibrated
  layer — and they steered four clicks and two reaches. Fix the surface.
- **L-m51b:** stale lines cost more than any formula (Sheppard #82 on a
  pre-downgrade row). S3/F7 cross-plane gate is the mechanism.
- **L-m51c:** Daniels-class hesitation is now Lopez-class: the owner takes the
  board's favorite guard and passes the board's favorite center (7 cards).
  Structural; the seat-10 slate should name the round-12/13 center.
- **L-m51d:** AST insurance for a 12th-ranked category does not move the
  category; the weekly model priced Lillard's and Pritchard's AST purchase
  the same (+0.28 vs +0.25) and the card was right both times.

## Bounds

n = 1 room; opponents disposable for intel (only the price signal is
durable). Champ% simulator-conditional (weekly constants unfit to the 8/4
weekly data). Hindsight on v23 lines vs a v22 card — they differ materially
only at #82 and #154, both stated. Single-swap gains do not add. Follow-card
arm is strict-pairwise (an undrafted card #1 is skipped → understates the
card). ADP join by folded name: 145/156 (Jr. suffixes, one alias).

## Provenance and regeneration (lesson 13)

Produced 2026-09-21 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`), branch
`claude/mock51-retro`.

```
python3 arena/mocks/mock51_retro.py replay      # -> arena/results/m51_replay.json      (~3 min)
python3 arena/mocks/mock51_retro.py final       # -> m51_final.json
python3 arena/mocks/mock51_retro.py hindsight   # -> m51_hindsight.json                  (~3 min)
python3 arena/mocks/mock51_retro.py forecast    # -> m51_forecast.json                   (~15 min)
python3 arena/mocks/mock51_retro.py arms        # -> m51_arms.json                       (~12 min)
python3 arena/mocks/mock51_combo.py             # combined arms + board rank -> m51_arms.json
python3 arena/mocks/mock51_deckcard.py rev:e7aac6b53351f23fd2ef6c8b6c177fbccdcb428b:docs/draft-deck.html arena/results/m51_deckcard_v22.json --punt-log
python3 arena/mocks/mock51_deckcard.py docs/draft-deck.html arena/results/m51_deckcard_v23.json --punt-log
python3 arena/mocks/mock51_extra.py             # survival calibration, ties, Embiid, punt advisor, ADP model (needs the kit repo beside this one, or KIT_REPO=)
```

The v22 pool (`m51_players_v22.csv`) is regenerated from git history by the
harness itself. **Regeneration status, stated honestly:** `replay`, `final`
and both `deckcard` runs were re-executed from the landed copies on
2026-09-21 and reproduced the session outputs **byte-identically**;
`m51_hindsight.json`, `m51_forecast.json` and `m51_arms.json` are the session
run's outputs copied in (their scripts are landed, the ~30-minute re-run was
not repeated). `mock51_extra.py` prints its findings to stdout (no JSON) and
was re-run from the landed copy.
