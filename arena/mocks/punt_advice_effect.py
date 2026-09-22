#!/usr/bin/env python3
"""D51R-3 effect measurement: for every owner turn of every committed mock
state, replay the punt advisor as it shipped before 2026-09-21 (13-man
z-sum ranks: FULL TILT pivot, Build-read Adopt offer, coherence Retarget)
against the room-relative read that replaced it (catWinProb / puntRead /
coherenceRead from the deck's own engine block, the consecutive-turn
counter chained across owner turns exactly as the app persists it).

For each proposal — old or new, punt-pivot or coherence swap — the row
records the proposed category's 13-man z-sum rank AND its share of the
room beaten in a typical week, so the branch rule can be counted: a
room-relative advisor must never propose punting a category the roster is
winning against the majority of the room (pw >= 0.50) or ranked top-4.

Mock 51's punt box changed during the draft (debrief 2026-09-21); its
timeline is replayed. Other punted states carry their final box throughout
(their boxes were set pre-draft). Writes arena/results/m51_punt_advice_effect.json.

    python3 arena/mocks/punt_advice_effect.py
"""
import json, os, re, subprocess, tempfile
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
html = open(os.path.join(REPO, "docs", "draft-deck.html"), encoding="utf-8").read()
ex = lambda tag: re.search(r'<script id="%s">(.*?)</script>' % tag, html, re.S).group(1)
tmp = tempfile.mkdtemp()
mod = os.path.join(tmp, "deck.mjs")
open(mod, "w", encoding="utf-8").write(ex("data") + "\n" + ex("engine") +
    "\nexport const api = { PLAYERS, CATS, buildRosters, teamOfPick, categoryRanks, rankTiers, puntPath, totalValue,"
    " catWinProb, puntRead, coherenceRead, winPath, PUNT_BUTTONS, PUNT_LOW, PUNT_EXIT, PUNT_TURNS, PUNT_WIN, PUNT_PATH };\n")
