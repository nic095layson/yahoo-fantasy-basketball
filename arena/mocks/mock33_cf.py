"""Mock 33 counterfactual: would a PUNT-AWARE card have produced a better team?

Mock 33 = 12 teams / 13 rounds, owner slot 8, DECLARED PUNT ["FT%","3PTM","PTS"].
Complaint under test: "punt was declared but the system kept proposing centers."

Arms (each 18000 seasons, CRN-paired against the as-drafted baseline):
  ARM0 as_drafted   -- baseline, no swaps.
  ARM1 shipped      -- owner follows the SHIPPED card's #1 at every turn.
                       (shipped ordering = decwScores(): 0.5*pct(dECW) +
                        0.5*pct(adjValue) with an EMPTY punt set -> punt-blind)
  ARM2 punt_aware   -- owner follows the PUNT-AWARE card's #1 at every turn
                       (adjValue with the declared punt, pwins over kept cats).
  ARM3 placebo      -- E11 perturbation control: same number of roster-changing
                       swaps as the winning arm, on the SAME turns, targets drawn
                       at random from the legal available pool.

Recommendations are NOT recomputed here; they are read from the already-computed
per-turn replay (m31_replay.json, fields "shipped" / "puntAware", each a top-5 in
order).  Legality is screened against the RUNNING board, in pick order: a
recommended name that an earlier swap has already consumed is skipped and the
walk descends the top-5.  (This is the mock27-29 lesson: screening against the
ORIGINAL board lets a swap target a player an earlier swap already took.)

Swap model (established, mock28_cf.py / decw_cf.py): PAIRWISE.  The owner takes
`alt` at his turn and the player he actually took is displaced to `alt`'s
original slot -- so the room still drafts 156 distinct players and every roster
still holds 13.  Two boundary cases the earlier harnesses only screened out:
  * alt sits at a LATER OWNER slot -> the swap is legal on the running board but
    roster-neutral; it is applied (so the board is consumed correctly for later
    turns) and reported separately as a no-op swap.
  * alt was never drafted in this room -> no pairwise partner exists.  Default
    mode descends past him (strict pairwise).  MODE=release additionally runs a
    sensitivity variant where the owner simply takes the undrafted player and
    his actual pick goes to free agency (opponents still untouched).

Run: python3 arena/mocks/mock33_cf.py
"""
import sys, os, json, random, math, statistics

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts"), os.path.abspath("arena")] + [
    p for p in sys.path if p not in (os.path.abspath("scripts"), os.path.abspath("arena"))]

import hoops
players = hoops.zscores(hoops.load_players())   # LIVE pool, before arena import
import arena  # noqa: E402

CATS = hoops.CATS
byname = {p["player"]: p for p in players}

STATE = "/root/.claude/uploads/58588377-022f-59e5-ac2c-106514acd881/6ae5fe0f-draft_state_20.json"
SP = os.environ.get(
    "M31_OUT",
    "/tmp/claude-0/-home-user-yahoo-fantasy-basketball/58588377-022f-59e5-ac2c-106514acd881/scratchpad")
REPLAY = f"{SP}/m31_replay.json"
OWNER = 8

state = json.load(open(STATE))
assert state["teams"] == 12 and state["size"] == 13 and state["slot"] == OWNER, state
PUNT = list(state.get("punt") or [])
assert PUNT == ["FT%", "3PTM", "PTS"], PUNT
KEPT = [c for c in CATS if c not in PUNT]
picks = state["picks"]
assert len(picks) == 156
assert not [pk["player"] for pk in picks if pk["player"] not in byname]
OWNER_TURNS = [i + 1 for i, pk in enumerate(picks) if pk["slot"] == OWNER]
assert len(OWNER_TURNS) == 13, OWNER_TURNS

replay = json.load(open(REPLAY))
assert [t["pickNo"] for t in replay] == OWNER_TURNS, "replay turns != owner turns"
for t in replay:                                    # replay must describe THIS draft
    assert t["actual"] == picks[t["pickNo"] - 1]["player"], (t["pickNo"], t["actual"])
