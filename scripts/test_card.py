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
  D51R-1R survival refit (2026-09-22): SURVIVAL_DISPLAY is back on, survivalProb
          is the price-only model Phi((price - N) / max(8, 0.30 * price)) on the
          baked Yahoo price, chips BUY NOW <= 0.20 / TOSS-UP < 0.40; and
          the app block's chip / 🚌 paths are gated by it
  D51R-3  punt advisor, advice-only and room-relative: catWinProb /
          puntRead (hysteresis: PUNT_TURNS consecutive owner turns) /
          coherenceRead read the weekly model, not z-sum ranks; PUNT_BUTTONS
          is off and no app-block button assigns deck.state.punt (the one
          write path, adoptPunt, returns while the switch is off)

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
  survivalProb: typeof survivalProb === "function" ? survivalProb : null,
  clockRead: typeof clockRead === "function" ? clockRead : null,
  SURVIVAL_DISPLAY: typeof SURVIVAL_DISPLAY === "undefined" ? null : SURVIVAL_DISPLAY,
  PIN_MAX_GAP: typeof PIN_MAX_GAP === "undefined" ? null : PIN_MAX_GAP,
  catWinProb: typeof catWinProb === "function" ? catWinProb : null,
  puntRead: typeof puntRead === "function" ? puntRead : null,
  coherenceRead: typeof coherenceRead === "function" ? coherenceRead : null,
  PUNT_BUTTONS: typeof PUNT_BUTTONS === "undefined" ? null : PUNT_BUTTONS };
