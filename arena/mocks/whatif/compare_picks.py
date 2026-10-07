#!/usr/bin/env python3
"""Pick-by-pick view: the real 2025-26 draft vs the canonical redraft (seed 1000); the owner's 13 picks under both,
with draft-time value rank, Yahoo pre-draft rank, and actual 2025-26 production rank (z-sum on the actual pool)."""
import sys, json, csv
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad/ls2025"
D = "/home/user/yahoo-fantasy-basketball"; sys.path.insert(0, D + "/scripts")
import hoops
CATS = hoops.CATS
def ranks(path):
    hoops.DATA_PATH = path; pl = hoops.zscores(hoops.load_players())
    order = sorted(pl, key=lambda p: -sum(p["z"][c] for c in CATS)); return {p["player"]: i + 1 for i, p in enumerate(order)}, {p["player"]: round(sum(p["z"][c] for c in CATS), 2) for p in pl}
vr, vz = ranks(S + "/pool_2025.csv"); ar, az = ranks(S + "/pool_actual.csv")
gp = json.load(open(S + "/actual_gp.json"))
real = json.load(open(S + "/real_draft_2025.json")); seat_of = {int(k): v for k, v in real["seat_of"].items()}
rooms = json.load(open(S + "/rooms_2025.json")); room = rooms["rooms"][0]
mkt = {}
import re, unicodedata
fold = lambda s: "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).replace(".", "").lower().strip()
pool = {fold(r["player"]): r["player"] for r in csv.DictReader(open(S + "/pool_2025.csv", encoding="utf-8"))}
for line in open(D + "/arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt", encoding="utf-8"):
    m = re.match(r"^(\d+)\t(.+?) \([A-Z]{2,3} - [A-Z,]+\)\t", line)
    if m and fold(m.group(2)) in pool: mkt[pool[fold(m.group(2))]] = int(m.group(1))
state = json.load(open(S + "/draft_state_real_2025.json"))
realp = state["picks"]; mine_real = [(i + 1, p["player"]) for i, p in enumerate(realp) if p["slot"] == 4]
mine_cf = [(i + 1, p["player"]) for i, p in enumerate(room["picks"]) if p["slot"] == 4]
fmt = lambda n: f"{n:<24} val#{vr.get(n, '-'):>4} mkt#{mkt.get(n, '-'):>4}  actual#{ar.get(n, '-'):>4} z{az.get(n, 0):+6.2f} gp {gp.get(n, {}).get('gp', 0):>2}"
print("=== the owner's real 2025-26 picks (seat 4)"); [print(f"#{k:>3} {fmt(n)}") for k, n in mine_real]
print("    sum actual z:", round(sum(az.get(n, 0) for _, n in mine_real), 2), "| sum draft-time z:", round(sum(vz.get(n, 0) for _, n in mine_real), 2))
print("=== the card's picks, canonical redraft (seed 1000)"); [print(f"#{k:>3} {fmt(n)}") for k, n in mine_cf]
print("    sum actual z:", round(sum(az.get(n, 0) for _, n in mine_cf), 2), "| sum draft-time z:", round(sum(vz.get(n, 0) for _, n in mine_cf), 2))
print("=== round 1-2, real vs redraft (seat: real -> redraft)")
for i in range(24):
    print(f"#{i+1:>2} {seat_of[realp[i]['slot']]:<7} real {realp[i]['player']:<26} redraft {room['picks'][i]['player']:<26}" + (" (same)" if realp[i]['player'] == room['picks'][i]['player'] else ""))
# where the real owner's men went in the redraft, and vice versa
cf_pos = {p["player"]: (i + 1, seat_of[p["slot"]]) for i, p in enumerate(room["picks"])}
real_pos = {p["player"]: (i + 1, seat_of[p["slot"]]) for i, p in enumerate(realp)}
print("=== the owner's real men in the redraft:", [(n, cf_pos.get(n, "undrafted")) for _, n in mine_real])
print("=== the card's men in the real draft:", [(n, real_pos.get(n, "undrafted")) for _, n in mine_cf])
# the card at the owner's turns (top-5 and what the real owner took there)
print("=== the card's top-5 at each owner turn (redraft) vs the owner's real pick at that turn")
rp = dict(mine_real)
for e in room["cardLog"]:
    print(f"#{e['pick']:>3} 🎯 {e['top5'][0]['n']:<22} top5 {[r['n'] for r in e['top5']]}  | real pick: {rp.get(e['pick'])}")
# the redraft's spread: the owner's roster frequency by round
from collections import Counter
byround = {}
for rm in rooms["rooms"]:
    for i, p in enumerate(rm["picks"]):
        if p["slot"] == 4: byround.setdefault(i // 12 + 1, Counter())[p["player"]] += 1
print("=== most common card pick by round across 30 rooms:", {r: c.most_common(2) for r, c in byround.items()})
