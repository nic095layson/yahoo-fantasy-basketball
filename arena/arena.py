#!/usr/bin/env python3
"""arena — self-play draft tournament for the fantasy basketball system.

ISOLATION CONTRACT: this folder tests the system; it never modifies it.
The arena imports the production engine (scripts/hoops.py) read-only, uses
its own frozen dataset (data/players_2025-10-21.csv — opening night of the
2025-26 season, no hindsight), and writes only under arena/results/.

    python3 arena/arena.py draft --seed 1        # one 12-team draft
    python3 arena/arena.py tournament            # rotations x seeds x seasons
    python3 arena/arena.py tournament --seasons 200 --seeds 5 --rotations 3
    python3 arena/arena.py tournament --generations 3   # fixed-seed evolution

Scoring is CHAMPIONSHIPS from Monte-Carlo H2H seasons, not draft-day value.
Statistical honesty (verified 2026-07-12): champ% differences under ~2 points
need ~10 seeds x 200 seasons to be trusted; the mid-board is noise below
that. Generations are evaluated on a FIXED seed set so mutation effects are
attributable. The built-in hill-climb is a baseline; the Fable 5 strategy
lab (Cowork phase 2) supplies reasoned evolution.
"""

import argparse
import importlib.util
import json
import math
import os
import random

ARENA_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ARENA_DIR)
DATA = os.environ.get("ARENA_DATA",
                      os.path.join(ARENA_DIR, "data", "players_2025-10-21.csv"))

_spec = importlib.util.spec_from_file_location(
    "hoops", os.path.join(REPO, "scripts", "hoops.py"))
hoops = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hoops)
hoops.DATA_PATH = DATA  # arena reads its own frozen snapshot

CATS = hoops.CATS
BASE_POS = ("PG", "SG", "SF", "PF", "C")
TEAMS, ROUNDS = 12, 15
WEEKS, PLAYOFF_TEAMS = 18, 6
STARTERS = 13           # weekly lineup slots; bench beyond this barely counts
BENCH_WEIGHT = 0.15
# Per-game coefficient of variation by category: low-count stats are noisier.
CV = {"PTS": 0.30, "REB": 0.35, "AST": 0.40, "3PTM": 0.55,
      "ST": 0.70, "BLK": 0.75, "TO": 0.50}
PCT_WEEK_SD = 0.012     # weekly team FG%/FT% sd, fraction units (~1.2 pts)
TEAM_WEEK_SHOCK = 0.06  # shared games-played shock, correlates counting cats


# --------------------------------------------------------------------------
# Strategy personalities
# --------------------------------------------------------------------------
# Knobs (all optional; defaults neutral):
#   punt: cats ignored | matrix_aware: contested-category weighting (council)
#   locked_w / lost_w: weight for cats ranked top-2 / 10+ once matrix-aware
#   risk: "normal" (production availability), "safe" (avoid injury-flagged),
#         "upside" (ignore discounts) | rec_compound: council recovery rule
#   need_w: positional-need bonus | scarcity_w: dry-position response
#   stack_pen: 3rd-same-NBA-team penalty | value_exp: >1 favors stars
#   noise: gaussian pick noise (the "market" persona)

DEFAULT = dict(punt=(), matrix_aware=False, locked_w=0.35, lost_w=0.45,
               risk="normal", rec_compound=False, need_w=0.0,
               scarcity_w=0.0, stack_pen=0.0, value_exp=1.0, noise=0.0)

STRATEGIES = {
    "council":     dict(matrix_aware=True, rec_compound=True, stack_pen=0.5,
                        need_w=0.3),          # the production ruleset
    "bpa_pure":    dict(),
    "punt_ft":     dict(punt=("FT%",), matrix_aware=True),
    "punt_ast":    dict(punt=("AST",), matrix_aware=True),
    "punt_ft_to":  dict(punt=("FT%", "TO"), matrix_aware=True),
    "stars":       dict(value_exp=1.35),
    "slot_filler": dict(need_w=1.2),
    "scarcity":    dict(scarcity_w=1.0, need_w=0.4),
    "safe_floor":  dict(risk="safe"),
    "upside":      dict(risk="upside", value_exp=1.15),
    "specialist":  dict(matrix_aware=True, locked_w=1.4, lost_w=0.2),
    "market":      dict(noise=0.6),           # adp-like ordinary league-mate
}