""")
    probes = [("draft_state_51.json", 58), ("draft_state_mock32.json", 34), ("draft_state_mock32.json", 63)]
    states = {fn: json.load(open(os.path.join(STATES, fn), encoding="utf-8")) for fn, _ in probes}
    states["draft_state_53.json"] = json.load(open(os.path.join(STATES, "draft_state_53.json"), encoding="utf-8"))
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
if (api.survivalChip) out.chips = [api.survivalChip(0.01, []), api.survivalChip(0.5, ["C"]), api.survivalChip(0.3, []), api.survivalChip(0.7, [])];
out.surv = api.survivalProb ? [api.survivalProb(60, 40), api.survivalProb(5, 150), api.survivalProb(null, 40), api.survivalProb(120, 100), api.survivalProb(200, 30)] : null;
out.pins = [];
if (api.pinDecision && api.rankCard) {
  const { PLAYERS } = api;
  /* F8 (2026-09-22): the build now bakes Yahoo prices into PLAYERS[].mkt and marketRanks
     orders priced rows by that price. These three probes were authored against the
     internal market model (the only ordering on 2026-09-21), and their urgency reads
     depend on it — so they run with the prices stripped, keeping the fixtures fixed
     across every future Yahoo paste. The priced ordering itself is F8's own test. */
  const MKT_RANK = api.marketRanks([...PLAYERS].filter(p => p.av > 0).map(p => ({ ...p, mkt: null, mktsrc: null })));
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
/* M53 (2026-09-22): the countdown under the feed title read "(you're on the clock)" for
   every pick after the owner's 13th — myNextPick() is null there and the app treated
   "no next pick" as "until = 0". clockRead is the engine's single read of the clock. */
out.clock = null;
if (api.clockRead) {
  const st0 = inp.states["draft_state_53.json"];
  const at = n => api.clockRead({ teams: st0.teams, slot: st0.slot, size: st0.size, punt: [], picks: st0.picks.slice(0, n) });
  out.clock = { p86: at(86), p87: at(87), p153: at(153), p154: at(154), p155: at(155), p156: at(156) };
}
out.advisor = { present: { catWinProb: !!api.catWinProb, puntRead: !!api.puntRead, coherenceRead: !!api.coherenceRead }, PUNT_BUTTONS: api.PUNT_BUTTONS };
if (api.puntRead && api.coherenceRead && api.catWinProb) {
  /* mock-51 #58 shape: AST dead, TO the roster's 2nd-best category in the room */
  const pw = { "FG%": 0.56, "FT%": 0.40, "3PTM": 0.31, "PTS": 0.29, "REB": 0.62, "AST": 0.06, "ST": 0.66, "BLK": 0.55, "TO": 0.76 };
  const kept = [...api.CATS ?? ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]];
  const r1 = api.puntRead(pw, kept, {});
  const r2 = api.puntRead(pw, kept, r1.seen);
  out.advisor.turn1 = { lean: r1.lean, advise: r1.advise, clear: r1.clear, seen: r1.seen };
  out.advisor.turn2 = { lean: r2.lean, advise: r2.advise, clear: r2.clear, winnable: r2.winnable, keptAfter: r2.keptAfter };
  const pwLate = { ...pw, "FG%": 0.43, "FT%": 0.68, "3PTM": 0.79, "PTS": 0.63, "REB": 0.44, "AST": 0.28, "ST": 0.78, "BLK": 0.57, "TO": 0.68 };
  out.advisor.late = api.puntRead(pwLate, kept, r2.seen);
  out.advisor.coh63 = api.coherenceRead(pw, ["FT%", "TO"]);
  out.advisor.cohNone = api.coherenceRead(pw, []);
  /* real roster at mock-51 #58: win probabilities from the engine's own weekly model */
  const st0 = inp.states["draft_state_51.json"]; const n = 57;
  const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt: [], picks: st0.picks.slice(0, n) };
  const rosters = api.buildRosters(st, api.PLAYERS); const mine = rosters[st.slot] || [];
  const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
  const real = api.catWinProb(mine, opp);
  out.advisor.real58 = real ? Object.fromEntries(Object.entries(real).map(([c, v]) => [c, +v.toFixed(2)])) : null;
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

    # ---- M53 clock read (2026-09-22): one engine read for "who is on the clock / your next"
    ck = js.get("clock")
    case("M53 clockRead exported from the engine", ck is not None, "clockRead absent")
    case("M53 clockRead #87 (86 logged): YOU on the clock, next #87, until 0",
         ck is not None and ck["p86"]["onClock"] and ck["p86"]["next"] == 87 and ck["p86"]["until"] == 0 and ck["p86"]["phase"] == "you", f"got {ck and ck['p86']}")
    case("M53 clockRead #88 (87 logged, after the Coby White insert): seat 9, 18 until #106",
         ck is not None and not ck["p87"]["onClock"] and ck["p87"]["seat"] == 9 and ck["p87"]["next"] == 106 and ck["p87"]["until"] == 18 and ck["p87"]["phase"] == "wait", f"got {ck and ck['p87']}")
    case("M53 clockRead #154 (153 logged): YOU on the clock for the last owner pick",
         ck is not None and ck["p153"]["onClock"] and ck["p153"]["phase"] == "you", f"got {ck and ck['p153']}")
    case("M53 clockRead #155 (154 logged): NOT on the clock — no owner pick left, phase none-left (the bug)",
         ck is not None and not ck["p154"]["onClock"] and ck["p154"]["next"] is None and ck["p154"]["phase"] == "none-left" and ck["p154"]["seat"] == 11, f"got {ck and ck['p154']}")
    case("M53 clockRead #156 (155 logged): still none-left, seat 12",
         ck is not None and not ck["p155"]["onClock"] and ck["p155"]["phase"] == "none-left" and ck["p155"]["seat"] == 12, f"got {ck and ck['p155']}")
    case("M53 clockRead after #156: phase done",
         ck is not None and ck["p156"]["phase"] == "done" and not ck["p156"]["onClock"], f"got {ck and ck['p156']}")
    app = html[html.find('<script id="engine">') + 1:]
    case("M53 the app's countdown renders from clockRead, not from until === 0",
         "clockRead(st)" in app and 'nxt === null ? 0' not in app, "renderStrip still derives the countdown from until === 0")

    # ---- D51R-1R survival refit (2026-09-22): display back on, price-only model
    case("D51R-1R SURVIVAL_DISPLAY is defined and true", js.get("SURVIVAL_DISPLAY") is True,
         f"got {js.get('SURVIVAL_DISPLAY')}")
    case("D51R-1R survivalChip: BUY NOW <= 0.20, dying shelf forces BUY NOW, TOSS-UP < 0.40, nothing above",
         js.get("chips") == ["BUY NOW", "BUY NOW", "TOSS-UP", None], f"got {js.get('chips')}")
    sv = js.get("surv")
    import math as _m
    def _phi(x): return 0.5 * (1 + _m.erf(x / _m.sqrt(2)))
    exp60 = _phi((60 - 40) / max(8, 0.30 * 60))
    case("D51R-1R survivalProb exported: Phi((price - N) / max(8, 0.30 * price)) at (60, 40)",
         sv is not None and abs(sv[0] - exp60) < 1e-6, f"got {sv} want {exp60:.6f}")
    case("D51R-1R survivalProb clamps to [0.01, 0.99] and is null without a price",
         sv is not None and sv[1] == 0.01 and sv[2] is None and sv[4] == 0.99 and abs(sv[3] - _phi(20 / 36)) < 1e-6,
         f"got {sv}")
    app = html[html.find('<script id="engine">') + 1:]
    case("D51R-1R the app's survivalP prices off the baked Yahoo price before the market-rank position",
         "p.mkt != null ? p.mkt : MKT_RANK.get(" in app, "survivalP does not read PLAYERS[].mkt first")
    case("D51R-1R the room-mix blend is gone from the app (no VAL_RANK survival path)",
         "SURV_W_VAL" not in app and "survPhi(" not in app, "old blend constants still present")
    case("D51R-1 the app's chip path consults survivalChip", "let chip = survivalChip(" in app,
         "chip block still hard-codes the thresholds")
    case("D51R-1 the 🚌 wait-chain is gated by SURVIVAL_DISPLAY",
         "if (SURVIVAL_DISPLAY && ladderFam" in app, "ladder block not gated")
    case("D51R-4 the app's sixth row styles LAST CALL off the gated decision, not readR.urgent",
         'li.style.borderColor = tgOnPin ?' in app and "(tgOnPin\n            ? `LAST CALL" in app,
         "sixth row still keys off readR.urgent")

    # ---- D51R-3 punt advisor: advice-only, room-relative, with hysteresis
    adv = js.get("advisor", {})
    pres = adv.get("present", {})
    case("D51R-3 catWinProb / puntRead / coherenceRead exist in the engine block",
         all(pres.get(k) for k in ("catWinProb", "puntRead", "coherenceRead")), f"present {pres}")
    case("D51R-3 PUNT_BUTTONS is defined and false (advice-only)", adv.get("PUNT_BUTTONS") is False,
         f"got {adv.get('PUNT_BUTTONS')}")
    t1, t2 = adv.get("turn1", {}), adv.get("turn2", {})
    case("D51R-3 a category losing most of the room leans punt; TO at 0.76 never does",
         t1.get("lean") == ["AST"], f"got {t1.get('lean')}")
    case("D51R-3 hysteresis: no advice on the first losing turn, advice on the second",
         t1.get("advise") is False and t2.get("advise") is True, f"turn1 {t1.get('advise')} turn2 {t2.get('advise')}")
    case("D51R-3 clear path is room-relative: 5/8 kept winnable at #58-shape is NOT clear, 6/8 late IS",
         t2.get("clear") is False and adv.get("late", {}).get("clear") is True,
         f"#58 clear {t2.get('clear')} ({t2.get('winnable')}) late clear {adv.get('late', {}).get('clear')}")
    coh = adv.get("coh63") or {}
    case("D51R-3 coherence on the mock-51 punt box (FT%+TO) reads WRONG TARGETS: keep TO, punt AST",
         coh.get("state") == "inverted" and (coh.get("best") or {}).get("out") == "TO" and (coh.get("best") or {}).get("inn") == "AST",
         f"got {coh}")
    case("D51R-3 coherence with no punt declared is null", adv.get("cohNone", "x") is None, f"got {adv.get('cohNone')}")
    real = adv.get("real58")
    case("D51R-3 the engine's own weekly model at mock-51 #58: AST <= 0.25, TO >= 0.55",
         bool(real) and real.get("AST", 1) <= 0.25 and real.get("TO", 0) >= 0.55, f"got {real}")
    app2 = html[html.find('<script id="engine">') + 1:]
    case("D51R-3 no advisor button writes the punt box (FULL TILT / Retarget / Adopt assignments gone)",
         "deck.state.punt = drift;" not in app2 and "deck.state.punt = best.alt;" not in app2
         and "deck.state.punt = [...new Set([...deck.state.punt, ...val])];" not in app2,
         "an advisor assignment to deck.state.punt remains")
    m = re.search(r"function adoptPunt\(list, why\) \{\s*if \(!PUNT_BUTTONS\) return;", app2)
    case("D51R-3 adoptPunt is the advisor's only write path and returns while PUNT_BUTTONS is off",
         bool(m) and app2.count("adoptPunt(") == 4 and 'el("button", "adopt fulltilt"' in app2 and "if (PUNT_BUTTONS && read.advise && read.clear)" in app2,
         f"guard {bool(m)}, adoptPunt call sites {app2.count('adoptPunt(')} (want 4 = definition + 3 buttons)")

    print()
    if FAILS:
        print(f"CARD: {len(FAILS)} of {CASES} cases FAILED")
        sys.exit(1)
    print(f"CARD: all {CASES} cases passed")


if __name__ == "__main__":
    main()
