# E25b — frame-declaring bots FAIL, backwards, in all 8 rooms; DISCARDED (2026-08-06)

**Owner-directed** ("If it fails again, discard. Test and provide
results."). Measured against the bar registered with E25b **before** the
run. It failed all three measurable prongs, and prong 2 failed in the
**opposite direction** — declared frames made the bots *worse*, handing
the owner +9.28pp of title odds. **Discarded: the deck was never
modified** (the variant lived only in the measurement harness).

Regenerate: `E25_TAG=b ROOM_RUNNER=<e25b runner> python3
arena/mocks/e25_measurement.py` → `arena/results/e25b_measurement_out.json`.

## 1. What was tested

After `FRAME_R0` rounds, each manager declares the 3-cat punt its own
roster best supports and values every later candidate **under that frame**
(`adjValue(p, puntSet)` — the same concession machinery the owner's board
uses), conceding those categories outright. The ADP half, noise, bias and
loyalties are untouched. This is the design the E25 diagnosis pointed to:
*coherence requires concession.*

Pre-screened on **held-out dev seeds** (roster diagnostics, no sims):

| Variant | bot dead-kept |
|---|---|
| default (no sharp) | 1.66 |
| E25b declare after R3 | **1.43** |
| E25b declare after R4 | 1.68 |
| E25b declare after R5 | 1.70 |

R3 was the only variant better than default, so R3 went to the registered
8-room evaluation (18k CRN-paired seasons per arm, v2 instrument).

## 2. Result — failed on every prong, and reversed on prong 2

| Room | Owner default → E25b | Bot dead-kept | Bot ECW |
|---|---|---|---|
| 101 slot 4 | 24.31 → 33.35 (**+9.04**) | 1.82 → 1.82 | 4.463 → 4.458 |
| 202 slot 1 | 37.66 → 43.65 (**+5.99**) | 1.82 → 1.45 | 4.446 → 4.442 |
| 303 slot 6 | 19.06 → 32.74 (**+13.69**) | 1.36 → 1.73 | 4.474 → 4.462 |
| 404 slot 12 | 16.98 → 20.95 (**+3.97**) | 2.00 → 1.55 | 4.476 → 4.474 |
| 505 slot 8 | 19.62 → 35.67 (**+16.05**) | 1.55 → 1.36 | 4.473 → 4.455 |
| 606 slot 3 | 32.93 → 41.29 (**+8.36**) | 1.64 → 1.36 | 4.453 → 4.444 |
| 707 slot 10 | 20.29 → 31.84 (**+11.55**) | 1.91 → 1.91 | 4.474 → 4.461 |
| 808 slot 4 | 19.24 → 24.81 (**+5.57**) | 1.45 → 1.36 | 4.467 → 4.472 |
| **mean** | **23.76 → 33.04 (+9.28)** | **1.69 → 1.57** | **4.466 → 4.459 (−0.007)** |

| Prong (as registered) | Target | Measured | Verdict |
|---|---|---|---|
| 1a bots sharper | dead-kept ≤ 0.80 | 1.57 | **FAIL** |
| 1b bots sharper | bot ECW ≥ +0.05 | **−0.007** | **FAIL** (bots got *worse*) |
| 2 harder room | owner ≤ −3pp | **+9.28pp** | **FAIL — reversed** |
| 3 realism guard | default byte-identical | untouched deck | n/a (never shipped) |

**8 of 8 rooms got EASIER for the owner.** Unanimity across seats 1, 3, 4,
6, 8, 10, 12, punted and unpunted, both owner policies — this is not noise.

## 3. What it means (the finding worth keeping)

**G1a generalizes from the owner's card to the bots.** The pre-registered
counterweight was explicit: punt-*declaring* policies measured −5 to −11pp
for the owner's board, and whether that transferred to bots was open. It
transfers, and harder: **−9.28pp in the mirror**, i.e. the declaring side
loses roughly what the July G1a study measured, transferred intact.

Mechanism: a bot that concedes three categories on **round-3 evidence**
locks in a frame chosen from four players of signal, then spends ten
rounds compounding it. The owner's declarations work because they are
*judgment applied to a whole board*, made once and matched to a roster he
then builds deliberately — not an early automated commitment. Concession
without judgment is just a smaller player pool.

Combined with E25, the two results bracket the problem cleanly:
- **E25 (add to weak cats, never concede):** too weak to change anything —
  bots stay incoherent, room barely moves (−2.53pp).
- **E25b (concede early, draft the frame):** decisively worse — the bots
  hurt themselves and the room gets *easier* (+9.28pp).

Bot category coherence is not reachable by either lever. Making these bots
genuinely stronger would require something closer to real judgment
(board-wide lookahead, frame revision as the draft develops), which is a
much larger design and is **not** registered as a follow-up — three
measured attempts is enough evidence that this is the wrong tree.

## 4. Reachability note on prong 1a (EVIDENCE, for the record)

The 0.80 dead-kept target was anchored on a single observation — mock 40's
owner scored 0. Measured now across the same 8 rooms:

- the **owner seat following the shipped card** averages **1.12**
  dead-kept (per-room 1, 2, 1, 2, 0, 0, 1, 2);
- of 88 default bot teams, only **6** reach 0.

So prong 1a asked the bots to become *more categorically coherent than the
tool's own card-following policy*. That does not rescue either experiment
(both also failed prongs 1b and 2, E25b catastrophically), but the target
was probably unreachable by construction, and any future bot work should
set that threshold from a distribution rather than one draft.

## 5. Disposition

- **E25b: discarded.** Deck untouched; the variant existed only in the
  harness. Nothing to revert.
- **E25 sharp mode: unchanged** — still shipped as the owner's explicitly
  labeled, unvalidated stress test.
- Harness, rooms, and both result sets committed for reproducibility.
