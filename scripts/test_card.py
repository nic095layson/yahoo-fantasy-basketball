#!/usr/bin/env python3
"""Card-governance regression suite (mock 51 retro, 2026-09-21).

    python3 scripts/test_card.py

Runs the deck's OWN engine block under node (the check_parity extraction)
and pins three behaviours the retro found wrong or undefined:

  D51R-2  rankCard: exact blend ties order by ΔECW before name
  D51R-4  pinDecision: the urgent TARGET takes the 🎯 only at availability
          1.0 and within PIN_MAX_GAP cats/week of #1 — measured on the
          committed states (state_51 #58 blocked, mock32 #34 blocked,
          mock32 #63 kept)
  D51R-1  survivalChip: nothing renders while SURVIVAL_DISPLAY is off, and
          the app block's chip / 🚌 paths are gated by it

Exit 0 and `CARD: all N cases passed` only if every case holds.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DECK = os.path.join(ROOT, "docs", "draft-deck.html")
STATES = os.path.join(ROOT, "arena", "data", "states")
FAILS = []
CASES = 0


def case(name, ok, detail=""):
    global CASES
    CASES += 1
    print(("  ok    " if ok else "  FAIL  ") + name + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        FAILS.append((name, detail))


def extract(tag, html):
    m = re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S)
    if not m:
        sys.exit(f"CARD: FAILED — <script id=\"{tag}\"> not found")
    return m.group(1)


def main():
    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        sys.exit("CARD: SKIPPED — node is unavailable")
    html = open(DECK, encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="card-")
    mod = os.path.join(tmp, "deck.mjs")
    with open(mod, "w", encoding="utf-8") as f:
        f.write(extract("data", html) + "\n" + extract("engine", html) + """
export const api = { PLAYERS, decwScores, archetypeRead, categoryRanks, buildRosters,
  availablePool, marketRanks, myNextPick, familiesOf, teamOfPick,
  rankCard: typeof rankCard === "function" ? rankCard : null,
  pinDecision: typeof pinDecision === "function" ? pinDecision : null,
  survivalChip: typeof survivalChip === "function" ? survivalChip : null,
  SURVIVAL_DISPLAY: typeof SURVIVAL_DISPLAY === "undefined" ? null : SURVIVAL_DISPLAY,
  PIN_MAX_GAP: typeof PIN_MAX_GAP === "undefined" ? null : PIN_MAX_GAP };
""")
    probes = [("draft_state_51.json", 58), ("draft_state_mock32.json", 34), ("draft_state_mock32.json", 63)]
    states = {fn: json.load(open(os.path.join(STATES, fn), encoding="utf-8")) for fn, _ in probes}
    fixture = os.path.join(tmp, "in.json")
    json.dump({"states": states, "probes": probes}, open(fixture, "w"))
    driver = os.path.join(tmp, "run.mjs")
    with open(driver, "w", encoding="utf-8") as f:
        f.write(r"""
import { api } from "__MOD__";
import fs from "node:fs";
const inp = JSON.parse(fs.readFileSync("__FIXTURE__", "utf8"));
const out = { present: { rankCard: !!api.rankCard, pinDecision: !!api.pinDecision, survivalChip: !!api.survivalChip },
              SURVIVAL_DISPLAY: api.SURVIVAL_DISPLAY, PIN_MAX_GAP: api.PIN_MAX_GAP };
