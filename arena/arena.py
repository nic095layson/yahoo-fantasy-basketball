#!/usr/bin/env python3
"""arena — self-play draft tournament for the fantasy basketball system.

ISOLATION CONTRACT: this folder tests the system; it never modifies it.
The arena imports the production engine (scripts/hoops.py) read-only, uses
its own frozen dataset (data/players_2025-10-21.csv — opening night of the
2025-26 season, no hindsight), and writes only under arena/results/.

    python3 arena/arena.py draft --seed 1        # one 12-team draft
    python3 arena/arena.py live --slot 4         # YOU + 11 AI managers:
                                                 #   bots pick into the
                                                 #   production draft state,
                                                 #   pausing at your turns
    python3 arena/arena.py tournament            # rotations x seeds x seasons
    python3 arena/arena.py slots                 # champ%% by strategy x SLOT
    python3 arena/arena.py cadence --slot 4      # what the board loses
                                                 #   between YOUR turns
    python3 arena/arena.py tournament --seasons 200 --seeds 5 --rotations 3
    python3 arena/arena.py tournament --generations 3   # fixed-seed evolution

Scoring is CHAMPIONSHIPS from Monte-Carlo H2H seasons, not draft-day value.
Statistical honesty (verified 2026-07-12): champ% differences under ~2 points
need ~10 seeds x 200 seasons to be trusted; the mid-board is noise below
that. Generations are evaluated on a FIXED seed set so mutation effects are
attributable. The built-in hill-climb is a baseline; the Fable 5 strategy
lab (Cowork phase 2) supplies reasoned evolution.
"""

import argparse
import importlib.util
import json
import math
import re
import os
import random

ARENA_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ARENA_DIR)
DATA = os.environ.get("ARENA_DATA",
                      os.path.join(ARENA_DIR, "data", "players_2025-10-21.csv"))

_spec = importlib.util.spec_from_file_location(
    "hoops", os.path.join(REPO, "scripts", "hoops.py"))
hoops = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hoops)
hoops.DATA_PATH = DATA  # arena reads its own frozen snapshot

CATS = hoops.CATS

# Real ADP for market_ranks (work order step 5, 2026-08-21): the same
# room-price map the deck injects as `const ADP`, so market_ranks agrees
# with the deck's marketRanks cross-language. Read-only load; honours the
# isolation contract (arena never writes the production system). Empty when
# the file is absent, which reproduces the pre-ADP proxy behaviour exactly.
def _load_adp():
    try:
        with open(os.path.join(REPO, "data", "market_adp.json")) as _f:
            return json.load(_f)
    except (OSError, ValueError):
        return {}

ADP = _load_adp()
BASE_POS = ("PG", "SG", "SF", "PF", "C")
TEAMS, ROUNDS = 12, 13   # 13-slot league codified 2026-07-12 (was 15; re-based 2026-07-28)
WEEKS, PLAYOFF_TEAMS = 18, 6
STARTERS = 13           # legacy cap (lineup_weights governs since 2026-07-23)
BENCH_WEIGHT = 0.15
# Per-game coefficient of variation by category: low-count stats are noisier.
CV = {"PTS": 0.30, "REB": 0.35, "AST": 0.40, "3PTM": 0.55,
      "ST": 0.70, "BLK": 0.75, "TO": 0.50}
# Slot-conditional gradient ordering (codified 2026-07-30, council 5-0):
# from draft slots 1-3 the council seat scores candidates by the marginal
# category-win-probability gradient instead of the flat z-sum. CRN-paired
# confirmation at fresh seeds: +12.67pp champ, t=4.63 (18 cells, slots
# 1-3, seeds 7/13/21/34/55/89); the global variant was inconclusive
# (t=0.64, 36 cells), so the gradient stays slot-gated.
GRAD_DEFL = {"ST": 0.580, "TO": 0.705, "FG%": 0.736, "PTS": 0.774,
             "BLK": 0.785, "3PTM": 0.790, "REB": 0.819, "AST": 0.837,
             "FT%": 0.862}
GRAD_K, GRAD_SLOTS, GRAD_SCALE = 1.0, 3, 10.0
PCT_MIX_INFL = 1.15     # shot-mix/lineup inflation over the binomial floor
# (PCT_WEEK_SD=0.012 retired 2026-07-30: it sat 2-4x under the binomial
#  floor of the sim's own attempt volumes, making % cats near-deterministic
#  — 9-CAT math audit, findings_2026-07-30. Weekly % variance is now
#  per-roster binomial x PCT_MIX_INFL, computed in team_week_model.)
TEAM_WEEK_SHOCK = 0.06  # shared games-played shock, correlates counting cats


# --------------------------------------------------------------------------
# Strategy personalities
# --------------------------------------------------------------------------
# Knobs (all optional; defaults neutral):
#   punt: cats ignored | matrix_aware: contested-category weighting (council)
#   locked_w / lost_w: weight for cats ranked top-2 / 10+ once matrix-aware
#   risk: "normal" (production availability), "safe" (avoid injury-flagged),
#         "upside" (ignore discounts) | rec_compound: council recovery rule
#   need_w: positional-need bonus | scarcity_w: dry-position response
#   stack_pen: 3rd-same-NBA-team penalty | value_exp: >1 favors stars
#   noise: gaussian pick noise (the "market" persona)

MKT_W = {"PTS": 1.6, "3PTM": 1.2, "AST": 1.0, "REB": 1.0,
         "ST": 0.7, "BLK": 0.7, "FG%": 0.5, "FT%": 0.5, "TO": 0.25}

