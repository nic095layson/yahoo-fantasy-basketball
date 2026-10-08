#!/usr/bin/env python3
"""Derive per-game CSVs from the Basketball-Reference per-game tables the 2025-26 what-if downloaded on
2026-10-07 (untrusted HTML, parsed as data only; the first row per player is the season total — B-Ref
lists the 2TM/3TM row first). Run with python3 -I.

    python3 -I arena/mocks/tuning_1008/bref_extract.py pergame_2025.html pergame_2026.html OUTDIR
writes OUTDIR/bref_pergame_2024-25.csv and OUTDIR/bref_pergame_2025-26.csv
"""
import csv, html as H, os, re, sys
COLS = [("age", "age"), ("team_name_abbr", "team"), ("games", "gp"), ("mp_per_g", "mpg"), ("fga_per_g", "fga"),
        ("fg_pct", "fg_pct"), ("fta_per_g", "fta"), ("ft_pct", "ft_pct"), ("fg3_per_g", "tpm"), ("pts_per_g", "pts"),
        ("trb_per_g", "reb"), ("ast_per_g", "ast"), ("stl_per_g", "stl"), ("blk_per_g", "blk"), ("tov_per_g", "tov")]


def parse(path):
    t = open(path, encoding="utf-8").read()
    out = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        if 'data-stat="name_display"' not in row:
            continue
        cells = dict(re.findall(r'<t[dh][^>]*data-stat="([^"]+)"[^>]*>(.*?)</t[dh]>', row, re.S))
        name = H.unescape(re.sub(r"<[^>]+>", "", cells.get("name_display", ""))).strip()
        if not name or name == "Player" or name in out:
            continue
        d = {"player": name}
        for k, v in COLS:
            raw = H.unescape(re.sub(r"<[^>]+>", "", cells.get(k, ""))).strip()
            d[v] = raw
        out[name] = d
    return list(out.values())


a, b, outdir = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
for src, season in ((a, "2024-25"), (b, "2025-26")):
    rows = parse(src)
    with open(os.path.join(outdir, f"bref_pergame_{season}.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["player"] + [v for _, v in COLS])
        w.writeheader()
        w.writerows(rows)
    print(f"{season}: {len(rows)} players")
