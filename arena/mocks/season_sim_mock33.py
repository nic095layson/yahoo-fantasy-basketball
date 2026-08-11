"""Mock 33 (slot 10, no punt declared (balanced build)) — season sim + readouts.

First harness written under LESSONS.md lesson 13 (evidence-landing law):
repo-relative paths only; the draft state lives at
arena/data/states/draft_state_mock33.json and the output JSON is committed
next to the results. Fresh clone + `python3 arena/mocks/season_sim_mock33.py`
regenerates every number quoted in the mock-31 debrief and LEDGER row.
"""

import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import sys, os, json, random

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(REPO)
sys.path = [os.path.join(REPO, "scripts"), os.path.join(REPO, "arena")] + [
    p for p in sys.path if p not in (os.path.join(REPO, "scripts"), os.path.join(REPO, "arena"))]

import hoops
players = hoops.zscores(hoops.load_players())
import arena  # noqa: E402

STATE = os.path.join(REPO, "arena", "data", "states", "draft_state_mock33.json")
state = json.load(open(STATE))
OWNER = state["slot"]
assert state["teams"] == 12 and state["size"] == 13 and OWNER == 10, state
picks = state["picks"]
assert len(picks) == 156, len(picks)
DECLARED_PUNT = state.get("punt", [])

byname = {p["player"]: p for p in players}
ALIAS = {}  # fill only if a name genuinely differs between deck pool and state
missing = [pk["player"] for pk in picks if ALIAS.get(pk["player"], pk["player"]) not in byname]
assert not missing, f"UNMATCHED (fix or alias, never drop silently): {missing}"

rosters = {}
for pk in picks:
    rosters.setdefault(pk["slot"], []).append(byname[ALIAS.get(pk["player"], pk["player"])])
assert sorted(rosters) == list(range(1, 13))
for s in sorted(rosters):
    assert len(rosters[s]) == 13, (s, len(rosters[s]))
allnames = [pk["player"] for pk in picks]
assert len(set(allnames)) == len(allnames), "duplicate picks!"

SEEDS = [11, 23, 47]
N = 6000
tot_c = {i: 0 for i in rosters}
tot_p = {i: 0 for i in rosters}
per_seed = {}
for sd in SEEDS:
    c, p = arena.simulate_seasons(rosters, N, random.Random(sd))
    per_seed[sd] = (dict(c), dict(p))
    for i in rosters:
        tot_c[i] += c[i]
        tot_p[i] += p[i]
TOTAL = N * len(SEEDS)

CATS = hoops.CATS
zsum = {i: {c: sum(pl["z"][c] for pl in rosters[i]) for c in CATS} for i in rosters}
ztot = {i: sum(zsum[i].values()) for i in rosters}

# ECW readout (E8 metric): expected cats won per week vs the field.
# Inlined verbatim from decw_card_v2.pwins_total (that module runs argv/state
# loading at import time and cannot be imported headless — noted defect).
import math  # noqa: E402


def pwins_total(my_model, opp_models):
    tot = 0.0
    for om in opp_models:
        for c in CATS:
            ma, va = my_model[0][c], my_model[1][c]
            mb, vb = om[0][c], om[1][c]
            d = (ma - mb) / (math.sqrt(va + vb) or 1e-9)
            p = 0.5 * (1 + math.erf(d / math.sqrt(2)))
            tot += (1 - p) if c == "TO" else p
    return tot / (len(opp_models) or 1)
models = {i: arena.team_week_model(rosters[i]) for i in rosters}
ecw = {i: pwins_total(models[i], [models[j] for j in rosters if j != i]) for i in rosters}

# Owner build under the DECLARED punt: kept-total dropping punted cats
kept_declared = {i: sum(z for c, z in zsum[i].items() if c not in DECLARED_PUNT) for i in rosters}

print(f"mock 33 — slot {OWNER}, declared punt {DECLARED_PUNT}")
print(f"seasons/seed {N}, seeds {SEEDS}, total {TOTAL}")
print("\nslot  champ%  playoff%  ECW/wk  9cat-z  kept-z(owner-punt)")
order = sorted(rosters, key=lambda x: -tot_c[x])
for i in order:
    tag = " <- OWNER" if i == OWNER else ""
    print(f"{i:>4} {100*tot_c[i]/TOTAL:7.2f} {100*tot_p[i]/TOTAL:8.2f} {ecw[i]:7.2f} {ztot[i]:+8.2f} {kept_declared[i]:+8.2f}{tag}")

print("\nowner ranks: champ", order.index(OWNER) + 1,
      "| kept-total(9cat)", sorted(rosters, key=lambda x: -ztot[x]).index(OWNER) + 1,
      "| ECW", sorted(rosters, key=lambda x: -ecw[x]).index(OWNER) + 1)
print("per-seed owner champ%:", {sd: round(100*per_seed[sd][0][OWNER]/N, 2) for sd in SEEDS})

ranks = {}
for c in CATS:
    ranked = sorted(rosters, key=lambda i: -zsum[i][c])
    ranks[c] = ranked.index(OWNER) + 1
print("\nowner per-cat rank/z:", {c: (ranks[c], round(zsum[OWNER][c], 2)) for c in CATS})

out = {
    "mock": 33, "owner_slot": OWNER, "declared_punt": DECLARED_PUNT,
    "seeds": SEEDS, "seasons_per_seed": N,
    "table": [{"slot": i, "champ_pct": round(100*tot_c[i]/TOTAL, 2),
               "playoff_pct": round(100*tot_p[i]/TOTAL, 2),
               "ecw_per_week": round(ecw[i], 3),
               "kept_total_9cat": round(ztot[i], 2),
               "kept_total_owner_punt": round(kept_declared[i], 2)} for i in sorted(rosters)],
    "owner_cat_ranks": ranks,
    "owner_cat_z": {c: round(zsum[OWNER][c], 2) for c in CATS},
    "owner_roster": [p["player"] for p in rosters[OWNER]],
}
OUT = os.path.join(REPO, "arena", "results", "season_sim_mock33_out.json")
json.dump(out, open(OUT, "w"), indent=1)
print(f"\nwrote {os.path.relpath(OUT, REPO)}")
