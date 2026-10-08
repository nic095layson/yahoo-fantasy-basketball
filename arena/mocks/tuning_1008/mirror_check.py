#!/usr/bin/env python3
"""Read-only sketch of the MIRROR of the repeat-name check (a suggestion, not a shipped rule):
players the card never shows although the market prices them well above our value — the Flagg shape.

For every graded mock replayed on the page (the repeat-name check's --keep-cards replays), count the owner
turns at which each player was still on the board (from the saved state) and the turns at which he made
the card's Top-5. A player is listed when he was available at MIN_TURNS+ owner turns, never made the
Top-5, and the market rank the card prints sits a full round (12 places) or more ahead of his value rank.

    python3 arena/mocks/tuning_1008/mirror_check.py CARDS_DIR OUT.json
"""
import glob, json, os, re, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
CARDS, OUT = sys.argv[1:3]
MIN_TURNS, MIN_GAP = 5, 12
src = open(os.path.join(ROOT, "docs", "draft-deck.html"), encoding="utf-8").read()
data = re.search(r'<script id="data">([\s\S]*?)</script>', src).group(1)
engine = re.search(r'<script id="engine">([\s\S]*?)</script>', src).group(1)
PLAYERS = json.loads(re.search(r"const PLAYERS = (\[.*?\]);\n", data, re.S).group(1))
# value rank and market rank exactly as the card prints them: taken from the replays' own rows where the
# player appears; for players the card never shows, recompute with the replayer's engine once via node.
import subprocess, tempfile
tmp = tempfile.mkdtemp(prefix="mirror-")
mod = os.path.join(tmp, "deck.mjs")
open(mod, "w", encoding="utf-8").write(data + "\n" + engine + "\nexport const api = { PLAYERS, CATS, marketRanks, fitZ };\n")
drv = os.path.join(tmp, "run.mjs")
open(drv, "w", encoding="utf-8").write(f"""
import {{ api }} from "{mod}";
const {{ PLAYERS, CATS }} = api;
const MKT = api.marketRanks([...PLAYERS].filter(p => p.av > 0));
const nw = {{}}; for (const c of CATS) nw[c] = 1.0;
const byVal = [...PLAYERS].filter(p => p.av > 0).sort((a, b) => api.fitZ(b, nw).adj - api.fitZ(a, nw).adj);
const out = {{}};
byVal.forEach((p, i) => {{ out[p.n] = [i + 1, MKT instanceof Map ? MKT.get(p.n) : MKT[p.n], p.mkt || null]; }});
console.log(JSON.stringify(out));
""")
ranks = json.loads(subprocess.run(["node", drv], capture_output=True, text=True, check=True).stdout)
avail, shown = {}, {}
for f in sorted(glob.glob(os.path.join(CARDS, "m*.json"))):
    m = int(re.search(r"m(\d+)\.json$", f).group(1))
    turns = json.load(open(f, encoding="utf-8"))
    st = json.load(open(os.path.join(ROOT, "arena", "data", "states", f"draft_state_{m}.json"), encoding="utf-8"))
    went = {p["player"]: i + 1 for i, p in enumerate(st["picks"])}
    for t in turns:
        top5 = {r["n"] for r in t.get("rows", [])}
        for n, (vr, mr, price) in ranks.items():
            if went.get(n, 10 ** 6) >= t["pick"]:
                avail[n] = avail.get(n, 0) + 1
                if n in top5:
                    shown[n] = shown.get(n, 0) + 1
rows = []
for n, (vr, mr, price) in ranks.items():
    if price and avail.get(n, 0) >= MIN_TURNS and not shown.get(n) and vr - mr >= MIN_GAP:
        rows.append(dict(player=n, value_rank=vr, market_rank=mr, turns_available=avail[n]))
rows.sort(key=lambda r: r["market_rank"])
json.dump(dict(min_turns=MIN_TURNS, min_gap=MIN_GAP, rows=rows), open(OUT, "w"), indent=1, ensure_ascii=False)
print(f"{len(rows)} players: available at {MIN_TURNS}+ owner turns, never in the card's Top-5, market a round+ ahead")
for r in rows[:25]:
    print(f"  {r['player']:<26} market {r['market_rank']:>4}  value {r['value_rank']:>4}  available at {r['turns_available']} turns")
