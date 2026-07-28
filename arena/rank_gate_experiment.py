#!/usr/bin/env python3
"""Rank-activation gate study (arena lab, 2026-07-27).

Owner question: the matrix-aware swing weighting (locked x0.35 / lost x0.45)
activates once the roster has >= 2 players ("from your 3rd pick"). Is that
the right moment — and how reliable is the rank signal on tiny rosters?

Mode A (stability): for the council seat across many drafts, compute the
category-rank vector after every one of its picks and compare against its
FINAL ranks: mean |rank drift|, locked/lost classification agreement, and
the harmful-mislabel rate (a cat down-weighted as locked/lost at size k
that ends up a contested swing cat at final size).

Mode B (sweep): championship% for activation thresholds K in
{1,2(current),3,4,5,never} — the weights engage only once len(roster)>=K.
K=1 uses an in-memory patch of arena.py's hard-coded >=2 floor. Same
fixed 11-personality field as the punt study; test seat is council-like
in every other respect.
"""
import argparse
import importlib.util
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arena  # noqa: E402

# arena clone with the >=2 floor relaxed to >=1 (for K=1 only)
_src = open(os.path.join(HERE, "arena.py")).read().replace(
    'len(roster) >= 2', 'len(roster) >= 1')
_spec = importlib.util.spec_from_loader("arena1", loader=None)
arena1 = importlib.util.module_from_spec(_spec)
arena1.__file__ = os.path.join(HERE, "arena.py")
exec(compile(_src, "arena1", "exec"), arena1.__dict__)

TEAMS = arena.TEAMS
FIELD = ["council", "punt_ft", "punt_ft_to", "stars", "slot_filler",
         "scarcity", "safe_floor", "upside", "specialist", "market",
         "points_chaser"]


def run_draft_gated(order, pool_master, rng, K, mod):
    """arena.run_draft with the test seat's matrix weighting gated at K."""
    pool = list(pool_master)
    mkt = mod.market_ranks(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    snapshots = []            # (k, ranks) for the test seat, mode A
    for n in range(TEAMS * mod.ROUNDS):
        slot = mod.hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        if name == "TEST":
            params = mod.strategy_params("council")
            if K is None or len(rosters[slot]) < K:
                params["matrix_aware"] = False
        else:
            params = mod.strategy_params(name)
        ranks = (mod.ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = mod.pick_for(params, pool, rosters[slot], ranks,
                         n // TEAMS + 1, rng, mkt=mkt)
        rosters[slot].append(p)
        pool.remove(p)
        if name == "TEST":
            snapshots.append((len(rosters[slot]),
                              mod.ranks_for(rosters, slot)))
    return rosters, snapshots


def mode_stability(seeds, rotations):
    tiers = (2, 10)           # locked <= 2, lost >= 10 at 12 teams
    agg = {}                  # k -> [n, drift_sum, agree, harmful, labels]
    names = FIELD + ["TEST"]
    for seed in seeds:
        rng = random.Random(seed)
        shuffler = random.Random(seed * 7 + 1)
        for rr in range(rotations):
            base = names[:]
            if rr:
                shuffler.shuffle(base)
            for rot in range(TEAMS):
                order = base[rot:] + base[:rot]
                _, snaps = run_draft_gated(order, arena.load_pool(),
                                           rng, 2, arena)
                final = snaps[-1][1]
                fin_cls = {c: ('L' if final[c] <= tiers[0] else
                               'X' if final[c] >= tiers[1] else 'S')
                           for c in arena.CATS}
                for k, ranks in snaps[:-1]:
                    a = agg.setdefault(k, [0, 0.0, 0, 0, 0])
                    for c in arena.CATS:
                        cls = ('L' if ranks[c] <= tiers[0] else
                               'X' if ranks[c] >= tiers[1] else 'S')
                        a[0] += 1
                        a[1] += abs(ranks[c] - final[c])
                        a[2] += cls == fin_cls[c]
                        if cls in 'LX':
                            a[4] += 1
                            if fin_cls[c] == 'S':
                                a[3] += 1
    print(f"{'roster size':>11s} {'mean |Δrank| to final':>22s} "
          f"{'class agreement':>16s} {'harmful mislabel*':>18s}")
    for k in sorted(agg):
        n, drift, agree, harm, labeled = agg[k]
        harm_pct = 100 * harm / labeled if labeled else 0.0
        print(f"{k:11d} {drift / n:22.2f} {100 * agree / n:15.1f}% "
              f"{harm_pct:17.1f}%")
    print("* cat down-weighted as locked/lost at size k that ends SWING "
          "(contested) at final size — the costly error class")


def mode_sweep(K, seeds, seasons, rotations):
    mod = arena1 if K == 1 else arena
    names = FIELD + ["TEST"]
    total_c = total_p = 0
    per_seed = []
    for seed in seeds:
        rng = random.Random(seed)
        shuffler = random.Random(seed * 7 + 1)
        c_seed = 0
        for rr in range(rotations):
            base = names[:]
            if rr:
                shuffler.shuffle(base)
            for rot in range(TEAMS):
                order = base[rot:] + base[:rot]
                rosters, _ = run_draft_gated(order, mod.load_pool(),
                                             rng, K, mod)
                slot = order.index("TEST") + 1
                champs, plays = mod.simulate_seasons(rosters, seasons, rng)
                total_c += champs[slot]
                total_p += plays[slot]
                c_seed += champs[slot]
        per_seed.append(round(100 * c_seed / (seasons * TEAMS * rotations), 3))
    denom = seasons * TEAMS * rotations * len(seeds)
    print(json.dumps({
        "K": "never" if K is None else K,
        "champ_pct_mean": round(100 * total_c / denom, 3),
        "champ_pct_per_seed": per_seed,
        "playoff_pct_mean": round(100 * total_p / denom, 3),
        "n_samples": denom,
    }))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["stability", "sweep"])
    ap.add_argument("--gate", default="2",
                    help="sweep only: 1|2|3|4|5|never")
    ap.add_argument("--seasons", type=int, default=1000)
    ap.add_argument("--rotations", type=int, default=2)
    ap.add_argument("--seeds", default="11,23,47,89,131")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    if args.mode == "stability":
        mode_stability(seeds, args.rotations)
    else:
        K = None if args.gate == "never" else int(args.gate)
        mode_sweep(K, seeds, args.seasons, args.rotations)


if __name__ == "__main__":
    main()
