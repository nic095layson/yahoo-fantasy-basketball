# Debrief — Slot-9 manual-feed practice draft (2026-07-12)

Opening-night 2025 snapshot (`arena/data/players_2025-10-21.csv`), production engine,
manual pick-by-pick feed (owner fed all 12 seats). State:
`arena/results/practice_2026-07-12_slot9.json`.

## Status caveat — draft halted at 158 of a configured 180

Init was `--teams 12 --size 15` per session brief. Owner ended the draft after
pick #158 (mid-R14), then noted the intended roster size was smaller (real league
is 13 slots: PG SG G SF PF F C C U U BN BN BN). Consequences, stated plainly:

- Rosters are uneven at stop time: T1–T4 hold 12 players, T5–T11 and YOU hold 13,
  T12 holds 14 (incl. Tatum). All cross-team totals below carry that pick-count bias.
- Your picks #160 and #177 were never made; your roster is 13 — coincidentally the
  real league size, so the profile below is usable as-is.
- Lesson codified below: pre-flight must confirm teams × rounds = total picks
  before pick #1, not after the last one.

## 1. Your roster (13) — "Fifty Shades of Slot Nine"

AD, Maxey, Barnes, Murphy III, Ausar, Kessler, Cam Johnson, Hart, Sheppard,
McDaniels, Grimes, NAW, Draymond.

Category z-totals (all computed by the engine from the snapshot):

| Cat | z | Rank vs field |
|---|---|---|
| FG% | +0.27 | 8/12 |
| FT% | −0.07 | 8/12 |
| 3PTM | +0.72 | 8/12 |
| PTS | +1.51 | 12/12 (punted) |
| REB | +3.16 | 4/12 |
| AST | +1.97 | 7/12 |
| ST | +9.45 | **1/12** |
| BLK | +6.50 | 2/12 |
| TO | −0.53 | 3/12 |

Read: a defense/possession monster — ST locked at #1 by a wide margin, BLK #2,
TO #3, REB #4. PTS punted (declared at pick ~105; the roster obeyed it). The
championship problem is the middle: FG%/FT%/3PTM/AST all sit 7th–8th — in a
weekly H2H you bank 3–4 cats and need 1–2 swings from that middle band. That is
a playable but thin 5-cat path; the classic profile of this build wins 5–4 and
loses 3–6 to elite-efficiency teams.

## 2. Draft matrix — kept-cat value by team (engine, all-9-cat basis)

T4 +33.4 · **YOU +23.0** · T3 +17.0 · T2 +15.0 · T1 +14.8 · T6 +13.3 ·
T11 +12.3 · T7 +11.9 · T8 +10.1 · T12 +6.8 · T5 +4.3 · T10 +1.7

You drafted the #2 board — with T4 holding one FEWER pick than you, so their
lead is real, not an artifact of the count bias. On a punt-PTS basis (subtract
each side's PTS z) the gap narrows from 10.4 to ~5.7 but does not close.

## 3. Head-to-head vs the top rival (T4: SGA, Brunson, JJJ, Jam Murray, Kawhi…)

Engine `draft vs --team 4`: **you lead 3–6** (REB, AST, ST). They own FG%, FT%,
PTS, TO, and edge you on BLK (+7.85 vs +6.50) and 3PTM (+0.81 vs +0.72 — razor
thin). Path to beating T4 in a week: hold REB/AST/ST, flip 3PTM (a 0.09-z gap is
streamable), and pick off TO in a low-volume week. Realistic but you're the
underdog. Vs the #3 board (T3, Luka/Embiid): you lead 5–4 — that's the
semifinal you want.

## 4. Slot-9 cadence — how the calls aged

Pre-draft plan: safe_floor build (slot intel: 10.8% champ, best from 9), pairs
at 9/16, reach on the 16-pick side. How it played:

- **Urgency calls verified right by survival data**: Butler recommended at your
  #40 (74%) — went #47, before your #57; Vucevic recommended at #57 (78%) — went
  #62, before your #64. Both "take him now" calls were the last chance. You
  passed on both; the cost shows up in exactly the cats now ranked 7th–8th
  (Butler: FG%/FT%; Vucevic: FG%/REB).
- **Followed recs**: Maxey #16 (76%), Kessler #64 (62%), Cam Johnson #81 (64%) —
  all three still grade well post-hoc (Maxey was the last top-tier guard; the
  next PG off the board at comparable value went #45).
- **Off-card picks**: AD #9 (fed mid-batch, no card consulted), Barnes #33,
  Ausar #57, Hart #88, Draymond #153. Barnes/Ausar/Hart/Draymond built the
  ST/BLK/TO fortress — coherent with each other, but they're also why the
  efficiency middle is thin. The build that emerged is closer to a
  defense-specialist archetype than safe_floor; slot intel gives that family a
  lower champ% from 9. Honest verdict: disciplined punt, riskier shape than the
  plan.
- Punt detection fired on schedule (pick 9 of 15 checkpoint): flagged PTS as the
  natural punt at #105, committed at #112.

## 5. System operation grade: A− (one process caveat)

158 picks + 6 fixes + 5 UNKNOWNs, zero corruption, zero undos, zero RESYNCs.

Incident log:
- **Root cause (owner-confirmed)**: owner re-sent messages while the previous
  feed was still processing → 4 feeds' tool results/echoes lost (picks 2–4,
  8–11, 82–84, 124–126). Every one was absorbed by the codified protocol:
  state-read-first before any resend; zero double-logs. The 2026-07-12 ledger
  lesson ("a lost tool result ≠ nothing happened") paid for itself four times.
- **1 `--expect` mismatch** (before #13–14 feed): my pick-count arithmetic was
  off by one; engine refused the feed, nothing logged, clean resend. The
  handshake worked exactly as designed.
- **6 `draft fix` corrections**, all clean: Shaedon Sharpe (#67), Keyonte George
  (#106), Herbert Jones (#117), Kyshawn George (#123), De'Andre Hunter (#137),
  Jamie Jaquez Jr. (#155).
- **5 UNKNOWN placeholders** (outside the frozen 210 pool, no CSV edits by
  design): #131 Hansen, #141 Queta, #145 Hauser, #146 Whitmore, #147 Caruso.
  Attribution never drifted.
- **Recovery/out exclusions held**: Kyrie (#154) and Tatum (#157) were logged as
  bot picks only; never appeared on any candidate board. No rule churn mid-draft.
- **Caveat**: end-of-draft size mismatch (see status section) — a pre-flight
  gap, now a ledger lesson.

## 6. Verification note (adversarial pass)

- Category ranks, matrix, and H2H are engine-computed from the snapshot, not
  estimated. Punt-adjusted matrix figure is my arithmetic on engine numbers.
- Matrix bias from uneven roster sizes is disclosed (§ status caveat); it
  overstates T12 and understates T1–T4 slightly. It does not change the ordering
  at the top (T4 leads with fewer picks).
- Survival claims (Butler #47, Vucevic #62) checked against the pick log.
- Draft never formally completed; "final" anywhere above means "as of pick 158."
