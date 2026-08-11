/* E25 room generator: run a FULL mock draft with the deck's own AI.
   Env: ROOM_SEED, ROOM_SLOT, ROOM_SHARP ("1"/"0"), ROOM_OWNER_POLICY
        ("card" = shipped Top-5 #1 | "m40" = owner's mock-40 picks, card as
        fallback when a pick is gone).
   Emits one JSON line: {slot, sharp, seed, cast, picks, ownerGot}. */
const SEED = +process.env.ROOM_SEED;
const SLOT = +process.env.ROOM_SLOT;
const SHARP = process.env.ROOM_SHARP === "1";
const POLICY = process.env.ROOM_OWNER_POLICY || "card";
const TEAMS = 12, SIZE = 13;
const PUNT = (process.env.ROOM_PUNT || "").split(",").filter(Boolean);
const M40 = (process.env.ROOM_M40 || "").split("|").filter(Boolean);

const st = { teams: TEAMS, slot: SLOT, size: SIZE, punt: PUNT, picks: [], sharp: SHARP };

/* cast shuffle: identical procedure to the app's start handler */
const rngState = (SEED ^ (SLOT * 2654435761)) >>> 0;
const names = Object.keys(MANAGERS);
const crng = makeRng((rngState ^ 0x9e3779b9) >>> 0);
for (let i = names.length - 1; i > 0; i--) {
  const j = Math.floor(crng.next() * (i + 1));
  [names[i], names[j]] = [names[j], names[i]];
}
const cast = [];
{
  let i = 0;
  for (let s = 1; s <= TEAMS; s++) { if (s === SLOT) continue; cast.push([s, names[i % names.length]]); i++; }
}
st.cast = cast;
const castBySlot = new Map(cast);
const rng = makeRng(rngState);

let ownerGot = 0, ownerIdx = 0;
while (st.picks.length < TEAMS * SIZE) {
  const n = st.picks.length;
  const slot = teamOfPick(n, TEAMS);
  const pool = availablePool(st, PLAYERS);
  const rosters = buildRosters(st, PLAYERS);
  let pick = null;
  if (slot === SLOT) {
    if (POLICY === "m40" && ownerIdx < M40.length) {
      const want = M40[ownerIdx];
      const hit = pool.find(p => p.n === want);
      if (hit) { pick = hit; ownerGot++; }
      ownerIdx++;
    }
    if (!pick) {
      const oppRosters = [];
      for (let s2 = 1; s2 <= TEAMS; s2++) if (s2 !== SLOT && rosters[s2].length) oppRosters.push(rosters[s2]);
      const ds = decwScores(pool, rosters[SLOT], oppRosters);
      ds.sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0));
      pick = ds[0].p;
    }
  } else {
    const name = castBySlot.get(slot);
    const scored = managerScores(name, pool, rosters[slot],
      Math.floor(n / TEAMS) + 1, SIZE, rng, SHARP);
    pick = scored[0].p;
  }
  st.picks.push({ player: pick.n, slot });
}
console.log(JSON.stringify({ slot: SLOT, sharp: SHARP, seed: SEED, policy: POLICY,
  cast, picks: st.picks, ownerGot }));
