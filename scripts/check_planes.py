#!/usr/bin/env python3
"""Cross-plane consistency gate — F7 (adopted 2026-09-21; mock-51 retro T7,
the S3 prototype of the 2026-09-21 validation report; owner: REFUSE).

    python3 scripts/check_planes.py [--kit PATH] [--waive "Name: reason"]... [--json]
    python3 scripts/check_planes.py --write-snapshot [--kit PATH]

The kit (fantasy-basketball-2026-27/report/projections-2026-27.csv) and the
deck (data/players.csv) are two planes of one system with DIFFERENT pools and
DIFFERENT lines by design (measured 2026-09-21: 235 shared names, 201 with
differing per-game lines, most with differing position strings). What must
never disagree, for every player BOTH planes carry:

  1. team placement
  2. exclusion class — a deck out-*/recovery tag (availability 0.0) <=> kit
     GP <= EXCL_GP (the four excluded rows sit at 15-20 GP; the two-way rows
     at 30 are not excluded on either plane)
  3. spelling — a name on one plane only whose surname and first three
     letters match a name on the other plane only is drift, not a legitimate
     one-plane row (Cam/Cameron Johnson class)
  4. re-derivation propagation — a line that MOVED on one plane since the
     last build must have moved on the other, or be waived by name. Mock 51:
     the kit's 9/16 bench downgrade of Reed Sheppard never reached the deck
     and the owner drafted him off the stale row (~7 points of title odds).
     The kit side of "since the last build" is data/kit-snapshot.csv (written
     by build_deck after each passing build); the deck side is the pool the
     published deck currently embeds.

Positions are not compared (Yahoo eligibility strings vs the kit's listing
differ by design). Exit 0 = clean, 1 = mismatches, 2 = kit not found.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import hoops  # noqa: E402

KIT_DEFAULT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")
KIT_FILE = os.path.join("report", "projections-2026-27.csv")
SNAPSHOT = os.path.join(ROOT, "data", "kit-snapshot.csv")
DECK_HTML = os.path.join(ROOT, "docs", "draft-deck.html")
POOL = os.path.join(ROOT, "data", "players.csv")
EXCL_GP = 25
# kit column -> deck column, and the deck's embedded raw order (RAW_COLS)
COLS = [("fgp", "fg_pct"), ("fga", "fga"), ("ftp", "ft_pct"), ("fta", "fta"), ("tpm", "tpm"),
        ("pts", "pts"), ("reb", "reb"), ("ast", "ast"), ("stl", "stl"), ("blk", "blk"), ("tov", "tov")]
RAW_ORDER = ["tpm", "pts", "reb", "ast", "stl", "blk", "tov", "fg_pct", "fga", "ft_pct", "fta"]
ALIASES = {"herb jones": "herbert jones", "cam johnson": "cameron johnson",
           "nic claxton": "nicolas claxton", "alex sarr": "alexandre sarr"}


def norm(name):
    """Twin of the kit's build_market.norm: accent-fold, lowercase, DROP . ' - ,
    (so "P.J. Washington Jr." and "PJ Washington" both read pj washington — a
    Yahoo spelling the 2026-09-22 rankings paste carries), then any other
    punctuation to a space, strip a generational suffix."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,\u2019-]", "", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"})
    return ALIASES.get(s, s)


def load_kit(kit_dir):
    path = os.path.join(kit_dir, KIT_FILE)
    if not os.path.isfile(path):
        return None, path
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows[norm(r["name"])] = r
    return rows, path


def kit_line(r):
    return {d: float(r[k]) for k, d in COLS}


def load_pool(path=POOL):
    with open(path, encoding="utf-8") as f:
        return {norm(r["player"]): r for r in csv.DictReader(f)}


def deck_line(r):
    return {d: float(r[d]) for _, d in COLS}


def load_deck_prev(path=DECK_HTML):
    """Per-game lines the published deck currently embeds (the deck side of
    'since the last build')."""
    try:
        html = open(path, encoding="utf-8").read()
    except OSError:
        return {}
    m = re.search(r"const PLAYERS = (\[.*?\]);", html, re.S)
    if not m:
        return {}
    out = {}
    for p in json.loads(m.group(1)):
        raw = p.get("r")
        if raw and len(raw) == len(RAW_ORDER):
            out[norm(p["n"])] = dict(zip(RAW_ORDER, [float(x) for x in raw]))
    return out


def load_snapshot(path=SNAPSHOT):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return {norm(r["name"]): r for r in csv.DictReader(f)}


def same(a, b, tol=1e-9):
    return all(abs(a[k] - b[k]) <= tol for k in a)


