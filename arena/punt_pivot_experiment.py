#!/usr/bin/env python3
"""Punt-pivot gate sweep (arena lab, 2026-07-27).

Question under test: is the clear-path rule's 0.7 actionability threshold
(owner law 2026-07-23, deck puntPath) leaving championships on the table,
and does a stage-aware two-gate rule beat it?

Design: a single ADAPTIVE seat is added to a fixed 11-personality field.
The seat drafts exactly like `council` until its gate fires, then commits
to the chosen single-category punt for the rest of the draft. Variants
differ ONLY in the gate:

  pivot_off   never pivots (council clone; the control)
  static50/60/70/80  winnable/keptAfter >= X, evaluated on current ranks
  twogate     winnable/keptAfter >= 0.5 AND
              (winnable + min(reachable, picks_left//2)) / keptAfter >= 0.7
              where reachable = cats ranked thresh+1..thresh+2 (one good
              pick from winnable)

Common adoption mechanics (identical across variants so ONLY the gate is
measured): consider the six classic punts (FG%, FT%, 3PTM, PTS, AST, TO);
candidate cat must be personally weak (rank >= 7 of 12); evaluated each
pick in rounds 3..9 with roster >= 3; among passing cats adopt the one
with the strongest kept-cat profile (sum of (TEAMS-r)/(TEAMS-1)).

Metrics per variant: championship% and playoff% (slot-rotated), pivot
adoption rate, adoption round distribution, and champ% conditional on
having pivoted vs not (the gate's precision).

Runs entirely off the frozen 2025-10-21 snapshot. No production files
touched. Cross-seed spread is the honest uncertainty band.
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

CATS = arena.CATS
TEAMS, ROUNDS = arena.TEAMS, arena.ROUNDS
PUNTABLE = ("FG%", "FT%", "3PTM", "PTS", "AST", "TO")
THRESH = max(2, round(TEAMS / 3))          # rank <= 4 of 12 = winnable
REACH = THRESH + 2                          # rank 5..6 = one pick away
WEAK = 7                                    # only punt cats you're losing

FIELD = ["council", "punt_ft", "punt_ft_to", "stars", "slot_filler",
         "scarcity", "safe_floor", "upside", "specialist", "market",
         "points_chaser"]                   # 11 fixed seats + 1 test seat

ZGAP = 1.25   # z-deficit to the rank-THRESH team convertible by ~one pick

GATES = {
    "pivot_off": lambda W, R, kept, left: None,
    "static50":  lambda W, R, kept, left: W / kept >= 0.50,
    "static60":  lambda W, R, kept, left: W / kept >= 0.60,
    "static70":  lambda W, R, kept, left: W / kept >= 0.70,
    "static80":  lambda W, R, kept, left: W / kept >= 0.80,
    # rank-proximity credit (R = cats ranked THRESH+1..THRESH+2)
    "twogate":   lambda W, R, kept, left: (W / kept >= 0.50 and
                                           (W + min(R, left // 2)) / kept >= 0.70),
    # z-gap credit (R = cats within ZGAP of the rank-THRESH team's total) —
    # rank proximity collapses under the bimodal mid-draft rank pattern;
    # z-gap measures actual convertibility by remaining picks
    "twogate_z": lambda W, R, kept, left: (W / kept >= 0.50 and
                                           (W + min(R, left // 2)) / kept >= 0.70),
}


def totals_for(rosters):
    return {i: {c: sum(p["z"][c] for p in r) for c in CATS}
            for i, r in rosters.items()}


def gate_check(variant, ranks, punt_cat, picks_left, rosters=None, me=None):
    """Apply this variant's gate to adopting punt_cat given current ranks."""
    kept = [c for c in CATS if c != punt_cat]
    W = sum(1 for c in kept if ranks[c] <= THRESH)
    if variant == "twogate_z":
        totals = totals_for(rosters)
        mine = totals[me]
        R = 0
        for c in kept:
            if ranks[c] <= THRESH:
                continue
            others = sorted((t[c] for i, t in totals.items() if i != me),
                            reverse=True)
            bar = others[THRESH - 1]  # z-total of the rank-THRESH team
            if bar - mine[c] <= ZGAP:
                R += 1
    else:
        R = sum(1 for c in kept if THRESH < ranks[c] <= REACH)
    fn = GATES[variant]
    ok = fn(W, R, len(kept), picks_left)
    return bool(ok)


def kept_strength(ranks, punt_cat):
    return sum((TEAMS - ranks[c]) / (TEAMS - 1) for c in CATS if c != punt_cat)


