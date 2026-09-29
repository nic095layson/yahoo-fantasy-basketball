// Dump the deck engine's weekly-model numbers as the REFERENCE for the third
// implementation (arena/mocks/decw_third.py; system validation 2026-09-29,
// owner decision D5). For every committed draft state and every owner turn it
// records, for EVERY available candidate, the engine's ΔECW (cats/week) and
// blend score ds, plus rankCard's full ordering; and the dfHash values on the
// parity vectors. Same block extraction and turn construction as
// scripts/check_parity.py, so the turns are the parity gate's 143.
//   node arena/mocks/decw_reference.mjs <deck.html> <states_dir> <out.json>
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
const [html, statesDir, outPath] = process.argv.slice(2);
const src = fs.readFileSync(html, "utf8");
const block = tag => { const m = src.match(new RegExp(`<script id="${tag}">([\\s\\S]*?)</script>`)); if (!m) throw new Error(tag + " block missing"); return m[1]; };
const modPath = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "decwref-")), "deck.mjs");
fs.writeFileSync(modPath, block("data") + "\n" + block("engine") + "\nexport const api = { PLAYERS, decwScores, rankCard, adjValue, dfHash, teamWeekModel, dailyFillWeights, weeklyAvail, CATS };\n");
const { api } = await import("file://" + modPath);
const by = new Map(api.PLAYERS.map(p => [p.n, p]));
const teamOf = (n, T) => { const r = Math.floor(n / T), i = n % T; return r % 2 === 0 ? i + 1 : T - i; };
const out = { deck: html, turns: [], dfhash: [], roster_models: [] };
const DF_NAMES = ["Nikola Jokic", "D'Angelo Russell", "Jaren Jackson Jr.", "Alperen Sengun", "Luka Doncic", "Jonas Valančiūnas"];
for (const s of DF_NAMES) for (const k of [0, 1, 31]) for (const salt of [1, 10, 20, 26]) out.dfhash.push([s, k, salt, api.dfHash(s, k, salt)]);
for (const fn of fs.readdirSync(statesDir).sort()) {
  if (!fn.endsWith(".json")) continue;
  const st = JSON.parse(fs.readFileSync(path.join(statesDir, fn), "utf8"));
  if (!Array.isArray(st.picks)) continue;
  for (let upto = 0; upto < st.picks.length; upto++) {
    if (teamOf(upto, st.teams) !== st.slot) continue;
    const ros = new Map(); const taken = new Set();
    for (const pk of st.picks.slice(0, upto)) {
      taken.add(pk.player);
      const p = by.get(pk.player);
      if (p) { if (!ros.has(pk.slot)) ros.set(pk.slot, []); ros.get(pk.slot).push(p); }
    }
    const mine = ros.get(st.slot) || [];
    const opp = [...ros.entries()].filter(([s]) => s !== st.slot).map(([, r]) => r);
    const pool = api.PLAYERS.filter(p => !taken.has(p.n) && p.av > 0);
    const scored = api.decwScores(pool, mine, opp);
    const order = api.rankCard(scored).map(x => x.p.n);
    out.turns.push({ state: fn, upto, pickNo: upto + 1, mine: mine.map(p => p.n), oppSeats: opp.length,
      rows: scored.map(x => [x.p.n, x.decw, x.ds]), order });
    // the owner's own weekly model at this turn — mu/va per category — for a direct model check
    if (mine.length) { const m = api.teamWeekModel(mine); const w = api.dailyFillWeights(mine);
      out.roster_models.push({ state: fn, upto, mu: m.mu, va: m.va, fill: [...w.entries()] }); }
  }
}
fs.writeFileSync(outPath, JSON.stringify(out));
console.log(JSON.stringify({ turns: out.turns.length, rosterModels: out.roster_models.length, dfhash: out.dfhash.length, out: outPath }));