CARDS = {k: {t["pickNo"]: [x["n"] for x in t[k]] for t in replay}
         for k in ("shipped", "puntAware")}
for k, cm in CARDS.items():
    for pn, lst in cm.items():
        assert lst, (k, pn, "empty top-5")
        assert all(n in byname for n in lst), (k, pn, [n for n in lst if n not in byname])


# ---------------------------------------------------------------- swap engine
def apply_card(cardmap, mode="pairwise"):
    """Walk owner turns in PICK ORDER against a RUNNING board."""
    newp = [dict(pk) for pk in picks]
    swaps, noops, log = [], [], []
    for pn in OWNER_TURNS:
        i = pn - 1
        cur = newp[i]["player"]
        assert newp[i]["slot"] == OWNER
        took = False
        for nm in cardmap.get(pn, []):
            if nm == cur:
                log.append([pn, nm, "card #1 == actual pick, no swap"])
                took = True
                break
            j = next((k for k in range(len(newp)) if newp[k]["player"] == nm), None)
            if j is None:
                if mode == "release":
                    newp[i]["player"] = nm
                    swaps.append([pn, cur, nm])
                    log.append([pn, nm, f"RELEASE swap: {cur} -> undrafted"])
                    took = True
                    break
                log.append([pn, nm, "undrafted in this room, descend"])
                continue
            if j <= i:
                log.append([pn, nm, f"already off the running board (#{j+1}), descend"])
                continue
            noop = newp[j]["slot"] == OWNER
            newp[i]["player"], newp[j]["player"] = nm, cur
            (noops if noop else swaps).append([pn, cur, nm])
            log.append([pn, nm, ("NO-OP swap (alt is owner's own pick #%d): " % (j + 1))
                        if noop else ("SWAP: %s displaced to #%d (slot %d)"
                                      % (cur, j + 1, newp[j]["slot"]))])
            took = True
            break
        if not took:
            log.append([pn, None, "no legal candidate in top-5, keep actual pick"])
    return finish_board(newp), swaps, noops, log


def finish_board(newp):
    ros = {}
    for pk in newp:
        ros.setdefault(pk["slot"], []).append(byname[pk["player"]])
    names = [pk["player"] for pk in newp]
    assert len(set(names)) == len(names), "duplicate player on the board"
    assert sorted(ros) == list(range(1, 13))
    for s in ros:
        assert len(ros[s]) == 13, (s, len(ros[s]))
    return ros


BASE_ROS = finish_board([dict(pk) for pk in picks])
BASE_SET = {p["player"] for p in BASE_ROS[OWNER]}


def opp_untouched(ros):
    """every non-owner roster identical to as-drafted?  (pairwise swaps DO move
    one opponent player per swap -- this reports how many opponents changed)"""
    n = 0
    for s in ros:
        if s == OWNER:
            continue
        if {p["player"] for p in ros[s]} != {p["player"] for p in BASE_ROS[s]}:
            n += 1
    return n


# ---------------------------------------------------------------- diagnostics
def pcat(ros, who=OWNER):
    """per-category mean win prob vs the 11 opponents (TO inverted)."""
    mod = {i: arena.team_week_model(r) for i, r in ros.items()}
    out = {}
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
        out[c] = s / (len(ros) - 1)
    return out


def ecw(ros, who=OWNER, cats=CATS):
    pc = pcat(ros, who)
    return sum(pc[c] for c in cats)


HEAD_SEEDS = [11, 23, 47]      # ledger convention
HEAD_N = 6000                  # 3 x 6000 = 18000 seasons
BLK_SEEDS = list(range(1001, 1019))   # 18 paired blocks
BLK_N = 1000                          # 18 x 1000 = 18000 seasons, for a paired SE


