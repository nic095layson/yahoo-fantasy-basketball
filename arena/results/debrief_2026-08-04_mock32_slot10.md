# Mock 32 debrief — slot 10, declared triple punt (FT% / 3PM / ST)

Owner-uploaded state (`arena/data/states/draft_state_mock32.json`), analyzed
2026-08-04. Regenerate everything:
`python3 arena/mocks/season_sim_mock32.py` →
`arena/results/season_sim_mock32_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Same instrument caveats as mock 31's debrief (pre-E14 bracket,
unfit weekly constants, ~0.45× room texture); this state also carries no
E18 seat map.

## Headline

| Metric | Value | Rank | Mock 31 (comparison) |
|---|---|---|---|
| Champ% | **4.11** (4.27/4.08/3.97 per-seed) | 9 of 12 | 6.16, 5th |
| Playoff% | 39.0 | — | 59.4 |
| ECW/week | 4.45 | 6 of 12 | 4.61, 5th |
| Kept-total, 9 cats | −8.67 | 12 of 12 | −12.14, 12th |
| Kept under declared punt | +11.07 | 1 of 12 | +23.50, 1st by 16 |

Room winners: slot 1 (Wemby/Mobley/Eason core, 26.3%), slots 3/4 (~16%).

## The core defect: the punt is inverted for the roster that was drafted

This roster's steals are **good** — rank 3, +1.68 z (Cade/Ausar/Wallace/
Flagg all contribute) — and its turnovers are **terrible** — rank 11,
−4.81 z (Giannis, Cade, Zion, Embiid, Banchero are all high-TO engines).
The declaration punts the strength and keeps the weakness. Measured on
this exact 13-man roster:

- kept-z under the **declared** punt (FT%/3PM/**ST**): **+11.07**
- kept-z under the **inverted** punt (FT%/3PM/**TO**): **+17.57**

Six and a half z — the difference between this build and a mock-31-class
build — given away in the declaration box before pick one. Mock 31 got
this right (its high-TO core punted TO); mock 32 drafted an even more
TO-heavy core and punted steals instead.

## Decision ledger (kept-z under the declared punt; pickwise reads, not
compounded counterfactuals; no E11 placebo arms)

| Pick | Took | kept-z | Best available fit | Δ | Read |
|---|---|---|---|---|---|
| 10 | Cade (bal-13) | +1.4 | **Giannis +8.2** | −6.8 | Same shape as m31's KAT pick: the balanced board's star over the build's anchor. Giannis again survived to the turn (15) — the second straight mock where that luck bailed out the seat. |
| 15 | Giannis | +8.2 | (best) | 0 | Anchor secured. |
| 34 | Flagg (bal-37) | +0.5 | Zubac +5.2 | −4.7 | Name-brand upside into a frame that wanted a punt-fit C. |
| 39 | Banchero (bal-107) | +0.5 | Zubac +5.2 | −4.7 | Below balanced value AND anti-fit — m31's Trae-class pick. |
| 58 | Embiid | +0.1 | Kessler +4.6 | −4.5 | Availability haircut eats him; kept cats don't survive it. |
| 63 | Myles Turner | +1.1 | Kessler +4.6 | −3.5 | Right archetype, wrong pick order — Kessler strictly better. |
| 82 | Zion | +2.4 | Duren +3.8 | −1.4 | Fine. |
| 87 | Dylan Harper | **−2.5** | Duren +3.8 | −6.3 | Second straight mock taking Harper at a negative kept-z. |
| 106 | Gobert | +3.5 | (≈best) | 0 | Correct. |
| 111 | **Cason Wallace** | **−1.8** | Clingan +3.3 | −5.1 | A steals specialist under a declared ST punt — the purest lens error in either mock. |
| 130 | Ausar | −0.4 | Gafford +3.2 | −3.6 | Elite-STL wing, punted STL. Same error, smaller. |
| 135 | Lendeborg | +0.0 | Gafford +3.2 | −3.2 | — |
| 154 | Anthony Black | −2.7 | Queta +1.8 | −4.5 | — |

## Lessons

- **L-m32a (the punt-declaration check the card should run):** before pick
  one — and again at mid-draft — compare kept-z under the declared punt vs
  every adjacent single-swap punt for the roster as drafted. This mock's
  declaration was 6.5 z worse than its own single-swap neighbor; that
  check is mechanical and free. Candidate September item alongside E9b.
- **L-m32b:** The m31 lens-switching failure repeated and worsened: five
  picks (Cade, Flagg, Banchero, Embiid, Wallace) took the balanced/market
  board inside a declared-punt draft. Two mocks, one owner pattern: the
  declaration is treated as a preference, and the picks follow the
  consensus board anyway. Either follow the punt card or don't declare —
  the half-measure prices worse than both (m22: 0.22%; m32: 4.11%; m31,
  the disciplined version: 6.16%; balanced winners in these rooms:
  16–32%).
- **L-m32c:** Dylan Harper went at negative kept-z in both triple-punt
  mocks. Whatever the rookie thesis is, it does not fit a three-cat punt.
