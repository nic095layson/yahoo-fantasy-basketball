#!/usr/bin/env python3
"""D51R-2 effect measurement: for every owner turn of every committed mock
state, compare the card's Top-5 under the pre-2026-09-21 order (blend50,
then name DESC) with rankCard (blend50, ΔECW, name DESC). Per-turn results on
every state, the punted mocks included (E21). Writes
arena/results/m51_tiebreak_effect.json.

    python3 arena/mocks/tiebreak_effect.py
"""
import json, os, re, subprocess, sys, tempfile
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
html = open(os.path.join(REPO, "docs", "draft-deck.html"), encoding="utf-8").read()
ex = lambda tag: re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S).group(1)
tmp = tempfile.mkdtemp()
mod = os.path.join(tmp, "deck.mjs")
open(mod, "w", encoding="utf-8").write(ex("data") + "\n" + ex("engine") + "\nexport const api = { PLAYERS, decwScores, rankCard, buildRosters, availablePool, teamOfPick };\n")
sdir = os.path.join(REPO, "arena", "data", "states")
states = {fn: json.load(open(os.path.join(sdir, fn), encoding="utf-8")) for fn in sorted(os.listdir(sdir)) if fn.endswith(".json")}
fixture = os.path.join(tmp, "in.json"); json.dump(states, open(fixture, "w"))
driver = os.path.join(tmp, "run.mjs")
open(driver, "w", encoding="utf-8").write(r"""
import { api } from "__MOD__"; import fs from "node:fs";
const S = JSON.parse(fs.readFileSync("__IN__", "utf8")); const { PLAYERS } = api;
const oldOrder = rows => [...rows].sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0));
const out = [];
for (const [name, st0] of Object.entries(S)) {
  for (let n = 0; n < st0.picks.length; n++) {
    if (api.teamOfPick(n, st0.teams) !== st0.slot) continue;
    const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt: st0.punt || [], picks: st0.picks.slice(0, n) };
    const rosters = api.buildRosters(st, PLAYERS); const mine = rosters[st.slot] || [];
    const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
    const rows = api.decwScores(api.availablePool(st, PLAYERS), mine, opp);
    const a = oldOrder(rows).slice(0, 5), b = api.rankCard(rows).slice(0, 5);
    const tied = rows.filter(r => r.ds === a[0].ds).length;
    out.push({ state: name, pick: n + 1, punt: st.punt, tiedAtTop: tied,
      old1: a[0].p.n, new1: b[0].p.n, old1decw: a[0].decw, new1decw: b[0].decw,
      top5Changed: a.map(x => x.p.n).join("|") !== b.map(x => x.p.n).join("|"),
      actual: st0.picks[n].player });
  }
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__IN__", fixture))
r = subprocess.run(["node", driver], capture_output=True, text=True); assert r.returncode == 0, r.stderr[:2000]
rows = json.loads(r.stdout)
json.dump(rows, open(os.path.join(REPO, "arena", "results", "m51_tiebreak_effect.json"), "w"), indent=1)
turns = len(rows); ties = sum(1 for x in rows if x["tiedAtTop"] > 1)
top1 = [x for x in rows if x["old1"] != x["new1"]]; top5 = sum(1 for x in rows if x["top5Changed"])
print(f"owner turns: {turns} across {len(states)} states; exact tie at #1: {ties}; Top-5 order changed: {top5}; #1 changed: {len(top1)}")
for x in top1:
    print(f"  {x['state']:<26} #{x['pick']:>3} punt={x['punt']}  #1 {x['old1']} (ΔECW {x['old1decw']:.3f}) -> {x['new1']} (ΔECW {x['new1decw']:.3f})  owner took {x['actual']}")
by = {}
for x in rows: by.setdefault(x["state"], [0, 0]); by[x["state"]][0] += 1; by[x["state"]][1] += x["old1"] != x["new1"]
print("per state (#1 changes / turns):", {k: f"{v[1]}/{v[0]}" for k, v in by.items()})
