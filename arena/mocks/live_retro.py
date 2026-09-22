#!/usr/bin/env python3
"""live_retro — retro analysis of a live mock draft on the deck plane
(generalized from mock51_retro.py, 2026-09-22; mock 51 reproduces from it).

    python3 arena/mocks/live_retro.py <mock> <stage>

Stages (each writes arena/results/m<mock>_<stage>.json):
  replay     card reconstruction at every owner turn on each configured pool
             — exact port of decwScores (check_parity), old name tie-break
             (the order the published deck used through v23)
  final      as-drafted final rosters: ECW, per-opp expected cats, category
             ranks (weekly model + z-sum), season-shape H2H (draft51 method)
  hindsight  per turn: every legal single-swap alternative, scored by ECW vs
             the FINAL rosters (pairwise swap when the alt was drafted later)
  forecast   the room-forecast experiment (mock 51 study)
  arms       Monte-Carlo season arms (CRN, 6000 seasons x seeds 11/23/47)

Poolless opponent picks (a live human drafted a name the deck's pool lacks)
are tolerated everywhere: that seat simulates with the men the pool has, and
the missing names are recorded in every output (mock 52: Daniss Jenkins,
Gui Santos — seats 4 and 11 play 12 men).
"""
import sys, os, json, math, random, argparse, statistics

DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SP = os.path.join(DECK, "arena", "results")
sys.path.insert(0, DECK + "/scripts")
sys.path.insert(0, DECK + "/arena")
import hoops  # noqa: E402
import arena  # noqa: E402  (its own hoops instance reads the frozen snapshot; unused here)

CATS = hoops.CATS
POOLS = {"v22": SP + "/m51_players_v22.csv", "v23": SP + "/m52_players_v23.csv", "v25": DECK + "/data/players.csv"}
# v23 = the 264-row pool mocks 51 (tuned replay) and 52 were drafted against
# (data pull 2026-09-21, players.csv md5 a1a1eda60f34; the live file grew to
# 330 rows on 2026-09-22, so it is regenerated from git like v22).
# v25 = data/players.csv as of the 2026-09-22 pool completion (mock 53).
V23_REV = "f724435"
# v22 = the pool the deck the owner drafted against in mock 51 was built from
# (data pull 2026-09-15, players.csv sha256 e3e17e279ea5); regenerated from git
# below, only for a mock whose config names it.
MOCKS = {
    # pools the owner drafted against ("v22" = the 9/15 pool, regenerated from
    # git; "v23" = data/players.csv as of the 9/21 pull, sha c1f87ac1db09)
    51: dict(tags=("v22", "v23"), v22_rev="e7aac6b53351f23fd2ef6c8b6c177fbccdcb428b"),
    52: dict(tags=("v23",)),
    53: dict(tags=("v25",)),
}
MOCK = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 51
CFG = MOCKS[MOCK]
TAGS = CFG["tags"]
GRADE_TAG = TAGS[-1]   # the pool the grading stages run on: the deck the owner drafted against (mock 53: v25)
STATE = DECK + f"/arena/data/states/draft_state_{MOCK}.json"
state = json.load(open(STATE, encoding="utf-8"))
TEAMS, SLOT, SIZE = state["teams"], state["slot"], state["size"]
PICKS = state["picks"]
assert len(PICKS) == TEAMS * SIZE, (len(PICKS), TEAMS, SIZE)
OWNER_IDX = [n for n in range(len(PICKS)) if hoops.team_of_pick(n, TEAMS) == SLOT]
assert len(OWNER_IDX) == SIZE and all(PICKS[n]["slot"] == SLOT for n in OWNER_IDX)
if "v22" in TAGS and not os.path.exists(POOLS["v22"]):
    import subprocess
    with open(POOLS["v22"], "w", encoding="utf-8") as _f:
        _f.write(subprocess.run(["git", "-C", DECK, "show", CFG["v22_rev"] + ":data/players.csv"],
                                capture_output=True, text=True, check=True).stdout)
if not os.path.exists(POOLS["v23"]):   # regenerated whenever missing — every mock's hindsight/forecast/arms may grade on it
    import subprocess
    with open(POOLS["v23"], "w", encoding="utf-8") as _f:
        _f.write(subprocess.run(["git", "-C", DECK, "show", V23_REV + ":data/players.csv"],
                                capture_output=True, text=True, check=True).stdout)
