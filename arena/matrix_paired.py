#!/usr/bin/env python3
"""Paired causal test: matrix-aware swing weighting (K=2, current) vs
matrix OFF ("never") for the council-style seat — common random numbers.

The activation-gate sweep measured "never" at +2.7pp championship over the
current design across all 5 seeds, refuting the pre-registered prediction.
This harness removes draft-lottery and season-noise confounds: every
(seed, rotation-round, rotation) key drafts BOTH ways with a key-dedicated
rng (identical field behavior until the test seat's first divergent pick)
and simulates both league states under an identical season rng.
"""
import json
import math
import random
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arena  # noqa: E402
from rank_gate_experiment import FIELD, run_draft_gated  # noqa: E402

TEAMS = arena.TEAMS


def main():
    seeds = [11, 23, 47, 89, 131]
    seasons, rotations = 1000, 2
    names = FIELD + ["TEST"]
    pairs = []
    for seed in seeds:
        shuffler = random.Random(seed * 7 + 1)
        for rr in range(rotations):
            base = names[:]
            if rr:
                shuffler.shuffle(base)
            for rot in range(TEAMS):
                order = base[rot:] + base[:rot]
                key = f"{seed}-{rr}-{rot}"
                slot = order.index("TEST") + 1
                r_on, _ = run_draft_gated(order, arena.load_pool(),
                                          random.Random(f"{key}-draft"), 2, arena)
                r_off, _ = run_draft_gated(order, arena.load_pool(),
                                           random.Random(f"{key}-draft"), None, arena)
                c_on, p_on = arena.simulate_seasons(
                    r_on, seasons, random.Random(f"{key}-seasons"))
                c_off, p_off = arena.simulate_seasons(
                    r_off, seasons, random.Random(f"{key}-seasons"))
                pairs.append((c_on[slot], c_off[slot],
                              p_on[slot], p_off[slot]))
    n = seasons * len(pairs)
    on = 100 * sum(p[0] for p in pairs) / n
    off = 100 * sum(p[1] for p in pairs) / n
    deltas = [100 * (b - a) / seasons for a, b, _, _ in pairs]
    mean_d = sum(deltas) / len(deltas)
    sd = math.sqrt(sum((d - mean_d) ** 2 for d in deltas) / (len(deltas) - 1))
    print(json.dumps({
        "drafts_paired": len(pairs),
        "champ_pct_matrix_on": round(on, 3),
        "champ_pct_matrix_off": round(off, 3),
        "causal_delta_pp_off_minus_on": round(off - on, 3),
        "mean_per_draft_delta_pp": round(mean_d, 3),
        "sd_per_draft_delta_pp": round(sd, 3),
        "t_stat": round(mean_d / (sd / math.sqrt(len(deltas))), 2),
        "drafts_better_off": sum(1 for d in deltas if d > 0),
        "drafts_better_on": sum(1 for d in deltas if d < 0),
        "playoff_pct_on": round(100 * sum(p[2] for p in pairs) / n, 2),
        "playoff_pct_off": round(100 * sum(p[3] for p in pairs) / n, 2),
    }))


if __name__ == "__main__":
    main()
