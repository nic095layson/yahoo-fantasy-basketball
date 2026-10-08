#!/usr/bin/env python3
"""Owner question 2026-10-08 — "is there any additional, logical and effective fine tuning?" Three read-only
tests on records, run before suggesting anything (kit after-report-2026-10-08-standing-checks.md §5):

  A. Market blend. Last season, which predicted 2025-26 nine-category value better: entering-season lines
     built from the prior season's production (arena/data/players_2025-10-21.csv, priced by the deck
     engine), Yahoo's pre-draft ranks of 10/16/2025 (the league's own list), or a 50/50 rank blend?
  B. Age curve. Did those entering-season lines miss systematically by age (the WO-5 method has no
     development term)?
  C. Range check. How many cells of the card's current lines (data/players.csv, top 150 by value) sit
     outside every outside per-game reference on file — Yahoo 10/06, Hashtag 10/06, RotoBaller 9/29 and
     the player's own 2025-26 line (25+ games) — and how would the board move if each such cell were
     pulled to the nearest reference (a crude sensitivity, not a re-derivation)?

Actuals: Basketball-Reference per-game tables (derived CSVs beside the output, bref_extract.py).

    python3 arena/mocks/tuning_1008/tuning_tests.py RESULTS_DIR      (KIT_REPO or the sibling checkout)
"""
import copy, csv, importlib.util, json, math, os, re, sys, unicodedata
from collections import Counter
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
KIT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
RES = sys.argv[1]
spec = importlib.util.spec_from_file_location("hoops", os.path.join(ROOT, "scripts", "hoops.py"))
H = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, ["hoops"]
spec.loader.exec_module(H)
sys.argv = _argv
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def bref(season):
    out = {}
    for r in csv.DictReader(open(os.path.join(RES, f"bref_pergame_{season}.csv"), encoding="utf-8")):
        d = {}
        for k in ["age", "gp", "mpg", "fga", "fg_pct", "fta", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
            try:
                d[k] = float(r[k]) if r[k] else 0.0
            except ValueError:
                d[k] = 0.0
        out.setdefault(fold(r["player"]), d)
    return out


b25, b26 = bref("2024-25"), bref("2025-26")


def frame(pool):
    lf = sum(p["fg_pct"] * p["fga"] for p in pool) / sum(p["fga"] for p in pool)
    lt = sum(p["ft_pct"] * p["fta"] for p in pool) / sum(p["fta"] for p in pool)
    cols = {"FG": [(p["fg_pct"] - lf) * p["fga"] for p in pool], "FT": [(p["ft_pct"] - lt) * p["fta"] for p in pool]}
    for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
        cols[c] = [p[c] for p in pool]
    prm = {}
    for c, v in cols.items():
        m = sum(v) / len(v)
        prm[c] = (m, math.sqrt(sum((x - m) ** 2 for x in v) / len(v)) or 1.0)
    return lf, lt, prm


def zsum(p, F):
    lf, lt, prm = F
    vals = {"FG": (p["fg_pct"] - lf) * p["fga"], "FT": (p["ft_pct"] - lt) * p["fta"]}
    for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
        vals[c] = p[c]
    return sum((-1 if c == "tov" else 1) * (v - prm[c][0]) / prm[c][1] for c, v in vals.items())


# one actual-2025-26 frame: the top 156 by a first-pass value among players with 25+ games
qual = [v for v in b26.values() if v["gp"] >= 25]
F0 = frame(qual)
F = frame(sorted(qual, key=lambda p: -zsum(p, F0))[:156])
out = {}

# ---- A. market blend ----------------------------------------------------------------------------------
pool25 = list(csv.DictReader(open(os.path.join(ROOT, "arena", "data", "players_2025-10-21.csv"), encoding="utf-8")))
for r in pool25:
    for k in H.NUMERIC_COLS:
        r[k] = float(r[k])
H.zscores(pool25)
a_val = {fold(r["player"]): H.adj_value(r) for r in pool25}
a_av = {fold(r["player"]): H.availability(r) for r in pool25}
b_rank = {}
for ln in open(os.path.join(ROOT, "arena", "data", "league_predraft_ranks_2025-26_raw_2026-10-01.txt"), encoding="utf-8"):
    m = re.match(r"(\d+)\t(.+?) \(", ln)
    if m:
        b_rank.setdefault(fold(m.group(2)), int(m.group(1)))


def season_value(f):
    d = b26.get(f)
    if not d or d["gp"] == 0:
        return 0.0
    v = zsum(d, F); a = d["gp"] / 82.0
    return v * (a + (1 - a) * 0.20) if v > 0 else v


def pergame_value(f):
    d = b26.get(f)
    return zsum(d, F) if d and d["gp"] >= 10 else None


def ranks(d):
    return {k: i + 1 for i, (k, _) in enumerate(sorted(d.items(), key=lambda kv: -kv[1]))}


def spearman(x, y):
    keys = [k for k in x if k in y]; n = len(keys)
    rx = {k: i + 1 for i, k in enumerate(sorted(keys, key=lambda k: x[k]))}
    ry = {k: i + 1 for i, k in enumerate(sorted(keys, key=lambda k: y[k]))}
    return 1 - 6 * sum((rx[k] - ry[k]) ** 2 for k in keys) / (n * (n * n - 1)), n


A = []
for scope in (200, 120, 60):
    keys = [k for k, r in b_rank.items() if r <= scope and k in a_val and a_av[k] > 0]
    ar = ranks({k: a_val[k] for k in keys}); br = ranks({k: -b_rank[k] for k in keys})
    bl = ranks({k: -(ar[k] + br[k]) / 2 for k in keys})
    for label, actual in (("season value", {k: season_value(k) for k in keys}),
                          ("per-game value", {k: v for k in keys if (v := pergame_value(k)) is not None})):
        act = {k: -v for k, v in actual.items()}
        row = dict(scope=scope, actual=label)
        for name, pred in (("lines", ar), ("yahoo", br), ("blend", bl)):
            rho, n = spearman(pred, act); row[name] = round(rho, 3); row["n"] = n
        A.append(row)
        print(f"A  Yahoo top {scope:<3} n={row['n']:<3} {label:<15} lines {row['lines']:.3f} | Yahoo {row['yahoo']:.3f} | blend {row['blend']:.3f}")
out["A_market_blend"] = A

# ---- B. age curve -----------------------------------------------------------------------------------------
proj = {fold(r["player"]): r for r in pool25}
B_rows = []
for f, pr in proj.items():
    a = b26.get(f); prev = b25.get(f)
    if not a or a["gp"] < 25:
        continue
    line = {k: float(pr[k]) for k in ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]}
    B_rows.append(dict(player=pr["player"], age=a["age"], rookie=(prev is None or prev["gp"] < 10),
                       resid=round(zsum(a, F) - zsum(line, F), 3)))
