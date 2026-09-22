#!/usr/bin/env python3
"""Insert-at-# integrity test (mock 53, 2026-09-22 — owner: "when I use the insert
at # function, is the tool assigning the players to the right team, and is the
categorical computation still accurate?").

Replays the owner's whole tool log (every feed / insert / undo, in order) through
the deck ENGINE headlessly (state A), builds the same board from scratch in the
Yahoo recap's order (state B), and compares what the deck computes from each:
picks and seats, every roster, every seat's category ranks, the category matrix,
and the ΔECW card ordering at all 13 owner turns. Also runs the Python engine's
insert_pick on the exact pre-insert boards and checks it produces the JS result.

    python3 arena/mocks/insert_integrity.py <deck.html> <events.json> <truth.json> <out.json>
"""
import json, os, subprocess, sys, tempfile, re
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts")); import hoops  # noqa: E402
html_path, ev_path, truth_path, out_path = sys.argv[1:5]
html = open(html_path, encoding="utf-8").read()
def extract(tag):
    m = re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S); assert m, tag; return m.group(1)
tmp = tempfile.mkdtemp(prefix="insint-"); mod = os.path.join(tmp, "deck.mjs")
open(mod, "w", encoding="utf-8").write(extract("data") + "\n" + extract("engine") + """
export const api = { PLAYERS, CATS, processFeed, insertPick, matchCandidates, buildRosters, categoryRanks,
  decwScores, availablePool, teamOfPick, myNextPick, adjValue, rankCard: typeof rankCard === "function" ? rankCard : null };
""")
driver = os.path.join(tmp, "run.mjs")
open(driver, "w", encoding="utf-8").write(r"""
import { api } from "__MOD__";
import fs from "node:fs";
const { PLAYERS, CATS } = api;
const events = JSON.parse(fs.readFileSync("__EV__", "utf8"));
const truth = JSON.parse(fs.readFileSync("__TRUTH__", "utf8")).truth;
const teams = 12, size = 13, slot = 10;
const snap = st => st.picks.map(p => ({ player: p.player, slot: p.slot }));
// ---- state A: the owner's session, event by event ----
const A = { teams, slot, size, punt: [], picks: [] };
const steps = [], preInserts = [];
for (const ev of events) {
  let lines;
  if (ev.op === "feed") lines = api.processFeed(A, PLAYERS, ev.text).lines;
  else if (ev.op === "insert") { preInserts.push({ P: ev.P, name: ev.text, picksBefore: snap(A) }); lines = api.insertPick(A, PLAYERS, ev.P, ev.text).lines; }
  else if (ev.op === "undo") { const last = A.picks.pop(); lines = [{ t: `  ↶ undid: ${last.player} (Seat ${last.slot})` }]; }
  const echoOK = lines.some(l => l.t.includes(ev.expect));
  steps.push({ op: ev.op, text: ev.text ?? null, P: ev.P ?? null, expect: ev.expect, echoOK, n: A.picks.length, picks: snap(A) });
}
// ---- state B: from scratch in Yahoo order (names resolved by the deck's own resolver) ----
const B = { teams, slot, size, punt: [], picks: [] }; const resolve = [];
for (let i = 0; i < truth.length; i++) {
  const taken = new Set(B.picks.map(p => p.player));
  let c = api.matchCandidates(PLAYERS, truth[i].yahoo).filter(p => !taken.has(p.n));
  if (c.length !== 1) { const alt = truth[i].yahoo.replace(/ (III|Jr\.|II)$/, ""); c = api.matchCandidates(PLAYERS, alt).filter(p => !taken.has(p.n)); }
  if (c.length !== 1) { const alt = truth[i].yahoo.replace(/\./g, ""); c = api.matchCandidates(PLAYERS, alt).filter(p => !taken.has(p.n)); }  // Yahoo "P.J." vs pool "PJ": the feed resolver keeps dots (noted, out of scope here)
  resolve.push({ i: i + 1, yahoo: truth[i].yahoo, n: c.length, name: c.length === 1 ? c[0].n : null, cands: c.slice(0, 4).map(p => p.n) });
  B.picks.push({ player: c.length === 1 ? c[0].n : `UNRESOLVED ${truth[i].yahoo}`, slot: api.teamOfPick(i, teams) });
}
// ---- prefix consistency of A with B after every event ----
const truthNames = B.picks.map(p => p.player);
for (const s of steps) s.prefixOfTruth = s.picks.every((p, i) => p.player === truthNames[i] && p.slot === B.picks[i].slot);
// ---- computations from A vs B ----
const same = (x, y) => JSON.stringify(x) === JSON.stringify(y);
const rosterOf = st => { const r = api.buildRosters(st, PLAYERS); const o = {}; for (const s of Object.keys(r)) o[s] = r[s].map(p => p.n); return o; };
const ranksOf = st => api.categoryRanks(st, PLAYERS);
const matrixOf = st => { const r = api.buildRosters(st, PLAYERS); const m = {}; for (const s of Object.keys(r)) { m[s] = {}; for (const c of CATS) m[s][c] = +r[s].reduce((t, p) => t + p.z[c], 0).toFixed(9); } return m; };
const cardAt = (st, n) => { const pre = { ...st, picks: st.picks.slice(0, n) }; const r = api.buildRosters(pre, PLAYERS); const mine = r[slot] || [];
  const opp = []; for (let s = 1; s <= teams; s++) if (s !== slot && r[s] && r[s].length) opp.push(r[s]);
  const pool = api.availablePool(pre, PLAYERS); let rows = api.decwScores(pool, mine, opp); if (api.rankCard) rows = api.rankCard(rows);
  return rows.slice(0, 10).map(x => [x.p.n, +x.ds.toFixed(6), x.decw == null ? null : +x.decw.toFixed(6)]); };
const ownerTurns = []; for (let n = 0; n < teams * size; n++) if (api.teamOfPick(n, teams) === slot) ownerTurns.push(n);
const out = {
  picksEqual: same(snap(A), snap(B)), nA: A.picks.length, nB: B.picks.length,
  firstDiff: snap(A).findIndex((p, i) => !B.picks[i] || p.player !== B.picks[i].player || p.slot !== B.picks[i].slot),
  rostersEqual: same(rosterOf(A), rosterOf(B)), ranksEqual: same(ranksOf(A), ranksOf(B)), matrixEqual: same(matrixOf(A), matrixOf(B)),
  ranksA: ranksOf(A), matrixA: matrixOf(A), ownerRoster: rosterOf(A)[slot], rostersA: rosterOf(A),
  cardsEqual: ownerTurns.every(n => same(cardAt(A, n), cardAt(B, n))), ownerTurns: ownerTurns.map(n => n + 1),
  cardsA: Object.fromEntries(ownerTurns.map(n => [n + 1, cardAt(A, n)])),
  unresolved: resolve.filter(r => r.n !== 1), steps, preInserts, echoMisses: steps.filter(s => !s.echoOK).length,
  notPrefixSteps: steps.map((s, k) => [k, s.op, s.text, s.n, s.prefixOfTruth]).filter(x => !x[4]),
};
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__EV__", ev_path).replace("__TRUTH__", truth_path))
js = json.loads(subprocess.run(["node", driver], capture_output=True, text=True, check=True).stdout)
# ---- Python engine: insert_pick on the exact pre-insert boards must reproduce the JS result ----
players = hoops.zscores(hoops.load_players())
py_inserts = []
for pi in js["preInserts"]:
    st = {"teams": 12, "slot": 10, "size": 13, "punt": [], "picks": [dict(p) for p in pi["picksBefore"]]}
    try:
        res = hoops.insert_pick(st, players, pi["P"], pi["name"]); ok, text = True, str(res)[:200]
    except (ValueError, SystemExit) as e:   # the Python engine refuses by raising; the JS returns a warn line
        ok, text = False, str(e)[:200]
    py_inserts.append({"P": pi["P"], "name": pi["name"], "ok": ok, "picks_after": st["picks"], "text": text})
# compare each Python post-insert board with the JS board after the same event
js_after = [s["picks"] for s in js["steps"] if s["op"] == "insert"]
py_vs_js = [{"P": p["P"], "name": p["name"], "py_ok": p["ok"], "board_equal": p["picks_after"] == a} for p, a in zip(py_inserts, js_after)]
# Python rosters/ranks from the final board vs the JS numbers
final = {"teams": 12, "slot": 10, "size": 13, "punt": [], "picks": js["steps"][-1]["picks"]}
py_rosters = {str(k): [p["player"] for p in v] for k, v in hoops.build_rosters(final, players).items()}
cr = getattr(hoops, "category_ranks", None) or getattr(hoops, "my_category_ranks", None)
py_ranks = cr(final, players) if cr else None
out = {"mock": 53, "deck": html_path, "js": {k: js[k] for k in ("picksEqual", "nA", "nB", "firstDiff", "rostersEqual", "ranksEqual", "matrixEqual", "cardsEqual", "ownerTurns", "echoMisses", "notPrefixSteps", "unresolved", "ownerRoster")},
       "python": {"insert_pick_vs_js": py_vs_js, "rosters_equal_js": py_rosters == js["rostersA"], "owner_ranks_equal_js": (py_ranks[0] == js["ranksA"]["ranks"]) if isinstance(py_ranks, tuple) else None,
                  "totals_equal_js": all(abs(py_ranks[1][int(t)][c] - js["ranksA"]["totals"][t][c]) < 1e-9 for t in js["ranksA"]["totals"] for c in hoops.CATS) if isinstance(py_ranks, tuple) and isinstance(js["ranksA"].get("totals"), dict) else None},
       "cardsA": js["cardsA"], "ranksA": js["ranksA"], "matrixA": js["matrixA"], "steps": js["steps"], "py_inserts": py_inserts, "py_owner_ranks": py_ranks[0] if isinstance(py_ranks, tuple) else py_ranks}
json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
print(json.dumps(out["js"], ensure_ascii=False)[:1200]); print("python:", out["python"]); print("shapes: js ranksA keys", list(js["ranksA"].keys()) if isinstance(js["ranksA"], dict) else type(js["ranksA"]).__name__, "| py_ranks", type(py_ranks).__name__, str(py_ranks)[:160])
