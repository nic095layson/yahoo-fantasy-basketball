#!/usr/bin/env python3
"""Run the deck's OWN JavaScript engine (data + engine blocks, extracted the
way check_parity.py does it) at every owner turn of draft_state_51 and emit
the card as the deck computes it: blend50 Top-5, ΔECW, the archetype TARGET
read (🎯 pin), market rank, and the survival chips (BUY NOW / TOSS-UP) with
the DOM-side survival model reproduced verbatim from the deck source.

    python3 arena/mocks/mock51_deckcard.py <deck.html | rev:<sha>:docs/draft-deck.html> <out.json> [--punt-log]

The deck the owner drafted against is v22 = docs/draft-deck.html at
e7aac6b53351f23fd2ef6c8b6c177fbccdcb428b (data and engine blocks verified
identical to the published artifact version 22).

--punt-log replays the punt box as the owner drove it in mock 51 (the log
shows the FULL TILT click after #46 and three Retarget clicks); ordering is
punt-blind by design, so only the TARGET read and chips can move.
"""
import json, os, re, subprocess, sys, tempfile

html_path, out_path = sys.argv[1], sys.argv[2]
punt_log = "--punt-log" in sys.argv
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if html_path.startswith("rev:"):
    _rev, _p = html_path[4:].split(":", 1)
    html = subprocess.run(["git", "-C", REPO, "show", f"{_rev}:{_p}"], capture_output=True, text=True, check=True).stdout
else:
    html = open(html_path, encoding="utf-8").read()


def extract(tag):
    m = re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S)
    assert m, tag
    return m.group(1)


state = json.load(open(os.path.join(REPO, "arena", "data", "states", "draft_state_51.json")))
# punt box as logged in the owner's feed (mock 51): adopted after pick 46,
# retargeted after 52, after 63, after 111
PUNT_TIMELINE = [(0, []), (46, ["AST", "FT%"]), (52, ["FT%", "TO"]), (63, ["TO", "FG%"]), (111, ["TO", "AST"])]

