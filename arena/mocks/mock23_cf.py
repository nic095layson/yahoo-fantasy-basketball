import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import sys, os, json, random

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/117b5573-draft_state_12.json"
OWNER = 12
state = json.load(open(STATE))
picks = state["picks"]
byname = {p["player"]: p for p in players}
order = {pk["player"]: i for i, pk in enumerate(picks)}

def build(swaps):
    """swaps: {ownerPlayer: altPlayer}. Pairwise: the team that drafted alt
    later receives the owner's player. Alt must be drafted AFTER the owner
    pick it replaces (i.e. was available on the card)."""
    newp = [dict(pk) for pk in picks]
    for mine, alt in swaps.items():
        i, j = order[mine], order[alt]
        assert newp[i]["slot"] == OWNER and j > i, (mine, alt, i, j)
        newp[i]["player"], newp[j]["player"] = alt, mine
    rosters = {}
    for pk in newp:
        rosters.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == 156 and all(len(r) == 13 for r in rosters.values())
    return rosters

ARMS = {
  "as_drafted": {},
  "CF1_deep_deviations_to_card": {        # the three board-10+ reaches -> the card's 🎯
      "Stephen Curry": "Evan Mobley",      # your #13 (board 10, -1.17)
      "Jalen Brunson": "Josh Giddey",      # your #37 (board 17, -1.46)
      "Dylan Harper": "Josh Hart",         # your #85 (board 64, -2.84)
  },
  "CF2_interior_repair_only": {            # keep every guard EXCEPT two interior swaps
      "Zach LaVine": "Jarrett Allen",      # your #60 (card had Allen quiet)
      "Kon Knueppel": "John Collins",      # your #109 (the TARGET's C plea)
  },
  "CF3_one_early_big": {                   # single earliest structural fix
      "Stephen Curry": "Evan Mobley",      # your #13 — the 🎯 at BOTH halves of the pair
  },
}

SEEDS = [11, 23]
N = 6000
out = {}
for arm, swaps in ARMS.items():
    rosters = build(swaps)
    tc = tp = 0
    for sd in SEEDS:
        c, p = arena.simulate_seasons(rosters, N, random.Random(sd))
        tc += c[OWNER]; tp += p[OWNER]
    T = N * len(SEEDS)
    champs = {}
    # full-room champ ordering for finish position
    totc = {i: 0 for i in rosters}
    for sd in SEEDS:
        c, _ = arena.simulate_seasons(rosters, N, random.Random(sd))
        for i in rosters: totc[i] += c[i]
    finish = sorted(totc, key=lambda x: -totc[x]).index(OWNER) + 1
    out[arm] = {"champ_pct": round(100*tc/T, 2), "playoff_pct": round(100*tp/T, 2), "finish": finish}
    print(f"{arm:<32} champ {out[arm]['champ_pct']:6.2f}%  playoff {out[arm]['playoff_pct']:6.2f}%  finish {finish}")

json.dump(out, open("/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad/mock23_cf_out.json", "w"), indent=1)
print("wrote mock23_cf_out.json")
