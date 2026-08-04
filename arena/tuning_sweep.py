#!/usr/bin/env python3
"""Factorial tuning sweep (arena lab, 2026-07-28; 13-round re-based arena).

Cells: weight config W x TARGET-obedience policy T for the test seat in the
fixed 11-personality field.

  W: cur     locked_w=0.35 lost_w=0.45   (production)
     mid     locked_w=0.70 lost_w=0.70
     neutral locked_w=1.00 lost_w=1.00   (rank-reactive layer off)
  T: no      picks are pure council scoring
     obey    urgent-TARGET mirror: rounds 3-10, when a needed family's
             market-window shelf is <=2 and the best positive-value family
             candidate exists, take it (the deck's "click TARGET, take the
             top name" policy, with the fs-floor urgency decay built in)

5 seeds x 1000 seasons x 2 rotation-rounds per cell = 120k championship
samples per cell.
"""
import argparse
import json
import random
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import arena  # noqa: E402

# Freeze the FIELD's council seat at the pre-codification constants so the
# archived 2026-07-28 6-cell table stays reproducible from repo head — the
# codification this sweep motivated changed STRATEGIES["council"] to
# 1.0/1.0, and an unfrozen field would draft a different room.
arena.STRATEGIES["council"] = dict(arena.STRATEGIES["council"],
                                   locked_w=0.35, lost_w=0.45)

# Known mirror divergences from the deck's urgent-TARGET (disclosed after
# gauntlet review 2026-07-28; all bias the obey cells toward attenuation
# or neutral, none were codified into production):
#   - candidate choice + urgency floor use raw adj_value, not the deck's
#     punt-aware neutral fitZ, and are never crossed with the W-cell
#     weights;
#   - the scarcity gate uses static primary-position floors, not the
#     deck's openFams/balCt/imbalance conditions;
#   - family priority is C,F,G (deck: G,F,C);
#   - obedience stops after round 10 while the deck has no upper cap.

TEAMS = arena.TEAMS
FIELD = ["council", "punt_ft", "punt_ft_to", "stars", "slot_filler",
         "scarcity", "safe_floor", "upside", "specialist", "market",
         "points_chaser"]
W = {"cur": (0.35, 0.45), "mid": (0.70, 0.70), "neutral": (1.00, 1.00)}
FAM = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}
FLOOR = {"G": 3, "F": 3, "C": 2}


def families(p):
    return {FAM[b] for b in arena.positions_of(p)}


def obey_target(pool, roster, rnd, mkt, picks_so_far):
    """Return the forced pick under the urgent-TARGET mirror, or None."""
    if not (3 <= rnd <= 10) or len(roster) < 2:
        return None
    window = picks_so_far + TEAMS * 2
    shelf = {"G": 0, "F": 0, "C": 0}
    for p in pool:
        if mkt.get(p["player"], 999) <= window:
            for f in families(p):
                shelf[f] += 1
    ct = {"G": 0, "F": 0, "C": 0}
    for p in roster:
        ct[FAM[arena.positions_of(p)[0]]] += 1
    for f in ("C", "F", "G"):
        if shelf[f] <= 2 and ct[f] < FLOOR[f]:
            cands = [p for p in pool
                     if f in families(p) and arena.hoops.adj_value(p) > 0]
            if cands:
                return max(cands, key=arena.hoops.adj_value)
    return None


def run_draft_cell(order, pool_master, rng, weights, obey):
    pool = list(pool_master)
    mkt = arena.market_ranks(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    for n in range(TEAMS * arena.ROUNDS):
        slot = arena.hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        rnd = n // TEAMS + 1
        if name == "TEST":
            params = arena.strategy_params(
                "council", {"locked_w": weights[0], "lost_w": weights[1]})
            p = None
            if obey:
                p = obey_target(pool, rosters[slot], rnd, mkt, n)
            if p is None:
                ranks = (arena.ranks_for(rosters, slot)
                         if params["matrix_aware"] and rosters[slot] else None)
                p = arena.pick_for(params, pool, rosters[slot], ranks, rnd,
                                   rng, mkt=mkt)
        else:
            params = arena.strategy_params(name)
            ranks = (arena.ranks_for(rosters, slot)
                     if params["matrix_aware"] and rosters[slot] else None)
            p = arena.pick_for(params, pool, rosters[slot], ranks, rnd, rng,
                               mkt=mkt)
        rosters[slot].append(p)
        pool.remove(p)
    return rosters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w", required=True, choices=list(W))
    ap.add_argument("--t", required=True, choices=["no", "obey"])
    ap.add_argument("--seasons", type=int, default=1000)
    ap.add_argument("--rotations", type=int, default=2)
    ap.add_argument("--seeds", default="11,23,47,89,131")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    names = FIELD + ["TEST"]
    weights = W[args.w]
    obey = args.t == "obey"
    total_c = total_p = 0
    per_seed = []
    for seed in seeds:
        rng = random.Random(seed)
        shuffler = random.Random(seed * 7 + 1)
        c_seed = 0
        for rr in range(args.rotations):
            base = names[:]
            if rr:
                shuffler.shuffle(base)
            for rot in range(TEAMS):
                order = base[rot:] + base[:rot]
                rosters = run_draft_cell(order, arena.load_pool(), rng,
                                         weights, obey)
                slot = order.index("TEST") + 1
                champs, plays = arena.simulate_seasons(rosters, args.seasons,
                                                       rng)
                total_c += champs[slot]
                total_p += plays[slot]
                c_seed += champs[slot]
        per_seed.append(round(100 * c_seed /
                              (args.seasons * TEAMS * args.rotations), 3))
    denom = args.seasons * TEAMS * args.rotations * len(seeds)
    print(json.dumps({
        "cell": f"{args.w}/{args.t}",
        "champ_pct_mean": round(100 * total_c / denom, 3),
        "champ_pct_per_seed": per_seed,
        "playoff_pct_mean": round(100 * total_p / denom, 3),
    }))


if __name__ == "__main__":
    main()
