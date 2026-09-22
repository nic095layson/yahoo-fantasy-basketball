#!/usr/bin/env python3
"""Data-driven debrief of a live mock (mock 53 onward, 2026-09-22): every number
and every turn-level statement is computed from the landed JSON outputs
(live_retro replay/final/hindsight/arms, live_deckcard, live_advisor,
live_survival) — no mock-specific prose baked in. The pool tag comes from
live_retro.MOCKS.

    python3 arena/mocks/live_debrief_generic.py <mock> <out.md> [deck_label]
"""
import hashlib, json, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, REPO + "/scripts"); sys.path.insert(0, HERE)
import hoops  # noqa: E402
MOCK, OUT = int(sys.argv[1]), sys.argv[2]
LABEL = sys.argv[3] if len(sys.argv) > 3 else "deck (current main)"
R = os.path.join(REPO, "arena", "results")
J = lambda name: json.load(open(os.path.join(R, f"m{MOCK}_{name}.json"), encoding="utf-8"))
STATE = os.path.join(REPO, "arena", "data", "states", f"draft_state_{MOCK}.json")
state = json.load(open(STATE, encoding="utf-8")); md5 = hashlib.md5(open(STATE, "rb").read()).hexdigest()
SLOT, TEAMS, SIZE = state["slot"], state["teams"], state["size"]
CAST = {s: n for s, n in state.get("cast", [])}; CATS = hoops.CATS
_argv = sys.argv; sys.argv = ["live_retro.py", str(MOCK)]
import live_retro  # noqa: E402  (reads MOCKS/TAGS for this mock)
sys.argv = _argv
TAG = live_retro.GRADE_TAG
rep = {t["pick"]: t for t in J("replay")[TAG]}; fin = J("final")[TAG]; hs = J("hindsight"); arms = J("arms")
dc = {t["pick"]: t for t in J(f"deckcard_{TAG}")}; adv = J("advisor")["rows"]; sv = J("survival")
players = hoops.zscores(hoops.load_players()); byn = {p["player"]: p for p in players}
tot = {s: 0.0 for s in range(1, TEAMS + 1)}
for pk in state["picks"]:
    if pk["player"] in byn: tot[pk["slot"]] += sum(byn[pk["player"]]["z"][c] for c in CATS)
board_rank = 1 + sum(1 for s in tot if s != SLOT and tot[s] > tot[SLOT]); board_next = max(v for s, v in tot.items() if s != SLOT)
me = arms["as_drafted"]; ecw_sorted = sorted(((v, int(s)) for s, v in fin["ecw"].items()), reverse=True)
next_seat = next((v, s) for v, s in ecw_sorted if s != SLOT)
tg = lambda t: t["pinTarget"] if t["tgOnPin"] else t["rows"][0]["n"]
turns = sorted(rep); H = {x["pick"]: x for x in hs["turns"]}
def brier_base(rows, alive): p = alive / rows; return p * (1 - p) ** 2 + (1 - p) * p ** 2
L = [f"# Mock {MOCK} debrief — slot {SLOT}, live public room, {LABEL}", ""]
L.append(f"**Fingerprint.** owner slot {SLOT}, {len(state['picks'])} picks, Yahoo public mock; state `arena/data/states/draft_state_{MOCK}.json` "
         f"(md5 `{md5}`), reconciled pick-by-pick against Yahoo's recap (156/156 incl. the tool's inserts, unknown-name fixes and undos — "
         f"`m{MOCK}_insert_integrity.json`). Pool tag `{TAG}`; poolless names in this room: {', '.join(fin.get('missing', [])) or 'none'}. "
         f"Punt box: {'none declared' if not state.get('punt') else ', '.join(state['punt'])}.")
L.append("")
L.append("**Method.** Card reconstructed two ways at every owner turn (Python port `live_retro.py replay`; the deck's own JS under node, "
         "`live_deckcard.py`). Grading on current lines: ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H, "
         "championships (18,000 CRN seasons). Counterfactuals: pairwise-swap model per `arena/mocks/README.md`.")
