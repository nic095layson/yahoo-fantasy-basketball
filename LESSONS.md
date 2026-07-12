# Lessons ledger

Hard-won operational lessons. Future sessions: read this before live drafts
or arena work. Add entries dated, with the incident that taught them.

## 2026-07-12 — 127-pick live draft simulation (Cowork)

1. **A lost tool result ≠ nothing happened.** A command whose output never
   arrives may still have mutated state. Never re-send a feed on silence —
   read the draft state first. Enforced mechanically now: every
   `draft turn` in a live draft carries `--expect <pre-feed pick count>`;
   a mismatch logs nothing and prints the state tail.
   (Incident: picks #40–43 corrupted by a double-logged feed; cost 2 undos
   + 2 fixes mid-draft.)

2. **Surname-only feeds are the top live-draft error source.** One draft
   produced ambiguous White, Murray, Robinson, Ball, Bridges, Sharpe,
   Collins, Thompson. Prefer first initial + surname for common names.
   The engine now HALTS a batch when a fed name's best match is already
   drafted, and quarantines unmatched names as UNKNOWN instead of
   fuzzy-jumping surnames (Collins→Rollins class).

3. **The Cowork sandbox can neither push nor pull git remotes.** Anything
   worth keeping must be written into the repo folder (David commits via
   GitHub Desktop) or pushed through the GitHub connector — otherwise it
   dies with the session. Session scratch (/tmp) always dies.

4. **Positive findings need fresh-seed replication before they're findings.**
   The arena's "safe_stars beats safe_floor" result (t=3.06, 10 seeds) died
   on 10 fresh seeds (+0.18, t=0.4) — seed-set luck amplified by testing
   three hypotheses at once. Refutations replicated; the enhancement didn't.
   Rule: no positive variant result enters a report headline without
   replication on unseen seeds. (Arena baseline work, same night.)

5. **Draft-price injury discounts that match expected production are still
   wrong for H2H.** Fair-priced mean, unpriced variance: flagged players
   carry ~1.8× weekly game-count variance in-sim, and real 2025-26 was
   harsher than the sim (risk-flagged: 51% of games vs 75% assumed;
   recovery: ~9% vs 60%). Variance needs its own price. (Arena calibration,
   web-verified vs StatMuse/NBA.com.)

## 2026-07-12 — Live-arena ×3 integrity run (slots 1/6/10, post-discount)

6. **Mean-priced discounts don't police concentration.** After deepening to
   ×0.60/×0.78, three full live-arena drafts at three slots converged on the
   IDENTICAL four recovery players (Haliburton, Tatum, Lillard, VanVleet):
   risk-flagged players vanished from every roster, but discounted recovery
   stars still out-price the healthy shelf where it collapses (R4–11), so
   2nd/3rd/4th concurrent bets each won "clearly" on compounded value.
   Deepening the per-player discount moved WHERE they were drafted, not
   WHETHER. Concentration needs its own rule (capped bets or steeper
   compounding) — see arena/results/report_2026-07-12_live_arena_x3.md §5-P1;
   codification gate applies. Also surfaced there: the healthy-tiebreak's ~5%
   band must name its reference number (adjusted vs compounded value — they
   gave contradictory answers mid-draft), and the skill defines no multiplier
   past the 3rd concurrent recovery bet.
