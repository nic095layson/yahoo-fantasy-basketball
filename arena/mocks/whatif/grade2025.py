#!/usr/bin/env python3
"""Phase 4: grade roster sets with the arena (the retro grader's method): ECW per seat, the owner's category ranks,
head-to-heads favored, title and playoff odds (18,000 CRN seasons, seeds 11/23/47 for the headline arms; 6,000 on seed 11
for the 30-room spread). Pools: the draft-time lines (ex ante) and the actual 2025-26 lines (ex post).
   python3 grade2025.py <out.json>"""
import sys, json, math, random, statistics
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad/ls2025"
D = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, D + "/scripts"); sys.path.insert(0, D + "/arena")
import hoops, arena
CATS = hoops.CATS; TEAMS = 12; SLOT = 4
POOLS = {"ex_ante": S + "/pool_2025.csv", "ex_post": S + "/pool_actual.csv"}
real = json.load(open(S + "/draft_state_real_2025.json")); rooms = json.load(open(S + "/rooms_2025.json"))
seat_of = {int(k): v for k, v in json.load(open(S + "/real_draft_2025.json"))["seat_of"].items()}
def load(tag):
    hoops.DATA_PATH = POOLS[tag]; return hoops.zscores(hoops.load_players())
def rosters(picks, players):
    by = {p["player"]: p for p in players}; ros = {s: [] for s in range(1, TEAMS + 1)}; missing = []
    for pk in picks:
        pl = by.get(pk["player"])
        if pl is None: missing.append(pk["player"]); continue
        ros[pk["slot"]].append(pl)
    return ros, missing
def pwin_cats(my, om):
    out = {}
    for c in CATS:
        d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
        pr = 0.5 * (1 + math.erf(d / math.sqrt(2)))
        out[c] = (1 - pr) if c == "TO" else pr
    return out
def pwins(my, opps): return sum(sum(pwin_cats(my, om).values()) for om in opps) / len(opps)
def run_arm(ros, seeds=(11, 23, 47), seasons=6000):
    champs = {s: 0 for s in ros}; plays = {s: 0 for s in ros}
    for sd in seeds:
        rng = random.Random(sd); c, p = arena.simulate_seasons(ros, seasons, rng)
        for s in ros: champs[s] += c[s]; plays[s] += p[s]
    tot = seasons * len(seeds); return {s: (100 * champs[s] / tot, 100 * plays[s] / tot) for s in ros}
def grade(picks, players, seeds=(11, 23, 47), seasons=6000, full=True):
    ros, missing = rosters(picks, players)
    models = {s: arena.team_week_model(r) for s, r in ros.items()}
    ecw = {s: pwins(models[s], [models[o] for o in ros if o != s]) for s in ros}
    ecw_rank = {s: 1 + sum(1 for o in ros if o != s and ecw[o] > ecw[s]) for s in ros}
    catp = {s: {c: statistics.mean(pwin_cats(models[s], models[o])[c] for o in ros if o != s) for c in CATS} for s in ros}
    cat_rank = {c: 1 + sum(1 for o in ros if o != SLOT and catp[o][c] > catp[SLOT][c]) for c in CATS}
    per_opp = {o: round(sum(pwin_cats(models[SLOT], models[o]).values()), 3) for o in ros if o != SLOT}
    favored = sum(1 for v in per_opp.values() if v > 4.5)
    out = dict(missing=missing, ecw={s: round(v, 3) for s, v in ecw.items()}, ecw_rank=ecw_rank, owner_cat_rank=cat_rank, owner_per_opp=per_opp, owner_favored=favored,
               rosters={s: [p["player"] for p in r] for s, r in ros.items()})
    if full:
        arm = run_arm(ros, seeds, seasons)
        out["champ"] = {s: round(v[0], 2) for s, v in arm.items()}; out["playoff"] = {s: round(v[1], 2) for s, v in arm.items()}
        out["owner_champ_rank"] = 1 + sum(1 for o in ros if o != SLOT and arm[o][0] > arm[SLOT][0])
    return out
OUT = {}
for tag in POOLS:
    players = load(tag)
    print(f"=== {tag}: real draft", flush=True)
    OUT.setdefault(tag, {})["real"] = grade(real["picks"], players)
    print(f"=== {tag}: canonical redraft (seed {rooms['rooms'][0]['seed']})", flush=True)
    OUT[tag]["redraft"] = grade(rooms["rooms"][0]["picks"], players)
    spread = []
    for rm in rooms["rooms"]:
        g = grade(rm["picks"], players, seeds=(11,), seasons=6000, full=True)
        spread.append(dict(seed=rm["seed"], ecw=g["ecw"][SLOT], ecw_rank=g["ecw_rank"][SLOT], champ=g["champ"][SLOT], champ_rank=g["owner_champ_rank"], playoff=g["playoff"][SLOT], favored=g["owner_favored"], roster=g["rosters"][SLOT]))
        print(f"  room {rm['seed']}: ECW {g['ecw'][SLOT]:.3f} rank {g['ecw_rank'][SLOT]} champ {g['champ'][SLOT]:.2f}% (rank {g['owner_champ_rank']})", flush=True)
    OUT[tag]["spread"] = spread
    for k in ("real", "redraft"):
        g = OUT[tag][k]; print(f"{tag} {k}: owner ECW {g['ecw'][SLOT]:.3f} rank {g['ecw_rank'][SLOT]}, favored {g['owner_favored']}/11, champ {g['champ'][SLOT]:.2f}% rank {g['owner_champ_rank']}, playoff {g['playoff'][SLOT]:.2f}%; missing {g['missing']}")
        print("   ECW by seat:", {seat_of[s]: g["ecw"][s] for s in sorted(g["ecw"], key=lambda s: -g["ecw"][s])})
        print("   champ by seat:", {seat_of[s]: g["champ"][s] for s in sorted(g["champ"], key=lambda s: -g["champ"][s])})
json.dump(dict(slot=SLOT, seat_of=seat_of, pools=POOLS, results=OUT), open(sys.argv[1], "w"), indent=1)
print("written", sys.argv[1])
