#!/usr/bin/env python3
"""Measure BENCH_WEIGHT from a daily-lineup fill (audit 2026-08-09, item A1).

WHY. `arena.BENCH_WEIGHT = 0.15` and the deck's `BENCH_WEIGHT` price any player
who cannot claim one of the ten daily lineup slots at 15% of production. The
owner's league sets lineups DAILY, so a "bench" player is only idle on days when
all ten slots are already claimed by teammates who also have games — which is
rare, because an NBA team plays ~3.2 games a week and a 13-man roster therefore
has only ~6 players with a game on a typical day.

WHAT THIS MEASURES. Slot-competition loss ONLY: the share of a player's OWN
games that reach the lineup, conditional on him having a game and being healthy.
Availability is deliberately excluded because `team_week_model` already applies
it separately as `g = 3.5 * weekly_availability(p)`; folding it in here would
double-count the injury haircut on exactly the last three picks.

HOW TO READ THE OUTPUT. The number that replaces BENCH_WEIGHT is the ranks-11-13
start-share RELATIVE to ranks 1-10 (printed as `relative weight`), because the
top-10 figure is the implicit denominator of a weight of 1.0 in the current
model.

    python3 arena/mocks/bench_share_fit.py [--drafts 12] [--weeks 18]

Runs in ~1-2 minutes. Reproduces the figure quoted in
arena/results/analysis_2026-08-09_self_critique_round3.md section 1a.
"""
import argparse
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
sys.path.insert(0, os.path.join(HERE, ".."))

import arena  # noqa: E402
import hoops  # noqa: E402

# 82 games over a 25.4-week season = 3.23 team-games per week. Using the real
# pace rather than the model's 3.5 matters: it is the denominator of every
# start-share below.
GAMES_PER_WEEK = 82 / 25.4
DAYS = 7


def team_week(rng):
    """Days 0-6 this player's NBA team plays. 3 or 4 games, no 3-in-3."""
    n = 3 if rng.random() < (4 - GAMES_PER_WEEK) else 4
    while True:
        days = sorted(rng.sample(range(DAYS), n))
        if not any(days[i + 2] - days[i] == 2 for i in range(len(days) - 2)):
            return days


def fill(available, order):
    """Max-cardinality assignment of today's available players to LINEUP_SLOTS.

    Greedy by roster value with an augmenting repair pass, so a star is never
    left benched by an unlucky early assignment. `available` holds indices into
    the roster; `order` ranks roster indices by value (best first).
    """
    slots = arena.LINEUP_SLOTS
    assign = {}          # slot index -> roster index
    positions = {}

    def eligible(ri, si):
        s = slots[si]
        return s is None or any(b in s for b in positions[ri])

    for ri in available:
        positions[ri] = arena.positions_of(ROSTER[ri])

    def augment(ri, seen):
        for si in range(len(slots)):
            if si in seen or not eligible(ri, si):
                continue
            seen.add(si)
            if si not in assign or augment(assign[si], seen):
                assign[si] = ri
                return True
        return False

    started = set()
    for ri in sorted(available, key=lambda i: order.index(i)):
        if augment(ri, set()):
            started.add(ri)
    return started


ROSTER = []  # module-level so fill() can read positions without re-threading


def measure(rosters, weeks, rng):
    """Return per-rank (games, starts) summed over every roster given."""
    games = [0] * arena.ROUNDS
    starts = [0] * arena.ROUNDS
    global ROSTER
    for roster in rosters:
        ROSTER = sorted(roster, key=lambda p: -sum(p["z"][c] for c in arena.CATS))
        order = list(range(len(ROSTER)))
        for _ in range(weeks):
            sched = [team_week(rng) for _ in ROSTER]
            for day in range(DAYS):
                avail = [i for i in order if day in sched[i]]
                if not avail:
                    continue
                for i in avail:
                    games[i] += 1
                for i in fill(avail, order):
                    starts[i] += 1
    return games, starts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", type=int, default=12,
                    help="independent drafts to measure (12 teams each)")
    ap.add_argument("--weeks", type=int, default=18)
    args = ap.parse_args()

    pool = arena.load_pool()
    names = list(arena.STRATEGIES)
    rosters = []
    for seed in range(args.drafts):
        rng = random.Random(seed)
        order = [names[(seed + i) % len(names)] for i in range(arena.TEAMS)]
        rosters.extend(arena.run_draft(order, pool, rng).values())

    games, starts = measure(rosters, args.weeks, random.Random(99))
    share = [starts[i] / games[i] if games[i] else 0.0
             for i in range(arena.ROUNDS)]

    print(f"{len(rosters)} rosters drafted by the system itself "
          f"({args.drafts} drafts x {arena.TEAMS} teams), {args.weeks} weeks each")
    print(f"NBA pace: {GAMES_PER_WEEK:.2f} team-games/week; "
          f"lineup: {len(arena.LINEUP_SLOTS)} daily slots, "
          f"{arena.ROUNDS} roster spots\n")
    print(" roster rank   own games   started   start-share")
    for i in range(arena.ROUNDS):
        print(f"   {i + 1:>2}        {games[i]:>9}  {starts[i]:>8}      "
              f"{share[i]:.3f}")

    top = sum(starts[:10]) / (sum(games[:10]) or 1)
    tail = sum(starts[10:]) / (sum(games[10:]) or 1)
    print(f"\n  ranks 1-10 start-share : {top:.3f}")
    print(f"  ranks 11-13 start-share: {tail:.3f}")
    print(f"  RELATIVE WEIGHT (11-13 vs 1-10): {tail / top:.3f}")
    print(f"  shipped BENCH_WEIGHT           : {arena.BENCH_WEIGHT:.3f}"
          f"   ({(tail / top) / arena.BENCH_WEIGHT:.1f}x too low)")
    print("\nNote: slot competition only. Availability is applied separately by")
    print("team_week_model as g = 3.5 * weekly_availability(p) — do not fold it")
    print("in here. Streaming (E16/N5) is excluded and would raise this further.")


if __name__ == "__main__":
    main()
