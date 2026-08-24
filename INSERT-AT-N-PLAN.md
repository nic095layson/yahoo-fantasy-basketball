# Design plan — `Insert at #` (insert-and-shift a missed pick)

**Status: PLAN for owner approval. No feature code written yet.** This documents the
design, the full system-integrity analysis, and a phased build, so implementation
cannot trigger a cascade. Authored 2026-08-24.

## 1. Problem & why it is needed

A live pick can be **dropped** from the log (the tool never records that a pick
happened). Every pick after it is then off by one — the exact failure that hit a real
mock at pick #108 (Neemias Queta dropped; #108–116 shifted a seat). The current tools
cannot repair this cleanly:

- `processFeed`'s `N- Name` **overwrites** the player at slot N (no shift), and
  **back-fills only trailing gaps** with `UNKNOWN`. Neither inserts into the middle.
- Repairing a drop by overwriting #108, #109, #110… trips the **3-corrections-per-batch
  halt** ("numbering drift") → the whole batch is rejected. (This is precisely why a
  manual fix "did not register.")
- The **JS deck has no `resync`** (only `hoops.py` does). So on the owner's actual
  surface there is *no* good remedy for a dropped pick.

`Insert at #` fills that gap: put player X at position P and shift P…end down by one.

## 2. The load-bearing invariant (why this is tractable, not a cascade)

**`state.picks` is the single source of truth.** Verified in source: every render —
`renderStrip`, `renderDecision`, `renderCoherence`, `renderPuntAnalyzer`,
`renderBuildRead`, `renderMyRoster`, `renderMirror` — re-derives from `state.picks`
via `buildRosters(state, PLAYERS)` **fresh on every call**. There is **no cached
derived state**: no stored rosters, no stored category totals, no stored board order.

Consequence — and this is the direct answer to *"does INSERT also correct all the
rosters and categorical implications?"*:

> **Yes, automatically.** Rosters, category z-totals, category ranks,
> strengths/weaknesses, the board ordering (blend50/decwScores), survival markers,
> targets, the coherence strip, and the available pool are **pure functions of
> `state.picks`**, recomputed on every render. The insert's *entire* job is to
> produce a correct, canonical `state.picks`. Everything downstream then cascades
> **correctly** — a good cascade, not a failure one.

So the whole integrity problem collapses to one obligation: **the insert must leave
`state.picks` in the exact state a clean, in-order draft would have produced.**

## 3. The algorithm

`insertPick(state, players, P, name)` where P is 1-indexed:

1. **Validate** (refuse set, §5). Snapshot `state` for undo first.
2. **Resolve the name** with the *same* resolver the feed uses (`matchCandidates` /
   `match_player` — nicknames, typos, accents, surname-collision rules). No match →
   insert an `UNKNOWN #P` placeholder (fixable later), consistent with existing
   UNKNOWN handling.
3. **Splice**: `picks.splice(P-1, 0, {player, slot: null})`.
4. **Recompute slots positionally** for indices `P-1 … end`:
   `picks[i].slot = teamOfPick(i, state.teams)`. (Picks `0 … P-2` are untouched —
   byte-identical.)
5. **Persist** (autosave / `save_state`), **echo** the before/after (§5), **re-render**
   → all analysis re-derives.

### Why positional slot-recompute is correct (and its one boundary)
`slot` is positional by default (`teamOfPick(index)`) and the tool assigns it that way
at log time, so a normally-logged draft is **positionally consistent**: every pick `i`
has `slot == teamOfPick(i)`. A dropped-pick state is *still* positionally consistent
(the recorded slots followed the snake) — only the **players** are shifted. Inserting
the missing pick and recomputing slots positionally therefore **realigns players to
seats** exactly as reality had them (e.g. Sheppard moves seat 12→11, which is correct),
and it fixes the owner's own `my:` picks too (a `my:` pick shifted one early sat on the
wrong seat; the recompute lands it back on `teamOfPick == state.slot`).

The **only** state where positional recompute is wrong is one with a **deliberate,
non-positional slot** — a keeper or trade logged out of snake order (`--slot`), i.e.
a pick where `slot != teamOfPick(i)`. There, recompute would clobber the override.
**Decision (S3): detect and refuse.** Before inserting, scan existing picks; if any
has `slot != teamOfPick(i)`, refuse the insert and direct the owner to `RESYNC` (full
re-paste, which rebuilds correctly) or a manual fix. The owner's league is a standard
snake with no keepers, so this refusal fires only in genuinely ambiguous states —
never silently corrupts one.

## 4. System-integrity analysis (every dimension, explicitly)

| Dimension | Effect of insert | Integrity mechanism |
|---|---|---|
| **Rosters** | shifted picks change seats (correct) | `buildRosters` re-derives from picks — automatic |
| **Category z-totals / ranks** | recompute from new rosters | `my_category_ranks` / JS equivalent re-derive — automatic |
| **Board ordering, survival, targets, coherence, punt analyzer** | recompute | all read `state.picks` each render — automatic |
| **Available pool** | inserted player now taken, removed from board | `availablePool` re-derives — automatic |
| **Snake order / "on the clock" / your-next-pick** | length +1 → seats recompute | `teamOfPick`, `myNextPick`, `draftDone` derive from `picks.length` — automatic |
| **Player mapping** | name → canonical player | same resolver as feed; **dup-check refuses** an already-drafted player; UNKNOWN placeholder if no match |
| **`decwScores` ordering + `df_hash` (parity-tested)** | change because state changed (correct) | both JS & Python compute from the same corrected state → parity holds |
| **maxPick / draft length** | length +1 | **guard**: refuse/ warn if already at `teams×size` (would push a real pick off the end) |
| **Persisted state (`draft_state.json` / localStorage)** | new canonical picks | Export/Import + `hoops.py` reconciliation still valid (state is just picks) |