def run(ros, blocks=True):
    tc = {i: 0 for i in ros}
    tp = {i: 0 for i in ros}
    per_seed = {}
    for sd in HEAD_SEEDS:
        c, p = arena.simulate_seasons(ros, HEAD_N, random.Random(sd))
        per_seed[sd] = 100.0 * c[OWNER] / HEAD_N
        for i in ros:
            tc[i] += c[i]
            tp[i] += p[i]
    T = HEAD_N * len(HEAD_SEEDS)
    blk = []
    if blocks:
        for sd in BLK_SEEDS:
            c, _ = arena.simulate_seasons(ros, BLK_N, random.Random(sd))
            blk.append(100.0 * c[OWNER] / BLK_N)
    kept_z = sum(sum(pl["z"][c] for c in KEPT) for pl in ros[OWNER])
    pc = pcat(ros)
    return {
        "pcat": {c: round(pc[c], 3) for c in CATS},
        "champ": round(100.0 * tc[OWNER] / T, 3),
        "playoff": round(100.0 * tp[OWNER] / T, 3),
        "finish": sorted(ros, key=lambda x: -tc[x]).index(OWNER) + 1,
        "seasons": T,
        "champ_per_seed": {str(k): round(v, 3) for k, v in per_seed.items()},
        "champ_blocks": [round(v, 3) for v in blk],
        "ecw9": round(ecw(ros), 3),
        "ecw_kept6": round(ecw(ros, cats=KEPT), 3),
        "kept_z": round(kept_z, 2),
        "roster": [p["player"] for p in ros[OWNER]],
        "changed_vs_base": sorted({p["player"] for p in ros[OWNER]} - BASE_SET),
        "opp_rosters_touched": opp_untouched(ros),
    }


def placebo_seq(turns, rng):
    """random legal targets on the running board at the SAME turns."""
    newp = [dict(pk) for pk in picks]
    swaps = []
    for pn in sorted(turns):
        i = pn - 1
        cur = newp[i]["player"]
        legal = [k for k in range(i + 1, len(newp)) if newp[k]["slot"] != OWNER]
        if not legal:
            continue
        j = rng.choice(legal)
        alt = newp[j]["player"]
        newp[i]["player"], newp[j]["player"] = alt, cur
        swaps.append([pn, cur, alt])
    return finish_board(newp), swaps


# ---------------------------------------------------------------------- main
OUT = {"mock": 31, "owner": OWNER, "punt": PUNT, "kept": KEPT,
       "seasons_per_arm": HEAD_N * len(HEAD_SEEDS),
       "head_seeds": HEAD_SEEDS, "block_seeds": BLK_SEEDS, "arms": {}}

arms = {}
arms["ARM0_as_drafted"] = (BASE_ROS, [], [], [[None, None, "baseline"]])
for tag, key in (("ARM1_shipped_card", "shipped"), ("ARM2_punt_aware_card", "puntAware")):
    arms[tag] = apply_card(CARDS[key], "pairwise")

for tag, (ros, sw, no, log) in arms.items():
    r = run(ros)
    r["swaps"] = sw
    r["noop_swaps"] = no
    r["n_swaps"] = len(sw)
    r["n_noop_swaps"] = len(no)
    r["log"] = log
    OUT["arms"][tag] = r
    print(f"{tag:<22} champ {r['champ']:6.3f}%  playoff {r['playoff']:6.3f}%  "
          f"finish {r['finish']:>2}  ECW9 {r['ecw9']:.3f}  ECWkept {r['ecw_kept6']:.3f}  "
          f"swaps {len(sw)} (+{len(no)} no-op)")

# ---- ARM3 placebo: matched to the WINNING arm (highest champ%) among 1 & 2
cand = {k: OUT["arms"][k]["champ"] for k in ("ARM1_shipped_card", "ARM2_punt_aware_card")}
winner = max(cand, key=cand.get)
wsw = OUT["arms"][winner]["swaps"]
wturns = [s[0] for s in wsw]
OUT["placebo_matched_to"] = winner
OUT["placebo_turns"] = wturns
print(f"\nplacebo matched to {winner}: {len(wturns)} roster-changing swaps at turns {wturns}")