def compare(kit, pool, prev_deck, snapshot, waivers):
    shared = sorted(set(kit) & set(pool))
    kit_only = sorted(set(kit) - set(pool))
    deck_only = sorted(set(pool) - set(kit))
    res = {"shared": len(shared), "kit_only": [kit[n]["name"] for n in kit_only],
           "deck_only": [pool[n]["player"] for n in deck_only],
           "team": [], "exclusion": [], "drift": [], "propagation": [], "waived": [],
           "snapshot": snapshot is not None}
    waived_names = {norm(w.split(":", 1)[0]) for w in waivers}
    for n in shared:
        k, d = kit[n], pool[n]
        if k["team"].strip().upper() != d["team"].strip().upper():
            res["team"].append(f"{d['player']}: kit {k['team']} vs deck {d['team']}")
        kit_excl = float(k["gp"]) <= EXCL_GP
        deck_excl = hoops.availability(d) == 0.0
        if kit_excl != deck_excl:
            res["exclusion"].append(
                f"{d['player']}: kit GP {k['gp']} ({'excluded' if kit_excl else 'playable'}) vs deck tag "
                f"{(d.get('note') or '').split(' ')[0] or '(none)'} ({'excluded' if deck_excl else 'playable'})")
        if snapshot is not None:
            s = snapshot.get(n)
            kit_moved = s is None or not same(kit_line(k), kit_line(s)) or float(s["gp"]) != float(k["gp"])
            pd = prev_deck.get(n)
            deck_moved = pd is None or not same(deck_line(d), pd)
            if s is not None and pd is not None and kit_moved != deck_moved:
                if n in waived_names:
                    res["waived"].append(next(w for w in waivers if norm(w.split(":", 1)[0]) == n))
                    continue
                if kit_moved:
                    what = ", ".join(f"{dcol} {float(s[kcol])}->{float(k[kcol])}" for kcol, dcol in COLS
                                     if abs(float(s[kcol]) - float(k[kcol])) > 1e-9) or f"GP {s['gp']}->{k['gp']}"
                    res["propagation"].append(f"{d['player']}: kit re-derived ({what}) but the deck row is unchanged")
                else:
                    what = ", ".join(f"{dcol} {pd[dcol]}->{float(d[dcol])}" for _, dcol in COLS
                                     if abs(pd[dcol] - float(d[dcol])) > 1e-9)
                    res["propagation"].append(f"{d['player']}: deck re-derived ({what}) but the kit row is unchanged")
    key = lambda n: ((n.split() or [n])[-1], (n.split() or [n])[0][:3])
    ko = {key(n): n for n in kit_only}
    for n in deck_only:
        if key(n) in ko:
            res["drift"].append(f"kit '{kit[ko[key(n)]]['name']}' vs deck '{pool[n]['player']}' — one-plane on both sides, same surname + initial: a spelling, not two players")
    res["mismatches"] = len(res["team"]) + len(res["exclusion"]) + len(res["drift"]) + len(res["propagation"])
    return res


def write_snapshot(kit_path, dest=SNAPSHOT):
    data = open(kit_path, "rb").read()
    with open(dest, "wb") as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()


def run(kit_dir=KIT_DEFAULT, waivers=(), pool_path=POOL, deck_html=DECK_HTML, snapshot_path=SNAPSHOT):
    kit, kit_path = load_kit(kit_dir)
    if kit is None:
        return None, kit_path
    res = compare(kit, load_pool(pool_path), load_deck_prev(deck_html), load_snapshot(snapshot_path), list(waivers))
    res["kit_path"] = kit_path
    res["kit_sha256"] = hashlib.sha256(open(kit_path, "rb").read()).hexdigest()
    return res, kit_path


def report(res):
    print(f"planes: {res['shared']} shared · kit-only {len(res['kit_only'])} · deck-only {len(res['deck_only'])} · "
          f"team {len(res['team'])} · exclusion {len(res['exclusion'])} · drift {len(res['drift'])} · "
          f"propagation {len(res['propagation'])}" + ("" if res["snapshot"] else " (no kit snapshot: propagation check is a BASELINE this build)")
          + (f" · waived {len(res['waived'])}" if res["waived"] else ""))
    for k in ("team", "exclusion", "drift", "propagation"):
        for m in res[k]:
            print(f"  {k}: {m}")
    for w in res["waived"]:
        print(f"  waived: {w}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", default=KIT_DEFAULT)
    ap.add_argument("--waive", action="append", default=[], help='"Name: reason" (repeatable)')
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-snapshot", action="store_true")
    a = ap.parse_args()
    if a.write_snapshot:
        _, kit_path = load_kit(a.kit)
        if not os.path.isfile(kit_path):
            sys.exit(f"PLANES: kit not found at {kit_path}")
        print(f"snapshot written: {write_snapshot(kit_path)[:12]}")
        return
    res, kit_path = run(a.kit, a.waive)
    if res is None:
        print(f"PLANES: kit not found at {kit_path} (set KIT_REPO or --kit)")
        sys.exit(2)
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        report(res)
    sys.exit(1 if res["mismatches"] else 0)


if __name__ == "__main__":
    main()
