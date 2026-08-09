# Bench-weight re-grade, system integrity, and the surviving season data (2026-08-09)

**Owner's request:** implement A4; then "conduct a full system calibration and
integrity test"; then "do a rerun of the other mock draft data that you have —
provide a dissertation style report if, with the newly dialed information and
system, [the] championship probability went up." Plus: can the three seasons of
uploaded league data still be pulled and fully analyzed?

---

## 0. The question, restated precisely — because the obvious reading is wrong

"Did championship probability go up?" has two readings, and they have opposite
answers.

1. **Did today's shipped changes make the system draft better?** No. Measurably,
   provably no — and not because they failed, but because none of them touches
   what the system recommends. §2 proves this: **0 of 52 card orderings changed.**
2. **Does correcting the bench weight change the graded outcome of the drafts
   already in the ledger?** Yes, substantially and in one direction — §4. But
   this is a change in *measurement*, not in the teams. The rosters in mocks
   31–34 are the same files they always were. Nothing about those teams
   improved. What changed is that the instrument had been mis-crediting the
   last three roster spots by a factor of ~6.4, and correcting that arithmetic
   produces different numbers for identical inputs.

Reading (2) as "champ% went up" would be the exact error this repo's LEDGER
exists to prevent. **A roster's championship probability is a property of the
roster. What moved is our estimate of it.**

Claims below are marked EVIDENCE (measured here, reproduction named) or
INFERENCE. Every number is EVIDENCE unless marked otherwise.

---

## 1. Method

Four artifacts, all committed, all regenerable from a fresh clone:

| Harness | What it does |
|---|---|
| `arena/mocks/bench_share_fit.py` | measures slot-competition start-share under a daily-lineup fill |
| `arena/mocks/bench_weight_study.py` | re-grades mocks 31–34 at both weights, identical seeds, rosters fixed |
| `scripts/check_parity.py` | JS↔Python parity across pool, z, values, name matching, and card ordering |
| `scripts/test_draft.py` | 23-case live-draft smoke suite |

**Design.** Paired: same rosters, same seeds, same simulator; the *only* varying
term is `arena.BENCH_WEIGHT` (0.15 shipped → 0.956 measured). 6,000 seasons ×
3 seeds = 18,000 per arm, ×2 arms ×4 mocks = 144,000 simulated seasons.

**Deliberate scope limit.** Rosters are held **fixed**. This re-grades the
drafts that happened; it does not re-draft them under a corrected model. It
answers *"does the corrected weekly model change who wins with these rosters"* —
not *"would a corrected engine have drafted better."* The second question needs
the ordering rebuilt on the new weight and a full replay, which is September
work behind the E14 re-baseline.

---

## 2. Integrity test

### 2a. Lesson-13 reproducibility — 4/4 EXACT

Every committed champ% regenerates from the committed state at the committed
seeds:

| Mock | Committed | Regenerated | Δ |
|---|---|---|---|
| 31 | 6.16 | 6.16 | −0.004 |
| 32 | 4.11 | 4.11 | −0.004 |
| 33 | 11.37 | 11.37 | +0.002 |
| 34 | 9.52 | 9.52 | +0.002 |

Residuals are float-accumulation only. **The four mocks with committed states
are genuine evidence.** Mocks 10–30 remain unreproducible (their states were
never committed — audit F08/F34); nothing in this report rests on them.

### 2b. JS↔Python parity — EXACT MATCH

`scripts/check_parity.py`, the gate SEPTEMBER-PLAN §3 and §6 both cite and
which did not exist until today:

```
pool rows compared      : 246
z-score cells compared  : 2214
name fixtures compared  : 39
card orderings compared : 52 owner turns across 4 committed states
PARITY: EXACT MATCH
```

Tolerance is stated, not pretended: `build_deck.py` bakes z rounded to 6dp, so
a 9-category value sum inherits up to 9 × 5e-7 of rounding. z compares at 1e-6,
value sums at 1e-5. Bit-equality is impossible by construction and claiming it
would have been false.

