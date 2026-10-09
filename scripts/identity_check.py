#!/usr/bin/env python3
"""Points-identity check for projection passes (owner decision D-1009-3, 2026-10-09).

A per-game line's points follow from its own shooting: pts = 2·FGM + 3PM + FTM, with FGM = FG% × FGA and
FTM = FT% × FTA (a three counts twice inside FGM and once more here). The outside lines on file hold the
identity to rounding (Hashtag's residual sd 0.056, the 2025-26 actual lines' 0.055); the 2026-10-09 category
audit (kit after-report-2026-10-09.md §8) found 9 deck and 6 kit top-200 lines more than max(1.0, 8%) off —
Embiid 24.0 against 21.1 from his shooting. The identity says a line is inconsistent, not which half is wrong:
on the 2025-26 entering pool, setting points to the implied value cut the flagged lines' points error from 2.42
to 1.98 (20 of 30 improved) but made Embiid's worse, because his shooting line was the wrong half
(arena/results/fix_backtest_2026-10-09.json). So on a projection pass (WO-5, the 10/14 lock) every listed line
is reconciled by evidence — either side may move — or carries a mechanism naming two dated outlets.

  default            both planes' top TOP lines — the deck's by adjusted value over playable rows
                     (data/players.csv), the kit's by its committed board (report/top-200-2026-27.md, lines
                     from report/projections-2026-27.csv; a kit without a board is skipped and said so) —
                     every line whose points sit more than TOL from 2·FGM + 3PM + FTM is listed. Prints the
                     ready-to-paste "Points identity" section.
  --check-report P   verify the report at P has a "Points identity" section with one table row per listed
                     player whose text names two outlets, counted with the KIT's own lexicon
                     (report/check_report.py outlet_count). Exit 1 naming every player without a row or with
                     fewer than two outlets.
  --json PATH        write the run record.
"""
import argparse
import csv
import importlib.util
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
KIT_DEFAULT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
HEADING = "Points identity"
TOP = 200
TOL = 1.0
sys.path.insert(0, HERE)
import hoops  # noqa: E402


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def implied_points(fg_pct, fga, ft_pct, fta, tpm):
    return 2.0 * fg_pct * fga + tpm + ft_pct * fta


def deck_rows(top, tol):
    P = hoops.zscores(hoops.load_players())
    live = sorted((p for p in P if hoops.availability(p) > 0), key=lambda p: -hoops.adj_value(p))
    out = []
    for rank, p in enumerate(live[:top], 1):
        imp = implied_points(p["fg_pct"], p["fga"], p["ft_pct"], p["fta"], p["tpm"])
        gap = p["pts"] - imp
        if abs(gap) > tol:
            out.append(dict(player=p["player"], plane="deck", rank=rank, pts=p["pts"], implied=round(imp, 2), gap=round(gap, 2)))
    return out, len(live[:top])


def kit_rows(kit, top, tol):
    board_path = os.path.join(kit, "report", "top-200-2026-27.md")
    csv_path = os.path.join(kit, "report", "projections-2026-27.csv")
    if not (os.path.exists(board_path) and os.path.exists(csv_path)):
        return [], 0, f"kit board not found at {os.path.relpath(board_path)} — deck plane only"
    lines = {}
    for r in csv.DictReader(open(csv_path, encoding="utf-8-sig")):
        try:
            lines[fold(r["name"])] = {k: float(r[k]) for k in ("fgp", "fga", "ftp", "fta", "tpm", "pts")}
        except (KeyError, TypeError, ValueError):
            continue
    out, n = [], 0
    for ln in open(board_path, encoding="utf-8"):
        m = re.match(r"\| (\d+) \| ([^|]+) \|", ln)
        if not m or not m.group(1).isdigit():
            continue
        rank, name = int(m.group(1)), m.group(2).strip()
        if rank > top:
            break
        d = lines.get(fold(name))
        if d is None:
            continue
        n += 1
        imp = implied_points(d["fgp"], d["fga"], d["ftp"], d["fta"], d["tpm"])
        gap = d["pts"] - imp
        if abs(gap) > tol:
            out.append(dict(player=name, plane="kit", rank=rank, pts=d["pts"], implied=round(imp, 2), gap=round(gap, 2)))
    return out, n, None


