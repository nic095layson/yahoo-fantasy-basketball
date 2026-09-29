#!/usr/bin/env python3
"""Third implementation of the deck's weekly category-win model and blend
ordering (system validation 2026-09-29, owner decision D5).

Written from the SPECIFICATION — the engine block's comments and constants
(instrument v2 daily-fill start rates, availability tiers, 3.5·a games with
binomial game-count variance, per-category CV, percentage mix inflation, the
FNV-style hash, the lineup slots, percentile blend at 0.5, the card's sort
key) and the 2026-08-04/05 arena findings — WITHOUT importing arena/arena.py
or scripts/hoops.py and without executing the page. It reads DATA only: the
PLAYERS array baked into docs/draft-deck.html (z, av, raw rows, notes) and
the committed draft states. It is compared against the engine's own numbers
dumped by arena/mocks/decw_reference.mjs.

    python3 arena/mocks/decw_third.py <deck.html> <states_dir> <reference.json> <out.json> [--approx-cdf]

Two modes: the default uses the exact normal CDF (math.erf) where the spec
says Φ; --approx-cdf uses the Abramowitz–Stegun 7.1.26 polynomial the engine
uses, so the two runs separate "same model" from "same rounding".
"""
import json, math, os, re, sys
from functools import cmp_to_key

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
COUNT_IDX = {"3PTM": 0, "PTS": 1, "REB": 2, "AST": 3, "ST": 4, "BLK": 5, "TO": 6}
R_FGP, R_FGA, R_FTP, R_FTA = 7, 8, 9, 10          # raw row: tpm,pts,reb,ast,stl,blk,tov,fg_pct,fga,ft_pct,fta
CV = {"PTS": 0.30, "REB": 0.35, "AST": 0.40, "3PTM": 0.55, "ST": 0.70, "BLK": 0.75, "TO": 0.50}
PCT_MIX_INFL, ALPHA = 1.15, 0.5
DF_K = 32
DAY_W = [1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4]
LINEUP = [["PG"], ["SG"], ["PG", "SG"], ["SF"], ["PF"], ["SF", "PF"], ["C"], ["C"], None, None]
M32 = 0xFFFFFFFF


def tag_of(note):
    return re.split(r"[\s(]", (note or "").lower(), 1)[0]


def weekly_avail(p):
    t = tag_of(p.get("note"))
    if t.endswith("-recovery"):
        return 0.60
    if t.endswith("-risk") or t in ("risk", "inj-risk"):
        return 0.75
    if "recovery" in t:
        return 0.60
    if "risk" in t:
        return 0.75
    return 0.88


def positions_of(p):
    return [s.strip() for s in p["p"].split(",")]


def adj_value(p):
    tv = sum(p["z"][c] for c in CATS)
    return tv * p["av"] if tv > 0 else tv


def imul(a, b):
    return ((a & M32) * (b & M32)) & M32


def df_hash(s, k, salt):
    """Spec: FNV-1a-shaped 32-bit hash over the string's UTF-16 code units, seeded
    by k and salt through two multiplicative constants, then a murmur-style
    finalizer; result in [0, 1)."""
    h = (2166136261 ^ imul(k, 2654435761) ^ imul(salt, 2246822519)) & M32
    units = s.encode("utf-16-le")
    for i in range(0, len(units), 2):
        h ^= units[i] | (units[i + 1] << 8)
        h = imul(h, 16777619)
    h ^= h >> 15
    h = imul(h, 2246822507)
    h ^= h >> 13
    h = imul(h, 3266489909)
    h ^= h >> 16
    return (h & M32) / 4294967296.0


def daily_fill_weights(roster):
    """Start rate = started / played over DF_K simulated weeks: each week a player
    gets 2/3/4/5 games (8% / 55% / 35% / 2%), spread over the week's days by the
    day weights without replacement; each game is played with probability equal
    to his availability tier; each day the played players fill the ten lineup
    slots in value order (first eligible slot, then a util slot); the rest sit."""
    val = {p["n"]: sum(p["z"][c] for c in CATS) for p in roster}
    started = {p["n"]: 0 for p in roster}
    played = {p["n"]: 0 for p in roster}
    for k in range(DF_K):
        by_day = [[] for _ in range(7)]
        for p in roster:
            u = df_hash(p["n"], k, 1)
            g = 2 if u < 0.08 else 3 if u < 0.63 else 4 if u < 0.98 else 5
            days = [0, 1, 2, 3, 4, 5, 6]
            a = weekly_avail(p)
            for j in range(g):
                u2 = df_hash(p["n"], k, 10 + j)
                tot = sum(DAY_W[d] for d in days)
                r = u2 * tot
                acc = 0.0
                pick = days[-1]
                for d in days:
                    acc += DAY_W[d]
                    if r < acc:
                        pick = d
                        break
                days.remove(pick)
                if df_hash(p["n"], k, 20 + pick) < a:
                    played[p["n"]] += 1
                    by_day[pick].append(p)
        for d in range(7):
            cands = sorted(by_day[d], key=lambda q: (-val[q["n"]], q["n"]))
            open_slots = list(LINEUP)
            for q in cands:
                pos = positions_of(q)
                idx = next((i for i, sl in enumerate(open_slots) if sl is not None and any(b in pos for b in sl)), -1)
                if idx == -1:
                    idx = next((i for i, sl in enumerate(open_slots) if sl is None), -1)
                if idx != -1:
                    open_slots.pop(idx)
                    started[q["n"]] += 1
    return {p["n"]: (started[p["n"]] / played[p["n"]] if played[p["n"]] else 1.0) for p in roster}


