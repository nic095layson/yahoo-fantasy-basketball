#!/usr/bin/env python3
"""Run the deck's OWN JavaScript engine (data + engine blocks, extracted the
way check_parity.py does it) at every owner turn of a live mock and emit the
card as that deck computes it: Top-5 in the deck's own order (rankCard when
the engine exports it, else the pre-2026-09-21 blend50-then-name order),
ΔECW, the archetype TARGET read and its 🎯 pin (pinDecision when exported),
market rank, and the survival model — the engine's survivalProb when the deck exports it (D51R-1R), else the room-mix blend reproduced verbatim from the DOM source
(the raw survival probability is always recorded; the chip follows the
deck's survivalChip when exported, so a deck with SURVIVAL_DISPLAY off
renders none).

    python3 arena/mocks/live_deckcard.py <mock> <deck.html | rev:<sha>:docs/draft-deck.html> <out.json> [--punt-log]

Generalized from mock51_deckcard.py (2026-09-22). --punt-log replays the
punt box as the owner drove it (PUNT_TIMELINES below); ordering is
punt-blind by design, so only the TARGET read and chips can move.
"""
import json, os, re, subprocess, sys, tempfile

MOCK, html_path, out_path = int(sys.argv[1]), sys.argv[2], sys.argv[3]
punt_log = "--punt-log" in sys.argv
PUNT_TIMELINES = {
    # mock 51: FULL TILT after #46, retargeted after 52, 63, 111
    51: [(0, []), (46, ["AST", "FT%"]), (52, ["FT%", "TO"]), (63, ["TO", "FG%"]), (111, ["TO", "AST"])],
    # mock 52: FULL TILT (FG%+AST) and an immediate Retarget to FG%+TO, both
    # right after the owner's #39; no later change logged
    52: [(0, []), (39, ["FG%", "TO"])],
    # mock 53: no punt declared and no advisor click in the tool log
    53: [(0, [])],
}
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


state = json.load(open(os.path.join(REPO, "arena", "data", "states", f"draft_state_{MOCK}.json")))
PUNT_TIMELINE = PUNT_TIMELINES[MOCK]

tmp = tempfile.mkdtemp(prefix="deckcard-")
mod = os.path.join(tmp, "deck.mjs")
with open(mod, "w", encoding="utf-8") as f:
    f.write(extract("data") + "\n" + extract("engine") + """
export const api = { PLAYERS, CATS, adjValue, decwScores, archetypeRead, categoryRanks,
  buildRosters, availablePool, marketRanks, myNextPick, familiesOf, teamOfPick, fitZ, teamWeekModel, pwinsTotal,
  rankCard: typeof rankCard === "function" ? rankCard : null,
  pinDecision: typeof pinDecision === "function" ? pinDecision : null,
  survivalChip: typeof survivalChip === "function" ? survivalChip : null,
  survivalProb: typeof survivalProb === "function" ? survivalProb : null,
  SURVIVAL_DISPLAY: typeof SURVIVAL_DISPLAY === "undefined" ? null : SURVIVAL_DISPLAY };
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
/* D51R-1R (2026-09-22): a deck that exports survivalProb prices survival off the
   baked Yahoo price (else the market-rank position); older decks keep the
   room-mix blend reproduced above, so pre-refit cards replay unchanged. */
const byName = new Map(PLAYERS.map(p => [p.n, p]));
function survivalP(name, pickN) {
  if (api.survivalProb) {
    const p = byName.get(name);
    return api.survivalProb(p && p.mkt != null ? p.mkt : MKT_RANK.get(name), pickN);
  }
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
  const raw = api.decwScores(pool, mine, oppRosters);
  const dsAll = api.rankCard ? api.rankCard(raw)
    : [...raw].sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0));
  const scored = dsAll.slice(0, 5);
  const { ranks } = api.categoryRanks(st, PLAYERS);
  const pickNo = api.myNextPick(st) ?? 0;
  let readR = null, readErr = null;
  try { readR = api.archetypeRead(st, mine, pool, ranks, pickNo, MKT_RANK); } catch (e) { readErr = String(e); }
  const pinTarget = readR && readR.fam && readR.best && !scored.some(r => api.familiesOf(r.p).includes(readR.fam))
    ? PLAYERS.find(p => p.n === readR.best) : null;
  let tgOnPin = !!(pinTarget && readR && readR.urgent), withheld = "";
  if (api.pinDecision) {
    const d = api.pinDecision(readR, scored, pinTarget, nm => { const r = dsAll.find(x => x.p.n === nm); return r ? r.decw : null; });
    tgOnPin = d.tgOnPin; withheld = d.withheld;
  }
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
      if (api.survivalChip) chip = api.survivalChip(ps, dying);
      else if (dying.length) chip = "BUY NOW(shelf)"; else if (ps <= 0.20) chip = "BUY NOW"; else if (ps < 0.40) chip = "TOSS-UP";
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
             readErr, pinTarget: pinTarget ? pinTarget.n : null, tgOnPin, withheld,
             engine: { rankCard: !!api.rankCard, pinDecision: !!api.pinDecision, survivalDisplay: api.SURVIVAL_DISPLAY },
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
