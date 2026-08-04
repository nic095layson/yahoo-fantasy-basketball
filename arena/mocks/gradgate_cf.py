"""Gradient-gate experiment (measure-only, September E6/E9 probe).

The shipped deck applies the win-probability gradient to Top-5 ORDER only at
draft slots 1-3 (GRAD_SLOTS = 3). Mocks 27/28/29 were drafted from slots 4/5/6
— just outside that gate — and all three finished mid-table. This asks a
counterfactual question: at those seats, would following the GRADIENT card have
beaten following the COMPOSITE card the deck actually showed?

Usage:  python3 gradgate_cf.py <mock> <arm>
        mock in {27,28,29}; arm in {as_drafted, composite_card, gradient_card}

Card recommendations are read from the replay artifacts, NOT re-derived here:
  mock<NN>_replay.json   — composite card (shipped deck)
  gradall_cards.json     — gradient card (engine patched GRAD_SLOTS 3 -> 12)

Swaps are pairwise and legal-only: the alternative must have been drafted
strictly later than the owner turn it replaces. Arms are applied IN PICK ORDER
against a running board. Two screens are enforced, both learned from earlier
mocks: an alternative that is ALSO an owner pick makes the arm degenerate
(mock 28's keyonte_to_harris), and an alternative already off the board is
illegal (mock 27's CF4). Both are refused, not silently run.
"""
import sys, os, json, random, math

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

SP = "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad"
UP = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/"
MOCKS = {27: ("5130afad-draft_state_16.json", 4),
         28: ("4cb343cd-draft_state_17.json", 5),
         29: ("9c3e53b2-draft_state_18.json", 6)}
CATS = hoops.CATS
byname = {p["player"]: p for p in players}

mock = int(sys.argv[1])
arm = sys.argv[2]
fn, OWNER = MOCKS[mock]
state = json.load(open(UP + fn))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER
picks = state["picks"]
owner_picks = {i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER}


def composite_card():
    out = {}
    for d in json.load(open(f"{SP}/mock{mock}_replay.json")):
        rec = [t["n"] for t in d["top5"] if t["rec"]]
        tgt = d.get("target")
        out[d["pickNo"]] = rec[0] if rec else ((tgt or {}).get("n"))
    return out


def gradient_card():
    rows = json.load(open(f"{SP}/gradall_cards.json"))[str(mock)]
    return {r["pickNo"]: r["grad_pick"] for r in rows}


def seq_for(card):
    """Only turns where the card disagrees with what the owner actually did."""
    seq, skipped = [], []
    order = {pk["player"]: i for i, pk in enumerate(picks)}
    for pn in sorted(owner_picks):
        alt = card.get(pn)
        actual = picks[pn - 1]["player"]
        if not alt or alt == actual:
            continue
        j = order.get(alt)
        if j is None:
            skipped.append((pn, alt, "not drafted in this room"))
            continue
        if j + 1 in owner_picks:
            skipped.append((pn, alt, f"DEGENERATE: alt is also an owner pick (#{j+1})"))
            continue
        if j <= pn - 1:
            skipped.append((pn, alt, f"ILLEGAL: alt sits at #{j+1}, at or before this turn"))
            continue
        seq.append((pn, alt))
    return seq, skipped


def build(seq, dropped=None):
    """Swaps are applied against a RUNNING board. A card may name the same player at
    two owner turns; after the first swap that player is no longer available later, so
    the second occurrence is dropped (recorded), not asserted away. Screening against
    the original order alone is insufficient — that bug killed 3 of 9 cells on the
    first run of this experiment (found by adversarial verification 2026-08-03)."""
    newp = [dict(pk) for pk in picks]
    for pn, alt in seq:
        i = pn - 1
        j = next((k for k in range(len(newp)) if newp[k]["player"] == alt), None)
        if j is None or j <= i:
            if dropped is not None:
                dropped.append([pn, alt, "already consumed by an earlier swap in this arm"])
            continue
        newp[i]["player"], newp[j]["player"] = alt, newp[i]["player"]
    ros = {}
    for pk in newp:
        ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == 156 and all(len(r) == 13 for r in ros.values())
    return ros


def ecw(ros, who=OWNER):
    mod = {i: arena.team_week_model(r) for i, r in ros.items()}
    tot = 0.0
    for c in CATS:
        s = 0.0
        for o in ros:
            if o == who:
                continue
            ma, va = mod[who][0][c], mod[who][1][c]
            mb, vb = mod[o][0][c], mod[o][1][c]
            d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            s += (1 - p) if c == "TO" else p
        tot += s / (len(ros) - 1)
    return tot


if arm == "as_drafted":
    seq, skipped = [], []
elif arm == "composite_card":
    seq, skipped = seq_for(composite_card())
elif arm == "gradient_card":
    seq, skipped = seq_for(gradient_card())
else:
    raise SystemExit(f"unknown arm {arm}")

for pn, alt, why in skipped:
    print(f"  screened out: #{pn} -> {alt}: {why}")

dropped = []
ros = build(seq, dropped)
for pn, alt, why in dropped:
    print(f"  dropped mid-arm: #{pn} -> {alt}: {why}")
SEEDS = [11, 23]
N = 6000
tc = {i: 0 for i in ros}
tp = {i: 0 for i in ros}
for sd in SEEDS:
    c, p = arena.simulate_seasons(ros, N, random.Random(sd))
    for i in ros:
        tc[i] += c[i]
        tp[i] += p[i]
T = N * len(SEEDS)
res = {"mock": mock, "arm": arm,
       "champ": round(100 * tc[OWNER] / T, 2),
       "playoff": round(100 * tp[OWNER] / T, 2),
       "finish": sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1,
       "kept_total": round(sum(sum(pl["z"][c] for c in CATS) for pl in ros[OWNER]), 2),
       "ecw": round(ecw(ros), 3),
       "n_swaps": len(seq), "swaps": seq,
       "screened_out": [[pn, alt, why] for pn, alt, why in skipped],
       "dropped_mid_arm": dropped,
       "n_applied": len(seq) - len(dropped)}
json.dump(res, open(f"{SP}/gradgate_m{mock}_{arm}.json", "w"), indent=1)
print(f"m{mock} {arm:<16} champ {res['champ']:6.2f}%  playoff {res['playoff']:6.2f}%  "
      f"finish {res['finish']:>2}  kept {res['kept_total']:+6.2f}  ECW {res['ecw']:.3f}  "
      f"({len(seq)} swaps)")