DEFAULT = dict(punt=(), matrix_aware=False, locked_w=0.35, lost_w=0.45,
               risk="normal", rec_compound=False, need_w=0.0,
               scarcity_w=0.0, stack_pen=0.0, value_exp=1.0, noise=0.0,
               adp=False, cat_w=None)

STRATEGIES = {
    "council":     dict(matrix_aware=True, rec_compound=True, stack_pen=0.5,
                        need_w=0.3,
                        # locked/lost neutralized 2026-07-28: swing
                        # down-weighting cost -3.78pp champ causally
                        # (120 CRN-paired drafts, t=5.16; monotone
                        # cur->mid->neutral sweep). Field seats keep
                        # DEFAULT 0.35/0.45 so baselines stay comparable.
                        locked_w=1.0, lost_w=1.0),
    "bpa_pure":    dict(),
    "punt_ft":     dict(punt=("FT%",), matrix_aware=True),
    "punt_ast":    dict(punt=("AST",), matrix_aware=True),
    "punt_ft_to":  dict(punt=("FT%", "TO"), matrix_aware=True),
    "stars":       dict(value_exp=1.35),
    "slot_filler": dict(need_w=1.2),
    "scarcity":    dict(scarcity_w=1.0, need_w=0.4),
    "safe_floor":  dict(risk="safe"),
    "upside":      dict(risk="upside", value_exp=1.15),
    "specialist":  dict(matrix_aware=True, locked_w=1.4, lost_w=0.2),
    "market":      dict(adp=True, noise=4.0), # ADP-anchored ordinary league-mate
    "points_chaser": dict(cat_w=MKT_W, noise=0.4), # points-league habits in a 9-cat room
}


def load_pool():
    players = hoops.zscores(hoops.load_players())
    return [p for p in players if hoops.availability(p) > 0]


def positions_of(p):
    return [s.strip() for s in p["pos"].replace('"', "").split(",")]


def strategy_params(name, overrides=None):
    params = dict(DEFAULT)
    params.update(STRATEGIES[name])
    if overrides:
        params.update(overrides)
    return params


# Owner-league weekly lineup: 10 starters by slot + 3 bench (research-backed
# realism fix, 2026-07-23: flat top-13 let 6-center rosters bank phantom
# minutes; real layout caps startable bigs at C,C,Util,Util).
LINEUP_SLOTS = (("PG",), ("SG",), ("PG", "SG"), ("SF",), ("PF",),
                ("SF", "PF"), ("C",), ("C",), None, None)  # None = Util


def lineup_weights(roster):
    """Greedy weekly lineup: players in value order claim the first open
    eligible slot (specific before flex before Util). Returns id->weight."""
    ordered = sorted(roster, key=lambda p: -sum(p["z"][c] for c in CATS))
    open_slots = list(LINEUP_SLOTS)
    weights = {}
    for p in ordered:
        pos = positions_of(p)
        claimed = None
        for i, s in enumerate(open_slots):
            if s is not None and any(b in s for b in pos):
                claimed = i
                break
        if claimed is None:
            for i, s in enumerate(open_slots):
                if s is None:
                    claimed = i
                    break
        if claimed is not None:
            open_slots.pop(claimed)
            weights[id(p)] = 1.0
        else:
            weights[id(p)] = BENCH_WEIGHT
    return weights


# --------------------------------------------------------------------------
# DAILY-FILL start rates (instrument v2, 2026-08-05; re-landed 2026-08-13)
# --------------------------------------------------------------------------
# Yahoo lineups are set DAILY — every started game counts 100%, bench games
# count 0, and a bench player backfills any eligible open slot on his game
# days (owner-league ground truth; measured ~99.4% of a 13-man roster's
# played games start). The static weekly `lineup_weights` model above —
# 10 starters x 1.0 + 3 bench x BENCH_WEIGHT — underweighted the bench by
# ~6.5x, which is what let a mis-shaped star inflate against the card.
#
# `lineup_weights` is UNCHANGED and still used by the pick engine
# (slots_left / trial); only `team_week_model` reads the daily-fill weights.
#
# This is the Python half of the deck's `dailyFillWeights`. The two must stay
# bit-identical or `check_parity.py` fails: `df_hash` mirrors JS `dfHash`
# exactly (FNV-1a-style mix under Math.imul semantics), and the day draw,
# availability gate, candidate ordering, and slot-claim rule all mirror the
# deck one-for-one. Both are exercised by check_parity's df_hash vector
# check and by the card-ordering comparison.
DF_K = 32
DF_DAY_W = (1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4)
_U32 = 0xFFFFFFFF


def _imul(a, b):
    """JS Math.imul: 32-bit multiply. Bit patterns are kept unsigned here —
    identical to JS's signed int32 result under XOR/shift/multiply."""
    return (a * b) & _U32


def df_hash(s, k, salt):
    """Deterministic [0,1) draw keyed on (player name, trial, salt).
    Bit-identical to the deck's dfHash. Iterates UTF-16 code units so
    non-ASCII names hash the same as JS String.charCodeAt."""
    h = (2166136261 ^ _imul(k, 2654435761) ^ _imul(salt, 2246822519)) & _U32
    buf = s.encode("utf-16-le")
    for i in range(0, len(buf), 2):
        h = (h ^ (buf[i] | (buf[i + 1] << 8))) & _U32
        h = _imul(h, 16777619)
    h = (h ^ (h >> 15)) & _U32
    h = _imul(h, 2246822507)
    h = (h ^ (h >> 13)) & _U32
    h = _imul(h, 3266489909)
    h = (h ^ (h >> 16)) & _U32
    return h / 4294967296


