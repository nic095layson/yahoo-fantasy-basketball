#!/usr/bin/env python3
"""Why does the kit board rank Cooper Flagg 14 and the deck board 22? (owner question 2026-10-08, D-RN-2)

Read-only. Prices both planes with their own engines (the kit's report/rank_engine.py, the deck's
scripts/hoops.py), then isolates the three candidate mechanisms: his own line, the availability rule
(the kit's games-based multiplier applied to the deck's z-sum), and the lines of the players ranked
between his two places.

    python3 arena/mocks/tuning_1008/flagg_planes.py OUT.json        (KIT_REPO or the sibling checkout)
"""
import csv, importlib.util, json, os, re, sys, unicodedata
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
KIT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
OUT = sys.argv[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, [name]
    spec.loader.exec_module(mod)
    sys.argv = argv
    return mod


H = load("hoops", os.path.join(ROOT, "scripts", "hoops.py"))
sys.path.insert(0, os.path.join(KIT, "report"))
K = load("rank_engine", os.path.join(KIT, "report", "rank_engine.py"))


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s); s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


# the kit board exactly as rank_engine.main builds it (two-pass top-180 pool, games-based availability)
rows = [r for r in K.load(os.path.join(KIT, "report", "projections-2026-27.csv")) if r["team"] != "FA"]
z1 = K.zscores(rows, rows)
pool = sorted(rows, key=lambda r: -K.total(z1[r["name"]]))[:K.POOL_SIZE]
z2 = K.zscores(rows, pool)
kval = {}
for r in rows:
    t = K.total(z2[r["name"]])
    kval[r["name"]] = t * K.avail(r["gp"]) if t > 0 else t
krank = {n: i + 1 for i, (n, _) in enumerate(sorted(kval.items(), key=lambda kv: -kv[1]))}
kby = {fold(r["name"]): r for r in rows}

# the deck board (top-156 fixed point, the note-tag availability)
P = H.zscores(H.load_players())
live = [p for p in P if H.availability(p) > 0]
drank = {p["player"]: i + 1 for i, p in enumerate(sorted(live, key=lambda p: -H.adj_value(p)))}
dby = {fold(p["player"]): p for p in P}


def kit_gp_value(p):
    k = kby.get(fold(p["player"]))
    tv = H.total_value(p)
    a = K.avail(k["gp"]) if k else H.availability(p)
    return tv * a if tv > 0 else tv


drank_gp = {p["player"]: i + 1 for i, p in enumerate(sorted(live, key=lambda p: -kit_gp_value(p)))}
COLS = [("pts", "pts"), ("reb", "reb"), ("ast", "ast"), ("stl", "stl"), ("blk", "blk"), ("tpm", "tpm"),
        ("tov", "tov"), ("fgp", "fg_pct"), ("fga", "fga"), ("ftp", "ft_pct"), ("fta", "fta")]


def line_diff(fn):
    k, d = kby.get(fn), dby.get(fn)
    if not k or not d:
        return None
    return {kc: [float(k[kc]), float(d[dc])] for kc, dc in COLS if abs(float(k[kc]) - float(d[dc])) > 1e-9}


F = "Cooper Flagg"
between = []
for n, r in sorted(drank.items(), key=lambda kv: kv[1]):
    if r >= drank[F]:
        break
    kn = kby.get(fold(n), {}).get("name")
    if kn and krank.get(kn, 999) > krank[F]:
        between.append(dict(player=n, deck_rank=r, kit_rank=krank[kn], kit_minus_deck=line_diff(fold(n))))
top150 = [fold(n) for n, r in drank.items() if r <= 150]
same = sum(1 for f in top150 if line_diff(f) == {})
res = dict(flagg=dict(kit_rank=krank[F], deck_rank=drank[F], deck_rank_with_kit_games=drank_gp[F],
                      line_differs_between_planes=line_diff(fold(F))),
           above_on_deck_not_on_kit=between,
           top150_same_line=same, top150_compared=sum(1 for f in top150 if line_diff(f) is not None))
json.dump(res, open(OUT, "w"), indent=1)
print(f"Flagg: kit {krank[F]}, deck {drank[F]}, deck with the kit's games rule {drank_gp[F]}; "
      f"his line differs between planes: {bool(line_diff(fold(F)))}")
print(f"players above him on the deck but not on the kit: {len(between)}, of which with a different line: "
      f"{sum(1 for b in between if b['kit_minus_deck'])}")
for b in between:
    print(f"  {b['player']:<24} deck {b['deck_rank']:>3}  kit {b['kit_rank']:>3}  "
          + ("same line" if not b["kit_minus_deck"] else ", ".join(f"{k} {v[0]:g}/{v[1]:g}" for k, v in b["kit_minus_deck"].items())))
print(f"top-150 deck rows with the same line on both planes: {res['top150_same_line']} of {res['top150_compared']}")