### 2c. Gate behaviour — verified in both directions

| Scenario | Result |
|---|---|
| evidence file stale (08-04), stamp attempted | REFUSED, exit 1 |
| evidence re-authored today | stamp accepted |
| JUDGMENT dated 07-28 vs pool 08-09 | BUILD REFUSED |
| JUDGMENT re-authored | builds, PARTIAL VERIFICATION banner shown |
| second build, pool byte-identical | BUILD REFUSED (content hash) |
| quiet day, explicitly declared with sources | builds |
| `Naz Reid` CHA→LAL | MISMATCH, exit 1 |
| `Bronny James,ZZZ` (fabricated team) | UNMATCHED, exit 1 |

The last row is the one that mattered: before A4 that row exited 0 and passed
every gate.

### 2d. Live-draft suite — 23/23, card at 47 ms

---

## 3. Are today's changes responsible for anything in §4? No — and here is the proof

The decisive control. Extract the deck's engine at `d3b4a49` (the pre-audit
commit) and at `HEAD`, run both over the same 52 owner turns:

```
card Top-5 compared on 52 owner turns across mocks 31-34
orderings that CHANGED between d3b4a49 (pre-audit) and HEAD: 0
```

**EVIDENCE: every recommendation the card makes is identical to what it made
before this audit began.** A3, A4, A5, A6 and A7 changed what the system
*reports*, what it *refuses to do*, and how it *fails* — not what it picks.
That is what a display/robustness/gate change is supposed to mean, and it is
now measured rather than asserted.

So §4's numbers are attributable **entirely** to the bench-weight correction,
which is not shipped.

---

## 4. The bench-weight re-grade

`BENCH_WEIGHT` = the share of production credited to a roster's 11th–13th
players. Shipped: **0.15**. Measured under a daily-lineup fill over the 144
rosters the system itself drafts: **0.956** (ranks 11–13 start 95.3% of their
own games; ranks 1–10, 99.7%). The constant was ~6.4× too low.

Seeds 11/23/47, 18,000 seasons per arm, rosters fixed:

| Mock | Slot | Punt | champ% 0.15 → 0.956 | Δ | playoff% Δ | ECW/wk Δ | finish |
|---|---|---|---|---|---|---|---|
| 31 | 9 | FT%/3PTM/TO | 6.16 → **13.17** | **+7.01** | +16.02 | +0.134 | 5 → **3** |
| 32 | 10 | FT%/3PTM/ST | 4.11 → **6.18** | **+2.08** | +9.57 | +0.074 | 9 → **5** |
| 33 | 10 | none | 11.37 → **12.54** | **+1.17** | +1.98 | +0.002 | 3 → **2** |
| 34 | 8 | FT%/3PTM/PTS | 9.52 → **15.48** | **+5.96** | +11.15 | +0.135 | 4 → **2** |

The owner's estimated championship rate rises in **4 of 4**, his playoff rate
in 4 of 4, and his finish improves in 4 of 4. Between 5 and 8 of the room's 12
seats change championship rank in each mock, so this is not a common-mode
rescaling that cancels — it reorders the room.

---

## 5. Mechanism: two hypotheses proposed, both refuted

A consistent 4/4 result invites a story. I tested the two obvious ones and
neither survived, which is reported here rather than buried.

**H1 — "the owner gains because his bench is stronger than the room's."**
REFUTED. Correlation between the owner's bench-z advantage and his champ% gain
is **−0.515** (n=4), i.e. the wrong sign. In mock 31 his bench is *worse* than
the room mean (−2.57 z) and he gains the **most** (+7.01pp).

**H2 — "raising w compresses relative variance, so stronger rosters win more."**
The algebra is right: μ scales as w while σ scales as √w, so CV falls as
1/√w. The prediction is that high-ECW teams gain. REFUTED: across 48
team-observations the correlation between baseline ECW rank and champ% delta is
**+0.206** — the wrong sign again — and the three best rosters *lose* on
average (−0.96, −1.10, −1.72pp).