L.append(""); L.append("## Headline"); L.append(""); L.append("| Readout | Value |"); L.append("|---|---|")
L.append(f"| Championship rate (18,000 seasons) | **{me['champ']:.2f}%** (rank {me['champ_rank']} of {TEAMS}) |")
L.append(f"| Playoff rate | {me['playoff']:.2f}% |")
L.append(f"| ECW | **{fin['ecw'][str(SLOT)]:.3f}** cats/week (rank {fin['ecw_rank']}; next {next_seat[0]:.3f}, {CAST.get(next_seat[1], 'T' + str(next_seat[1]))}) — favored in {fin['exp_winning_weeks']}/{TEAMS - 1} head-to-heads |")
L.append(f"| Season-shape H2H | wins {fin['seasonshape_winning']}/{TEAMS - 1} |")
L.append(f"| Board rank (kept-total z-sum) | **{board_rank}** ({tot[SLOT]:+.2f}; next {board_next:+.2f}) |")
cr = fin["cat_rank_weekly"]
L.append("| Category rank, weekly model | " + " · ".join(f"{c} {'**' + str(cr[c]) + '**' if cr[c] in (1, TEAMS) or cr[c] >= 9 else cr[c]}" for c in CATS) + " |")
L.append(""); L.append("Random public room: excluded from the LEDGER superlatives (owner directive 2026-08-25)."); L.append("")
L.append("## Decision ledger — card vs owner vs hindsight"); L.append("")
L.append("Card 🎯 = what the deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). Hindsight = best legal single-swap "
         "alternative on current lines, ECW gain in cats/week; \"owner's own later pick\" = the card's #1 was a player the owner took later (screened).")
L.append(""); L.append("| pick | card 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |"); L.append("|---|---|---|---|---|---|---|")
for p in turns:
    t, h = dc[p], H[p]; best = h["top"][0] if h["top"] else None
    bestS = f"{best['n']} ({best['gain']:+.3f})" if best and best["gain"] > 0 else "none"
    c1 = "owner's own later pick" if h["card1_gain"] is None else f"{h['card1_gain']:+.3f}"
    L.append(f"| {p} | {tg(t)} | {h['actual']} | {t['actualCardRank']} | {bestS} | {h['n_better']}/{h['n_legal']} | {c1} |")
L.append("")
zero = [p for p in turns if H[p]["n_better"] == 0]; one = [p for p in turns if H[p]["n_better"] == 1]
took1 = [p for p in turns if dc[p]["actualCardRank"] == 1]; top5 = [p for p in turns if dc[p]["actualCardRank"] and dc[p]["actualCardRank"] <= 5]
L.append(f"Hindsight found **no better legal pick** at {len(zero)} turns ({', '.join('#' + str(p) for p in zero) or '—'}) and exactly one at "
         f"{len(one)} ({', '.join('#' + str(p) for p in one) or '—'}). The owner took the card's #1 at {len(took1)} turns "
         f"({', '.join('#' + str(p) for p in took1) or '—'}) and a Top-5 row at {len(top5)} of {len(turns)}.")
L.append(""); L.append("### The turns that cost the most (by hindsight gain)"); L.append("")
costly = sorted(turns, key=lambda p: -(H[p]["top"][0]["gain"] if H[p]["top"] else 0))[:3]
for p in costly:
    h, t = H[p], dc[p]; pl = byn.get(h["actual"], {})
    if not h["top"] or h["top"][0]["gain"] <= 0: continue
    L.append(f"- **#{p} {h['actual']}** (card #{t['actualCardRank']}, availability {hoops.availability(pl) if pl else '?'}, note `{pl.get('note', '')}`): "
             f"{h['n_better']} of {h['n_legal']} legal alternatives grade higher — " + "; ".join(f"{r['n']} {r['gain']:+.3f} (drafted #{r['drafted_at']} by {r['drafted_by']})" for r in h["top"][:3]) + ".")
