"""E9 validation arms: follow the ΔECW card vs as-drafted, with an E11
perturbation-matched placebo (same number of random legal swaps).

Usage: python3 decw_cf.py <mock> <arm>
  arm ∈ {as_drafted, ecw_card, placebo}

Hardened swap machinery (lessons from mocks 27–29): pairwise legal only
(alt drafted strictly LATER than the owner turn), degenerate arms screened
(alt must not be another owner pick), repeated card targets dropped
mid-arm and recorded, never fatal.
"""

import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import sys, os, json, random, math

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}
UP = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/"
SP = os.environ.get(
    "DECW_OUT",
    "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad")
MOCKS = {16: ("fdc581ea-draft_state_5.json", 3), 17: ("39481e0a-draft_state_6.json", 12),
         18: ("01f8de77-draft_state_7.json", 2), 19: ("e1e01942-draft_state_8.json", 4),
         20: ("b6aeaca6-draft_state_9.json", 5), 21: ("773c5fc1-draft_state_10.json", 4),
         23: ("117b5573-draft_state_12.json", 12), 24: ("1a51e011-draft_state_13.json", 1),
         25: ("c0d8a926-draft_state_14.json", 2), 26: ("0371e8b0-draft_state_15.json", 3),
         27: ("5130afad-draft_state_16.json", 4), 28: ("4cb343cd-draft_state_17.json", 5),
         29: ("9c3e53b2-draft_state_18.json", 6), 30: ("e7463e95-draft_state_19.json", 7)}

mock = int(sys.argv[1])
arm = sys.argv[2]
fn, OWNER = MOCKS[mock]
state = json.load(open(UP + fn))
picks = state["picks"]
owner_picks = {i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER}
order = {pk["player"]: i for i, pk in enumerate(picks)}


def screen(card):
    seq, skipped = [], []
    for pn in sorted(owner_picks):
        alt = card.get(pn)
        actual = picks[pn - 1]["player"]
        if not alt or alt == actual:
            continue
        j = order.get(alt)
        if j is None:
            skipped.append((pn, alt, "not drafted in this room"))
        elif j + 1 in owner_picks:
            skipped.append((pn, alt, f"DEGENERATE: alt is owner pick #{j+1}"))
        elif j <= pn - 1:
            skipped.append((pn, alt, f"ILLEGAL: alt at #{j+1}"))
        else:
            seq.append((pn, alt))
    return seq, skipped


def build(seq):
    dropped = []
    newp = [dict(pk) for pk in picks]
    for pn, alt in seq:
        i = pn - 1
        j = next((k for k in range(len(newp)) if newp[k]["player"] == alt), None)
        if j is None or j <= i:
            dropped.append([pn, alt, "consumed by earlier swap"])
            continue
        newp[i]["player"], newp[j]["player"] = alt, newp[i]["player"]
    ros = {}
    for pk in newp:
        ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == 156 and all(len(r) == 13 for r in ros.values())
    return ros, dropped


if arm == "as_drafted":
    seq, skipped = [], []
elif arm == "ecw_card":
    card_rows = json.load(open(f"{SP}/decw_card_m{mock}.json"))
    card = {t["pickNo"]: t["top5"][0]["n"] for t in card_rows if t["top5"]}
    seq, skipped = screen(card)
elif arm == "placebo":
    # E11: same NUMBER of applied swaps as the ecw arm, random legal targets
    card_rows = json.load(open(f"{SP}/decw_card_m{mock}.json"))
    card = {t["pickNo"]: t["top5"][0]["n"] for t in card_rows if t["top5"]}
    ecw_seq, _ = screen(card)
    _, ecw_dropped = build(ecw_seq)
    n_target = len(ecw_seq) - len(ecw_dropped)
    rng = random.Random(1000 + mock)
    turns = [pn for pn, _ in ecw_seq]
    rng.shuffle(turns)
    seq, skipped, used = [], [], set()
    for pn in sorted(turns[:n_target]):
        legal = [q["player"] for k, q in enumerate(picks)
                 if k > pn - 1 and k + 1 not in owner_picks and q["player"] not in used]
        if not legal:
            continue
        alt = rng.choice(legal)
        used.add(alt)
        seq.append((pn, alt))
else:
    raise SystemExit(f"unknown arm {arm}")

for pn, alt, why in skipped:
    print(f"  screened out: #{pn} -> {alt}: {why}")
ros, dropped = build(seq)
for pn, alt, why in dropped:
    print(f"  dropped mid-arm: #{pn} -> {alt}: {why}")

SEEDS = [int(x) for x in os.environ.get("DECW_SEEDS", "11,23").split(",")]
N = int(os.environ.get("DECW_N", "6000"))
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
       "n_applied": len(seq) - len(dropped),
       "swaps": seq, "dropped": dropped,
       "screened_out": [[pn, alt, why] for pn, alt, why in skipped]}
suffix = os.environ.get("DECW_TAG", "")
json.dump(res, open(f"{SP}/decw_cf_m{mock}_{arm}{suffix}.json", "w"), indent=1)
print(f"m{mock} {arm:<12} champ {res['champ']:6.2f}%  playoff {res['playoff']:6.2f}%  "
      f"finish {res['finish']:>2}  ({res['n_applied']} swaps applied)")
