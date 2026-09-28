#!/usr/bin/env python3
"""D54-3 (2026-09-28): paired championship arms for a DECLARED punt on a live room.

    python3 arena/mocks/punt_arms.py <mock> <from_pick> <CAT[,CAT]> [--veto]

--veto applies the deck's JUDGMENT.doNotDraft list to the owner's candidates
(the card as it reads after PR #45); without it the arms replay the pre-veto
card the room was drafted against.

Three arms on the room as it happened, seasons by CRN (6000 x seeds 11/23/47):
  as_drafted                     the owner's actual roster
  follow_card_from<N>            from pick N on, take the card's #1 (blend50 over
                                 balanced value + ΔECW on all nine cats), strict
                                 pairwise swaps — the follow-card rule
  follow_card_from<N>_punt<CATS> the same, but the card is punt-STEERED: value and
                                 ΔECW over the kept categories only (the E20 ordering)

Registered bar (before running): the steered arm must beat the unsteered arm by
>= 2.0 championship points on >= 2 of 3 seeds for the advisor to stop being
advice-only. Per-seed results are recorded so the bar is checkable.
"""
import sys, os, json, random
MOCK = int(sys.argv[1]); FROM = int(sys.argv[2])
PUNT = tuple(c for c in (sys.argv[3].split(",") if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else []) if c)
VETO_ON = "--veto" in sys.argv
_argv = sys.argv; sys.argv = ["live_retro.py", str(MOCK)]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import live_retro as LR  # noqa: E402  (module-level setup: state, pools)
sys.argv = _argv
hoops, arena = LR.hoops, LR.arena
players = LR.load_pool(LR.GRADE_TAG)
VETO = hoops.do_not_draft() if VETO_ON else set()
CATS = hoops.CATS
SEEDS = (11, 23, 47); SEASONS = 6000


def pwins_kept(my, opps, kept):
    if not opps:
        return 0.0
    return sum(sum(v for c, v in LR.pwin_cats(my, om).items() if c in kept) for om in opps) / len(opps)


def follow_card(from_pick, punt):
    kept = [c for c in CATS if c not in punt]
    picks_run = [dict(pk) for pk in LR.PICKS]
    byn = {p["player"]: p for p in players}
    swaps = []
    for n in LR.OWNER_IDX:
        if n + 1 < from_pick:
            continue
        taken = {pk["player"] for pk in picks_run[:n]}
        ros = {s: [] for s in range(1, LR.TEAMS + 1)}
        for pk in picks_run[:n]:
            if pk["player"] in byn:
                ros[pk["slot"]].append(byn[pk["player"]])
        mine = ros[LR.SLOT]; opp = [r for s, r in ros.items() if s != LR.SLOT and r]
        pool = [p for p in players if p["player"] not in taken and hoops.availability(p) > 0
                and p["player"] not in VETO]
        vals = [hoops.adj_value(p, punt) for p in pool]
        models = [arena.team_week_model(r) for r in opp]
        if not models:
            ds = LR.pct(vals)
        else:
            base = pwins_kept(arena.team_week_model(mine), models, kept) if mine else 0.0
            decw = [pwins_kept(arena.team_week_model(mine + [p]), models, kept) - base for p in pool]
            pd, pv = LR.pct(decw), LR.pct(vals)
            ds = [0.5 * pd[i] + 0.5 * pv[i] for i in range(len(pool))]
        order = sorted(range(len(pool)), key=lambda i: (-ds[i], [-ord(ch) for ch in pool[i]["player"]]))
        actual = picks_run[n]["player"]
        later = {pk["player"]: j for j, pk in enumerate(picks_run) if j > n}
        chosen = None
        for i in order[:5]:
            nm = pool[i]["player"]
            if nm == actual:
                chosen = None; break
            j = later.get(nm)
            if j is not None and picks_run[j]["slot"] != LR.SLOT:
                chosen = (nm, j); break
        if chosen:
            nm, j = chosen
            picks_run[n]["player"], picks_run[j]["player"] = nm, actual
            swaps.append((n, nm))
    return swaps


def run_arm_seeds(rosters):
    per = {}
    for sd in SEEDS:
        rng = random.Random(sd)
        c, p = arena.simulate_seasons(rosters, SEASONS, rng)
        per[sd] = (100 * c[LR.SLOT] / SEASONS, 100 * p[LR.SLOT] / SEASONS)
    return per


arms = {"as_drafted": [],
        f"follow_card_from{FROM}": follow_card(FROM, ()),
        f"follow_card_from{FROM}_punt{'+'.join(PUNT)}": follow_card(FROM, PUNT)}
results = {}
for name, sw in arms.items():
    ros, _ = LR.apply_swaps(players, sw)
    per = run_arm_seeds(ros)
    champ = sum(v[0] for v in per.values()) / len(per); play = sum(v[1] for v in per.values()) / len(per)
    results[name] = dict(champ=round(champ, 3), playoff=round(play, 2), per_seed={str(k): round(v[0], 3) for k, v in per.items()},
                         swaps=[(n + 1, a) for n, a in sw])
    print(f"{name:<40} champ {champ:6.3f}%  playoff {play:5.2f}%  per-seed {results[name]['per_seed']}  swaps {results[name]['swaps']}")
un, st = results[f"follow_card_from{FROM}"], results[f"follow_card_from{FROM}_punt{'+'.join(PUNT)}"]
wins = sum(1 for sd in st["per_seed"] if st["per_seed"][sd] - un["per_seed"][sd] >= 2.0)
verdict = {"bar": "steered beats unsteered by >= 2.0 pp on >= 2 of 3 seeds", "seeds_meeting_bar": wins,
           "steered_minus_unsteered_pp": round(st["champ"] - un["champ"], 3), "passes": wins >= 2}
print("VERDICT:", json.dumps(verdict))
json.dump({"mock": MOCK, "from_pick": FROM, "punt": list(PUNT), "veto": sorted(VETO), "arms": results, "verdict": verdict},
          open(LR.SP + f"/m{MOCK}_punt_arms{'_veto' if VETO_ON else ''}.json", "w"), indent=1)
