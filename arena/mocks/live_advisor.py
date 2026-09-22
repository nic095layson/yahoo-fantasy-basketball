#!/usr/bin/env python3
"""Punt advisor replay for ONE live mock: at every owner turn, what the
pre-2026-09-21 advisor said (13-man z-sum ranks: FULL TILT pivot, Build-read
Adopt offer, coherence Retarget) against the room-relative read (catWinProb /
puntRead / coherenceRead, D51R-3, yahoo-fantasy-basketball PR #37), from the
deck's OWN engine block. The punt box follows the owner's logged clicks
(PUNT_TIMELINES in live_deckcard.py). Same per-turn logic as
punt_advice_effect.py (the 8-state measurement), for a state that harness
does not yet carry.

    python3 arena/mocks/live_advisor.py <mock> <deck.html | rev:<sha>:docs/draft-deck.html> <out.json>

The deck must export the D51R-3 functions (a v23 deck reports the old
advisor only).
"""
import json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from live_deckcard import PUNT_TIMELINES  # noqa: E402  (importable: module guards on __name__)

MOCK, html_path, out_path = int(sys.argv[1]), sys.argv[2], sys.argv[3]
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if html_path.startswith("rev:"):
    _rev, _p = html_path[4:].split(":", 1)
    html = subprocess.run(["git", "-C", REPO, "show", f"{_rev}:{_p}"], capture_output=True, text=True, check=True).stdout
else:
    html = open(html_path, encoding="utf-8").read()