def load_pool():
    players = hoops.zscores(hoops.load_players())
    return [p for p in players if hoops.availability(p) > 0]


def positions_of(p):
    return [s.strip() for s in p["pos"].replace('"', "").split(",")]


def strategy_params(name, overrides=None):
    params = dict(DEFAULT)
    params.update(STRATEGIES[name])
    if overrides:
        params.update(overrides)
    return params


def pick_for(params, pool, roster, my_ranks, rnd, rng):
    """Score every available player under this strategy's knobs; take max."""
    remaining = ROUNDS - len(roster)
    unfilled = [b for b in BASE_POS
                if not any(b in positions_of(p) for p in roster)]
    must_fill = len(unfilled) >= remaining  # hard feasibility guard
    team_ct, rec_ct = {}, 0
    for p in roster:
        team_ct[p["team"]] = team_ct.get(p["team"], 0) + 1
        if "recovery" in (p.get("note") or "").lower():
            rec_ct += 1
    scarce = {}
    if params["scarcity_w"]:
        top = sorted(pool, key=lambda p: -hoops.adj_value(p))[:100]
        for b in BASE_POS:
            scarce[b] = sum(1 for p in top if b in positions_of(p))

    def weight(cat):
        if cat in params["punt"]:
            return 0.0
        if params["matrix_aware"] and my_ranks and len(roster) >= 2:
            r = my_ranks[cat]
            if r <= 2:
                return params["locked_w"]
            if r >= 10:
                return params["lost_w"]
        return 1.0

    def score(p):
        s = sum(p["z"][c] * weight(c) for c in CATS)
        note = (p.get("note") or "").lower()
        injury_note = "inj" in note or note.startswith("out-")
        if params["risk"] != "upside":
            av = hoops.availability(p)
            if params["rec_compound"] and "recovery" in note:
                av *= 0.85 if rec_ct == 1 else (0.7 if rec_ct >= 2 else 1.0)
            s = s * av if s > 0 else s
        if params["value_exp"] != 1.0:
            s = math.copysign(abs(s) ** params["value_exp"], s)
        if params["need_w"] and unfilled:
            fills = sum(1 for b in unfilled if b in positions_of(p))
            s += params["need_w"] * fills * (0.5 + rnd / ROUNDS)
        if params["scarcity_w"]:
            for b in positions_of(p):
                if scarce.get(b, 99) <= 8:
                    s += params["scarcity_w"] * (9 - scarce[b]) / 8
        if params["stack_pen"] and team_ct.get(p["team"], 0) >= 2:
            s -= params["stack_pen"]
        if params["noise"]:
            s += rng.gauss(0, params["noise"])
        if params["risk"] == "safe" and injury_note:
            s -= 100.0  # avoid, but preserve ordering when forced
        return s

    cands = pool
    if must_fill:
        filtered = [p for p in pool
                    if any(b in positions_of(p) for b in unfilled)]
        cands = filtered or pool
    return max(cands, key=score)


def ranks_for(rosters, me):
    totals = {i: {c: sum(p["z"][c] for p in r) for c in CATS}
              for i, r in rosters.items()}
    mine = totals[me]
    return {c: 1 + sum(1 for i, t in totals.items()
                       if i != me and t[c] > mine[c]) for c in CATS}


