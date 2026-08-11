"""Mock 27 counterfactuals — parametrized: `python3 mock27_cf.py ARM_NAME [ARM_NAME...]`
with no args runs every arm. Pairwise legal swaps only (alt must be drafted AFTER
the owner pick it replaces). 6000 seasons x seeds [11,23]."""

import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import sys, os, json, random

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/5130afad-draft_state_16.json"
OWNER = 4
state = json.load(open(STATE))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER
picks = state["picks"]
byname = {p["player"]: p for p in players}
order = {pk["player"]: i for i, pk in enumerate(picks)}
CATS = hoops.CATS


def build(swaps):
    newp = [dict(pk) for pk in picks]
    for mine, alt in swaps.items():
        i, j = order[mine], order[alt]
        assert newp[i]["slot"] == OWNER, (mine, "not an owner pick")
        assert j > i, (mine, alt, "ILLEGAL: alt was already drafted at that turn")
        newp[i]["player"], newp[j]["player"] = alt, mine
    rosters = {}
    for pk in newp:
        rosters.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == 156 and all(len(r) == 13 for r in rosters.values())
    return rosters


ARMS = {
    "as_drafted": {},
    # The card's ST repair, offered and declined at #76 (Suggs went #78, two picks later)
    "CF1_bridges_to_suggs": {"Mikal Bridges": "Jalen Suggs"},
    # The deepest deviation in the whole ledger: board-44 reach at #141
    "CF2_mathurin_to_wcj": {"Bennedict Mathurin": "Wendell Carter Jr."},
    # Every off-card pick -> the card's system pick at that turn (9 swaps)
    "CF3_all_deviations_to_card": {
        "Jalen Brunson": "Kristaps Porzingis",
        "Joel Embiid": "Coby White",
        "Mikal Bridges": "Jalen Suggs",
        "Deni Avdija": "Norman Powell",
        "Zach Edey": "Nikola Vucevic",
        "DeMar DeRozan": "Jabari Smith Jr.",
        "Bennedict Mathurin": "Wendell Carter Jr.",
        "Al Horford": "De'Anthony Melton",
    },
    # Targeted repair of the one dead category (ST, rank 12, -6.00) using players
    # available at those turns; tests whether the flat-board roster was fixable
    "CF4_steals_repair": {
        "Mikal Bridges": "Jalen Suggs",        # #76, Suggs #78
        "DeMar DeRozan": "Toumani Camara",     # #117, Camara #113? -> check legality
    },
    # Isolate the mid-draft big reach (#69 Embiid, board 15)
    "CF5_embiid_to_white": {"Joel Embiid": "Coby White"},
    # Two-name ST repair using only legal, later-drafted defenders
    "CF6_steals_repair_legal": {
        "Mikal Bridges": "Jalen Suggs",        # #76 -> Suggs #78
        "CJ McCollum": "Keon Ellis",           # #124 -> Ellis #129
    },
}

SEEDS = [11, 23]
N = 6000
want = sys.argv[1:] or list(ARMS)
out = {}
for name in want:
    swaps = ARMS[name]
    try:
        rosters = build(swaps)
    except AssertionError as e:
        print(f"{name}: SKIPPED — {e}")
        out[name] = {"error": str(e)}
        continue
    tc = {i: 0 for i in rosters}
    tp = {i: 0 for i in rosters}
    for sd in SEEDS:
        c, p = arena.simulate_seasons(rosters, N, random.Random(sd))
        for i in rosters:
            tc[i] += c[i]
            tp[i] += p[i]
    T = N * len(SEEDS)
    champ = 100 * tc[OWNER] / T
    playoff = 100 * tp[OWNER] / T
    finish = sorted(rosters, key=lambda x: -tc[x]).index(OWNER) + 1
    zs = {c: sum(pl["z"][c] for pl in rosters[OWNER]) for c in CATS}
    ranks = {c: sorted(rosters, key=lambda i: -sum(pl["z"][c] for pl in rosters[i])).index(OWNER) + 1
             for c in CATS}
    out[name] = {"champ": round(champ, 2), "playoff": round(playoff, 2), "finish": finish,
                 "kept_total": round(sum(zs.values()), 2),
                 "cat_ranks": ranks, "swaps": swaps}
    print(f"{name:<32} champ {champ:6.2f}%  playoff {playoff:6.2f}%  finish {finish:>2}  "
          f"kept {sum(zs.values()):+6.2f}  ST rank {ranks['ST']}")

# per-arm output files: parallel runs must not race on a shared path
SPD = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad"
for name, res in out.items():
    json.dump({name: res}, open(f"{SPD}/mock27_cf_{name}.json", "w"), indent=1)
print("wrote per-arm mock27_cf_<arm>.json")
