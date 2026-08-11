# Mock 35 debrief — slot 12 (wheel), declared punt FT%/AST/3PTM (2026-08-05)

State: `arena/data/states/draft_state_mock35.json` (upload md5 db1ad725).
Regenerate: `python3 arena/mocks/season_sim_mock35.py` →
`arena/results/season_sim_mock35_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Per-turn replay: `arena/results/m35_replay.json` (fake-DOM,
current deck at merge `ac197ce`). Same instrument caveats as mocks 31–34
(pre-E14 bracket, unfit weekly constants, ~0.45× room texture, punt-blind
shipped ordering per E20).

## Headline

| Metric | Value | Rank |
|---|---|---|
| Champ% | **7.11** (7.38/6.98/6.97 per-seed) | 6 of 12 |
| Playoff% | 54.7 | — |
| ECW/week | 4.54 | 6 of 12 |
| Kept-total, 9 cats | −4.12 | 11 of 12 |
| Kept-z under declared punt | **+15.72** | best in room on this frame |

Room note: T1 is a monster — 30.77% champ, ECW 5.02 (above the 4.90
winners' bar). Sixth here is a mid-table finish in a top-heavy room.

## The declaration was OPTIMAL — the first punt done right

Checked all 84 possible 3-cat punts against this roster's category z:
**FT%/AST/3PTM is the #1 punt of 84** (kept-z +15.72; next best +14.76).
Mock 32's failure mode (inverted punt, −6.5z given away in the box) did
NOT recur. The owner read his build correctly.

## The structural problem — the mock-34 pattern, one seat over

**PTS is a KEPT category ranking 12 of 12 (−2.75z)**, clustered with the
punted cats. The declared 3-cat punt landed as a de-facto 4-cat punt,
leaving a 5-cat build: FG% (1), REB (4), ST (2), BLK (2), TO (1). Five
winnable categories in a 5-of-9 game = zero weekly margin — every kept
cat must hit every week. ECW 4.54 is exactly what that arithmetic
predicts, and it is mid-table (winners ≥ 4.90). This is now the SECOND
consecutive punted mock where a kept category silently died (m34: AST at
0.202 pwin; m35: PTS at rank 12) — E23's "which kept cat dies with this
punt" warning has two data points.

## Card grading (punt-blind shipped card vs punt-aware counterfactual)

Actual pick inside shipped Top-5: **9/13** (exact #1 at 6 turns) — the
owner largely followed the card. Inside the punt-aware top-5: 5/13.

The E20 defect steered at least two picks toward punted-cat value:
- **R4 Payton Pritchard** — shipped #1 (punt-blind value: he is pool #4
  in 3PM at 3.8/g); the punt-aware card said Amen Thompson. On a
  3PTM-punt team, Pritchard's headline category is discarded on arrival.
- **R6 Lauri Markkanen** — shipped #1 again; punt-aware wanted Zubac
  (center depth for the FG%/REB/BLK frame the punt implies).
The punt-aware ordering spent rounds 5–13 on the big frame (Zubac, Allen,
Clingan, Gafford) — more PTS-dead but deeper in the five live cats.
No counterfactual arms were simulated (m31–33 pattern; E20's measurement
will do this properly across all punted mocks). Blend50 out-of-sample
kill-rule counter: unchanged — no arm-based grading performed here.

## Read

Sixth with the room's best punt discipline is the punt-blind card's
fingerprint plus one structural lesson: on a defense-first big build,
PTS dies with AST/3PTM whether you declare it or not. If this build is
the October intent, the draft plan must either (a) buy PTS volume that
fits the frame (scoring bigs — the Giannis pick is the template) or
(b) accept a 5-cat identity and win the five harder (ECW needs ~+0.4).
E20/E22/E23 all gain evidence from this draft; it joins the punted-mock
screening set (now five: 22, 31, 32, 34, 35).

## LEDGER row

`| 35 | 12 | 7.11 | 54.7 | 6 | 12 | ECW 4.54; declared punt FT%/AST/3PTM
is the OPTIMAL punt of all 84 for this roster (kept-z +15.72, best frame
in room) — but KEPT PTS died (rank 12, −2.75z): second straight punted
mock with an undeclared extra punt (cf. m34 AST). Shipped-card follow
9/13; punt-blind card led R4 Pritchard (pool #4 3PM on a 3PTM punt) |`
