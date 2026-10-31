#!/usr/bin/env python3
"""league_sim — the house season simulator (arena.simulate_seasons) with the season's full outcome recorded:
every team's category record, its playoff seed, its finishing round, the title. The random draws are the house
simulator's, in its order, so on the same seed the champion and playoff counts equal arena.simulate_seasons'
exactly; --verify asserts that before anything is written.

    python3 arena/mocks/league_sim.py <draft_state.json> <tag> <seasons> <seed> <out.json> [--verify]
                                      [--schedule <kit data/league_schedule.json>] [--season-cv] [--pool <players.csv>]
                                      [--patch <patch.json>]
A pick with "from_week" / "to_week" counts only in that window of regular-season weeks (kit owner 2026-10-31, the
IL-return scenarios); the record carries "windows".

--schedule fixes the owner's seat against the listed opponent in every regular-season week
(the league's real schedule, owner message 2026-10-15) and pairs the other ten teams at random
each week; it changes the draw order, so it cannot be combined with --verify.
  With "pairings" in the file ({week: [[seatA, seatB] x 6]}, the kit's league_pairings.py from Yahoo's
  published schedule; kit owner 2026-10-26) every team's pairing comes from the file every week.
  With "played" ({week: {seat: [wins, losses, ties]}}, the kit's data/weeks records) those weeks are
  not simulated: each season starts from the recorded category record (a tie counts half a win,
  Yahoo's standings rule) and only the remaining weeks and the playoffs are drawn. A played week
  that does not cover every seat is an error before anything is written.

--season-cv runs the weekly model on arena.SEASON_CV, the per-game variation fitted to the 2025-26 game logs
(D-ZS-3, owner 2026-10-21: the season tools only); without it the draft engine's arena.CV, as before. --verify
compares against arena.simulate_seasons on the same CV, and the record says "cv": "season".

--pool loads the player lines from the named deck-schema CSV instead of arena/results/players_<tag>.csv (kit owner
2026-10-26, "use the season pool": the kit's data/season/pool_season.csv, the season-blended lines its board already
plays, with the in-season pickups in data/pool_additions.csv); the record names the file, its sha256 and its player
count. Without it the frozen tag file, as before, and the record has no "pool" key.

Built for the league draft of 2026-10-14 (owner: "simulate 10000 seasons")."""
import hashlib, json, math, os, random, sys
DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops  # noqa: E402
import arena  # noqa: E402
import patches  # noqa: E402

state_path, tag, SEASONS, SEED, out_path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
VERIFY = "--verify" in sys.argv
# kit owner 2026-10-26: one hand-set constant moved (arena/patches.py, the sweep's own patch), applied before anything
# reads SEASON_CV or builds a team model; --verify then checks against arena.simulate_seasons patched the same way
PATCH = json.load(open(sys.argv[sys.argv.index("--patch") + 1], encoding="utf-8")) if "--patch" in sys.argv else None
if PATCH:
    patches.apply(arena, PATCH)
CV = arena.SEASON_CV if "--season-cv" in sys.argv else None
SCHEDULE = None
if "--schedule" in sys.argv:
    sched_path = sys.argv[sys.argv.index("--schedule") + 1]
    SCHEDULE = json.load(open(sched_path, encoding="utf-8"))
    assert not VERIFY, "--schedule changes the draw order; run --verify without it"
POOL = sys.argv[sys.argv.index("--pool") + 1] if "--pool" in sys.argv else None
hoops.DATA_PATH = POOL or os.path.join(DECK, "arena", "results", f"players_{tag}.csv")
players = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in players}
st = json.load(open(state_path, encoding="utf-8"))
rosters = {s: [] for s in range(1, st["teams"] + 1)}
missing = []
for pk in st["picks"]:
    (rosters[pk["slot"]].append(by[pk["player"]]) if pk["player"] in by else missing.append(pk["player"]))
