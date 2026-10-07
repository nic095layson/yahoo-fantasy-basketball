#!/usr/bin/env python3
"""All 30 card rosters dropped into the REAL room (eleven real rosters unchanged), both pools, 6,000 CRN seasons on seed 11:
isolates the roster effect from the room effect."""
import sys, json, random, math
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad/ls2025"
D = "/home/user/yahoo-fantasy-basketball"; sys.path.insert(0, D + "/scripts"); sys.path.insert(0, D + "/arena")
import hoops, arena
CATS = hoops.CATS; SLOT = 4
POOLS = {"ex_ante": S + "/pool_2025.csv", "ex_post": S + "/pool_actual.csv"}
real = json.load(open(S + "/draft_state_real_2025.json")); rooms = json.load(open(S + "/rooms_2025.json"))
def pwin_cats(my, om):
    out = {}
    for c in CATS:
        d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9); pr = 0.5 * (1 + math.erf(d / math.sqrt(2))); out[c] = (1 - pr) if c == "TO" else pr
    return out
def pwins(my, opps): return sum(sum(pwin_cats(my, om).values()) for om in opps) / len(opps)
OUT = {}
for tag, path in POOLS.items():
    hoops.DATA_PATH = path; players = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in players}
    ros = {s: [] for s in range(1, 13)}
    for pk in real["picks"]: ros[pk["slot"]].append(by[pk["player"]])
    opp_models = [arena.team_week_model(ros[o]) for o in ros if o != SLOT]
    def score(mine):
        R = dict(ros); R[SLOT] = mine
        ecw = pwins(arena.team_week_model(mine), opp_models)
        c, p = arena.simulate_seasons(R, 6000, random.Random(11))
        return dict(ecw=round(ecw, 3), champ=round(100 * c[SLOT] / 6000, 2), playoff=round(100 * p[SLOT] / 6000, 2))
    res = dict(real=score(ros[SLOT]), rooms=[])
    for rm in rooms["rooms"]:
        mine = [by[pk["player"]] for pk in rm["picks"] if pk["slot"] == SLOT]
        r = score(mine); r["seed"] = rm["seed"]; r["opening"] = mine[0]["player"]; res["rooms"].append(r)
        print(tag, rm["seed"], r, flush=True)
    OUT[tag] = res
    ch = sorted(x["champ"] for x in res["rooms"]); print(tag, "real", res["real"], "| card rosters vs the real room: median champ", ch[15], "range", ch[0], ch[-1], "beat real in", sum(1 for x in res["rooms"] if x["champ"] > res["real"]["champ"]), "of 30", flush=True)
json.dump(OUT, open(S + "/swap_spread_2025.json", "w"), indent=1); print("written")
