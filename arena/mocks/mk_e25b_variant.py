"""Build an E25b engine variant: frame-declaring bots.
FRAME_R0 = rounds completed before a manager declares its 3-cat punt."""
import re, sys
SP = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad"
R0 = int(sys.argv[1]); out = sys.argv[2]
eng = open(f"{SP}/uB_engine.js").read()
# 1. drop the failed additive term
eng = eng.replace("    if (sharp && rnd >= SHARP_R0) s += sharpBonus(p, roster);\n", "")
# 2. frame declaration helper + frame-aware value ranking
helper = """
/* ---- E25b: frame-declaring bots (measurement variant) ----
   Once a manager has FRAME_R0 rounds of roster, it declares the 3-cat punt
   its roster best supports and values every later candidate under that
   frame (adjValue with the punt set) — a real concession, which the failed
   E25 additive term could not produce. ADP half untouched. */
const FRAME_R0 = %d;
function declaredFrame(roster) {
  if (roster.length < FRAME_R0) return null;
  const rz = {};
  for (const c of CATS) rz[c] = roster.reduce((a, q) => a + q.z[c], 0);
  const tot = CATS.reduce((a, c) => a + rz[c], 0);
  let best = null, bestZ = -Infinity;
  for (let i = 0; i < CATS.length; i++)
    for (let j = i + 1; j < CATS.length; j++)
      for (let k = j + 1; k < CATS.length; k++) {
        const z = tot - rz[CATS[i]] - rz[CATS[j]] - rz[CATS[k]];
        if (z > bestZ) { bestZ = z; best = [CATS[i], CATS[j], CATS[k]]; }
      }
  return new Set(best);
}
""" % R0
eng = eng.replace("function managerScores(mgr, pool, roster, rnd, rounds, rng, sharp) {",
                  helper + "function managerScores(mgr, pool, roster, rnd, rounds, rng, sharp) {")
old = """  const noPunt = new Set();
  const vrank = new Map([...pool].sort((a, b) => adjValue(b, noPunt) - adjValue(a, noPunt))
    .map((p, i) => [p.n, i + 1]));"""
new = """  const noPunt = new Set();
  const vset = (sharp && declaredFrame(roster)) || noPunt;
  const vrank = new Map([...pool].sort((a, b) => adjValue(b, vset) - adjValue(a, vset))
    .map((p, i) => [p.n, i + 1]));"""
assert eng.count(old) == 1
eng = eng.replace(old, new)
open(f"{SP}/{out}", "w").write(eng)
print(f"built {out} (FRAME_R0={R0})")
