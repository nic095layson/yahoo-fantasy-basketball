"""Usage: python3 arena/mocks/whatif_hk_aggregate.py <folder>
Combine the per-room arms with survival odds. E[Towns first] = pH*both + (1-pH)*K_noH ; E[Haliburton first] = pK*both + (1-pK)*H_noK."""
import json, glob, statistics as st
import sys
S=sys.argv[1]   # a folder of whatif_hk.py room files (m<mock>.json)
rooms=[json.load(open(f)) for f in sorted(glob.glob(S+"/m*.json"), key=lambda f:int(f.split("/m")[-1][:-5]))]
rows=[]
for r in rooms:
    a=r["arms"]; m=r["mock"]
    kno=st.mean([a["K_noH_11"]["champ"], a["K_noH_14"]["champ"]]); hno=st.mean([a["H_noK_11"]["champ"], a["H_noK_14"]["champ"]])
    rows.append(dict(mock=m, ad=a["as_drafted"]["champ"], both=a["both"]["champ"], K_noH=kno, H_noK=hno,
        k15=a["K_noH_11"]["card15"][0][0], h15=a["H_noK_11"]["card15"][0][0],
        k15b=a["K_noH_14"]["card15"][0][0], h15b=a["H_noK_14"]["card15"][0][0],
        owner=(r["owner10"], r["owner15"]), where=r["where"], missing=r["missing_from_v58"]))
print(f"{'room':5} {'owner #10 / #15':42} {'as drafted':>10} {'both':>7} {'Towns, no Hali':>14} {'Hali, no Towns':>14}  card #15 fallbacks")
for x in rows:
    print(f"m{x['mock']:<4} {x['owner'][0].split()[-1]+' / '+x['owner'][1].split()[-1]:42} {x['ad']:10.2f} {x['both']:7.2f} {x['K_noH']:14.2f} {x['H_noK']:14.2f}  K-path {x['k15']}/{x['k15b']} · H-path {x['h15']}/{x['h15b']}" + (f"  missing {x['missing']}" if x['missing'] else ""))
mb, mk, mh = st.mean(x["both"] for x in rows), st.mean(x["K_noH"] for x in rows), st.mean(x["H_noK"] for x in rows)
print(f"\nmeans over {len(rows)} rooms: both {mb:.2f} | Towns + fallback {mk:.2f} (cost of losing Haliburton {mk-mb:+.2f}) | Haliburton + fallback {mh:.2f} (cost of losing Towns {mh-mb:+.2f})")
r2=[x for x in rows if x["mock"]!=51]
print(f"without mock 51 (the K-path fallback there is the owner's own #10, Edwards): both {st.mean(x['both'] for x in r2):.2f} | Towns + fallback {st.mean(x['K_noH'] for x in r2):.2f} | Haliburton + fallback {st.mean(x['H_noK'] for x in r2):.2f}")
print("rooms where losing Towns costs more than losing Haliburton:", sum(1 for x in rows if x["H_noK"] < x["K_noH"]), "of", len(rows))
def E(pK, pH):
    eK = st.mean(pH*x["both"] + (1-pH)*x["K_noH"] for x in rows); eH = st.mean(pK*x["both"] + (1-pK)*x["H_noK"] for x in rows)
    return eK, eH
for lab, pK, pH in (("human public rooms on record (Towns 6 of 6, Haliburton 3 of 11)", 1.0, 3/11),
                    ("the deck's survival model at #10, v59 prices (Towns 0.53, Haliburton 0.43)", 0.53, 0.43),
                    ("the league cast on the real seating (Cayas took Towns at #11 both times; Haliburton 0.43 from the model)", 0.0, 0.43)):
    eK, eH = E(pK, pH); print(f"{lab}: Towns first {eK:.2f}, Haliburton first {eH:.2f}, difference {eH-eK:+.2f}")
# break-even pK for each pH
for pH in (3/11, 0.43, 0.6):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid=(lo+hi)/2; eK, eH = E(mid, pH)
        if eH < eK: lo=mid
        else: hi=mid
    print(f"break-even: with Haliburton's survival at {pH:.2f}, Haliburton first wins once Towns survives to #15 with probability >= {hi:.2f}")
json.dump(dict(rows=rows, means=dict(both=mb, K_noH=mk, H_noK=mh)), open(S+"/aggregate.json","w"), indent=1)
