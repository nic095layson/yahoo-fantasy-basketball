#!/usr/bin/env python3
"""Full 9-category integrity audit of both planes (owner request 2026-10-09: "conduct full categorical research to
ensure data computation is operating with integrity and accuracy").

Five parts, every number computed here from files, nothing typed in:
  A  Engine reproduction. An independent re-implementation of each plane's z-score method, written from its spec
     (deck: hoops.zscores docstring — top-156 fixed point over playable rows, volume-weighted FG%/FT% impact, TO
     negated, availability 0.78/0 on adj; kit: PROMPT.md §4.2 — pass 1 over all signed rows, pass 2 over the top 180,
     availability GP/82 + (1-GP/82)*0.20 on positive totals), compared cell by cell with each engine's own output
     (hoops.zscores in memory; the kit's committed top-200 board as printed).
  B  Data integrity per category, both planes: domains, 3PM <= FGM, the points identity
     pts = 2*FGM + 3PM + FTM, duplicates, and (kit) minutes/GP bounds and per-36 rates above last season's league max.
  C  Category agreement with the outside world on the top 150 by each plane's value: per-category bias against the
     median of the outside per-game lines (Yahoo, Hashtag, RotoBaller — two or more present), in raw units and in the deck's z
     frame; Spearman rank agreement per category against each source and against the 2025-26 actual line, with each
     source's own agreement with the actual line as the benchmark.
  D  Ranking sensitivity per category: the deck board recomputed with one category at a time replaced by the outside
     median (players without three outside lines keep ours), mean and max rank move in the top 150.
  E  Cross-plane agreement per category on the shared names.
Writes the JSON record (argv[1]) and prints a summary. Read-only on both repos."""
import csv, glob, json, math, os, re, statistics, sys, unicodedata
DECK = "/home/user/yahoo-fantasy-basketball"; KIT = os.environ.get("KIT_REPO", "/home/user/fantasy-basketball-2026-27")
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops  # noqa: E402  (engine under test — used only for its own outputs and the availability tag reader)

CATS = ["fg_pct", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
HC = {"fg_pct": "FG%", "ft_pct": "FT%", "tpm": "3PTM", "pts": "PTS", "reb": "REB", "ast": "AST", "stl": "ST", "blk": "BLK", "tov": "TO"}
KITC = {"fg_pct": "fgp", "ft_pct": "ftp"}

def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()

def mean_sd(v):
    m = sum(v) / len(v)
    return m, (math.sqrt(sum((x - m) ** 2 for x in v) / len(v)) or 1.0)

def zframe(pool, fga="fga", fta="fta"):
    """Independent z frame over `pool` (list of dicts with CATS + fga/fta): league %s volume-weighted, impact = (pct-lg)*att."""
    lg_fg = sum(p["fg_pct"] * p[fga] for p in pool) / sum(p[fga] for p in pool)
    lg_ft = sum(p["ft_pct"] * p[fta] for p in pool) / sum(p[fta] for p in pool)
    prm = {"fg_pct": mean_sd([(p["fg_pct"] - lg_fg) * p[fga] for p in pool]),
           "ft_pct": mean_sd([(p["ft_pct"] - lg_ft) * p[fta] for p in pool])}
    for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
        prm[c] = mean_sd([p[c] for p in pool])
    def z(p, c, v=None, fga_v=None, fta_v=None):
        v = p[c] if v is None else v
        if c == "fg_pct": return ((v - lg_fg) * (p[fga] if fga_v is None else fga_v) - prm[c][0]) / prm[c][1]
        if c == "ft_pct": return ((v - lg_ft) * (p[fta] if fta_v is None else fta_v) - prm[c][0]) / prm[c][1]
        zz = (v - prm[c][0]) / prm[c][1]
        return -zz if c == "tov" else zz
    return z, dict(lg_fg=lg_fg, lg_ft=lg_ft, prm=prm)

def spearman(a, b):
    def ranks(x):
        o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b); ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else float("nan")

# ---------------------------------------------------------------- inputs
deck_raw = list(csv.DictReader(open(os.path.join(DECK, "data/players.csv"), encoding="utf-8", newline="")))
for r in deck_raw:
    for c in CATS + ["fga", "fta"]: r[c] = float(r[c])
