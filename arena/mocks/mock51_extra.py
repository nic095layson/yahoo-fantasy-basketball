#!/usr/bin/env python3
"""Supplementary measurements for the mock-51 retro:
  A. survival-chip calibration on THIS room (predicted vs realized)
  B. exact blend ties at the top of the card (alphabetical 🎯)
  C. Embiid at #58 in hindsight (the v23 urgent TARGET pin)
  D. punt-advisor replay: drift detection + coherence-strip retarget vs the
     room-relative rank of the category it proposes to punt
  E. Yahoo-ADP survival alternative (kit consensus file) on the same rows
"""
import sys, os, json, math, csv, statistics
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
import mock51_retro as R
hoops, arena = R.hoops, R.arena
CATS = R.CATS
PICKS = R.PICKS
OWNER_IDX = R.OWNER_IDX

def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---------------------------------------------------------------- A
print("===== A. SURVIVAL CHIP CALIBRATION — v22 card rows vs what the room did =====")
dc = json.load(open(SP + "/m51_deckcard_v22.json"))
obs = []
for t in dc:
    if not t["nextTurn"]:
        continue
    between = {pk["player"] for pk in PICKS[t["pick"]: t["nextTurn"] - 1]}  # picks strictly between
    for r in t["rows"]:
        if r["n"] == t["actual"] or r["surv"] is None:
            continue
        alive = r["n"] not in between
        obs.append(dict(pick=t["pick"], n=r["n"], pred=r["surv"], alive=alive, chip=r["chip"], mkt=r["mkt"], val=r["valRank"]))
n = len(obs); alive = sum(o["alive"] for o in obs)
brier = statistics.mean((o["pred"] - (1 if o["alive"] else 0)) ** 2 for o in obs)
print(f"rows scored: {n}; mean predicted survival {statistics.mean(o['pred'] for o in obs):.3f}; realized survival {alive}/{n} = {alive/n:.3f}; Brier {brier:.3f}")
for chip in ("BUY NOW", "TOSS-UP", None):
    sub = [o for o in obs if o["chip"] == chip]
    if sub:
        print(f"  chip {str(chip):<8}: n={len(sub):>2} mean pred {statistics.mean(o['pred'] for o in sub):.3f}  realized alive {sum(o['alive'] for o in sub)}/{len(sub)}")
print("  survivors the model called ≤2%:", [f"#{o['pick']} {o['n']} (pred {o['pred']:.2f})" for o in obs if o["alive"] and o["pred"] <= 0.02])

# ---------------------------------------------------------------- B
print("\n===== B. EXACT TIES AT THE TOP OF THE CARD (🎯 decided by the name tie-break) =====")
rep = json.load(open(SP + "/m51_replay.json"))
for tag in ("v22", "v23"):
    ties = []
    for t in rep[tag]:
        top = t["top"]
        tied = [x["n"] for x in top if abs(x["ds"] - top[0]["ds"]) < 5e-5]
        if len(tied) > 1:
            ties.append((t["pick"], tied, t["actual"]))
    print(f"{tag}: {len(ties)} of 13 turns tied at #1 →", "; ".join(f"#{p}: {' = '.join(tt)} (took {a})" for p, tt, a in ties))

# ---------------------------------------------------------------- C
print("\n===== C. EMBIID AT #58 (v23 urgent TARGET pin) — hindsight =====")
players = R.load_pool("v23")
ros_final, _, _ = R.rosters_upto(players, len(PICKS))
order_idx = {pk["player"]: i for i, pk in enumerate(PICKS)}
hs = json.load(open(SP + "/m51_hindsight.json"))
n58 = OWNER_IDX[4]
assert PICKS[n58]["player"] == "OG Anunoby"
for alt in ("Joel Embiid", "Myles Turner", "Payton Pritchard"):
    e, w = R.final_swap_eval(players, ros_final, n58, alt, "OG Anunoby", order_idx)
    byn = {p["player"]: p for p in players}
    print(f"  {alt:<18} av {hoops.availability(byn[alt])}  note {byn[alt].get('note')!r:<40} ECW {e:.4f} (gain {e - hs['base_ecw']:+.4f}) wins {w}/11")

