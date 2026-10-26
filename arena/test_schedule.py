#!/usr/bin/env python3
"""Red-first tests for arena/mocks/league_sim.py --schedule with every team's pairings and the weeks already final
(kit owner 2026-10-26, "full pairings + results so far"). Before this the simulator honoured only the owner's seat's
opponent and paired the other ten at random, and every simulated season started 0-0.

Run:  python3 arena/test_schedule.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATE = os.path.join(DECK, "arena", "data", "states", "draft_state_100.json")
SIM = os.path.join(DECK, "arena", "mocks", "league_sim.py")
WEEKS = 17


def round_robin():
    """A fixed 12-team schedule: week w pairs seat i with the seat the circle method gives; every seat once a week."""
    ids = list(range(1, 13)); out = {}
    for w in range(1, WEEKS + 1):
        r = [ids[0]] + ids[1:][(w - 1) % 11:] + ids[1:][:(w - 1) % 11]
        out[str(w)] = [[r[k], r[11 - k]] for k in range(6)]
    return out


def schedule(pairings=None, played=None):
    s = dict(owner_seat=10, regular_season_weeks=WEEKS, playoff_weeks=[18, 19, 20],
             owner_opponents=[dict(week=w, seat=next(b if a == 10 else a for a, b in pairings[str(w)] if 10 in (a, b)))
                              for w in range(1, WEEKS + 1)] if pairings else [])
    if pairings: s["pairings"] = pairings
    if played: s["played"] = played
    return s


def run(sched, seasons=200, seed=7):
    d = tempfile.mkdtemp(); sp = os.path.join(d, "sched.json"); out = os.path.join(d, "out.json")
    json.dump(sched, open(sp, "w"))
    p = subprocess.run([sys.executable, SIM, STATE, "v69", str(seasons), str(seed), out, "--schedule", sp, "--season-cv"],
                       capture_output=True, text=True, cwd=DECK)
    assert p.returncode == 0, p.stderr[-1200:]
    return json.load(open(out))


class Pairings(unittest.TestCase):
    def test_every_weeks_pairing_comes_from_the_file_and_the_record_says_so(self):
        rec = run(schedule(round_robin()), seasons=50)
        self.assertEqual(rec["schedule"]["honored"], 50 * WEEKS)
        self.assertEqual(rec["schedule"]["pairings"], "every team's pairing from the file, all 17 weeks")
        self.assertEqual(rec["schedule"]["weeks_played"], 0)

    def test_the_owner_only_schedule_still_runs_as_before(self):
        pr = round_robin()
        s = schedule(pr); del s["pairings"]
        rec = run(s, seasons=20)
        self.assertEqual(rec["schedule"]["others"], "the other ten teams paired at random each week")


class Played(unittest.TestCase):
    def test_a_fully_played_season_reproduces_the_recorded_standings_exactly(self):
        # every regular-season week final: the record is deterministic, so cat_record_mean equals the recorded wins
        # (+ half a tie) and the seeds follow that order; only the playoffs are simulated
        pr = round_robin(); played = {}
        for w in range(1, WEEKS + 1):
            played[str(w)] = {}
            for a, b in pr[str(w)]:
                wa = (a * 7 + w) % 10          # 0..9 wins for a, a hand rule, no ties
                played[str(w)][str(a)] = [wa, 9 - wa, 0]; played[str(w)][str(b)] = [9 - wa, wa, 0]
        rec = run(schedule(pr, played), seasons=30)
        totals = {s: sum(played[str(w)][str(s)][0] for w in range(1, WEEKS + 1)) for s in range(1, 13)}
        for s in range(1, 13):
            self.assertAlmostEqual(rec["teams"][str(s)]["cat_record_mean"], totals[s], places=9)
            self.assertAlmostEqual(rec["teams"][str(s)]["cat_record_sd"], 0.0, places=9)
        self.assertEqual(rec["schedule"]["weeks_played"], WEEKS)
        best = max(totals, key=totals.get)
        if list(totals.values()).count(totals[best]) == 1:
            self.assertAlmostEqual(rec["teams"][str(best)]["seed_pct"][0], 100.0)

    def test_a_played_week_counts_once_and_the_rest_are_simulated(self):
        pr = round_robin()
        played = {"1": {}}
        for a, b in pr["1"]:
            played["1"][str(a)] = [9, 0, 0]; played["1"][str(b)] = [0, 9, 0]
        rec = run(schedule(pr, played), seasons=40)
        self.assertEqual(rec["schedule"]["weeks_played"], 1)
        self.assertEqual(rec["schedule"]["honored"], 40 * (WEEKS - 1))
        a0 = pr["1"][0][0]
        self.assertGreaterEqual(rec["teams"][str(a0)]["cat_record_mean"], 9.0)   # the recorded 9 are in every season
        self.assertLessEqual(rec["teams"][str(a0)]["cat_record_mean"], 9.0 + 9 * (WEEKS - 1))

    def test_a_tie_counts_half_a_win_in_the_record(self):
        # every week final and every matchup 4-4-1: the record is 17 x 4.5 for everyone, deterministic
        pr = round_robin(); played = {str(w): {str(s): [4, 4, 1] for s in range(1, 13)} for w in range(1, WEEKS + 1)}
        rec = run(schedule(pr, played), seasons=10, seed=3)
        for s in range(1, 13):
            self.assertAlmostEqual(rec["teams"][str(s)]["cat_record_mean"], 4.5 * WEEKS, places=9)
            self.assertAlmostEqual(rec["teams"][str(s)]["cat_record_sd"], 0.0, places=9)

    def test_a_played_week_whose_seats_are_incomplete_halts(self):
        pr = round_robin()
        d = tempfile.mkdtemp(); sp = os.path.join(d, "sched.json"); out = os.path.join(d, "out.json")
        json.dump(schedule(pr, {"1": {"1": [9, 0, 0]}}), open(sp, "w"))
        p = subprocess.run([sys.executable, SIM, STATE, "v69", "5", "1", out, "--schedule", sp, "--season-cv"],
                           capture_output=True, text=True, cwd=DECK)
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse(os.path.exists(out))


if __name__ == "__main__":
    unittest.main(verbosity=2)
