#!/usr/bin/env python3
"""Apples to apples: the card's seat-4 roster (room 1000) dropped into the REAL room against the eleven real rosters
unchanged (a hypothetical; overlaps ignored), on both pools — ECW, favored, title and playoff odds (18,000 CRN seasons)."""
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
    card = [by[pk["player"]] for pk in rooms["rooms"][0]["picks"] if pk["slot"] == SLOT]
    res = {}
    for lab, mine in (("real", ros[SLOT]), ("card", card)):
        R = dict(ros); R[SLOT] = mine
        models = {s: arena.team_week_model(r) for s, r in R.items()}
        ecw = pwins(models[SLOT], [models[o] for o in R if o != SLOT]); fav = sum(1 for o in R if o != SLOT and sum(pwin_cats(models[SLOT], models[o]).values()) > 4.5)
        champs = {s: 0 for s in R}; plays = {s: 0 for s in R}
        for sd in (11, 23, 47):
            c, p = arena.simulate_seasons(R, 6000, random.Random(sd))
            for s in R: champs[s] += c[s]; plays[s] += p[s]
        res[lab] = dict(ecw=round(ecw, 3), favored=fav, champ=round(100 * champs[SLOT] / 18000, 2), playoff=round(100 * plays[SLOT] / 18000, 2))
        print(tag, lab, res[lab], flush=True)
    OUT[tag] = res
json.dump(OUT, open(S + "/swap_2025.json", "w"), indent=1); print("written swap_2025.json")
