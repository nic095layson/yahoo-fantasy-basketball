"""E9 round 2: regularized ΔECW cards (findings_2026-08-04_decw_round1.md).

Round 1 failed the ship bar because the raw marginal objective concedes
categories emergently (m25 −27.6, m26 −19.5). Round-2 variants:

  blend   — per-turn percentile blend: score = α·pct(ΔECW) + (1−α)·pct(adjValue)
            (the value term keeps paying for every category — the concession
            floor expressed in rank space, no new constants inside ΔECW)
  anchor  — first K owner picks scored by pure adj-value (anchor protection:
            ΔECW's opponent context at those turns is 0–2 partial rosters,
            i.e. noise, and round 1 swapped Wemby out on turn one)

Usage: DECW_OUT=<dir> python3 decw_card_v2.py <alpha> <anchor_rounds> [mock...]
Writes decw_card_m<NN>.json into DECW_OUT (same schema as v1, so decw_cf.py
consumes them unchanged via its DECW_OUT env var).
"""

import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import sys, os, json, math

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}
UP = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/"
MOCKS = {16: ("fdc581ea-draft_state_5.json", 3), 17: ("39481e0a-draft_state_6.json", 12),
         18: ("01f8de77-draft_state_7.json", 2), 19: ("e1e01942-draft_state_8.json", 4),
         20: ("b6aeaca6-draft_state_9.json", 5), 21: ("773c5fc1-draft_state_10.json", 4),
         23: ("117b5573-draft_state_12.json", 12), 24: ("1a51e011-draft_state_13.json", 1),
         25: ("c0d8a926-draft_state_14.json", 2), 26: ("0371e8b0-draft_state_15.json", 3),
         27: ("5130afad-draft_state_16.json", 4), 28: ("4cb343cd-draft_state_17.json", 5),
         29: ("9c3e53b2-draft_state_18.json", 6), 30: ("e7463e95-draft_state_19.json", 7)}

ALPHA = float(sys.argv[1])
ANCHOR = int(sys.argv[2])
OUTDIR = os.environ["DECW_OUT"]
os.makedirs(OUTDIR, exist_ok=True)


def adj_value(p):
    return hoops.adj_value(p)


def pwins_total(my_model, opp_models):
    tot = 0.0
    for om in opp_models:
        for c in CATS:
            ma, va = my_model[0][c], my_model[1][c]
            mb, vb = om[0][c], om[1][c]
            d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            tot += (1 - p) if c == "TO" else p
    return tot / (len(opp_models) or 1)


def pct_ranks(vals):
    """value -> percentile in [0,1] (average rank for ties)."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = [0.0] * len(vals)
    for r, i in enumerate(order):
        out[i] = r / (len(vals) - 1 or 1)
    return out


def card_for(mock):
    fn, owner = MOCKS[mock]
    st = json.load(open(UP + fn))
    picks = st["picks"]
    turns = []
    n_mine = 0
    for i, pk in enumerate(picks):
        if pk["slot"] != owner:
            continue
        taken = {q["player"] for q in picks[:i]}
        mine = [byname[q["player"]] for q in picks[:i] if q["slot"] == owner]
        opps = {}
        for q in picks[:i]:
            if q["slot"] != owner:
                opps.setdefault(q["slot"], []).append(byname[q["player"]])
        opp_models = [arena.team_week_model(r) for r in opps.values() if r]
        pool = [p for p in players if p["player"] not in taken and hoops.availability(p) > 0]
        vals = [adj_value(p) for p in pool]
        if n_mine < ANCHOR or not opp_models:
            scores = vals  # anchor protection / no-opponent fallback: pure value
        else:
            base = pwins_total(arena.team_week_model(mine), opp_models) if mine else 0.0
            decw = [pwins_total(arena.team_week_model(mine + [p]), opp_models) - base for p in pool]
            pd, pv = pct_ranks(decw), pct_ranks(vals)
            scores = [ALPHA * a + (1 - ALPHA) * b for a, b in zip(pd, pv)]
        ranked = sorted(zip(scores, (p["player"] for p in pool)), reverse=True)
        turns.append({"pickNo": i + 1, "actual": pk["player"],
                      "top5": [{"n": n, "decw": round(s, 4)} for s, n in ranked[:5]],
                      "actual_rank": next((k + 1 for k, (_, n) in enumerate(ranked) if n == pk["player"]), None)})
        n_mine += 1
    return turns


for m in [int(x) for x in sys.argv[3:]] or sorted(MOCKS):
    turns = card_for(m)
    json.dump(turns, open(os.path.join(OUTDIR, f"decw_card_m{m}.json"), "w"), indent=1)
    print(f"m{m}: v2 card (alpha={ALPHA}, anchor={ANCHOR})")
