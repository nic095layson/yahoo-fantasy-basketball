#!/usr/bin/env python3
"""league_sim — the house season simulator (arena.simulate_seasons) with the season's full outcome recorded:
every team's category record, its playoff seed, its finishing round, the title. The random draws are the house
simulator's, in its order, so on the same seed the champion and playoff counts equal arena.simulate_seasons'
exactly; --verify asserts that before anything is written.

    python3 arena/mocks/league_sim.py <draft_state.json> <tag> <seasons> <seed> <out.json> [--verify]

Built for the league draft of 2026-10-14 (owner: "simulate 10000 seasons")."""
import json, math, os, random, sys
DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops  # noqa: E402
import arena  # noqa: E402

state_path, tag, SEASONS, SEED, out_path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
VERIFY = "--verify" in sys.argv
hoops.DATA_PATH = os.path.join(DECK, "arena", "results", f"players_{tag}.csv")
players = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in players}
st = json.load(open(state_path, encoding="utf-8"))
rosters = {s: [] for s in range(1, st["teams"] + 1)}
missing = []
for pk in st["picks"]:
    (rosters[pk["slot"]].append(by[pk["player"]]) if pk["player"] in by else missing.append(pk["player"]))
assert not missing, missing
CATS, TEAMS, WEEKS, PO = hoops.CATS, arena.TEAMS, arena.WEEKS, arena.PLAYOFF_TEAMS
assert TEAMS == len(rosters)


def simulate(rosters, seasons, rng):
    """arena.simulate_seasons, line for line, plus the record."""
    models = {i: arena.team_week_model(r) for i, r in rosters.items()}
    sigmas = {i: {c: math.sqrt(models[i][1][c]) or 1e-6 for c in CATS} for i in rosters}
    counting = set(hoops.COUNT_COLS)
    ids = list(rosters)
    R = {i: dict(champ=0, final=0, semi=0, playoff=0, seed=[0] * TEAMS, cat_wins=0.0, cat_wins_sq=0.0,
                 cat_by={c: 0 for c in CATS}, weeks_won=0) for i in ids}

    def week_result(a, b, rec=None):
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
            if rec is not None:
                R[a if better else b]["cat_by"][c] += 1
        return wins

    for _ in range(seasons):
        record = {i: 0 for i in ids}
        for _w in range(WEEKS):
            pairing = ids[:]
            rng.shuffle(pairing)
            for k in range(0, TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                wa = week_result(a, b, rec=True)
                record[a] += wa
                record[b] += 9 - wa
                if wa >= 5: R[a]["weeks_won"] += 1
                else: R[b]["weeks_won"] += 1
        seeds = sorted(ids, key=lambda i: (-record[i], rng.random()))
        for k, i in enumerate(seeds):
            R[i]["seed"][k] += 1; R[i]["cat_wins"] += record[i]; R[i]["cat_wins_sq"] += record[i] ** 2
        top = seeds[:PO]
        for i in top:
            R[i]["playoff"] += 1
        # arena.playoff_champion, expanded to record the rounds (same pairs, same draw order)
        qf = [(top[0], top[7]), (top[3], top[4]), (top[1], top[6]), (top[2], top[5])]
        w1 = [a if week_result(a, b) >= 5 else b for a, b in qf]
        for i in w1: R[i]["semi"] += 1
        sf = [(w1[0], w1[1]), (w1[2], w1[3])]
        w2 = [a if week_result(a, b) >= 5 else b for a, b in sf]
        for i in w2: R[i]["final"] += 1
        champ = w2[0] if week_result(*w2) >= 5 else w2[1]
        R[champ]["champ"] += 1
    return R, models


R, models = simulate(rosters, SEASONS, random.Random(SEED))
if VERIFY:
    c, p = arena.simulate_seasons(rosters, SEASONS, random.Random(SEED))
    assert all(c[i] == R[i]["champ"] and p[i] == R[i]["playoff"] for i in rosters), ({i: (c[i], R[i]["champ"], p[i], R[i]["playoff"]) for i in rosters})
    print(f"verify: champions and playoff counts equal arena.simulate_seasons on seed {SEED} for all {len(rosters)} teams")
out = dict(state=os.path.relpath(state_path, DECK), tag=tag, seasons=SEASONS, seed=SEED, weeks=WEEKS, playoff_teams=PO,
           verified_against_arena=VERIFY, teams={})
n_matchups = SEASONS * WEEKS
for i in rosters:
    r = R[i]; mean = r["cat_wins"] / SEASONS
    out["teams"][i] = dict(champ=100 * r["champ"] / SEASONS, final=100 * r["final"] / SEASONS, semi=100 * r["semi"] / SEASONS,
                           playoff=100 * r["playoff"] / SEASONS, seed_pct=[100 * x / SEASONS for x in r["seed"]],
                           mean_seed=sum((k + 1) * x for k, x in enumerate(r["seed"])) / SEASONS,
                           cat_record_mean=mean, cat_record_sd=math.sqrt(max(r["cat_wins_sq"] / SEASONS - mean ** 2, 0)),
                           cats_per_week=mean / WEEKS, week_win_pct=100 * r["weeks_won"] / n_matchups,
                           cat_win_pct={c: 100 * r["cat_by"][c] / n_matchups for c in CATS},
                           week_mu={c: models[i][0][c] for c in CATS})
json.dump(out, open(out_path, "w"), indent=1)
for i in sorted(rosters, key=lambda i: -out["teams"][i]["champ"]):
    t = out["teams"][i]
    print(f"seat {i:>2}: title {t['champ']:6.2f}%  final {t['final']:6.2f}%  playoffs {t['playoff']:6.2f}%  mean seed {t['mean_seed']:5.2f}  cats/wk {t['cats_per_week']:.3f}  #1 seed {t['seed_pct'][0]:5.2f}%")
