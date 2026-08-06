"""E9 prototype (owner-authorized 2026-08-04): the ΔECW draft-time card.

At each owner turn, every available candidate is scored by the MARGINAL
change in expected categories won per week:

    score(p) = Σ_c [ pwin_c(mine + p) − pwin_c(mine) ]

where pwin_c comes from the arena's own weekly model (`team_week_model` —
lineup-weighted means, full variance model, TO inverted) averaged against
the CURRENT PARTIAL opponent rosters. Strictly realizable: uses only
information the deck has at that turn (picks so far, live pool). No
foresight, no market model, no punt weighting.

This is the realizable version of the m28 oracle objective (LEDGER §5).
Ship bar (SEPTEMBER-PLAN E9): beat the composite card across ledger
replays WITHOUT regressing the winners m21/m24/m25/m26.

Usage: python3 decw_card.py <mock> [mock...]   (no args = all)
Writes decw_card_m<NN>.json next to this file's output dir (scratchpad if
present, else cwd): per-turn top-5 by ΔECW + the full score of the actual
pick, for grading and counterfactuals.
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

OUTDIR = os.environ.get(
    "DECW_OUT",
    "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad")
if not os.path.isdir(OUTDIR):
    OUTDIR = "."


def pwins(my_model, opp_models):
    """Average per-category win prob vs each opponent's weekly model."""
    out = {c: 0.0 for c in CATS}
    for om in opp_models:
        for c in CATS:
            ma, va = my_model[0][c], my_model[1][c]
            mb, vb = om[0][c], om[1][c]
            d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            out[c] += (1 - p) if c == "TO" else p
    n = len(opp_models) or 1
    return {c: out[c] / n for c in CATS}


def card_for(mock):
    fn, owner = MOCKS[mock]
    st = json.load(open(UP + fn))
    picks = st["picks"]
    turns = []
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
        base = sum(pwins(arena.team_week_model(mine), opp_models).values()) if mine and opp_models else 0.0
        scored = []
        for p in pool:
            m = arena.team_week_model(mine + [p])
            if opp_models:
                s = sum(pwins(m, opp_models).values()) - base
            else:
                # turn 1 with no opponents drafted yet: fall back to the
                # candidate's own weekly-model strength vs a par (empty) frame —
                # rank by lineup-weighted 9-cat z, the only realizable signal.
                s = sum(p["z"][c] for c in CATS)
            scored.append((s, p["player"]))
        scored.sort(reverse=True)
        turns.append({"pickNo": i + 1, "actual": pk["player"],
                      "top5": [{"n": n, "decw": round(s, 4)} for s, n in scored[:5]],
                      "actual_rank": next((k + 1 for k, (_, n) in enumerate(scored) if n == pk["player"]), None)})
    return turns


for m in [int(x) for x in sys.argv[1:]] or sorted(MOCKS):
    turns = card_for(m)
    path = os.path.join(OUTDIR, f"decw_card_m{m}.json")
    json.dump(turns, open(path, "w"), indent=1)
    hits = sum(1 for t in turns if t["top5"] and t["top5"][0]["n"] == t["actual"])
    print(f"m{m}: card written ({len(turns)} turns, owner matched ΔECW #1 on {hits})")
