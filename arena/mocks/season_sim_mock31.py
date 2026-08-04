"""Mock 31 season simulation — owner slot 8, declared punt ["FT%","3PTM","PTS"].

Same harness as season_sim_mock30.py (LIVE pool via hoops, seasons via
arena.simulate_seasons), plus two readouts mock30 did not carry:

  * ECW  — expected categories won per week. Identical formula to the one
           already used in mock28_cf.py: for each of the 9 cats, the normal
           win probability of the owner's weekly (mu, var) vs each of the 11
           opponents' (arena.team_week_model), averaged over opponents, summed
           over cats. TO is inverted (lower is better).
  * place — mean regular-season standings place (1-12). arena.simulate_seasons
           returns only champs/playoffs, so the season loop below is a
           duplicate of arena.simulate_seasons's mechanics (same models, same
           TEAM_WEEK_SHOCK, same 9-cat record accumulation, same WEEKS) with
           standings position recorded. It is a SEPARATE measurement on its own
           seeds; it does not replace the arena's own champ/playoff numbers.

Per-category league rank is reported two ways: the ledger-convention z-sum
rank (what every prior mock reported) and the weekly-model per-category win
probability rank, which is the quantity ECW is built from.

Run: python3 arena/mocks/season_sim_mock31.py
"""
import sys, os, json, random, math

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())  # LIVE pool (deck's data source), BEFORE arena import
live_data_path = hoops.DATA_PATH

import arena  # noqa: E402  (loads its own hoops instance on the frozen snapshot; ours stays live)

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/6ae5fe0f-draft_state_20.json"
OWNER = 8
state = json.load(open(STATE))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER, state
PUNT = list(state.get("punt") or [])
assert PUNT == ["FT%", "3PTM", "PTS"], PUNT
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

# Persona map: deck mockCastFor() — MOCK_CAST assigned in slot order, skipping owner slot
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

CATS = hoops.CATS
KEPT = [c for c in CATS if c not in PUNT]

SEEDS = [11, 23, 47]      # standard seed set (season_sim_mock30.py)
N = 6000                  # 3 seeds x 6000 = 18000 seasons
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
print(f"declared punt: {PUNT}   kept: {KEPT}")
print(f"seasons/seed: {N}  seeds: {SEEDS}  total: {TOTAL}")

# ---------------------------------------------------------------- weekly model
models = {i: arena.team_week_model(r) for i, r in rosters.items()}


def pwin(who, opp, c):
    ma, va = models[who][0][c], models[who][1][c]
    mb, vb = models[opp][0][c], models[opp][1][c]
    d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
    p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
    return (1 - p) if c == "TO" else p


def cat_pwins(who):
    """Per-category mean win prob vs the other 11 teams."""
    others = [o for o in rosters if o != who]
    return {c: sum(pwin(who, o, c) for o in others) / len(others) for c in CATS}


pw = {i: cat_pwins(i) for i in rosters}
ecw = {i: sum(pw[i].values()) for i in rosters}   # expected categories won per week (0-9)

# ------------------------------------------------- mean regular-season place
# Duplicate of arena.simulate_seasons's season mechanics with standings place
# recorded. Own seeds, own RNG stream; reported separately from champ/playoff.
sigmas = {i: {c: math.sqrt(models[i][1][c]) or 1e-6 for c in CATS} for i in rosters}
counting = set(hoops.COUNT_COLS)
ids = list(rosters)


def week_result(a, b, rng):
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


