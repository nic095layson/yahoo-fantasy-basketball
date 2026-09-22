#!/usr/bin/env python3
"""Survival-chip calibration on a live room (mock 51 retro §A, generalized
2026-09-22): for every Top-5 card row the deck showed at an owner turn, the
DOM survival model's predicted P(still there at the owner's next turn) vs
what the room actually did. Feeds the refit the owner asked for after two
more live rooms (D51R-1). Reads a live_deckcard.py output (which reproduces
survivalP from the deck source) and the state.

    python3 arena/mocks/live_survival.py <mock> <deckcard.json> <out.json> [<other deckcard.json> ...]

Extra deckcard files (other rooms) are pooled into a combined Brier.
"""
import json, os, statistics, sys
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def rows_for(mock, deckcard_path):
    st = json.load(open(os.path.join(REPO, "arena", "data", "states", f"draft_state_{mock}.json")))
    dc = json.load(open(deckcard_path))
    picks = st["picks"]
    obs = []
    for t in dc:
        if not t["nextTurn"]:
            continue
        between = {pk["player"] for pk in picks[t["pick"]: t["nextTurn"] - 1]}  # picks strictly between the two owner turns
        for r in t["rows"]:
            if r["n"] == t["actual"] or r["surv"] is None:
                continue
            obs.append(dict(mock=mock, pick=t["pick"], n=r["n"], pred=r["surv"], alive=r["n"] not in between,
                            chip=r["chip"], mkt=r["mkt"], valRank=r["valRank"]))
    return obs


def summarize(obs):
    n = len(obs); alive = sum(o["alive"] for o in obs)
    return dict(rows=n, mean_pred=round(statistics.mean(o["pred"] for o in obs), 3), realized=round(alive / n, 3),
                alive=alive, brier=round(statistics.mean((o["pred"] - (1 if o["alive"] else 0)) ** 2 for o in obs), 3),
                by_chip={str(c): dict(n=len(sub), mean_pred=round(statistics.mean(o["pred"] for o in sub), 3),
                                      alive=sum(o["alive"] for o in sub))
                         for c in ("BUY NOW", "BUY NOW(shelf)", "TOSS-UP", None)
                         for sub in [[o for o in obs if o["chip"] == c]] if sub},
                survivors_called_le_2pct=[f"#{o['pick']} {o['n']} ({o['pred']:.2f})" for o in obs if o["alive"] and o["pred"] <= 0.02])


if __name__ == "__main__":
    mock, dc_path, out_path = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    obs = rows_for(mock, dc_path)
    out = {"mock": mock, "this_room": summarize(obs), "rows": obs}
    print(f"mock {mock}: {out['this_room']}")
    pooled = list(obs)
    for extra in sys.argv[4:]:
        m = int(os.path.basename(extra).split("_")[0][1:])
        more = rows_for(m, extra)
        pooled += more
        print(f"pooled with mock {m} ({len(more)} rows)")
    if len(pooled) > len(obs):
        out["pooled"] = summarize(pooled)
        print("POOLED:", out["pooled"])
    json.dump(out, open(out_path, "w"), indent=1)
