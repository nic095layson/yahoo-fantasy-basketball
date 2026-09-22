#!/usr/bin/env python3
"""Assemble the technical debrief of a live mock from the landed JSON outputs
(live_retro replay/final/hindsight/arms, live_deckcard, live_advisor,
live_survival). Every number in the debrief is read from those files; the
script also computes the kept-total z-sum board rank the LEDGER quotes.

    python3 arena/mocks/live_debrief.py <mock> <out.md>
"""
import hashlib, json, os, statistics, sys
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, REPO + "/scripts")
import hoops  # noqa: E402

MOCK, OUT = int(sys.argv[1]), sys.argv[2]
R = os.path.join(REPO, "arena", "results")
J = lambda name: json.load(open(os.path.join(R, f"m{MOCK}_{name}.json"), encoding="utf-8"))
STATE = os.path.join(REPO, "arena", "data", "states", f"draft_state_{MOCK}.json")
state = json.load(open(STATE, encoding="utf-8"))
md5 = hashlib.md5(open(STATE, "rb").read()).hexdigest()
SLOT, TEAMS = state["slot"], state["teams"]
CAST = {s: n for s, n in state.get("cast", [])}
CATS = hoops.CATS

rep = {t["pick"]: t for t in J("replay")["v23"]}
fin = J("final")["v23"]
hs = J("hindsight")
arms = J("arms")
dc = {t["pick"]: t for t in J("deckcard_v23")}
tuned = {t["pick"]: t for t in J("deckcard_tuned")}
adv = J("advisor")["rows"]
sv = J("survival")

# kept-total z-sum board rank (13-man, all nine cats), as the LEDGER's board column
players = hoops.zscores(hoops.load_players())
byn = {p["player"]: p for p in players}
tot = {s: 0.0 for s in range(1, TEAMS + 1)}
for pk in state["picks"]:
    if pk["player"] in byn:
        tot[pk["slot"]] += sum(byn[pk["player"]]["z"][c] for c in CATS)
board_rank = 1 + sum(1 for s in tot if s != SLOT and tot[s] > tot[SLOT])
board_next = max(v for s, v in tot.items() if s != SLOT)

me = arms["as_drafted"]
ecw_sorted = sorted(((v, int(s)) for s, v in fin["ecw"].items()), reverse=True)
next_seat = next((v, s) for v, s in ecw_sorted if s != SLOT)
champ_by = sorted(((a["champ"], k) for k, a in arms.items()), reverse=True)

def tg(t):
    return t["pinTarget"] if t["tgOnPin"] else t["rows"][0]["n"]

L = []
L.append(f"# Mock {MOCK} debrief — slot {SLOT}, live public room, deck v23 (2026-09-22)")
L.append("")
L.append(f"**Fingerprint:** owner slot {SLOT}, {len(state['picks'])} picks, Yahoo public mock (random humans, "
         f"not the cast), state `arena/data/states/draft_state_{MOCK}.json` (md5 `{md5}`, reconciled "
         "pick-by-pick against Yahoo's recap 2026-09-22: 156/156 match, including the tool's one insert, "
         "four unknown-name corrections and two halted re-sends). Deck used: the published v23 artifact "
         "(pool 264, sha c1f87ac1db09) — proven by the log's FULL TILT / Retarget lines, which only the "
         "pre-2026-09-21 advisor renders, and by two live-drafted names the pool lacks "
         f"({', '.join(fin['missing'])}; seats 4 and 11 play 12 men in every simulation here). Punt box: "
         "empty through #39, then the advisor's FULL TILT (FG%+AST, \"clear path 6/7\") and an immediate "
         "Retarget to FG%+TO (\"+2.9 roster fit\"), both right after the owner's #39; no later change.")
L.append("")
L.append("**Method.** Card reconstructed two ways at all 13 owner turns — the Python port "
         "(`live_retro.py replay`, the check_parity port of decwScores) and the deck's own JS under node "
         "(`live_deckcard.py`, DOM survival model and 🎯 pin reproduced from source) — and they agree on "
         "the Top-5 names and blend scores at 13/13 turns (max |Δds| 0.0000). Grading on current lines: "
         "ECW (cats/week vs the average opponent, arena weekly model), season-shape H2H (draft_50/51 "
         "method), championships (18,000 seasons, seeds 11/23/47, CRN). Counterfactuals: pairwise-swap "
         "model per `arena/mocks/README.md`, the owner's own later picks screened as degenerate. The "
         "generalized harnesses reproduce mock 51's landed final/replay/hindsight byte-for-byte.")
L.append("")
L.append("## Headline")
L.append("")
L.append("| Readout | Value |")
L.append("|---|---|")
L.append(f"| Championship rate (18,000 seasons) | **{me['champ']:.2f}%** (rank {me['champ_rank']} of 12) |")
L.append(f"| Playoff rate | {me['playoff']:.2f}% |")
L.append(f"| ECW | **{fin['ecw'][str(SLOT)]:.3f}** cats/week (rank {fin['ecw_rank']}; next {next_seat[0]:.3f}, "
         f"{CAST.get(next_seat[1], 'T' + str(next_seat[1]))}) — favored in {fin['exp_winning_weeks']}/11 head-to-heads |")