def daily_fill_weights(roster):
    """Monte-Carlo daily-fill start rate per player: started/played across
    DF_K simulated weeks. Returns id->weight (1.0 for a player who never
    played, matching the deck's `?? 1.0`)."""
    val = {p["player"]: sum(p["z"][c] for c in CATS) for p in roster}
    started = {id(p): 0 for p in roster}
    played = {id(p): 0 for p in roster}
    for k in range(DF_K):
        by_day = [[] for _ in range(7)]
        for p in roster:
            name = p["player"]
            u = df_hash(name, k, 1)
            g = 2 if u < 0.08 else 3 if u < 0.63 else 4 if u < 0.98 else 5
            days = [0, 1, 2, 3, 4, 5, 6]
            a = weekly_availability(p)
            for j in range(g):
                u2 = df_hash(name, k, 10 + j)
                tot = 0.0
                for d in days:
                    tot += DF_DAY_W[d]
                r = u2 * tot
                acc = 0.0
                pick = days[-1]
                for d in days:
                    acc += DF_DAY_W[d]
                    if r < acc:
                        pick = d
                        break
                days.remove(pick)
                if df_hash(name, k, 20 + pick) < a:
                    played[id(p)] += 1
                    by_day[pick].append(p)
        for d in range(7):
            cands = sorted(by_day[d],
                           key=lambda p: (-val[p["player"]], p["player"]))
            open_slots = list(LINEUP_SLOTS)
            for p in cands:
                pos = positions_of(p)
                idx = -1
                for i, sl in enumerate(open_slots):
                    if sl is not None and any(b in pos for b in sl):
                        idx = i
                        break
                if idx == -1:
                    for i, sl in enumerate(open_slots):
                        if sl is None:
                            idx = i
                            break
                if idx != -1:
                    open_slots.pop(idx)
                    started[id(p)] += 1
    weights = {}
    for p in roster:
        pl = played[id(p)]
        weights[id(p)] = started[id(p)] / pl if pl else 1.0
    return weights


# Market (ADP) model — how ordinary drafters price players, per 9-cat draft
# research (2026-07-23): points-volume bias, efficiency/TO myopia, rookie
# hype (~2-round premium), name value for recovering stars (no availability
# discount at the draft table), mild star top-heaviness.
# Research-backed market pins (2026-07-23): hype the stat model can't see.
# ESPN/SI early boards take Flagg top-20 (year-2 leap premium); lottery
# rookies go rounds 3-7 on name value despite the 9-cat rookie tax.
MKT_PIN = {"Cooper Flagg": 18, "AJ Dybantsa": 30, "Darryn Peterson": 55,
           "Dylan Harper": 60, "Cameron Boozer": 70, "Caleb Wilson": 90,
           "Mikel Brown Jr.": 95}


def market_ranks(pool):
    """1-based estimated real-draft rank: real ADP leads, z-proxy fills the tail.

    Work order step 5 (2026-08-21): the market model consulted its OWN z-scores
    (~0.9 correlated with the value board by construction), so it could never
    tell the room disagreed with us. It now leads with real Hashtag consensus
    ADP (module-level ADP, injected into the deck as `const ADP`), falling back
    to the z-derived proxy only for players the feed does not cover. Mirrors the
    deck's marketRanks exactly (locked by scripts/check_parity.py). Empty ADP
    reproduces the pre-ADP proxy output verbatim.
    """
    def mscore(p):
        s = sum(p["z"][c] * MKT_W[c] for c in CATS)
        note = (p.get("note") or "").lower()
        # Sign-aware multipliers (codified 2026-07-30): a plain product
        # inverted in the negative tail — rookie hype LOWERED
        # negative-score rookies, the risk discount RAISED negative
        # vets. Division mirrors the intent below zero.
        if "rookie-proj" in note:
            s = s * 1.15 if s > 0 else s / 1.15
        if "risk" in hoops.note_tag(note):  # leading tag only (R4-F23)
            s = s * 0.95 if s > 0 else s / 0.95
        return s
    # proxy fallback (unchanged z-model + MKT_PIN)
    ordered = sorted(pool, key=lambda p: -mscore(p))
    model = {p["player"]: i + 1 for i, p in enumerate(ordered)}
    eff = {n: min(r, MKT_PIN.get(n, r)) for n, r in model.items()}
    proxy_ranked = sorted(model, key=lambda n: (eff[n], model[n]))
    proxy_rank = {n: i + 1 for i, n in enumerate(proxy_ranked)}
    # ADP-primary: real room price leads; the proxy tail follows. Real ADP
    # overrides MKT_PIN (measured price beats a hand pin). Ties broken by proxy
    # rank so the ordering is identical to the deck's marketRanks.
    adp_players = sorted((p["player"] for p in pool if p["player"] in ADP),
                         key=lambda n: (ADP[n], proxy_rank[n]))
    rest = [n for n in proxy_ranked if n not in ADP]
    final = adp_players + rest
    return {n: i + 1 for i, n in enumerate(final)}