kit_raw = list(csv.DictReader(open(os.path.join(KIT, "report/projections-2026-27.csv"), encoding="utf-8")))
for r in kit_raw:
    for k in list(r):
        if k not in ("name", "team", "pos"): r[k] = float(r[k])
    r["player"] = r["name"]; r["fg_pct"] = r["fgp"]; r["ft_pct"] = r["ftp"]

def newest(pat):
    f = sorted(x for x in glob.glob(os.path.join(KIT, "report/market/*.csv")) if re.fullmatch(pat, os.path.basename(x)))
    return f[-1] if f else None
SOURCES = {}
for label, pat, pre, scale, nm in [("Yahoo", r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv", "", 1.0, "player"),
                                   ("Hashtag", r"hashtag-\d{4}-\d{2}-\d{2}\.csv", "", 1.0, "player"),
                                   ("RotoBaller", r"rotoballer-\d{4}-\d{2}-\d{2}\.csv", "src_", 100.0, "player")]:
    # Rotoworld's kit is NOT a line source: its 9-cat sheet's stat columns are the players' 2025-26 lines
    # (report/market/rotoworld-parse-2026-10-05.md: "The kit carries no projected stat lines"); the first run of this
    # audit included it and its Spearman against the 2025-26 actual came back 1.000 in eight categories, which is how
    # the mislabel showed. Excluded here as in range_check.py.
    f = newest(pat); lines = {}
    colmap = {c: pre + c for c in CATS}
    for r in csv.DictReader(open(f, encoding="utf-8-sig")):
        try:
            d = {c: float(r[colmap[c]]) / (scale if c.endswith("pct") else 1.0) for c in CATS}
        except (KeyError, TypeError, ValueError):
            continue
        lines[fold(r[nm])] = d
    SOURCES[label] = dict(file=os.path.basename(f), lines=lines)
ACT_F = os.path.join(DECK, "arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv")
actual = {}
for r in csv.DictReader(open(ACT_F, encoding="utf-8-sig")):
    try:
        if float(r["gp"] or 0) < 25: continue
        d = {c: float(r[c]) for c in CATS + ["fga", "fta", "mpg", "gp"]}
    except (KeyError, TypeError, ValueError):
        continue
    actual[fold(r["player"])] = d
rec = dict(inputs=dict(deck_pool="data/players.csv", deck_rows=len(deck_raw), kit_csv="report/projections-2026-27.csv",
                       kit_rows=len(kit_raw), sources={k: v["file"] for k, v in SOURCES.items()},
                       source_rows={k: len(v["lines"]) for k, v in SOURCES.items()},
                       actual=os.path.relpath(ACT_F, DECK), actual_rows=len(actual)))

# ---------------------------------------------------------------- A. engine reproduction
# A1 deck: engine output
P = hoops.zscores(hoops.load_players())
eng = {p["player"]: p for p in P}
avail = {p["player"]: hoops.availability(p) for p in P}
# independent fixed point
rows = [dict(r) for r in deck_raw]
z, fr = zframe(rows)
def tot(r, zf): return sum(zf(r, c) for c in CATS)
seen, pool_names, iters = set(), None, 0
live = [r for r in rows if avail[r["player"]] > 0]
for it in range(10):
    top = sorted(live, key=lambda r: -tot(r, z))[:156]
    key = frozenset(r["player"] for r in top)
    if key in seen: break
    seen.add(key); pool_names = key; iters = it + 1
    z, fr = zframe(top)
maxdiff = {c: max(abs(z(r, c) - eng[r["player"]]["z"][HC[c]]) for r in rows) for c in CATS}
def adj_ind(r):
    t = tot(r, z); a = avail[r["player"]]
    return t * a if t > 0 else t
ord_ind = [r["player"] for r in sorted(rows, key=lambda r: (-adj_ind(r), r["player"]))]
ord_eng = [p["player"] for p in sorted(P, key=lambda p: (-hoops.adj_value(p), p["player"]))]
fp_check = frozenset(r["player"] for r in sorted(live, key=lambda r: -tot(r, z))[:156]) == pool_names
rec["A_deck"] = dict(rows=len(rows), live=len(live), excluded=sum(1 for v in avail.values() if v == 0),
                     risk=sum(1 for v in avail.values() if 0 < v < 1), fixed_point_iterations=iters,
                     fixed_point_stable=fp_check, league_fg=round(fr["lg_fg"], 5), league_ft=round(fr["lg_ft"], 5),
                     max_abs_z_diff={c: maxdiff[c] for c in CATS}, order_identical_all=ord_ind == ord_eng,
                     order_identical_top200=ord_ind[:200] == ord_eng[:200])
# A2 kit
krows = [dict(r) for r in kit_raw if r["team"] != "FA"]
z1, _ = zframe(krows)
pool180 = sorted(krows, key=lambda r: -tot(r, z1))[:180]
z2, fr2 = zframe(pool180)
def kavail(gp): a = gp / 82.0; return a + (1 - a) * 0.20
for r in krows:
    r["_zt"] = tot(r, z2); r["_za"] = r["_zt"] * kavail(r["gp"]) if r["_zt"] > 0 else r["_zt"]
kord = sorted(krows, key=lambda r: -r["_za"])
board = []
for ln in open(os.path.join(KIT, "report/top-200-2026-27.md"), encoding="utf-8"):
    m = re.match(r"\| (\d+) \| ([^|]+) \| [^|]* \| [^|]* \| [^|]* \| [^|]* \| [^|]* \| ([+-][\d.]+) \| ([+-][\d.]+) \|", ln)
    if m: board.append((int(m.group(1)), m.group(2).strip(), float(m.group(3)), float(m.group(4))))
kd = {r["name"]: r for r in krows}
zt_diff = max(abs(kd[n]["_zt"] - zt) for _, n, zt, _ in board)
za_diff = max(abs(kd[n]["_za"] - za) for _, n, _, za in board)
kit_order_same = [n for _, n, _, _ in board] == [r["name"] for r in kord[:200]]
# the kit engine's own unrounded output (its functions, imported read-only) against the independent values
sys.path.insert(0, os.path.join(KIT, "report"))
import rank_engine as KE  # noqa: E402
kr = [r for r in KE.load(os.path.join(KIT, "report/projections-2026-27.csv")) if r["team"] != "FA"]
kz1 = KE.zscores(kr, kr); kpool = sorted(kr, key=lambda r: -KE.total(kz1[r["name"]]))[:KE.POOL_SIZE]; kz2 = KE.zscores(kr, kpool)
kcat = {"fg_pct": "fgp", "ft_pct": "ftp"}
kit_engine_maxdiff = {c: max(abs(z2(kd[n], c) - kz2[n][kcat.get(c, c)]) for n in kd) for c in CATS}
# convergence information: a third pass
pool3 = sorted(krows, key=lambda r: -tot(r, z2))[:180]
z3, _ = zframe(pool3)
ord3 = sorted(krows, key=lambda r: -(tot(r, z3) * kavail(r["gp"]) if tot(r, z3) > 0 else tot(r, z3)))
pos2 = {r["name"]: i for i, r in enumerate(kord)}; pos3 = {r["name"]: i for i, r in enumerate(ord3)}
moves3 = [abs(pos2[n] - pos3[n]) for n in pos2 if pos2[n] < 200]
# the kit pool admits rows the deck excludes (availability 0): how many GP<=25 rows sit inside the kit's 180
gp25_in_pool = sorted(r["name"] for r in pool180 if r["gp"] <= 25)
rec["A_kit"] = dict(rows_signed=len(krows), board_rows=len(board), max_abs_z_diff_vs_engine_unrounded=kit_engine_maxdiff, max_abs_zpg_diff_vs_board=round(zt_diff, 4),
                    max_abs_zadj_diff_vs_board=round(za_diff, 4), board_rounding=0.005, order_identical_top200=kit_order_same,
                    league_fg=round(fr2["lg_fg"], 5), league_ft=round(fr2["lg_ft"], 5),
                    pool3_overlap_with_pool2=len({r["name"] for r in pool3} & {r["name"] for r in pool180}),
                    pass3_top200_mean_rank_move=round(sum(moves3) / len(moves3), 3), pass3_top200_max_rank_move=max(moves3),
                    gp25_rows_inside_the_180_pool=gp25_in_pool)
# A3 sign/direction checks on the deck frame
sign = {}
for c in ["tpm", "pts", "reb", "ast", "stl", "blk", "tov"]:
    sign[c] = round(spearman([r[c] for r in rows], [z(r, c) for r in rows]), 6)
for c, att in [("fg_pct", "fga"), ("ft_pct", "fta")]:
    sign[c] = round(spearman([r[c] * r[att] - fr["lg_fg" if c == "fg_pct" else "lg_ft"] * r[att] for r in rows], [z(r, c) for r in rows]), 6)
rec["A_direction_spearman_raw_vs_z"] = sign

# A4 the availability haircut's reach: adj = tv*av only when tv > 0, so it bites only above the z-sum's zero
live_rows_a4 = sorted([r for r in rows if avail[r["player"]] > 0], key=lambda r: -adj_ind(r))
last_pos = max(i for i, r in enumerate(live_rows_a4, 1) if tot(r, z) > 0)
pool_mean_total = sum(tot(r, z) for r in rows if r["player"] in pool_names) / 156
risk_neg = [(i, r["player"], round(tot(r, z), 3)) for i, r in enumerate(live_rows_a4, 1)
            if i <= 200 and 0 < avail[r["player"]] < 1 and tot(r, z) <= 0]
risk_pos = [(i, r["player"]) for i, r in enumerate(live_rows_a4, 1) if i <= 200 and 0 < avail[r["player"]] < 1 and tot(r, z) > 0]
# counterfactual: haircut measured from replacement (the live rank-156 total) instead of from zero
repl = tot(live_rows_a4[155], z)
def adj_repl(r):
    t = tot(r, z); a = avail[r["player"]]
    return (t - repl) * a + repl if t > repl else t
cf = sorted(live_rows_a4, key=lambda r: -adj_repl(r)); cpos = {r["player"]: i for i, r in enumerate(cf, 1)}
cf_moves = [(i, r["player"], cpos[r["player"]]) for i, r in enumerate(live_rows_a4, 1) if i <= 200 and cpos[r["player"]] != i]
rec["A4_haircut_reach"] = dict(pool_mean_total=round(pool_mean_total, 9), last_positive_live_rank=last_pos,
    risk_rows_top200_discounted=len(risk_pos), risk_rows_top200_not_discounted=risk_neg,
    replacement_total_rank156=round(repl, 3),
    counterfactual_replacement_haircut=dict(rows_moved_top200=len(cf_moves),
        risk_rows_moved=[(a, n, b) for a, n, b in cf_moves if 0 < avail[n] < 1],
        max_move=max((abs(a - b) for a, _, b in cf_moves), default=0)))
# kit twin: same rule, zero at the mean of its 180 pool
kpos_last = max(i for i, r in enumerate(kord, 1) if r["_zt"] > 0)
k_gp_short_neg = [(i, r["name"], int(r["gp"]), round(r["_zt"], 3)) for i, r in enumerate(kord, 1) if i <= 200 and r["gp"] < 70 and r["_zt"] <= 0]
rec["A4_kit"] = dict(last_positive_rank=kpos_last, gp_under_70_top200_not_discounted=k_gp_short_neg)

# ---------------------------------------------------------------- B. data integrity
def integrity(rows, name_key, plane, top_names):
    out = dict(domain=[], tpm_gt_fgm=[], pts_identity=[], duplicates=[], resid_stats={})
    seen = {}
    for r in rows:
        n = r[name_key]; k = fold(n)
        if k in seen: out["duplicates"].append(n)
        seen[k] = 1
        bad = [c for c in CATS + ["fga", "fta"] if not (r[c] == r[c]) or r[c] < 0]
        if not (0 < r["fg_pct"] < 1): bad.append("fg_pct range")
        if not (0 <= r["ft_pct"] <= 1): bad.append("ft_pct range")
        if r["fga"] <= 0: bad.append("fga<=0")
        if bad: out["domain"].append((n, bad))
        fgm = r["fg_pct"] * r["fga"]; ftm = r["ft_pct"] * r["fta"]
        if r["tpm"] > fgm + 1e-9: out["tpm_gt_fgm"].append((n, r["tpm"], round(fgm, 2)))
        implied = 2 * fgm + r["tpm"] + ftm; res = r["pts"] - implied
        r["_resid"] = res
        if n in top_names and abs(res) > max(1.0, 0.08 * r["pts"]):
            out["pts_identity"].append(dict(player=n, pts=r["pts"], implied=round(implied, 2), resid=round(res, 2)))
    top = [r["_resid"] for r in rows if r[name_key] in top_names]
    out["resid_stats"] = dict(n=len(top), mean=round(statistics.mean(top), 3), sd=round(statistics.pstdev(top), 3),
                              max_abs=round(max(abs(x) for x in top), 2))
    out["pts_identity"].sort(key=lambda d: -abs(d["resid"]))
    return out
deck_top = set(ord_eng[:200]); kit_top = {r["name"] for r in kord[:200]}
# outside reference for the identity: Hashtag carries its own fgm/fga/ftm/fta
hs = list(csv.DictReader(open(newest(r"hashtag-\d{4}-\d{2}-\d{2}\.csv"), encoding="utf-8-sig")))
hres = []
for r in hs:
    try:
        f = {c: float(r[c]) for c in ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts"]}
    except ValueError:
        continue
    hres.append(f["pts"] - (2 * f["fg_pct"] * f["fga"] + f["tpm"] + f["ft_pct"] * f["fta"]))
act_res = [d["pts"] - (2 * d["fg_pct"] * d["fga"] + d["tpm"] + d["ft_pct"] * d["fta"]) for d in actual.values()]
rec["B_deck"] = integrity(rows, "player", "deck", deck_top)
rec["B_kit"] = integrity(krows, "name", "kit", kit_top)
rec["B_reference_identity"] = dict(hashtag=dict(n=len(hres), mean=round(statistics.mean(hres), 3), sd=round(statistics.pstdev(hres), 3)),
                                   actual_2025_26=dict(n=len(act_res), mean=round(statistics.mean(act_res), 3), sd=round(statistics.pstdev(act_res), 3)))
# kit minutes / gp bounds and per-36 above last season's max (players 15+ mpg, 25+ gp)
qual = [d for d in actual.values() if d["mpg"] >= 15]
max36 = {c: max(d[c] * 36 / d["mpg"] for d in qual) for c in ["pts", "reb", "ast", "stl", "blk", "tpm", "tov"]}
k36 = []
for r in krows:
    if not (0 <= r["gp"] <= 82) or not (0 < r["mpg"] <= 40): k36.append((r["name"], "gp/mpg bound", r["gp"], r["mpg"]))
    for c, mx in max36.items():
        if r["mpg"] >= 10 and r[c] * 36 / r["mpg"] > mx + 1e-9:
            k36.append((r["name"], c, round(r[c] * 36 / r["mpg"], 2), round(mx, 2)))
rec["B_kit_per36"] = dict(league_max_per36_2025_26={c: round(v, 2) for c, v in max36.items()}, flags=k36)

# ---------------------------------------------------------------- C. category agreement with outside lines
def outside_median(k):
    vals = [s["lines"][k] for s in SOURCES.values() if k in s["lines"]]
    if len(vals) < 2: return None
    return {c: statistics.median(v[c] for v in vals) for c in CATS}
def agreement(rows, name_key, order, plane):
    top = [r for r in order[:150]]
    out = {}
    for c in CATS:
        diffs, zd = [], []
        for r in top:
            med = outside_median(fold(r[name_key]))
            if med is None: continue
            diffs.append(r[c] - med[c])
            # z beyond the median in the deck frame (positive flatters)
            zd.append(z(r, c) - z(r, c, v=med[c]) if plane == "deck" else z2(r, c) - z2(r, c, v=med[c]))
        sp = {}
        for lab, s in SOURCES.items():
            pr = [(r[c], s["lines"][fold(r[name_key])][c]) for r in top if fold(r[name_key]) in s["lines"]]
            sp[lab] = round(spearman([a for a, _ in pr], [b for _, b in pr]), 3)
        pa = [(r[c], actual[fold(r[name_key])][c]) for r in top if fold(r[name_key]) in actual]
        sp["2025-26 actual"] = round(spearman([a for a, _ in pa], [b for _, b in pa]), 3)
        out[c] = dict(n=len(diffs), mean_diff_vs_outside_median=round(statistics.mean(diffs), 4),
                      share_above=round(sum(1 for d in diffs if d > 0) / len(diffs), 3),
                      net_z_vs_outside_median=round(sum(zd), 2), mean_z_vs_outside_median=round(statistics.mean(zd), 3),
                      spearman=sp)
    return out
live_rows = [r for r in rows if avail[r["player"]] > 0]
rec["C_deck"] = agreement(rows, "player", sorted(live_rows, key=lambda r: -adj_ind(r)), "deck")
rec["C_kit"] = agreement(krows, "name", kord, "kit")
# benchmark: each outside source's own Spearman with the 2025-26 actual on the same deck top-150 names
bench = {}
top150 = sorted(live_rows, key=lambda r: -adj_ind(r))[:150]
for c in CATS:
    bench[c] = {}
    for lab, s in SOURCES.items():
        pr = [(s["lines"][fold(r["player"])][c], actual[fold(r["player"])][c]) for r in top150
              if fold(r["player"]) in s["lines"] and fold(r["player"]) in actual]
        bench[c][lab] = round(spearman([a for a, _ in pr], [b for _, b in pr]), 3)
rec["C_benchmark_outside_vs_actual"] = bench

# ---------------------------------------------------------------- D. ranking sensitivity per category (deck)
base = sorted(live_rows, key=lambda r: -adj_ind(r)); bpos = {r["player"]: i for i, r in enumerate(base)}
sens = {}
for c in CATS:
    def adj_sub(r):
        med = outside_median(fold(r["player"]))
        t = sum(z(r, cc, v=(med[cc] if (cc == c and med) else None)) for cc in CATS); a = avail[r["player"]]
        return t * a if t > 0 else t
    o = sorted(live_rows, key=lambda r: -adj_sub(r)); pos = {r["player"]: i for i, r in enumerate(o)}
    mv = [(r["player"], bpos[r["player"]] + 1, pos[r["player"]] + 1) for r in base[:150]]
    d = [abs(a - b) for _, a, b in mv]
    big = sorted(mv, key=lambda t: -abs(t[1] - t[2]))[:5]
    sens[c] = dict(mean_rank_move_top150=round(sum(d) / len(d), 2), max_rank_move=max(d),
                   biggest=[dict(player=p, now=a, with_outside_median=b) for p, a, b in big])
rec["D_deck_sensitivity"] = sens

# ---------------------------------------------------------------- F. the largest departures per category (deck top 150)
dep = {}
for c in CATS:
    L = []
    for i, r in enumerate(base[:150], 1):
        med = outside_median(fold(r["player"]))
        if med is None: continue
        act = actual.get(fold(r["player"]), {}).get(c)
        L.append(dict(player=r["player"], deck_rank=i, ours=r[c], outside_median=round(med[c], 3),
                      actual_2025_26=act, z_beyond_median=round(z(r, c) - z(r, c, v=med[c]), 3)))
    L.sort(key=lambda d: -abs(d["z_beyond_median"]))
    dep[c] = L[:8]
rec["F_deck_largest_departures"] = dep

# ---------------------------------------------------------------- A5 kit counterfactual: the exclusion class held off like FA rows
krows_x = [r for r in krows if r["gp"] > 25]
zx1, _ = zframe(krows_x)
poolx = sorted(krows_x, key=lambda r: -tot(r, zx1))[:180]
zx2, _ = zframe(poolx)
for r in krows_x:
    t = tot(r, zx2); r["_zax"] = t * kavail(r["gp"]) if t > 0 else t
kx = sorted(krows_x, key=lambda r: -r["_zax"]); kxpos = {r["name"]: i for i, r in enumerate(kx, 1)}
kpos_now = {r["name"]: i for i, r in enumerate(kord, 1)}
left = [(kpos_now[r["name"]], r["name"], int(r["gp"])) for r in krows if r["gp"] <= 25 and kpos_now[r["name"]] <= 200]
mv = [abs(kpos_now[n] - kxpos[n]) for n in kxpos if kpos_now[n] <= 200]
rec["A5_kit_exclusion_class_counterfactual"] = dict(gp25_rows_on_the_top200_now=sorted(left), top200_rows_moving=sum(1 for x in mv if x),
                                                    mean_move=round(sum(mv) / len(mv), 2), max_move=max(mv))

# ---------------------------------------------------------------- E. cross-plane
kmap = {fold(r["name"]): r for r in krows}
shared = [(r, kmap[fold(r["player"])]) for r in rows if fold(r["player"]) in kmap]
cross = {}
for c in CATS:
    d = [a[c] - b[c] for a, b in shared]
    tol = 0.005 if c.endswith("pct") else 0.1
    cross[c] = dict(n=len(d), mean_deck_minus_kit=round(statistics.mean(d), 4), spearman=round(spearman([a[c] for a, _ in shared], [b[c] for _, b in shared]), 3),
                    differ_beyond_tol=sum(1 for x in d if abs(x) > tol))
rec["E_cross_plane"] = cross
json.dump(rec, open(sys.argv[1], "w"), indent=1, default=str)

# ---------------------------------------------------------------- summary
print("A deck: fixed point", iters, "iterations, stable", fp_check, "| max |z diff| per cat:", {c: f"{v:.1e}" for c, v in maxdiff.items()},
      "| order identical (all rows):", ord_ind == ord_eng)
print("A kit: max |z diff| vs the engine (unrounded) per cat:", {c: f"{v:.1e}" for c, v in kit_engine_maxdiff.items()}, "| max |zPG diff| vs board", round(zt_diff, 4), "| max |zAdj diff|", round(za_diff, 4), "| top-200 order identical:", kit_order_same,
      "| pass-3 top-200 mean/max move", rec["A_kit"]["pass3_top200_mean_rank_move"], max(moves3), "| GP<=25 rows inside the 180 pool:", len(gp25_in_pool))
print("A direction (Spearman raw vs z):", sign)
a4 = rec["A4_haircut_reach"]
print("A4 deck: pool-mean total", a4["pool_mean_total"], "| last positive live rank", last_pos, "| risk rows in top 200: discounted", len(risk_pos),
      "not discounted", len(risk_neg), "| replacement-haircut counterfactual moves", len(cf_moves), "max", a4["counterfactual_replacement_haircut"]["max_move"])
print("A4 kit: last positive rank", kpos_last, "| GP<70 rows in top 200 with no discount:", len(k_gp_short_neg))
for pl in ["B_deck", "B_kit"]:
    b = rec[pl]
    print(pl, "domain", len(b["domain"]), "| 3PM>FGM", len(b["tpm_gt_fgm"]), "| dupes", len(b["duplicates"]), "| pts identity flags (top 200)", len(b["pts_identity"]), "| resid", b["resid_stats"])
print("B reference identity residuals:", rec["B_reference_identity"])
print("B kit per-36 flags:", len(k36))
for pl in ["C_deck", "C_kit"]:
    print(pl)
    for c in CATS:
        v = rec[pl][c]; print(f"  {c:7} n={v['n']} mean diff {v['mean_diff_vs_outside_median']:+.4f} above {v['share_above']:.2f} net z {v['net_z_vs_outside_median']:+.2f} | rho", v["spearman"], "| bench", bench[c] if pl == "C_deck" else "")
print("A5 kit exclusion-class counterfactual:", rec["A5_kit_exclusion_class_counterfactual"])
for c in CATS:
    print("F", c, [(d["player"], d["ours"], d["outside_median"], d["actual_2025_26"], d["z_beyond_median"]) for d in rec["F_deck_largest_departures"][c][:5]])
print("D sensitivity:", {c: (v["mean_rank_move_top150"], v["max_rank_move"]) for c, v in sens.items()})
print("E cross-plane:", {c: (v["mean_deck_minus_kit"], v["spearman"], v["differ_beyond_tol"]) for c, v in cross.items()})
