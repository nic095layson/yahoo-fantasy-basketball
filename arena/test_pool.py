#!/usr/bin/env python3
"""Red-first tests for arena/mocks/league_sim.py --pool (kit owner 2026-10-26, "use the season pool"): the simulator
loads the player lines from the named deck-schema CSV instead of the frozen arena/results/players_<tag>.csv, so an
in-season pickup the frozen pool lacks can be simulated. Without --pool the frozen file, as before.

Run:  python3 arena/test_pool.py
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATE = os.path.join(DECK, "arena", "data", "states", "draft_state_100.json")
SIM = os.path.join(DECK, "arena", "mocks", "league_sim.py")
FROZEN = os.path.join(DECK, "arena", "results", "players_v69.csv")
NEW = "Test Pickup Zzz"


def fixtures():
    """A pool with one extra player (a copy of the first pick's line under a new name) and a state that rosters him."""
    d = tempfile.mkdtemp()
    st = json.load(open(STATE, encoding="utf-8"))
    first = st["picks"][0]["player"]
    st["picks"][0]["player"] = NEW
    sp = os.path.join(d, "state.json"); json.dump(st, open(sp, "w"))
    with open(FROZEN, encoding="utf-8") as f:
        r = csv.DictReader(f); fields = r.fieldnames; rows = list(r)
    extra = dict(next(x for x in rows if x["player"] == first), player=NEW)
    pp = os.path.join(d, "pool.csv")
    with open(pp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows + [extra])
    return d, sp, pp


def run(state, extra, seasons=50, seed=7):
    out = os.path.join(tempfile.mkdtemp(), "out.json")
    p = subprocess.run([sys.executable, SIM, state, "v69", str(seasons), str(seed), out, "--season-cv"] + extra,
                       capture_output=True, text=True, cwd=DECK)
    return p, (json.load(open(out)) if p.returncode == 0 else None)


class Pool(unittest.TestCase):
    def test_a_player_only_in_the_named_pool_is_simulated_and_the_record_names_the_pool(self):
        _, sp, pp = fixtures()
        p, rec = run(sp, ["--pool", pp])
        self.assertEqual(p.returncode, 0, p.stderr[-800:])
        self.assertEqual(rec["pool"]["file"], pp)
        self.assertEqual(rec["pool"]["sha256"], hashlib.sha256(open(pp, "rb").read()).hexdigest())
        self.assertEqual(rec["pool"]["players"], 336)

    def test_without_the_flag_that_player_is_missing_from_the_frozen_pool(self):
        _, sp, _ = fixtures()
        p, _ = run(sp, [])
        self.assertNotEqual(p.returncode, 0)
        self.assertIn(NEW, p.stderr)

    def test_naming_the_frozen_file_gives_the_same_season_as_no_flag(self):
        _, a = run(STATE, [])
        _, b = run(STATE, ["--pool", FROZEN])
        self.assertNotIn("pool", a)
        self.assertEqual(a["teams"], b["teams"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