def pick_for(params, pool, roster, my_ranks, rnd, rng, mkt=None):
    """Score every available player under this strategy's knobs; take max."""
    remaining = ROUNDS - len(roster)
    unfilled = [b for b in BASE_POS
                if not any(b in positions_of(p) for p in roster)]
    must_fill = len(unfilled) >= remaining  # hard feasibility guard
    team_ct, rec_ct = {}, 0
    for p in roster:
        team_ct[p["team"]] = team_ct.get(p["team"], 0) + 1
        if "recovery" in hoops.note_tag(p.get("note")):  # R4-F23
            rec_ct += 1
    scarce = {}
    if params["scarcity_w"]:
        top = sorted(pool, key=lambda p: -hoops.adj_value(p))[:100]
        for b in BASE_POS:
            scarce[b] = sum(1 for p in top if b in positions_of(p))

    def weight(cat):
        if params.get("cat_w"):
            return params["cat_w"].get(cat, 1.0)
        if cat in params["punt"]:
            return 0.0
        if params["matrix_aware"] and my_ranks and len(roster) >= 2:
            r = my_ranks[cat]
            if r <= 2:
                return params["locked_w"]
            if r >= 10:
                return params["lost_w"]
        return 1.0

    slots_left = lineup_weights(roster)  # who starts today
    n_started = sum(1 for w in slots_left.values() if w == 1.0)

    def bench_bound(p):
        """Would this candidate crack the starting lineup right now?"""
        if n_started < len(LINEUP_SLOTS):
            trial = lineup_weights(roster + [p])
            return trial.get(id(p), BENCH_WEIGHT) < 1.0
        return False  # lineup full: every candidate is depth, no distortion

    def score(p):
        if params.get("adp") and mkt is not None:
            s = -mkt.get(p["player"], 300)
            if bench_bound(p):
                s -= 50.0  # ordinary drafters don't hoard unplayable positions
            if unfilled and rnd >= 6 and any(b in positions_of(p)
                                             for b in unfilled):
                s += 15.0  # "I still need a center" instinct in the mid-rounds
            if params["noise"]:
                s += rng.gauss(0, params["noise"])
            return s
        if params.get("grad_k"):
            gk = params["grad_k"]
            rr = len(roster)
            s = 0.0
            for c in CATS:
                w = weight(c)
                if not w:
                    continue
                S = sum(q["z"][c] for q in roster)
                sig = gk * math.sqrt(rr + 1) / GRAD_DEFL[c]
                s += w * (0.5 * (1 + math.erf((S + p["z"][c]) / (sig * math.sqrt(2))))
                          - 0.5 * (1 + math.erf(S / (sig * math.sqrt(2)))))
            s *= GRAD_SCALE
        else:
            s = sum(p["z"][c] * weight(c) for c in CATS)
        note = (p.get("note") or "").lower()
        injury_note = "inj" in note or note.startswith("out-")
        if params["risk"] != "upside":
            av = hoops.availability(p)
            if params["rec_compound"] and "recovery" in hoops.note_tag(note):
                av *= 0.85 if rec_ct == 1 else (0.7 if rec_ct >= 2 else 1.0)
            s = s * av if s > 0 else s
        if params["value_exp"] != 1.0:
            s = math.copysign(abs(s) ** params["value_exp"], s)
        if params["need_w"] and unfilled:
            fills = sum(1 for b in unfilled if b in positions_of(p))
            s += params["need_w"] * fills * (0.5 + rnd / ROUNDS)
        if params["scarcity_w"]:
            for b in positions_of(p):
                if scarce.get(b, 99) <= 8:
                    s += params["scarcity_w"] * (9 - scarce[b]) / 8
        if params["stack_pen"] and team_ct.get(p["team"], 0) >= 2:
            s -= params["stack_pen"]
        if params["noise"]:
            s += rng.gauss(0, params["noise"])
        if params["risk"] == "safe" and injury_note:
            s -= 100.0  # avoid, but preserve ordering when forced
        if s > 0 and bench_bound(p):
            s *= BENCH_WEIGHT  # a bench-bound pick is worth bench minutes
        return s

    cands = pool
    if must_fill:
        filtered = [p for p in pool
                    if any(b in positions_of(p) for b in unfilled)]
        cands = filtered or pool
    return max(cands, key=score)


def ranks_for(rosters, me):
    totals = {i: {c: sum(p["z"][c] for p in r) for c in CATS}
              for i, r in rosters.items()}
    mine = totals[me]
    return {c: 1 + sum(1 for i, t in totals.items()
                       if i != me and t[c] > mine[c]) for c in CATS}


