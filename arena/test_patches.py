#!/usr/bin/env python3
"""Red-first tests for arena/patches.py and league_sim.py --patch (kit owner 2026-10-26, "build the real-schedule
re-measurement"): the kit's assumption sweep moves one hand-set constant at a time; the same patch, from one shared
module, now reaches the real-schedule simulator so the bands sit on the configuration the title odds use.

Run:  python3 arena/test_patches.py
"""
import importlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

DECK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(DECK, "arena")); sys.path.insert(0, os.path.join(DECK, "scripts"))
STATE = os.path.join(DECK, "arena", "data", "states", "draft_state_100.json")
SIM = os.path.join(DECK, "arena", "mocks", "league_sim.py")


def fresh():
    import arena
    return importlib.reload(arena)


class Patches(unittest.TestCase):
    def test_a_constant_patch_sets_the_module_value(self):
        import patches
        a = fresh(); patches.apply(a, {"const": {"TEAM_WEEK_SHOCK": 0.0}})
        self.assertEqual(a.TEAM_WEEK_SHOCK, 0.0)

    def test_an_unknown_constant_is_an_error(self):
        import patches
        with self.assertRaises(AttributeError):
            patches.apply(fresh(), {"const": {"NO_SUCH_THING": 1}})

    def test_the_availability_patch_remaps_the_two_tiers(self):
        import patches
        a = fresh(); a.weekly_availability = lambda p: p["x"]     # a stand-in returning the tier it is given
        patches.apply(a, {"avail": [0.95, 0.65]})
        self.assertEqual([a.weekly_availability(dict(x=v)) for v in (0.88, 0.75, 0.5)], [0.95, 0.65, 0.5])

    def test_the_cv_patch_scales_every_category(self):
        import patches
        a = fresh(); before = dict(a.SEASON_CV)
        patches.apply(a, {"cv": 2.0})
        self.assertEqual(a.SEASON_CV, {c: v * 2.0 for c, v in before.items()})

    def test_the_games_patch_replaces_the_literal_or_fails(self):
        import patches
        a = fresh(); self.assertIn(3.5, a.team_week_model.__code__.co_consts)
        patches.apply(a, {"games": 4.0})
        self.assertIn(4.0, a.team_week_model.__code__.co_consts)
        self.assertNotIn(3.5, a.team_week_model.__code__.co_consts)


class LeagueSimPatch(unittest.TestCase):
    def run_sim(self, extra, seasons=200, seed=7):
        out = os.path.join(tempfile.mkdtemp(), "o.json")
        p = subprocess.run([sys.executable, SIM, STATE, "v69", str(seasons), str(seed), out, "--season-cv"] + extra,
                           capture_output=True, text=True, cwd=DECK)
        self.assertEqual(p.returncode, 0, p.stderr[-800:])
        return json.load(open(out)), open(out, "rb").read()

    def test_no_patch_file_leaves_the_output_unchanged_and_names_no_patch(self):
        rec, _ = self.run_sim([])
        self.assertNotIn("patch", rec)

    def test_a_patch_file_moves_the_season_and_the_record_names_it(self):
        pf = os.path.join(tempfile.mkdtemp(), "p.json"); json.dump({"const": {"TEAM_WEEK_SHOCK": 0.12}}, open(pf, "w"))
        base, _ = self.run_sim([])
        rec, _ = self.run_sim(["--patch", pf])
        self.assertEqual(rec["patch"], {"const": {"TEAM_WEEK_SHOCK": 0.12}})
        self.assertNotEqual(rec["teams"], base["teams"])   # every team's season, not one share that can tie by chance

    def test_the_patch_matches_arena_simulate_seasons_patched_the_same_way(self):
        # --verify on a patched run: the house simulator, patched by the same module, draws the same seasons
        pf = os.path.join(tempfile.mkdtemp(), "p.json"); json.dump({"avail": [0.95, 0.65], "cv": 1.1}, open(pf, "w"))
        rec, _ = self.run_sim(["--patch", pf, "--verify"])
        self.assertTrue(rec["verified_against_arena"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
