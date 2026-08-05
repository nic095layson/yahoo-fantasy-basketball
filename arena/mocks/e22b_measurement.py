"""E22b measurement (owner-directed 2026-08-05: "it wouldn't routinely have
me load up on 5 or 6 C's").

Guard-rail SLF, exactly as registered in SEPTEMBER-PLAN E22b: keep the
shipped static ordering at every turn EXCEPT when the shipped Top-5 is
>=4/5 one position family (G/F/C; dual-eligible players count in both) in
round 10 or later — at those turns, use the SLF (resil) ordering from the
same committed E22 replays. Owner-league fact anchoring the trigger: at
most FOUR centers can start a day (C, C, Util, Util; Util is any
position), so a late all-big card is offering picks that cannot all play.

Arms: baseline and shipped are the committed E22 numbers (identical seeds
and machinery); this script simulates the ONE new arm (e22b) for the
mocks where its card differs from shipped, and records e22b == shipped
for the rest.

BAR (registered with E22b, applied as written): re-clear the full E22
panel — (a) non-regression on m21/24/25/26 (>= shipped - 1.5pp each);
(b) punted set: beat shipped on >=5 of the 9 punted mocks AND mean gain
> +1.0pp. Ties (identical cards) are not wins.

Fresh clone + `python3 arena/mocks/e22b_measurement.py` regenerates
arena/results/e22b_measurement_out.json. E22B_MOCKS=34 etc. for one mock
per process (partials: e22b_measurement_out_m<ids>.json).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e22_measurement as e22  # noqa: E402  (chdirs to repo root on import)

FAM = {"PG": "G", "SG": "G", "SF": "F", "PF": "F", "C": "C"}


def fams(pos):
    return {FAM[t.strip()] for t in pos.split(",") if t.strip() in FAM}


def e22b_cardmap(replay):
    """shipped cards, resil at triggered turns (registered trigger)."""
    cards = {}
    trig_turns = []
    for t in replay:
        trig = None
        if t["rnd"] >= 10 and len(t["shipped"]) == 5:
            for f in ("G", "F", "C"):
                if sum(1 for x in t["shipped"] if f in fams(x["pos"])) >= 4:
                    trig = f
                    break
        src = t["resil"] if trig else t["shipped"]
        cards[t["pickNo"]] = [x["n"] for x in src]
        if trig:
            trig_turns.append([t["rnd"], trig])
    return cards, trig_turns


def measure_e22b(mk):
    """one new arm on the E22 machinery; reuses its state/replay assertions."""
    state = json.load(open(f"arena/data/states/draft_state_mock{mk}.json"))
    replay = json.load(open(f"arena/results/e22_replay_m{mk}.json"))
    for t in replay:
        t.setdefault("rnd", None)
    cards, trig_turns = e22b_cardmap(replay)
    shipped_cards = {t["pickNo"]: [x["n"] for x in t["shipped"]] for t in replay}
    identical = cards == shipped_cards
    full = e22.measure_mock.__globals__  # noqa: F841  (import side effects only)

    # rebuild the minimal apply/run pipeline via measure_mock's own helpers is
    # not exposed; re-run measure_mock-equivalent inline for the single arm.
    OWNER = state["slot"]
    picks = state["picks"]
    OWNER_TURNS = [i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER]

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

    import random
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

    out = {"mock": mk, "owner_slot": OWNER, "trigger_turns": trig_turns,
           "card_identical_to_shipped": identical}
    if identical:
        out["arm"] = "== shipped (no simulation needed)"
        return out
    ros, swaps = apply_card(cards)
    r = run(ros)
    r["swaps"] = swaps
    out["arm"] = r
    return out


def main():
    only = os.environ.get("E22B_MOCKS")
    todo = only.split(",") if only else e22.PUNTED + e22.UNPUNTED
    results = {}
    for mk in todo:
        print(f"=== e22b mock {mk} ===", flush=True)
        results[mk] = measure_e22b(mk)
        a = results[mk]
        c = a["arm"]["champ"] if isinstance(a["arm"], dict) else "== shipped"
        print(f"  e22b {c} | triggers {a['trigger_turns']}", flush=True)
    path = ("arena/results/e22b_measurement_out.json" if not only else
            f"arena/results/e22b_measurement_out_m{'_'.join(todo)}.json")
    json.dump(results, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