CAST = {s: nm for s, nm in state.get("cast", [])}


def load_pool(tag):
    hoops.DATA_PATH = POOLS[tag]
    return hoops.zscores(hoops.load_players())


def pct(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    den = (len(vals) - 1) or 1
    out = [0.0] * len(vals)
    for r, idx in enumerate(order):
        out[idx] = r / den
    return out


def pwin_cats(my, om):
    """P(win) per category for model `my` vs one opponent model `om`."""
    out = {}
    for c in CATS:
        d = (my[0][c] - om[0][c]) / (math.sqrt(my[1][c] + om[1][c]) or 1e-9)
        pr = 0.5 * (1 + math.erf(d / math.sqrt(2)))
        out[c] = (1 - pr) if c == "TO" else pr
    return out


def pwins(my, opps):
    """Expected categories won per week vs the average opponent (= ECW)."""
    if not opps:
        return 0.0
    return sum(sum(pwin_cats(my, om).values()) for om in opps) / len(opps)


def rosters_upto(players, upto):
    by = {p["player"]: p for p in players}
    ros, taken, missing = {s: [] for s in range(1, TEAMS + 1)}, set(), []
    for pk in PICKS[:upto]:
        taken.add(pk["player"])
        pl = by.get(pk["player"])
        if pl is None:
            missing.append(pk["player"])
            continue
        ros[pk["slot"]].append(pl)
    return ros, taken, missing


def avail_pool(players, taken):
    return [p for p in players if p["player"] not in taken and hoops.availability(p) > 0]


def card(players, upto):
    """Exact port of decwScores at the moment before pick index `upto`."""
    ros, taken, missing = rosters_upto(players, upto)
    mine = ros[SLOT]
    opp = [r for s, r in ros.items() if s != SLOT and r]
    pool = avail_pool(players, taken)
    vals = [hoops.adj_value(p, ()) for p in pool]
    models = [arena.team_week_model(r) for r in opp]
    if not models:
        decw = [None] * len(pool)
        ds = pct(vals)
    else:
        base = pwins(arena.team_week_model(mine), models) if mine else 0.0
        decw = [pwins(arena.team_week_model(mine + [p]), models) - base for p in pool]
        pd, pv = pct(decw), pct(vals)
        ds = [0.5 * pd[i] + 0.5 * pv[i] for i in range(len(pool))]
    order = sorted(range(len(pool)),
                   key=lambda i: (-ds[i], [-ord(ch) for ch in pool[i]["player"]]))
    vorder = sorted(range(len(pool)), key=lambda i: -vals[i])
    return dict(pool=pool, vals=vals, decw=decw, ds=ds, order=order, vorder=vorder,
                mine=mine, opp=opp, ros=ros, taken=taken, missing=missing)


def cat_ranks_zsum(ros):
    totals = {s: {c: sum(p["z"][c] for p in r) for c in CATS} for s, r in ros.items()}
    mine = totals[SLOT]
    return {c: 1 + sum(1 for s, t in totals.items() if s != SLOT and t[c] > mine[c])
            for c in CATS}


# ---------------------------------------------------------------- replay
def stage_replay():
    out = {}
    for tag in TAGS:
        players = load_pool(tag)
        byn = {p["player"]: p for p in players}
        turns = []
        for n in OWNER_IDX:
            c = card(players, n)
            actual = PICKS[n]["player"]
            pool_names = [p["player"] for p in c["pool"]]
            ai = pool_names.index(actual) if actual in pool_names else None
            top = []
            for rk, i in enumerate(c["order"][:8], 1):
                p = c["pool"][i]
                top.append(dict(rank=rk, n=p["player"], t=p["team"], pos=p["pos"],
                                ds=round(c["ds"][i], 4),
                                decw=(None if c["decw"][i] is None else round(c["decw"][i], 4)),
                                val=round(c["vals"][i], 3),
                                av=hoops.availability(p)))
            rec = dict(pick=n + 1, rnd=n // TEAMS + 1, actual=actual,
                       actual_in_pool=ai is not None, top=top,
                       n_pool=len(c["pool"]), n_opp_with_picks=len(c["opp"]),
                       missing_so_far=c["missing"])
            if ai is not None:
                rec.update(actual_ds_rank=c["order"].index(ai) + 1,
                           actual_val_rank=c["vorder"].index(ai) + 1,
                           actual_ds=round(c["ds"][ai], 4),
                           actual_decw=(None if c["decw"][ai] is None else round(c["decw"][ai], 4)),
                           actual_val=round(c["vals"][ai], 3),
                           top1_gap_ds=round(c["ds"][c["order"][0]] - c["ds"][ai], 4),
                           top1_gap_decw=(None if c["decw"][ai] is None else
                                          round(c["decw"][c["order"][0]] - c["decw"][ai], 4)))
                if c["decw"][ai] is not None:
                    dorder = sorted(range(len(c["pool"])), key=lambda i: -c["decw"][i])
                    rec["actual_decw_rank"] = dorder.index(ai) + 1
            if c["mine"]:
                rec["my_zsum_ranks"] = cat_ranks_zsum(c["ros"])
            # what each choice BUYS, category by category: mean over the
            # room's current rosters of the change in P(win cat)
            if c["opp"] and c["mine"]:
                models = [arena.team_week_model(r) for r in c["opp"]]
                m0 = arena.team_week_model(c["mine"])
                base_c = {k: statistics.mean(pwin_cats(m0, om)[k] for om in models) for k in CATS}
                rec["base_ecw_partial"] = round(sum(base_c.values()), 4)
                rec["base_cat_p"] = {k: round(v, 3) for k, v in base_c.items()}

                def buys(p):
                    m1 = arena.team_week_model(c["mine"] + [p])
                    return {k: round(statistics.mean(pwin_cats(m1, om)[k] for om in models) - base_c[k], 3)
                            for k in CATS}
                rec["card1_buys"] = buys(c["pool"][c["order"][0]])
                if ai is not None:
                    rec["actual_buys"] = buys(c["pool"][ai])
            turns.append(rec)
        out[tag] = turns
        # ---- print
        print(f"\n===== CARD REPLAY — pool {tag} ({len(players)} rows) =====")
        for t in turns:
            top5 = " | ".join(f"{x['n']} {x['ds']:.3f}" for x in t["top"][:5])
            if t["actual_in_pool"]:
                print(f"#{t['pick']:>3} R{t['rnd']:>2}  actual {t['actual']:<24} card#{t['actual_ds_rank']:>3} "
                      f"val#{t['actual_val_rank']:>3} decw#{t.get('actual_decw_rank', '-'):>3} "
                      f"ds {t['actual_ds']:.3f} (gap {t['top1_gap_ds']:.3f})")
            else:
                print(f"#{t['pick']:>3} R{t['rnd']:>2}  actual {t['actual']:<24} NOT IN POOL")
            print(f"        top5: {top5}")
    json.dump(out, open(SP + f"/m{MOCK}_replay.json", "w"), indent=1)
    return out


# ---------------------------------------------------------------- final
def season_shape(ros):
    """draft51/draft50 method on the deck plane: availability-weighted
    per-game sums, attempt-weighted percentages; per-category compare."""
    tot = {}
    for s, r in ros.items():
        t = {c: 0.0 for c in CATS}
        fga = fta = fgm = ftm = 0.0
        for p in r:
            a = hoops.availability(p)
            for c, col in hoops.COUNT_COLS.items():
                t[c] += a * p[col]
            fga += a * p["fga"]; fgm += a * p["fga"] * p["fg_pct"]
            fta += a * p["fta"]; ftm += a * p["fta"] * p["ft_pct"]
        t["FG%"] = fgm / (fga or 1); t["FT%"] = ftm / (fta or 1)
        tot[s] = t
    return tot


def stage_final():
    out = {}
    for tag in TAGS:
        players = load_pool(tag)
        ros, taken, missing = rosters_upto(players, len(PICKS))
        models = {s: arena.team_week_model(r) for s, r in ros.items()}
        ecw = {s: pwins(models[s], [models[o] for o in ros if o != s]) for s in ros}
        # per-category expected win prob vs field, per team -> rank
        catp = {s: {c: statistics.mean(pwin_cats(models[s], models[o])[c] for o in ros if o != s)
                    for c in CATS} for s in ros}
        cat_rank = {c: 1 + sum(1 for o in ros if o != SLOT and catp[o][c] > catp[SLOT][c]) for c in CATS}
        per_opp = {}
        for o in ros:
            if o == SLOT:
                continue
            pc = pwin_cats(models[SLOT], models[o])
            per_opp[o] = dict(name=CAST.get(o, f"T{o}"), exp_cats=round(sum(pc.values()), 3),
                              cats={c: round(v, 3) for c, v in pc.items()})
        ss = season_shape(ros)
        ss_rec = {}
        for o in ros:
            if o == SLOT:
                continue
            w = sum(1 for c in CATS
                    if ((ss[SLOT][c] < ss[o][c]) if c == "TO" else (ss[SLOT][c] > ss[o][c])))
            ss_rec[o] = w
        ss_rank = {c: 1 + sum(1 for o in ros if o != SLOT and
                              ((ss[o][c] < ss[SLOT][c]) if c == "TO" else (ss[o][c] > ss[SLOT][c])))
                   for c in CATS}
        zs = cat_ranks_zsum(ros)
        ecw_rank = 1 + sum(1 for o in ros if o != SLOT and ecw[o] > ecw[SLOT])
        out[tag] = dict(missing=missing, ecw={s: round(v, 4) for s, v in ecw.items()},
                        ecw_rank=ecw_rank, cat_rank_weekly=cat_rank, cat_rank_zsum=zs,
                        cat_rank_seasonshape=ss_rank, per_opp=per_opp,
                        seasonshape_wins={o: w for o, w in ss_rec.items()},
                        exp_winning_weeks=sum(1 for v in per_opp.values() if v["exp_cats"] > 4.5),
                        seasonshape_winning=sum(1 for w in ss_rec.values() if w >= 5),
                        roster=[p["player"] for p in ros[SLOT]])
        print(f"\n===== FINAL — pool {tag} =====  missing names: {missing}")
        print("ECW by seat:", {CAST.get(s, f'T{s}'): round(v, 3) for s, v in sorted(ecw.items(), key=lambda kv: -kv[1])})
        print(f"owner ECW {ecw[SLOT]:.3f} rank {ecw_rank}/12")
        print("cat rank (weekly pwin):", cat_rank)
        print("cat rank (z-sum):      ", zs)
        print("cat rank (season-shape):", ss_rank)
        print("per-opp expected cats:", {v['name']: v['exp_cats'] for v in per_opp.values()},
              "-> winning weeks", out[tag]["exp_winning_weeks"], "/ 11")
        print("season-shape H2H cats won:", {CAST.get(o, o): w for o, w in ss_rec.items()},
              "-> wins", out[tag]["seasonshape_winning"], "/ 11")
    json.dump(out, open(SP + f"/m{MOCK}_final.json", "w"), indent=1)
    return out


# ---------------------------------------------------------------- hindsight
def final_swap_eval(players, ros_final, n, alt, actual, order_idx):
    """ECW of the owner's FINAL roster with `alt` in place of `actual`
    (the pick at index n), pairwise-swapping when alt was drafted later."""
    byn = {p["player"]: p for p in players}
    mine = [p for p in ros_final[SLOT] if p["player"] != actual] + [byn[alt]]
    j = order_idx.get(alt)
    opp_models = {}
    for o, r in ros_final.items():
        if o == SLOT:
            continue
        rr = r
        if j is not None and PICKS[j]["slot"] == o:
            rr = [p for p in r if p["player"] != alt] + [byn[actual]]
        opp_models[o] = arena.team_week_model(rr)
    my = arena.team_week_model(mine)
    per = {o: sum(pwin_cats(my, om).values()) for o, om in opp_models.items()}
    return statistics.mean(per.values()), sum(1 for v in per.values() if v > 4.5)


def stage_hindsight(tag=None):
    tag = tag or GRADE_TAG
    players = load_pool(tag)
    byn = {p["player"]: p for p in players}
    ros_final, _, missing = rosters_upto(players, len(PICKS))
    if missing:
        print(f"poolless opponent picks (their seats play short): {missing}")
    order_idx = {pk["player"]: i for i, pk in enumerate(PICKS)}
    owner_later = set()
    base_models = {o: arena.team_week_model(r) for o, r in ros_final.items() if o != SLOT}
    my0 = arena.team_week_model(ros_final[SLOT])
    per0 = {o: sum(pwin_cats(my0, om).values()) for o, om in base_models.items()}
    base_ecw, base_w = statistics.mean(per0.values()), sum(1 for v in per0.values() if v > 4.5)
    print(f"as-drafted ({tag}): ECW {base_ecw:.4f}, winning weeks {base_w}/11")
    replay = json.load(open(SP + f"/m{MOCK}_replay.json"))
    cards = {t["pick"]: t for t in replay[tag]}
    cards22 = {t["pick"]: t for t in replay.get("v22", [])}
    out = dict(base_ecw=base_ecw, base_w=base_w, turns=[])
    for n in OWNER_IDX:
        actual = PICKS[n]["player"]
        c = card(players, n)
        owner_later = {PICKS[m]["player"] for m in OWNER_IDX if m > n}
        rows = []
        for i, p in enumerate(c["pool"]):
            nm = p["player"]
            if nm == actual or nm in owner_later:
                continue
            e, w = final_swap_eval(players, ros_final, n, nm, actual, order_idx)
            j = order_idx.get(nm)
            rows.append(dict(n=nm, t=p["team"], pos=p["pos"], ecw=round(e, 4),
                             gain=round(e - base_ecw, 4), wins=w,
                             drafted_at=(None if j is None else j + 1),
                             drafted_by=(None if j is None else CAST.get(PICKS[j]["slot"], f"T{PICKS[j]['slot']}")),
                             card_rank=c["order"].index(i) + 1,
                             val_rank=c["vorder"].index(i) + 1,
                             card_rank_v22=next((x["rank"] for x in cards22.get(n + 1, {"top": []})["top"] if x["n"] == nm), None)))
        rows.sort(key=lambda r: -r["gain"])
        n_better = sum(1 for r in rows if r["gain"] > 0)
        top = rows[:6]
        # where did the card's #1 (v23) land in hindsight?
        card1 = c["pool"][c["order"][0]]["player"]
        c1 = next((r for r in rows if r["n"] == card1), None)
        rec = dict(pick=n + 1, actual=actual, n_legal=len(rows), n_better=n_better,
                   actual_hindsight_rank=(n_better + 1), top=top,
                   card1=card1, card1_gain=(None if c1 is None else c1["gain"]),
                   card1_wins=(None if c1 is None else c1["wins"]))
        out["turns"].append(rec)
        print(f"\n#{n + 1:>3} actual {actual:<22} better-in-hindsight: {n_better:>3}/{len(rows)}  "
              f"card#1 {card1} gain {rec['card1_gain']}")
        for r in top:
            print(f"      {r['n']:<24} {r['pos']:<6} gain {r['gain']:+.4f} wins {r['wins']:>2}  "
                  f"card#{r['card_rank']:>3} val#{r['val_rank']:>3} v22card#{r['card_rank_v22']}  "
                  f"drafted {r['drafted_at']} by {r['drafted_by']}")
    json.dump(out, open(SP + f"/m{MOCK}_hindsight.json", "w"), indent=1)
    return out


# ---------------------------------------------------------------- forecast
def simulate_rest(players, upto, rng, owner_strategy="bpa_pure"):
    """Finish the draft from pick index `upto` with arena personas:
    opponents = 'market' (ADP-anchored + noise), owner = bpa_pure."""
    ros, taken, _ = rosters_upto(players, upto)
    pool_master = [p for p in players if hoops.availability(p) > 0]
    mkt = arena.market_ranks(pool_master)
    pool = [p for p in pool_master if p["player"] not in taken]
    for n in range(upto, TEAMS * SIZE):
        s = hoops.team_of_pick(n, TEAMS)
        name = owner_strategy if s == SLOT else "market"
        params = arena.strategy_params(name)
        p = arena.pick_for(params, pool, ros[s], None, n // TEAMS + 1, rng, mkt=mkt)
        ros[s].append(p)
        pool.remove(p)
    return ros


def spearman(a, b):
    n = len(a)
    ra = pct(a); rb = pct(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) or 1e-9
    return num / den


def stage_forecast(tag=None, K=12):
    tag = tag or GRADE_TAG
    players = load_pool(tag)
    hs = json.load(open(SP + f"/m{MOCK}_hindsight.json"))
    hs_turns = {t["pick"]: t for t in hs["turns"]}
    ros_final, _, _ = rosters_upto(players, len(PICKS))
    order_idx = {pk["player"]: i for i, pk in enumerate(PICKS)}
    final_opp = [arena.team_week_model(r) for o, r in ros_final.items() if o != SLOT]
    out = []
    for n in OWNER_IDX:
        actual = PICKS[n]["player"]
        c = card(players, n)
        owner_later = {PICKS[m]["player"] for m in OWNER_IDX if m > n}
        # forecast opponent final rosters
        draws = []
        for k in range(K):
            rng = random.Random(1000 * (n + 1) + k)
            r = simulate_rest(players, n, rng)
            draws.append({o: rr for o, rr in r.items() if o != SLOT})
        draw_models = [{o: arena.team_week_model(rr) for o, rr in d.items()} for d in draws]
        draw_names = [{o: {q["player"] for q in rr} for o, rr in d.items()} for d in draws]
        base_f = 0.0
        if c["mine"]:
            mm = arena.team_week_model(c["mine"])
            base_f = statistics.mean(pwins(mm, list(dm.values())) for dm in draw_models)
        # candidate evaluation restricted to the top-40 by value (the card's visible shelf)
        cand = [i for i in c["vorder"][:40]
                if c["pool"][i]["player"] != actual and c["pool"][i]["player"] not in owner_later]
        # hindsight gain (from stage hindsight) for these candidates
        hgain = {}
        for i in cand:
            nm = c["pool"][i]["player"]
            e, _ = final_swap_eval(players, ros_final, n, nm, actual, order_idx)
            hgain[nm] = e - hs["base_ecw"]
        f_decw, o_decw, p_decw = {}, {}, {}
        for i in cand:
            p = c["pool"][i]; nm = p["player"]
            mm = arena.team_week_model(c["mine"] + [p])
            # forecast: drop the candidate from any simulated opp roster that took him
            vals = []
            for d, dm, dn in zip(draws, draw_models, draw_names):
                oms = [dm[o] if nm not in dn[o]
                       else arena.team_week_model([q for q in d[o] if q["player"] != nm])
                       for o in d]
                vals.append(pwins(mm, oms))
            f_decw[nm] = statistics.mean(vals) - base_f
            o_decw[nm] = pwins(mm, final_opp) - (pwins(arena.team_week_model(c["mine"]), final_opp) if c["mine"] else 0.0)
            p_decw[nm] = (c["decw"][i] if c["decw"][i] is not None else 0.0)
        vals_c = {c["pool"][i]["player"]: c["vals"][i] for i in cand}
        names = list(vals_c)
        pv = dict(zip(names, pct([vals_c[x] for x in names])))

        def blend(d):
            pd = dict(zip(names, pct([d[x] for x in names])))
            return {x: 0.5 * pd[x] + 0.5 * pv[x] for x in names}
        orders = {"shipped(partial)": blend(p_decw), "forecast": blend(f_decw), "oracle(final)": blend(o_decw),
                  "value-only": {x: pv[x] for x in names}}
        rec = dict(pick=n + 1, actual=actual, actual_hgain=round(hgain.get(actual, 0.0), 4))
        for lab, sc in orders.items():
            top = sorted(names, key=lambda x: -sc[x])
            rec[lab] = dict(top1=top[0], top1_hgain=round(hgain[top[0]], 4),
                            top5_mean_hgain=round(statistics.mean(hgain[x] for x in top[:5]), 4),
                            rho=round(spearman([sc[x] for x in names], [hgain[x] for x in names]), 3))
        out.append(rec)
        print(f"#{n + 1:>3} {actual:<22} " + "  ".join(
            f"{lab}: #1 {rec[lab]['top1']} ({rec[lab]['top1_hgain']:+.3f}) rho {rec[lab]['rho']:+.2f}"
            for lab in orders))
    json.dump(out, open(SP + f"/m{MOCK}_forecast.json", "w"), indent=1)
    return out


# ---------------------------------------------------------------- arms
def run_arm(rosters, seeds=(11, 23, 47), seasons=6000):
    champs = {s: 0 for s in rosters}; plays = {s: 0 for s in rosters}
    for sd in seeds:
        rng = random.Random(sd)
        c, p = arena.simulate_seasons(rosters, seasons, rng)
        for s in rosters:
            champs[s] += c[s]; plays[s] += p[s]
    tot = seasons * len(seeds)
    return {s: (100 * champs[s] / tot, 100 * plays[s] / tot) for s in rosters}


def apply_swaps(players, swaps):
    """swaps: list of (owner_pick_index n, alt_name). Pairwise on the running
    board; returns final rosters."""
    byn = {p["player"]: p for p in players}
    picks = [dict(pk) for pk in PICKS]
    order_idx = {pk["player"]: i for i, pk in enumerate(picks)}
    for n, alt in swaps:
        actual = picks[n]["player"]
        j = order_idx.get(alt)
        picks[n]["player"] = alt
        if j is not None:
            picks[j]["player"] = actual
            order_idx[actual] = j
        else:
            order_idx.pop(actual, None)
        order_idx[alt] = n
    ros = {s: [] for s in range(1, TEAMS + 1)}
    for pk in picks:
        if pk["player"] in byn:
            ros[pk["slot"]].append(byn[pk["player"]])
    return ros, picks


def stage_arms(tag=None):
    tag = tag or GRADE_TAG
    players = load_pool(tag)
    hs = json.load(open(SP + f"/m{MOCK}_hindsight.json"))
    arms = {"as_drafted": []}
    # single best hindsight swap per turn (positive gain only)
    for t in hs["turns"]:
        if t["top"] and t["top"][0]["gain"] > 0:
            arms[f"swap#{t['pick']}:{t['top'][0]['n']}"] = [(t["pick"] - 1, t["top"][0]["n"])]
    # follow the shipped card #1 at every turn, SELF-CONSISTENT, strict pairwise
    picks_run = [dict(pk) for pk in PICKS]
    swaps = []
    byn = {p["player"]: p for p in players}
    for n in OWNER_IDX:
        # running board
        taken = {pk["player"] for pk in picks_run[:n]}
        ros = {s: [] for s in range(1, TEAMS + 1)}
        for pk in picks_run[:n]:
            if pk["player"] in byn:
                ros[pk["slot"]].append(byn[pk["player"]])
        mine = ros[SLOT]; opp = [r for s, r in ros.items() if s != SLOT and r]
        pool = [p for p in players if p["player"] not in taken and hoops.availability(p) > 0]
        vals = [hoops.adj_value(p, ()) for p in pool]
        models = [arena.team_week_model(r) for r in opp]
        if not models:
            ds = pct(vals)
        else:
            base = pwins(arena.team_week_model(mine), models) if mine else 0.0
            decw = [pwins(arena.team_week_model(mine + [p]), models) - base for p in pool]
            pd, pv = pct(decw), pct(vals)
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
            if j is not None and picks_run[j]["slot"] != SLOT:
                chosen = (nm, j); break
        if chosen:
            nm, j = chosen
            picks_run[n]["player"], picks_run[j]["player"] = nm, actual
            swaps.append((n, nm))
    arms["follow_card_selfconsistent"] = swaps
    # cumulative hindsight: greedy sequential, accept a turn's best swap if it still improves
    results = {}
    for name, sw in arms.items():
        ros, _ = apply_swaps(players, sw)
        res = run_arm(ros)
        me = res[SLOT]
        rank = 1 + sum(1 for s in ros if s != SLOT and res[s][0] > me[0])
        results[name] = dict(champ=round(me[0], 3), playoff=round(me[1], 2), champ_rank=rank,
                             swaps=[(n + 1, a) for n, a in sw])
        print(f"{name:<40} champ {me[0]:6.3f}%  playoff {me[1]:5.2f}%  rank {rank}/12  swaps {results[name]['swaps']}")
        json.dump(results, open(SP + f"/m{MOCK}_arms.json", "w"), indent=1)
    return results


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mock", type=int, choices=sorted(MOCKS))
    ap.add_argument("stage", choices=["replay", "final", "hindsight", "forecast", "arms"])
    a = ap.parse_args()
    {"replay": stage_replay, "final": stage_final, "hindsight": stage_hindsight,
     "forecast": stage_forecast, "arms": stage_arms}[a.stage]()
