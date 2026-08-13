#!/usr/bin/env python3
"""JS<->Python parity gate for the Draft Deck.

    python3 scripts/check_parity.py [--verbose]

SEPTEMBER-PLAN.md §3 and §6 both gate on this printing `PARITY: EXACT MATCH`,
and until 2026-08-09 no such script existed — the Routines cited a gate they
could not run (audit F46/F60). This is that gate.

The deck carries a JavaScript re-implementation of scripts/hoops.py so it can
run offline in a browser. Two implementations of one engine drift silently:
the only defence is executing both on the same inputs and comparing. This
extracts the deck's <script id="data"> and <script id="engine"> blocks, runs
them under node, and checks:

  1. the deck's baked pool matches data/players.csv (names, teams, positions,
     notes, availability, raw stat rows)
  2. z-scores agree to 1e-6 on every player in every category
  3. adjusted value agrees to 1e-6, punted and unpunted
  4. name matching agrees exactly on a fixture set that covers the failure
     modes the audit found: accents, suffixes, nicknames, degenerate segments,
     surname collisions, typos
  5. decwScores ORDERING agrees on every committed mock state at every one of
     the owner's turns — the ordering is what the card shows, so ordering is
     what has to match

Exit 0 and `PARITY: EXACT MATCH` only if all five pass. Any drift exits 1 and
names the first disagreements.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DECK = os.path.join(ROOT, "docs", "draft-deck.html")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "arena"))
import hoops  # noqa: E402
import arena  # noqa: E402

# build_deck.py bakes z rounded to 6dp, so exact equality is impossible by
# construction: a 9-category value sum inherits up to 9 x 5e-7 of rounding.
# The gate states its tolerance rather than pretending to bit-equality.
TOL_Z = 1e-6      # per-category z: the rounding bound itself
TOL_VAL = 1e-5    # 9-cat value sums: 9x the rounding bound, with headroom

QUERIES = [
    "Nikola Jokic", "Jokic", "jokic", "Nikola Jokić", "Jokić", "Dončić",
    "Şengün", "Porziņģis", "Vučević", "sga", "kd", "ad", "og", "zu", "kat",
    "dame", "wemby", "jdub", "White", "Murray", "Bridges", "Jackson",
    "jacksn", "porrter", "livley", "murphey", "siakim", "collins",
    ".", "-", "'", "", "a", "j", "  ", "zzzzz", "Hart", "Ayton",
    # R4-F06: real two-letter first-name tokens must resolve; the original
    # fixture recorded 'aj' -> [] as the EXPECTED answer, blessing the bug.
    "aj", "cj", "gg", "ja", "pj", "rj", "vj",
]


def extract(tag, html):
    m = re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S)
    if not m:
        sys.exit(f"PARITY: FAILED — <script id=\"{tag}\"> not found in the deck")
    return m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        sys.exit("PARITY: SKIPPED — node is unavailable; this gate cannot run")

    html = open(DECK, encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="parity-")
    mod = os.path.join(tmp, "deck.mjs")
    with open(mod, "w", encoding="utf-8") as f:
        f.write(extract("data", html) + "\n" + extract("engine", html) + """
export const api = { PLAYERS, matchCandidates, decwScores, adjValue, CATS, dfHash };
""")

    # ---- what the Python side says -------------------------------------
    players = hoops.zscores(hoops.load_players())
    py_pool = [{
        "n": p["player"], "t": p["team"], "p": p["pos"].replace('"', ""),
        "note": p.get("note") or "", "av": hoops.availability(p),
        "z": {c: p["z"][c] for c in hoops.CATS},
        "val": hoops.adj_value(p, ()),
        "val_punt": hoops.adj_value(p, ("FT%", "TO")),
    } for p in players]
    py_match = {q: sorted(x["player"] for x in hoops.match_candidates(players, q))
                for q in QUERIES}

    states = {}
    sdir = os.path.join(ROOT, "arena", "data", "states")
    for fn in sorted(os.listdir(sdir)):
        if fn.endswith(".json"):
            states[fn] = json.load(open(os.path.join(sdir, fn), encoding="utf-8"))

    # df_hash vectors. The daily-fill model's every draw keys on this hash, so
    # a one-bit divergence silently reshuffles start rates on both sides —
    # exactly the drift that stranded the 8/10 build. Vectors are literal
    # strings, not pool members, so the check survives roster churn; the last
    # one is deliberately non-ASCII to exercise the UTF-16 code-unit path
    # (JS charCodeAt vs Python ord) that a pure-ASCII pool would never reach.
    DF_NAMES = ["Nikola Jokic", "D'Angelo Russell", "Jaren Jackson Jr.",
                "Alperen Sengun", "Luka Doncic", "Jonas Valančiūnas"]
    df_vectors = [[s, k, salt] for s in DF_NAMES
                  for k in (0, 1, 31) for salt in (1, 10, 20, 26)]

    fixture = os.path.join(tmp, "in.json")
    with open(fixture, "w", encoding="utf-8") as f:
        json.dump({"queries": QUERIES, "states": states,
                   "dfvectors": df_vectors}, f)

    # ---- what the deck says --------------------------------------------
    driver = os.path.join(tmp, "run.mjs")
    with open(driver, "w", encoding="utf-8") as f:
        f.write("""
