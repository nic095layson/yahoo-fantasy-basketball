import sys, os, json, random

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())  # LIVE pool (deck's data source), BEFORE arena import
live_data_path = hoops.DATA_PATH

import arena  # noqa: E402  (loads its own hoops instance on the frozen snapshot; ours stays live)

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/fdc581ea-draft_state_5.json"
OWNER = 3
state = json.load(open(STATE))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER, state
picks = state["picks"]
assert len(picks) == 156, len(picks)

byname = {p["player"]: p for p in players}
missing = [pk["player"] for pk in picks if pk["player"] not in byname]
assert not missing, missing

rosters = {}
for pk in picks:
    rosters.setdefault(pk["slot"], []).append(byname[pk["player"]])
assert sorted(rosters) == list(range(1, 13))
for s in sorted(rosters):
    assert len(rosters[s]) == 13, (s, len(rosters[s]))
allnames = [pk["player"] for pk in picks]
assert len(set(allnames)) == len(allnames), "duplicate picks!"

# Persona map: deck mockCastFor() — MOCK_CAST assigned in slot order, skipping owner owner slot
MOCK_CAST = ["market", "points_chaser", "market", "punt_ft", "stars",
             "slot_filler", "scarcity", "safe_floor", "upside", "bpa_pure", "punt_ft_to"]
persona = {}
i = 0
for s in range(1, 13):
    if s == state["slot"]:
        persona[s] = "OWNER (deck user)"
        continue
    persona[s] = MOCK_CAST[i % len(MOCK_CAST)]
    i += 1

SEEDS = [11, 23, 47]
N = 6000
tot_c = {i: 0 for i in rosters}
tot_p = {i: 0 for i in rosters}
per_seed = {}
for sd in SEEDS:
    c, p = arena.simulate_seasons(rosters, N, random.Random(sd))
    per_seed[sd] = (dict(c), dict(p))
    for i in rosters:
        tot_c[i] += c[i]
        tot_p[i] += p[i]

TOTAL = N * len(SEEDS)
print(f"live data path: {live_data_path}")
print(f"seasons/seed: {N}  seeds: {SEEDS}  total: {TOTAL}")

CATS = hoops.CATS
zsum = {i: {c: sum(pl["z"][c] for pl in rosters[i]) for c in CATS} for i in rosters}
ztot = {i: sum(zsum[i].values()) for i in rosters}  # all-9-cat kept-total (TO inverted in hoops.zscores)

print("\nslot  persona            champ%   playoff%   9cat-z-total")
order = sorted(rosters, key=lambda x: -tot_c[x])
for i in order:
    print(f"{i:>4}  {persona[i]:<18} {100*tot_c[i]/TOTAL:6.2f}   {100*tot_p[i]/TOTAL:6.2f}     {ztot[i]:+7.2f}")

print("\nkept-total rank of owner slot:", sorted(rosters, key=lambda x: -ztot[x]).index(OWNER) + 1)
print("champ rank of owner slot:", order.index(OWNER) + 1, "of 12")
print("per-seed owner champ%:", {sd: round(100*per_seed[sd][0][OWNER]/N, 2) for sd in SEEDS})
print("per-seed owner playoff%:", {sd: round(100*per_seed[sd][1][OWNER]/N, 2) for sd in SEEDS})

print("\nowner slot per-category z-sum + rank (1=best; TO inverted so higher=better everywhere):")
ranks4 = {}
for c in CATS:
    ranked = sorted(rosters, key=lambda i: -zsum[i][c])
    ranks4[c] = ranked.index(OWNER) + 1
    print(f"  {c:>5}: rank {ranks4[c]:>2}   z-sum {zsum[OWNER][c]:+7.2f}")

by_rank = sorted(CATS, key=lambda c: (ranks4[c], -zsum[OWNER][c]))
print("\n3 strongest:", [(c, ranks4[c], round(zsum[OWNER][c], 2)) for c in by_rank[:3]])
print("3 weakest:  ", [(c, ranks4[c], round(zsum[OWNER][c], 2)) for c in by_rank[-3:]])

out = {
    "seeds": SEEDS, "seasons_per_seed": N,
    "table": [{"slot": i, "persona": persona[i],
               "champ_pct": round(100*tot_c[i]/TOTAL, 2),
               "playoff_pct": round(100*tot_p[i]/TOTAL, 2),
               "kept_total": round(ztot[i], 2)} for i in sorted(rosters)],
    "owner_cat_ranks": ranks4,
    "owner_cat_z": {c: round(zsum[OWNER][c], 2) for c in CATS},
}
json.dump(out, open("/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad/season_sim_mock16_out.json", "w"), indent=1)
print("\nwrote season_sim_mock16_out.json")