**Net:** because analysis is stateless-over-`picks`, no derived structure can drift out
of sync. The insert cannot half-update the tool; it either produces a valid `picks`
(everything correct) or is refused (nothing changed).

## 5. Safety contract (from this repo's scars: F30, F31, F36, R4-F01)

- **Snapshot before mutation** — stash pre-insert `state` to a one-shot recovery slot
  (browser: a `preInsert` key; CLI: `draft_state.json.pre-insert`), restorable, mirroring
  `resync`'s `.pre-resync`. (Plain `undo` pops the *last* pick and will **not** reverse
  an insert — the insert needs its own restore path.)
- **Echo before/after** (SKILL §5/§68): print the insert and the shift explicitly —
  "✎ inserted Queta at #108; #108–116 → #109–117; slots recomputed (T12,T11,…)". The
  owner must be able to verify the exact blast radius.
- **Refuse (never silently corrupt):** (a) P out of range `1…maxPick`; (b) resolved
  player already drafted; (c) draft already full (length == maxPick); (d) any existing
  pick has a non-positional slot (keeper/trade) → point to RESYNC. Each refusal changes
  nothing and states the safe alternative.
- **Bounded blast radius:** picks `0…P-2` are provably untouched (asserted in tests).

## 6. Surfaces & triggers

One implementation, two entry points, mirrored across both engines:

- **JS deck** (owner's surface): (T1) the **`Insert at #` control** in the reserved
  left header slot — `[#] [name] [Insert]`; and optionally (T2) a **feed token**
  `108+ Queta` (the `+` = insert-and-shift; distinct from `108-` overwrite and `108`
  append — no grammar collision with the current `[-—.,:]` separators). Both call one
  `insertPick(...)`.
- **`hoops.py`** (fallback + reconciliation): a `draft insert N "Name"` command, so the
  JS stays a faithful **port** and the two surfaces reconcile via `draft_state.json`.
  `check_parity.py` tests ordering/`df_hash`, not the feed grammar, so it would **not**
  catch a JS-only insert — which is *why* the port + tests below are the real guard.

## 7. Test plan (the change lands with tests that FAIL first)

- **`scripts/test_draft.py`** new cases: (a) insert-and-shift realigns players and
  recomputes slots on a positionally-consistent board; (b) picks before P byte-identical;
  (c) refuse P out of range; (d) refuse already-drafted player; (e) refuse when a
  keeper/manual slot is present; (f) refuse when draft is full; (g) UNKNOWN placeholder
  on no-match; (h) before/after echo names both players.
- **Parity fixture:** add a committed state under `arena/data/states/` that has been
  repaired by an insert, so `check_parity.py` confirms JS and Python agree on the
  post-insert board ordering + `df_hash`.
- **JS:** a small headless check (reuse the `check_parity` node harness) asserting
  `insertPick` produces the identical `picks` the Python command produces on the same
  inputs.
- Re-run the full gate suite (`test_gates.py`, `test_draft.py`, `check_parity.py`) green
  before proposing the diff.

## 8. Relationship to `RESYNC` (when to use which)

- **Insert** = surgical, one dropped pick, positionally-consistent board. Cheap, keeps
  the log; ideal mid-draft on a 45-second clock.
- **RESYNC** = nuclear, rebuild the whole board from a full re-paste. Handles arbitrary
  corruption (including keeper/trade boards the insert refuses). The insert's refusal
  messages route the owner to RESYNC. Recommendation: **also add RESYNC to the JS deck**
  (it only exists in `hoops.py` today) as the general fallback — a small follow-up, noted
  not scoped here.

## 9. Build / republish implications (out-of-scope-by-design, but stated)

`build_deck.py` is fail-closed on **today's roster verification + freshness stamp**, so
the live published deck cannot be republished without a **same-day data pull**. Therefore
"ship to the live deck" = code merged **+** a data-pull-gated republish. The code change
(this feature) and the republish are separable; the republish is an owner-gated data-pull
step, not part of writing the feature.

## 10. Phased implementation (each phase gated, driven red-first)

1. **Python first** — `draft insert` in `hoops.py` + `test_draft.py` cases (red→green).
   The Python is the reference the JS ports.
2. **JS port** — `insertPick` in `draft-deck.html`, wired to the left-slot control (and
   the `+` feed token if approved). Headless-assert JS≡Python on shared inputs.
3. **Parity fixture** — add the repaired state; `check_parity.py` green.
4. **Full gate suite** green; self-review the diff adversarially.
5. **Propose the diff** (PR). Republish only via a data-pull-gated `build_deck.py` run.

## 11. Open decisions for the owner

1. **Trigger:** control-only, or control **+** `108+ Queta` feed token? (Recommend both.)
2. **Scope:** both engines (recommended, keeps the port honest + testable), or deck-only
   now with Python to follow?
3. **Keeper/trade boards:** refuse-and-route-to-RESYNC (recommended), or add a
   `--force`/confirm path that recomputes anyway?
4. **Add RESYNC to the deck too** (the general fallback the deck currently lacks)?
