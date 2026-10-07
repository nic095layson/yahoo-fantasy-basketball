#!/usr/bin/env python3
"""Phase 1: the draft-time pool (2025-10-21 + the eight missing late picks on their 2024-25 lines), Yahoo's pre-draft
ranks as the market, the real 2025-26 draft as a state, and a deck module (v49 engine + this pool) for the draft runner."""
import csv, json, re, sys, unicodedata, os
S = "/tmp/claude-0/-home-user-fantasy-basketball-2026-27/3cdbbd9b-02dd-585e-8d00-b8a370128fae/scratchpad"
D = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, S + "/ls2025"); sys.path.insert(0, D + "/scripts")
import bref
fold = lambda s: "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).replace(".", "").replace("'", "'").lower().strip()
ALIAS = {"jimmy butler": "jimmy butler iii", "bobby portis": "bobby portis jr", "cameron johnson": "cam johnson"}
# ---- the real 2025-26 draft -> state (seat per pick from the round-1 order; snake)
txt = open(D + "/arena/data/league_draft_2025-26_raw_2026-10-01.txt", encoding="utf-8").read()
rounds = re.split(r"^Round (\d+)\s*$", txt, flags=re.M)
MGR = {"JAMAL AL-QUETA": "David", "Gotta Be Bamonte": "Robby", "HalleLuka Amen": "Martin", "Itsy Bitsy Spida": "Oblena", "All guards no defense": "Kevin",
       "Devin Minutes in Heaven": "Noah", "IM SO HORT": "Cayas", "John's Cool Team": "John", "Not hurt just SARR": "Hegi", "The Konclave": "Will",
       "ur my only hope Anti-wan": "Kyle", "Wing Chun Wemby": "JCo"}
picks = []
for i in range(1, len(rounds), 2):
    rnd = int(rounds[i])
    for m in re.finditer(r"^(\d+)\.\t(.+?)\n\((.+?)\)\n(.+?)$", rounds[i + 1], flags=re.M):
        k = int(m.group(1)); seat = k if rnd % 2 == 1 else 13 - k
        picks.append(dict(round=rnd, pick=(rnd - 1) * 12 + k, player=m.group(2).strip(), seat=seat, team_name=m.group(4).strip(), manager=MGR[m.group(4).strip()]))
assert len(picks) == 156 and [p["pick"] for p in picks] == list(range(1, 157))
seat_of = {p["seat"]: p["manager"] for p in picks if p["round"] == 1}
assert seat_of[4] == "David", seat_of
# ---- the draft-time pool
rows = list(csv.DictReader(open(D + "/arena/data/players_2025-10-21.csv", encoding="utf-8")))
byf = {fold(r["player"]): r for r in rows}
def resolve(name):
    f = fold(name)
    if f in byf: return byf[f]["player"]
    if ALIAS.get(f) in byf: return byf[ALIAS[f]]["player"]
    # suffix-insensitive
    for g, r in byf.items():
        if g.replace(" jr", "").replace(" iii", "").replace(" ii", "") == f.replace(" jr", "").replace(" iii", "").replace(" ii", ""): return r["player"]
    return None
missing = [p["player"] for p in picks if resolve(p["player"]) is None]
print("drafted names missing from the 2025-10-21 pool:", missing)
prior = bref.parse(S + "/ls2025/dl/pergame_2025.html")
pf = {fold(k): v for k, v in prior.items()}
added = []
for name in missing:
    f = fold(name); key = f if f in pf else next((g for g in pf if g.replace(" jr", "").replace(" iii", "") == f.replace(" jr", "").replace(" iii", "")), None)
    if not key:
        assert name == "Yang Hansen", ("no 2024-25 line for", name)
        b = dict(team="POR", pos="C", fg_pct=0.500, fga=6.0, ft_pct=0.650, fta=1.5, tpm=0.2, pts=7.0, reb=5.0, ast=1.5, stl=0.5, blk=0.8, tov=1.3, gp=0)  # 2025 rookie, no NBA line: late-round rookie-center placeholder
    else: b = pf[key]
    rows.append(dict(player=name, team=b["team"], pos=b["pos"], fg_pct=f"{b['fg_pct']:.3f}", fga=b["fga"], ft_pct=f"{b['ft_pct']:.3f}", fta=b["fta"], tpm=b["tpm"], pts=b["pts"], reb=b["reb"], ast=b["ast"], stl=b["stl"], blk=b["blk"], tov=b["tov"], note=("rookie-proj (placeholder, no NBA line)" if name == "Yang Hansen" else "added 2024-25 B-Ref line (not in the 2025-10-21 pool)")))
    added.append((name, b["team"], b["pos"], b["gp"], b["pts"]))