assert not missing, missing
CATS, TEAMS, WEEKS, PO = hoops.CATS, arena.TEAMS, arena.WEEKS, arena.PLAYOFF_TEAMS
# kit owner 2026-10-31 ("take ESPN injury return as a variable title odds in a separate section"): a pick may carry
# "from_week" and/or "to_week", the first and last regular-season week the player counts for his team; outside that
# window he is absent, as an IL player is under the kit's D-IS-8. A team's weekly model is rebuilt only where its
# active roster changes; the playoffs play the final week's roster. Without any window the draws are the same as
# before, in the same order. --verify cannot follow a window (arena.simulate_seasons has no weeks).
WINDOWS = {}
for pk in st["picks"]:
    if "from_week" in pk or "to_week" in pk:
        lo, hi = int(pk.get("from_week", 1)), int(pk.get("to_week", WEEKS))
        assert 1 <= lo and hi <= WEEKS + 1 and lo <= hi + 1, (pk["player"], lo, hi)
        WINDOWS[(pk["slot"], pk["player"])] = (lo, hi)
assert not (WINDOWS and VERIFY), "from_week/to_week change the weekly rosters; run --verify without them"
assert TEAMS == len(rosters)
PAIRINGS, PLAYED = {}, {}
if SCHEDULE:
    assert SCHEDULE["regular_season_weeks"] == WEEKS, (SCHEDULE["regular_season_weeks"], WEEKS)
    OWNER = SCHEDULE["owner_seat"]
    OPP = [o["seat"] for o in sorted(SCHEDULE["owner_opponents"], key=lambda o: o["week"])]
    PAIRINGS = {int(w): [(int(a), int(b)) for a, b in pairs] for w, pairs in (SCHEDULE.get("pairings") or {}).items()}
    for w, pairs in PAIRINGS.items():
        seen = sorted(s for pr in pairs for s in pr)
        assert seen == list(range(1, TEAMS + 1)), f"pairings week {w}: seats {seen} do not cover every team once"
    if PAIRINGS:
        assert sorted(PAIRINGS) == list(range(1, WEEKS + 1)), f"pairings cover weeks {sorted(PAIRINGS)}, not 1..{WEEKS}"
    PLAYED = {int(w): {int(s): tuple(int(x) for x in rec) for s, rec in recs.items()} for w, recs in (SCHEDULE.get("played") or {}).items()}
    for w, recs in PLAYED.items():
        assert sorted(recs) == list(range(1, TEAMS + 1)), f"played week {w}: records for seats {sorted(recs)}, not every team"
        assert 1 <= w <= WEEKS, f"played week {w} is outside 1..{WEEKS}"
HONORED = [0]


