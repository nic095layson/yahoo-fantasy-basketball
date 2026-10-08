#!/usr/bin/env python3
"""How much do injured players on RIVAL rosters count in the category math? (owner question, 2026-10-08)

Every roster in the weekly model (arena.team_week_model, the same model the deck's card, punt
advisor and the retro grade use) scales each player by arena.weekly_availability, read from the
LEADING tag of his note: *-recovery 0.60, *-risk 0.75, untagged 0.88. Nothing is calendar-aware:
a man out until January counts at his tier every week. This re-grades one room's FINAL rosters
three ways for the named men: as shipped, at 0 (what an early-season week looks like while they
sit), and at the healthy 0.88.

  python3 arena/mocks/injured_rivals_cf.py MOCK TAG OUT.json "Name One" "Name Two" ...
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
MOCK, TAG, OUT, NAMES = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], MOCK]          # live_retro reads the mock number from argv at import
import live_retro as L                  # noqa: E402
arena = L.arena
players = L.load_pool(TAG)
ros, taken, missing = L.rosters_upto(players, len(L.PICKS))
assert not missing, missing
byn = {p["player"]: p for p in players}
assert all(n in byn for n in NAMES), [n for n in NAMES if n not in byn]
ship = arena.weekly_availability


def run(label, override):
    def wa(p):
        return override.get(p["player"], ship(p))
    arena.weekly_availability = wa
    try:
        models = {s: arena.team_week_model(r) for s, r in ros.items()}
    finally:
        arena.weekly_availability = ship
    ecw = {s: L.pwins(models[s], [models[o] for o in ros if o != s]) for s in ros}
    mine = ecw[L.SLOT]
    per = {o: sum(L.pwin_cats(models[L.SLOT], models[o]).values()) for o in ros if o != L.SLOT}
    return dict(label=label, owner_ecw=round(mine, 3),
                owner_rank=1 + sum(1 for s in ros if s != L.SLOT and ecw[s] > mine),
                owner_vs_seat={str(o): round(v, 3) for o, v in per.items()},
                seat_ecw={str(s): round(v, 3) for s, v in ecw.items()})


holders = {pk["player"]: pk["slot"] for pk in L.PICKS if pk["player"] in NAMES}
out = dict(mock=int(MOCK), pool=TAG, owner_seat=L.SLOT,
           holders={n: dict(seat=holders.get(n), pick=next((i + 1 for i, pk in enumerate(L.PICKS) if pk["player"] == n), None),
                            tag=(byn[n].get("note") or "").lower().split()[0].split("(")[0] if byn[n].get("note") else "",
                            weekly_availability=ship(byn[n])) for n in NAMES},
           runs=[run("shipped", {}), run("named men at 0", {n: 0.0 for n in NAMES}),
                 run("named men at the healthy 0.88", {n: 0.88 for n in NAMES})])
json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for r in out["runs"]:
    print(f"{r['label']:32s} owner ECW {r['owner_ecw']:.3f} rank {r['owner_rank']} | owner vs holders "
          + ", ".join(f"seat {holders[n]} {r['owner_vs_seat'][str(holders[n])]:.3f}" for n in NAMES if n in holders))
