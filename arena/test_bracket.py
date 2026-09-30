#!/usr/bin/env python3
"""Playoff-bracket tests for arena.simulate_seasons (E14, shipped 2026-09-30).

The owner's league sends 8 of 12 teams to a fixed, no-bye bracket
(1v8, 4v5, 2v7, 3v6; winners meet in seed order; one week per round).
The arena shipped a six-team bracket with byes for seeds 1-2 from 2026-07
until this test went red on 2026-09-30 (league_intel_2025-26.md §1/§4/§7).

Run:  python3 arena/test_bracket.py
"""
import json
import os
import random
import sys
import unittest

DECK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(DECK)
for p in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena")):
    if p not in sys.path:
        sys.path.insert(0, p)

import hoops  # noqa: E402
import arena  # noqa: E402


def rosters_from_state(path):
    players = hoops.zscores(hoops.load_players())
    by = {p["player"]: p for p in players}
    st = json.load(open(path, encoding="utf-8"))
    ros = {s: [] for s in range(1, st["teams"] + 1)}
    for pk in st["picks"]:
        if pk["player"] in by:
            ros[pk["slot"]].append(by[pk["player"]])
    return ros


class BracketShape(unittest.TestCase):
    """Pure-bracket checks: the function takes the top seeds in order and a
    week_result(a, b) -> categories won by a."""

    def test_constant_is_eight(self):
        self.assertEqual(arena.PLAYOFF_TEAMS, 8)

    def test_seed_eight_can_win_when_the_higher_seed_number_always_wins(self):
        # week_result returns cats won by a (>= 5 advances a); under the old
        # 6-team bracket the same rule crowns seed 6, because 7 and 8 never play
        champ = arena.playoff_champion(list(range(1, 9)), lambda a, b: 9 if a > b else 0)
        self.assertEqual(champ, 8)

    def test_seed_one_wins_when_the_lower_seed_number_always_wins(self):
        champ = arena.playoff_champion(list(range(1, 9)), lambda a, b: 9 if a < b else 0)
        self.assertEqual(champ, 1)

    def test_no_byes_every_seed_plays_round_one(self):
        played = []

        def spy(a, b):
            played.append((a, b))
            return 9
        arena.playoff_champion(list(range(1, 9)), spy)
        first_round = played[:4]
        self.assertEqual(sorted(x for pair in first_round for x in pair), list(range(1, 9)))
        self.assertEqual(first_round, [(1, 8), (4, 5), (2, 7), (3, 6)])
        self.assertEqual(len(played), 7)  # 4 QF + 2 SF + 1 final


class SeasonIntegration(unittest.TestCase):
    def test_eight_playoff_credits_per_season(self):
        ros = rosters_from_state("arena/data/states/draft_state_57.json")
        seasons = 25
        champs, playoffs = arena.simulate_seasons(ros, seasons, random.Random(1))
        self.assertEqual(sum(playoffs.values()), 8 * seasons)
        self.assertEqual(sum(champs.values()), seasons)


if __name__ == "__main__":
    unittest.main(verbosity=2)