ex = lambda tag: re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S).group(1)
state = json.load(open(os.path.join(REPO, "arena", "data", "states", f"draft_state_{MOCK}.json")))
tmp = tempfile.mkdtemp(prefix="advisor-")
mod = os.path.join(tmp, "deck.mjs")
open(mod, "w", encoding="utf-8").write(ex("data") + "\n" + ex("engine") + """
export const api = { PLAYERS, CATS, buildRosters, teamOfPick, categoryRanks, rankTiers, puntPath, totalValue,
  catWinProb: typeof catWinProb === "function" ? catWinProb : null,
  puntRead: typeof puntRead === "function" ? puntRead : null,
  coherenceRead: typeof coherenceRead === "function" ? coherenceRead : null,
  winPath: typeof winPath === "function" ? winPath : null };
""")
fixture = os.path.join(tmp, "in.json")
CLICKS = {  # (picks logged at the click, label, box the click left) — from the owner's tool log
    52: [(39, "post-click FULL TILT", ["FG%", "AST"])],
}
json.dump({"state": state, "timeline": PUNT_TIMELINES[MOCK], "clicks": CLICKS.get(MOCK, [])}, open(fixture, "w"))
driver = os.path.join(tmp, "run.mjs")
open(driver, "w", encoding="utf-8").write(r"""
import { api } from "__MOD__"; import fs from "node:fs";
const IN = JSON.parse(fs.readFileSync("__IN__", "utf8")); const { PLAYERS, CATS } = api; const st0 = IN.state;
const out = { engine: { catWinProb: !!api.catWinProb, puntRead: !!api.puntRead, coherenceRead: !!api.coherenceRead }, rows: [] };
let seen = {};
/* Evaluation moments: "pre" = the owner on the clock (picks so far = n, the
   counter ticks); "post" = right after the owner's pick (the moment the old
   buttons rendered, box as it stood BEFORE any click at that count, no tick);
   plus explicit click moments per mock (the box as the click left it). */
const points = [];
for (let n = 0; n < st0.picks.length; n++) {
  if (api.teamOfPick(n, st0.teams) !== st0.slot) continue;
  let pre = []; for (const [after, p] of IN.timeline) if (n >= after) pre = p;
  let post = []; for (const [after, p] of IN.timeline) if (n + 1 > after) post = p;
  points.push({ n, moment: "pre", punt: pre, tick: true });
  points.push({ n: n + 1, moment: "post", punt: post, tick: false });
  for (const [at, label, box] of (IN.clicks || [])) if (at === n + 1) points.push({ n: n + 1, moment: label, punt: box, tick: false });
}
for (const pt of points) {
  const n = pt.n, punt = pt.punt;
  const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt, picks: st0.picks.slice(0, n) };
  const rosters = api.buildRosters(st, PLAYERS); const mine = rosters[st.slot] || [];
  if (mine.length < 2) continue;
  const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
  const { ranks, totals } = api.categoryRanks(st, PLAYERS);
  const pw = api.catWinProb ? api.catWinProb(mine, opp) : null;
  const kept = CATS.filter(c => !punt.includes(c));
  const tiers = api.rankTiers(st.teams);
  const row = { pick: pt.moment === "pre" ? n + 1 : n, moment: pt.moment, roster: mine.length, punt, ranks, pw: pw && Object.fromEntries(CATS.map(c => [c, +pw[c].toFixed(3)])) };
  /* OLD advisor (z-sum), exactly the shipped v23 logic */
  if (!punt.length && mine.length >= 4) {
    const drift = kept.filter(c => ranks[c] >= tiers.lostFrom).sort((a, b) => ranks[b] - ranks[a]).slice(0, 3);
    if (drift.length) {
      const firm = drift.length >= 2 || ranks[drift[0]] >= st.teams;
      const path = api.puntPath(ranks, kept, drift, st.teams);
      row.old_lean = drift; row.old_fulltilt = !!(firm && path.clear); row.old_path = `${path.winnable.length}/${path.keptAfter.length}`;
    }
  }
  if (mine.length >= 5) {
    const drift = kept.filter(c => ranks[c] >= tiers.lostFrom).sort((a, b) => ranks[b] - ranks[a] || totals[st.slot][a] - totals[st.slot][b]);
    const adoptList = drift.slice(0, Math.max(0, 3 - punt.length));
    const path = adoptList.length ? api.puntPath(ranks, kept, adoptList, st.teams) : null;
    row.old_adopt = !!(adoptList.length && path.clear); row.old_adopt_set = row.old_adopt ? adoptList : [];
  }
  if (punt.length && mine.length >= 3) {
    const keptSum = arr => { const ps = new Set(arr); return mine.reduce((t, q) => t + api.totalValue(q, ps), 0); };
    const declared = keptSum(punt); let best = null;
    for (const o of punt) for (const i of CATS.filter(c => !punt.includes(c))) {
      const alt = punt.filter(c => c !== o).concat(i); const v = keptSum(alt);
      if (!best || v > best.v) best = { alt, v, out: o, inn: i };
    }
    const delta = best.v - declared;
    row.old_coh = { state: delta > 2 ? "inverted" : delta > 0.75 ? "drifting" : "aligned", out: best.out, inn: best.inn, delta: +delta.toFixed(2) };
  }
  /* NEW advisor (D51R-3), counter chained across owner turns as the app persists it */
  if (api.puntRead && pw && !punt.length && mine.length >= 4) {
    const r = api.puntRead(pw, kept, seen, pt.tick); if (pt.tick) seen = r.seen;
    row.new_lean = r.lean; row.new_advise = r.advise; row.new_set = r.advise ? r.punt : []; row.new_clear = r.clear;
    row.new_path = `${r.winnable.length}/${r.keptAfter.length}`; row.new_seen = r.seen;
  }
  if (api.coherenceRead && pw && punt.length && mine.length >= 3) {
    const c = api.coherenceRead(pw, punt);
    row.new_coh = c && { state: c.state, out: c.best && c.best.out, inn: c.best && c.best.inn, delta: +c.delta.toFixed(3), declared: +c.declared.toFixed(3) };
  }
  out.rows.push(row);
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__IN__", fixture))
r = subprocess.run(["node", driver], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:2000]
res = json.loads(r.stdout)
json.dump(res, open(out_path, "w"), indent=1)
print("engine exports:", res["engine"])
for x in res["rows"]:
    pwq = " ".join(f"{c}:{x['pw'][c]:.2f}" for c in ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]) if x["pw"] else "-"
    zq = " ".join(f"{c}:{x['ranks'][c]}" for c in ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"])
    old = (f"FULL TILT {'·'.join(x['old_lean'])} ({x['old_path']})" if x.get("old_fulltilt") else
           f"lean {x['old_lean']} no button ({x.get('old_path')})" if x.get("old_lean") else
           f"Adopt {'·'.join(x['old_adopt_set'])}" if x.get("old_adopt") else
           (f"coh {x['old_coh']['state']} → punt {x['old_coh']['inn']} for {x['old_coh']['out']} ({x['old_coh']['delta']:+.2f} fit)" if x.get("old_coh") else "-"))
    new = (f"ADVISE {'·'.join(x['new_set'])} clear={x['new_clear']} {x['new_path']}" if x.get("new_advise") else
           f"watch {x['new_lean']} seen={x['new_seen']}" if x.get("new_lean") else
           (f"coh {x['new_coh']['state']} {('punt ' + x['new_coh']['inn'] + ' for ' + x['new_coh']['out']) if x['new_coh']['inn'] else 'drop ' + x['new_coh']['out']} (+{x['new_coh']['delta']})" if x.get("new_coh") else "-"))
    print(f"#{x['pick']:>3} {x['moment']:<20} r{x['roster']:>2} punt={x['punt']!s:<14} OLD: {old:<44} NEW: {new}")
    print(f"        z-rank {zq}\n        room   {pwq}")