**INFERENCE: the mechanism is not a single factor.** ECW is a per-category
probabilistic comparison over raw weekly totals; which teams gain depends on
*which categories* their bench supplies relative to the field, not on aggregate
bench quality or roster strength. I could not resolve it in the time available,
and I am not going to assert a mechanism I could not measure.

**This matters for the disposition.** A large, consistent effect with no
understood mechanism is precisely the profile that should not ship on this
evidence.

---

## 6. Replication on unseen seeds

LESSONS.md lesson 4: *"no positive variant result enters a report headline
without replication on unseen seeds."* The 2026-07-12 arena finding that died
this way (t=3.06 → +0.18) is why the rule exists. Re-run at seeds
**101 / 202 / 303**, never used by this study, same 18,000 seasons per arm:

| Mock | Punt | Δ champ% (11/23/47) | Δ champ% (101/202/303) | Direction | Finish (fresh) |
|---|---|---|---|---|---|
| 31 | yes | +7.01 | **+6.38** | replicates | 5 → 3 |
| 32 | yes | +2.08 | **+1.77** | replicates | 9 → 6 |
| 33 | **no** | +1.17 | **+0.48** | direction only | 3 → 3 |
| 34 | yes | +5.96 | **+5.84** | replicates | 4 → 2 |

**Verdict: the direction replicates 4/4. The magnitude replicates closely for
mocks 31, 32 and 34** (within 0.63pp, 0.31pp, 0.12pp respectively).

**Mock 33 does not.** Its gain more than halves (+1.17 → +0.48) and the rank
improvement disappears (it stays 3rd). That is the honest signature of an
effect small enough to be seed-sensitive — and it is the *only* mock in the set
with **no declared punt**.

That sharpens the pre-registration from §7: across both seed sets, the three
punted mocks average **+4.7pp** and the single unpunted mock **+0.8pp**. n=3
vs 1, so this is a hypothesis, not a finding — but it is now a *dated,
pre-registered* hypothesis, testable the moment the September re-baseline runs
on a wider panel: **the bench-weight correction may matter chiefly in punt
builds**, where a roster deliberately concedes categories and the last three
spots carry more of what remains.

---

## 7. Error analysis

**Monte-Carlo error is not the binding constraint.** At 18,000 seasons per arm,
the per-arm SE on champ% is 0.15–0.24pp. The observed deltas are 5× to 39×
that. Monte-Carlo noise cannot explain them.

**The binding constraint is n=4.** The audit measured draft-to-draft sd at
5.9–6.9pp (F09), so a four-draft mean carries an SE near 3.2pp. Under a
coin-flip null, P(the owner gains in all four) = 0.5⁴ = **6.25%** — suggestive,
not conclusive.

**Other bounds.**
- 0.956 is slot-competition only; `team_week_model` applies availability
  separately as `g = 3.5 × availability`. Folding availability in again would
  double-count the injury haircut.
- Streaming is excluded (E16/N5). Including it raises the effective bench
  weight further, not lower — the owner banked 41.7 player-games/week in
  2025-26 against a static roster's 36.0 simulated supply.
- All four mocks share one pool, one room model, and one bracket format
  (6-team + byes, which league_intel §4 already establishes is the *wrong*
  bracket — E14). A re-baseline changes all of these at once.
- Three of the four mocks are declared-punt drafts. The two largest gains
  (m31 +7.01, m34 +5.96) are both punted; the only unpunted mock has the
  smallest gain (m33 +1.17). n=4, but worth pre-registering: the bench
  correction may interact with punt builds specifically.

---

## 8. What this licenses, and what it does not

**Licensed:** the shipped constant is wrong, the correction is measurable, and
its effect on the graded record is large relative to the ledger's entire ECW
spread (0.27 cats/wk across 25 mocks; this moves single mocks by up to 0.135).
Every champ% in `LEDGER.md` is conditional on a constant the owner's own league
format refutes.