def run_draft(order, pool_master, rng, param_overrides=None):
    pool = list(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    for n in range(TEAMS * ROUNDS):
        slot = hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        params = strategy_params(name, (param_overrides or {}).get(name))
        ranks = (ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = pick_for(params, pool, rosters[slot], ranks, n // TEAMS + 1, rng)
        rosters[slot].append(p)
        pool.remove(p)
    return rosters


# --------------------------------------------------------------------------
# Season Monte Carlo — weekly H2H categories, fixed top-6 bracket
# --------------------------------------------------------------------------

def weekly_availability(p):
    note = (p.get("note") or "").lower()
    if "recovery" in note:
        return 0.60
    if "risk" in note:
        return 0.75
    return 0.88


def team_week_model(roster):
    """Per-category weekly (mu, var). Only STARTERS players count fully;
    deep bench is discounted. Counting-stat variance = compound-sum
    E[G]*Var[X] + Var[G]*E[X]^2 with category-specific per-game CV and
    availability-tier game-count variance Var[G] = 3.5*a*(1-a)."""
    mu = {c: 0.0 for c in CATS}
    var = {c: 0.0 for c in CATS}
    ordered = sorted(roster, key=lambda p: -sum(p["z"][c] for c in CATS))
    fg_mk = fg_at = ft_mk = ft_at = 0.0
    for i, p in enumerate(ordered):
        w = 1.0 if i < STARTERS else BENCH_WEIGHT
        a = weekly_availability(p)
        g = 3.5 * a
        g_var = 3.5 * a * (1 - a)
        for c, col in hoops.COUNT_COLS.items():
            x = p[col]
            mu[c] += w * x * g
            var[c] += w * ((x * CV[c]) ** 2 * g + x ** 2 * g_var)
        fg_mk += w * p["fg_pct"] * p["fga"] * g
        fg_at += w * p["fga"] * g
        ft_mk += w * p["ft_pct"] * p["fta"] * g
        ft_at += w * p["fta"] * g
    mu["FG%"], var["FG%"] = fg_mk / (fg_at or 1), PCT_WEEK_SD ** 2
    mu["FT%"], var["FT%"] = ft_mk / (ft_at or 1), PCT_WEEK_SD ** 2
    return mu, var


def simulate_seasons(rosters, seasons, rng):
    models = {i: team_week_model(r) for i, r in rosters.items()}
    sigmas = {i: {c: math.sqrt(models[i][1][c]) or 1e-6 for c in CATS}
              for i in rosters}
    champs = {i: 0 for i in rosters}
    playoffs = {i: 0 for i in rosters}
    counting = set(hoops.COUNT_COLS)

    def week_result(a, b):
        # shared games-played shock correlates a team's counting cats
        sh_a = rng.gauss(1.0, TEAM_WEEK_SHOCK)
        sh_b = rng.gauss(1.0, TEAM_WEEK_SHOCK)
        wins = 0
        for c in CATS:
            ma = models[a][0][c] * (sh_a if c in counting else 1.0)
            mb = models[b][0][c] * (sh_b if c in counting else 1.0)
            sa = rng.gauss(ma, sigmas[a][c])
            sb = rng.gauss(mb, sigmas[b][c])
            better = sa < sb if c == "TO" else sa > sb
            wins += 1 if better else -1
        return wins > 0  # 9 cats: no ties

    ids = list(rosters)
    for _ in range(seasons):
        record = {i: 0 for i in ids}
        for _w in range(WEEKS):
            pairing = ids[:]
            rng.shuffle(pairing)
            for k in range(0, TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                if week_result(a, b):
                    record[a] += 1
                else:
                    record[b] += 1
        seeds = sorted(ids, key=lambda i: (-record[i], rng.random()))
        top = seeds[:PLAYOFF_TEAMS]
        for i in top:
            playoffs[i] += 1
        # seeds 1-2 byes; 3v6, 4v5; FIXED bracket (Yahoo default, no reseed)
        qf = [(top[2], top[5]), (top[3], top[4])]
        w1 = [a if week_result(a, b) else b for a, b in qf]
        sf = [(top[0], w1[1]), (top[1], w1[0])]
        w2 = [a if week_result(a, b) else b for a, b in sf]
        champs[w2[0] if week_result(*w2) else w2[1]] += 1
    return champs, playoffs


# --------------------------------------------------------------------------
# Tournament: rotations x slots x seeds
# --------------------------------------------------------------------------

def tournament(seasons, seed, rotations=1, param_overrides=None, names=None):
    """One seed's tournament. Each rotation round shuffles the strategy
    order (varying draft-slot adjacency), then cycles it through all 12
    slots so every strategy sees every slot exactly once per round."""
    rng = random.Random(seed)
    pool = load_pool()
    names = names or list(STRATEGIES)
    total_c = {n: 0 for n in names}
    total_p = {n: 0 for n in names}
    for rr in range(rotations):
        base = names[:]
        if rr:
            rng.shuffle(base)
        for rotation in range(TEAMS):
            order = base[rotation:] + base[:rotation]
            rosters = run_draft(order, pool, rng, param_overrides)
            champs, plays = simulate_seasons(rosters, seasons, rng)
            for slot, name in enumerate(order, 1):
                total_c[name] += champs[slot]
                total_p[name] += plays[slot]
    denom = seasons * TEAMS * rotations
    return {n: {"champ_pct": 100 * total_c[n] / denom,
                "playoff_pct": 100 * total_p[n] / denom} for n in names}


def evaluate(seasons, seeds, rotations, param_overrides=None):
    """Aggregate over a FIXED seed list; returns mean and cross-seed spread."""
    names = list(STRATEGIES)
    per_seed = {n: [] for n in names}
    for s in seeds:
        res = tournament(seasons, s, rotations, param_overrides)
        for n in names:
            per_seed[n].append(res[n]["champ_pct"])
    out = {}
    for n in names:
        vals = per_seed[n]
        out[n] = {"champ_pct": sum(vals) / len(vals),
                  "spread": max(vals) - min(vals)}
    return out


def main():
    ap = argparse.ArgumentParser(prog="arena.py", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft", help="run one 12-team draft, print rosters")
    d.add_argument("--seed", type=int, default=1)
    t = sub.add_parser("tournament", help="rotations x seeds x seasons")
    t.add_argument("--seasons", type=int, default=200)
    t.add_argument("--seeds", type=int, default=3,
                   help="number of seeds averaged (fixed list from --seed)")
    t.add_argument("--rotations", type=int, default=3,
                   help="shuffled rotation rounds per seed (12 drafts each)")
    t.add_argument("--seed", type=int, default=1)
    t.add_argument("--generations", type=int, default=1)
    t.add_argument("--out", default=os.path.join(ARENA_DIR, "results"))
    args = ap.parse_args()

    if args.cmd == "draft":
        rng = random.Random(args.seed)
        rosters = run_draft(list(STRATEGIES), load_pool(), rng)
        for slot, name in enumerate(STRATEGIES, 1):
            print(f"T{slot:<2} {name:<12} " +
                  ", ".join(p["player"] for p in rosters[slot][:7]) + " ...")
        return

    seed_list = [args.seed + 97 * k for k in range(args.seeds)]  # FIXED set
    overrides, history = {}, []
    for gen in range(args.generations):
        results = evaluate(args.seasons, seed_list, args.rotations, overrides)
        board = sorted(results.items(), key=lambda kv: -kv[1]["champ_pct"])
        n_seasons = args.seasons * TEAMS * args.rotations * args.seeds
        print(f"\n=== GENERATION {gen} — {n_seasons} seasons/strategy, "
              f"seeds {seed_list}, {args.rotations} rotations ===")
        for name, r in board:
            mark = " *mutated" if overrides.get(name) else ""
            print(f"  {name:<12} champ {r['champ_pct']:5.2f}%  "
                  f"(±{r['spread']:.2f} across seeds){mark}")
        history.append({"generation": gen, "results": results,
                        "overrides": dict(overrides)})
        if gen + 1 < args.generations:
            # baseline hill-climb on the SAME fixed seeds (attributable)
            rng = random.Random(args.seed * 100 + gen)
            tops = [n for n, _ in board[:3]]
            bottoms = [n for n, _ in board[-3:]]
            for loser, winner in zip(bottoms, tops):
                base = strategy_params(winner, overrides.get(winner))
                mut = dict(base)
                for k in ("locked_w", "lost_w", "need_w", "scarcity_w",
                          "stack_pen", "value_exp", "noise"):
                    mut[k] = round(max(0.0, base[k] + rng.gauss(0, 0.15)), 3)
                overrides[loser] = mut
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, f"tournament_seed{args.seed}.json")
    with open(path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"\nresults written: {path}")


if __name__ == "__main__":
    main()