sdir = os.path.join(REPO, "arena", "data", "states")
states = {fn: json.load(open(os.path.join(sdir, fn), encoding="utf-8")) for fn in sorted(os.listdir(sdir)) if fn.endswith(".json")}
# mock 51's punt box as the owner set it during the draft (pick index thresholds, 0-based)
TIMELINE = {"draft_state_51.json": [[0, []], [46, ["AST", "FT%"]], [52, ["FT%", "TO"]], [63, ["TO", "FG%"]], [111, ["TO", "AST"]]]}
fixture = os.path.join(tmp, "in.json"); json.dump({"states": states, "timeline": TIMELINE}, open(fixture, "w"))
driver = os.path.join(tmp, "run.mjs")
open(driver, "w", encoding="utf-8").write(r"""
import { api } from "__MOD__"; import fs from "node:fs";
const IN = JSON.parse(fs.readFileSync("__IN__", "utf8")); const { PLAYERS, CATS } = api;
const out = { consts: { PUNT_BUTTONS: api.PUNT_BUTTONS, PUNT_LOW: api.PUNT_LOW, PUNT_EXIT: api.PUNT_EXIT, PUNT_TURNS: api.PUNT_TURNS, PUNT_WIN: api.PUNT_WIN, PUNT_PATH: api.PUNT_PATH }, rows: [] };
for (const [name, st0] of Object.entries(IN.states)) {
  let seen = {};
  for (let n = 0; n < st0.picks.length; n++) {
    if (api.teamOfPick(n, st0.teams) !== st0.slot) continue;
    let punt = st0.punt || [];
    if (IN.timeline[name]) for (const [after, p] of IN.timeline[name]) if (n >= after) punt = p;
    const st = { teams: st0.teams, slot: st0.slot, size: st0.size, punt, picks: st0.picks.slice(0, n) };
    const rosters = api.buildRosters(st, PLAYERS); const mine = rosters[st.slot] || [];
    if (mine.length < 2) continue;
    const opp = []; for (let s = 1; s <= st.teams; s++) if (s !== st.slot && rosters[s] && rosters[s].length) opp.push(rosters[s]);
    const { ranks, totals } = api.categoryRanks(st, PLAYERS);
    const pw = api.catWinProb(mine, opp);
    const kept = CATS.filter(c => !punt.includes(c));
    const tiers = api.rankTiers(st.teams);
    const row = { state: name, pick: n + 1, roster: mine.length, punt, ranks, pw: pw && Object.fromEntries(CATS.map(c => [c, +pw[c].toFixed(3)])) };
    /* ---- OLD advisor (pre-2026-09-21), z-sum ranks ---- */
    if (!punt.length && mine.length >= 4) {
      const drift = kept.filter(c => ranks[c] >= tiers.lostFrom).sort((a, b) => ranks[b] - ranks[a]).slice(0, 3);
      if (drift.length) {
        const firm = drift.length >= 2 || ranks[drift[0]] >= st.teams;
        const path = api.puntPath(ranks, kept, drift, st.teams);
        row.old_lean = drift;
        row.old_fulltilt = !!(firm && path.clear);
        row.old_fulltilt_set = row.old_fulltilt ? drift : [];
      }
    }
    if (mine.length >= 5) {
      const drift = kept.filter(c => ranks[c] >= tiers.lostFrom).sort((a, b) => ranks[b] - ranks[a] || totals[st.slot][a] - totals[st.slot][b]);
      const adoptList = drift.slice(0, Math.max(0, 3 - punt.length));
      const path = adoptList.length ? api.puntPath(ranks, kept, adoptList, st.teams) : null;
      row.old_adopt = !!(adoptList.length && path.clear); row.old_adopt_set = row.old_adopt ? adoptList : [];
    }
    if (punt.length && mine.length >= 3) {
      const keptSum = arr => { const ps = new Set(arr); return mine.reduce((t, q) => t + api.totalValue(q, ps), 0); };
      const declared = keptSum(punt); let best = null;
      for (const o of punt) for (const i of CATS.filter(c => !punt.includes(c))) {
        const alt = punt.filter(c => c !== o).concat(i); const v = keptSum(alt);
        if (!best || v > best.v) best = { alt, v, out: o, inn: i };
      }
      const delta = best.v - declared;
      row.old_coh = { state: delta > 2 ? "inverted" : delta > 0.75 ? "drifting" : "aligned", out: best.out, inn: best.inn, delta: +delta.toFixed(2) };
    }
    /* ---- NEW advisor (D51R-3), room-relative, counter chained per owner turn ---- */
    if (!punt.length && mine.length >= 4 && pw) {
      const r = api.puntRead(pw, kept, seen, true); seen = r.seen;
      row.new_lean = r.lean; row.new_advise = r.advise; row.new_set = r.advise ? r.punt : []; row.new_clear = r.clear;
      row.new_path = `${r.winnable.length}/${r.keptAfter.length}`; row.new_seen = r.seen;
    }
    if (punt.length && mine.length >= 3 && pw) {
      const c = api.coherenceRead(pw, punt);
      row.new_coh = c && { state: c.state, out: c.best && c.best.out, inn: c.best && c.best.inn, delta: +c.delta.toFixed(3) };
    }
    out.rows.push(row);
  }
}
process.stdout.write(JSON.stringify(out));
""".replace("__MOD__", mod).replace("__IN__", fixture))
r = subprocess.run(["node", driver], capture_output=True, text=True); assert r.returncode == 0, r.stderr[:2000]
res = json.loads(r.stdout)
rows = res["rows"]

def proposals(kind):
    """(row, category) pairs the advisor proposed to PUNT under `kind`."""
    outp = []
    for x in rows:
        if kind == "old":
            for c in x.get("old_fulltilt_set", []) + x.get("old_adopt_set", []):
                outp.append((x, c, "pivot"))
            oc = x.get("old_coh")
            if oc and oc["state"] != "aligned":
                outp.append((x, oc["inn"], "coherence"))
        else:
            for c in x.get("new_set", []):
                outp.append((x, c, "pivot"))
            nc = x.get("new_coh")
            if nc and nc["state"] != "aligned" and nc["inn"] is not None:
                outp.append((x, nc["inn"], "coherence"))
    return outp

summary = {"owner_turns": len(rows), "states": len(states), "consts": res["consts"]}
for kind in ("old", "new"):
    ps = proposals(kind)
    top4 = [(x, c, k) for x, c, k in ps if x["ranks"][c] <= 4]
    winning = [(x, c, k) for x, c, k in ps if x["pw"] and x["pw"][c] >= 0.50]
    summary[kind] = {
        "turns_with_pivot_advice": sum(1 for x in rows if (x.get("old_fulltilt") or x.get("old_adopt")) if kind == "old") if kind == "old" else sum(1 for x in rows if x.get("new_advise")),
        "proposals": len(ps), "pivot_proposals": sum(1 for _, _, k in ps if k == "pivot"), "coherence_proposals": sum(1 for _, _, k in ps if k == "coherence"),
        "on_top4_zsum": len(top4), "on_winning_majority_pw": len(winning),
        "examples_winning": [f"{x['state']} #{x['pick']} {k}: punt {c} (z-rank {x['ranks'][c]}, beats {x['pw'][c]:.2f} of the room)" for x, c, k in winning][:12],
        "examples_top4": [f"{x['state']} #{x['pick']} {k}: punt {c} (z-rank {x['ranks'][c]}, beats {x['pw'][c]:.2f} of the room)" for x, c, k in top4][:12],
    }