**Not licensed:** shipping it. Three reasons, each independently sufficient
under this repo's own standards:
1. n=4, p≈0.06 under the null. The fresh-seed replication (§6) satisfies
   lesson 4 on direction but shows one of four magnitudes halving — the effect
   is real, its size is not yet pinned.
2. Mechanism unexplained after two refuted hypotheses.
3. It re-grades every historical result at once, destroying ledger comparability
   — which is exactly why `league_intel §4` dual-reported the bracket change
   rather than switching.

**Disposition:** register against **E14** as a re-baseline item with a
pre-registered bar, dual-reported, alongside the bracket correction. That is
what SEPTEMBER-PLAN's own ship rule requires, and the calendar turning does not
relax it.

---

## 9. The three seasons you uploaded — fully recoverable

**Yes. All of it landed, and none of it is lost.**

| Asset | Where | State |
|---|---|---|
| Complete draft boards, all 3 seasons | `arena/draft_boards.json` | **468 picks** — 156 per season, 13 per manager, 0 duplicates, manager-attributed |
| Real weekly per-category totals, 2025-26 | `arena/data/weekly_matchups_2025-26.csv` | 45 rows incl. the champion's playoff run; 22/22 matchups reconcile; reproduces the 103-58-1 record |
| Standings, settings, manager identity map, room reach model | `arena/results/league_intel_2025-26.md` | complete, 3 seasons |
| Behavioural manager models | `arena/profiles.json` | 11 managers |

One correction to the record: `league_intel_2025-26.md` says the 2024-25 and
2023-24 boards are "preserved in this repo's git history via the owner's
message." That is wrong in a way worth fixing — git history holds files, not
chat messages. They are preserved *properly*, as a committed JSON. The claim
understates what survived.

**What is genuinely gone:** the mock draft states 10–30, which lived under a
session-scoped uploads path and were never committed (lesson 13). Your season
data is not affected.

### New extraction from that data — October reach intel

Repeat-target analysis across all three boards, restricted to players still in
the 2026-27 pool. A manager who took the same player in 2+ of 3 seasons is
telling you who they will reach for:

| Manager | Repeat targets still draftable |
|---|---|
| **Robby** | **Collin Sexton (3×), Jarrett Allen (3×)**, Devin Booker (2×), Devin Vassell (2×) |
| David (you) | OG Anunoby, Shai Gilgeous-Alexander, Jamal Murray (2× each) |
| JCo | Jimmy Butler, Tyrese Haliburton, Nic Claxton |
| John | Tyrese Maxey, Jakob Poeltl, Jeremy Sochan |
| Martin | Brandon Ingram, Luka Doncic, Jalen Suggs |
| Hegi | Andrew Wiggins, Immanuel Quickley |
| Noah | LaMelo Ball, Naz Reid |
| Will | Onyeka Okongwu, Jaden Ivey |
| Kevin | Pascal Siakam |
| Oblena | Donovan Mitchell |

24 repeat targets remain draftable. Chance baseline: with 13 picks off a
~156-deep board, a specific manager–player repeat has probability ≈ (13/156)² =
0.0069. Two-time repeats are behavioural; **Robby taking Sexton and Allen in
all three seasons is not a coincidence.**

---

## 10. Provenance

Produced 2026-08-09 on `claude/fantasy-basketball-audit-i9pio4`. Regenerate:

```
python3 arena/mocks/bench_share_fit.py          # the 0.956 measurement
python3 arena/mocks/bench_weight_study.py       # §2a integrity + §4 re-grade
python3 scripts/check_parity.py                 # §2b
python3 scripts/test_draft.py                   # §2d
```

Outputs committed at `arena/results/bench_weight_study_out.json` and
`arena/results/bench_weight_study_seeds101-202-303_out.json`.
