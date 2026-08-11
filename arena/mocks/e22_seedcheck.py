"""E22 seed-robustness check (2026-08-05).

The four largest shipped-vs-resil champ%% gaps in e22_measurement (m21
-26.1, m24 -23.7, m34 +10.1, m39 +24.1) each trace to one or two
late-round player differences. Before quoting them, re-simulate those
four mocks' three arms on a DISJOINT seed set (101/103/107 x 6000) —
if a gap is a common-random-number artifact it will not survive.

Fresh clone + `python3 arena/mocks/e22_seedcheck.py` regenerates
arena/results/e22_seedcheck_out.json.
"""

import os as _os_epoch
_os_epoch.environ.setdefault("ARENA_WEEK_MODEL", "static")  # v1-epoch harness: regenerates pre-2026-08-05 instrument numbers
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e22_measurement as e22  # noqa: E402  (chdirs to repo root on import)

e22.HEAD_SEEDS = [101, 103, 107]

MOCKS = ["21", "24", "34", "39"]
only = os.environ.get("E22_SEEDCHECK_MOCKS")
todo = only.split(",") if only else MOCKS

out = {}
for mk in todo:
    print(f"=== seedcheck mock {mk} (seeds {e22.HEAD_SEEDS}) ===", flush=True)
    out[mk] = e22.measure_mock(mk)
    a = out[mk]["arms"]
    print(f"  baseline {a['baseline']['champ']:6.2f} | shipped {a['shipped']['champ']:6.2f} "
          f"| resil {a['resil']['champ']:6.2f}", flush=True)

path = ("arena/results/e22_seedcheck_out.json" if not only else
        f"arena/results/e22_seedcheck_out_m{'_'.join(todo)}.json")
json.dump(out, open(path, "w"), indent=1)
print("wrote", path)