def team_week_model(roster):
    """Per-category weekly mean and variance: counting stats are compound sums
    (E[G]·Var[X] + Var[G]·E[X]², per-game CV, G = 3.5·a with Var 3.5·a·(1−a)),
    each player scaled by his daily-fill start rate; percentages are
    attempt-weighted makes over attempts with a binomial floor inflated by the
    mix factor."""
    mu = {c: 0.0 for c in CATS}
    va = {c: 0.0 for c in CATS}
    lw = daily_fill_weights(roster)
    fg_mk = fg_at = ft_mk = ft_at = 0.0
    for p in roster:
        w = lw.get(p["n"], 1.0)
        a = weekly_avail(p)
        g = 3.5 * a
        g_var = 3.5 * a * (1 - a)
        for c, i in COUNT_IDX.items():
            x = p["r"][i]
            mu[c] += w * x * g
            va[c] += w * ((x * CV[c]) ** 2 * g + x * x * g_var)
        fg_mk += w * p["r"][R_FGP] * p["r"][R_FGA] * g
        fg_at += w * p["r"][R_FGA] * g
        ft_mk += w * p["r"][R_FTP] * p["r"][R_FTA] * g
        ft_at += w * p["r"][R_FTA] * g
    p_fg = fg_mk / (fg_at or 1)
    p_ft = ft_mk / (ft_at or 1)
    mu["FG%"] = p_fg
    va["FG%"] = (PCT_MIX_INFL ** 2) * max(p_fg * (1 - p_fg), 1e-4) / (fg_at or 1)
    mu["FT%"] = p_ft
    va["FT%"] = (PCT_MIX_INFL ** 2) * max(p_ft * (1 - p_ft), 1e-4) / (ft_at or 1)
    return mu, va


def cdf_exact(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def cdf_approx(x):
    ax = abs(x) / math.sqrt(2)
    t = 1 / (1 + 0.3275911 * ax)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    erf = 1 - poly * math.exp(-ax * ax)
    return 0.5 * (1 + (-erf if x < 0 else erf))


def pwins_total(mine, opps, cdf):
    """Expected categories won per week against the room: for every opponent and
    category, P(my weekly total beats his) under independent normals; turnovers
    are won by being lower."""
    if not opps:
        return 0.0
    tot = 0.0
    for om in opps:
        for c in CATS:
            d = (mine[0][c] - om[0][c]) / (math.sqrt(mine[1][c] + om[1][c]) or 1e-9)
            pr = cdf(d)
            tot += (1 - pr) if c == "TO" else pr
    return tot / len(opps)


def pct_ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])   # stable, like the engine's sort
    den = (len(vals) - 1) or 1
    out = [0.0] * len(vals)
    for r, i in enumerate(order):
        out[i] = r / den
    return out


def decw_scores(pool, mine, opp_rosters, cdf):
    vals = [adj_value(p) for p in pool]
    opps = [team_week_model(r) for r in opp_rosters if r]
    if not opps:
        pv0 = pct_ranks(vals)
        return [{"n": p["n"], "ds": pv0[i], "decw": None} for i, p in enumerate(pool)]
    base = pwins_total(team_week_model(mine), opps, cdf) if mine else 0.0
    decw = [pwins_total(team_week_model(mine + [p]), opps, cdf) - base for p in pool]
    pd, pv = pct_ranks(decw), pct_ranks(vals)
    return [{"n": p["n"], "decw": decw[i], "ds": ALPHA * pd[i] + (1 - ALPHA) * pv[i]} for i, p in enumerate(pool)]