def run_draft(order, pool_master, rng, param_overrides=None):
    pool = list(pool_master)
    mkt = market_ranks(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    for n in range(TEAMS * ROUNDS):
        slot = hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        params = strategy_params(name, (param_overrides or {}).get(name))
        if name == "council" and slot <= GRAD_SLOTS and "grad_k" not in params:
            params = {**params, "grad_k": GRAD_K}
        ranks = (ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = pick_for(params, pool, rosters[slot], ranks, n // TEAMS + 1, rng,
                     mkt=mkt)
        rosters[slot].append(p)
        pool.remove(p)
    return rosters


# --------------------------------------------------------------------------
# Season Monte Carlo — weekly H2H categories, fixed top-6 bracket
# --------------------------------------------------------------------------

def weekly_availability(p):
    # Leading tag only, risk before recovery (audit 2026-08-09, F16 — mirrors
    # hoops.availability). Substring-matching the whole note made
    # "inj-achilles-risk (recovery on track)" score as a 0.60 recovery tier.
    tag = hoops.note_tag(p.get("note"))
    if tag.endswith("-recovery"):
        return 0.60
    if tag.endswith("-risk") or tag in ("risk", "inj-risk"):
        return 0.75
    if "recovery" in tag:
        return 0.60
    if "risk" in tag:
        return 0.75
    return 0.88


def team_week_model(roster):
    """Per-category weekly (mu, var). Each player's contribution is scaled by
    his DAILY-FILL start rate (started/played across DF_K simulated weeks),
    which replaced the static 10-starters + 3-bench weighting on 2026-08-05
    (re-landed with its deck half 2026-08-13). Counting-stat variance = compound-sum
    E[G]*Var[X] + Var[G]*E[X]^2 with category-specific per-game CV and
    availability-tier game-count variance Var[G] = 3.5*a*(1-a)."""
    mu = {c: 0.0 for c in CATS}
    var = {c: 0.0 for c in CATS}
    lw = daily_fill_weights(roster)
    fg_mk = fg_at = ft_mk = ft_at = 0.0
    for p in roster:
        w = lw.get(id(p), 1.0)
        a = weekly_availability(p)
        g = 3.5 * a
        g_var = 3.5 * a * (1 - a)
        for c, col in hoops.COUNT_COLS.items():
            x = p[col]
            mu[c] += w * x * g
            var[c] += w * ((x * CV[c]) ** 2 * g + x ** 2 * g_var)
        fg_mk += w * p["fg_pct"] * p["fga"] * g
        fg_at += w * p["fga"] * g
        ft_mk += w * p["ft_pct"] * p["fta"] * g
        ft_at += w * p["fta"] * g
    # Weekly % variance: per-roster binomial floor x mix inflation
    # (codified 2026-07-30; replaces the flat PCT_WEEK_SD=0.012 that
    #  made the better team win FT% in 99.4% of weeks).
    p_fg = fg_mk / (fg_at or 1)
    p_ft = ft_mk / (ft_at or 1)
    mu["FG%"] = p_fg
    var["FG%"] = (PCT_MIX_INFL ** 2) * max(p_fg * (1 - p_fg), 1e-4) / (fg_at or 1)
    mu["FT%"] = p_ft
    var["FT%"] = (PCT_MIX_INFL ** 2) * max(p_ft * (1 - p_ft), 1e-4) / (ft_at or 1)
    return mu, var


def simulate_seasons(rosters, seasons, rng):
    models = {i: team_week_model(r) for i, r in rosters.items()}
    sigmas = {i: {c: math.sqrt(models[i][1][c]) or 1e-6 for c in CATS}
              for i in rosters}
    champs = {i: 0 for i in rosters}
    playoffs = {i: 0 for i in rosters}
    counting = set(hoops.COUNT_COLS)

    def week_result(a, b):
        # shared games-played shock correlates a team's counting cats
        sh_a = rng.gauss(1.0, TEAM_WEEK_SHOCK)
        sh_b = rng.gauss(1.0, TEAM_WEEK_SHOCK)
        wins = 0
        for c in CATS:
            ma = models[a][0][c] * (sh_a if c in counting else 1.0)
            mb = models[b][0][c] * (sh_b if c in counting else 1.0)
            sa = rng.gauss(ma, sigmas[a][c])
            sb = rng.gauss(mb, sigmas[b][c])
            better = sa < sb if c == "TO" else sa > sb
            wins += 1 if better else 0
        return wins  # cats won by a, 0..9 (continuous draws: no ties)

    ids = list(rosters)
    for _ in range(seasons):
        record = {i: 0 for i in ids}
        for _w in range(WEEKS):
            pairing = ids[:]
            rng.shuffle(pairing)
            for k in range(0, TEAMS, 2):
                a, b = pairing[k], pairing[k + 1]
                # Yahoo H2H-each-cat standings accumulate the CATEGORY
                # record, not weekly binary wins (codified 2026-07-30;
                # the weekly-binary rule shifted playoff% by up to
                # +-29pp on identical rosters — 9-CAT math audit).
                wa = week_result(a, b)
                record[a] += wa
                record[b] += 9 - wa
        seeds = sorted(ids, key=lambda i: (-record[i], rng.random()))
        top = seeds[:PLAYOFF_TEAMS]
        for i in top:
            playoffs[i] += 1
        # seeds 1-2 byes; 3v6, 4v5; FIXED bracket (Yahoo default, no reseed)
        qf = [(top[2], top[5]), (top[3], top[4])]
        w1 = [a if week_result(a, b) >= 5 else b for a, b in qf]
        sf = [(top[0], w1[1]), (top[1], w1[0])]
        w2 = [a if week_result(a, b) >= 5 else b for a, b in sf]
        champs[w2[0] if week_result(*w2) >= 5 else w2[1]] += 1
    return champs, playoffs


# --------------------------------------------------------------------------
# Tournament: rotations x slots x seeds
# --------------------------------------------------------------------------

def tournament(seasons, seed, rotations=1, param_overrides=None, names=None):
    """One seed's tournament. Each rotation round shuffles the strategy
    order (varying draft-slot adjacency), then cycles it through all 12
    slots so every strategy sees every slot exactly once per round."""
    rng = random.Random(seed)
    pool = load_pool()
    names = names or list(STRATEGIES)
    total_c = {n: 0 for n in names}
    total_p = {n: 0 for n in names}
    seated = {n: 0 for n in names}
    for rr in range(rotations):
        base = names[:]
        if rr:
            rng.shuffle(base)
        for rotation in range(TEAMS):
            order = base[rotation:] + base[:rotation]
            rosters = run_draft(order, pool, rng, param_overrides)
            champs, plays = simulate_seasons(rosters, seasons, rng)
            # only the first TEAMS names are seated; with more strategies
            # than seats, extras sit this draft out (crash fix 2026-07-28:
            # adding the 13th personality made enumerate(order) walk past
            # slot 12 -> KeyError, breaking stock tournament/slots/cadence)
            for slot, name in enumerate(order[:TEAMS], 1):
                total_c[name] += champs[slot]
                total_p[name] += plays[slot]
                seated[name] += 1
    return {n: {"champ_pct": 100 * total_c[n] / (seasons * seated[n]),
                "playoff_pct": 100 * total_p[n] / (seasons * seated[n]),
                "drafts_seated": seated[n]} for n in names if seated[n]}


def evaluate(seasons, seeds, rotations, param_overrides=None):
    """Aggregate over a FIXED seed list; returns mean and cross-seed spread."""
    names = list(STRATEGIES)
    per_seed = {n: [] for n in names}
    for s in seeds:
        res = tournament(seasons, s, rotations, param_overrides)
        for n in names:
            per_seed[n].append(res[n]["champ_pct"])
    out = {}
    for n in names:
        vals = per_seed[n]
        out[n] = {"champ_pct": sum(vals) / len(vals),
                  "spread": max(vals) - min(vals)}
    return out


def cmd_live(args):
    """Practice mode: 11 arena personalities + one human seat. Bots log
    their picks into the PRODUCTION draft state (draft_state.json), so the
    normal `draft turn` card / suggestions flow works unchanged at the
    user's turns. Re-run after each user pick to advance the bots."""
    state_path = os.environ.get("HOOPS_DRAFT_STATE", "draft_state.json")
    rng = random.Random(args.seed)
    names = [n for n in STRATEGIES if n != "council"]
    rng.shuffle(names)
    if not os.path.isfile(state_path):
        opp_slots = [s for s in range(1, TEAMS + 1) if s != args.slot]
        state = {"teams": TEAMS, "slot": args.slot, "size": ROUNDS,
                 "punt": [], "picks": [],
                 # one personality per opponent seat, no duplicates
                 "arena_managers": {str(s): names[i]
                                    for i, s in enumerate(opp_slots)}}
        json.dump(state, open(state_path, "w"), indent=2)
        print(f"live draft created: you are slot {args.slot}; opponents: "
              + ", ".join(f"T{s}={n}" for s, n in
                          sorted(state["arena_managers"].items(),
                                 key=lambda kv: int(kv[0]))))
    else:
        state = json.load(open(state_path))
        if "arena_managers" not in state:
            raise SystemExit(f"{state_path} exists but is not an arena live "
                             "draft — remove it or set HOOPS_DRAFT_STATE.")
    managers = state["arena_managers"]
    user_slot = state["slot"]
    pool_all = load_pool()
    # cross-pool guard: bots draft from the frozen snapshot but the user's
    # cards price from the live CSV — a snapshot name missing there would
    # silently skew roster totals in the production draft state.
    live_csv = os.path.join(REPO, "data", "players.csv")
    if os.path.isfile(live_csv):
        import csv as _csv
        with open(live_csv, newline="") as fh:
            live_names = {row["player"] for row in _csv.DictReader(fh)}
        missing = sorted(p["player"] for p in pool_all
                         if p["player"] not in live_names)
        if missing:
            print(f"⚠ cross-pool: {len(missing)} snapshot player(s) absent "
                  f"from live data/players.csv — cards will show them as "
                  f"UNKNOWN: {', '.join(missing[:8])}"
                  + (" …" if len(missing) > 8 else ""))
    taken = {p["player"] for p in state["picks"]}
    pool = [p for p in pool_all if p["player"] not in taken]
    by_name = {p["player"]: p for p in pool_all}
    mkt = market_ranks(pool_all)   # audit F11/A15: the ADP seat was inert here
    while len(state["picks"]) < TEAMS * ROUNDS:
        n = len(state["picks"])
        slot = hoops.team_of_pick(n, TEAMS)
        if slot == user_slot:
            print(f"⏸  pick #{n + 1} is YOURS — get the card with: "
                  f"python3 scripts/hoops.py draft turn \"\" "
                  f"then log with draft turn \"my:Name\"; re-run live after.")
            break
        name = managers[str(slot)]
        params = strategy_params(name)
        rosters = {i: [] for i in range(1, TEAMS + 1)}
        for pk in state["picks"]:
            pl = by_name.get(pk["player"])
            if pl:
                rosters[pk["slot"]].append(pl)
        ranks = (ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = pick_for(params, pool, rosters[slot], ranks, n // TEAMS + 1, rng,
                     mkt=mkt)
        state["picks"].append({"player": p["player"], "slot": slot})
        pool.remove(p)
        print(f"  ✓ #{n + 1} R{n // TEAMS + 1}: {p['player']} → "
              f"T{slot} ({name})")
    else:
        print("🏁 draft complete — analyze with scripts/hoops.py draft "
              "matrix / status / vs.")
    json.dump(state, open(state_path, "w"), indent=2)


def run_draft_ordered(order, pool_master, rng, param_overrides=None):
    """run_draft + the pick sequence in draft order (for cadence analysis)."""
    pool = list(pool_master)
    # Audit 2026-08-09 (F11/A15): this and cmd_live omitted mkt, so pick_for's
    # ADP branch (gated on `mkt is not None`) never fired. The `market` persona
    # — the only adp=True strategy, i.e. the room's ordinary league-mate —
    # silently degraded to sum(z) + gauss(0, 4.0), skipping the -50 bench-bound
    # penalty and the +15 mid-round positional instinct. Practice drafts and
    # the committed cadence_intel.json therefore contained ZERO ADP drafters.
    mkt = market_ranks(pool_master)
    rosters = {i: [] for i in range(1, TEAMS + 1)}
    sequence = []
    for n in range(TEAMS * ROUNDS):
        slot = hoops.team_of_pick(n, TEAMS)
        name = order[slot - 1]
        params = strategy_params(name, (param_overrides or {}).get(name))
        if name == "council" and slot <= GRAD_SLOTS and "grad_k" not in params:
            params = {**params, "grad_k": GRAD_K}
        ranks = (ranks_for(rosters, slot)
                 if params["matrix_aware"] and rosters[slot] else None)
        p = pick_for(params, pool, rosters[slot], ranks, n // TEAMS + 1, rng,
                     mkt=mkt)
        rosters[slot].append(p)
        sequence.append((slot, p))
        pool.remove(p)
    return rosters, sequence


TIERS = ((1, 12), (13, 24), (25, 50), (51, 100))


def cmd_cadence(args):
    """Across many drafts, measure what disappears from the board between a
    slot's consecutive turns: tier drain and position drain per gap. This is
    draft-night intelligence — 'from slot 4, between your round-1 and
    round-2 picks, expect ~N top-24 players and ~M centers to vanish'."""
    rng = random.Random(args.seed)
    pool = load_pool()
    ranked = sorted(pool, key=lambda p: -hoops.adj_value(p))
    rank_of = {p["player"]: i + 1 for i, p in enumerate(ranked)}
    slots = [args.slot] if args.slot else list(range(1, TEAMS + 1))
    # gaps[slot][k] = players taken between the slot's pick k and pick k+1
    acc = {s: [{"tiers": [0.0] * len(TIERS), "pos": {b: 0.0 for b in BASE_POS},
                "n": 0.0}
               for _ in range(ROUNDS - 1)] for s in slots}
    for d in range(args.drafts):
        names = list(STRATEGIES)
        rng.shuffle(names)
        _, seq = run_draft_ordered(names, pool, rng)
        for s in slots:
            turns = [i for i, (slot, _) in enumerate(seq) if slot == s]
            for k in range(len(turns) - 1):
                between = seq[turns[k] + 1: turns[k + 1]]
                g = acc[s][k]
                g["n"] += 1
                for _, p in between:
                    r = rank_of[p["player"]]
                    for ti, (lo, hi) in enumerate(TIERS):
                        if lo <= r <= hi:
                            g["tiers"][ti] += 1
                    for b in positions_of(p):
                        g["pos"][b] += 1
    report = {}
    for s in slots:
        rows = []
        for k, g in enumerate(acc[s]):
            n = g["n"] or 1
            rows.append({
                "between_rounds": f"{k + 1}->{k + 2}",
                "picks_between": (TEAMS - 1) * 2 - 1
                if False else len_between(s, k),
                "tier_drain": {f"top{hi}" if lo == 1 else f"{lo}-{hi}":
                               round(g["tiers"][ti] / n, 2)
                               for ti, (lo, hi) in enumerate(TIERS)},
                "pos_drain": {b: round(v / n, 2)
                              for b, v in g["pos"].items()},
            })
        report[s] = rows
        print(f"\nSLOT {s} cadence ({args.drafts} drafts):")
        for row in rows[:6]:
            td = row["tier_drain"]
            pd = row["pos_dr" "ain"]
            print(f"  R{row['between_rounds']:<6} ({row['picks_between']:>2} "
                  f"picks pass) | top12: {td['top12']:.1f}  13-24: "
                  f"{td['13-24']:.1f}  25-50: {td['25-50']:.1f} | " +
                  " ".join(f"{b}:{pd[b]:.1f}" for b in BASE_POS))
        if len(rows) > 6:
            print(f"  ... rounds 7-15 in the JSON report")
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "cadence_intel.json")
    with open(path, "w") as f:
        json.dump({"drafts": args.drafts, "seed": args.seed,
                   "slots": {str(s): report[s] for s in slots}}, f, indent=2)
    print(f"\ncadence intel written: {path}")


def len_between(slot, k):
    """Picks made by others between a slot's pick k+1 and pick k+2 (snake)."""
    n = 0
    my = [i for i in range(TEAMS * ROUNDS)
          if hoops.team_of_pick(i, TEAMS) == slot]
    return my[k + 1] - my[k] - 1


def cmd_slots(args):
    """Championship%% per (strategy, slot): which builds win from which seat."""
    rng = random.Random(args.seed)
    pool = load_pool()
    names = list(STRATEGIES)
    cell_c = {n: {s: 0 for s in range(1, TEAMS + 1)} for n in names}
    cell_n = {n: {s: 0 for s in range(1, TEAMS + 1)} for n in names}
    for rr in range(args.rotations):
        base = names[:]
        if rr:
            rng.shuffle(base)
        for rotation in range(TEAMS):
            order = base[rotation:] + base[:rotation]
            rosters = run_draft(order, pool, rng)
            champs, _ = simulate_seasons(rosters, args.seasons, rng)
            # 13 personalities, 12 seats: only the seated prefix scores
            # (same fix as tournament(), gauntlet 2026-07-28)
            for slot, name in enumerate(order[:TEAMS], 1):
                cell_c[name][slot] += champs[slot]
                cell_n[name][slot] += args.seasons
    print(f"\nchamp% by strategy x slot ({args.rotations} rotations x "
          f"{args.seasons} seasons; ~{args.rotations} samples/cell — "
          "directional, not gospel):\n")
    print("STRATEGY      " + "".join(f"  S{s:<4}" for s in range(1, 13)))
    for n in names:
        row = "".join(f"  {100 * cell_c[n][s] / (cell_n[n][s] or 1):5.1f}"
                      for s in range(1, 13))
        print(f"{n:<12}{row}")
    best = {}
    for s in range(1, 13):
        best[s] = max(names,
                      key=lambda n: cell_c[n][s] / (cell_n[n][s] or 1))
    print("\nbest strategy per slot: " +
          "  ".join(f"S{s}:{best[s]}" for s in range(1, 13)))
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "slot_intel.json")
    with open(path, "w") as f:
        json.dump({"champ_pct": {n: {str(s):
                   100 * cell_c[n][s] / (cell_n[n][s] or 1)
                   for s in range(1, 13)} for n in names},
                   "best_per_slot": {str(s): best[s] for s in best}},
                  f, indent=2)
    print(f"slot intel written: {path}")


def main():
    ap = argparse.ArgumentParser(prog="arena.py", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft", help="run one 12-team draft, print rosters")
    d.add_argument("--seed", type=int, default=1)
    lv = sub.add_parser("live", help="practice: you + 11 AI managers, "
                        "production suggestion flow at your turns")
    lv.add_argument("--slot", type=int, default=4)
    lv.add_argument("--seed", type=int, default=1)
    cd = sub.add_parser("cadence", help="board drain between a slot's turns")
    cd.add_argument("--slot", type=int, help="one slot (default: all 12)")
    cd.add_argument("--drafts", type=int, default=60)
    cd.add_argument("--seed", type=int, default=1)
    cd.add_argument("--out", default=os.path.join(ARENA_DIR, "results"))
    sl = sub.add_parser("slots", help="champ%% by strategy x draft slot")
    sl.add_argument("--seasons", type=int, default=200)
    sl.add_argument("--rotations", type=int, default=5)
    sl.add_argument("--seed", type=int, default=1)
    sl.add_argument("--out", default=os.path.join(ARENA_DIR, "results"))
    t = sub.add_parser("tournament", help="rotations x seeds x seasons")
    t.add_argument("--seasons", type=int, default=200)
    t.add_argument("--seeds", type=int, default=3,
                   help="number of seeds averaged (fixed list from --seed)")
    t.add_argument("--rotations", type=int, default=3,
                   help="shuffled rotation rounds per seed (12 drafts each)")
    t.add_argument("--seed", type=int, default=1)
    t.add_argument("--generations", type=int, default=1)
    t.add_argument("--out", default=os.path.join(ARENA_DIR, "results"))
    args = ap.parse_args()

    if args.cmd == "live":
        cmd_live(args)
        return
    if args.cmd == "cadence":
        cmd_cadence(args)
        return
    if args.cmd == "slots":
        cmd_slots(args)
        return
    if args.cmd == "draft":
        rng = random.Random(args.seed)
        rosters = run_draft(list(STRATEGIES), load_pool(), rng)
        for slot, name in enumerate(STRATEGIES, 1):
            print(f"T{slot:<2} {name:<12} " +
                  ", ".join(p["player"] for p in rosters[slot][:7]) + " ...")
        return

    seed_list = [args.seed + 97 * k for k in range(args.seeds)]  # FIXED set
    overrides, history = {}, []
    for gen in range(args.generations):
        results = evaluate(args.seasons, seed_list, args.rotations, overrides)
        board = sorted(results.items(), key=lambda kv: -kv[1]["champ_pct"])
        n_seasons = args.seasons * TEAMS * args.rotations * args.seeds
        print(f"\n=== GENERATION {gen} — {n_seasons} seasons/strategy, "
              f"seeds {seed_list}, {args.rotations} rotations ===")
        for name, r in board:
            mark = " *mutated" if overrides.get(name) else ""
            print(f"  {name:<12} champ {r['champ_pct']:5.2f}%  "
                  f"(±{r['spread']:.2f} across seeds){mark}")
        history.append({"generation": gen, "results": results,
                        "overrides": dict(overrides)})
        if gen + 1 < args.generations:
            # baseline hill-climb on the SAME fixed seeds (attributable)
            rng = random.Random(args.seed * 100 + gen)
            tops = [n for n, _ in board[:3]]
            bottoms = [n for n, _ in board[-3:]]
            for loser, winner in zip(bottoms, tops):
                base = strategy_params(winner, overrides.get(winner))
                mut = dict(base)
                for k in ("locked_w", "lost_w", "need_w", "scarcity_w",
                          "stack_pen", "value_exp", "noise"):
                    mut[k] = round(max(0.0, base[k] + rng.gauss(0, 0.15)), 3)
                overrides[loser] = mut
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, f"tournament_seed{args.seed}.json")
    with open(path, "w") as f:
        json.dump(history, f, indent=2)
    print(f"\nresults written: {path}")


if __name__ == "__main__":
    main()
