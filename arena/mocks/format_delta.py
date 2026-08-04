"""Playoff-format calibration: the arena's 6-team-with-byes bracket vs the
owner's REAL league format (confirmed from 2025-26 standings: 8 of 12
qualify, no byes — 8 asterisked teams; the champion had the 7th-best record
and would not even qualify under the sim's 6-team format).

Measure-only. Re-simulates ledger mocks under both brackets at identical
seeds and reports the champ%/playoff% deltas for the owner seat and the
room's top seed.  Usage: python3 format_delta.py <mock> ...
"""
import sys, os, json, random, math

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}
UP = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/"
MOCKS = {21: ("773c5fc1-draft_state_10.json", 4),
         25: ("c0d8a926-draft_state_14.json", 2),
         27: ("5130afad-draft_state_16.json", 4),
         30: ("e7463e95-draft_state_19.json", 7)}


def simulate(rosters, seasons, rng, playoff_teams, byes):
    """Faithful copy of arena.simulate_seasons with a parametrized bracket.
    byes=True  -> 6-team Yahoo default (seeds 1-2 byes, 3v6 4v5)   [shipped]
    byes=False -> 8-team no-bye (1v8 2v7 3v6 4v5, fixed bracket)   [owner's real league]
    """
    models = {i: arena.team_week_model(r) for i, r in rosters.items()}
    sigmas = {i: {c: math.sqrt(models[i][1][c]) or 1e-6 for c in CATS} for i in rosters}
    champs = {i: 0 for i in rosters}
    playoffs = {i: 0 for i in rosters}
    counting = set(hoops.COUNT_COLS)

    def week_result(a, b):
        sh_a = rng.gauss(1.0, arena.TEAM_WEEK_SHOCK)
        sh_b = rng.gauss(1.0, arena.TEAM_WEEK_SHOCK)
        wins = 0
        for c in CATS:
            ma = models[a][0][c] * (sh_a if c in counting else 1.0)
            mb = models[b][0][c] * (sh_b if c in counting else 1.0)
            sa = rng.gauss(ma, sigmas[a][c])
            sb = rng.gauss(mb, sigmas[b][c])
            better = sa < sb if c == "TO" else sa > sb
            wins += 1 if better else 0
        return wins

    ids = list(rosters)
    for _ in range(seasons):
        record = {i: 0 for i in ids}
        for _w in range(arena.WEEKS):
            pairing = ids[:]
            rng.shuffle(pairing)
            for k in range(0, arena.TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                wa = week_result(a, b)
                record[a] += wa
                record[b] += 9 - wa
        seeds = sorted(ids, key=lambda i: (-record[i], rng.random()))
        top = seeds[:playoff_teams]
        for i in top:
            playoffs[i] += 1
        if byes:
            qf = [(top[2], top[5]), (top[3], top[4])]
            w1 = [a if week_result(a, b) >= 5 else b for a, b in qf]
            sf = [(top[0], w1[1]), (top[1], w1[0])]
        else:
            qf = [(top[0], top[7]), (top[3], top[4]), (top[1], top[6]), (top[2], top[5])]
            w1 = [a if week_result(a, b) >= 5 else b for a, b in qf]
            sf = [(w1[0], w1[1]), (w1[2], w1[3])]
        w2 = [a if week_result(a, b) >= 5 else b for a, b in sf]
        champs[w2[0] if week_result(*w2) >= 5 else w2[1]] += 1
    return champs, playoffs


SEEDS = [11, 23]
N = 6000
out = {}
for m in [int(x) for x in sys.argv[1:]] or list(MOCKS):
    fn, owner = MOCKS[m]
    st = json.load(open(UP + fn))
    ros = {}
    for pk in st["picks"]:
        ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
    res = {}
    for label, (pt, byes) in {"shipped_6team_byes": (6, True),
                              "real_8team_nobyes": (8, False)}.items():
        tc = {i: 0 for i in ros}
        tp = {i: 0 for i in ros}
        for sd in SEEDS:
            c, p = simulate(ros, N, random.Random(sd), pt, byes)
            for i in ros:
                tc[i] += c[i]
                tp[i] += p[i]
        T = N * len(SEEDS)
        order = sorted(ros, key=lambda x: -tc[x])
        res[label] = {
            "owner_champ": round(100 * tc[owner] / T, 2),
            "owner_playoff": round(100 * tp[owner] / T, 2),
            "owner_finish": order.index(owner) + 1,
            "top_team_champ": round(100 * tc[order[0]] / T, 2),
            "spread_top_minus_median": round(100 * (tc[order[0]] - tc[order[5]]) / T, 2),
        }
    out[m] = res
    a, b = res["shipped_6team_byes"], res["real_8team_nobyes"]
    print(f"m{m}: owner champ {a['owner_champ']:6.2f} -> {b['owner_champ']:6.2f}  "
          f"playoff {a['owner_playoff']:5.1f} -> {b['owner_playoff']:5.1f}   "
          f"room-best champ {a['top_team_champ']:6.2f} -> {b['top_team_champ']:6.2f}")
SP = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad"
json.dump(out, open(f"{SP}/format_delta_out.json", "w"), indent=1)
print("wrote format_delta_out.json")