def compute(args):
    d_rows, d_n = deck_rows(args.top, args.tol)
    k_rows, k_n, k_note = kit_rows(args.kit, args.top, args.tol)
    rows = sorted(d_rows + k_rows, key=lambda r: (-abs(r["gap"]), r["player"], r["plane"]))
    players = sorted({r["player"] for r in rows}, key=fold)
    return dict(top=args.top, tol=args.tol, deck_checked=d_n, kit_checked=k_n, kit_note=k_note,
                players=len(players), lines=len(rows), player_names=players, rows=rows)


def section(rec):
    out = [f"## {HEADING} (D-1009-3)", "",
           f"Rule (owner, 2026-10-09): on a projection pass, every top-{rec['top']} line on either plane whose points sit "
           f"more than {rec['tol']:g} from its own shooting (2·FGM + 3PM + FTM, with FGM = FG% × FGA and FTM = FT% × FTA) "
           "is reconciled by evidence — either side may be the wrong half — or carries a one-line mechanism naming two "
           f"dated outlets. This pass: {rec['players']} player(s), {rec['lines']} line(s), of {rec['deck_checked']} deck and "
           f"{rec['kit_checked']} kit lines checked" + (f" ({rec['kit_note']})" if rec["kit_note"] else "") + ".", "",
           "| player | plane | rank | pts | implied (2·FGM + 3PM + FTM) | gap | mechanism (two dated outlets) |",
           "|---|---|---|---|---|---|---|"]
    for r in rec["rows"]:
        out.append(f"| {r['player']} | {r['plane']} | {r['rank']} | {r['pts']:g} | {r['implied']:.1f} | {r['gap']:+.1f} | — |")
    return "\n".join(out) + "\n"


def kit_outlet_count(kit):
    path = os.path.join(kit, "report", "check_report.py")
    if not os.path.exists(path):
        print(f"POINTS IDENTITY: STOP — the kit's outlet lexicon is missing ({path}); set KIT_REPO or --kit")
        sys.exit(2)
    spec = importlib.util.spec_from_file_location("kit_check_report", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.outlet_count


def check_report(path, rec, outlets):
    lines = open(path, encoding="utf-8").read().splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("#") and HEADING in ln), None)
    if start is None:
        print(f"POINTS IDENTITY: FAIL — no '{HEADING}' section in {os.path.basename(path)}")
        return 1
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    rows = {}
    for ln in lines[start + 1:]:
        if ln.startswith("#") and len(ln) - len(ln.lstrip("#")) <= level:
            break
        s = ln.strip()
        if s.startswith("|") and not set(s) <= set("|-: "):
            rows.setdefault(fold(s.strip("|").split("|")[0]), []).append(s)
    problems = []
    for name in rec["player_names"]:
        got = rows.get(fold(name))
        if not got:
            problems.append(f"{name}: no row")
        elif not any(outlets(r) >= 2 for r in got):
            problems.append(f"{name}: fewer than two outlets in its row")
    if problems:
        print(f"POINTS IDENTITY: FAIL — {os.path.basename(path)}: " + "; ".join(problems))
        return 1
    print(f"POINTS IDENTITY: PASS — {os.path.basename(path)}: {rec['players']} listed player(s), each with a row naming two outlets")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kit", default=KIT_DEFAULT)
    ap.add_argument("--top", type=int, default=TOP)
    ap.add_argument("--tol", type=float, default=TOL)
    ap.add_argument("--json")
    ap.add_argument("--check-report", metavar="PATH")
    args = ap.parse_args()
    rec = compute(args)
    if args.json:
        json.dump(rec, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if args.check_report:
        sys.exit(check_report(args.check_report, rec, kit_outlet_count(args.kit)))
    print(f"POINTS IDENTITY: {rec['players']} player(s), {rec['lines']} line(s) more than {rec['tol']:g} from their own shooting "
          f"({rec['deck_checked']} deck and {rec['kit_checked']} kit lines checked"
          + (f"; {rec['kit_note']}" if rec["kit_note"] else "") + ")")
    print()
    print(section(rec))


if __name__ == "__main__":
    main()