def simulate(rosters, seasons, rng):
    """arena.simulate_seasons, line for line, plus the record."""
    ids = list(rosters)
    if WINDOWS:
        def active(i, w):
            return [p for p in rosters[i] if WINDOWS.get((i, p["player"]), (1, WEEKS))[0] <= w <= WINDOWS.get((i, p["player"]), (1, WEEKS))[1]]
        cache, weekly = {}, {}
        for i in ids:
            weekly[i] = []
            for w in range(1, WEEKS + 1):
                key = (i, tuple(p["player"] for p in active(i, w)))
                if key not in cache:
                    cache[key] = arena.team_week_model(active(i, w), CV)
                weekly[i].append(cache[key])
        models = {i: weekly[i][-1] for i in ids}
    else:
        models = {i: arena.team_week_model(r, CV) for i, r in rosters.items()}
        weekly = {i: [models[i]] * WEEKS for i in ids}
    sig_of = {}

    def sigmas_for(m):
        if id(m) not in sig_of:
            sig_of[id(m)] = {c: math.sqrt(m[1][c]) or 1e-6 for c in CATS}
        return sig_of[id(m)]
    counting = set(hoops.COUNT_COLS)
    R = {i: dict(champ=0, final=0, semi=0, playoff=0, seed=[0] * TEAMS, cat_wins=0.0, cat_wins_sq=0.0,
                 cat_by={c: 0 for c in CATS}, weeks_won=0) for i in ids}

    def week_result(a, b, rec=None, week=None):
        m_a = weekly[a][week - 1] if week else models[a]
        m_b = weekly[b][week - 1] if week else models[b]
        s_a, s_b = sigmas_for(m_a), sigmas_for(m_b)
        sh_a = rng.gauss(1.0, arena.TEAM_WEEK_SHOCK)
        sh_b = rng.gauss(1.0, arena.TEAM_WEEK_SHOCK)
        wins = 0
        for c in CATS:
            ma = m_a[0][c] * (sh_a if c in counting else 1.0)
            mb = m_b[0][c] * (sh_b if c in counting else 1.0)
            sa = rng.gauss(ma, s_a[c])
            sb = rng.gauss(mb, s_b[c])
            better = sa < sb if c == "TO" else sa > sb
            wins += 1 if better else 0
            if rec is not None:
                R[a if better else b]["cat_by"][c] += 1
        return wins

    for _ in range(seasons):
        record = {i: 0 for i in ids}
        for _w in range(WEEKS):
            if (_w + 1) in PLAYED:
                # the week is final: the recorded category record, no draw (a tie is half a win, Yahoo's standings rule);
                # cat_by stays simulated-only, the record's per-category rates say so
                for i, (w_, l_, t_) in PLAYED[_w + 1].items():
                    record[i] += w_ + 0.5 * t_
                    if w_ >= 5: R[i]["weeks_won"] += 1
                continue
            if PAIRINGS:
                pairing = [s for pr in PAIRINGS[_w + 1] for s in pr]
                HONORED[0] += 1
            elif SCHEDULE:
                rest = [i for i in ids if i not in (OWNER, OPP[_w])]
                rng.shuffle(rest)
                pairing = [OWNER, OPP[_w]] + rest
                HONORED[0] += 1
            else:
                pairing = ids[:]
                rng.shuffle(pairing)
            for k in range(0, TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                wa = week_result(a, b, rec=True, week=_w + 1)
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
        sf = arena.reseed(w1, top)
        w2 = [a if week_result(a, b) >= 5 else b for a, b in sf]
        for i in w2: R[i]["final"] += 1
        champ = w2[0] if week_result(*w2) >= 5 else w2[1]
        R[champ]["champ"] += 1
    return R, models


R, models = simulate(rosters, SEASONS, random.Random(SEED))
if VERIFY:
    c, p = arena.simulate_seasons(rosters, SEASONS, random.Random(SEED), cv=CV)
    assert all(c[i] == R[i]["champ"] and p[i] == R[i]["playoff"] for i in rosters), ({i: (c[i], R[i]["champ"], p[i], R[i]["playoff"]) for i in rosters})
    print(f"verify: champions and playoff counts equal arena.simulate_seasons on seed {SEED} for all {len(rosters)} teams")
out = dict(state=os.path.relpath(state_path, DECK), tag=tag, seasons=SEASONS, seed=SEED, weeks=WEEKS, playoff_teams=PO,
           verified_against_arena=VERIFY, teams={})
if CV is not None:
    out["cv"] = "season"
if PATCH:
    out["patch"] = PATCH
if POOL:
    out["pool"] = dict(file=POOL, sha256=hashlib.sha256(open(POOL, "rb").read()).hexdigest(), players=len(players))
if WINDOWS:
    out["windows"] = {str(i): {p: list(w) for (s_, p), w in sorted(WINDOWS.items()) if s_ == i} for i in sorted({s_ for s_, _ in WINDOWS})}
    out["windows_rule"] = "from_week..to_week inclusive, regular season; absent outside; playoffs on the final week's roster"
if SCHEDULE:
    out["schedule"] = dict(file=os.path.relpath(sched_path, DECK), owner_seat=OWNER, opponents=OPP, honored=HONORED[0],
                           weeks_played=len(PLAYED), played_weeks=sorted(PLAYED))
    if PAIRINGS:
        out["schedule"]["pairings"] = f"every team's pairing from the file, all {WEEKS} weeks"
    else:
        out["schedule"]["others"] = "the other ten teams paired at random each week"
    if PLAYED:
        out["schedule"]["played_rule"] = "recorded category record, a tie half a win; cat_win_pct covers simulated weeks only"
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
