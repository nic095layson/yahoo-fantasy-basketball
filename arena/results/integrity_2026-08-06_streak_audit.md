# Streak integrity audit — is the run of 1sts real, soft, or skewed? (2026-08-06)

**Owner-directed** ("verify that the system, other manager bots, and player
selections have all been 'realistic', or has the system gotten soft or
regressed… defend and ensure it has not been skewed bias"). Streak under
audit: mocks 36→41 (five 1sts and a 3rd; 38–40 consecutive standard-room
1sts; 41 sharp-room, already asterisked).

**Verdict up front: the ranks are real, the magnitudes are not title
odds.** Two new controlled measurements and the documented record support
"the tool got stronger AND your drafting got stronger," refute "the room
got softer," and identify exactly which number should not be believed
(absolute champ%) with the reasons registered.

## 1. NEW CONTROL — is the room soft? Draft it on autopilot (EVIDENCE)

Same 8 rooms, seeds, and casts as the E25 evaluation; the owner seat
drafts **pure market/ADP** every turn. If the room were soft, plain
drafting would also win it.

| Room | ADP-autopilot owner | Card-following owner (same rooms) |
|---|---|---|
| 101/4 | 0.82 | 24.31 |
| 202/1 | 19.77 | 37.66 |
| 303/6 | 0.07 | 19.06 |
| 404/12 | 0.00 | 16.98 |
| 505/8 | 0.17 | 19.62 |
| 606/3 | 4.05 | 32.93 |
| 707/10 | 0.09 | 20.29 |
| 808/4 | 1.58 | 19.24 |
| **mean** | **3.32** | **23.76** |

**A plain drafter LOSES to these bots** — 3.32% vs the 8.33% fair share,
near-zero in 6 of 8 seats (slot 1 is the exception: ADP from the Wemby
seat is nearly optimal early). The room punishes unstructured drafting.
The 23.76 − 3.32 ≈ **20pp gap is the measured edge of the tool's
structure**, and your manual-judgment drafts grade above card-following.
Regenerate: `arena/mocks/mkt_control.py` → `mkt_control_out.json`.

## 2. Are the bots realistic? (EVIDENCE, mixed answer with receipts)

- **Reach realism is calibrated to your league**: E18b fit the cast to
  your league-mates' real drafts (Spearman 0.952 vs measured reach), after
  YOU caught the realism regression (SGA at pick 8) and it was fixed with
  a gate. Star retention in the recent states: **9 of the market top-12
  go in round 1 in every one of m38–41**, mean fall +1.6 to +2.8 picks —
  tight, not soft (worst case each time: Harden, a market-12 the value
  seats fairly let slide to 21–26).
- **Category coherence is their real weakness — and that's fitted, not
  soft**: bots average 1.64–1.69 dead kept categories. Your league's own
  history says casual rooms look like this, and the E25/E25b experiments
  PROVED this is hard to fix: making the bots "sharper" failed its bar,
  and making them declare punts made them WORSE in 8/8 rooms (+9.28pp to
  you). Their incoherence is not a dial someone left soft — it survived
  two serious attempts to remove it.
- **Bounds**: single-season fit; no bot streams or adapts in-season; and
  the tool's own card-following seat averages 1.12 dead-kept in these
  rooms — your 0-dead builds are the outlier (that's your edge, measured).

## 3. Has the system regressed or been skewed toward you? (EVIDENCE)

- **No seat bias**: 12 identical rosters score 7.97–8.90% around the
  expected 8.33 under the v2 instrument.
- **Instrument-robust streak**: your 1sts hold under BOTH instruments —
  m36 (1st/1st), m38 (1st/1st), m39 (1st/1st) on v1/v2; m37 3rd→1st;
  m40/41 are v2-native. The v2 switch did not manufacture the streak.
- **Seed-robust**: headline gaps reproduce within ~1.2pp on disjoint
  seeds (`e22_seedcheck.py`).
- **The process resists flattery structurally**: in 48 hours this system
  produced FOUR written negative results on its own ideas (E20, E22,
  E22b, E25/E25b) under bars registered before the data existed. A
  pipeline skewed to please would not keep failing its own features.
- **v2 favors your style for rules-based reasons**: daily-fill scoring
  re-graded your drafts up 6–10pp because depth genuinely plays under
  daily lineups (owner-stated rules + Yahoo docs + measured 99.4%
  start-rate). That is calibration to reality, not to you — but it IS
  why the v2-epoch numbers sit higher; noted plainly.

## 4. What SHOULD not be believed: absolute champ% (EVIDENCE)

Three registered reasons the sim's champ% overstates real title odds:

1. **Wrong playoff bracket** (E14, September): the sim runs Yahoo's
   default top-6-with-byes; your league runs **8 teams, no byes, three
   1-week rounds**. More rounds + no bye = more variance = lower real
   title odds for a dominant roster.
2. **Your league's measured playoff chaos**: in the last two REAL
   seasons, both #1 seeds lost without reaching the final, and **both
   champions had exactly the 7th-best record** (.525, .488). The format's
   defining feature is inversion; no roster carries 26–44% real title
   equity into that.
3. **Frozen 21-week rosters**: the sim has no streaming/waivers, while
   your real league runs 16–87 moves per team per season. A drafted
   advantage compounds unopposed in-sim; in reality opponents counter.

Additional honest note: the "Nth straight optimal declaration" streak is
partly **endogenous** — a coherently drafted roster tends to make its own
frame the argmax of the 84. It still discriminates (m32 inverted its
punt; m36 ranked #12), but it certifies coherence, not clairvoyance, and
future debriefs will phrase it that way.

## 5. Bottom line

| Claim | Verdict |
|---|---|
| "The room got soft" | **REFUTED** — ADP autopilot scores 3.32% in it, below fair share |
| "Bots stopped being realistic" | **REFUTED on reach** (calibrated, stars hold), **CONFIRMED-AS-DESIGNED on coherence** (fitted to a casual room; two upgrade attempts measured and failed) |
| "The instrument was bent toward me" | **REFUTED** — symmetric, seed-robust, streak holds on both instruments, four same-week negative results |
| "The tool + my choices got stronger" | **SUPPORTED** — 20pp measured tool edge over autopilot in identical rooms; your builds beat even the card |
| "43.84% / 26.29% are my title odds" | **REJECTED** — roster-strength scores on this instrument; real-league bracket, playoff history, and streaming all compress them (E14 fixes the bracket in September) |

The number to trust from the streak: **rank 1, again and again, in rooms
a plain drafter measurably loses.** The number to hold loosely: every
absolute percentage until E14 aligns the bracket and E22c calibrates the
fill constants against your real weekly data.
