"""E20 measurement (owner-authorized 2026-08-05, measure-only under the freeze).

Both Top-5 orderings — SHIPPED (punt-blind blend50) and PUNT-AWARE (same
blend, adjValue under the declared punt + pwins over kept cats) — followed
at every owner turn across ALL FIVE punted mocks in the ledger, simulated
CRN-paired against the as-drafted baseline. Verifier corrections from the
mock-34 counterfactual are built in:
  - placebo is DEPTH-MATCHED (random legal target within the next 25 picks
    on the running board, not uniform over the whole board), matched to the
    winning card arm's roster-changing turns; 3 draws, mean reported
  - exact-score ties between arms at any turn are disclosed in the output
  - one season set (HEAD_SEEDS x HEAD_N) for every arm — no estimator mixing
  - every arm reports its full season denominator

Fresh clone + `python3 arena/mocks/e20_measurement.py` regenerates
arena/results/e20_measurement_out.json. Runtime ~1-2h serial; set
E20_MOCKS=22 (etc.) to run one mock per process for parallelism.

Ship decision NOT taken here: the September bar (SEPTEMBER-PLAN E20) does
that. This file only measures.
"""
import json
import os
import random
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(REPO)
sys.path = [os.path.join(REPO, "scripts"), os.path.join(REPO, "arena")] + [
    p for p in sys.path if p not in (os.path.join(REPO, "scripts"), os.path.join(REPO, "arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}

MOCKS = {
    "22": dict(state="arena/data/states/draft_state_mock22.json", replay="arena/results/m22_replay.json"),
    "31": dict(state="arena/data/states/draft_state_mock31.json", replay="arena/results/m31_replay.json"),
    "32": dict(state="arena/data/states/draft_state_mock32.json", replay="arena/results/m32_replay.json"),
    "34": dict(state="arena/data/states/draft_state_mock34.json", replay="arena/results/m34_replay.json"),
    "35": dict(state="arena/data/states/draft_state_mock35.json", replay="arena/results/m35_replay.json"),
}
HEAD_SEEDS = [11, 23, 47]
HEAD_N = 6000
PLACEBO_DRAWS = 3
PLACEBO_DEPTH = 25


def measure_mock(mk, cfg):
    state = json.load(open(cfg["state"]))
    OWNER = state["slot"]
    PUNT = list(state.get("punt") or [])
    assert PUNT, (mk, "not a punted mock")
    KEPT = [c for c in CATS if c not in PUNT]
    picks = state["picks"]
    assert len(picks) == 156 and state["teams"] == 12 and state["size"] == 13
    assert not [pk["player"] for pk in picks if pk["player"] not in byname]
    OWNER_TURNS = [i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER]
    assert len(OWNER_TURNS) == 13

    replay = json.load(open(cfg["replay"]))
    assert [t["pickNo"] for t in replay] == OWNER_TURNS
    for t in replay:
        assert t["actual"] == picks[t["pickNo"] - 1]["player"], (mk, t["pickNo"])
    cards = {k: {t["pickNo"]: [x["n"] for x in t[k]] for t in replay}
             for k in ("shipped", "puntAware")}
    # tie disclosure: exact ds tie between an arm's #1 and #2 at any turn
    ties = {}
    for k in ("shipped", "puntAware"):
        ties[k] = [t["pickNo"] for t in replay
                   if len(t[k]) > 1 and t[k][0].get("ds") is not None
                   and t[k][0]["ds"] == t[k][1]["ds"]]

    def finish_board(newp):
        ros = {}
        for pk in newp:
            ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
        for s in range(1, 13):
            assert len(ros[s]) == 13, (mk, s)
        names = [pk["player"] for pk in newp]
        assert len(set(names)) == 156
        return ros

    def apply_card(cardmap):
        """walk owner turns in pick order against a RUNNING board (pairwise
        swaps; legality screened vs the running board, mock28_cf lesson)."""
        newp = [dict(pk) for pk in picks]
        swaps, noops = [], []
        for pn in OWNER_TURNS:
            i = pn - 1
            cur = newp[i]["player"]
            for nm in cardmap.get(pn, []):
                if nm == cur:
                    break
                j = next((k for k in range(len(newp)) if newp[k]["player"] == nm), None)
                if j is None or j <= i:
                    continue  # undrafted in this room, or already off the running board: descend
                (noops if newp[j]["slot"] == OWNER else swaps).append([pn, cur, nm])
                newp[i]["player"], newp[j]["player"] = nm, cur
                break
        return finish_board(newp), swaps, noops

    def placebo(turns, rng):
        """depth-matched: target drawn from the next PLACEBO_DEPTH legal
        picks on the running board at the same turns."""
        newp = [dict(pk) for pk in picks]
        swaps = []
        for pn in sorted(turns):
            i = pn - 1
            legal = [k for k in range(i + 1, min(i + 1 + PLACEBO_DEPTH, len(newp)))
                     if newp[k]["slot"] != OWNER]
            if not legal:
                continue
            j = rng.choice(legal)
            newp[i]["player"], newp[j]["player"] = newp[j]["player"], newp[i]["player"]
            swaps.append(pn)
        return finish_board(newp), swaps

    def run(ros):
        tc = {s: 0 for s in ros}
        tp = {s: 0 for s in ros}
        for sd in HEAD_SEEDS:
            champs, plyf = arena.simulate_seasons(ros, HEAD_N, random.Random(sd))
            for s in ros:
                tc[s] += champs[s]
                tp[s] += plyf[s]
        T = HEAD_N * len(HEAD_SEEDS)
        kept_z = sum(sum(p["z"][c] for c in KEPT) for p in ros[OWNER])
        return {"champ": round(100.0 * tc[OWNER] / T, 3),
                "playoff": round(100.0 * tp[OWNER] / T, 3),
                "finish": sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1,
                "seasons": T, "kept_z": round(kept_z, 2),
                "roster": [p["player"] for p in ros[OWNER]]}

    out = {"mock": mk, "owner_slot": OWNER, "punt": PUNT,
           "seeds": HEAD_SEEDS, "seasons_per_arm": HEAD_N * len(HEAD_SEEDS),
           "ties_at_top": ties, "arms": {}}
    base_ros = finish_board([dict(pk) for pk in picks])
    out["arms"]["baseline"] = run(base_ros)

    arm_rosters = {}
    for k in ("shipped", "puntAware"):
        ros, swaps, noops = apply_card(cards[k])
        r = run(ros)
        r["swaps"] = swaps
        r["noop_swaps"] = noops
        out["arms"][k] = r
        arm_rosters[k] = (ros, [s[0] for s in swaps])

    winner = max(("shipped", "puntAware"), key=lambda k: out["arms"][k]["champ"])
    wturns = arm_rosters[winner][1]
    out["placebo_matched_to"] = winner
    pl = []
    for d in range(PLACEBO_DRAWS):
        rng = random.Random(4200 + d)
        ros, sw = placebo(wturns, rng)
        r = run(ros)
        r["swap_turns"] = sw
        pl.append(r)
    out["arms"]["placebo_draws"] = pl
    out["arms"]["placebo_mean_champ"] = round(sum(x["champ"] for x in pl) / len(pl), 3)
    return out


def main():
    only = os.environ.get("E20_MOCKS")
    todo = only.split(",") if only else list(MOCKS)
    results = {}
    for mk in todo:
        print(f"=== mock {mk} ===", flush=True)
        results[mk] = measure_mock(mk, MOCKS[mk])
        a = results[mk]["arms"]
        print(f"  baseline {a['baseline']['champ']:6.2f} | shipped-follow {a['shipped']['champ']:6.2f} "
              f"| punt-aware-follow {a['puntAware']['champ']:6.2f} | placebo {a['placebo_mean_champ']:6.2f}",
              flush=True)
    out_path = ("arena/results/e20_measurement_out.json" if not only else
                f"arena/results/e20_measurement_out_m{'_'.join(todo)}.json")
    json.dump(results, open(out_path, "w"), indent=1)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
