#!/usr/bin/env python3
"""D59-2 large: the two-pick 🎯 against the D58-3 bar, across the public live rooms.
Pre-registered in arena/results/pair_experiment_2026-10-01_design.md (read it first).

    python3 arena/mocks/pair_experiment.py 51 52 53 54 56 57 58 59 --out arena/results/pair_experiment_2026-10-01.json

Runs `live_retro.py <mock> pairarms` per room (its own pool tag; m<NN>_pairarms.json beside
the room's files), then aggregates: per-room title odds of the blend-🎯 chain and the
two-pick-🎯 chain on both seed sets, the turns where the marker moved, and the verdict
against the bar (pair mean ≥ blend mean on BOTH seed sets)."""
import argparse, json, os, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.normpath(os.path.join(HERE, "..", "results"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rooms", nargs="+", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip-run", action="store_true", help="aggregate existing m<NN>_pairarms.json only")
    a = ap.parse_args()
    rooms = {}
    for m in a.rooms:
        if not a.skip_run:
            r = subprocess.run([sys.executable, os.path.join(HERE, "live_retro.py"), str(m), "pairarms"],
                               capture_output=True, text=True)
            sys.stdout.write("\n".join(r.stdout.strip().splitlines()[-8:]) + "\n")
            if r.returncode != 0:
                sys.stdout.write(r.stderr[-2000:] + "\n")
                sys.exit(f"room {m} failed")
        rooms[m] = json.load(open(os.path.join(R, f"m{m}_pairarms.json")))
    rows, means = [], {}
    for key in ("as_drafted_S1", "as_drafted_S2", "blend_S1", "blend_S2", "pair_S1", "pair_S2"):
        means[key] = round(statistics.mean(rooms[m]["results"][key]["champ"] for m in rooms), 3)
    for m, d in rooms.items():
        res = d["results"]
        rows.append(dict(mock=m, tag=d["tag"], price_source=d["price_source"], blend_matches_recorded_arms=d["blend_matches_recorded_arms"],
                         as_drafted=(res["as_drafted_S1"]["champ"], res["as_drafted_S2"]["champ"]),
                         blend=(res["blend_S1"]["champ"], res["blend_S2"]["champ"]),
                         pair=(res["pair_S1"]["champ"], res["pair_S2"]["champ"]),
                         blend_ecw=res["blend_ecw"], pair_ecw=res["pair_ecw"],
                         moves=[(x["pick"], x["rows"][0], x["rows"][x["idx"]], x["gain"]) for x in res["pair_moves"]],
                         chains_identical=(res["blend_swaps"] == res["pair_swaps"])))
    moved = sum(len(r["moves"]) for r in rows)
    bar = means["pair_S1"] >= means["blend_S1"] and means["pair_S2"] >= means["blend_S2"]
    per_room = dict(pair_better_S1=sum(1 for r in rows if r["pair"][0] > r["blend"][0]), pair_worse_S1=sum(1 for r in rows if r["pair"][0] < r["blend"][0]),
                    pair_better_S2=sum(1 for r in rows if r["pair"][1] > r["blend"][1]), pair_worse_S2=sum(1 for r in rows if r["pair"][1] < r["blend"][1]),
                    identical=sum(1 for r in rows if r["chains_identical"]))
    verdict = ("SHIP MARKER (bar holds, marker moved)" if bar and moved else
               "INERT (bar holds trivially, marker never moved) — PAIR_MARKER false" if bar else
               "BAR FAILED — PAIR_MARKER false, advice only")
    out = dict(date="2026-10-01", design="pair_experiment_2026-10-01_design.md", rooms=rows, means=means, moved_turns=moved,
               per_room=per_room, bar_holds=bar, verdict=verdict)
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(dict(means=means, moved_turns=moved, per_room=per_room, bar_holds=bar, verdict=verdict), indent=1))
    for r in rows:
        print(f"m{r['mock']:<3} {r['tag']:<4} as drafted {r['as_drafted']} blend {r['blend']} pair {r['pair']} moves {r['moves']} arms-match {r['blend_matches_recorded_arms']} {r['price_source']}")


if __name__ == "__main__":
    main()
