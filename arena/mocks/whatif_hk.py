#!/usr/bin/env python3
"""Owner question 2026-10-12: Haliburton at #10 and Towns at #15, against Towns at #10 and Haliburton at #15.
One room per call:  python3 whatif_hk.py <mock> <out.json>
All arms on the current pool (tag v58 = v59 values), the owner's other eleven picks as drafted, strict pairwise swaps
(the live_retro convention), 18,000 CRN seasons (seeds 11/23/47) on the league's real eight-team bracket.
  as_drafted            the room as it happened, re-graded on v58
  both                  Towns + Haliburton at #10/#15 (the same thirteen men in either order)
  K_noH_j               Towns at #10; Haliburton taken at pick j (that seat's real pick goes back on the board);
                        #15 = the card's #1 on that board
  H_noK_j               Haliburton at #10; Towns taken at pick j; #15 = the card's #1 on that board
for j in {11, 14} (the first and the last pick before #15)."""
import sys, os, json
MOCK = int(sys.argv[1]); OUT = sys.argv[2]
DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.argv = ["live_retro.py", str(MOCK), "--tag", "v58"]
sys.path.insert(0, DECK + "/arena/mocks")
import live_retro as lr
hoops, arena = lr.hoops, lr.arena
K, H = "Karl-Anthony Towns", "Tyrese Haliburton"
LINES2526 = os.environ.get("LINES2526") == "1"
if LINES2526:   # sensitivity: every pool row with 2025-26 GP >= 40 on its 2025-26 per-game actuals (bref + ESPN, verified)
    import csv, unicodedata
    _norm = lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower().replace('.', '').replace("'", '')
    _A = {_norm(r["player"]): r for r in csv.DictReader(open(DECK + "/arena/results/actuals_2026-10-09/actuals_2025-26.csv", encoding="utf-8"))}
    hoops.DATA_PATH = lr.POOLS["v58"]; _raw = hoops.load_players()
    for _p in _raw:
        _a = _A.get(_norm(_p["player"]))
        if _a and float(_a["gp"]) >= 40:
            for _f in ("fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"): _p[_f] = float(_a[_f])
    players = hoops.zscores(_raw)
else:
    players = lr.load_pool("v58")
HEALTHY = "--hali-healthy" in sys.argv[0:0] or os.environ.get("HALI_HEALTHY") == "1"
if HEALTHY:   # sensitivity: Haliburton's first-season-back tag cleared (value x1.0, weekly 0.88), everything else as shipped
    for _p in players:
        if _p["player"] == H: _p["note"] = ""
byn = {p["player"]: p for p in players}
SLOT, TEAMS = lr.SLOT, lr.TEAMS
base = [dict(pk) for pk in lr.PICKS]

def put(picks, n, name):
    """Strict pairwise: `name` to index n; whoever held `name` gets n's man (or he leaves the board if `name` was undrafted)."""
    cur = picks[n]["player"]
    if cur == name: return
    j = next((i for i, pk in enumerate(picks) if pk["player"] == name), None)
    picks[n]["player"] = name
    if j is not None: picks[j]["player"] = cur

def card1(picks, n):
    """The card's #1 before index n on this board (live_retro.card / stage_arms port)."""
    taken = {pk["player"] for pk in picks[:n]}
    ros = {s: [] for s in range(1, TEAMS + 1)}
    for pk in picks[:n]:
        if pk["player"] in byn: ros[pk["slot"]].append(byn[pk["player"]])
    mine = ros[SLOT]; opp = [r for s, r in ros.items() if s != SLOT and r]
    veto = hoops.do_not_draft()   # the current deck: the owner veto is on for every room here
    pool = [p for p in players if p["player"] not in taken and hoops.availability(p) > 0 and p["player"] not in veto]
    pool = lr.card_pool(pool, n)
    vals = [hoops.adj_value(p, ()) for p in pool]
    models = [arena.team_week_model(r) for r in opp]
    b = lr.pwins(arena.team_week_model(mine), models) if mine else 0.0
    decw = [lr.pwins(arena.team_week_model(mine + [p]), models) - b for p in pool]
    pd, pv = lr.pct(decw), lr.pct(vals)
    ds = [0.5 * pd[i] + 0.5 * pv[i] for i in range(len(pool))]
    order = sorted(range(len(pool)), key=lambda i: (-ds[i], -decw[i], [-ord(ch) for ch in pool[i]["player"]]))
    return [(pool[i]["player"], round(ds[i], 4), round(decw[i], 3)) for i in order[:5]]

def grade(picks):
    ros = {s: [] for s in range(1, TEAMS + 1)}
    for pk in picks:
        if pk["player"] in byn: ros[pk["slot"]].append(byn[pk["player"]])
    models = {s: arena.team_week_model(r) for s, r in ros.items()}
    ecw = lr.pwins(models[SLOT], [models[o] for o in ros if o != SLOT])
    res = lr.run_arm(ros); me = res[SLOT]
    rank = 1 + sum(1 for s in ros if s != SLOT and res[s][0] > me[0])
    return dict(champ=round(me[0], 3), playoff=round(me[1], 2), champ_rank=rank, ecw=round(ecw, 3),
                roster=[p["player"] for p in ros[SLOT]])

names = [pk["player"] for pk in base]
assert K in names[9:] and H in names[9:], "both men must be on the board at #10"
out = dict(mock=MOCK, tag="v58", haliburton_healthy=HEALTHY, lines_2025_26=LINES2526, owner10=names[9], owner15=names[14],
           where={K: names.index(K) + 1, H: names.index(H) + 1},
           picks_11_14=[(i + 1, base[i]["slot"], names[i]) for i in range(10, 14)],
           missing_from_v58=sorted({n for n in names if n not in byn}), arms={})
arms = {}
p = [dict(x) for x in base]; arms["as_drafted"] = (p, None)
p = [dict(x) for x in base]; put(p, 9, H); put(p, 14, K); arms["both"] = (p, None)
for j in (11, 14):
    for first, gone, tag in ((K, H, "K_noH"), (H, K, "H_noK")):
        p = [dict(x) for x in base]
        put(p, 9, first)
        put(p, j - 1, gone)           # that seat takes the other man; its real pick goes back to where `gone` sat
        top = card1(p, 14)
        put(p, 14, top[0][0])
        arms[f"{tag}_{j}"] = (p, top)
for k, (p, top) in arms.items():
    g = grade(p); g["card15"] = top; g["owner_10_15"] = (p[9]["player"], p[14]["player"])
    g["seat_j_took"] = [(i + 1, p[i]["player"]) for i in range(10, 14)]
    out["arms"][k] = g
    print(f"m{MOCK} {k:10} #10 {p[9]['player']:20} #15 {p[14]['player']:22} champ {g['champ']:6.2f} (rank {g['champ_rank']}) ECW {g['ecw']:.3f}" + (f"  card15 {top[:3]}" if top else ""), flush=True)
json.dump(out, open(OUT, "w"), indent=1)