groups = []
vets = [x for x in B_rows if not x["rookie"]]
for lo, hi, lab in [(0, 22, "<=22"), (23, 25, "23-25"), (26, 29, "26-29"), (30, 33, "30-33"), (34, 99, "34+")]:
    sel = sorted(x["resid"] for x in vets if lo <= x["age"] <= hi)
    if sel:
        n = len(sel); mean = sum(sel) / n
        sd = math.sqrt(sum((v - mean) ** 2 for v in sel) / (n - 1)) if n > 1 else 0.0
        groups.append(dict(group=lab, n=n, mean=round(mean, 2), se=round(sd / math.sqrt(n), 2), beat=sum(v > 0 for v in sel)))
allm = sum(x["resid"] for x in vets) / len(vets)
for g in groups:
    print(f"B  age {g['group']:<6} n={g['n']:>3} mean {g['mean']:+.2f} (se {g['se']:.2f}; vs all {g['mean'] - allm:+.2f}) beat {g['beat']}/{g['n']}")
out["B_age_curve"] = dict(n_vets=len(vets), mean_all=round(allm, 2), groups=groups)

# ---- C. range check ---------------------------------------------------------------------------------------
refs = {}


def add(src, name, get):
    try:
        d = {c: get(c) for c in CATS}
    except (ValueError, KeyError):
        return
    refs.setdefault(fold(name), {})[src] = d


M = os.path.join(KIT, "report", "market")
for r in csv.DictReader(open(os.path.join(M, "yahoo-proj-2026-10-06.csv"), encoding="utf-8")):
    add("Yahoo 10/06", r["player"], lambda c: float(r[c]))
for r in csv.DictReader(open(os.path.join(M, "hashtag-2026-10-06.csv"), encoding="utf-8")):
    add("Hashtag 10/06", r["player"], lambda c: float(r[c]))
