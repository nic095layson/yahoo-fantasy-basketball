#!/usr/bin/env python3
"""Per-category range check for projection passes (owner decision D-RN-3, 2026-10-08).

Born from the 2026-10-08 tuning tests (kit after-report-2026-10-08-standing-checks.md
§5 C): 131 of the 145 checkable top-150 lines carried at least one category more
extreme than every outside reference — Flagg's free throws at .780 against .827–.840
everywhere else among them — and those cells leaned flattering (252 lift a player,
184 hold one down). A line may sit outside every source for a real reason (a role
the sources have not priced), so the rule does not assume the sources are right: on
a projection pass (WO-5, the 10/14 lock), every cell still outside ALL of its
references either carries a one-line mechanism backed by two dated outlets, or comes
back inside the range.

  default            for the top TOP lines by the deck's value (data/players.csv,
                     the page's source), set every category against the range of
                     its references — the kit's newest Yahoo projection, Hashtag and
                     RotoBaller per-game lines and the player's own 2025-26 line
                     (25+ games) — wherever three or more exist. A cell is outside
                     when it misses [min, max] by more than .005 on a percentage or
                     max(0.1, 5% of the max) on a counting stat. Print the
                     ready-to-paste "Range check" section: one row per player with
                     his cells, the z they carry beyond the nearest reference (the
                     deck's own frame; positive flatters him) and a mechanism
                     column to fill.
  --check-report P   verify the report at P has a "Range check" section with one
                     table row per listed player whose text names two outlets,
                     counted with the KIT's own lexicon (report/check_report.py
                     outlet_count). Exit 1 naming every player without a row or
                     with fewer than two outlets.
  --json PATH        write the run record.
  --actual CSV       the 2025-26 per-game reference (default: the committed
                     derivation of Basketball-Reference's table,
                     arena/results/tuning_2026-10-08/bref_pergame_2025-26.csv).
"""
import argparse
import csv
import glob
import importlib.util
import json
import math
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
KIT_DEFAULT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
ACTUAL_DEFAULT = os.path.join(ROOT, "arena", "results", "tuning_2026-10-08", "bref_pergame_2025-26.csv")
HEADING = "Range check"
TOP = 150
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
# (label, filename pattern, column prefix, percentage scale)
LINE_SOURCES = [
    ("Yahoo", r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv", "", 1.0),
    ("Hashtag", r"hashtag-\d{4}-\d{2}-\d{2}\.csv", "", 1.0),
    ("RotoBaller", r"rotoballer-\d{4}-\d{2}-\d{2}\.csv", "src_", 100.0),
]
sys.path.insert(0, HERE)
import hoops  # noqa: E402


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def newest(kit, pattern):
    files = sorted(f for f in glob.glob(os.path.join(kit, "report", "market", "*.csv"))
                   if re.fullmatch(pattern, os.path.basename(f)))
    return files[-1] if files else None


def references(kit, actual):
    refs, used = {}, {}
    for label, pat, pre, scale in LINE_SOURCES:
        f = newest(kit, pat)
        if not f:
            continue
        used[label] = os.path.basename(f)
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            try:
                d = {c: float(r[pre + c]) / (scale if c.endswith("pct") else 1.0) for c in CATS}
            except (KeyError, TypeError, ValueError):
                continue
            refs.setdefault(fold(r["player"]), {})[label] = d
    if actual and os.path.exists(actual):
        used["2025-26 actual"] = os.path.relpath(actual, ROOT) if actual.startswith(ROOT) else os.path.basename(actual)
        for r in csv.DictReader(open(actual, encoding="utf-8-sig")):
            try:
                if float(r["gp"] or 0) < 25:
                    continue
                d = {c: float(r[c]) for c in CATS}
            except (KeyError, TypeError, ValueError):
                continue
            refs.setdefault(fold(r["player"]), {})["2025-26 actual"] = d
    return refs, used


def compute(args):
    P = hoops.zscores(hoops.load_players())
    live = [p for p in P if hoops.availability(p) > 0]
    order = sorted(live, key=lambda p: -hoops.adj_value(p))
    # the deck's own z frame: the same arithmetic as hoops.zscores over the top-156 fixed point
    fp = sorted(live, key=lambda p: -hoops.total_value(p))[:hoops.DRAFTABLE]
    lg_fg = sum(p["fg_pct"] * p["fga"] for p in fp) / sum(p["fga"] for p in fp)
    lg_ft = sum(p["ft_pct"] * p["fta"] for p in fp) / sum(p["fta"] for p in fp)

    def ms(vals):
        m = sum(vals) / len(vals)
        return m, (math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) or 1.0)

    prm = {"fg_pct": ms([(p["fg_pct"] - lg_fg) * p["fga"] for p in fp]),
           "ft_pct": ms([(p["ft_pct"] - lg_ft) * p["fta"] for p in fp])}
    for c in ["pts", "reb", "ast", "stl", "blk", "tpm", "tov"]:
        prm[c] = ms([p[c] for p in fp])

    def zcell(p, c, v):
        if c == "fg_pct":
            return ((v - lg_fg) * p["fga"] - prm[c][0]) / prm[c][1]
        if c == "ft_pct":
            return ((v - lg_ft) * p["fta"] - prm[c][0]) / prm[c][1]
        z = (v - prm[c][0]) / prm[c][1]
        return -z if c == "tov" else z

    refs, used = references(args.kit, args.actual)
    rows, checkable, ncells = [], 0, 0
    for rank, p in enumerate(order[:args.top], 1):
        ref = refs.get(fold(p["player"]), {})
        if len(ref) < 3:
            continue
        checkable += 1
        cells, net = [], 0.0
        for c in CATS:
            vals = [d[c] for d in ref.values()]
            lo, hi = min(vals), max(vals)
            ours = float(p[c])
            tol = 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
            if lo - tol <= ours <= hi + tol:
                continue
            bound = lo if ours < lo else hi
            z = zcell(p, c, ours) - zcell(p, c, bound)
            net += z
            f = (lambda v: f"{v:.3f}".lstrip("0")) if c.endswith("pct") else (lambda v: f"{v:g}")
            cells.append(dict(cat=c, ours=ours, lo=lo, hi=hi, z_beyond=round(z, 3),
                              text=f"{c} {f(ours)} vs {f(lo)}-{f(hi)}"))
        if cells:
            ncells += len(cells)
            rows.append(dict(player=p["player"], deck_rank=rank, refs=sorted(ref), cells=cells, net_z=round(net, 2)))
    rows.sort(key=lambda r: (-abs(r["net_z"]), r["deck_rank"]))
    return dict(top=args.top, checkable=checkable, players=len(rows), cells=ncells, references=used, rows=rows)