place_sum = {i: 0 for i in ids}
place_hist = {i: [0] * 12 for i in ids}
for sd in SEEDS:
    rng = random.Random(sd)
    for _ in range(N):
        record = {i: 0 for i in ids}
        for _w in range(arena.WEEKS):
            pairing = ids[:]
            rng.shuffle(pairing)
            for k in range(0, arena.TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                wa = week_result(a, b, rng)
                record[a] += wa
                record[b] += 9 - wa
        standings = sorted(ids, key=lambda i: (-record[i], rng.random()))
        for pos, i in enumerate(standings, 1):
            place_sum[i] += pos
            place_hist[i][pos - 1] += 1
mean_place = {i: place_sum[i] / TOTAL for i in ids}

# --------------------------------------------------------------- z-sum board
zsum = {i: {c: sum(pl["z"][c] for pl in rosters[i]) for c in CATS} for i in rosters}
ztot = {i: sum(zsum[i].values()) for i in rosters}  # all-9-cat kept-total (TO inverted in hoops.zscores)

print("\nslot  persona             champ%  playoff%   ECW    meanPlace  9cat-z-total")
order = sorted(rosters, key=lambda x: -tot_c[x])
for i in order:
    print(f"{i:>4}  {persona[i]:<18} {100*tot_c[i]/TOTAL:6.2f}   {100*tot_p[i]/TOTAL:6.2f}  "
          f"{ecw[i]:6.3f}   {mean_place[i]:6.2f}     {ztot[i]:+7.2f}")

finish = order.index(OWNER) + 1                                            # ledger "Finish" column
board_rank = sorted(rosters, key=lambda x: -ztot[x]).index(OWNER) + 1
ecw_rank = sorted(rosters, key=lambda x: -ecw[x]).index(OWNER) + 1
place_rank = sorted(rosters, key=lambda x: mean_place[x]).index(OWNER) + 1

print(f"\nowner slot {OWNER}")
print(f"  champ%            {100*tot_c[OWNER]/TOTAL:.2f}")
print(f"  playoff%          {100*tot_p[OWNER]/TOTAL:.2f}")
print(f"  Finish (champ-order rank, ledger convention): {finish} of 12")
print(f"  mean reg-season standings place: {mean_place[OWNER]:.2f}  (rank {place_rank} of 12)")
print(f"  ECW               {ecw[OWNER]:.3f}   (rank {ecw_rank} of 12)")
print(f"  board rank (kept-total): {board_rank}")
print("  per-seed champ%:  ", {sd: round(100*per_seed[sd][0][OWNER]/N, 2) for sd in SEEDS})
print("  per-seed playoff%:", {sd: round(100*per_seed[sd][1][OWNER]/N, 2) for sd in SEEDS})

print("\nowner per-category league rank (1=best of 12); TO inverted so higher=better:")
print("  cat    role     z-sum   z-rank   pwin    pwin-rank")
zrank, prank = {}, {}
for c in CATS:
    zrank[c] = sorted(rosters, key=lambda i: -zsum[i][c]).index(OWNER) + 1
    prank[c] = sorted(rosters, key=lambda i: -pw[i][c]).index(OWNER) + 1
    role = "PUNT" if c in PUNT else "kept"
    print(f"  {c:>5}  {role:<6} {zsum[OWNER][c]:+7.2f}   {zrank[c]:>2}     {pw[OWNER][c]:.3f}    {prank[c]:>2}")

print("\nkept-cat pwin-rank mean:  %.2f" % (sum(prank[c] for c in KEPT) / len(KEPT)))
print("punt-cat pwin-rank mean:  %.2f" % (sum(prank[c] for c in PUNT) / len(PUNT)))
print("ECW contributed by kept cats: %.3f / punt cats: %.3f"
      % (sum(pw[OWNER][c] for c in KEPT), sum(pw[OWNER][c] for c in PUNT)))

OUT = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad/season_sim_mock31_out.json"
out = {
    "state": STATE, "owner_slot": OWNER, "punt": PUNT,
    "seeds": SEEDS, "seasons_per_seed": N, "total_seasons": TOTAL,
    "live_data_path": live_data_path,
    "table": [{"slot": i, "persona": persona[i],
               "champ_pct": round(100*tot_c[i]/TOTAL, 2),
               "playoff_pct": round(100*tot_p[i]/TOTAL, 2),
               "ecw": round(ecw[i], 3),
               "mean_place": round(mean_place[i], 2),
               "kept_total": round(ztot[i], 2)} for i in sorted(rosters)],
    "owner": {
        "champ_pct": round(100*tot_c[OWNER]/TOTAL, 2),
        "playoff_pct": round(100*tot_p[OWNER]/TOTAL, 2),
        "finish_champ_order": finish,
        "mean_place": round(mean_place[OWNER], 2),
        "mean_place_rank": place_rank,
        "ecw": round(ecw[OWNER], 3),
        "ecw_rank": ecw_rank,
        "board_rank": board_rank,
        "per_seed_champ_pct": {sd: round(100*per_seed[sd][0][OWNER]/N, 2) for sd in SEEDS},
        "per_seed_playoff_pct": {sd: round(100*per_seed[sd][1][OWNER]/N, 2) for sd in SEEDS},
        "cat_z": {c: round(zsum[OWNER][c], 2) for c in CATS},
        "cat_z_rank": zrank,
        "cat_pwin": {c: round(pw[OWNER][c], 3) for c in CATS},
        "cat_pwin_rank": prank,
        "place_hist": place_hist[OWNER],
    },
}
json.dump(out, open(OUT, "w"), indent=1)
print("\nwrote", OUT)
