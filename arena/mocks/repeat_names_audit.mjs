// Repeat-name bias audit (owner question, 2026-09-29): at every owner turn of a live
// room, is the card's #1 a function of THIS roster and THIS room, or does the same
// name surface regardless? For each turn the deck's own engine (data + engine blocks,
// the check_parity extraction) ranks the available pool (rankCard over decwScores,
// the veto applied) under: the owner's actual roster; each other room's owner roster
// at the same turn count (substituted in, and removed from any opponent that holds
// those men); an empty roster; value-only order; ΔECW-only order. It also records,
// for a watch-list of names, their value rank, ΔECW rank and market rank at each turn.
//   node arena/mocks/repeat_names_audit.mjs <deck.html> <states_dir> <mock> <other mocks csv> <out.json> [watch names ; separated]
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
const [html, statesDir, mockA, othersA, outPath, watchA] = process.argv.slice(2);
const src = fs.readFileSync(html, "utf8");
const block = tag => { const m = src.match(new RegExp(`<script id="${tag}">([\\s\\S]*?)</script>`)); if (!m) throw new Error(tag + " block missing"); return m[1]; };
const veto = (() => { const m = block("judgment").match(/doNotDraft:\s*\[(.*?)\]/s); return new Set(m ? [...m[1].matchAll(/"([^"]+)"/g)].map(x => x[1]) : []); })();
const modPath = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "rnaudit-")), "deck.mjs");
fs.writeFileSync(modPath, block("data") + "\n" + block("engine") + "\nexport const api = { PLAYERS, decwScores, rankCard, adjValue, marketRanks };\n");
const { api } = await import("file://" + modPath);
const by = new Map(api.PLAYERS.map(p => [p.n, p]));
const teamOf = (n, T) => { const r = Math.floor(n / T), i = n % T; return r % 2 === 0 ? i + 1 : T - i; };
const load = m => JSON.parse(fs.readFileSync(path.join(statesDir, `draft_state_${m}.json`), "utf8"));
const mock = +mockA, others = othersA.split(",").map(Number);
const watch = (watchA || "").split(";").map(s => s.trim()).filter(Boolean);
const st = load(mock), OTH = Object.fromEntries(others.map(m => [m, load(m)]));
const MKT = api.marketRanks ? api.marketRanks(api.PLAYERS) : null;
const mktRank = MKT instanceof Map ? (n => MKT.get(n) ?? null) : (n => (MKT && MKT[n]) ?? null);
const ownerRosterAt = (state, upto) => state.picks.slice(0, upto).filter(pk => pk.slot === state.slot).map(pk => by.get(pk.player)).filter(Boolean);
const out = { deck: html, mock, others, veto: [...veto], turns: [] };
function card(pool, mine, opp) {
  const scored = api.decwScores(pool, mine, opp);
  const ranked = api.rankCard(scored);
  const byVal = [...scored].sort((a, b) => api.adjValue(b.p, new Set()) - api.adjValue(a.p, new Set()) || a.p.n.localeCompare(b.p.n));
  const byDecw = [...scored].sort((a, b) => b.decw - a.decw || a.p.n.localeCompare(b.p.n));
  return { ranked, byVal, byDecw };
}
for (let upto = 0; upto < st.picks.length; upto++) {
  if (teamOf(upto, st.teams) !== st.slot) continue;
  const taken = new Set(st.picks.slice(0, upto).map(pk => pk.player));
  const ros = new Map();
  for (const pk of st.picks.slice(0, upto)) { const p = by.get(pk.player); if (!p) continue; if (!ros.has(pk.slot)) ros.set(pk.slot, []); ros.get(pk.slot).push(p); }
  const mine = ros.get(st.slot) || [];
  const oppOf = excl => [...ros.entries()].filter(([s]) => s !== st.slot).map(([, r]) => r.filter(p => !excl.has(p.n)));
  const poolAll = api.PLAYERS.filter(p => !taken.has(p.n) && p.av > 0 && !veto.has(p.n));
  const actual = card(poolAll, mine, oppOf(new Set()));
  const t = { pick: upto + 1, actual: st.picks[upto].player, mine: mine.map(p => p.n),
              card1: actual.ranked[0].p.n, top5: actual.ranked.slice(0, 5).map(x => x.p.n),
              value1: actual.byVal[0].p.n, decw1: actual.byDecw[0].p.n, alt: {}, watch: {} };
  for (const [m, s2] of Object.entries(OTH)) {
    const mine2 = ownerRosterAt(s2, upto).filter(p => !mine.some(q => q.n === p.n) || true);
    const excl = new Set(mine2.map(p => p.n));
    const pool2 = poolAll.filter(p => !excl.has(p.n));
    const c2 = card(pool2, mine2, oppOf(excl));
    t.alt[`mock${m}`] = { mine: mine2.map(p => p.n), card1: c2.ranked[0].p.n, top5: c2.ranked.slice(0, 5).map(x => x.p.n),
                          rankOfActualCard1: c2.ranked.findIndex(x => x.p.n === t.card1) + 1 || null };
  }
  const empty = card(poolAll, [], oppOf(new Set()));
  t.alt.emptyRoster = { card1: empty.ranked[0].p.n, top5: empty.ranked.slice(0, 5).map(x => x.p.n), rankOfActualCard1: empty.ranked.findIndex(x => x.p.n === t.card1) + 1 || null };
  for (const n of watch) {
    const i = actual.ranked.findIndex(x => x.p.n === n);
    if (i < 0) { t.watch[n] = null; continue; }
    t.watch[n] = { cardRank: i + 1, valueRank: actual.byVal.findIndex(x => x.p.n === n) + 1, decwRank: actual.byDecw.findIndex(x => x.p.n === n) + 1,
                   ds: +actual.ranked[i].ds.toFixed(4), decw: +actual.ranked[i].decw.toFixed(4), mkt: mktRank(n), av: by.get(n).av, poolLeft: actual.ranked.length };
  }
  out.turns.push(t);
}
fs.writeFileSync(outPath, JSON.stringify(out, null, 1));
for (const t of out.turns) {
  const alts = Object.entries(t.alt).map(([k, v]) => `${k}:${v.card1 === t.card1 ? "same" : v.card1 + "(actual#" + v.rankOfActualCard1 + ")"}`).join(" | ");
  console.log(`#${t.pick} actual ${t.actual} | card1 ${t.card1} | value1 ${t.value1} | decw1 ${t.decw1} || ${alts}`);
}
