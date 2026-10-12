"""Sensitivity on mock 75's #10 board: replace projected lines with 2025-26 per-game actuals (arena/results/actuals_2026-10-09,
bref + ESPN, status verified). S1: Towns only. S2: Towns, Maxey, Edwards. S3: every pool row with 2025-26 GP >= 40
(the rest, Haliburton included, keep their lines and tags). Availability tags are untouched in every variant."""
import sys, csv, copy, unicodedata, json
OUT = sys.argv[1] if len(sys.argv) > 1 else None   # usage: whatif_hk_lines2526.py <out.json>
import os
DECK=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.argv=["live_retro.py","75"]; sys.path.insert(0,DECK+"/arena/mocks")
import live_retro as lr
hoops = lr.hoops
norm=lambda x: unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower().replace('.','').replace("'",'')
A={norm(r["player"]):r for r in csv.DictReader(open(DECK+"/arena/results/actuals_2026-10-09/actuals_2025-26.csv",encoding="utf-8"))}
hoops.DATA_PATH = lr.POOLS["v58"]; raw = hoops.load_players()
F=["fg_pct","fga","ft_pct","fta","tpm","pts","reb","ast","stl","blk","tov"]
def variant(names=None, gpmin=None):
    rr = copy.deepcopy(raw); n=0
    for p in rr:
        a = A.get(norm(p["player"]))
        if not a: continue
        if (names and p["player"] in names) or (gpmin and float(a["gp"]) >= gpmin):
            for f in F: p[f] = float(a[f])
            n += 1
    return hoops.zscores(rr), n
def show(lab, P, n):
    c = lr.card(P, 9); o=[c["pool"][i]["player"] for i in c["order"]]
    top=[(o[k], round(c["ds"][c["order"][k]],4), round(c["decw"][c["order"][k]],3), round(c["vals"][c["order"][k]],2)) for k in range(6)]
    pos={nm:(o.index(nm)+1 if nm in o else None) for nm in ("Karl-Anthony Towns","Tyrese Maxey","Anthony Edwards","Tyrese Haliburton")}
    print(f"{lab} (rows replaced {n}): card ranks {pos}\n   top6 {top}", flush=True)
    return dict(label=lab, replaced=n, ranks=pos, top6=top)
out=[]
P0=hoops.zscores(copy.deepcopy(raw)); out.append(show("shipped v58 lines", P0, 0))
for lab, kw in (("S1 Towns on his 2025-26", dict(names={"Karl-Anthony Towns"})),
                ("S2 Towns, Maxey, Edwards on 2025-26", dict(names={"Karl-Anthony Towns","Tyrese Maxey","Anthony Edwards"})),
                ("S3 every row with 2025-26 GP>=40 on 2025-26", dict(gpmin=40))):
    P,n = variant(**kw); out.append(show(lab, P, n))
if OUT: json.dump(out, open(OUT, "w"), indent=1)
