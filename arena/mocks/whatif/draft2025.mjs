// The 2025-26 league redrafted with the page's own engine: the owner at seat 4 takes the card's #1
// (rankCard(decwScores(cardPool))), the eleven profiled managers draft with managerScores (the shipped
// bots: E18 profiles, XRank value axis from round 7) in their real 2025-26 seats. N rooms, seeded.
//   node draft2025.mjs <rooms> <out.json>
import { api } from "./deck_2025.mjs";
import fs from "fs";
const ROOMS = +process.argv[2] || 30, OUT = process.argv[3];
const TEAMS = 12, SIZE = 13, SLOT = 4;
const CAST = { 1: "Hegi", 2: "JCo", 3: "Martin", 5: "Will", 6: "Kyle", 7: "Oblena", 8: "Kevin", 9: "John", 10: "Noah", 11: "Cayas", 12: "Robby" };
function makeRng(seed) {
  let a = seed >>> 0;
  const u = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  return { random: u, next: u, gauss: (m, s) => m + s * Math.sqrt(-2 * Math.log(1 - u())) * Math.cos(2 * Math.PI * u()) };
}
function runRoom(seed) {
  const rng = makeRng(seed);
  const picks = [], rosters = {}; for (let s = 1; s <= TEAMS; s++) rosters[s] = [];
  const all = api.PLAYERS.filter(p => p.av > 0);
  const cardLog = [];
  for (let i = 0; i < TEAMS * SIZE; i++) {
    const rnd = Math.floor(i / TEAMS) + 1, pos = i % TEAMS, seat = rnd % 2 === 1 ? pos + 1 : TEAMS - pos;
    const taken = new Set(picks.map(p => p.player));
    const pool = all.filter(p => !taken.has(p.n));
    let pick;
    if (seat === SLOT) {
      const mine = rosters[SLOT], opp = Object.entries(rosters).filter(([s]) => +s !== SLOT).map(([, r]) => r).filter(r => r.length);
      const cands = api.cardPool(pool, rnd);
      const rows = api.rankCard(api.decwScores(cands, mine, opp));
      pick = rows[0].p;
      cardLog.push({ pick: i + 1, top5: rows.slice(0, 5).map(r => ({ n: r.p.n, ds: +r.ds.toFixed(4), decw: r.decw == null ? null : +r.decw.toFixed(4), mkt: r.p.mkt })) });
    } else {
      pick = api.managerScores(CAST[seat], pool, rosters[seat], rnd, SIZE, rng)[0].p;
    }
    picks.push({ player: pick.n, slot: seat }); rosters[seat].push(pick);
  }
  if (new Set(picks.map(p => p.player)).size !== picks.length) throw new Error("duplicate pick");
  return { picks, cardLog };
}
const rooms = [];
for (let r = 0; r < ROOMS; r++) { const seed = 1000 + r; const { picks, cardLog } = runRoom(seed); rooms.push({ seed, picks, cardLog }); }
const mine = rooms.map(r => r.picks.filter(p => p.slot === SLOT).map(p => p.player));
const freq = {}; for (const m of mine) for (const n of m) freq[n] = (freq[n] || 0) + 1;
console.log("rooms", rooms.length, "| owner's picks in room 1000:", mine[0].join(", "));
console.log("owner picks across rooms (count of 30):", Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 30).map(([n, c]) => `${n} ${c}`).join(" | "));
fs.writeFileSync(OUT, JSON.stringify({ teams: TEAMS, size: SIZE, slot: SLOT, cast: CAST, rooms }, null, 1));
