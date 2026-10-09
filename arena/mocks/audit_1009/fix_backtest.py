#!/usr/bin/env python3
"""Owner question 2026-10-09: would the audit's proposed fixes (D-1009-1..4) have sharpened last season's forecast?
Read-only backtest on the 2025-26 entering pool (arena/data/players_2025-10-21.csv, 220 rows, 20 inj-risk tags) against
the actual 2025-26 per-game lines (Basketball-Reference, arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv) and
the 2024-25 lines for stability. Value frame and season_value as in tuning_1008/tuning_tests.py (per-game 9-cat z over
the actual top-156, times GP/82 + (1-GP/82)*0.20 when positive).

  T1  D-1009-2, the discount anchor: rank the entering pool under (a) the shipped rule (×av only above the pool-mean
      zero), (b) the discount anchored at replacement (the rank-156 total), (c) no discount, (d) ×av on every row
      (negatives shrink too). Spearman vs realized season value; and the 20 risk rows' mean realized rank minus
      forecast rank (positive = the forecast was too high).
  T2  D-1009-3, the points identity: |pts - (2·FGM + 3PM + FTM)| on the entering lines vs the realized points error;
      and the points MAE if every line's points were replaced by its implied points.
  T3  Per category: Spearman of the entering line vs the actual (which categories we forecast worst), and the
      year-over-year stability of the actuals (2024-25 → 2025-26) as the ceiling any forecast works against.
  T4  Departures: in each category, where the entering line departed from the player's 2024-25 actual by 0.5+ z,
      how often was the line closer to the 2025-26 actual than the prior season was (did the departure add
      information)?
    python3 arena/mocks/audit_1009/fix_backtest.py OUT.json
"""
import copy, csv, json, math, os, re, statistics, sys, unicodedata
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
_argv, sys.argv = sys.argv, ["hoops"]; import hoops as H; sys.argv = _argv  # noqa: E402
RES = os.path.join(ROOT, "arena", "results", "tuning_2026-10-08")
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]

def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s); return re.sub(r"\s+", " ", s).strip()

def bref(season):
    out = {}
    for r in csv.DictReader(open(os.path.join(RES, f"bref_pergame_{season}.csv"), encoding="utf-8")):
        d = {}
        for k in ["age", "gp", "mpg", "fga", "fg_pct", "fta", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
            try: d[k] = float(r[k]) if r[k] else 0.0
            except ValueError: d[k] = 0.0
        out.setdefault(fold(r["player"]), d)
    return out
b25, b26 = bref("2024-25"), bref("2025-26")

def frame(pool):
    lf = sum(p["fg_pct"] * p["fga"] for p in pool) / sum(p["fga"] for p in pool)
    lt = sum(p["ft_pct"] * p["fta"] for p in pool) / sum(p["fta"] for p in pool)
    cols = {"fg_pct": [(p["fg_pct"] - lf) * p["fga"] for p in pool], "ft_pct": [(p["ft_pct"] - lt) * p["fta"] for p in pool]}
    for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]: cols[c] = [p[c] for p in pool]
    prm = {c: (sum(v) / len(v), math.sqrt(sum((x - sum(v) / len(v)) ** 2 for x in v) / len(v)) or 1.0) for c, v in cols.items()}
    return lf, lt, prm
def zc(p, c, F, v=None):
    lf, lt, prm = F; v = p[c] if v is None else v
    if c == "fg_pct": x = (v - lf) * p["fga"]
    elif c == "ft_pct": x = (v - lt) * p["fta"]
    else: x = v
    z = (x - prm[c][0]) / prm[c][1]; return -z if c == "tov" else z
def zsum(p, F): return sum(zc(p, c, F) for c in CATS)
qual = [v for v in b26.values() if v["gp"] >= 25]
F0 = frame(qual); F = frame(sorted(qual, key=lambda p: -zsum(p, F0))[:156])
def season_value(f):
    d = b26.get(f)
    if not d or d["gp"] == 0: return 0.0
    v = zsum(d, F); a = d["gp"] / 82.0
    return v * (a + (1 - a) * 0.20) if v > 0 else v
def spearman(x, y):
    keys = [k for k in x if k in y]; n = len(keys)
    rx = {k: i + 1 for i, k in enumerate(sorted(keys, key=lambda k: x[k]))}; ry = {k: i + 1 for i, k in enumerate(sorted(keys, key=lambda k: y[k]))}
    return round(1 - 6 * sum((rx[k] - ry[k]) ** 2 for k in keys) / (n * (n * n - 1)), 3), n

