#!/usr/bin/env python3
"""Derive per-outlet per-game CSVs (four seasons) from the raw pages in DL (untrusted; parsed as data only).
Run with python3 -I:  extract_actuals.py DL OUT
bref:  first row per player is the season total (2TM/3TM listed first); 'League Average' dropped.
espn:  byathlete pages 1..12 per season; values mapped by the page's own category name lists;
       athlete count must equal pagination.count; ids unique.
"""
import csv, glob, html as H, json, os, re, sys
DL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SEASON = {2023: "2022-23", 2024: "2023-24", 2025: "2024-25", 2026: "2025-26"}
FIELDS = ["player", "team", "gp", "mpg", "fga", "fgm", "fg_pct", "fta", "ftm", "ft_pct", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
BCOLS = [("team_name_abbr", "team"), ("games", "gp"), ("mp_per_g", "mpg"), ("fga_per_g", "fga"), ("fg_per_g", "fgm"),
         ("fg_pct", "fg_pct"), ("fta_per_g", "fta"), ("ft_per_g", "ftm"), ("ft_pct", "ft_pct"), ("fg3_per_g", "tpm"),
         ("pts_per_g", "pts"), ("trb_per_g", "reb"), ("ast_per_g", "ast"), ("stl_per_g", "stl"), ("blk_per_g", "blk"), ("tov_per_g", "tov")]

def bref(path):
    t = open(path, encoding="utf-8").read()
    out = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        if 'data-stat="name_display"' not in row:
            continue
        cells = dict(re.findall(r'<t[dh][^>]*data-stat="([^"]+)"[^>]*>(.*?)</t[dh]>', row, re.S))
        name = H.unescape(re.sub(r"<[^>]+>", "", cells.get("name_display", ""))).strip()
        if not name or name in ("Player", "League Average") or name in out:
            continue
        d = {"player": name}
        for k, v in BCOLS:
            d[v] = H.unescape(re.sub(r"<[^>]+>", "", cells.get(k, ""))).strip()
        out[name] = d
    return list(out.values())

EMAP = {"gamesPlayed": "gp", "avgMinutes": "mpg", "avgFieldGoalsAttempted": "fga", "avgFieldGoalsMade": "fgm",
        "fieldGoalPct": "fg_pct", "avgFreeThrowsAttempted": "fta", "avgFreeThrowsMade": "ftm", "freeThrowPct": "ft_pct",
        "avgThreePointFieldGoalsMade": "tpm", "avgPoints": "pts", "avgRebounds": "reb", "avgAssists": "ast",
        "avgSteals": "stl", "avgBlocks": "blk", "avgTurnovers": "tov"}

def espn(files):
    rows, ids, count = [], set(), None
    for fp in files:
        d = json.load(open(fp, encoding="utf-8"))
        count = d["pagination"]["count"]
        if not d.get("athletes"):
            continue  # a page past the last (2022-23 has 11 pages of 50 for 539 athletes)
        names = {c["name"]: c["names"] for c in d["categories"]}
        for a in d["athletes"]:
            x = a["athlete"]
            if x["id"] in ids:
                raise SystemExit(f"duplicate athlete id {x['id']} in {fp}")
            ids.add(x["id"])
            r = {"player": x["displayName"], "team": x.get("teamShortName", "")}
            for c in a["categories"]:
                for n, v in zip(names[c["name"]], c["values"]):
                    if n in EMAP:
                        r[EMAP[n]] = v
            for k in ("fg_pct", "ft_pct"):
                r[k] = f"{r[k] / 100:.4f}"
            r["gp"] = str(int(r["gp"]))
            for k in FIELDS[3:]:
                if k not in ("fg_pct", "ft_pct"):
                    r[k] = f"{float(r[k]):.4f}"
            rows.append(r)
    if len(rows) != count:
        raise SystemExit(f"espn athletes {len(rows)} != pagination.count {count}")
    return rows

def write(path, rows):
    rows = sorted(rows, key=lambda r: (r["player"], r["team"]))
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    return len(rows)

for y, season in SEASON.items():
    nb = write(os.path.join(OUT, f"bref_pergame_{season}.csv"), bref(os.path.join(DL, f"bref_{y}.html")))
    ne = write(os.path.join(OUT, f"espn_pergame_{season}.csv"), espn(sorted(glob.glob(os.path.join(DL, f"espn_{y}_p*.json")), key=lambda p: int(re.search(r"_p(\d+)", p).group(1)))))
    print(f"{season}: bref {nb} rows, espn {ne} rows")
