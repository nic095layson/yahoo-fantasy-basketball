"""Daily-schedule Monte Carlo: how much weekly production does a REAL
daily-managed lineup capture vs arena's static team_week_model?

Assumptions (stated per task spec):
- Week = 7 days (Mon..Sun).
- Each NBA team's games/week G drawn: P(3)=0.55, P(4)=0.35, P(2)=0.08,
  P(5)=0.02  => E[G] = 3.31 (note: static model uses 3.5).
- Game days drawn without replacement, weighted Mon..Sun
  [1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4] (Mon/Wed/Fri/Sun heavy).
- All rostered players on the same NBA team share that team's schedule.
- Each scheduled game is played with prob arena.weekly_availability(p).
- Daily lineup: among players WITH a game who are playing, greedy-fill
  arena.LINEUP_SLOTS in hoops z-total order (arena.positions_of eligibility,
  specific slot before flex before Util). Started => full per-game counting
  stats that day.
- 2000 weeks, random.Random(20260805), fully deterministic.
"""
import json
import os
import random
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(REPO)
sys.path = [os.path.join(REPO, "scripts"), os.path.join(REPO, "arena")] + [
    p for p in sys.path if p not in (os.path.join(REPO, "scripts"),
                                     os.path.join(REPO, "arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
COUNT = hoops.COUNT_COLS  # cat -> per-game column
byname = {p["player"]: p for p in players}

G_DIST = [(3, 0.55), (4, 0.35), (2, 0.08), (5, 0.02)]
DAY_W = [1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4]  # Mon..Sun
N_WEEKS = 2000
SEED = 20260805
EG = sum(g * p for g, p in G_DIST)  # 3.31


def load_roster(mock, slot):
    state = json.load(open(f"arena/data/states/draft_state_mock{mock}.json"))
    assert state["slot"] == slot, (mock, state["slot"])
    ros = [byname[pk["player"]] for pk in state["picks"] if pk["slot"] == slot]
    assert len(ros) == 13
    return ros


def draw_games(rng):
    r, acc = rng.random(), 0.0
    for g, p in G_DIST:
        acc += p
        if r < acc:
            return g
    return G_DIST[-1][0]


def draw_days(rng, g):
    """g distinct days, weighted without replacement."""
    days, w = list(range(7)), list(DAY_W)
    chosen = []
    for _ in range(g):
        tot = sum(w)
        r = rng.random() * tot
        for i in range(len(days)):
            r -= w[i]
            if r <= 0:
                chosen.append(days.pop(i))
                w.pop(i)
                break
    return chosen


def greedy_start(cands):
    """Greedy LINEUP_SLOTS fill in z-total order; returns set of started ids."""
    ordered = sorted(cands, key=lambda p: -sum(p["z"][c] for c in CATS))
    open_slots = list(arena.LINEUP_SLOTS)
    started = set()
    for p in ordered:
        pos = arena.positions_of(p)
        claimed = None
        for i, s in enumerate(open_slots):
            if s is not None and any(b in s for b in pos):
                claimed = i
                break
        if claimed is None:
            for i, s in enumerate(open_slots):
                if s is None:
                    claimed = i
                    break
        if claimed is not None:
            open_slots.pop(claimed)
            started.add(id(p))
    return started


def run_mock(mock, slot):
    roster = load_roster(mock, slot)
    lw = arena.lineup_weights(roster)
    starters10 = [p for p in roster if lw[id(p)] == 1.0]
    bench3 = [p for p in roster if lw[id(p)] < 1.0]
    assert len(starters10) == 10 and len(bench3) == 3

    avail = {id(p): arena.weekly_availability(p) for p in roster}
    teams = {}
    for p in roster:
        teams.setdefault(p["team"], []).append(p)

    rng = random.Random(SEED + int(mock))
    played = {id(p): 0 for p in roster}
    started_ct = {id(p): 0 for p in roster}
    tot = {c: 0.0 for c in COUNT}

    for _ in range(N_WEEKS):
        day_players = {d: [] for d in range(7)}
        for tm, ps in teams.items():
            g = draw_games(rng)
            days = draw_days(rng, g)
            for p in ps:
                a = avail[id(p)]
                for d in days:
                    if rng.random() < a:
                        day_players[d].append(p)
        for d in range(7):
            cands = day_players[d]
            for p in cands:
                played[id(p)] += 1
            st = greedy_start(cands)
            for p in cands:
                if id(p) in st:
                    started_ct[id(p)] += 1
                    for c, col in COUNT.items():
                        tot[c] += p[col]

    def frac(group):
        pl = sum(played[id(p)] for p in group)
        st = sum(started_ct[id(p)] for p in group)
        return st / pl, pl, st

    f_all = frac(roster)
    f_top = frac(starters10)
    f_bench = frac(bench3)

    mc_week = {c: tot[c] / N_WEEKS for c in COUNT}
    mu, _ = arena.team_week_model(roster)
    static_week = {c: mu[c] for c in COUNT}
    # schedule-matched static: rescale the static 3.5 games baseline to
    # this week model's E[G]=3.31 so the lineup effect is isolated
    static_adj = {c: mu[c] * EG / 3.5 for c in COUNT}

    per_player = []
    for p in sorted(roster, key=lambda q: -sum(q["z"][c] for c in CATS)):
        per_player.append(dict(
            player=p["player"], pos=p["pos"], team=p["team"],
            tier="top10" if lw[id(p)] == 1.0 else "bench",
            avail=avail[id(p)],
            played_pw=played[id(p)] / N_WEEKS,
            start_frac=started_ct[id(p)] / max(played[id(p)], 1)))

    return dict(
        mock=mock, slot=slot,
        n_C_eligible=sum(1 for p in roster if "C" in arena.positions_of(p)),
        frac_all=f_all[0], frac_top10=f_top[0], frac_bench=f_bench[0],
        played_pw_all=f_all[1] / N_WEEKS, started_pw_all=f_all[2] / N_WEEKS,
        mc_week=mc_week, static_week=static_week, static_adj=static_adj,
        gap_raw={c: 100 * (mc_week[c] / static_week[c] - 1) for c in COUNT},
        gap_schedule_matched={c: 100 * (mc_week[c] / static_adj[c] - 1)
                              for c in COUNT},
        per_player=per_player)


if __name__ == "__main__":
    out = {m: run_mock(m, s) for m, s in (("39", 4), ("34", 8))}
    out["_assumptions"] = dict(
        weeks=N_WEEKS, seed=SEED, G_dist=G_DIST, E_G=EG,
        day_weights=DAY_W, static_bench_weight=arena.BENCH_WEIGHT,
        static_games_baseline=3.5)
    print(json.dumps(out, indent=1))