# ---------------------------------------------------------------- D
print("\n===== D. PUNT ADVISOR REPLAY (v22 pool) — drift/FULL TILT gate and coherence retarget vs room-relative rank =====")
players22 = R.load_pool("v22")
PUNT_TIMELINE = [(0, []), (46, ["AST", "FT%"]), (52, ["FT%", "TO"]), (63, ["TO", "FG%"]), (111, ["TO", "AST"])]
lostFrom = 12 - max(1, round(12 / 4)) + 1
thresh = max(2, round(12 / 3))
for n in OWNER_IDX:
    ros, taken, _ = R.rosters_upto(players22, n)
    mine = ros[R.SLOT]
    if len(mine) < 2:
        continue
    ranks = R.cat_ranks_zsum(ros)
    # weekly-model (room-relative) category standing at this moment
    opp = [r for s, r in ros.items() if s != R.SLOT and r]
    models = [arena.team_week_model(r) for r in opp]
    m0 = arena.team_week_model(mine)
    catp = {c: statistics.mean(R.pwin_cats(m0, om)[c] for om in models) for c in CATS}
    punt = []
    for after, p in PUNT_TIMELINE:
        if n >= after:
            punt = p
    kept = [c for c in CATS if c not in punt]
    line = f"#{n + 1:>3} roster {len(mine):>2} punt={punt} zsum-ranks " + " ".join(f"{c}:{ranks[c]}" for c in CATS)
    if not punt and len(mine) >= 4:
        drift = sorted([c for c in kept if ranks[c] >= lostFrom], key=lambda c: -ranks[c])[:3]
        if drift:
            firm = len(drift) >= 2 or ranks[drift[0]] >= 12
            keptAfter = [c for c in kept if c not in drift]
            winnable = [c for c in keptAfter if ranks[c] <= thresh]
            clear = (len(winnable) / len(keptAfter) if keptAfter else 0) >= 0.7
            line += f"\n       drift {drift} firm={firm} winnable {winnable} ({len(winnable)}/{len(keptAfter)}) clear={clear} → FULL TILT button {'SHOWN' if firm and clear else 'hidden'}"
    if punt and len(mine) >= 3:
        keptsum = lambda ps: sum(sum(q["z"][c] for c in CATS if c not in set(ps)) for q in mine)
        declared = keptsum(punt)
        best = None
        for out in punt:
            for inn in [c for c in CATS if c not in punt]:
                alt = [c for c in punt if c != out] + [inn]
                v = keptsum(alt)
                if best is None or v > best[1]:
                    best = (alt, v, out, inn)
        delta = best[1] - declared
        state = "inverted" if delta > 2 else "drifting" if delta > 0.75 else "aligned"
        line += (f"\n       coherence: declared fit {declared:+.1f}; best alt punt {best[0]} fit {best[1]:+.1f} (+{delta:.1f}) → {state.upper()}"
                 f" — proposes punting {best[3]!r} whose room-relative weekly P(win) is {catp[best[3]]:.2f} (z-sum rank {ranks[best[3]]})")
    line += "\n       weekly P(win) by cat: " + " ".join(f"{c}:{catp[c]:.2f}" for c in CATS)
    print(line)

# ---------------------------------------------------------------- E
print("\n===== E. YAHOO-ADP SURVIVAL ALTERNATIVE (kit consensus 2026-09-15) =====")
path = os.path.join(os.environ.get("KIT_REPO", os.path.join(R.DECK, "..", "fantasy-basketball-2026-27")),
                    "report", "market", "consensus-2026-09-15.csv")  # kit plane: Yahoo 9/15 consensus
rows = list(csv.DictReader(open(path, encoding="utf-8")))
cols = rows[0].keys()
name_col = next(c for c in cols if "name" in c.lower() or "player" in c.lower())
adp_col = next((c for c in cols if "adp" in c.lower()), None)
print("columns:", list(cols), "| using", name_col, adp_col)
adp = {}
for r in rows:
    try:
        v = float(r[adp_col])
    except (TypeError, ValueError):
        continue
    adp[hoops.fold(r[name_col])] = v
matched = [(i + 1, pk["player"], adp.get(hoops.fold(pk["player"]))) for i, pk in enumerate(PICKS)]
have = [(i, nm, a) for i, nm, a in matched if a is not None]
print(f"picks with a Yahoo ADP: {len(have)}/156; unmatched sample: {[nm for i, nm, a in matched if a is None][:12]}")
resid = [i - a for i, nm, a in have]
sig = statistics.pstdev(resid)
print(f"pick − ADP: mean {statistics.mean(resid):+.1f}, sd {sig:.1f}, median {statistics.median(resid):+.1f}; sd by round third: "
      + ", ".join(f"picks {lo}-{hi}: {statistics.pstdev([i - a for i, nm, a in have if lo <= i <= hi]):.1f}" for lo, hi in ((1, 52), (53, 104), (105, 156))))
# ADP-only survival on the same v22 top-5 rows: P(alive at N) = Φ((ADP − N)/σ), σ = max(8, 0.20·ADP) (deck's own σ rule) and σ = fitted sd
for label, sfun in (("deck σ rule", lambda a: max(8, 0.20 * a)), ("fitted sd", lambda a: sig)):
    preds = []
    for o in obs:
        a = adp.get(hoops.fold(o["n"]))
        nxt = next(t["nextTurn"] for t in dc if t["pick"] == o["pick"])
        p = phi((a - nxt) / sfun(a)) if a is not None else 0.95
        preds.append((p, o["alive"]))
    br = statistics.mean((p - (1 if al else 0)) ** 2 for p, al in preds)
    quiet = [(p, al) for p, al in preds if p >= 0.40]; buy = [(p, al) for p, al in preds if p <= 0.20]
    print(f"  ADP model ({label}): Brier {br:.3f} (shipped {brier:.3f}); mean pred {statistics.mean(p for p, _ in preds):.3f}; "
          f"quiet(p≥.40) n={len(quiet)} alive {sum(al for _, al in quiet)}; BUY(p≤.20) n={len(buy)} gone {sum(not al for _, al in buy)}")
print("  rows where ADP says quiet but the deck said BUY NOW, and the player DID survive:",
      [f"#{o['pick']} {o['n']} ADP {adp.get(hoops.fold(o['n']))}" for o in obs if o["alive"] and (adp.get(hoops.fold(o["n"])) or 0) >= next(t["nextTurn"] for t in dc if t["pick"] == o["pick"]) + 8][:12])