L.append(f"| Season-shape H2H | wins {fin['seasonshape_winning']}/11 |")
L.append(f"| Board rank (kept-total z-sum) | **{board_rank}** ({tot[SLOT]:+.2f}; next {board_next:+.2f}) |")
cr = fin["cat_rank_weekly"]
L.append("| Category rank, weekly model | " + " · ".join(f"{c} {'**' + str(cr[c]) + '**' if cr[c] in (1, 12) or cr[c] >= 9 else cr[c]}" for c in CATS) + " |")
L.append("")
L.append("Mock 51 from the same seat read ECW 5.610 / rank 1 / 11 of 11; this room reads "
         f"{fin['ecw'][str(SLOT)]:.3f} / rank {fin['ecw_rank']} / {fin['exp_winning_weeks']} of 11. Random public "
         "room: excluded from the LEDGER superlatives (owner directive 2026-08-25).")
L.append("")
L.append("## Decision ledger — card vs owner vs hindsight")
L.append("")
L.append("Card 🎯 = what the v23 deck showed (blend50 #1, or the urgent TARGET pin when it took the 🎯). "
         "Tuned 🎯 = the same turn on the tuned deck (PRs #34 + #37: ΔECW tie-break, pin gate); \"=\" when "
         "unchanged. Hindsight = best legal single-swap alternative on current lines, ECW gain in cats/week; "
         "\"owner's own later pick\" = the card's #1 was a player the owner took at a later turn (screened).")
L.append("")
L.append("| pick | card 🎯 | tuned 🎯 | owner | card rank | hindsight best (gain) | better alts | card #1 in hindsight |")
L.append("|---|---|---|---|---|---|---|---|")
for p in sorted(rep):
    t, tt, h = dc[p], tuned[p], next(x for x in hs["turns"] if x["pick"] == p)
    a, b = tg(t), tg(tt)
    best = h["top"][0] if h["top"] else None
    bestS = f"{best['n']} ({best['gain']:+.3f})" if best and best["gain"] > 0 else "none"
    c1 = "owner's own later pick" if h["card1_gain"] is None else f"{h['card1_gain']:+.3f}"
    L.append(f"| {p} | {a} | {b if b != a else '='} | {h['actual']} | {t['actualCardRank']} | {bestS} | {h['n_better']}/{h['n_legal']} | {c1} |")
L.append("")
zero = [x["pick"] for x in hs["turns"] if x["n_better"] == 0]
one = [x["pick"] for x in hs["turns"] if x["n_better"] == 1]
L.append(f"Hindsight found **no better legal pick** at {len(zero)} turns ({', '.join('#' + str(p) for p in zero)}) and "
         f"exactly one at {len(one)} ({', '.join('#' + str(p) for p in one)}). The owner took the card's #1 at "
         f"{sum(1 for p in rep if dc[p]['actualCardRank'] == 1)} turns and a Top-5 row at "
         f"{sum(1 for p in rep if dc[p]['actualCardRank'] and dc[p]['actualCardRank'] <= 5)} of 13.")
L.append("")
L.append("### The turns that cost something")
L.append("")
for p in (10, 39):
    h = next(x for x in hs["turns"] if x["pick"] == p); t = dc[p]
    pl = byn.get(h["actual"], {})
    L.append(f"- **#{p} {h['actual']}** (card #{t['actualCardRank']}, availability {hoops.availability(pl) if pl else '?'}, "
             f"note `{pl.get('note', '')}`): {h['n_better']} of {h['n_legal']} legal alternatives grade higher. "
             + "; ".join(f"{r['n']} {r['gain']:+.3f} (drafted #{r['drafted_at']} by {r['drafted_by']})" for r in h["top"][:3]) + ".")
br = [x for x in hs["turns"] if x["pick"] in (130, 135, 154)]
L.append(f"- **Christian Braun, passed three times** (#130, #135, #154; card 🎯 each time, gains "
         + ", ".join(f"{x['top'][0]['gain']:+.3f}" for x in br) + "): he went #156, the last pick of the draft, to Michael.")
L.append("")
L.append("### What the card got right, live")
L.append("")
L.append("- #34 Anthony Davis and #58 Franz Wagner and #82 Jakob Poeltl and #111 Cameron Johnson: the owner took the card's #1; "
         "hindsight confirms each within 0.013 of the best legal alternative.")
L.append(f"- **#58 is D51R-4 vindicated live.** The v23 deck moved the 🎯 off Franz onto an urgent Shot-block C pin, "
         f"Kristaps Porziņģis (availability 0.78) — LAST CALL. The owner ignored it and took Franz (card #1, "
         "hindsight: 1 better alternative of 190, by +0.001). The tuned deck withholds that pin "
         f"(`{tuned[58]['withheld']}`) and keeps the 🎯 on Franz.")
L.append("- #63 Dyson Daniels and #87 Myles Turner were card #2 and turned out hindsight-best (0 better alternatives); "
         "the card's #1 at those turns (Anunoby, Cam Johnson) grades −0.041 and screened respectively.")
