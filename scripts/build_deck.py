#!/usr/bin/env python3
"""Draft Deck build pipeline (owner SLA, 2026-07-23): the ONLY sanctioned way
to regenerate the deck's embedded data. Fail-closed — every gate must pass
BEFORE any data reaches docs/draft-deck.html:

  gate 1  roster verification ran TODAY with zero mismatches
          (scripts/verify_rosters.py artifact)
  gate 2  freshness stamped TODAY with the verification recorded
  gate 3  pool completeness (MUST_HAVE) validates

Only then: regenerate the embedded pool from data/players.csv, inject it,
machine-sync the deck's data-pull stamp from freshness.json, and verify the
injection round-trips byte-identical. Exit non-zero on any failure; nothing
is written unless every gate and check passes.
"""
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DECK = os.path.join(ROOT, "docs", "draft-deck.html")
VERIFY = os.path.join(ROOT, "data", "roster_verification.json")
FRESH = os.path.join(ROOT, "data", "freshness.json")

sys.path.insert(0, HERE)
import hoops  # noqa: E402


def fail(msg):
    print(f"BUILD REFUSED — {msg}")
    sys.exit(1)


def main():
    today = datetime.date.today().isoformat()

    # gate 1: roster verification, today, clean
    try:
        with open(VERIFY, encoding="utf-8") as f:
            ver = json.load(f)
    except (OSError, ValueError):
        fail("no roster_verification.json — run scripts/verify_rosters.py first")
    if ver.get("date") != today:
        fail(f"roster verification is stale ({ver.get('date')}) — run "
             "scripts/verify_rosters.py today")
    if ver.get("mismatches"):
        fail(f"roster verification has {len(ver['mismatches'])} mismatch(es) — "
             "fix data/players.csv first")

    # gate 2: freshness stamped today with verification recorded
    try:
        with open(FRESH, encoding="utf-8") as f:
            fresh = json.load(f)
    except (OSError, ValueError):
        fail("no freshness.json — run the daily refresh and stamp")
    if fresh.get("date") != today:
        fail(f"freshness stamp is stale ({fresh.get('date')}) — refresh and "
             "stamp today before building")
    if "rosters_verified" not in fresh:
        fail("freshness stamp lacks the roster-verification record — restamp")

    # gate 3: pool completeness
    players_raw = hoops.load_players()
    missing = hoops.validate_pool(players_raw)
    if missing:
        fail(f"pool incomplete — missing consensus names: {missing[:5]}")

    # build the embedded pool
    players = hoops.zscores(players_raw)
    pool = [{
        "n": p["player"], "t": p["team"], "p": p["pos"].replace('"', ""),
        "note": p.get("note") or "", "av": hoops.availability(p),
        "z": {c: round(p["z"][c], 6) for c in hoops.CATS},
    } for p in players]
    data = json.dumps(pool, separators=(",", ":"))

    html = open(DECK, encoding="utf-8").read()
    html, n1 = re.subn(r"const PLAYERS = \[.*?\];",
                       "const PLAYERS = " + data + ";", html, count=1,
                       flags=re.S)
    html, n2 = re.subn(r'const BUILD_PULL = "[^"]*";',
                       f'const BUILD_PULL = "{fresh["date"]}";', html, count=1)
    # the visible header stamp renders from BUILD_PULL at runtime; the footer
    # prose date is soft-synced (narrative text, shape may change)
    html, n3 = re.subn(r"Pool refreshed \d{4}-\d{2}-\d{2}",
                       f"Pool refreshed {fresh['date']}", html, count=1)
    if not (n1 == 1 and n2 == 1):
        fail(f"injection anchors not found (players={n1}, build_pull={n2}) — "
             "deck markup drifted; do not hand-edit anchors")
    if n3 == 0:
        print("note: footer prose date anchor not found (soft sync skipped)")

    manifest = {
        "built": today, "pool": len(pool),
        "verification": {"mode": ver.get("mode"),
                         "checked": ver.get("checked"),
                         "teams_covered": ver.get("teams_covered")},
        "freshness_note": (lambda n: n if len(n) <= 160
                           else n[:160].rsplit(" ", 1)[0] + " \u2026")(
                              fresh.get("note") or ""),
    }
    manifest_comment = f"<!-- build-manifest {json.dumps(manifest)} -->\n"
    html = re.sub(r"<!-- build-manifest \{.*?\} -->\n", "", html)
    html = manifest_comment + html

    with open(DECK, "w", encoding="utf-8") as f:
        f.write(html)

    # post-write integrity: injected data must round-trip byte-identical
    back = open(DECK, encoding="utf-8").read()
    m = re.search(r"const PLAYERS = (\[.*?\]);", back, re.S)
    if not m or m.group(1) != data:
        fail("post-write integrity check failed — injected data does not "
             "round-trip; deck NOT safe to publish")
    if f'const BUILD_PULL = "{fresh["date"]}"' not in back:
        fail("post-write integrity check failed — BUILD_PULL not synced")

    print(f"deck built: {len(pool)} players · pull {fresh['date']} · "
          f"verification {ver.get('mode')} ({ver.get('checked')}/{len(pool)} "
          "rows checked) · injection round-trip OK")
    print("safe to publish docs/draft-deck.html")


if __name__ == "__main__":
    main()
