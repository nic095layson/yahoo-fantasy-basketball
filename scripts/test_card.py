#!/usr/bin/env python3
"""Card-governance regression suite (mock 51 retro, 2026-09-21).

    python3 scripts/test_card.py

Runs the deck's OWN engine block under node (the check_parity extraction)
and pins three behaviours the retro found wrong or undefined:

  D51R-2  rankCard: exact blend ties order by ΔECW before name
  D51R-4  pinDecision: the urgent TARGET takes the 🎯 only at availability
          1.0 and within PIN_MAX_GAP cats/week of #1. Originally measured on
          the committed states (state_51 #58 blocked, mock32 #34 blocked,
          mock32 #63 kept). Re-pointed 2026-09-29: the D-M1 position sync
          (every Yahoo-matched row now carries Yahoo's official eligibility)
          filled the family shelves, so those three turns no longer produce
          an urgent read at all — a scan of all 13 committed states x owner
          turns finds 3 urgent reads, all withheld on availability (state_54
          #34 JJJ 0.78, mock41 #72 Zion 0.78, state_50 #68 no pin). The
          availability branch stays measured on state_54 #34; the behind /
          kept / non-urgent branches are pinned by calling the gate directly
          (it is a pure function of the read, the card and the pin).
          Re-pointed again 2026-10-01: D-WO1-1 (d) made thirteen wide lines
          one line on both planes (Poeltl 14.5 -> 11.5 points among them) and
          state_54 #34 stopped producing an urgent read. The same scan on the
          v39 page (16 committed states x 208 owner turns) finds 4 urgent
          reads: state_52 #63 (no pin), state_57 #39 and state_58 #63
          (Porzingis 0.78, withheld; vetoed on the owner's pool since 9/28),
          mock31 #64 (Zion 0.78, withheld). The availability branch now
          measures on mock31 #64, the un-vetoed example.
  D51R-1R survival refit (2026-09-22): SURVIVAL_DISPLAY is back on, survivalProb
          is the price-only model Phi((price - N) / max(8, 0.30 * price)) on the
          baked Yahoo price, chips BUY NOW <= 0.20 / TOSS-UP < 0.40; and
          the app block's chip / 🚌 paths are gated by it
  D54-2   UNKNOWN follow-up (2026-09-28): an unresolved name keeps its raw
          text; the next resolving name that matches that text fixes the
          UNKNOWN in place, a non-matching name logs as a new pick with a
          warning, a gap placeholder never auto-fixes; the strip names every
          open UNKNOWN
  D54-1   card-gap echo: a my: pick that is not the 🎯 states its card rank
          and gap (live hint under the feed + the log line)
  D54-3   dead-category trap line on the advisor read (reworded 2026-09-29 for
          the 60-second clock: one line — "Don't reach for a lost category:
          X (C, card #k) · … — none beats 🎯 T")
  VETO    owner veto list (executive decision 2026-09-28): JUDGMENT.doNotDraft
          names never enter YOUR candidate pool (card / 🎯 / LAST CALL) while
          the room, the resolver, rosters, matrix, category ranks and the mock
          AIs keep seeing them; hoops.py reads the same list from the deck
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
  processFeed: typeof processFeed === "function" ? processFeed : null,
  matchCandidates: typeof matchCandidates === "function" ? matchCandidates : null,
  rankCard: typeof rankCard === "function" ? rankCard : null,
  pinDecision: typeof pinDecision === "function" ? pinDecision : null,
  survivalChip: typeof survivalChip === "function" ? survivalChip : null,
  survivalProb: typeof survivalProb === "function" ? survivalProb : null,
  clockRead: typeof clockRead === "function" ? clockRead : null,
  adviceText: typeof adviceText === "function" ? adviceText : null,
  SURVIVAL_DISPLAY: typeof SURVIVAL_DISPLAY === "undefined" ? null : SURVIVAL_DISPLAY,
  PIN_MAX_GAP: typeof PIN_MAX_GAP === "undefined" ? null : PIN_MAX_GAP,
  catWinProb: typeof catWinProb === "function" ? catWinProb : null,
  puntRead: typeof puntRead === "function" ? puntRead : null,
  coherenceRead: typeof coherenceRead === "function" ? coherenceRead : null,
  PUNT_BUTTONS: typeof PUNT_BUTTONS === "undefined" ? null : PUNT_BUTTONS,
  pairDecision: typeof pairDecision === "function" ? pairDecision : null,
  relabelLog: typeof relabelLog === "function" ? relabelLog : null,
  insertPick: typeof insertPick === "function" ? insertPick : null,
  PAIR_MIN_GAIN: typeof PAIR_MIN_GAIN === "undefined" ? null : PAIR_MIN_GAIN,
  PAIR_WAIT_MIN: typeof PAIR_WAIT_MIN === "undefined" ? null : PAIR_WAIT_MIN,
  PAIR_MARKER: typeof PAIR_MARKER === "undefined" ? null : PAIR_MARKER,
  cardPool: typeof cardPool === "function" ? cardPool : null,
  CARD_PRICED_FROM: typeof CARD_PRICED_FROM === "undefined" ? null : CARD_PRICED_FROM };
""")
    probes = [("draft_state_mock31.json", 64)]
    states = {fn: json.load(open(os.path.join(STATES, fn), encoding="utf-8")) for fn, _ in probes}
    for fn in ("draft_state_51.json", "draft_state_53.json", "draft_state_63.json"):  # advisor / veto / clock / D-CAST-4 probes below
        states[fn] = json.load(open(os.path.join(STATES, fn), encoding="utf-8"))
    fixture = os.path.join(tmp, "in.json")
    jblock = extract("judgment", html)
    vm = re.search(r"doNotDraft:\s*\[(.*?)\]", jblock, re.S)
    veto = re.findall(r'"([^"]+)"', vm.group(1)) if vm else None
    # D59-2 (2026-10-01): two-pick 🎯 fixtures. "m59_82_v37" is the mock-59 #82 card the
    # owner saw (m59_deckcard_v37.json: ΔECW and survival-to-#87 of the Top-5); the deep
    # 🎯 Poeltl (Mkt 187, survival 0.829) must drop behind a scarcer near-equal row.
    PAIR_FIXTURES = [
        {"name": "m59_82_v37",
         "rows": [{"n": "Jakob Poeltl", "decw": 0.9397}, {"n": "Zach LaVine", "decw": 0.9341},
                  {"n": "Jalen Suggs", "decw": 0.9281}, {"n": "Miles Bridges", "decw": 0.9565},
                  {"n": "Josh Hart", "decw": 0.9129}],
         "surv": [0.829, 0.729, 0.765, 0.645, 0.623]},
        # a deep 🎯 (survival 0.85) over a near-equal scarce row (0.35): the marker must move
        {"name": "deep_vs_scarce",
         "rows": [{"n": "Deep", "decw": 0.94}, {"n": "Scarce", "decw": 0.93}, {"n": "C", "decw": 0.90},
                  {"n": "D", "decw": 0.88}, {"n": "E", "decw": 0.85}],
         "surv": [0.85, 0.35, 0.30, 0.30, 0.30]},
        # the pair prefers the BUY NOW row, but #1 is itself a coin flip (0.40): the guard holds
        {"name": "near_guard",
         "rows": [{"n": "A", "decw": 0.94}, {"n": "B", "decw": 0.935}, {"n": "C", "decw": 0.90},
                  {"n": "D", "decw": 0.88}, {"n": "E", "decw": 0.85}],
         "surv": [0.40, 0.05, 0.30, 0.30, 0.30]},
        # mock-59 #39 shape: the 🎯 (Derrick White) is a near-price row at 0.213 — never demoted
        {"name": "m59_39_near",
         "rows": [{"n": "Derrick White", "decw": 1.4764}, {"n": "Desmond Bane", "decw": 1.40},
                  {"n": "Kyrie Irving", "decw": 1.38}, {"n": "OG Anunoby", "decw": 1.30},
                  {"n": "Franz Wagner", "decw": 1.28}],
         "surv": [0.213, 0.35, 0.30, 0.56, 0.40]},
        # near-identical survivals: whatever the pair arithmetic prefers, the gain is under PAIR_MIN_GAIN
        {"name": "small_gain",
         "rows": [{"n": "A", "decw": 0.940}, {"n": "B", "decw": 0.935}, {"n": "C", "decw": 0.90},
                  {"n": "D", "decw": 0.88}, {"n": "E", "decw": 0.85}],
         "surv": [0.70, 0.68, 0.66, 0.60, 0.60]},
        # turn 1: no opponent roster, ΔECW null everywhere
        {"name": "turn1",
         "rows": [{"n": "A", "decw": None}, {"n": "B", "decw": None}], "surv": [0.5, 0.5]},
        # the 🎯 has no survival read (no price, no market rank): never moved
        {"name": "surv_null0",
         "rows": [{"n": "A", "decw": 0.9}, {"n": "B", "decw": 0.89}], "surv": [None, 0.3]},
    ]
    # D59-1 (2026-10-01): history re-numbering after Insert-at-#. A 12-team room, owner
    # seat 3 (so the shifted #3 lands on the owner): picks Jokic #1, Wemby #2, an UNKNOWN
    # #3, then Luka inserted at #2 — the log must re-number, re-seat, mark (YOU), rename.
    RELABEL_FIXTURE = {
        "state": {"teams": 12, "slot": 3, "size": 13, "punt": [],
                  "picks": [{"player": "Nikola Jokic", "slot": 1}, {"player": "Victor Wembanyama", "slot": 2},
                            {"player": "UNKNOWN #3", "slot": 3, "raw": "zzz"}]},
        "log": [{"t": "  ✓ (R1) #1: Nikola Jokic → Seat 1", "cls": "", "pick": 0, "kind": "pick", "note": ""},
                {"t": "  ✓ (R1) #2: Victor Wembanyama → Seat 2", "cls": "", "pick": 1, "kind": "pick", "note": "  (assumed over X)"},
                {"t": "⚠ (R1) #3: UNKNOWN (\"zzz\": no match) — fix with: 3- Name", "cls": "warn", "pick": 2, "kind": "unk", "raw": "zzz"},
                {"t": "— your pick, #4 —", "cls": ""}],
        "insertAt": 2, "insertName": "Luka Doncic"}
    json.dump({"states": states, "probes": probes, "veto": veto or [],
               "pairFixtures": PAIR_FIXTURES, "relabel": RELABEL_FIXTURE}, open(fixture, "w"))
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
out.advice = api.adviceText ? [
  api.adviceText("Chet Holmgren", "Jalen Williams", -0.017, 0.017, 25, false),
  api.adviceText("Derrick White", "OG Anunoby", 0.070, 0.020, 45, false),
  api.adviceText("OG Anunoby", "Payton Pritchard", -0.012, 0.012, null, false),
  api.adviceText("Nikola Jokic", null, null, null, 1, true),
  api.adviceText("Aaron", "Zed", 0.0, 0.0, 30, false)] : null;
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
  /* 2026-09-29: the behind / kept / non-urgent branches have no committed example
     under the Yahoo-synced pool (see the docstring), so the gate is called directly:
     #1 at ΔECW 0.60; the pin at 0.50 (0.100 behind), 0.56 (0.040 behind), or av 0.78. */
  const readU = { urgent: true, fam: "C", best: "Pin" }, readQ = { urgent: false, fam: "C", best: "Pin" };
  const top = [{ p: { n: "Top" }, ds: 0.9, decw: 0.60 }];
  const at = v => nm => (nm === "Pin" ? v : null);
  out.pinUnit = { avail: api.pinDecision(readU, top, { n: "Pin", av: 0.78 }, at(0.56)),
                  behind: api.pinDecision(readU, top, { n: "Pin", av: 1 }, at(0.50)),
                  kept: api.pinDecision(readU, top, { n: "Pin", av: 1 }, at(0.56)),
                  quiet: api.pinDecision(readQ, top, { n: "Pin", av: 1 }, at(0.56)) };
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
/* VETO (owner decision 2026-09-28): the owner's card is rankCard over availablePool minus
   JUDGMENT.doNotDraft; opponents' rosters and category ranks are untouched. */