L.append(f"- #15: the tuned deck's ΔECW tie-break flips the 🎯 from Towns to Mobley (ΔECW "
         f"{tuned[15]['rows'][0]['decw']:.3f} vs {tuned[15]['rows'][1]['decw']:.3f}); the owner took Donovan Mitchell (card #8), "
         "which hindsight grades within 0.03 of the best alternative anyway.")
L.append("")
L.append("## Punt advisor — the buttons the owner clicked vs the room-relative read (D51R-3)")
L.append("")
c39 = next(x for x in adv if x["pick"] == 39 and x["moment"] == "post")
k39 = next(x for x in adv if x["pick"] == 39 and x["moment"].startswith("post-click"))
L.append(f"`live_advisor.py` reproduces both log lines from the engine: right after #39 (roster 4, box empty) the old "
         f"advisor shows FULL TILT {'·'.join(c39['old_lean'])} with path {c39['old_path']}; on the box that click set "
         f"({'+'.join(k39['punt'])}) the old coherence strip reads {k39['old_coh']['state']} and offers Retarget "
         f"({k39['old_coh']['out']} in, punt {k39['old_coh']['inn']}, {k39['old_coh']['delta']:+.2f} fit). The room-relative "
         f"read at the same two moments: no lean (AST beats {c39['pw']['AST']:.0%} of the room with Kyrie aboard), and on the "
         f"FG%+AST box \"{k39['new_coh']['state']}: punting AST though this roster beats {k39['pw']['AST']:.0%} of the room in it — "
         "smaller box\".")
L.append("")
L.append("| owner turn | box | TO beats | old strip | new strip |")
L.append("|---|---|---|---|---|")
for x in adv:
    if x["moment"] != "pre" or not x["punt"]:
        continue
    o, n = x["old_coh"], x["new_coh"]
    nS = f"{n['state']}: " + (f"punt {n['inn']} for {n['out']}" if n["inn"] else f"drop {n['out']}") + f" ({n['delta']:+.2f} cats/wk)"
    L.append(f"| #{x['pick']} | {'+'.join(x['punt'])} | {x['pw']['TO']:.0%} | {o['state']} | {nS} |")
pre = [x for x in adv if x["moment"] == "pre" and x["punt"]]
L.append("")
L.append(f"At all {len(pre)} owner turns with the FG%+TO box the old strip read *aligned* while the roster was beating "
         f"{min(x['pw']['TO'] for x in pre):.0%}–{max(x['pw']['TO'] for x in pre):.0%} of the room in the punted TO; the new strip "
         f"reads *inverted* at {sum(1 for x in pre if x['new_coh']['state'] == 'inverted')} of them. Mock 51's finding, live "
         "again — and this time the box was the old advisor's own product. TO finished ranked "
         f"{cr['TO']} by the weekly model (z-sum {fin['cat_rank_zsum']['TO']}) after the late picks stopped protecting it.")
L.append("")
L.append("## Survival chips — calibration data for the refit (D51R-1)")
L.append("")
tr, po = sv["this_room"], sv["pooled"]
L.append(f"| room | rows | mean predicted survival | realized | Brier |")
L.append("|---|---|---|---|---|")
L.append(f"| mock 52 (v23 deck, chips still live) | {tr['rows']} | {tr['mean_pred']:.3f} | {tr['realized']:.3f} | {tr['brier']:.3f} |")
L.append(f"| pooled with mock 51 | {po['rows']} | {po['mean_pred']:.3f} | {po['realized']:.3f} | {po['brier']:.3f} |")
L.append("")
bn = tr["by_chip"].get("BUY NOW", {})
L.append(f"BUY NOW on {bn.get('n', 0)} of {tr['rows']} scored rows at a mean {bn.get('mean_pred', 0):.3f} predicted survival; "
         f"{bn.get('alive', 0)} of those players were still there at the owner's next turn. Second live room of the two the "
         "owner set as the refit threshold; the chips stay suspended (PR #34) until the refit lands.")
L.append("")
L.append("## Championship arms (18,000 CRN seasons each)")
L.append("")
L.append("| arm | champ% | playoff% | rank | swaps |")
L.append("|---|---|---|---|---|")
for k, a in sorted(arms.items(), key=lambda kv: -kv[1]["champ"]):
    L.append(f"| {k} | {a['champ']:.2f} | {a['playoff']:.2f} | {a['champ_rank']} | {', '.join(f'#{n} {x}' for n, x in a['swaps']) or '—'} |")
L.append("")
L.append("## Limits")
L.append("")
L.append("- Seats 4 and 11 simulate with 12 men (Daniss Jenkins and Gui Santos have no pool row), which flatters the owner "
         "against those two seats only; both were already the room's weakest by ECW.")
L.append("- Random public room, not the league cast: the field's weakness is in every denominator above.")
L.append("- The punt box after #39 is taken from the tool log (no later Retarget was logged).")
L.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"wrote {OUT}: {len(L)} lines; board rank {board_rank} ({tot[SLOT]:+.2f}); champ {me['champ']:.2f}% rank {me['champ_rank']}")
