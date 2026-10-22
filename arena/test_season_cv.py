#!/usr/bin/env python3
"""Season per-game variation (D-ZS-3, owner 2026-10-21: "Adopt the fitted values", then "Season tools only").

arena.SEASON_CV is the per-game coefficient of variation fitted to the 2025-26 game logs (kit record
report/after-reports/zscore-assessment-2026-10-21/gamelogs/gscore_weights_2025-26.json, cv_fit: the board's top 180
with 20+ games). The season tools opt in through a cv= argument (team_week_model, simulate_seasons) and
league_sim.py --season-cv. Every default path keeps arena.CV, the draft engine's hand-set values, so the frozen
draft page (its JavaScript port of team_week_model, checked by scripts/check_parity.py) and every past grade
compute exactly as before; the known answers below were taken on deck 80eecdf before the change.

Run:  python3 arena/test_season_cv.py
"""
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest

DECK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(DECK)
for p in (os.path.join(DECK, "scripts"), os.path.join(DECK, "arena")):
    if p not in sys.path:
        sys.path.insert(0, p)

import hoops  # noqa: E402
import arena  # noqa: E402

POOL = "arena/results/players_v69.csv"
STATE = "arena/data/states/draft_state_100.json"
FIT = {"PTS": 0.395, "REB": 0.445, "AST": 0.496, "3PTM": 0.717, "ST": 0.945, "BLK": 1.072, "TO": 0.668}
# deck 80eecdf, before the change: simulate_seasons(rosters, 600, Random(2026)) and the twelve default weekly models
KNOWN_CHAMPS = {1: 92, 2: 10, 3: 97, 4: 20, 5: 37, 6: 88, 7: 14, 8: 17, 9: 5, 10: 155, 11: 65, 12: 0}
KNOWN_MODELS_SHA = "88073a511f9ef895"


def rosters():
    hoops.DATA_PATH = POOL
    by = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
    st = json.load(open(STATE, encoding="utf-8"))
    ros = {s: [] for s in range(1, arena.TEAMS + 1)}
    for pk in st["picks"]:
        ros[pk["slot"]].append(by[pk["player"]])
    return ros


class SeasonCV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ros = rosters()

    def test_season_cv_is_the_2025_26_fit(self):
        self.assertEqual(arena.SEASON_CV, FIT)

    def test_the_draft_engine_values_are_untouched(self):
        self.assertEqual(arena.CV, {"PTS": 0.30, "REB": 0.35, "AST": 0.40, "3PTM": 0.55, "ST": 0.70, "BLK": 0.75, "TO": 0.50})

    def test_default_paths_compute_exactly_as_before(self):
        models = {s: arena.team_week_model(r) for s, r in self.ros.items()}
        sha = hashlib.sha256(json.dumps(models, sort_keys=True, default=str).encode()).hexdigest()
        self.assertEqual(sha[:16], KNOWN_MODELS_SHA)
        champs, _ = arena.simulate_seasons(self.ros, 600, random.Random(2026))
        self.assertEqual(champs, KNOWN_CHAMPS)
        champs_none, _ = arena.simulate_seasons(self.ros, 600, random.Random(2026), cv=None)
        self.assertEqual(champs_none, KNOWN_CHAMPS)

    def test_the_season_cv_widens_only_the_counting_variances(self):
        r = self.ros[10]
        mu0, var0 = arena.team_week_model(r)
        mu1, var1 = arena.team_week_model(r, cv=arena.SEASON_CV)
        self.assertEqual(mu0, mu1)
        for c in FIT:
            self.assertGreater(var1[c], var0[c], c)
        for c in ("FG%", "FT%"):
            self.assertEqual(var1[c], var0[c], c)

    def test_simulate_seasons_takes_the_season_cv(self):
        a, _ = arena.simulate_seasons(self.ros, 600, random.Random(2026), cv=arena.SEASON_CV)
        self.assertNotEqual(a, KNOWN_CHAMPS)
        self.assertEqual(sum(a.values()), 600)

    def test_league_sim_season_cv_flag_verifies_against_the_house_simulator(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "ls.json")
            p = subprocess.run([sys.executable, "arena/mocks/league_sim.py", STATE, "v69", "300", "2026", out,
                                "--verify", "--season-cv"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr[-800:])
            rec = json.load(open(out, encoding="utf-8"))
        self.assertEqual(rec.get("cv"), "season")


if __name__ == "__main__":
    unittest.main(verbosity=2)
