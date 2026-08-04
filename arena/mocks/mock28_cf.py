"""Mock 28 counterfactuals. `python3 mock28_cf.py ARM [ARM...]` or no args for all.
Pairwise legal swaps only (alt drafted strictly later). 6000 seasons x seeds [11,23].

Sequential arms (the ECW-greedy bundle) are applied IN PICK ORDER against a running
board, because a swap can displace a player whom a later swap then targets.
"""
import sys, os, json, random, math

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/4cb343cd-draft_state_17.json"
OWNER = 5
state = json.load(open(STATE))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER
picks = state["picks"]
byname = {p["player"]: p for p in players}
CATS = hoops.CATS


def build_seq(seq):
    """seq: list of (pickNo, altPlayer) applied in order against a running board."""
    newp = [dict(pk) for pk in picks]
    for pn, alt in seq:
        i = pn - 1
        assert newp[i]["slot"] == OWNER, (pn, "not an owner pick")
        j = next((k for k in range(len(newp)) if newp[k]["player"] == alt), None)
        assert j is not None, (alt, "not in draft")
        assert j > i, (pn, alt, f"ILLEGAL: alt sits at #{j+1}, at or before the #{pn} turn")
        newp[i]["player"], newp[j]["player"] = alt, newp[i]["player"]
    ros = {}
    for pk in newp:
        ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == 156 and all(len(r) == 13 for r in ros.values())
    return ros


def ecw(ros, who=OWNER):
    mod = {i: arena.team_week_model(r) for i, r in ros.items()}
    tot = 0.0
    for c in CATS:
        s = 0.0
        for o in ros:
            if o == who:
                continue
            ma, va = mod[who][0][c], mod[who][1][c]
            mb, vb = mod[o][0][c], mod[o][1][c]
            d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            s += (1 - p) if c == "TO" else p
        tot += s / (len(ros) - 1)
    return tot


# card's system pick at each owner turn where the owner deviated (from the replay)
CARD = [(20, "Jayson Tatum"), (44, "Walker Kessler"), (53, "Ivica Zubac"),
        (92, "Deni Avdija"), (116, "Ausar Thompson"), (125, "John Collins"),
        (140, "Tobias Harris")]
# ECW-greedy oracle bundle (mock28_ecw_greedy.json), in pick order
GREEDY = [(5, "Zach LaVine"), (20, "Domantas Sabonis"), (29, "Franz Wagner"),
          (44, "Brandon Miller"), (53, "Myles Turner"), (68, "CJ McCollum"),
          (77, "Rudy Gobert"), (92, "Deni Avdija"), (101, "PJ Washington"),
          (116, "Kyle Filipowski"), (140, "Cedric Coward"), (149, "Keyonte George")]

KEPTGREEDY = [(5, 'Tobias Harris'), (20, 'Jayson Tatum'), (29, 'Jaren Jackson Jr.'), (44, 'Walker Kessler'), (53, 'Ivica Zubac'), (77, 'Luka Doncic'), (92, 'Deni Avdija'), (101, 'Cameron Boozer'), (125, 'John Collins'), (140, 'Wendell Carter Jr.')]

ARMS = {
    "as_drafted": [],
    "CF1_all_deviations_to_card": CARD,
    "CF2_brunson_to_kessler": [(44, "Walker Kessler")],          # board-9 reach, the card's big
    "CF3_keyonte_to_harris": [(140, "Tobias Harris")],           # board-13 reach, deepest
    "CF4_bam_to_zubac": [(53, "Ivica Zubac")],                   # board-4 vs card's big
    "CF5_ecw_greedy_oracle": GREEDY,                             # E9 probe (oracle, not a strategy)
    # interior repair: the roster's holes are REB 33% / BLK 28% win rates
    "CF7_kept_greedy_oracle": KEPTGREEDY,   # control: same freedom, kept-total objective
    "CF6_interior_repair": [(44, "Walker Kessler"), (101, "Nic Claxton")],
}

SEEDS = [11, 23]
N = 6000
want = sys.argv[1:] or list(ARMS)
SPD = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad"
for name in want:
    try:
        ros = build_seq(ARMS[name])
    except AssertionError as e:
        print(f"{name}: SKIPPED — {e}")
        json.dump({name: {"error": str(e)}}, open(f"{SPD}/mock28_cf_{name}.json", "w"), indent=1)
        continue
    tc = {i: 0 for i in ros}
    tp = {i: 0 for i in ros}
    for sd in SEEDS:
        c, p = arena.simulate_seasons(ros, N, random.Random(sd))
        for i in ros:
            tc[i] += c[i]
            tp[i] += p[i]
    T = N * len(SEEDS)
    champ = 100 * tc[OWNER] / T
    playoff = 100 * tp[OWNER] / T
    finish = sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1
    kept = sum(sum(pl["z"][c] for c in CATS) for pl in ros[OWNER])
    e = ecw(ros)
    res = {"champ": round(champ, 2), "playoff": round(playoff, 2), "finish": finish,
           "kept_total": round(kept, 2), "ecw": round(e, 3),
           "swaps": [[pn, alt] for pn, alt in ARMS[name]]}
    json.dump({name: res}, open(f"{SPD}/mock28_cf_{name}.json", "w"), indent=1)
    print(f"{name:<30} champ {champ:6.2f}%  playoff {playoff:6.2f}%  finish {finish:>2}  "
          f"kept {kept:+6.2f}  ECW {e:.3f}")
