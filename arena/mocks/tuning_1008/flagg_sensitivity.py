#!/usr/bin/env python3
"""Sensitivity only (no file changes, D-RN-2): Cooper Flagg's deck board rank under alternative lines —
our line (both planes), his 2025-26 rookie line, and the mean of the four outside per-game lines on file.

    python3 arena/mocks/tuning_1008/flagg_sensitivity.py OUT.json      (KIT_REPO or the sibling checkout)
"""
import copy, csv, importlib.util, json, os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
KIT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
OUT = sys.argv[1]
spec = importlib.util.spec_from_file_location("hoops", os.path.join(ROOT, "scripts", "hoops.py"))
H = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, ["hoops"]
spec.loader.exec_module(H)
sys.argv = _argv
M = os.path.join(KIT, "report", "market")
NAME = "Cooper Flagg"


def row(fname, col="player"):
    return next(r for r in csv.DictReader(open(os.path.join(M, fname), encoding="utf-8")) if r[col] == NAME)


y, h = row("yahoo-proj-2026-10-06.csv"), row("hashtag-2026-10-06.csv")
rb, sd = row("rotoballer-2026-09-29.csv"), row("statdunk-2026-08-24.csv")
pr = row("rotoworld-profiles-2026-10-05.csv")
K = ["fg_pct", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
src = {
    "Yahoo 10/06": {k: float(y[k]) for k in K},
    "Hashtag 10/06": dict({k: float(h[k]) for k in K}, fga=float(h["fga"]), fta=float(h["fta"])),
    "RotoBaller 9/29": {k: float(rb["src_" + k]) / (100.0 if k.endswith("pct") else 1.0) for k in K},
    "Statdunk 8/24": dict({k: float(sd[k]) for k in K}, fga=float(sd["fga"]), fta=float(sd["fta"])),
}
rookie = dict(fg_pct=float(pr["fgp"]), fga=float(pr["fga"]), ft_pct=float(pr["ftp"]), fta=float(pr["fta"]),
              tpm=float(pr["tpm"]), pts=float(pr["pts"]), reb=float(pr["reb"]), ast=float(pr["ast"]),
              stl=float(pr["stl"]), blk=float(pr["blk"]), tov=float(pr["tov"]))
mean = {}
for c in K + ["fga", "fta"]:
    v = [s[c] for s in src.values() if c in s]
    mean[c] = round(sum(v) / len(v), 3)
base = H.load_players()


def rank_with(line):
    P = copy.deepcopy(base)
    f = next(p for p in P if p["player"] == NAME)
    if line:
        f.update(line)
    P = H.zscores(P)
    order = sorted([p for p in P if H.availability(p) > 0], key=lambda p: -H.adj_value(p))
    i = next(k for k, p in enumerate(order) if p["player"] == NAME)
    return i + 1, round(H.adj_value(order[i]), 3)


out = {"sources": src, "rookie_2025_26": rookie, "outside_mean": mean}
for label, line in (("our line (both planes)", None), ("2025-26 rookie line", rookie), ("outside mean (4 sources)", mean)):
    r, v = rank_with(line)
    out[label] = dict(deck_rank=r, value=v)
    print(f"{label:<28} deck rank {r:>3}  value {v}")
json.dump(out, open(OUT, "w"), indent=1)