for r in csv.DictReader(open(os.path.join(M, "rotoballer-2026-09-29.csv"), encoding="utf-8")):
    add("RotoBaller 9/29", r["player"], lambda c: float(r["src_" + c]) / (100.0 if c.endswith("pct") else 1.0))
for f, d in b26.items():
    if d["gp"] >= 25:
        refs.setdefault(f, {})["2025-26 actual"] = {c: d[c] for c in CATS}
base = H.load_players()
P = H.zscores(copy.deepcopy(base)); live = [p for p in P if H.availability(p) > 0]
order = sorted(live, key=lambda p: -H.adj_value(p)); top = order[:150]
fp = sorted(live, key=lambda p: -H.total_value(p))[:H.DRAFTABLE]
DF = frame(fp)


def zcell(p, c, v):
    lf, lt, prm = DF
    if c == "fg_pct":
        return ((v - lf) * p["fga"] - prm["FG"][0]) / prm["FG"][1]
    if c == "ft_pct":
        return ((v - lt) * p["fta"] - prm["FT"][0]) / prm["FT"][1]
    z = (v - prm[c][0]) / prm[c][1]
    return -z if c == "tov" else z


cells, covered = [], 0
for rank, p in enumerate(top, 1):
    ref = refs.get(fold(p["player"]), {})
    if len(ref) < 3:
        continue
    covered += 1
    for c in CATS:
        vals = [d[c] for d in ref.values()]; lo, hi = min(vals), max(vals); ours = float(p[c])
        tol = 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
        if lo - tol <= ours <= hi + tol:
            continue
        bound = lo if ours < lo else hi
        loose = abs(ours - bound) > (0.010 if c.endswith("pct") else max(0.2, 0.10 * hi))
        cells.append(dict(rank=rank, player=p["player"], cat=c, ours=ours, ref_lo=lo, ref_hi=hi, refs=len(ref),
                          loose=loose, z_beyond=round(zcell(p, c, ours) - zcell(p, c, bound), 3)))
up = [r for r in cells if r["z_beyond"] > 0]; dn = [r for r in cells if r["z_beyond"] < 0]
clamp = copy.deepcopy(base); by = {p["player"]: p for p in clamp}
for r in cells:
    by[r["player"]][r["cat"]] = r["ref_lo"] if r["ours"] < r["ref_lo"] else r["ref_hi"]


def board(Pl):
    Pl = H.zscores(Pl); lv = [p for p in Pl if H.availability(p) > 0]
    return {p["player"]: i + 1 for i, p in enumerate(sorted(lv, key=lambda p: -H.adj_value(p)))}


b0, b1 = board(copy.deepcopy(base)), board(clamp)
t150 = [n for n, r in b0.items() if r <= 150]
net = Counter()
for r in cells:
    net[r["player"]] += r["z_beyond"]
C = dict(checkable_rows=covered, rows_with_outlier=len({r["player"] for r in cells}), cells=len(cells),
         cells_loose=sum(r["loose"] for r in cells), rows_loose=len({r["player"] for r in cells if r["loose"]}),
         by_cat=dict(Counter(r["cat"] for r in cells)), flatter=len(up), flatter_z=round(sum(r["z_beyond"] for r in up), 2),
         understate=len(dn), understate_z=round(sum(r["z_beyond"] for r in dn), 2),
         clamp_moves_10plus=sum(abs(b1[n] - b0[n]) >= 10 for n in t150),
         largest_net=[dict(player=n, deck_rank=b0[n], net_z=round(z, 2)) for n, z in sorted(net.items(), key=lambda kv: -abs(kv[1]))[:15]],
         clamp_ranks={n: [b0[n], b1[n]] for n in t150}, cells_list=cells)
print(f"C  checkable {covered}, rows with an outlier cell {C['rows_with_outlier']}, cells {C['cells']} "
      f"(double tolerance: {C['cells_loose']} on {C['rows_loose']} rows); flatter {C['flatter']} ({C['flatter_z']:+}) / "
      f"understate {C['understate']} ({C['understate_z']:+}); clamp moves 10+: {C['clamp_moves_10plus']}")
out["C_range_check"] = C
json.dump(out, open(os.path.join(RES, "tuning_tests.json"), "w"), indent=1, ensure_ascii=False)