pins = [(p, dc[p]) for p in turns if dc[p]["pinTarget"]]
last_call = [f"#{p} {t['pinTarget']}" for p, t in pins if t["tgOnPin"]]
withheld = [f"#{p} {t['pinTarget']} ({t['withheld']})" for p, t in pins if not t["tgOnPin"] and t["withheld"]]
depth = [f"#{p} {t['pinTarget']}" for p, t in pins if not t["tgOnPin"] and not t["withheld"]]
L.append("")
L.append(f"Sixth-row pins: LAST CALL took the 🎯 at {len(last_call)} turn(s) ({', '.join(last_call) or '—'}); urgent pin withheld by the D51R-4 gate at "
         f"{len(withheld)} ({', '.join(withheld) or '—'}); DEPTH WATCH (informational) at {len(depth)} ({', '.join(depth) or '—'}).")
L.append(""); L.append("## Punt advisor (room-relative read, D51R-3)"); L.append("")
leans = [x for x in adv if x["moment"] == "pre" and x.get("new_lean")]
L.append(f"Box empty all draft. Room-relative lean at {len(leans)} of {len([x for x in adv if x['moment'] == 'pre'])} owner turns: "
         + ("; ".join(f"#{x['pick']} {'+'.join(x['new_lean'])}" + (" (advise)" if x.get("new_advise") else "") for x in leans) if leans else "none") + ".")
L.append(""); L.append("## Survival chips — first out-of-sample room for the price-only refit (D51R-1R)"); L.append("")
tr, po = sv["this_room"], sv["pooled"]
L.append("| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |"); L.append("|---|---|---|---|---|---|")
L.append(f"| mock {MOCK} (out of sample) | {tr['rows']} | {tr['mean_pred']:.3f} | {tr['realized']:.3f} | **{tr['brier']:.3f}** | {brier_base(tr['rows'], tr['alive']):.3f} |")
L.append(f"| pooled with mocks 51 + 52 (refit cards) | {po['rows']} | {po['mean_pred']:.3f} | {po['realized']:.3f} | {po['brier']:.3f} | {brier_base(po['rows'], po['alive']):.3f} |")
L.append("")
for lab, d in (("this room", tr), ("pooled", po)):
    bn, ts, qn = d["by_chip"].get("BUY NOW", {}), d["by_chip"].get("TOSS-UP", {}), d["by_chip"].get("None", {})
    L.append(f"- {lab}: BUY NOW {bn.get('n', 0)} rows, {bn.get('n', 0) - bn.get('alive', 0)} gone; TOSS-UP {ts.get('n', 0)} rows, {ts.get('n', 0) - ts.get('alive', 0)} gone; quiet {qn.get('n', 0)} rows, {qn.get('alive', 0)} survived.")
L.append(""); L.append("## Championship arms (18,000 CRN seasons each)"); L.append(""); L.append("| arm | champ% | playoff% | rank | swaps |"); L.append("|---|---|---|---|---|")
for k, a in sorted(arms.items(), key=lambda kv: -kv[1]["champ"]):
    L.append(f"| {k} | {a['champ']:.2f} | {a['playoff']:.2f} | {a['champ_rank']} | {', '.join(f'#{n} {x}' for n, x in a['swaps']) or '—'} |")
L.append(""); L.append("## Limits"); L.append("")
L.append("- Random public room, not the league cast: the field's weakness is in every denominator above.")
L.append(f"- Lines are the current pool ({TAG}); the room may have drafted against the previous same-day build (v24) — identical prices, 66 fewer rows.")
L.append("- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"wrote {OUT}: champ {me['champ']:.2f}% rank {me['champ_rank']}; ECW {fin['ecw'][str(SLOT)]:.3f} rank {fin['ecw_rank']}; board rank {board_rank}; survival OOS Brier {tr['brier']:.3f} vs base {brier_base(tr['rows'], tr['alive']):.3f}")