print("added on 2024-25 lines:", added)
# B-Ref positions are PG/SG/SF/PF/C single or "SG-SF" — convert to the pool's "SG,SF" style
for r in rows:
    r["pos"] = r["pos"].replace("-", ",")
P = S + "/ls2025/pool_2025.csv"
with open(P, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
byf = {fold(r["player"]): r for r in rows}
state_picks = [dict(player=resolve(p["player"]), slot=p["seat"]) for p in picks]
assert all(pk["player"] for pk in state_picks)
json.dump(dict(teams=12, slot=4, size=13, punt=[], picks=state_picks, cast=[[s, n] for s, n in sorted(seat_of.items()) if s != 4]), open(S + "/ls2025/draft_state_real_2025.json", "w"), indent=1)
json.dump(dict(seat_of=seat_of, picks=picks), open(S + "/ls2025/real_draft_2025.json", "w"), indent=1, ensure_ascii=False)
# ---- Yahoo pre-draft ranks (Dan Titus 10/16) -> market
mkt = {}
for line in open(D + "/arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt", encoding="utf-8"):
    m = re.match(r"^(\d+)\t(.+?) \([A-Z]{2,3} - [A-Z,]+\)\t(\d+)", line)
    if m:
        nm = resolve(m.group(2))
        if nm: mkt[nm] = int(m.group(1))
print("market ranks resolved:", len(mkt), "of 200")
# ---- PLAYERS array in the page's shape (z via hoops.zscores on this pool, availability via hoops.availability)
import hoops
hoops.DATA_PATH = P
players = hoops.zscores(hoops.load_players())
CATS = hoops.CATS
PL = []
for p in players:
    PL.append(dict(n=p["player"], t=p["team"], p=p["pos"], note=p.get("note") or "", av=hoops.availability(p), mkt=mkt.get(p["player"]), mktsrc="ADP" if p["player"] in mkt else None,
                   xr=mkt.get(p["player"]), z={c: round(p["z"][c], 6) for c in CATS},
                   r=[p["tpm"], p["pts"], p["reb"], p["ast"], p["stl"], p["blk"], p["tov"], p["fg_pct"], p["fga"], p["ft_pct"], p["fta"]], ar=None, fx=[], sy=0))
print("PLAYERS", len(PL), "priced", sum(1 for p in PL if p["mkt"]), "av<1", [(p["n"], p["av"]) for p in PL if p["av"] < 1][:12], "...")
html = open(S + "/m67/page_v49.html", encoding="utf-8").read()
data = re.search(r'<script id="data">(.*?)</script>', html, re.S).group(1)
engine = re.search(r'<script id="engine">(.*?)</script>', html, re.S).group(1)
data2 = re.sub(r"const PLAYERS = \[.*?\];", "const PLAYERS = " + json.dumps(PL, ensure_ascii=False) + ";", data, count=1, flags=re.S)
assert data2 != data
tail = open(S + "/dcast3/deck.mjs", encoding="utf-8").read().split("\nexport const VETO_LIST")[1]
mod = data2 + "\n" + engine + "\nexport const VETO_LIST=[];\nexport const api={PLAYERS,CATS,MANAGERS,MGR_NOISE_DIV,BASE_POS,LINEUP_SLOTS,BENCH_WEIGHT,marketRanks,adjValue,managerScores,positionsOf,familiesOf,lineupWeights,decwScores,rankCard,cardPool,CARD_PRICED_FROM,teamOfPick,BOT_XRANK_FROM};\n"
open(S + "/ls2025/deck_2025.mjs", "w", encoding="utf-8").write(mod)
print("deck_2025.mjs written", len(mod))
