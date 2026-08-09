#!/usr/bin/env python3
"""Does the corrected bench weight change who wins? (audit item A1)

    python3 arena/mocks/bench_weight_study.py            # full, ~9 min
    python3 arena/mocks/bench_weight_study.py --quick    # ~3 min, N=1500
                                                         # (phase 1 always
                                                         # runs at committed N)

Output goes to arena/results/bench_weight_study[_quick][_seedsX-Y-Z]_out.json.
A --quick run is tagged so it can NEVER overwrite the committed full-N
evidence artifact (R4-F24: a round-4 auditor clobbered the committed E24
evidence by following this docstring's own regenerate instruction), and any
run refuses to overwrite an existing output whose config differs.

WHAT THIS MEASURES. Every mock in the ledger was graded with
`arena.BENCH_WEIGHT = 0.15` — the assumption that a roster's 11th-13th players
contribute 15% of their production. Measured against a daily-lineup fill, the
true slot-competition weight is 0.956 (`arena/mocks/bench_share_fit.py`). This
script re-grades the four mocks whose draft states are committed (31-34) under
both weights at identical seeds, and reports what moves.

WHAT THIS DOES NOT MEASURE. The rosters are held FIXED — this re-grades the
drafts that happened, it does not re-draft them under a corrected model. So it
answers "does the corrected weekly model change who wins with these rosters",
not "would a corrected engine have drafted better". The second question needs
the ordering rebuilt on the new weight and a full replay; that is September
work, gated behind the E14 re-baseline.

PHASE 1 additionally re-derives each mock's COMMITTED champ%/playoff% from its
committed state at its committed seeds, which is the lesson-13 integrity check:
a number nobody can regenerate is not evidence.
"""
import argparse
import json
import math
import os
import random
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(REPO)
sys.path = [os.path.join(REPO, "scripts"), os.path.join(REPO, "arena")] + [
    p for p in sys.path
    if p not in (os.path.join(REPO, "scripts"), os.path.join(REPO, "arena"))]

import hoops  # noqa: E402
import arena  # noqa: E402

MOCKS = [31, 32, 33, 34]
SEEDS = [11, 23, 47]
SHIPPED, MEASURED = 0.15, 0.956   # bench_share_fit.py, 144 rosters x 18 weeks
CATS = hoops.CATS


def pwins_total(my, opps):
    tot = 0.0
    for om in opps:
        for c in CATS:
            d = ((my[0][c] - om[0][c])
                 / (math.sqrt(my[1][c] + om[1][c]) or 1e-9))
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            tot += (1 - p) if c == "TO" else p
    return tot / (len(opps) or 1)


def load(mock, byname):
    st = json.load(open(f"arena/data/states/draft_state_mock{mock}.json"))
    rosters = {}
    for pk in st["picks"]:
        rosters.setdefault(pk["slot"], []).append(byname[pk["player"]])
    assert sorted(rosters) == list(range(1, 13))
    for s in rosters:
        assert len(rosters[s]) == 13, (mock, s, len(rosters[s]))
    return st, rosters


def grade(rosters, bw, n, seeds):
    """champ%/playoff% per slot plus ECW, at one bench weight."""
    arena.BENCH_WEIGHT = bw
    tc = {i: 0 for i in rosters}
    tp = {i: 0 for i in rosters}
    for sd in seeds:
        c, p = arena.simulate_seasons(rosters, n, random.Random(sd))
        for i in rosters:
            tc[i] += c[i]
            tp[i] += p[i]
    total = n * len(seeds)
    models = {i: arena.team_week_model(rosters[i]) for i in rosters}
    ecw = {i: pwins_total(models[i], [models[j] for j in rosters if j != i])
           for i in rosters}
    return ({i: 100 * tc[i] / total for i in rosters},
            {i: 100 * tp[i] / total for i in rosters}, ecw)