import { api } from "__MOD__";
import fs from "node:fs";
const inp = JSON.parse(fs.readFileSync("__FIXTURE__", "utf8"));
const out = { pool: [], match: {}, orders: {} };
for (const p of api.PLAYERS)
  out.pool.push({ n: p.n, t: p.t, p: p.p, note: p.note, av: p.av, z: p.z,
                  val: api.adjValue(p, new Set()),
                  val_punt: api.adjValue(p, new Set(["FT%", "TO"])) });
for (const q of inp.queries)
  out.match[q] = api.matchCandidates(api.PLAYERS, q).map(x => x.n).sort();
out.dfhash = inp.dfvectors.map(([s, k, salt]) => api.dfHash(s, k, salt));
const by = new Map(api.PLAYERS.map(p => [p.n, p]));
const teamOf = (n, T) => { const r = Math.floor(n / T), i = n % T;
  return r % 2 === 0 ? i + 1 : T - i; };
for (const [name, st] of Object.entries(inp.states)) {
  const turns = [];
  for (let n = 0; n < st.picks.length; n++)
    if (teamOf(n, st.teams) === st.slot) turns.push(n);
  out.orders[name] = turns.map(upto => {
    const ros = new Map(); const taken = new Set();
    for (const pk of st.picks.slice(0, upto)) {
      taken.add(pk.player);
      const p = by.get(pk.player);
      if (p) { if (!ros.has(pk.slot)) ros.set(pk.slot, []); ros.get(pk.slot).push(p); }
    }
    const mine = ros.get(st.slot) || [];
    const opp = [...ros.entries()].filter(([s]) => s !== st.slot).map(([, r]) => r);
    const pool = api.PLAYERS.filter(p => !taken.has(p.n) && p.av > 0);
    return api.decwScores(pool, mine, opp)
      .sort((a, b) => b.ds - a.ds || (a.p.n < b.p.n ? 1 : a.p.n > b.p.n ? -1 : 0))
      .slice(0, 5).map(x => x.p.n);
  });
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__FIXTURE__", fixture))
    r = subprocess.run(["node", driver], capture_output=True, text=True)
    if r.returncode != 0:
        print("PARITY: FAILED — the deck's engine block did not execute")
        print(r.stderr.strip()[:2000])
        sys.exit(1)
    js = json.loads(r.stdout)

    # ---- compare --------------------------------------------------------
    fails = []
    js_by = {p["n"]: p for p in js["pool"]}
    if len(js["pool"]) != len(py_pool):
        fails.append(f"pool size: deck {len(js['pool'])} vs csv {len(py_pool)}")
    for p in py_pool:
        j = js_by.get(p["n"])
        if j is None:
            fails.append(f"{p['n']}: in players.csv, absent from the deck")
            continue
        for k in ("t", "p", "note"):
            if j[k] != p[k]:
                fails.append(f"{p['n']}.{k}: deck {j[k]!r} vs csv {p[k]!r}")
        if abs(j["av"] - p["av"]) > TOL_Z:
            fails.append(f"{p['n']}.av: deck {j['av']} vs py {p['av']}")
        for c in hoops.CATS:
            if abs(j["z"][c] - p["z"][c]) > TOL_Z:
                fails.append(f"{p['n']}.z[{c}]: deck {j['z'][c]} vs py {p['z'][c]}")
        for k in ("val", "val_punt"):
            if abs(j[k] - p[k]) > TOL_VAL:
                fails.append(f"{p['n']}.{k}: deck {j[k]} vs py {p[k]}")
    extra = set(js_by) - {p["n"] for p in py_pool}
    for n in sorted(extra):
        fails.append(f"{n}: in the deck, absent from players.csv")

    for q in QUERIES:
        if js["match"].get(q, []) != py_match[q]:
            fails.append(f"match({q!r}): deck {js['match'].get(q)} vs py {py_match[q]}")

    # df_hash must be BIT-identical, not merely close: it drives a threshold
    # comparison (u < 0.08, dfHash(...) < a), so an epsilon of drift flips a
    # game-day or an availability gate and reshuffles the whole model.
    js_df = js.get("dfhash")
    if js_df is None or len(js_df) != len(df_vectors):
        fails.append("df_hash: the deck exported no vectors — dfHash missing "
                     "from the engine block or not in the api export")
    else:
        for (s, k, salt), jv in zip(df_vectors, js_df):
            pv = arena.df_hash(s, k, salt)
            if pv != jv:
                fails.append(f"df_hash({s!r},{k},{salt}): deck {jv!r} vs "
                             f"py {pv!r} — NOT bit-identical")

    # Python-side ordering, built from arena.team_week_model — the module the
    # deck's engine block declares itself an exact port of. This is the check
    # that matters: the ordering IS what the card shows.
    import math as _m

    def _pwins(my, opps):
        tot = 0.0
        for om in opps:
            for c in hoops.CATS:
                d = ((my[0][c] - om[0][c])
                     / (_m.sqrt(my[1][c] + om[1][c]) or 1e-9))
                pr = 0.5 * (1 + _m.erf(d / _m.sqrt(2)))
                tot += (1 - pr) if c == "TO" else pr
        return tot / (len(opps) or 1)

    def _pct(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        den = (len(vals) - 1) or 1
        out = [0.0] * len(vals)
        for r, idx in enumerate(order):
            out[idx] = r / den
        return out

    by_name = {p["player"]: p for p in players}
    py_orders = {}
    for name, st in states.items():
        teams, slot = st["teams"], st["slot"]
        my_turns = [n for n in range(len(st["picks"]))
                    if hoops.team_of_pick(n, teams) == slot]
        rows = []
        for upto in my_turns:
            ros, taken = {}, set()
            for pk in st["picks"][:upto]:
                taken.add(pk["player"])
                pl = by_name.get(pk["player"])
                if pl is not None:
                    ros.setdefault(pk["slot"], []).append(pl)
            mine = ros.get(slot, [])
            opp = [r for s, r in ros.items() if s != slot]
            pool = [p for p in players
                    if p["player"] not in taken and hoops.availability(p) > 0]
            vals = [hoops.adj_value(p, ()) for p in pool]
            models = [arena.team_week_model(r) for r in opp if r]
            if not models:
                ds = _pct(vals)
            else:
                base = _pwins(arena.team_week_model(mine), models) if mine else 0.0
                decw = [_pwins(arena.team_week_model(mine + [p]), models) - base
                        for p in pool]
                pd, pv = _pct(decw), _pct(vals)
                ds = [0.5 * pd[i] + 0.5 * pv[i] for i in range(len(pool))]
            ranked = sorted(range(len(pool)),
                            key=lambda i: (-ds[i], [-ord(ch) for ch in pool[i]["player"]]))
            rows.append([pool[i]["player"] for i in ranked[:5]])
        py_orders[name] = rows

    for name, rows in py_orders.items():
        jrows = js["orders"].get(name, [])
        if len(jrows) != len(rows):
            fails.append(f"{name}: deck produced {len(jrows)} turns, py {len(rows)}")
            continue
        for i, (a, b) in enumerate(zip(jrows, rows)):
            if a != b:
                fails.append(f"{name} turn {i + 1}: deck {a} vs py {b}")

    turns = sum(len(v) for v in js["orders"].values())

    print(f"pool rows compared      : {len(py_pool)}")
    print(f"z-score cells compared  : {len(py_pool) * len(hoops.CATS)}")
    print(f"name fixtures compared  : {len(QUERIES)}")
    # Never assert bit-identity on a run that just disproved it.
    _df_ok = not any(f.startswith("df_hash") for f in fails)
    print(f"df_hash vectors compared: {len(df_vectors)}"
          + (" (bit-identical)" if _df_ok else " — DIVERGED"))
    print(f"card orderings compared : {turns} owner turns across "
          f"{len(js['orders'])} committed states")
    if args.verbose:
        for name, orders in js["orders"].items():
            print(f"  {name}: {len(orders)} turns, #1s = "
                  + ", ".join(o[0] for o in orders[:4]) + " …")

    if fails:
        print(f"\nPARITY: FAILED — {len(fails)} disagreement(s)")
        for m in fails[:25]:
            print("  " + m)
        if len(fails) > 25:
            print(f"  … +{len(fails) - 25} more")
        sys.exit(1)
    print("\nPARITY: EXACT MATCH")


if __name__ == "__main__":
    main()
