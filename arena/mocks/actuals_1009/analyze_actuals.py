#!/usr/bin/env python3
"""Analyses on the verified actuals (OUT/actuals_<season>.csv):
 (i)   year-over-year category stability, three transitions, players with 25+ games in both seasons;
 (ii)  the 2025-26 entering pool (arena/data/players_2025-10-21.csv) scored against the verified 2025-26 actual:
       ENTERING line vs PRIOR (2024-25) vs M3 (5/4/3 games-weighted 2024-25/2023-24/2022-23) vs BLEND (½ entering + ½ M3);
 (iii) games-played history 2023-24..2025-26 for the current deck pool -> OUT/gp_history_2026-27.csv;
 (iv)  the points identity on the actual lines (rounding noise behind the 1.0 threshold);
 (v)   the M3 reference line (5/4/3 over 2025-26/2024-25/2023-24) for the current deck pool -> OUT/baseline3_2026-27.csv.
Usage: analyze_actuals.py OUT ENTERING_POOL DECK_POOL -> OUT/analysis_summary.json"""
import csv, json, math, os, statistics, sys, unicodedata
OUT, ENTER, DECK = sys.argv[1:4]
CATS = ["fg_pct", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v"}
def fold(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = s.replace(".", "").replace("'", "").replace("’", "").replace("-", " ").lower()
    return " ".join(t for t in s.split() if t not in SUFFIX)
def key3(f):
    t = f.split(); return (t[-1], t[0][:3]) if len(t) >= 2 else (f, "")
def load_actuals(season):
    rows = list(csv.DictReader(open(os.path.join(OUT, f"actuals_{season}.csv"), encoding="utf-8")))
    byf = {}; by3 = {}
    for r in rows:
        for k in ("gp",): r[k] = int(r[k])
        for k in ["mpg", "fga", "fgm", "fta", "ftm", "tpm", "pts", "reb", "ast", "stl", "blk", "tov", "fg_pct", "ft_pct"]: r[k] = float(r[k])
        byf.setdefault(fold(r["player"]), []).append(r); by3.setdefault(key3(fold(r["player"])), []).append(r)
    return rows, byf, by3
def find(name, byf, by3):
    f = fold(name)
    if f in byf and len(byf[f]) == 1: return byf[f][0]
    k = key3(f)
    if k in by3 and len(by3[k]) == 1: return by3[k][0]
    return None
def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]: j += 1
        for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def pearson(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")
def spearman(x, y): return pearson(ranks(x), ranks(y))
A = {s: load_actuals(s) for s in ["2022-23", "2023-24", "2024-25", "2025-26"]}
summary = {}
# (i) stability
stab = {}
for s0, s1 in [("2022-23", "2023-24"), ("2023-24", "2024-25"), ("2024-25", "2025-26")]:
    rows1, byf1, by31 = A[s1]; pairs = []
    for r in A[s0][0]:
        if r["gp"] < 25: continue
        q = find(r["player"], byf1, by31)
        if q and q["gp"] >= 25: pairs.append((r, q))
    st = {}
    for c in CATS:
        x = [p[c] for p, _ in pairs]; y = [q[c] for _, q in pairs]
        sd = statistics.pstdev(x); mad = statistics.mean(abs(a - b) for a, b in zip(x, y))
        st[c] = {"spearman": round(spearman(x, y), 3), "pearson": round(pearson(x, y), 3), "mean_abs_change_over_sd": round(mad / sd, 3) if sd else None}
    stab[f"{s0}->{s1}"] = {"n": len(pairs), "cats": st}
avg = {c: round(statistics.mean(stab[t]["cats"][c]["spearman"] for t in stab), 3) for c in CATS}
summary["stability"] = {"transitions": stab, "mean_spearman": avg, "least_stable_order": sorted(CATS, key=lambda c: avg[c])}
# (ii) backtest of the entering pool
def m3(name, seasons, weights):
    """games-weighted average of per-game stats over the seasons found; pct from weighted makes/attempts."""
    acc = {c: 0.0 for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov", "fga", "fgm", "fta", "ftm"]}; wsum = 0.0; used = []
    for s, w in zip(seasons, weights):
        rows, byf, by3 = A[s]; r = find(name, byf, by3)
        if not r or r["gp"] == 0: continue
        ww = w * r["gp"]; wsum += ww; used.append(f"{s}:{r['gp']}")
        for c in acc: acc[c] += ww * r[c]
    if not wsum: return None, used
    line = {c: acc[c] / wsum for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]}
    line["fg_pct"] = acc["fgm"] / acc["fga"] if acc["fga"] else 0.0; line["ft_pct"] = acc["ftm"] / acc["fta"] if acc["fta"] else 0.0
    return line, used
entering = list(csv.DictReader(open(ENTER, encoding="utf-8")))
rows26, byf26, by326 = A["2025-26"]
arms = {"ENTERING": {}, "PRIOR": {}, "M3": {}, "BLEND": {}}; actual = {}; n_scored = 0; miss_prior = 0
for e in entering:
    q = find(e["player"], byf26, by326)
    if not q or q["gp"] < 25: continue
    ent = {c: float(e[c]) for c in CATS}
    prior, _ = m3(e["player"], ["2024-25"], [1])
    three, used = m3(e["player"], ["2024-25", "2023-24", "2022-23"], [5, 4, 3])
    if not prior or not three: miss_prior += 1; continue
    n_scored += 1; actual[e["player"]] = q
    arms["ENTERING"][e["player"]] = ent; arms["PRIOR"][e["player"]] = prior; arms["M3"][e["player"]] = three
    arms["BLEND"][e["player"]] = {c: 0.5 * ent[c] + 0.5 * three[c] for c in CATS}
bt = {}
for arm, lines in arms.items():
    per = {}
    for c in CATS:
        names = list(lines); x = [lines[n][c] for n in names]; y = [actual[n][c] for n in names]
        per[c] = {"mae": round(statistics.mean(abs(a - b) for a, b in zip(x, y)), 4), "spearman": round(spearman(x, y), 3)}
    bt[arm] = per
wins = {arm: sum(bt[arm][c]["mae"] < bt["ENTERING"][c]["mae"] for c in CATS) for arm in ("PRIOR", "M3", "BLEND")}
summary["backtest_2025_26"] = {"entering_rows": len(entering), "scored": n_scored, "skipped_no_prior": miss_prior, "arms": bt,
                               "cats_where_arm_beats_entering_on_mae": wins}
# departures (T4-style): entering vs prior by 0.5 SD of the category; did M3 land closer than ENTERING?
dep = {}
for c in CATS:
    sd = statistics.pstdev([arms["PRIOR"][n][c] for n in arms["PRIOR"]])
    names = [n for n in arms["ENTERING"] if abs(arms["ENTERING"][n][c] - arms["PRIOR"][n][c]) >= 0.5 * sd]
    if not names: dep[c] = {"n": 0}; continue
    ent_better = sum(abs(arms["ENTERING"][n][c] - actual[n][c]) < abs(arms["PRIOR"][n][c] - actual[n][c]) for n in names)
    m3_better = sum(abs(arms["M3"][n][c] - actual[n][c]) < abs(arms["ENTERING"][n][c] - actual[n][c]) for n in names)
    bl_better = sum(abs(arms["BLEND"][n][c] - actual[n][c]) < abs(arms["ENTERING"][n][c] - actual[n][c]) for n in names)
    dep[c] = {"n": len(names), "entering_beats_prior": ent_better, "m3_beats_entering": m3_better, "blend_beats_entering": bl_better}
summary["departures_2025_26"] = dep
# (iii) GP history for the current deck pool + (v) M3 reference
deck = list(csv.DictReader(open(DECK, encoding="utf-8")))
gp_rows, b3_rows, found = [], [], {0: 0, 1: 0, 2: 0, 3: 0}
for p in deck:
    g = {}
    for s in ["2023-24", "2024-25", "2025-26"]:
        rows, byf, by3 = A[s]; r = find(p["player"], byf, by3); g[s] = r["gp"] if r else ""
    have = [v for v in g.values() if v != ""]; found[len(have)] += 1
    gp_rows.append({"player": p["player"], "team": p["team"], "gp_2023_24": g["2023-24"], "gp_2024_25": g["2024-25"], "gp_2025_26": g["2025-26"],
                    "seasons": len(have), "gp_mean": round(statistics.mean(have), 1) if have else "", "gp_min": min(have) if have else "",
                    "gp_frac_mean": round(statistics.mean(have) / 82, 3) if have else ""})
    line, used = m3(p["player"], ["2025-26", "2024-25", "2023-24"], [5, 4, 3])
    row = {"player": p["player"], "team": p["team"], "seasons_used": " ".join(used)}
    for c in CATS: row[c] = (f"{line[c]:.3f}" if c in ("fg_pct", "ft_pct") else f"{line[c]:.2f}") if line else ""
    for c in CATS: row["pool_" + c] = p[c]
    b3_rows.append(row)
with open(os.path.join(OUT, "gp_history_2026-27.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(gp_rows[0].keys())); w.writeheader(); w.writerows(gp_rows)
with open(os.path.join(OUT, "baseline3_2026-27.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(b3_rows[0].keys())); w.writeheader(); w.writerows(b3_rows)
summary["gp_history"] = {"deck_rows": len(deck), "seasons_found": found,
                         "mean_gp_frac_3yr_players": round(statistics.mean(r["gp_frac_mean"] for r in gp_rows if r["seasons"] == 3), 3),
                         "players_3yr_under_60_mean": sum(1 for r in gp_rows if r["seasons"] == 3 and r["gp_mean"] < 60)}
# (iv) identity on actual lines (2025-26, 25+ games): ESPN unrounded, and bref's rounded cells through the check's formula
ids = [abs(r["pts"] - (2 * r["fgm"] + r["tpm"] + r["ftm"])) for r in rows26 if r["gp"] >= 25]
bref = [r for r in csv.DictReader(open(os.path.join(OUT, "bref_pergame_2025-26.csv"), encoding="utf-8")) if int(r["gp"]) >= 25 and r["fg_pct"]]
gaps = sorted(abs(float(r["pts"]) - (2 * float(r["fg_pct"]) * float(r["fga"]) + float(r["tpm"]) + (float(r["ft_pct"]) * float(r["fta"]) if r["ft_pct"] else 0))) for r in bref)
summary["identity_on_actuals"] = {"espn_unrounded_max_gap": round(max(ids), 4), "n": len(ids), "bref_rounded_through_formula": {
    "n": len(gaps), "max": round(gaps[-1], 3), "p95": round(gaps[int(0.95 * len(gaps))], 3), "over_0_5": sum(g > 0.5 for g in gaps), "over_1_0": sum(g > 1.0 for g in gaps)}}
json.dump(summary, open(os.path.join(OUT, "analysis_summary.json"), "w"), indent=1)
print("STABILITY mean Spearman by cat:", summary["stability"]["mean_spearman"], "| least stable first:", summary["stability"]["least_stable_order"])
for t, v in stab.items(): print(f"  {t}: n={v['n']} " + " ".join(f"{c}={v['cats'][c]['spearman']}" for c in CATS))
b = summary["backtest_2025_26"]; print(f"BACKTEST scored {b['scored']} of {b['entering_rows']} (no prior {b['skipped_no_prior']}); arms beating ENTERING on MAE (of 9 cats): {wins}")
for c in CATS: print(f"  {c}: " + " | ".join(f"{arm} mae {bt[arm][c]['mae']} rho {bt[arm][c]['spearman']}" for arm in arms))
print("DEPARTURES:", dep)
print("GP HISTORY:", summary["gp_history"]); print("IDENTITY on actuals:", summary["identity_on_actuals"])
