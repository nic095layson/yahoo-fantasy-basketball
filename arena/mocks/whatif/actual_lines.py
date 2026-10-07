#!/usr/bin/env python3
"""Phase 3: the actual 2025-26 lines from Basketball-Reference, scaled by games played / 82 (no in-season moves),
written in the pool schema; coverage against the draft-time pool's names."""
import csv, json, sys, unicodedata
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad"
sys.path.insert(0, S + "/ls2025")
import bref
fold = lambda s: "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).replace(".", "").replace("'", "'").lower().strip()
ALIAS = {"jimmy butler": "jimmy butler iii", "bobby portis": "bobby portis jr", "cameron johnson": "cam johnson", "herb jones": "herbert jones", "nicolas claxton": "nic claxton", "pj washington": "pj washington"}
act = bref.parse(S + "/ls2025/dl/pergame_2026.html")
af = {}
for k, v in act.items():
    f = fold(k); af[ALIAS.get(f, f)] = v
pool = list(csv.DictReader(open(S + "/ls2025/pool_2025.csv", encoding="utf-8")))
strip = lambda f: f.replace(" jr", "").replace(" iii", "").replace(" ii", "")
out, unresolved, zero = [], [], []
for r in pool:
    f = fold(r["player"]); b = af.get(f) or af.get(ALIAS.get(f, f))
    if b is None:
        key = next((g for g in af if strip(g) == strip(f)), None); b = af.get(key) if key else None
    if b is None:
        unresolved.append(r["player"])
        if r["player"] == "Jamie Jaquez Jr.": continue   # the pool's misspelt duplicate of Jaime Jaquez Jr.
        out.append(dict(player=r["player"], team=r["team"], pos=r["pos"], fg_pct="0.000", fga=0, ft_pct="0.000", fta=0, tpm=0, pts=0, reb=0, ast=0, stl=0, blk=0, tov=0, note="", gp=0, mpg=0)); continue
    gp = b["gp"]; k = gp / 82.0
    if gp == 0: zero.append(r["player"])
    out.append(dict(player=r["player"], team=b["team"] or r["team"], pos=r["pos"], fg_pct=f"{b['fg_pct']:.3f}", fga=round(b["fga"] * k, 2), ft_pct=f"{b['ft_pct']:.3f}", fta=round(b["fta"] * k, 2),
                    tpm=round(b["tpm"] * k, 2), pts=round(b["pts"] * k, 2), reb=round(b["reb"] * k, 2), ast=round(b["ast"] * k, 2), stl=round(b["stl"] * k, 2), blk=round(b["blk"] * k, 2), tov=round(b["tov"] * k, 2),
                    note="", gp=int(gp), mpg=b["mpg"]))
print("pool rows", len(pool), "resolved", len(out), "unresolved:", unresolved)
print("zero-game men (did not play in 2025-26):", zero)
# men the draft-time pool lacks entirely are irrelevant: only drafted men are graded
with open(S + "/ls2025/pool_actual.csv", "w", encoding="utf-8", newline="") as f:
    cols = ["player","team","pos","fg_pct","fga","ft_pct","fta","tpm","pts","reb","ast","stl","blk","tov","note"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); [w.writerow(r) for r in out]
json.dump({r["player"]: dict(gp=r["gp"], mpg=r["mpg"], team=r["team"]) for r in out}, open(S + "/ls2025/actual_gp.json", "w"), indent=1)
top = sorted(out, key=lambda r: -float(r["pts"]))[:5]; print("top scorers per scheduled game:", [(r["player"], r["pts"], r["gp"]) for r in top])
