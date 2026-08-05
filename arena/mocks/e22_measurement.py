"""E22 measurement (owner-directed 2026-08-05): lineup-resilience ordering.

The owner's hypothesis: a roster should be built to BEST fill the weekly
starting lineup (positional balance), including keeping productive plug-in
depth for when starters miss games. This script measures whether an
ordering that prices exactly that beats the shipped ordering.

RESIL ordering = the shipped blend50 with ONE substitution inside the
DeltaECW half: static lineup weights become STOCHASTIC LINEUP FILL (SLF):
  a_p = weekly availability (0.88 / 0.75 risk / 0.60 recovery)
  K = 128 deterministic common-random-number draws; p active in draw k iff
    hash(name_p, k) < a_p
  each draw greedy-fills LINEUP_SLOTS among ACTIVE players only (identical
    value order + slot priority to lineup_weights)
  s_p = starts_p / actives_p (conditional start rate)
  w_p = s_p + (1 - s_p) * BENCH_WEIGHT        <- replaces the static weight
  games term g = 3.5 * a_p unchanged
A bench guard behind an injury-flagged starter gains weight (he plugs in);
a 4th center behind healthy centers keeps ~BENCH_WEIGHT (he cannot).

Arms per mock, one CRN-paired season set each (seeds 11/23/47 x 6000):
  baseline  - the mock as drafted
  shipped   - shipped card's #1 followed at every owner turn (running-board
              legality, pairwise swaps: the E20 machinery, verbatim)
  resil     - resil card's #1 followed the same way
Per-turn cards come from the CURRENT deck blocks + the E22 driver
(committed replays: arena/results/e22_replay_m{mock}.json).

Screening set (E21 law): ALL nine punted mocks 22/31/32/34/35/36/37/38/39
+ the four unpunted record mocks 21/24/25/26 as the registered
non-regression panel.

SHIP BAR — registered BEFORE any measurement ran (bar-registry law):
  resil replaces the incumbent ONLY if BOTH hold:
  (a) non-regression: resil-follow champ% >= shipped-follow - 1.5pp on
      EACH of m21/m24/m25/m26;
  (b) punted-set win: resil-follow > shipped-follow on >= 5 of the 9
      punted mocks AND mean(resil - shipped) over the nine > +1.0pp
      (above the E20-measured placebo scale of ~1-3pp single-mock noise).
  Anything else: incumbent stands; negative result written (E20 pattern).

Fresh clone + `python3 arena/mocks/e22_measurement.py` regenerates
arena/results/e22_measurement_out.json. Set E22_MOCKS=34 (etc.) for one
mock per process; partials land as e22_measurement_out_m<ids>.json.
"""
import json
import os
import random
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(REPO)
sys.path = [os.path.join(REPO, "scripts"), os.path.join(REPO, "arena")] + [
    p for p in sys.path if p not in (os.path.join(REPO, "scripts"), os.path.join(REPO, "arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}

PUNTED = ["22", "31", "32", "34", "35", "36", "37", "38", "39"]
UNPUNTED = ["21", "24", "25", "26"]
HEAD_SEEDS = [11, 23, 47]
HEAD_N = 6000


def slf_hash(name, k):
    """FNV-1a + murmur-style finalizer, identical to the JS driver."""
    h = (2166136261 ^ ((k * 2654435761) & 0xFFFFFFFF)) & 0xFFFFFFFF
    for ch in name:
        h ^= ord(ch) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    h ^= h >> 15
    h = (h * 2246822507) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 3266489909) & 0xFFFFFFFF
    h ^= h >> 16
    return h / 4294967296.0


def slf_weights(roster, K=128):
    ordered = sorted(roster, key=lambda p: -sum(p["z"][c] for c in CATS))
    starts = {p["player"]: 0 for p in roster}
    actives = {p["player"]: 0 for p in roster}
    for k in range(K):
        act = [p for p in ordered
               if slf_hash(p["player"], k) < arena.weekly_availability(p)]
        for p in act:
            actives[p["player"]] += 1
        open_slots = list(arena.LINEUP_SLOTS)
        for p in act:
            pos = arena.positions_of(p)
            claimed = None
            for i, s in enumerate(open_slots):
                if s is not None and any(b in s for b in pos):
                    claimed = i
                    break
            if claimed is None:
                for i, s in enumerate(open_slots):
                    if s is None:
                        claimed = i
                        break
            if claimed is not None:
                open_slots.pop(claimed)
                starts[p["player"]] += 1
    stat = arena.lineup_weights(roster)
    out = {}
    for p in roster:
        na = actives[p["player"]]
        s = starts[p["player"]] / na if na else stat.get(id(p), arena.BENCH_WEIGHT)
        out[p["player"]] = s + (1 - s) * arena.BENCH_WEIGHT
    return out


def ecw_readout(ros, owner, model):
    """expected cats won/week vs the room, under the given week model."""
    import math
    mods = {s: model(r) for s, r in ros.items()}
    me = mods[owner]
    tot = 0.0
    n = 0
    for s, om in mods.items():
        if s == owner:
            continue
        for c in CATS:
            mu_d = me[0][c] - om[0][c]
            sd = (me[1][c] + om[1][c]) ** 0.5 or 1e-9
            pr = 0.5 * (1 + math.erf(mu_d / sd / 2 ** 0.5))
            tot += (1 - pr) if c == "TO" else pr
        n += 1
    return tot / n


def std_model(r):
    m = arena.team_week_model(r)
    return (m["mu"], m["var"]) if isinstance(m, dict) else m


def slf_model(r):
    """team_week_model with SLF weights substituted (readout only)."""
    mu = {c: 0.0 for c in CATS}
    var = {c: 0.0 for c in CATS}
    lw = slf_weights(r)
    fg_mk = fg_at = ft_mk = ft_at = 0.0
    for p in r:
        w = lw[p["player"]]
        a = arena.weekly_availability(p)
        g = 3.5 * a
        g_var = 3.5 * a * (1 - a)
        for c, col in hoops.COUNT_COLS.items():
            x = p[col]
            mu[c] += w * x * g
            var[c] += w * ((x * arena.CV[c]) ** 2 * g + x ** 2 * g_var)
        fg_mk += w * p["fg_pct"] * p["fga"] * g
        fg_at += w * p["fga"] * g
        ft_mk += w * p["ft_pct"] * p["fta"] * g
        ft_at += w * p["fta"] * g
    p_fg = fg_mk / (fg_at or 1)
    p_ft = ft_mk / (ft_at or 1)
    mu["FG%"] = p_fg
    var["FG%"] = (arena.PCT_MIX_INFL ** 2) * max(p_fg * (1 - p_fg), 1e-4) / (fg_at or 1)
    mu["FT%"] = p_ft
    var["FT%"] = (arena.PCT_MIX_INFL ** 2) * max(p_ft * (1 - p_ft), 1e-4) / (ft_at or 1)
    return (mu, var)


def measure_mock(mk):
    state = json.load(open(f"arena/data/states/draft_state_mock{mk}.json"))
    OWNER = state["slot"]
    PUNT = list(state.get("punt") or [])
    assert (mk in PUNTED) == bool(PUNT), (mk, PUNT)
    KEPT = [c for c in CATS if c not in PUNT]
    picks = state["picks"]
    assert len(picks) == 156 and state["teams"] == 12 and state["size"] == 13
    assert not [pk["player"] for pk in picks if pk["player"] not in byname]
    OWNER_TURNS = [i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER]
    assert len(OWNER_TURNS) == 13

    replay = json.load(open(f"arena/results/e22_replay_m{mk}.json"))
    assert [t["pickNo"] for t in replay] == OWNER_TURNS
    for t in replay:
        assert t["actual"] == picks[t["pickNo"] - 1]["player"], (mk, t["pickNo"])
    cards = {k: {t["pickNo"]: [x["n"] for x in t[k]] for t in replay}
             for k in ("shipped", "resil")}
    ties = {k: [t["pickNo"] for t in replay
                if len(t[k]) > 1 and t[k][0]["ds"] == t[k][1]["ds"]]
            for k in ("shipped", "resil")}
    diverge = [t["pickNo"] for t in replay
               if t["shipped"][0]["n"] != t["resil"][0]["n"]]

    def finish_board(newp):
        ros = {}
        for pk in newp:
            ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
        for s in range(1, 13):
            assert len(ros[s]) == 13, (mk, s)
        assert len({pk["player"] for pk in newp}) == 156
        return ros

    def apply_card(cardmap):
        newp = [dict(pk) for pk in picks]
        swaps, noops = [], []
        for pn in OWNER_TURNS:
            i = pn - 1
            cur = newp[i]["player"]
            for nm in cardmap.get(pn, []):
                if nm == cur:
                    break
                j = next((k for k in range(len(newp)) if newp[k]["player"] == nm), None)
                if j is None or j <= i:
                    continue
                (noops if newp[j]["slot"] == OWNER else swaps).append([pn, cur, nm])
                newp[i]["player"], newp[j]["player"] = nm, cur
                break
        return finish_board(newp), swaps, noops

    def run(ros):
        tc = {s: 0 for s in ros}
        tp = {s: 0 for s in ros}
        for sd in HEAD_SEEDS:
            champs, plyf = arena.simulate_seasons(ros, HEAD_N, random.Random(sd))
            for s in ros:
                tc[s] += champs[s]
                tp[s] += plyf[s]
        T = HEAD_N * len(HEAD_SEEDS)
        return {"champ": round(100.0 * tc[OWNER] / T, 3),
                "playoff": round(100.0 * tp[OWNER] / T, 3),
                "finish": sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1,
                "seasons": T,
                "kept_z": round(sum(sum(p["z"][c] for c in KEPT) for p in ros[OWNER]), 2),
                "ecw_std": round(ecw_readout(ros, OWNER, std_model), 3),
                "ecw_slf": round(ecw_readout(ros, OWNER, slf_model), 3),
                "roster": [p["player"] for p in ros[OWNER]]}

    out = {"mock": mk, "owner_slot": OWNER, "punt": PUNT,
           "seeds": HEAD_SEEDS, "seasons_per_arm": HEAD_N * len(HEAD_SEEDS),
           "ties_at_top": ties, "top1_diverge_turns": diverge, "arms": {}}
    out["arms"]["baseline"] = run(finish_board([dict(pk) for pk in picks]))
    for k in ("shipped", "resil"):
        ros, swaps, noops = apply_card(cards[k])
        r = run(ros)
        r["swaps"] = swaps
        r["noop_swaps"] = noops
        out["arms"][k] = r
    return out


def main():
    only = os.environ.get("E22_MOCKS")
    todo = only.split(",") if only else PUNTED + UNPUNTED
    results = {}
    for mk in todo:
        print(f"=== mock {mk} ===", flush=True)
        results[mk] = measure_mock(mk)
        a = results[mk]["arms"]
        print(f"  baseline {a['baseline']['champ']:6.2f} | shipped-follow {a['shipped']['champ']:6.2f} "
              f"| resil-follow {a['resil']['champ']:6.2f} | top1-diverge "
              f"{len(results[mk]['top1_diverge_turns'])}/13", flush=True)
    out_path = ("arena/results/e22_measurement_out.json" if not only else
                f"arena/results/e22_measurement_out_m{'_'.join(todo)}.json")
    json.dump(results, open(out_path, "w"), indent=1)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