pool = list(csv.DictReader(open(os.path.join(ROOT, "arena", "data", "players_2025-10-21.csv"), encoding="utf-8")))
for r in pool:
    for k in H.NUMERIC_COLS: r[k] = float(r[k])
H.zscores(pool)
live = [r for r in pool if H.availability(r) > 0]
tv = {fold(r["player"]): H.total_value(r) for r in live}; av = {fold(r["player"]): H.availability(r) for r in live}
order = sorted(tv, key=lambda k: -tv[k]); repl = tv[order[155]] if len(order) >= 156 else min(tv.values())
rules = {
    "a_shipped (×av above zero=mean)": lambda k: tv[k] * av[k] if tv[k] > 0 else tv[k],
    "b_replacement_anchor": lambda k: (tv[k] - repl) * av[k] + repl if tv[k] > repl else tv[k],
    "c_no_discount": lambda k: tv[k],
    "d_discount_every_row": lambda k: tv[k] * av[k],
}
actual = {k: season_value(k) for k in tv if k in b26}
out = {"inputs": dict(pool="arena/data/players_2025-10-21.csv", rows=len(pool), live=len(live), risk_rows=sum(1 for v in av.values() if 0 < v < 1),
                      excluded=len(pool) - len(live), replacement_total=round(repl, 3), actual_rows=len(actual))}
T1 = {}
for name, fn in rules.items():
    pred = {k: fn(k) for k in tv}
    row = {}
    for scope in (60, 120, 156, 200):
        top = sorted(pred, key=lambda k: -pred[k])[:scope]
        rho, n = spearman({k: pred[k] for k in top if k in actual}, {k: actual[k] for k in top if k in actual}); row[f"rho_top{scope}"] = rho; row[f"n_top{scope}"] = n
    pr = {k: i + 1 for i, k in enumerate(sorted(pred, key=lambda k: -pred[k]))}
    ar = {k: i + 1 for i, k in enumerate(sorted(actual, key=lambda k: -actual[k]))}
    risk = [k for k in tv if 0 < av[k] < 1 and k in ar]
    row["risk_rows_mean_realized_minus_forecast_rank"] = round(statistics.mean(ar[k] - pr[k] for k in risk), 1)
    row["risk_rows_forecast_too_high"] = sum(1 for k in risk if ar[k] > pr[k])
    row["risk_rows_n"] = len(risk)
    T1[name] = row
# where did the 20 risk rows sit on the entering board, and were the ones below zero discounted?
risk_detail = sorted([(pool_r["player"], round(tv[fold(pool_r["player"])], 2), {k: i + 1 for i, k in enumerate(order)}[fold(pool_r["player"])],
                       int(b26.get(fold(pool_r["player"]), {}).get("gp", 0))) for pool_r in live if 0 < av[fold(pool_r["player"])] < 1], key=lambda t: t[2])
T1["risk_rows_detail (name, entering total, entering rank, actual GP)"] = risk_detail
T1["risk_rows_below_zero_undiscounted"] = sum(1 for _, t, _, _ in risk_detail if t <= 0)
out["T1_discount_anchor"] = T1

# T2 points identity
T2 = {}; rows = []
for r in pool:
    k = fold(r["player"]); a = b26.get(k)
    if not a or a["gp"] < 25: continue
    implied = 2 * r["fg_pct"] * r["fga"] + r["tpm"] + r["ft_pct"] * r["fta"]
    rows.append(dict(name=r["player"], resid=r["pts"] - implied, err=r["pts"] - a["pts"], err_implied=implied - a["pts"]))