def section(rec):
    out = [f"## {HEADING} (D-RN-3)", "",
           f"Rule (owner, 2026-10-08): on a projection pass, every cell of a top-{rec['top']} line that sits "
           "outside the range of ALL its references (three or more of: " + ", ".join(
               f"{k} `{v}`" for k, v in rec["references"].items()) + "; tolerance .005 on percentages, 5% with a "
           "0.1 floor on counting stats) carries a one-line mechanism naming two dated outlets, or comes back inside "
           f"the range. This page: {rec['players']} player(s), {rec['cells']} cell(s), of {rec['checkable']} checkable "
           f"top-{rec['top']} lines. Net z is what the cells carry beyond the nearest reference in the deck's frame "
           "(positive flatters the player).", "",
           "| player | deck rank | cells outside every reference | net z | mechanism (two dated outlets) |",
           "|---|---|---|---|---|"]
    for r in rec["rows"]:
        out.append(f"| {r['player']} | {r['deck_rank']} | " + "; ".join(c["text"] for c in r["cells"])
                   + f" | {r['net_z']:+.2f} | — |")
    return "\n".join(out) + "\n"


def kit_outlet_count(kit):
    path = os.path.join(kit, "report", "check_report.py")
    if not os.path.exists(path):
        print(f"RANGE CHECK: STOP — the kit's outlet lexicon is missing ({path}); set KIT_REPO or --kit")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("kit_check_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.outlet_count


def check_report(path, rec, outlets):
    lines = open(path, encoding="utf-8").read().splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("#") and HEADING in ln), None)
    if start is None:
        print(f"RANGE CHECK: FAIL — no '{HEADING}' section in {os.path.basename(path)}")
        return 1
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    rows = {}
    for ln in lines[start + 1:]:
        if ln.startswith("#") and len(ln) - len(ln.lstrip("#")) <= level:
            break
        s = ln.strip()
        if s.startswith("|") and not set(s) <= set("|-: "):
            rows.setdefault(fold(s.strip("|").split("|")[0]), s)
    problems = []
    for r in rec["rows"]:
        row = rows.get(fold(r["player"]))
        if row is None:
            problems.append(f"{r['player']}: no row")
        elif outlets(row) < 2:
            problems.append(f"{r['player']}: fewer than two outlets in its row")
    if problems:
        print(f"RANGE CHECK: FAIL — {os.path.basename(path)}: " + "; ".join(problems))
        return 1
    print(f"RANGE CHECK: PASS — {os.path.basename(path)}: {rec['players']} listed player(s), each with a row "
          "naming two outlets")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kit", default=KIT_DEFAULT)
    ap.add_argument("--actual", default=ACTUAL_DEFAULT)
    ap.add_argument("--top", type=int, default=TOP)
    ap.add_argument("--json")
    ap.add_argument("--check-report", metavar="PATH")
    args = ap.parse_args()
    rec = compute(args)
    if args.json:
        json.dump(rec, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if args.check_report:
        sys.exit(check_report(args.check_report, rec, kit_outlet_count(args.kit)))
    print(f"RANGE CHECK: {rec['players']} player(s) with {rec['cells']} cell(s) outside every reference "
          f"({rec['checkable']} of the top {rec['top']} checkable)")
    print()
    print(section(rec))


if __name__ == "__main__":
    main()