tmp = tempfile.mkdtemp(prefix="deckcard-")
mod = os.path.join(tmp, "deck.mjs")
with open(mod, "w", encoding="utf-8") as f:
    f.write(extract("data") + "\n" + extract("engine") + """
export const api = { PLAYERS, CATS, adjValue, decwScores, archetypeRead, categoryRanks,
  buildRosters, availablePool, marketRanks, myNextPick, familiesOf, teamOfPick, fitZ, teamWeekModel, pwinsTotal };
""")
fixture = os.path.join(tmp, "in.json")
json.dump({"state": state, "puntTimeline": PUNT_TIMELINE, "puntLog": punt_log}, open(fixture, "w"))
driver = os.path.join(tmp, "run.mjs")
with open(driver, "w", encoding="utf-8") as f:
    f.write(r"""
import { api } from "__MOD__";
import fs from "node:fs";
const inp = JSON.parse(fs.readFileSync("__FIXTURE__", "utf8"));
const { PLAYERS, CATS } = api;
const st0 = inp.state;
/* ---- DOM-side constants, reproduced verbatim from the deck ---- */
const MKT_RANK = api.marketRanks([...PLAYERS].filter(p => p.av > 0));
const VAL_RANK = (() => {
  const nw = {}; for (const c of CATS) nw[c] = 1.0;
  const byVal = [...PLAYERS].filter(p => p.av > 0).sort((a, b) => api.fitZ(b, nw).adj - api.fitZ(a, nw).adj);
  return new Map(byVal.map((p, i) => [p.n, i + 1]));
})();
const SURV_K = 0.20, SURV_FLOOR = 8, SURV_W_VAL = 9 / 11, SURV_W_MKT = 2 / 11;
function survPhi(rank, pickN) {
  if (!rank || rank >= 999) return 0.95;
  const s = (rank - pickN) / Math.max(SURV_FLOOR, SURV_K * rank);
  const x = Math.abs(s) / Math.SQRT2;
  const t = 1 / (1 + 0.3275911 * x);
  const poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))));
  const erf = 1 - poly * Math.exp(-x * x);
  const phi = 0.5 * (1 + (s < 0 ? -erf : erf));
  return Math.min(0.99, Math.max(0.01, phi));
}
function survivalP(name, pickN) {
  const pv = survPhi(VAL_RANK.get(name), pickN), pm = survPhi(MKT_RANK.get(name), pickN);
  return Math.min(0.99, Math.max(0.01, Math.pow(pv, SURV_W_VAL) * Math.pow(pm, SURV_W_MKT)));
}
const turns = [];
for (let n = 0; n < st0.picks.length; n++) if (api.teamOfPick(n, st0.teams) === st0.slot) turns.push(n);
const out = [];
for (const n of turns) {
  let punt = [];
  if (inp.puntLog) for (const [after, p] of inp.puntTimeline) if (n >= after) punt = p;
  const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt, picks: st0.picks.slice(0, n) };
  const rosters = api.buildRosters(st, PLAYERS);
  const mine = rosters[st.slot] || [];
  const oppRosters = [];
  for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) oppRosters.push(rosters[s]);
  const pool = api.availablePool(st, PLAYERS);
  const dsAll = api.decwScores(pool, mine, oppRosters)
    .sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0));
  const scored = dsAll.slice(0, 5);
  const { ranks } = api.categoryRanks(st, PLAYERS);
  const pickNo = api.myNextPick(st) ?? 0;
  let readR = null, readErr = null;
  try { readR = api.archetypeRead(st, mine, pool, ranks, pickNo, MKT_RANK); } catch (e) { readErr = String(e); }
  const pinTarget = readR && readR.fam && readR.best && !scored.some(r => api.familiesOf(r.p).includes(readR.fam))
    ? PLAYERS.find(p => p.n === readR.best) : null;
  const tgOnPin = !!(pinTarget && readR.urgent);
  /* next turn with opponent picks before it (slot 10 always has a gap) */
  const future = [];
  for (let m = n; m < st0.teams * st0.size && future.length < 4; m++) if (api.teamOfPick(m, st0.teams) === st0.slot) future.push(m + 1);
  let nextTurn = null;
  for (let i = 1; i < future.length; i++) if (future[i] > future[i - 1] + 1) { nextTurn = future[i]; break; }
  if (nextTurn === null && future.length > 1) nextTurn = future[future.length - 1];
  const priceWin = st.picks.length + st.teams * 2;
  const shelfNow = { G: 0, F: 0, C: 0 };
  for (const q of pool) if ((MKT_RANK.get(q.n) || 999) <= priceWin) for (const f of api.familiesOf(q)) shelfNow[f]++;
  const rows = scored.map((r, i) => {
    const mktR = MKT_RANK.get(r.p.n);
    let chip = null, ps = null, dying = [];
    if (mktR && nextTurn) {
      ps = survivalP(r.p.n, nextTurn);
      dying = mktR <= priceWin ? api.familiesOf(r.p).filter(f => shelfNow[f] > 0 && shelfNow[f] <= 2) : [];
      if (dying.length) chip = "BUY NOW(shelf)"; else if (ps <= 0.20) chip = "BUY NOW"; else if (ps < 0.40) chip = "TOSS-UP";
    }
    return { rank: i + 1, n: r.p.n, t: r.p.t, pos: r.p.p, ds: +r.ds.toFixed(4), decw: r.decw == null ? null : +r.decw.toFixed(4),
             val: +api.adjValue(r.p, new Set()).toFixed(3), mkt: mktR ?? null, valRank: VAL_RANK.get(r.p.n) ?? null,
             surv: ps == null ? null : +ps.toFixed(3), chip, target: (i === 0 && !tgOnPin) };
  });
  const actual = st0.picks[n].player;
  const ai = dsAll.findIndex(x => x.p.n === actual);
  out.push({ pick: n + 1, punt, actual, actualCardRank: ai < 0 ? null : ai + 1,
             actualSurv: (ai < 0 || !nextTurn) ? null : +survivalP(actual, nextTurn).toFixed(3),
             actualMkt: MKT_RANK.get(actual) ?? null, actualValRank: VAL_RANK.get(actual) ?? null,
             nextTurn, priceWin, shelfNow, rows,
             read: readR ? { fam: readR.fam ?? null, best: readR.best ?? null, urgent: !!readR.urgent, label: readR.label ?? null,
                             lastCall: readR.lastCall ?? null, keys: Object.keys(readR) } : null,
             readErr, pinTarget: pinTarget ? pinTarget.n : null, tgOnPin,
             ranks });
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__FIXTURE__", fixture))
r = subprocess.run(["node", driver], capture_output=True, text=True)
if r.returncode != 0:
    print("NODE FAILED:\n" + r.stderr[:3000])
    sys.exit(1)
res = json.loads(r.stdout)
json.dump(res, open(out_path, "w"), indent=1)
for t in res:
    top = " | ".join(f"{('🎯' if x['target'] else '')}{x['n']} ds{x['ds']:.3f} mkt{x['mkt']} s{x['surv']}{(' ' + x['chip']) if x['chip'] else ''}" for x in t["rows"])
    rd = t["read"]
    print(f"#{t['pick']:>3} punt={t['punt']} actual {t['actual']:<22} card#{t['actualCardRank']} surv{t['actualSurv']} mkt{t['actualMkt']} | "
          f"read fam={rd and rd['fam']} best={rd and rd['best']} urgent={rd and rd['urgent']} pin={t['pinTarget']} tgOnPin={t['tgOnPin']} {t['readErr'] or ''}")
    print(f"       {top}")