flag = [x for x in rows if abs(x["resid"]) > max(1.0, 0.08 * (x["resid"] + 0))]  # placeholder, replaced below
flag = [x for x in rows if abs(x["resid"]) > 1.0]
T2["n"] = len(rows); T2["lines_with_|resid|>1"] = len(flag)
T2["pts_MAE_as_written"] = round(statistics.mean(abs(x["err"]) for x in rows), 3)
T2["pts_MAE_if_pts_set_to_implied"] = round(statistics.mean(abs(x["err_implied"]) for x in rows), 3)
T2["flagged_rows_MAE_as_written"] = round(statistics.mean(abs(x["err"]) for x in flag), 3) if flag else None
T2["flagged_rows_MAE_if_implied"] = round(statistics.mean(abs(x["err_implied"]) for x in flag), 3) if flag else None
T2["flagged_rows_improved_by_identity"] = sum(1 for x in flag if abs(x["err_implied"]) < abs(x["err"]))
rho, n = spearman({x["name"]: abs(x["resid"]) for x in rows}, {x["name"]: abs(x["err"]) for x in rows}); T2["spearman_|resid|_vs_|pts_error|"] = rho
T2["sign_agreement (resid and error same sign)"] = round(sum(1 for x in rows if x["resid"] * x["err"] > 0) / len(rows), 3)
T2["flagged_detail"] = sorted([(x["name"], round(x["resid"], 2), round(x["err"], 2), round(x["err_implied"], 2)) for x in flag], key=lambda t: -abs(t[1]))
out["T2_points_identity"] = T2

# T3 per-category forecast quality and y/y stability
T3 = {}
top150 = [r for r in sorted(live, key=lambda r: -H.adj_value(r))[:150]]
for c in CATS:
    pred = {fold(r["player"]): r[c] for r in top150 if fold(r["player"]) in b26 and b26[fold(r["player"])]["gp"] >= 25}
    act = {k: b26[k][c] for k in pred}
    rho_f, n_f = spearman(pred, act)
    prior = {k: b25[k][c] for k in pred if k in b25 and b25[k]["gp"] >= 25}
    rho_p, n_p = spearman(prior, {k: act[k] for k in prior})
    rho_line_vs_prior_subset, _ = spearman({k: pred[k] for k in prior}, {k: act[k] for k in prior})
    bias = statistics.mean(pred[k] - act[k] for k in pred)
    T3[c] = dict(n=n_f, rho_line_vs_actual=rho_f, rho_prior_actual_vs_actual=rho_p, rho_line_vs_actual_same_subset=rho_line_vs_prior_subset,
                 n_prior=n_p, mean_line_minus_actual=round(bias, 3))
out["T3_per_category"] = T3

# T4 departures: line vs prior actual, 0.5+ z apart in the entering frame
Fe = frame([dict(r) for r in top150])
T4 = {}
for c in CATS:
    won = tot = 0; ex = []
    for r in top150:
        k = fold(r["player"])
        if k not in b25 or k not in b26 or b25[k]["gp"] < 25 or b26[k]["gp"] < 25: continue
        dz = zc(r, c, Fe) - zc(r, c, Fe, v=b25[k][c])
        if abs(dz) < 0.5: continue
        tot += 1
        closer = abs(r[c] - b26[k][c]) < abs(b25[k][c] - b26[k][c])
        won += closer
        ex.append((r["player"], round(dz, 2), r[c], b25[k][c], b26[k][c], closer))
    T4[c] = dict(departures=tot, line_closer_than_prior=won, share=round(won / tot, 2) if tot else None,
                 largest=sorted(ex, key=lambda t: -abs(t[1]))[:4])
out["T4_departures"] = T4
json.dump(out, open(sys.argv[1], "w"), indent=1, default=str)
print("inputs", out["inputs"])
print("\nT1 discount anchor (Spearman vs realized season value; risk rows: realized rank − forecast rank, + = forecast too high)")
for k, v in T1.items():
    if isinstance(v, dict): print(f"  {k:36}", {kk: vv for kk, vv in v.items() if not kk.startswith("n_")})
print("  risk rows with entering total <= 0 (undiscounted under the shipped rule):", T1["risk_rows_below_zero_undiscounted"], "of", len(risk_detail))
print("\nT2 points identity:", {k: v for k, v in T2.items() if k != "flagged_detail"})
for t in T2["flagged_detail"][:8]: print("  ", t)
print("\nT3 per category (line ρ vs actual | prior-season actual ρ vs actual | bias line−actual)")
for c, v in T3.items(): print(f"  {c:7} line {v['rho_line_vs_actual']:.3f} (n {v['n']}) | prior {v['rho_prior_actual_vs_actual']:.3f} vs line-same-subset {v['rho_line_vs_actual_same_subset']:.3f} (n {v['n_prior']}) | bias {v['mean_line_minus_actual']:+.3f}")
print("\nT4 departures from prior actual (0.5+ z): share where the line beat the prior season")
for c, v in T4.items(): print(f"  {c:7} {v['line_closer_than_prior']}/{v['departures']} = {v['share']}", [(e[0], e[1]) for e in v["largest"][:2]])