out.veto = null;
if (inp.veto && inp.veto.length) {
  const V = new Set(inp.veto);
  const st0 = inp.states["draft_state_51.json"]; const n = 62;
  const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt: [], picks: st0.picks.slice(0, n) };
  const rosters = api.buildRosters(st, api.PLAYERS); const mine = rosters[st.slot] || [];
  const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
  const pool = api.availablePool(st, api.PLAYERS);
  const raw = api.rankCard(api.decwScores(pool, mine, opp)).map(x => x.p.n);
  const own = api.rankCard(api.decwScores(pool.filter(p => !V.has(p.n)), mine, opp)).map(x => x.p.n);
  /* mock 53: seat 3 took Porzingis at #99 (in mock 51 the OWNER took him at #87 — the veto's origin story) */
  const s53 = inp.states["draft_state_53.json"];
  const st99 = { teams: s53.teams, slot: s53.slot, size: s53.size, punt: [], picks: s53.picks.slice(0, 99) };
  const ros99 = api.buildRosters(st99, api.PLAYERS);
  const holder = Object.entries(ros99).find(([s, r]) => (r || []).some(p => V.has(p.n)));
  const ranks87 = api.categoryRanks(st99, api.PLAYERS).ranks;
  const ownerSlot53 = s53.slot;
  out.veto = { raw5: raw.slice(0, 5), own5: own.slice(0, 5), rawMinusVeto5: raw.filter(nm => !V.has(nm)).slice(0, 5),
               poolN: pool.length, ownN: pool.filter(p => !V.has(p.n)).length, vetoAvail: pool.filter(p => V.has(p.n)).length,
               holder: holder ? +holder[0] : null, ownerSlot53, ranksCats: Object.keys(ranks87 || {}).length };
}
/* D54-2 (2026-09-28): UNKNOWN follow-up in the engine's feed parser. */
out.unk = null;
if (api.processFeed) {
  const fresh = () => ({ teams: 12, slot: 10, size: 13, punt: [], picks: [] });
  const snap = st => st.picks.map(pk => [pk.player, pk.slot, pk.raw ?? null]);
  const s1 = fresh(); const r1 = api.processFeed(s1, api.PLAYERS, "Nikola Jokic; mamy"); const afterUnk = snap(s1);
  const r2 = api.processFeed(s1, api.PLAYERS, "Sandro Mamukelashvili"); const afterFix = snap(s1);
  const s2 = fresh(); const r3 = api.processFeed(s2, api.PLAYERS, "Nikola Jokic; LavineWiggins; Jabari Smith Jr.");
  const s3 = fresh(); api.processFeed(s3, api.PLAYERS, "3- Luka Doncic"); const r4 = api.processFeed(s3, api.PLAYERS, "Nikola Jokic");
  out.unk = { afterUnk, afterFix, fixLines: r2.lines.map(l => l.t), s2: snap(s2), s2Lines: r3.lines.map(l => [l.t, l.cls]), s3: snap(s3) };
}
/* D53-4 (mock 53, executed 2026-09-29): Yahoo's dotted spellings resolve in the feed. */
out.dots = null;
if (api.matchCandidates) {
  const names = q => api.matchCandidates(api.PLAYERS, q).map(p => p.n);
  out.dots = { pj: names("P.J. Washington"), tj: names("TJ McConnell"),
               pjPlain: names("PJ Washington"), tjDot: names("T.J. McConnell"), lone: names(".") };
}
/* D59-2 (2026-10-01): two-pick 🎯 — pairDecision(rows, surv, decwGiven) with independence
   (decwGiven(i, j) = rows[j].decw) so the Python twin reproduces the arithmetic exactly. */