def run_draft_adaptive(order, pool_master, rng, test_name, variant, stats):
    """arena.run_draft with the adaptive-pivot hook on the test seat."""
    pool = list(pool_master)
    mkt = arena.market_ranks(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    adopted = {}                             # slot -> punt cat
    test_slot = order.index(test_name) + 1
    for n in range(TEAMS * ROUNDS):
        slot = arena.hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        rnd = n // TEAMS + 1
        if name == test_name:
            params = arena.strategy_params("council")
            roster = rosters[slot]
            if slot in adopted:
                params["punt"] = (adopted[slot],)
            elif variant != "pivot_off" and 3 <= rnd <= 9 and len(roster) >= 3:
                ranks = arena.ranks_for(rosters, slot)
                passing = [c for c in PUNTABLE
                           if ranks[c] >= WEAK
                           and gate_check(variant, ranks, c,
                                          ROUNDS - len(roster),
                                          rosters=rosters, me=slot)]
                if passing:
                    cat = max(passing, key=lambda c: kept_strength(ranks, c))
                    adopted[slot] = cat
                    params["punt"] = (cat,)
                    stats["adopt_round"][rnd] = stats["adopt_round"].get(rnd, 0) + 1
                    stats["adopt_cat"][cat] = stats["adopt_cat"].get(cat, 0) + 1
        else:
            params = arena.strategy_params(name)
        ranks = (arena.ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = arena.pick_for(params, pool, rosters[slot], ranks, rnd, rng, mkt=mkt)
        rosters[slot].append(p)
        pool.remove(p)
    return rosters, (test_slot in adopted)


def tournament(variant, seasons, seed, rotations):
    rng = random.Random(seed)
    pool = arena.load_pool()
    test = "TEST"
    names = FIELD + [test]
    stats = {"adopt_round": {}, "adopt_cat": {},
             "drafts": 0, "pivoted_drafts": 0,
             "champ_piv": 0, "champ_nopiv": 0,
             "n_piv": 0, "n_nopiv": 0}
    total_c = {n: 0 for n in names}
    total_p = {n: 0 for n in names}
    for rr in range(rotations):
        base = names[:]
        if rr:
            rng.shuffle(base)
        for rotation in range(TEAMS):
            order = base[rotation:] + base[:rotation]
            rosters, pivoted = run_draft_adaptive(order, pool, rng, test,
                                                  variant, stats)
            stats["drafts"] += 1
            stats["pivoted_drafts"] += 1 if pivoted else 0
            champs, plays = arena.simulate_seasons(rosters, seasons, rng)
            for slot, name in enumerate(order, 1):
                total_c[name] += champs[slot]
                total_p[name] += plays[slot]
                if name == test:
                    if pivoted:
                        stats["champ_piv"] += champs[slot]
                        stats["n_piv"] += seasons
                    else:
                        stats["champ_nopiv"] += champs[slot]
                        stats["n_nopiv"] += seasons
    denom = seasons * TEAMS * rotations
    board = {n: {"champ_pct": 100 * total_c[n] / denom,
                 "playoff_pct": 100 * total_p[n] / denom} for n in names}
    return board, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=list(GATES))
    ap.add_argument("--seasons", type=int, default=1000)
    ap.add_argument("--rotations", type=int, default=2)
    ap.add_argument("--seeds", default="11,23,47,89,131")
    args = ap.parse_args()
    seeds = [int(s) for s in args.seeds.split(",")]
    per_seed, agg = [], None
    for s in seeds:
        board, stats = tournament(args.variant, args.seasons, s, args.rotations)
        per_seed.append({"seed": s, "test": board["TEST"],
                         "council": board["council"], "stats": stats})
        if agg is None:
            agg = {k: dict(v) if isinstance(v, dict) else v
                   for k, v in stats.items()}
        else:
            for k in ("adopt_round", "adopt_cat"):
                for kk, vv in stats[k].items():
                    agg[k][kk] = agg[k].get(kk, 0) + vv
            for k in ("drafts", "pivoted_drafts", "champ_piv", "champ_nopiv",
                      "n_piv", "n_nopiv"):
                agg[k] += stats[k]
    tvals = [r["test"]["champ_pct"] for r in per_seed]
    pvals = [r["test"]["playoff_pct"] for r in per_seed]
    n_samples = args.seasons * TEAMS * args.rotations * len(seeds)
    mean = sum(tvals) / len(tvals)
    out = {
        "variant": args.variant,
        "champ_pct_mean": round(mean, 3),
        "champ_pct_per_seed": [round(v, 3) for v in tvals],
        "champ_pct_spread": round(max(tvals) - min(tvals), 3),
        "playoff_pct_mean": round(sum(pvals) / len(pvals), 3),
        "binomial_se_pp": round(100 * math.sqrt(
            (mean / 100) * (1 - mean / 100) / n_samples), 3),
        "n_championship_samples": n_samples,
        "pivot_rate_pct": round(100 * agg["pivoted_drafts"] / agg["drafts"], 1),
        "adopt_round_dist": agg["adopt_round"],
        "adopt_cat_dist": agg["adopt_cat"],
        "champ_pct_when_pivoted": round(100 * agg["champ_piv"] / agg["n_piv"], 3)
            if agg["n_piv"] else None,
        "champ_pct_when_not": round(100 * agg["champ_nopiv"] / agg["n_nopiv"], 3)
            if agg["n_nopiv"] else None,
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
