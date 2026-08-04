import sys, os, json, random

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/773c5fc1-draft_state_10.json"
OWNER = 4
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
  "CF1_quickley_to_suggs": {                 # the one deep deviation (#76, board 23)
      "Immanuel Quickley": "Jalen Suggs",
  },
  "CF2_shallow_misses_to_target": {          # the near-coin-flip price picks
      "Kevin Durant": "Jamal Murray",        # your #28 (board 3, -0.38)
      "Cooper Flagg": "Payton Pritchard",    # your #45 (board 2, -0.18)
  },
  "CF3_interior_removed": {                  # 5th test of the interior family
      "Walker Kessler": "Darius Garland",    # your #52 quiet-C -> on-card G
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

json.dump(out, open("/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad/mock21_cf_out.json", "w"), indent=1)
print("wrote mock21_cf_out.json")