if (api.rankCard) {
  const rows = [{ p: { n: "Aaron" }, ds: 0.9, decw: 0.50 }, { p: { n: "Zed" }, ds: 0.9, decw: 0.30 },
                { p: { n: "Mid" }, ds: 0.95, decw: 0.10 }];
  out.tie = api.rankCard(rows).map(r => r.p.n);
  out.tieNull = api.rankCard([{ p: { n: "Aaron" }, ds: 0.9, decw: null }, { p: { n: "Zed" }, ds: 0.9, decw: null }]).map(r => r.p.n);
}
if (api.survivalChip) out.chips = [api.survivalChip(0.01, []), api.survivalChip(0.5, ["C"]), api.survivalChip(0.3, [])];
out.pins = [];
if (api.pinDecision && api.rankCard) {
  const { PLAYERS } = api;
  const MKT_RANK = api.marketRanks([...PLAYERS].filter(p => p.av > 0));
  for (const [fn, pickNo] of inp.probes) {
    const st0 = inp.states[fn]; const n = pickNo - 1;
    const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt: st0.punt || [], picks: st0.picks.slice(0, n) };  /* the read depends on the declared punt */
    const rosters = api.buildRosters(st, PLAYERS); const mine = rosters[st.slot] || [];
    const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
    const pool = api.availablePool(st, PLAYERS);
    const dsAll = api.rankCard(api.decwScores(pool, mine, opp)); const scored = dsAll.slice(0, 5);
    const ecw = new Map(dsAll.map(x => [x.p.n, x.decw]));
    const { ranks } = api.categoryRanks(st, PLAYERS);
    const r = api.archetypeRead(st, mine, pool, ranks, api.myNextPick(st) ?? 0, MKT_RANK);
    const pinRaw = r && r.fam && r.best && !scored.some(x => api.familiesOf(x.p).includes(r.fam)) ? PLAYERS.find(p => p.n === r.best) : null;
    const d = api.pinDecision(r, scored, pinRaw, nm => ecw.get(nm) ?? null);
    out.pins.push({ fn, pickNo, urgent: !!(r && r.urgent), pin: pinRaw ? pinRaw.n : null, av: pinRaw ? pinRaw.av : null,
                    tgOnPin: d.tgOnPin, withheld: d.withheld, top1: scored[0].p.n });
  }
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__FIXTURE__", fixture))
    r = subprocess.run(["node", driver], capture_output=True, text=True)
    if r.returncode != 0:
        print("CARD: FAILED — the deck's engine block did not execute")
        print(r.stderr.strip()[:1500])
        sys.exit(1)
    js = json.loads(r.stdout)
    pres = js["present"]

    # ---- D51R-2 tie-break
    case("D51R-2 rankCard exists in the engine block", pres["rankCard"], "rankCard absent")
    case("D51R-2 exact blend tie orders by ΔECW before name",
         js.get("tie") == ["Mid", "Aaron", "Zed"], f"got {js.get('tie')}")
    case("D51R-2 tie with no ΔECW (turn 1) still breaks by name DESC",
         js.get("tieNull") == ["Zed", "Aaron"], f"got {js.get('tieNull')}")

    # ---- D51R-4 pin gate
    case("D51R-4 pinDecision exists in the engine block", pres["pinDecision"], "pinDecision absent")
    case("D51R-4 PIN_MAX_GAP is 0.05 cats/wk", js.get("PIN_MAX_GAP") == 0.05, f"got {js.get('PIN_MAX_GAP')}")
    want = {("draft_state_51.json", 58): (False, "availability"),
            ("draft_state_mock32.json", 34): (False, "behind"),
            ("draft_state_mock32.json", 63): (True, "")}
    got = {(p["fn"], p["pickNo"]): p for p in js.get("pins", [])}
    for key, (tg, frag) in want.items():
        p = got.get(key)
        ok = p is not None and p["urgent"] and p["tgOnPin"] == tg and (frag in (p["withheld"] or ""))
        case(f"D51R-4 {key[0]} #{key[1]}: urgent pin {'kept' if tg else 'withheld'}"
             + (f" ({frag})" if frag else ""), ok, f"got {p}")

    # ---- D51R-1 survival display off
    case("D51R-1 SURVIVAL_DISPLAY is defined and false", js.get("SURVIVAL_DISPLAY") is False,
         f"got {js.get('SURVIVAL_DISPLAY')}")
    case("D51R-1 survivalChip renders nothing while the display is off",
         js.get("chips") == [None, None, None], f"got {js.get('chips')}")
    app = html[html.find('<script id="engine">') + 1:]
    case("D51R-1 the app's chip path consults survivalChip", "let chip = survivalChip(" in app,
         "chip block still hard-codes the thresholds")
    case("D51R-1 the 🚌 wait-chain is gated by SURVIVAL_DISPLAY",
         "if (SURVIVAL_DISPLAY && ladderFam" in app, "ladder block not gated")
    case("D51R-4 the app's sixth row styles LAST CALL off the gated decision, not readR.urgent",
         'li.style.borderColor = tgOnPin ?' in app and "(tgOnPin\n            ? `LAST CALL" in app,
         "sixth row still keys off readR.urgent")

    print()
    if FAILS:
        print(f"CARD: {len(FAILS)} of {CASES} cases FAILED")
        sys.exit(1)
    print(f"CARD: all {CASES} cases passed")


if __name__ == "__main__":
    main()