def rank_card(rows):
    def cmp(a, b):
        if b["ds"] != a["ds"]:
            return -1 if b["ds"] < a["ds"] else 1
        if a["decw"] is not None and b["decw"] is not None and b["decw"] != a["decw"]:
            return -1 if b["decw"] < a["decw"] else 1
        return 1 if a["n"] < b["n"] else (-1 if a["n"] > b["n"] else 0)
    return [r["n"] for r in sorted(rows, key=cmp_to_key(cmp))]


def team_of_pick(n, teams):
    r, i = divmod(n, teams)
    return i + 1 if r % 2 == 0 else teams - i


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    html_path, states_dir, ref_path, out_path = args
    cdf = cdf_approx if "--approx-cdf" in sys.argv else cdf_exact
    html = open(html_path, encoding="utf-8").read()
    players = json.loads(re.search(r"const PLAYERS = (\[.*?\]);", html, re.S).group(1))
    by = {p["n"]: p for p in players}
    ref = json.load(open(ref_path, encoding="utf-8"))

    # 1. the hash, bit for bit, on the parity vectors
    hash_bad = [(s, k, salt, df_hash(s, k, salt), v) for s, k, salt, v in ref["dfhash"] if df_hash(s, k, salt) != v]

    # 2. the owner's roster model at every turn where he has a roster
    model_max = 0.0
    fill_bad = 0
    for rm in ref["roster_models"]:
        st = json.load(open(os.path.join(states_dir, rm["state"]), encoding="utf-8"))
        mine = [by[pk["player"]] for pk in st["picks"][:rm["upto"]] if pk["slot"] == st["slot"] and pk["player"] in by]
        mu, va = team_week_model(mine)
        for c in CATS:
            model_max = max(model_max, abs(mu[c] - rm["mu"][c]), abs(va[c] - rm["va"][c]))
        w = daily_fill_weights(mine)
        for n, v in rm["fill"]:
            if abs(w[n] - v) > 1e-12:
                fill_bad += 1

    # 3. every candidate at every owner turn, and the card ordering
    turns = 0
    order_same = 0
    top5_same = 0
    first_div = []
    max_decw = 0.0
    max_ds = 0.0
    for t in ref["turns"]:
        st = json.load(open(os.path.join(states_dir, t["state"]), encoding="utf-8"))
        taken = set()
        ros = {}
        for pk in st["picks"][:t["upto"]]:
            taken.add(pk["player"])
            p = by.get(pk["player"])
            if p:
                ros.setdefault(pk["slot"], []).append(p)
        mine = ros.get(st["slot"], [])
        opp = [r for s, r in ros.items() if s != st["slot"]]
        pool = [p for p in players if p["n"] not in taken and p["av"] > 0]
        rows = decw_scores(pool, mine, opp, cdf)
        ref_rows = {n: (d, ds) for n, d, ds in t["rows"]}
        for r in rows:
            d0, ds0 = ref_rows[r["n"]]
            if r["decw"] is not None and d0 is not None:
                max_decw = max(max_decw, abs(r["decw"] - d0))
            max_ds = max(max_ds, abs(r["ds"] - ds0))
        order = rank_card(rows)
        turns += 1
        if order == t["order"]:
            order_same += 1
        else:
            i = next(i for i, (a, b) in enumerate(zip(order, t["order"])) if a != b)
            first_div.append({"state": t["state"], "pickNo": t["pickNo"], "firstDivergenceAt": i + 1,
                              "mine": order[i:i + 2], "engine": t["order"][i:i + 2]})
        if order[:5] == t["order"][:5]:
            top5_same += 1

    out = {"deck": html_path, "cdf": "approx (A-S 7.1.26)" if cdf is cdf_approx else "exact (math.erf)",
           "dfhash_vectors": len(ref["dfhash"]), "dfhash_mismatches": hash_bad,
           "roster_models": len(ref["roster_models"]), "roster_model_max_abs_diff": model_max, "fill_weight_mismatches": fill_bad,
           "turns": turns, "turns_with_identical_full_ordering": order_same, "turns_with_identical_top5": top5_same,
           "max_abs_decw_diff": max_decw, "max_abs_blend_diff": max_ds, "first_divergences": first_div[:10],
           "pass": (not hash_bad and fill_bad == 0 and order_same == turns and max_decw <= 1e-9 and max_ds <= 1e-9)}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: out[k] for k in ("cdf", "dfhash_mismatches", "roster_model_max_abs_diff", "fill_weight_mismatches", "turns",
                                          "turns_with_identical_full_ordering", "turns_with_identical_top5", "max_abs_decw_diff", "max_abs_blend_diff", "pass")}))


if __name__ == "__main__":
    main()