summary["new"]["coherence_drop_advice"] = sum(1 for x in rows if x.get("new_coh") and x["new_coh"]["state"] != "aligned" and x["new_coh"]["inn"] is None)
summary["new"]["watching_turns_no_advice"] = sum(1 for x in rows if x.get("new_lean") and not x.get("new_advise"))
summary["new"]["advised_turns_clear"] = sum(1 for x in rows if x.get("new_advise") and x.get("new_clear"))
summary["new"]["advised_turns_no_clear_path"] = sum(1 for x in rows if x.get("new_advise") and not x.get("new_clear"))
summary["old"]["fulltilt_turns"] = sum(1 for x in rows if x.get("old_fulltilt"))
summary["old"]["adopt_offer_turns"] = sum(1 for x in rows if x.get("old_adopt"))
by = {}
for x in rows:
    b = by.setdefault(x["state"], {"turns": 0, "old_pivot": 0, "new_advise": 0, "old_coh_swap": 0, "new_coh_swap": 0})
    b["turns"] += 1
    b["old_pivot"] += bool(x.get("old_fulltilt") or x.get("old_adopt"))
    b["new_advise"] += bool(x.get("new_advise"))
    b["old_coh_swap"] += bool(x.get("old_coh") and x["old_coh"]["state"] != "aligned")
    b["new_coh_swap"] += bool(x.get("new_coh") and x["new_coh"]["state"] != "aligned")
summary["by_state"] = by
json.dump({"summary": summary, "rows": rows}, open(os.path.join(REPO, "arena", "results", "m51_punt_advice_effect.json"), "w"), indent=1)

print(f"owner turns with a roster of 2+: {summary['owner_turns']} across {summary['states']} states; constants {summary['consts']}")
for kind in ("old", "new"):
    s = summary[kind]
    print(f"{kind.upper():<4} proposals to punt a category: {s['proposals']} (pivot {s['pivot_proposals']}, coherence swap {s['coherence_proposals']})"
          f" — on a top-4 z-sum cat: {s['on_top4_zsum']}; on a cat beating >= 50% of the room: {s['on_winning_majority_pw']}")
    for e in s["examples_winning"]:
        print("      winning:", e)
    for e in s["examples_top4"]:
        print("      top-4:  ", e)
print(f"OLD  FULL TILT turns {summary['old']['fulltilt_turns']}, Adopt-offer turns {summary['old']['adopt_offer_turns']}")
print(f"NEW  watching (lean, no advice yet) {summary['new']['watching_turns_no_advice']}; advised with clear path {summary['new']['advised_turns_clear']}; advised, no clear path {summary['new']['advised_turns_no_clear_path']}; coherence 'drop it, punt smaller' reads {summary['new']['coherence_drop_advice']}")
print("per state {turns, old pivot turns, new advised turns, old coherence swaps, new coherence swaps}:")
for k, v in by.items():
    print(f"  {k:<26} {v}")
print("\nmock 51 owner turns (the retro's case):")
for x in rows:
    if x["state"] != "draft_state_51.json": continue
    pwq = " ".join(f"{c}:{x['pw'][c]:.2f}" for c in ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]) if x["pw"] else "-"
    old = ("FULL TILT " + "·".join(x["old_fulltilt_set"])) if x.get("old_fulltilt") else ("Adopt " + "·".join(x["old_adopt_set"])) if x.get("old_adopt") else (f"coh {x['old_coh']['state']} punt {x['old_coh']['inn']}" if x.get("old_coh") else "-")
    new = (f"ADVISE {'·'.join(x['new_set'])} clear={x['new_clear']} {x['new_path']}") if x.get("new_advise") else (f"watch {x['new_lean']} seen={x['new_seen']}" if x.get("new_lean") else (f"coh {x['new_coh']['state']} {'punt ' + x['new_coh']['inn'] if x['new_coh']['inn'] else 'drop ' + x['new_coh']['out']} (+{x['new_coh']['delta']})" if x.get("new_coh") else "-"))
    print(f"  #{x['pick']:>3} r{x['roster']:>2} punt={x['punt']!s:<14} old: {old:<28} new: {new}")
    print(f"        pw {pwq}")
