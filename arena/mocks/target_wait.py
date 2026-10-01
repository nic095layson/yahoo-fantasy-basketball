#!/usr/bin/env python3
"""Did the card's 🎯 wait? (owner question, mock 59, 2026-10-01)

For every owner turn in the named live rooms, read the deck card replayed from the page the
owner drafted against (arena/results/m<NN>_deckcard_<tag>.json) and the room's final state,
and record: the 🎯, its Mkt rank against the pick number ("depth" = mkt − pick), its modeled
survival to the owner's next turn, where it actually went, whether it was still on the board at
the owner's next turn and the one after, and the scarcest Top-5 row (lowest modeled survival)
with its blend gap to the 🎯 and where it went.  Turns where the owner took the 🎯 say nothing
about waiting and are flagged `taken_now`.

    python3 arena/mocks/target_wait.py 56:v31 57:v33 58:v35 59:v37 arena/results/target_wait_2026-10-01.json
"""
import json, sys
R = "arena/results/"
S = "arena/data/states/"


def main(argv):
    out_path = argv[-1]
    rooms = [a.split(":") for a in argv[:-1]]
    turns, summary = [], {}
    for m, tag in rooms:
        m = int(m)
        dc = json.load(open(f"{R}m{m}_deckcard_{tag}.json"))
        st = json.load(open(f"{S}draft_state_{m}.json"))
        picks = st["picks"]
        pos = {p["player"]: i + 1 for i, p in enumerate(picks)}
        owner = [i + 1 for i, p in enumerate(picks) if p["slot"] == st["slot"]]
        for t in dc:
            pk, rows = t["pick"], t["rows"]
            tg = next((r for r in rows if r.get("target")), rows[0])
            later = [o for o in owner if o > pk]
            nxt = later[0] if later else None
            nxt2 = later[1] if len(later) > 1 else None
            went = pos.get(tg["n"])
            scarce = [r for r in rows[:5] if (r.get("surv") if r.get("surv") is not None else 1.0) < 0.5]
            sc = min(scarce, key=lambda r: r["surv"]) if scarce else None
            turns.append(dict(
                mock=m, tag=tag, pick=pk, target=tg["n"], mkt=tg.get("mkt"),
                depth=(tg.get("mkt") - pk) if tg.get("mkt") is not None else None,
                surv=tg.get("surv"), went=went, taken_now=(went == pk),
                alive_next=(None if nxt is None else (went is None or went >= nxt)),
                alive_next2=(None if nxt2 is None else (went is None or went >= nxt2)),
                next_turn=nxt, next_turn2=nxt2,
                scarcest=(None if sc is None else dict(n=sc["n"], surv=sc["surv"],
                                                      gap=round(tg["ds"] - sc["ds"], 4), went=pos.get(sc["n"]))),
            ))
    passed = [t for t in turns if not t["taken_now"] and t["alive_next"] is not None]
    for label, lo, hi in (("deep (mkt − pick ≥ 24)", 24, 10**9), ("mid (12–23)", 12, 23), ("near (< 12)", -10**9, 11)):
        sel = [t for t in passed if t["depth"] is not None and lo <= t["depth"] <= hi]
        summary[label] = dict(passed_on=len(sel), alive_next=sum(t["alive_next"] for t in sel),
                              alive_next2=sum(1 for t in sel if t["alive_next2"]),
                              with_next2=sum(1 for t in sel if t["alive_next2"] is not None),
                              turns=[f"m{t['mock']} #{t['pick']} {t['target']} (+{t['depth']}, surv {t['surv']}) → went #{t['went']}" for t in sel])
    res = dict(date="2026-10-01", rooms=[f"{m}:{tag}" for m, tag in rooms], turns=turns, summary=summary)
    json.dump(res, open(out_path, "w"), indent=1)
    for k, v in summary.items():
        print(f"{k:<26} passed on {v['passed_on']:>2}  alive at next owner turn {v['alive_next']:>2}  alive two turns on {v['alive_next2']:>2} of {v['with_next2']}")
        for s in v["turns"]:
            print("   ", s)


if __name__ == "__main__":
    main(sys.argv[1:])