def placebo_arm(turns, seed0, label):
    pl = []
    for d in range(6):
        rng = random.Random(seed0 + d)
        ros, sw = placebo_seq(turns, rng)
        r = run(ros, blocks=(d == 0))
        r["swaps"] = sw
        r["n_swaps"] = len(sw)
        r["draw"] = d
        pl.append(r)
        print(f"  {label} draw {d}: champ {r['champ']:6.3f}%  playoff {r['playoff']:6.3f}%  "
              f"swaps {len(sw)}  -> {[s[2] for s in sw]}")
    return {"draws": pl,
            "champ": round(statistics.mean(x["champ"] for x in pl), 3),
            "champ_min": min(x["champ"] for x in pl),
            "champ_max": max(x["champ"] for x in pl),
            "playoff": round(statistics.mean(x["playoff"] for x in pl), 3),
            "n_swaps": len(turns), "turns": sorted(turns),
            "champ_blocks": pl[0]["champ_blocks"]}


OUT["arms"]["ARM3_placebo"] = placebo_arm(wturns, 3100, "placebo(win-matched)")
# secondary control so the OTHER arm is not judged against a mismatched
# disturbance count (ARM1 makes 7 roster-changing swaps, ARM2 makes 9)
loser = [k for k in cand if k != winner][0]
lturns = [s[0] for s in OUT["arms"][loser]["swaps"]]
print(f"secondary placebo matched to {loser}: {len(lturns)} swaps at turns {lturns}")
OUT["arms"]["ARM3b_placebo_loser_matched"] = placebo_arm(lturns, 3200, "placebo(alt)")
OUT["placebo_secondary_matched_to"] = loser

# ---- sensitivity: release mode (undrafted recommendations become takeable)
for tag, key in (("SENS1_shipped_release", "shipped"),
                 ("SENS2_punt_aware_release", "puntAware")):
    ros, sw, no, log = apply_card(CARDS[key], "release")
    r = run(ros, blocks=False)
    r["swaps"] = sw
    r["noop_swaps"] = no
    r["n_swaps"] = len(sw)
    r["log"] = log
    OUT["arms"][tag] = r
    print(f"{tag:<24} champ {r['champ']:6.3f}%  playoff {r['playoff']:6.3f}%  swaps {len(sw)}")

# ---- decomposition: how much of each arm's loss is the OWNER's roster getting
# worse vs the pairwise displacement handing an opponent the owner's player?
# FIELD_FIXED holds the 11 opponents exactly as drafted and swaps in only the
# arm's owner roster.  CAVEAT: the displaced players then appear on two teams at
# once, so this is a decomposition diagnostic, NOT a legal draft board.  It is
# reported separately and never used as an arm result.
for tag in ("ARM1_shipped_card", "ARM2_punt_aware_card"):
    ros = {i: list(r) for i, r in BASE_ROS.items()}
    ros[OWNER] = [byname[n] for n in OUT["arms"][tag]["roster"]]
    r = run(ros, blocks=False)
    r["note"] = "DIAGNOSTIC ONLY - opponents held as-drafted, players duplicated"
    OUT["arms"]["FIELDFIXED_" + tag] = r
    print(f"{'FIELDFIXED_'+tag:<34} champ {r['champ']:6.3f}%  playoff {r['playoff']:6.3f}%  "
          f"ECW9 {r['ecw9']:.3f}")

# ---- paired deltas from the 18 CRN blocks
base_blk = OUT["arms"]["ARM0_as_drafted"]["champ_blocks"]
OUT["paired_delta"] = {}
for tag in OUT["arms"]:
    b = OUT["arms"][tag].get("champ_blocks")
    if not b or tag == "ARM0_as_drafted":
        continue
    d = [x - y for x, y in zip(b, base_blk)]
    se = statistics.stdev(d) / math.sqrt(len(d))
    OUT["paired_delta"][tag] = {"mean_pp": round(statistics.mean(d), 3),
                                "se_pp": round(se, 3), "n_blocks": len(d)}
    print(f"paired delta {tag:<24} {statistics.mean(d):+6.3f} pp  +-{se:.3f} (1 SE, 18 CRN blocks)")

json.dump(OUT, open(f"{SP}/mock33_cf_results.json", "w"), indent=1)
print(f"\nwrote {SP}/mock33_cf_results.json")