out.pair = null; out.PAIR_MIN_GAIN = api.PAIR_MIN_GAIN; out.PAIR_WAIT_MIN = api.PAIR_WAIT_MIN; out.PAIR_MARKER = api.PAIR_MARKER;
if (api.pairDecision) {
  out.pair = {};
  for (const f of inp.pairFixtures) out.pair[f.name] = api.pairDecision(f.rows, f.surv, (i, j) => f.rows[j].decw);
}
/* D59-1 (2026-10-01): insertPick renames the shifted UNKNOWN; relabelLog re-numbers,
   re-seats and (YOU)-marks the earlier history lines from the state. */
out.relabel = null;
if (api.relabelLog && api.insertPick) {
  const F = inp.relabel; const st = JSON.parse(JSON.stringify(F.state));
  const log = JSON.parse(JSON.stringify(F.log));
  const r = api.insertPick(st, api.PLAYERS, F.insertAt, F.insertName);
  const rl = api.relabelLog(log, st, F.insertAt - 1);
  out.relabel = { ok: r.ok, echo: r.lines.map(l => l.t), picks: st.picks.map(pk => [pk.player, pk.slot, pk.raw ?? null]),
                  lines: rl.log.map(e => [e.t, e.cls, e.pick ?? null]), movedOn: rl.movedOn, movedOff: rl.movedOff };
}
/* D-CAST-4 (owner 2026-10-07): from round CARD_PRICED_FROM the card's candidates are the priced rows (Yahoo ADP,
   else XRank, baked by the build); fewer than five priced rows left -> the whole pool. Probed on mock 63 at the
   owner's #154 (round 13) and #87 (round 8). */