def rank_of(d, slot):
    return sorted(d, key=lambda s: -d[s]).index(slot) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seeds", help="comma-separated replication seeds "
                                    "(lesson 4: positives replicate on unseen seeds)")
    args = ap.parse_args()
    n = 1500 if args.quick else 6000
    seeds = ([int(x) for x in args.seeds.split(",")] if args.seeds else SEEDS)
    tag = ("_quick" if args.quick else "")
    if args.seeds:
        tag += "_seeds" + args.seeds.replace(",", "-")
    # Overwrite guard (R4-F24) — checked BEFORE any simulation so a refusal
    # costs seconds, not minutes.
    dest = f"arena/results/bench_weight_study{tag}_out.json"
    if os.path.exists(dest):
        try:
            existing = json.load(open(dest))
        except ValueError:
            existing = {}
        if (existing.get("seasons_per_seed") != n
                or existing.get("seeds") != seeds):
            sys.exit(f"refusing to overwrite {dest}: it holds a run at "
                     f"seasons_per_seed={existing.get('seasons_per_seed')} "
                     f"seeds={existing.get('seeds')}, this invocation is "
                     f"n={n} seeds={seeds}. Delete the file deliberately if "
                     "you mean to replace it.")

    players = hoops.zscores(hoops.load_players())
    byname = {p["player"]: p for p in players}

    print("=" * 78)
    print("PHASE 1 — lesson-13 integrity: do the committed numbers regenerate?")
    print("=" * 78)
    print(f"{'mock':<6}{'committed':>11}{'regenerated':>13}{'delta':>9}   verdict")
    repro = []
    for m in MOCKS:
        st, rosters = load(m, byname)
        owner = st["slot"]
        committed = json.load(open(f"arena/results/season_sim_mock{m}_out.json"))
        row = next(r for r in committed["table"] if r["slot"] == owner)
        want = row["champ_pct"]
        champ, _, _ = grade(rosters, SHIPPED, committed["seasons_per_seed"],
                            committed["seeds"])
        got = champ[owner]
        d = got - want
        ok = abs(d) < 0.005
        repro.append(ok)
        print(f"{m:<6}{want:>11.2f}{got:>13.2f}{d:>+9.3f}   "
              + ("EXACT" if ok else "*** MISMATCH ***"))
    print(f"\n{sum(repro)}/{len(repro)} committed results regenerate from a "
          "fresh clone + one command.\n")

    print("=" * 78)
    print(f"PHASE 2 — bench weight {SHIPPED} (shipped) vs {MEASURED} (measured)")
    print(f"          {n} seasons x {len(SEEDS)} seeds = {n*len(SEEDS)} per arm, "
          "rosters held fixed")
    print("=" * 78)
    out = {"shipped_bw": SHIPPED, "measured_bw": MEASURED,
           "seasons_per_seed": n, "seeds": seeds, "mocks": {}}
    for m in MOCKS:
        st, rosters = load(m, byname)
        owner = st["slot"]
        c0, p0, e0 = grade(rosters, SHIPPED, n, seeds)
        c1, p1, e1 = grade(rosters, MEASURED, n, seeds)
        print(f"\nmock {m} — owner slot {owner}"
              + (f", declared punt {'/'.join(st['punt'])}" if st.get("punt") else
                 ", no punt declared"))
        print(f"  {'':14}{'champ%':>9}{'playoff%':>10}{'ECW/wk':>9}{'finish':>8}")
        print(f"  {'shipped 0.15':14}{c0[owner]:>9.2f}{p0[owner]:>10.2f}"
              f"{e0[owner]:>9.3f}{rank_of(c0, owner):>8}")
        print(f"  {'measured 0.96':14}{c1[owner]:>9.2f}{p1[owner]:>10.2f}"
              f"{e1[owner]:>9.3f}{rank_of(c1, owner):>8}")
        print(f"  {'delta':14}{c1[owner]-c0[owner]:>+9.2f}"
              f"{p1[owner]-p0[owner]:>+10.2f}{e1[owner]-e0[owner]:>+9.3f}"
              f"{rank_of(c0, owner)-rank_of(c1, owner):>+8}")
        moved = sum(1 for s in rosters if rank_of(c0, s) != rank_of(c1, s))
        print(f"  room: {moved} of 12 seats change championship rank")
        out["mocks"][m] = {
            "owner_slot": owner, "punt": st.get("punt", []),
            "shipped": {"champ": c0[owner], "playoff": p0[owner],
                        "ecw": e0[owner], "finish": rank_of(c0, owner)},
            "measured": {"champ": c1[owner], "playoff": p1[owner],
                         "ecw": e1[owner], "finish": rank_of(c1, owner)},
            "room_seats_reordered": moved,
            "champ_by_slot_shipped": c0, "champ_by_slot_measured": c1,
        }
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()
