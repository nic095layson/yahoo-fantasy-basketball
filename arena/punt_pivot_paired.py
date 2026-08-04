#!/usr/bin/env python3
"""Paired counterfactual for the punt-pivot gate study (arena lab, 2026-07-27).

The sweep's conditional stat (champ% when pivoted) confounds selection with
causation: gates fire on drafts that are already strong. This harness removes
the confound with common random numbers:

  for every (seed, rotation-round, rotation) draft key:
    - draft with the variant gate, using a rng dedicated to the key
    - if the gate fired: redraft the SAME key with the gate disabled
      (identical rng seed -> identical picks up to the pivot moment)
    - simulate BOTH final league states with the SAME season rng
      (simulate_seasons consumes a fixed number of draws per matchup,
      so identical seeds give identical weekly noise realizations)
    - record the test seat's championship count under pivot vs no-pivot

The paired delta on fired drafts is the gate's causal effect, free of
draft-selection bias and season-noise variance.
"""
import argparse
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arena  # noqa: E402
import punt_pivot_experiment as X  # noqa: E402

TEAMS = arena.TEAMS


def draft_with_gate(order, pool_master, key, variant, stats):
    rng = random.Random(f"{key}-draft")
    return X.run_draft_adaptive(order, pool_master, rng, "TEST", variant, stats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=[v for v in X.GATES if v != "pivot_off"])
    ap.add_argument("--seasons", type=int, default=1000)
    ap.add_argument("--rotations", type=int, default=2)
    ap.add_argument("--seeds", default="11,23,47,89,131")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    pool = arena.load_pool()
    names = X.FIELD + ["TEST"]
    pairs = []          # (champ_with, champ_without, seasons) per fired draft
    fired = drafts = 0
    stats = {"adopt_round": {}, "adopt_cat": {}}
    for seed in seeds:
        shuffler = random.Random(seed)
        for rr in range(args.rotations):
            base = names[:]
            if rr:
                shuffler.shuffle(base)
            for rot in range(TEAMS):
                order = base[rot:] + base[:rot]
                key = f"{seed}-{rr}-{rot}"
                drafts += 1
                rosters_v, pivoted = draft_with_gate(order, pool, key,
                                                     args.variant, stats)
                if not pivoted:
                    continue
                fired += 1
                rosters_c, _ = draft_with_gate(order, pool, key,
                                               "pivot_off", stats)
                slot = order.index("TEST") + 1
                cv, _ = arena.simulate_seasons(
                    rosters_v, args.seasons, random.Random(f"{key}-seasons"))
                cc, _ = arena.simulate_seasons(
                    rosters_c, args.seasons, random.Random(f"{key}-seasons"))
                pairs.append((cv[slot], cc[slot], args.seasons))
    n = sum(p[2] for p in pairs)
    with_p = 100 * sum(p[0] for p in pairs) / n if n else None
    without = 100 * sum(p[1] for p in pairs) / n if n else None
    deltas = [100 * (a - b) / s for a, b, s in pairs]
    mean_d = sum(deltas) / len(deltas) if deltas else None
    sd = (math.sqrt(sum((d - mean_d) ** 2 for d in deltas) / (len(deltas) - 1))
          if len(deltas) > 1 else None)
    out = {
        "variant": args.variant,
        "drafts": drafts, "fired": fired,
        "fire_rate_pct": round(100 * fired / drafts, 1),
        "paired_seasons": n,
        "champ_pct_with_pivot": round(with_p, 3) if with_p is not None else None,
        "champ_pct_without_pivot": round(without, 3) if without is not None else None,
        "causal_delta_pp": round(with_p - without, 3) if with_p is not None else None,
        "per_draft_deltas_pp": [round(d, 2) for d in deltas],
        "mean_per_draft_delta_pp": round(mean_d, 3) if mean_d is not None else None,
        "sd_per_draft_delta_pp": round(sd, 3) if sd is not None else None,
        "t_stat": round(mean_d / (sd / math.sqrt(len(deltas))), 2)
                  if sd else None,
        "drafts_improved": sum(1 for d in deltas if d > 0),
        "drafts_hurt": sum(1 for d in deltas if d < 0),
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
