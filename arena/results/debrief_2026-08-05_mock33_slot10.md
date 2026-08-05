# Mock 33 debrief — slot 10, no punt declared (balanced/defense build)

Owner-uploaded state (`arena/data/states/draft_state_mock33.json`),
analyzed 2026-08-05. Regenerate: `python3 arena/mocks/season_sim_mock33.py`
→ `arena/results/season_sim_mock33_out.json`. 18,000 seasons (6,000 ×
seeds 11/23/47). Instrument caveats unchanged (pre-E14 bracket, unfit
weekly constants, ~0.45× room texture, no E18 seat map on state).

## Headline

| Metric | Value | Rank | m31 (3-punt) | m32 (3-punt) |
|---|---|---|---|---|
| Champ% | **11.37** (11.03/11.58/11.50) | **3 of 12** | 6.16, 5th | 4.11, 9th |
| Playoff% | 64.4 | — | 59.4 | 39.0 |
| ECW/week | 4.650 | 3 | 4.610, 5 | 4.450, 6 |
| 9-cat kept-total | −0.40 | 7 | −12.14, 12 | −8.67, 12 |

**Best owner mock since m26**, from slot 10. The board (kept-total rank 7)
under-rates this roster; ECW ranks it 3rd and champ% agrees — the m29
pattern repeating: portfolio coherence beats summed player value.

## The build read

Category profile: **FG% rank 2, ST rank 2 (+3.68), TO rank 5 (+2.16),
BLK rank 5** vs PTS/3PM/REB all rank 11, FT% 9, AST 8. This is the
owner's brief made flesh — defense + efficiency + low-TO — and it is a
*de facto* punt build that was never declared: the roster's implied best
triple punt is **FT%/PTS/REB (kept-z +6.50)**. That is the house thesis
("punts emerge from value, they are not declared") producing its best
result: m31 declared and disciplined → 6.16%; m32 declared and drifted →
4.11%; m33 declared nothing, drafted coherently → 11.37%. Also note:
"never pay for points" (PROMPT.md Appendix A) — PTS rank 11, champ rank 3.

In-season implication if this were the real roster: contest FG%/ST/BLK/TO
every week, stream toward them, concede PTS/3PM/REB shootouts without
chasing.

## Decision ledger (balanced lens — no punt declared; pickwise reads)

Nearly clean. P10 Cade (+3.1) sat 0.2 z under the co-best tier
(Chet/Mobley/Dyson +3.3) — coin-flip territory. The one real early gap:
**P34 OG (+2.0) over Dyson Daniels (+3.3, −1.3)** — the board's favorite
STL engine again. P39 Flagg over Amen Thompson (−0.7). From pick 58 on,
every selection tracked within ~0.9 of best-available, and the
"negative-value" tail (Draymond −1.7, Jrue −2.3, Claxton −2.3, Ellis
−1.8) is the defense/TO glue the ECW result vindicates — per-player z
calls them losses; the portfolio ranks 3rd. Jimmy Butler (+0.0,
availability-crushed) was nominal best-available from P106 onward;
passing him for playable glue was defensible on the recovery-exclusion
rule. Total pickwise value left on the board: ~4-5 z — versus ~16 in
each of m31/m32.

## Lessons

- **L-m33a:** Third instance of ECW out-predicting kept-total (m28, m29,
  m33). The board lens under-rates coherent-portfolio builds; the E8
  decision to grade by ECW keeps being right.
- **L-m33b:** The undeclared-coherent build beat both declared triple
  punts from worse and better seats alike. The card's build-agnostic
  advice plus a drafter following an archetype (not a declaration) is
  the measured sweet spot to date.
- **L-m33c:** Dyson Daniels was the best-available at an owner pick for
  the third straight mock (33: P34; 32: implied; 31: P33) and was passed
  each time. Whatever the hesitation is, the board disagrees with it —
  worth an explicit owner decision before the real draft.
