"""Instrument v2 panel disclosure (2026-08-05).

The week model moved from a fixed weekly lineup (10 starters x 1.0, 3
bench x 0.15) to daily-fill start rates (instrument v2) on the owner's
league-rules authority: Yahoo lineups are set daily, started games count
100%, bench games count 0, and bench players backfill open slots on their
game days. Correctness of the instrument is settled by those rules and
the measured daily-fill MC (`daily_lineup_mc.py`), NOT by this script.

This script is the E21-mandated DISCLOSURE of what the change does to the
card ordering (the deck's DeltaECW half consumes the same model): for
every panel mock, three arms under the v2 instrument, one CRN-paired
18,000-season set each (seeds 11/23/47 x 6,000):

  baseline — the mock as drafted
  v1cards  — the OLD deck ordering's #1 followed at every owner turn
             (cards from arena/results/e22_replay_m*.json, shipped arm)
  v2cards  — the NEW deck ordering's #1 followed the same way
             (cards from arena/results/v2_replay_m*.json)

Reading rule, registered before the run: the instrument ships on rules
authority; this table discloses the ordering consequence. If v2cards
lands more than 5pp below v1cards on two or more of the record mocks
(21/24/25/26) under v2 grading, the ordering half is escalated to the
owner as a decision before the next draft rather than silently kept.

Fresh clone + `python3 arena/mocks/v2_panel_disclosure.py` regenerates
arena/results/v2_panel_disclosure_out.json. V2P_MOCKS=34 etc. per-process.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e22_measurement as e22  # noqa: E402  (chdirs to repo root; loads pool)

os.environ["ARENA_WEEK_MODEL"] = "daily"  # v2-epoch harness: hard-set, immune to import order


def measure(mk):
    state = json.load(open(f"arena/data/states/draft_state_mock{mk}.json"))
    OWNER = state["slot"]
    picks = state["picks"]
    OWNER_TURNS = [i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER]

    old = json.load(open(f"arena/results/e22_replay_m{mk}.json"))
    new = json.load(open(f"arena/results/v2_replay_m{mk}.json"))
    cards = {
        "v1cards": {t["pickNo"]: [x["n"] for x in t["shipped"]] for t in old},
        "v2cards": {t["pickNo"]: [x["n"] for x in t["shipped"]] for t in new},
    }
    diverge = [t["rnd"] for t, o in zip(new, old)
               if t["shipped"][0]["n"] != o["shipped"][0]["n"]]

    def finish_board(newp):
        ros = {}
        for pk in newp:
            ros.setdefault(pk["slot"], []).append(e22.byname[pk["player"]])
        for s in range(1, 13):
            assert len(ros[s]) == 13, (mk, s)
        assert len({pk["player"] for pk in newp}) == 156
        return ros

    def apply_card(cardmap):
        newp = [dict(pk) for pk in picks]
        swaps = []
        for pn in OWNER_TURNS:
            i = pn - 1
            cur = newp[i]["player"]
            for nm in cardmap.get(pn, []):
                if nm == cur:
                    break
                j = next((k for k in range(len(newp)) if newp[k]["player"] == nm), None)
                if j is None or j <= i:
                    continue
                if newp[j]["slot"] != OWNER:
                    swaps.append([pn, cur, nm])
                newp[i]["player"], newp[j]["player"] = nm, cur
                break
        return finish_board(newp), swaps

    def run(ros):
        tc = {s: 0 for s in ros}
        tp = {s: 0 for s in ros}
        for sd in e22.HEAD_SEEDS:
            champs, plyf = e22.arena.simulate_seasons(ros, e22.HEAD_N, random.Random(sd))
            for s in ros:
                tc[s] += champs[s]
                tp[s] += plyf[s]
        T = e22.HEAD_N * len(e22.HEAD_SEEDS)
        return {"champ": round(100.0 * tc[OWNER] / T, 3),
                "playoff": round(100.0 * tp[OWNER] / T, 3),
                "finish": sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1,
                "seasons": T,
                "roster": [p["player"] for p in ros[OWNER]]}

    out = {"mock": mk, "owner_slot": OWNER,
           "instrument": "v2 daily-fill", "top1_diverge_rounds": diverge,
           "arms": {"baseline": run(finish_board([dict(pk) for pk in picks]))}}
    for arm in ("v1cards", "v2cards"):
        ros, swaps = apply_card(cards[arm])
        r = run(ros)
        r["swaps"] = swaps
        out["arms"][arm] = r
    return out


def main():
    only = os.environ.get("V2P_MOCKS")
    todo = only.split(",") if only else e22.PUNTED + e22.UNPUNTED
    results = {}
    for mk in todo:
        print(f"=== v2 disclosure mock {mk} ===", flush=True)
        results[mk] = measure(mk)
        a = results[mk]["arms"]
        print(f"  baseline {a['baseline']['champ']:6.2f} | v1cards {a['v1cards']['champ']:6.2f} "
              f"| v2cards {a['v2cards']['champ']:6.2f} | top1-diverge "
              f"{len(results[mk]['top1_diverge_rounds'])}/13", flush=True)
    path = ("arena/results/v2_panel_disclosure_out.json" if not only else
            f"arena/results/v2_panel_disclosure_out_m{'_'.join(todo)}.json")
    json.dump(results, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
