#!/usr/bin/env python3
"""Red-first tests for arena/mocks/league_sim.py picks with "from_week" / "to_week" (kit owner 2026-10-31: the IL-return
scenarios, ESPN's return date as a variable in a separate section, the headline untouched). A player counts for his
team only inside his window of regular-season weeks; the playoffs play the final week's roster; a state with no
window draws exactly as before.

Run:  python3 arena/test_windows.py
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


def run(picks_fn=None, seasons=300, seed=7, extra=()):
    st = json.load(open(STATE, encoding="utf-8"))
    if picks_fn:
        st["picks"] = picks_fn(st["picks"])
    d = tempfile.mkdtemp(); sp = os.path.join(d, "state.json"); out = os.path.join(d, "out.json")
    json.dump(st, open(sp, "w"))
    r = subprocess.run([sys.executable, SIM, sp, "v69", str(seasons), str(seed), out, "--season-cv"] + list(extra),
                       capture_output=True, text=True)
    return r, (json.load(open(out)) if r.returncode == 0 else None)


def teams(rec):
    return json.dumps(rec["teams"], sort_keys=True)


class Windows(unittest.TestCase):
    def test_a_full_window_on_every_pick_draws_exactly_as_no_window(self):
        r0, base = run()
        r1, full = run(lambda picks: [dict(p, from_week=1, to_week=WEEKS) for p in picks])
        self.assertEqual((r0.returncode, r1.returncode), (0, 0), (r0.stderr, r1.stderr))
        self.assertEqual(teams(base), teams(full))
        self.assertNotIn("windows", base); self.assertIn("windows", full)

    def test_a_player_absent_all_season_equals_a_state_without_him(self):
        st = json.load(open(STATE)); seat1 = [p for p in st["picks"] if p["slot"] == 1]
        gone = seat1[0]["player"]
        _, without = run(lambda picks: [p for p in picks if p["player"] != gone])
        _, never = run(lambda picks: [dict(p, from_week=WEEKS + 1) if p["player"] == gone else p for p in picks])
        self.assertEqual(teams(without), teams(never))
        self.assertEqual(never["windows"]["1"][gone], [WEEKS + 1, WEEKS])

    def test_a_late_return_sits_between_absent_and_present(self):
        st = json.load(open(STATE)); seat1 = [p for p in st["picks"] if p["slot"] == 1]
        star = seat1[0]["player"]
        _, present = run(seasons=2000)
        _, absent = run(lambda picks: [p for p in picks if p["player"] != star], seasons=2000)
        _, mid = run(lambda picks: [dict(p, from_week=9) if p["player"] == star else p for p in picks], seasons=2000)
        lo, hi = sorted((absent["teams"]["1"]["cats_per_week"], present["teams"]["1"]["cats_per_week"]))
        self.assertLess(lo, mid["teams"]["1"]["cats_per_week"]); self.assertLess(mid["teams"]["1"]["cats_per_week"], hi)
        self.assertEqual(mid["windows"]["1"][star], [9, WEEKS])
        # the record's week_mu is the final week's model: with the star back it equals the present roster's
        self.assertEqual(mid["teams"]["1"]["week_mu"], present["teams"]["1"]["week_mu"])

    def test_verify_refuses_a_window_and_a_bad_window_halts(self):
        r, _ = run(lambda picks: [dict(p, from_week=3) for p in picks[:1]] + picks[1:], extra=["--verify"])
        self.assertNotEqual(r.returncode, 0); self.assertIn("verify", r.stderr)
        r, _ = run(lambda picks: [dict(p, from_week=0) for p in picks[:1]] + picks[1:])
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
