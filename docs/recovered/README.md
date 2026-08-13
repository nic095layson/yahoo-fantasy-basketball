# Recovered artifacts

Files here are **published deck versions that were never committed** — recovered
from the live artifact so the work is not lost. They are not built, not gated,
and are not the source of truth. `docs/draft-deck.html` is.

## `draft-deck-2026-08-10-published.html`

Recovered 2026-08-13 from the published artifact
(`claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0`), which was
serving a **2026-08-10** build that exists nowhere in git history.

**What it contains that `main` does not:**

1. A Monte-Carlo daily-fill lineup model — `dailyFillWeights()` with `DF_K = 32`
   trials, day-of-week weights `DF_DAY_W`, a hashed per-player game-count draw,
   and slot-filling against `LINEUP_SLOTS` — replacing `lineupWeights()`. The
   default weight for an unlisted player also changed (`0.15` → `1.0`).
2. The Best-available table's **Fit → ΔECW** column swap (`id="thRoster"`,
   `data-sort="decw"`), labelled in the page as an owner swap on 2026-08-10
   "replacing the Fit column after it inflated a mis-shaped star", plus the
   matching lens option and legend text.
3. Minor prose: pick-log height/scroll note, dual-eligible `G/F` and `F/C`
   position filter options.

**Why it was not carried forward.** The matching `scripts/hoops.py` change was
never committed either, so this JS disagrees with the canonical engine:
`check_parity.py` reports **20 card-ordering disagreements** against it
(z-scores and name fixtures still match — the divergence is purely the
recommendation ordering). The repo's own law is that the deck is a *port of*
`hoops.py`, "verified against engine output at build time" — a claim this
version's own Logic paragraph still makes while failing it.

Publishing it would have shipped a recommendation ordering that cannot be
verified against the engine, so the 2026-08-13 Fresh Deck Pull republished from
committed, parity-clean code (owner decision, recorded in the draft-kit
after-report for 2026-08-13).

**To land this work properly:** port `dailyFillWeights` into `scripts/hoops.py`
(the hash function must match exactly for parity), re-run `check_parity.py`
until EXACT, then bring the deck-side changes into `docs/draft-deck.html` and
rebuild. Do not hand-merge this file over the built deck.
