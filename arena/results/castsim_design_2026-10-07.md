# D-CAST-3 — cast-bot fidelity experiment, pre-registration (2026-10-07)

This is the design header of `castsim.mjs` (the session's scratch harness, kept here verbatim) as it stood when the N=30 run started;
the driver is reproduced below the design so the run can be repeated. Three amendments were made BEFORE the N=30 run and are
recorded in the header itself (M3's reference, twice; the engine module rebuilt from the v48 page). Result file: `castsim_n30_2026-10-07.json`.

```
D-CAST-3 pre-registered fidelity experiment (2026-10-07).
Simulates MOCK rooms with the page's OWN engine (deck.mjs = data + engine blocks of the live
page): owner at slot 10 follows the card's #1 (rankCard(decwScores)), the eleven league-mates
draft with managerScores under variant scoring rules. Metrics against the ten human rooms on
file (mocks 51-54, 56-61):
  M1  mean |cast mean pick - human mean pick| over players drafted in >= 5 human rooms
  M2  human-consensus names (drafted in >= 8 of 10 human rooms) left undrafted, per room
  M3  each manager's early-round reach index vs the MARKET (pick# - full-pool market rank, rounds 1-6),
      the quantity E18 measured against the real Yahoo board (reach_early: Noah -43.5, Hegi -26.0, Robby -25.7,
      Will -16.5, Kevin -15.8, Martin -14.8, John -8.0, Kyle -7.0, JCo +4.3, Cayas +5.5, Oblena +9.3);
      reported against E18 for information only (E18's numbers were measured on a different board and
      its own doc deferred the absolute bar). THE GUARD (second amendment, also before the N=30 run):
      M3 is a regression guard on the shipped bots — a variant's per-manager reach ordering must keep
      Spearman >= 0.7 against V0's, and its mean absolute per-manager change from V0 must be <= 8. (Amended before the N=30 run:
      the first draft used the deck's value rank as the reference, which a Yahoo-rank variant fails by
      construction.) M3v = the same index vs the deck's value rank, kept for the record.
Variants:
  V0  shipped formula
  V1  late market mode: from round 9, half of val_w moves to adp_w
  V2  XRank value axis: valueRank = Yahoo XRank where present (kit yahoo-2026-10-06.csv),
      else the deck's value rank
  V3  V1 + V2
Ship rule (pre-registered): ship the variant with the best M1 that also improves M2 over V0 and
passes M3 for all eleven managers; if none improves both M1 and M2, ship nothing.
  node castsim.mjs <rooms> <out.json>
seeded gaussian rng (mulberry32 + Box-Muller) so every variant sees the same noise stream per room
a faithful copy of managerScores with the two variant hooks (late market mode; XRank value axis)
human reference
```

## Driver (castsim.mjs, verbatim)

```js
// D-CAST-3 pre-registered fidelity experiment (2026-10-07).
// Simulates MOCK rooms with the page's OWN engine (deck.mjs = data + engine blocks of the live
// page): owner at slot 10 follows the card's #1 (rankCard(decwScores)), the eleven league-mates
// draft with managerScores under variant scoring rules. Metrics against the ten human rooms on
// file (mocks 51-54, 56-61):
//   M1  mean |cast mean pick - human mean pick| over players drafted in >= 5 human rooms
//   M2  human-consensus names (drafted in >= 8 of 10 human rooms) left undrafted, per room
//   M3  each manager's early-round reach index vs the MARKET (pick# - full-pool market rank, rounds 1-6),
//       the quantity E18 measured against the real Yahoo board (reach_early: Noah -43.5, Hegi -26.0, Robby -25.7,
//       Will -16.5, Kevin -15.8, Martin -14.8, John -8.0, Kyle -7.0, JCo +4.3, Cayas +5.5, Oblena +9.3);
//       reported against E18 for information only (E18's numbers were measured on a different board and
//       its own doc deferred the absolute bar). THE GUARD (second amendment, also before the N=30 run):
//       M3 is a regression guard on the shipped bots — a variant's per-manager reach ordering must keep
//       Spearman >= 0.7 against V0's, and its mean absolute per-manager change from V0 must be <= 8. (Amended before the N=30 run:
//       the first draft used the deck's value rank as the reference, which a Yahoo-rank variant fails by
//       construction.) M3v = the same index vs the deck's value rank, kept for the record.
// Variants:
//   V0  shipped formula
//   V1  late market mode: from round 9, half of val_w moves to adp_w
//   V2  XRank value axis: valueRank = Yahoo XRank where present (kit yahoo-2026-10-06.csv),
//       else the deck's value rank
//   V3  V1 + V2
// Ship rule (pre-registered): ship the variant with the best M1 that also improves M2 over V0 and
// passes M3 for all eleven managers; if none improves both M1 and M2, ship nothing.
//   node castsim.mjs <rooms> <out.json>
import { api, VETO_LIST } from "./deck.mjs";
import fs from "fs";
const ROOMS = +process.argv[2] || 30, OUT = process.argv[3];
const TEAMS = 12, SIZE = 13, SLOT = 10;
const CAST = { 1: "Oblena", 2: "Noah", 3: "Will", 4: "Robby", 5: "Kyle", 6: "Martin", 7: "John", 8: "JCo", 9: "Kevin", 11: "Cayas", 12: "Hegi" };
const STATES = "/home/user/yahoo-fantasy-basketball/arena/data/states/";
const HUMAN = [51, 52, 53, 54, 56, 57, 58, 59, 60, 61];
const XR = new Map();
for (const line of fs.readFileSync("/home/user/fantasy-basketball-2026-27/report/market/yahoo-2026-10-06.csv", "utf8").split("\n").slice(1)) {
  if (!line.trim()) continue;
  const cols = line.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map(c => c.replace(/,$/, "").replace(/^"|"$/g, "").replace(/""/g, '"'));
  const [player, , , xrank] = cols; if (xrank) XR.set(player, +xrank);
}
// seeded gaussian rng (mulberry32 + Box-Muller) so every variant sees the same noise stream per room
function makeRng(seed) {
  let a = seed >>> 0;
  const u = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  return { random: u, gauss: (m, s) => m + s * Math.sqrt(-2 * Math.log(1 - u())) * Math.cos(2 * Math.PI * u()) };
}
const POS = p => api.positionsOf(p);
// a faithful copy of managerScores with the two variant hooks (late market mode; XRank value axis)
function scoresV(mgr, pool, roster, rnd, rounds, rng, variant) {
  const m0 = api.MANAGERS[mgr];
  let adp_w = m0.adp_w, val_w = m0.val_w;
  if ((variant === "V1" || variant === "V3") && rnd >= 9) { adp_w += val_w / 2; val_w /= 2; }
  const m = { ...m0, adp_w, val_w };
  const remaining = rounds - roster.length;
  const unfilled = api.BASE_POS.filter(b => !roster.some(p => POS(p).includes(b)));
  const mustFill = unfilled.length >= remaining;
  const mkt = api.marketRanks(pool);
  const noPunt = new Set();
  const byVal = [...pool].sort((a, b) => api.adjValue(b, noPunt) - api.adjValue(a, noPunt));
  let vrank = new Map(byVal.map((p, i) => [p.n, i + 1]));
  if (variant === "V2" || variant === "V3") {
    // XRank where Yahoo ranks the player; the deck's value rank for the rest; re-ranked among the pool
    const key = p => XR.has(p.n) ? XR.get(p.n) : 1000 + vrank.get(p.n);
    vrank = new Map([...pool].sort((a, b) => key(a) - key(b)).map((p, i) => [p.n, i + 1]));
  }
  const nStarted = [...api.lineupWeights(roster).values()].filter(w => w === 1.0).length;
  const benchBound = p => nStarted >= api.LINEUP_SLOTS.length ? false : (api.lineupWeights([...roster, p]).get(p.n) ?? api.BENCH_WEIGHT) < 1.0;
  const score = p => {
    let r = m.adp_w * (mkt.get(p.n) ?? 300) + m.val_w * (vrank.get(p.n) ?? 300);
    let bias = 1.0; for (const f of api.familiesOf(p)) if (m.bias[f]) bias *= m.bias[f];
    if (bias !== 1.0) r /= bias;
    if (m.loyal[p.n]) r = Math.max(1, r - m.loyal[p.n]);
    r *= 1 + (1 - p.av) * (m.streamer ? 0.15 : 0.35);
    if (m.noise) r *= Math.exp(rng.gauss(0, m.noise / api.MGR_NOISE_DIV));
    let s = -r; if (benchBound(p)) s -= 50.0;
    if (unfilled.length && rnd >= 6 && POS(p).some(b => unfilled.includes(b))) s += 15.0;
    return s;
  };
  let cands = pool;
  if (mustFill) { const f = pool.filter(p => unfilled.some(b => POS(p).includes(b))); if (f.length) cands = f; }
  return cands.map(p => ({ p, s: score(p) })).sort((a, b) => b.s - a.s);
}
const VETO = new Set(VETO_LIST);
function runRoom(seed, variant) {
  const rng = makeRng(seed);
  const picks = [], rosters = {}; for (let s = 1; s <= TEAMS; s++) rosters[s] = [];
  const all = api.PLAYERS.filter(p => p.av > 0);
  for (let i = 0; i < TEAMS * SIZE; i++) {
    const rnd = Math.floor(i / TEAMS) + 1, pos = i % TEAMS, seat = rnd % 2 === 1 ? pos + 1 : TEAMS - pos;
    const taken = new Set(picks.map(p => p.player));
    const pool = all.filter(p => !taken.has(p.n));
    let pick;
    if (seat === SLOT) {
      const mine = rosters[SLOT], opp = Object.entries(rosters).filter(([s]) => +s !== SLOT).map(([, r]) => r).filter(r => r.length);
      // third amendment (before the N=30 run): deck.mjs is the v48 page that ships (D-CAST-1 exclusions baked) and the
      // owner's card draws from cardPool() as the page does (D-CAST-4); V0 is therefore the shipped bots on the shipped data
      const cands = api.cardPool ? api.cardPool(pool.filter(p => !VETO.has(p.n)), rnd) : pool.filter(p => !VETO.has(p.n));
      const rows = api.rankCard(api.decwScores(cands, mine, opp));
      pick = rows[0].p;
    } else {
      pick = scoresV(CAST[seat], pool, rosters[seat], rnd, SIZE, rng, variant)[0].p;
    }
    picks.push({ player: pick.n, slot: seat }); rosters[seat].push(pick);
  }
  return picks;
}
// human reference
const humanPicks = {};
for (const m of HUMAN) {
  const st = JSON.parse(fs.readFileSync(`${STATES}draft_state_${m}.json`, "utf8"));
  st.picks.forEach((pk, i) => { (humanPicks[pk.player] ??= []).push(i + 1); });
}
const ref = Object.entries(humanPicks).filter(([, v]) => v.length >= 5).map(([n, v]) => [n, v.reduce((a, b) => a + b, 0) / v.length]);
const consensus = Object.entries(humanPicks).filter(([, v]) => v.length >= 8).map(([n]) => n);
const E18 = { Noah: -43.5, Hegi: -26.0, Robby: -25.7, Will: -16.5, Kevin: -15.8, Martin: -14.8, John: -8.0, Kyle: -7.0, JCo: 4.3, Cayas: 5.5, Oblena: 9.3 };
const fullMkt = api.marketRanks(api.PLAYERS.filter(p => p.av > 0));
function spearman(a, b) { const rk = x => { const s = [...x].map((v, i) => [v, i]).sort((p, q) => p[0] - q[0]); const r = []; s.forEach(([, i], k) => r[i] = k + 1); return r; }; const ra = rk(a), rb = rk(b), n = a.length; const d2 = ra.reduce((t, v, i) => t + (v - rb[i]) ** 2, 0); return 1 - 6 * d2 / (n * (n * n - 1)); }
const noPunt = new Set();
const fullVal = new Map([...api.PLAYERS.filter(p => p.av > 0)].sort((a, b) => api.adjValue(b, noPunt) - api.adjValue(a, noPunt)).map((p, i) => [p.n, i + 1]));
const results = {};
for (const variant of ["V0", "V1", "V2", "V3"]) {
  const castPicks = {}, undrafted = [], reach = {}, reachM = {}; for (const n of Object.values(CAST)) { reach[n] = []; reachM[n] = []; }
  for (let r = 0; r < ROOMS; r++) {
    const picks = runRoom(1000 + r, variant);
    picks.forEach((pk, i) => { (castPicks[pk.player] ??= []).push(i + 1); if (pk.slot !== SLOT && i < TEAMS * 6) { reach[CAST[pk.slot]].push((i + 1) - (fullVal.get(pk.player) ?? 300)); reachM[CAST[pk.slot]].push((i + 1) - (fullMkt.get(pk.player) ?? 300)); } });
    const drafted = new Set(picks.map(p => p.player));
    undrafted.push(consensus.filter(n => !drafted.has(n)).length);
  }
  const m1rows = ref.map(([n, h]) => { const c = castPicks[n]; return c ? Math.abs(c.reduce((a, b) => a + b, 0) / c.length - h) : null; });
  const m1 = m1rows.filter(x => x != null).reduce((a, b) => a + b, 0) / m1rows.filter(x => x != null).length;
  const neverDrafted = ref.filter(([n]) => !castPicks[n]).map(([n]) => n);
  const m3v = Object.fromEntries(Object.entries(reach).map(([n, v]) => [n, +(v.reduce((a, b) => a + b, 0) / v.length).toFixed(1)]));
  const m3 = Object.fromEntries(Object.entries(reachM).map(([n, v]) => [n, +(v.reduce((a, b) => a + b, 0) / v.length).toFixed(1)]));
  const names = Object.keys(E18); const mae = +(names.reduce((t, n) => t + Math.abs(m3[n] - E18[n]), 0) / names.length).toFixed(2);
  const rho = +spearman(names.map(n => m3[n]), names.map(n => E18[n])).toFixed(3);
  const inBand = names.filter(n => Math.abs(m3[n] - E18[n]) <= 8).length;
  const base = results.V0 ? results.V0.M3_reach_vs_market : m3;
  const guardRho = +spearman(names.map(n => m3[n]), names.map(n => base[n])).toFixed(3);
  const guardMac = +(names.reduce((t, n) => t + Math.abs(m3[n] - base[n]), 0) / names.length).toFixed(2);
  results[variant] = { rooms: ROOMS, M1_mean_abs_gap: +m1.toFixed(2), M1_players: m1rows.filter(x => x != null).length, M2_consensus_undrafted_mean: +(undrafted.reduce((a, b) => a + b, 0) / undrafted.length).toFixed(2), M2_consensus_names: consensus.length, ref_never_drafted_by_cast: neverDrafted, M3_reach_vs_market: m3, M3_mae_vs_E18: mae, M3_spearman_vs_E18: rho, M3_in_band_pm8: inBand, M3_guard_spearman_vs_V0: guardRho, M3_guard_mean_abs_change_vs_V0: guardMac, M3_guard_pass: (guardRho >= 0.7 && guardMac <= 8), M3v_reach_vs_value: m3v };
  console.log(variant, JSON.stringify(results[variant]));
}
fs.writeFileSync(OUT, JSON.stringify({ design: "D-CAST-3 pre-registered 2026-10-07", rooms: ROOMS, human_rooms: HUMAN, results }, null, 1));
```

## Amendment 4 — V4 pre-registered 2026-10-07 (after the first N=30 run's verdict, before any V4 run)

The first N=30 run shipped nothing: V2 (XRank value axis in every round) won M1 and M2 but failed the M3 guard
(Spearman 0.30 against V0's early-round reach ordering). V4 is the follow-up named in that verdict: the XRank value
axis from round 7 only; rounds 1–6 use the shipped formula unchanged. Same metrics, same human reference, same
30 seeds (1000–1029), same ship rule: ship V4 only if its M1 beats V0's (12.07), its M2 improves on V0's (10.43) and
it passes the M3 guard (Spearman ≥ 0.7 against V0 and mean absolute per-manager change ≤ 8 — which V4 passes by
construction in rounds 1–6 only if the round-7+ change does not alter earlier picks; the guard is still measured,
not assumed). Driver: `castsim.mjs 30 castsim_n30_v4_2026-10-07.json V0,V4`. Result file: `castsim_n30_v4_2026-10-07.json`.

## Amendment 5 — verdict and ship (2026-10-07, after the V4 run)

`castsim_n30_v4_2026-10-07.json`: V4 M1 9.29 (V0 12.07), M2 7.2 (V0 10.43), guard Spearman 1.0 / mean abs change 0 — passes the
pre-registered rule on every term. Shipped to the page as `BOT_XRANK_FROM = 7` in `managerScores` (the build bakes `PLAYERS[].xr`
from the kit's Yahoo file); red-first in `scripts/test_card.py` (three cases failed on the unchanged engine, all pass after).
From this build the harness's V0 is the shipped formula, so a future run must treat the round-7 XRank axis as the baseline.
