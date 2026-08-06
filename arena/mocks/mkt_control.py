"""Market-autopilot control: same 8 rooms/seeds/casts, owner seat drafts pure
ADP. If this ALSO crushes the room, the room is soft; if it lands near 1/12
(8.33%), the room punishes plain drafting and the tool's edge is real."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e25_measurement as m
m.RUNNER = os.environ.get("ROOM_RUNNER_MKT", m.RUNNER.replace("room_run.js", "room_run_mkt.js"))
only = os.environ.get("MKT_ROOMS")
out = {}
for seed, slot, _pol, punt in m.ROOMS:
    if only and str(seed) != only: continue
    room = m.gen_room(seed, slot, False, "mkt", punt)
    g = m.grade(room)
    out[f"{seed}_{slot}"] = {"owner": g["owner"], "cast": g["cast"] if "cast" in g else room["cast"]}
    print(f'{seed}_{slot}: mkt-owner champ {g["owner"]["champ"]:6.2f} | ecw {g["owner"]["ecw"]:.3f}', flush=True)
p = f"arena/results/mkt_control_out{'_'+only if only else ''}.json"
json.dump(out, open(p, "w"), indent=1)
print("wrote", p)
