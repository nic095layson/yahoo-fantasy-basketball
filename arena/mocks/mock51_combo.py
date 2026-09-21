#!/usr/bin/env python3
"""Combined arm (the two turns where the card was right AND it mattered:
Turner at #82, Lopez at #154), CRN-paired like the other arms, plus the
ledger's board rank (13-man kept-total z-sum rank) and ECW rank."""
import json, os, sys
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
import mock51_retro as R

players = R.load_pool("v23")
ros, _, _ = R.rosters_upto(players, len(R.PICKS))
tot = {s: sum(sum(p["z"][c] for c in R.CATS) for p in r) for s, r in ros.items()}
board_rank = 1 + sum(1 for s in ros if s != R.SLOT and tot[s] > tot[R.SLOT])
print("kept-total z-sum by seat:", {R.CAST.get(s, f'T{s}'): round(v, 2) for s, v in sorted(tot.items(), key=lambda kv: -kv[1])})
print(f"owner board rank (kept-total) {board_rank}/12, total {tot[R.SLOT]:+.2f}")

arms = {"combo_turner82_lopez154": [(81, "Myles Turner"), (153, "Brook Lopez")],
        "combo_turner82_lopez154_pritchard63": [(62, "Payton Pritchard"), (81, "Myles Turner"), (153, "Brook Lopez")]}
prev = json.load(open(SP + "/m51_arms.json"))
for name, sw in arms.items():
    r2, _ = R.apply_swaps(players, sw)
    res = R.run_arm(r2)
    me = res[R.SLOT]
    rank = 1 + sum(1 for s in r2 if s != R.SLOT and res[s][0] > me[0])
    prev[name] = dict(champ=round(me[0], 3), playoff=round(me[1], 2), champ_rank=rank, swaps=[(n + 1, a) for n, a in sw])
    print(f"{name:<40} champ {me[0]:6.3f}%  playoff {me[1]:5.2f}%  rank {rank}/12")
prev["_board_rank"] = board_rank
prev["_kept_total"] = {str(s): round(v, 3) for s, v in tot.items()}
# the as-drafted run's per-seat champ% for the debrief table
r0, _ = R.apply_swaps(players, [])
res0 = R.run_arm(r0)
prev["_as_drafted_by_seat"] = {str(s): [round(v[0], 3), round(v[1], 2)] for s, v in res0.items()}
print("as-drafted champ% by seat:", {R.CAST.get(int(s), f'T{s}'): v[0] for s, v in sorted(prev["_as_drafted_by_seat"].items(), key=lambda kv: -kv[1][0])})
json.dump(prev, open(SP + "/m51_arms.json", "w"), indent=1)