out.cast4 = { present: !!api.cardPool, from: api.CARD_PRICED_FROM };
if (api.cardPool) {
  const st = inp.states["draft_state_63.json"];
  const by = new Map(api.PLAYERS.map(p => [p.n, p]));
  const veto = new Set(["Kristaps Porzingis"]);
  const probe = (upto) => {
    const taken = new Set(st.picks.slice(0, upto).map(pk => pk.player)); const ros = new Map();
    for (const pk of st.picks.slice(0, upto)) { const p = by.get(pk.player); if (p) { if (!ros.has(pk.slot)) ros.set(pk.slot, []); ros.get(pk.slot).push(p); } }
    const mine = ros.get(st.slot) || []; const opp = [...ros.entries()].filter(([s]) => s !== st.slot).map(([, r]) => r);
    const pool = api.PLAYERS.filter(p => !taken.has(p.n) && p.av > 0 && !veto.has(p.n));
    const rnd = Math.floor(upto / st.teams) + 1; const cp = api.cardPool(pool, rnd);
    const top = api.rankCard(api.decwScores(cp, mine, opp)).slice(0, 5).map(x => x.p.n);
    const topAll = api.rankCard(api.decwScores(pool, mine, opp)).slice(0, 5).map(x => x.p.n);
    return { rnd, poolN: pool.length, cpN: cp.length, unpricedInCp: cp.filter(p => p.mkt == null).length, top, topAll,
             unpricedInTopAll: topAll.filter(n => by.get(n).mkt == null).length };
  };
  out.cast4.r13 = probe(153); out.cast4.r8 = probe(86);
  const four = api.PLAYERS.filter(p => p.av > 0 && p.mkt != null).slice(0, 4).concat(api.PLAYERS.filter(p => p.av > 0 && p.mkt == null).slice(0, 6));
  out.cast4.fallback = { n: four.length, kept: api.cardPool(four, 13).length };
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

    # ---- D-CAST-4 (owner 2026-10-07): priced-only card candidates from round 11
    c4 = js.get("cast4") or {}
    case("D-CAST-4 cardPool exists in the engine block", c4.get("present"), "cardPool absent")
    case("D-CAST-4 CARD_PRICED_FROM is 11", c4.get("from") == 11, f"got {c4.get('from')}")
    r13, r8, fb = c4.get("r13") or {}, c4.get("r8") or {}, c4.get("fallback") or {}
    case("D-CAST-4 mock 63 #154 (round 13): the unfiltered Top-5 carried an unpriced row (the case this rule exists for)",
         r13.get("unpricedInTopAll", 0) >= 1, f"got {r13}")
    case("D-CAST-4 mock 63 #154: the card pool keeps no unpriced row and the Top-5 changes",
         r13.get("unpricedInCp") == 0 and r13.get("cpN", 0) < r13.get("poolN", 0) and r13.get("top") != r13.get("topAll"), f"got {r13}")
    case("D-CAST-4 mock 63 #87 (round 8): the card pool is the whole pool",
         r8.get("cpN") == r8.get("poolN") and r8.get("top") == r8.get("topAll"), f"got {r8}")
    case("D-CAST-4 fewer than five priced rows left: the whole pool stays",
         fb.get("n") == 10 and fb.get("kept") == 10, f"got {fb}")

    # ---- D51R-2 tie-break
    case("D51R-2 rankCard exists in the engine block", pres["rankCard"], "rankCard absent")
    case("D51R-2 exact blend tie orders by ΔECW before name",
         js.get("tie") == ["Mid", "Aaron", "Zed"], f"got {js.get('tie')}")
    case("D51R-2 tie with no ΔECW (turn 1) still breaks by name DESC",
         js.get("tieNull") == ["Zed", "Aaron"], f"got {js.get('tieNull')}")

    # ---- D51R-4 pin gate
    case("D51R-4 pinDecision exists in the engine block", pres["pinDecision"], "pinDecision absent")
    case("D51R-4 PIN_MAX_GAP is 0.05 cats/wk", js.get("PIN_MAX_GAP") == 0.05, f"got {js.get('PIN_MAX_GAP')}")
    want = {("draft_state_mock31.json", 64): (False, "availability")}
    got = {(p["fn"], p["pickNo"]): p for p in js.get("pins", [])}
    for key, (tg, frag) in want.items():
        p = got.get(key)
        ok = p is not None and p["urgent"] and p["tgOnPin"] == tg and (frag in (p["withheld"] or ""))
        case(f"D51R-4 {key[0]} #{key[1]}: urgent pin {'kept' if tg else 'withheld'}"
             + (f" ({frag})" if frag else ""), ok, f"got {p}")
    pu = js.get("pinUnit") or {}
    case("D51R-4 gate: urgent pin at availability 0.78 is withheld (availability)",
         pu.get("avail", {}).get("tgOnPin") is False and "availability 0.78" in (pu.get("avail", {}).get("withheld") or ""),
         f"got {pu.get('avail')}")
    case("D51R-4 gate: urgent pin 0.100 cats/wk behind #1 is withheld (behind, limit 0.05)",
         pu.get("behind", {}).get("tgOnPin") is False and "0.100 cats/wk behind #1" in (pu.get("behind", {}).get("withheld") or ""),
         f"got {pu.get('behind')}")
    case("D51R-4 gate: urgent pin at availability 1.0 and 0.040 behind is kept (🎯 on the pin)",
         pu.get("kept", {}).get("tgOnPin") is True and (pu.get("kept", {}).get("withheld") or "") == "",
         f"got {pu.get('kept')}")
    case("D51R-4 gate: a non-urgent read never takes the 🎯 and names no reason",
         pu.get("quiet", {}).get("tgOnPin") is False and (pu.get("quiet", {}).get("withheld") or "") == "",
         f"got {pu.get('quiet')}")

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
    # ---- D-LS-2 (2026-10-02): the chip tooltip states the owner's league's realized bands from
    # arena/results/league_survival_2025-26.json (BUY NOW rows survived 21 of 53, TOSS-UP 36 of 69,
    # quiet 447 of 481 at the owner's seat last season) so the words match the room he drafts in.
    case("D-LS-2 the chip tooltip carries the owner's league's realized survival bands (21 of 53 · 36 of 69 · 447 of 481)",
         "In your league last season" in app and "21 of 53" in app and "36 of 69" in app and "447 of 481" in app,
         "league bands absent from the chip tooltip")
    case("D51R-1 the app's chip path consults survivalChip", "let chip = survivalChip(" in app,
         "chip block still hard-codes the thresholds")
    case("D51R-1 the 🚌 wait-chain is gated by SURVIVAL_DISPLAY",
         "if (SURVIVAL_DISPLAY && ladderFam" in app, "ladder block not gated")
    case("D51R-4 the app's sixth row styles LAST CALL off the gated decision, not readR.urgent",
         'li.style.borderColor = tgOnPin ?' in app and "(tgOnPin\n            ? `LAST CALL" in app,
         "sixth row still keys off readR.urgent")

    # ---- D-R5 (owner-reported 2026-09-30): the advice sentence names the real reason
    # when the 🎯 wins the blend on value while trailing the #2 on ΔECW
    adv5 = js.get("advice")
    case("D-R5 adviceText exists in the engine block", adv5 is not None, "adviceText absent")
    a0 = (adv5 or [""])[0]
    case("D-R5 negative gap: names value and the #2's better fit, never a minus-signed 'over'",
         "the best value left (Mkt 25)" in a0 and "Jalen Williams fits this week's roster slightly better (+0.034 cats/wk) but ranks lower on value" in a0
         and "expected categories per week over" not in a0 and "\u2212" not in a0 and "−" not in a0, f"got {a0!r}")
    a1 = (adv5 or ["", ""])[1] if adv5 and len(adv5) > 1 else ""
    case("D-R5 positive gap keeps the measured-margin sentence",
         a1 == "Take Derrick White \u2014 +0.050 expected categories per week over OG Anunoby", f"got {a1!r}")
    a2 = adv5[2] if adv5 and len(adv5) > 2 else ""
    case("D-R5 negative gap without a price falls back to 'on the board'",
         "the best value left on the board; Payton Pritchard fits" in a2 and "(Mkt" not in a2, f"got {a2!r}")
    a3 = adv5[3] if adv5 and len(adv5) > 3 else ""
    case("D-R5 no opponent roster yet keeps the value-board sentence",
         a3 == "Take Nikola Jokic \u2014 top of the 9-cat value board; no opponent roster to measure a marginal category against yet", f"got {a3!r}")
    a4 = adv5[4] if adv5 and len(adv5) > 4 else ""
    case("D-R5 an exact ΔECW tie reads +0.000 over the #2 (unchanged)",
         a4 == "Take Aaron \u2014 +0.000 expected categories per week over Zed", f"got {a4!r}")
    app5 = html[html.find('<script id="engine">') + 1:]
    case("D-R5 the app composes the sentence through adviceText",
         "adviceText(top0.n" in app5 and "expected categories per week over ${scored[1].p.n}" not in app5,
         "app block still composes the sentence inline")

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

    # ---- VETO (owner decision 2026-09-28): DO NOT DRAFT list, owner-pool only
    case("VETO JUDGMENT.doNotDraft lists Kristaps Porzingis",
         bool(veto) and "Kristaps Porzingis" in veto, f"got {veto}")
    case("VETO doNotDraft precedes the players block (gate 5 reads players: as the last key)",
         bool(vm) and jblock.find("doNotDraft") < jblock.find("players: {"), "doNotDraft missing or after players:")
    vt = js.get("veto")
    case("VETO mock 51 #63: the owner card is the unfiltered card minus the veto list, and never names a vetoed player",
         bool(vt) and vt["own5"] == vt["rawMinusVeto5"] and not any(nm in (veto or []) for nm in vt["own5"]),
         f"got {vt}")
    case("VETO the owner pool is exactly the available pool minus the available vetoed names",
         bool(vt) and vt["ownN"] == vt["poolN"] - vt["vetoAvail"] and vt["vetoAvail"] >= 1, f"got {vt}")
    case("VETO mock 53 #99: an opponent's roster (seat 3) still holds the vetoed player and category ranks still compute",
         bool(vt) and vt["holder"] == 3 and vt["holder"] != vt["ownerSlot53"] and vt["ranksCats"] == 9,
         f"got {vt}")
    app3 = html[html.find('<script id="app">') + 1:]
    case("VETO the app builds YOUR candidates from ownerPool (availablePool minus JUDGMENT.doNotDraft)",
         "function ownerPool(st)" in app3 and "JUDGMENT.doNotDraft" in app3
         and "const pool = ownerPool(st);" in app3 and app3.count("ownerPool(st)") >= 3,
         f"ownerPool defined {'function ownerPool(st)' in app3}, call sites {app3.count('ownerPool(st)')}")
    case("VETO the Best-available table keeps the vetoed row and marks it DO NOT DRAFT",
         "DO NOT DRAFT" in app3 and "VETO.has(p.n)" in app3, "marker absent")
    case("VETO a my: pick of a vetoed name logs a warning, not a refusal",
         "on your DO NOT DRAFT list" in app3, "warn absent")
    sys.path.insert(0, HERE)
    import hoops  # noqa: E402
    case("VETO hoops.py reads the same list from the deck (do_not_draft twin)",
         hasattr(hoops, "do_not_draft") and hoops.do_not_draft() == set(veto or []),
         f"got {getattr(hoops, 'do_not_draft', lambda: None)()}")

    # ---- D54-2 UNKNOWN follow-up (2026-09-28)
    u = js.get("unk")
    case("D54-2 processFeed exported from the engine", u is not None, "processFeed absent")
    case("D54-2 an unresolved name logs UNKNOWN with its raw text kept",
         bool(u) and len(u["afterUnk"]) == 2 and u["afterUnk"][1][0] == "UNKNOWN #2" and u["afterUnk"][1][2] == "mamy",
         f"got {u and u['afterUnk']}")
    case("D54-2 the next resolving name that matches the unknown text fixes it in place (same seat, no new pick)",
         bool(u) and len(u["afterFix"]) == 2 and u["afterFix"][1][0] == "Sandro Mamukelashvili" and u["afterFix"][1][1] == 2
         and any("fixed: UNKNOWN" in t for t in u["fixLines"]),
         f"got {u and (u['afterFix'], u['fixLines'])}")
    case("D54-2 a non-matching name after an UNKNOWN logs as a new pick and warns that the UNKNOWN is still open",
         bool(u) and len(u["s2"]) == 3 and u["s2"][1][0] == "UNKNOWN #2" and u["s2"][2][0] == "Jabari Smith Jr."
         and any("still UNKNOWN" in t and cls == "warn" for t, cls in u["s2Lines"]),
         f"got {u and (u['s2'], u['s2Lines'])}")
    case("D54-2 a gap placeholder never auto-fixes",
         bool(u) and len(u["s3"]) == 4 and u["s3"][0][0] == "UNKNOWN #1" and u["s3"][1][0] == "UNKNOWN #2" and u["s3"][3][0] == "Nikola Jokic",
         f"got {u and u['s3']}")
    app4 = html[html.find('<script id="app">') + 1:]
    case("D54-2 the strip names every open UNKNOWN with the fix syntax", "UNKNOWN open" in app4, "strip badge absent")
    has_hint, has_gap, has_line = 'id="feedHint"' in html, "function cardGapText" in app4, "off the card:" in app4
    case("D54-1 a my: pick off the card gets its rank and gap under the feed and in the log line",
         has_hint and has_gap and has_line, f"feedHint {has_hint}, cardGapText {has_gap}, log line {has_line}")
    case("D54-3 the advisor read names the dead-category trap against the 🎯 (one plain line since v34)",
         "Don't reach for a lost category" in app4 and "none beats 🎯" in app4, "trap sentence absent")
    # V-D1/V-D2 (system validation 2026-09-29, owner: "Fix 1 and 2"): the two
    # empty-input guards must render AND save the warning they log (the
    # 127-assertion Chromium drive found both paths silent until the next
    # action), and the sweep panel must count the pool, not a July literal.
    import re as _re
    ins_ok = _re.search(r'log\("Insert needs a pick # and a player name\.", "warn"\);\s*save\(\);\s*renderMirror\(\);\s*(/\*.*?\*/\s*)?return;', app4, _re.S) is not None
    case("V-D1 empty Insert-at-# saves and renders its warning before returning", ins_ok, "guard lacks save(); renderMirror(); before return")
    rs_ok = _re.search(r'log\("RESYNC refused: paste is empty[^"]*", "warn"\);\s*save\(\);\s*renderMirror\(\);\s*(/\*.*?\*/\s*)?return;', app4, _re.S) is not None
    case("V-D1 empty Resync paste saves and renders its refusal before returning", rs_ok, "guard lacks save(); renderMirror(); before return")
    case("V-D2 the Daily-sweep panel counts the pool (PLAYERS.length), not a literal 246",
         "re-verifies all 246 placements" not in app4 and "re-verifies all ${PLAYERS.length} placements" in app4, "literal still present or PLAYERS.length missing")
    sys.path.insert(0, HERE)
    import hoops as _h  # noqa: E402
    case("D54-2 hoops.py carries the unknown_matches twin (mamy → Mamukelashvili yes; LavineWiggins → Jabari Smith Jr. no)",
         hasattr(_h, "unknown_matches") and _h.unknown_matches("mamy", "Sandro Mamukelashvili") and not _h.unknown_matches("LavineWiggins", "Jabari Smith Jr."),
         "unknown_matches missing or wrong")

    # ---- D53-4 dot-folding in the feed resolver (mock 53 ask, executed 2026-09-29):
    # the pool spells "PJ Washington" and "T.J. McConnell"; Yahoo pastes "P.J."
    # and rooms type "TJ". fold() kept dots, so both crossings failed every stage.
    dots = js.get("dots")
    case("D53-4 JS resolver folds dots: 'P.J. Washington' → PJ Washington, 'TJ McConnell' → T.J. McConnell",
         bool(dots) and dots["pj"] == ["PJ Washington"] and dots["tj"] == ["T.J. McConnell"], f"got {dots}")
    case("D53-4 JS resolver: the pool's own spellings still resolve and a lone '.' still matches nothing",
         bool(dots) and dots["pjPlain"] == ["PJ Washington"] and dots["tjDot"] == ["T.J. McConnell"] and dots["lone"] == [],
         f"got {dots}")
    _pl = _h.load_players()
    _mc = lambda q: [p["player"] for p in _h.match_candidates(_pl, q)]
    case("D53-4 hoops.match_candidates twin folds dots the same way",
         _mc("P.J. Washington") == ["PJ Washington"] and _mc("TJ McConnell") == ["T.J. McConnell"]
         and _mc("PJ Washington") == ["PJ Washington"] and _mc(".") == [],
         f"got {_mc('P.J. Washington')}, {_mc('TJ McConnell')}, {_mc('PJ Washington')}, {_mc('.')}")

    # ---- D59-2 (2026-10-01): the two-pick 🎯. The card's #1 is price-blind by design; when
    # the room prices him far below his value he waits (target_wait: deep 🎯s still there at
    # the next owner turn 4 of 5) while a near-equal scarce row is lost. pairDecision scores
    # the next TWO owner turns: value now + the survival-weighted value of the best row left
    # at the next turn, and moves the 🎯 marker (never the blend50 order) when the pair gain
    # is at least PAIR_MIN_GAIN and the #1's own survival is at least PAIR_WAIT_MIN.
    pr = js.get("pair")
    case("D59-2 pairDecision exists in the engine block", pr is not None, "pairDecision absent")
    case("D59-2 PAIR_MIN_GAIN 0.01 cats/wk and PAIR_WAIT_MIN 0.60 exported",
         js.get("PAIR_MIN_GAIN") == 0.01 and js.get("PAIR_WAIT_MIN") == 0.60,
         f"got {js.get('PAIR_MIN_GAIN')}, {js.get('PAIR_WAIT_MIN')}")
    dv = (pr or {}).get("deep_vs_scarce") or {}
    case("D59-2 a deep 🎯 (0.85) over a near-equal scarce row (0.35): the marker moves to the scarce row, the deep one is named next turn",
         dv.get("moved") is True and dv.get("idx") == 1 and (dv.get("next") or {}).get("n") == "Deep" and (dv.get("gain") or 0) >= 0.01,
         f"got {dv}")
    m82 = (pr or {}).get("m59_82_v37") or {}
    # The real #82 numbers: all five rows were deep (survival 0.62–0.83), so the pair arithmetic
    # prefers Bridges-now by only 0.007 cats/wk — under PAIR_MIN_GAIN, no move. That is the
    # §9b finding restated: at that turn nothing on the card was lost by waiting; the cost
    # was taking none of the five. The fixture pins the arithmetic, not a wished-for move.
    m82p = m82.get("pair") or []
    case("D59-2 mock-59 #82 (v37 card): the pair arithmetic prefers Bridges-now by under 0.01 — the 🎯 stays on Poeltl, the reason names the gain",
         m82.get("moved") is False and m82.get("idx") == 0 and len(m82p) == 5 and m82p.index(max(m82p)) == 3
         and 0.005 < (m82.get("gain") or 0) < 0.01 and "pair gain" in str(m82.get("why")), f"got {m82}")
    ng = (pr or {}).get("near_guard") or {}
    case("D59-2 the pair prefers the BUY NOW row but #1 is a coin flip (0.40 < 0.60): never demoted, the reason names the guard",
         ng.get("moved") is False and ng.get("idx") == 0 and (ng.get("gain") or 0) >= 0.01 and "0.60" in str(ng.get("why")), f"got {ng}")
    near = (pr or {}).get("m59_39_near") or {}
    case("D59-2 mock-59 #39 (Derrick White, survival 0.213): the 🎯 stays on #1",
         near.get("moved") is False and near.get("idx") == 0, f"got {near}")
    sg = (pr or {}).get("small_gain") or {}
    case("D59-2 a pair gain under 0.01 cats/wk leaves the 🎯 on the #1", sg.get("moved") is False and sg.get("idx") == 0, f"got {sg}")
    t1 = (pr or {}).get("turn1") or {}
    case("D59-2 turn 1 (no ΔECW) never moves the 🎯", t1.get("moved") is False and t1.get("idx") == 0, f"got {t1}")
    s0 = (pr or {}).get("surv_null0") or {}
    case("D59-2 a 🎯 with no survival read is never demoted", s0.get("moved") is False and s0.get("idx") == 0, f"got {s0}")
    twin_ok, twin_detail = False, "hoops.pair_decision missing"
    if hasattr(_h, "pair_decision") and pr:
        twin_ok, bad = True, []
        for f in PAIR_FIXTURES:
            py = _h.pair_decision(f["rows"], f["surv"], lambda i, j, rows=f["rows"]: rows[j]["decw"])
            jsr = pr.get(f["name"]) or {}
            pp, jp = py["pair"], jsr.get("pair")
            same = (py["idx"] == jsr.get("idx") and py["moved"] == jsr.get("moved")
                    and abs((py["gain"] or 0) - (jsr.get("gain") or 0)) < 1e-9
                    and ((pp is None and jp is None) or (pp is not None and jp is not None and len(pp) == len(jp)
                                                         and all(abs(a - b) < 1e-9 for a, b in zip(pp, jp)))))
            if not same:
                twin_ok = False; bad.append((f["name"], py, jsr))
        twin_detail = f"differs on {bad[:1]}" if bad else ""
    case("D59-2 hoops.pair_decision is the exact twin on every fixture (idx, moved, gain, pair values)", twin_ok, twin_detail)
    case("D59-2 PAIR_MARKER is a boolean switch set by the pre-registered experiment, and the app honours it on the marker",
         isinstance(js.get("PAIR_MARKER"), bool) and "(PAIR_MARKER ? pairRead.idx : 0)" in app4, f"got {js.get('PAIR_MARKER')}")
    case("D59-2 the app composes the 🎯 and the advice sentence through pairDecision",
         "pairDecision(" in app4 and "likely waits" in app4, "pairDecision not consumed by the app / no two-pick sentence")
    # ---- D59-1 (2026-10-01): history box after Insert-at-#. Earlier lines are re-rendered
    # from the state (number, seat, (YOU)), a shifted UNKNOWN is renamed to its new number in
    # the state and the log, and a pick the shift moves onto the owner's seat is reported.
    rl = js.get("relabel")
    case("D59-1 relabelLog and insertPick exported from the engine", rl is not None, "relabelLog/insertPick absent")
    case("D59-1 insertPick renames the shifted UNKNOWN to its new number in the state",
         bool(rl) and rl.get("ok") and [pk[0] for pk in rl.get("picks", [])] == ["Nikola Jokic", "Luka Doncic", "Victor Wembanyama", "UNKNOWN #4"],
         f"got {rl and rl.get('picks')}")
    lines = [l[0] for l in (rl or {}).get("lines", [])]
    case("D59-1 the earlier pick lines are re-numbered and re-seated from the state, notes kept",
         len(lines) == 4 and lines[0] == "  ✓ (R1) #1: Nikola Jokic → Seat 1"
         and lines[1] == "  ✓ (R1) #3: Victor Wembanyama → Seat 3 (YOU)  (assumed over X)", f"got {lines}")
    case("D59-1 the UNKNOWN line reads its new number and fix syntax",
         len(lines) == 4 and lines[2] == "⚠ (R1) #4: UNKNOWN (\"zzz\": no match) — fix with: 4- Name", f"got {lines}")
    case("D59-1 a non-pick line is untouched and pick indices follow the shift",
         len(lines) == 4 and lines[3] == "— your pick, #4 —" and [l[2] for l in rl["lines"]] == [0, 2, 3, None], f"got {rl and rl.get('lines')}")
    case("D59-1 the pick the shift moved onto the owner's seat is reported (movedOn [2]), none moved off",
         bool(rl) and rl.get("movedOn") == [2] and rl.get("movedOff") == [], f"got {rl and (rl.get('movedOn'), rl.get('movedOff'))}")
    case("D59-1 the app re-labels the history after an insert and echoes the card as of now for a pick moved onto YOUR seat",
         "relabelLog(" in app4 and "card as of now" in app4, "app does not consume relabelLog / no card-as-of-now echo")
    case("D59-1 pick lines carry their pick index and kind so the re-render is mechanical",
         'kind: "pick"' in app4 or "kind: \"pick\"" in app4 or 'kind:"pick"' in app4, "log entries carry no pick index")

    print()
    if FAILS:
        print(f"CARD: {len(FAILS)} of {CASES} cases FAILED")
        sys.exit(1)
    print(f"CARD: all {CASES} cases passed")


if __name__ == "__main__":
    main()
