"""Usage: python3 arena/mocks/whatif_hk_breakeven.py > breakeven.txt
Break-even on the engine's own two scales: t = 0 is the shipped risk tag (value x0.78, weekly 0.75), t = 1 is a healthy
row (value x1.0, weekly 0.88); both move together, linearly. Mock 75's #10 board."""
import sys
import os
DECK=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.argv=["live_retro.py","75"]; sys.path.insert(0,DECK+"/arena/mocks")
import live_retro as lr
hoops, arena = lr.hoops, lr.arena
P = lr.load_pool("v58"); oa, ow = hoops.availability, arena.weekly_availability; H="Tyrese Haliburton"
for t in (0.0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.75, 1.0):
    va, wa = 0.78 + 0.22*t, 0.75 + 0.13*t
    hoops.availability = lambda p, va=va: va if p["player"]==H else oa(p)
    arena.weekly_availability = lambda p, wa=wa: wa if p["player"]==H else ow(p)
    c = lr.card(P, 9); o=[c["pool"][i]["player"] for i in c["order"]]
    hi, ki = o.index(H), o.index("Karl-Anthony Towns")
    ih=c["order"][hi]; ik=c["order"][ki]
    print(f"t={t:.2f} value x{va:.3f} weekly {wa:.3f}: Haliburton card #{hi+1} (ΔECW {c['decw'][ih]:.3f}, value {c['vals'][ih]:.2f}) | Towns #{ki+1} (ΔECW {c['decw'][ik]:.3f}) | #1 {o[0]}")
