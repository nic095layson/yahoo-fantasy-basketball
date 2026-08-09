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
import hashlib
import json
import os
import re
import sys

import archetypes

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
    # gate 1b: rows on no official roster are not exempt (audit F01)
    if ver.get("unmatched_count"):
        fail(f"roster verification has {ver['unmatched_count']} unmatched row(s) "
             f"({', '.join(ver.get('unmatched', [])[:5])}) — these sit on no "
             "official roster and are the rows most likely to be wrong. Verify "
             "them, or re-run verify_rosters.py --allow-unmatched and state the "
             "reason in the freshness note.")

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

    # gate 4: the pool must have MOVED, or the note must say why it didn't
    # (audit 2026-08-09, F04). Gates 1-3 all reduce to dates the scripts
    # stamp on themselves; none of them observes whether any research
    # happened. A content hash does: either players.csv changed since the
    # last build, or this pull explicitly asserts a quiet day with its
    # sources named. Nothing else gets to publish.
    pool_hash = hashlib.sha256(
        open(os.path.join(ROOT, "data", "players.csv"), "rb").read()).hexdigest()
    prev = re.search(r"<!-- build-manifest (\{.*?\}) -->", open(DECK, encoding="utf-8").read())
    prev_hash = json.loads(prev.group(1)).get("pool_sha256") if prev else None
    note_l = (fresh.get("note") or "").lower()
    quiet_ok = any(k in note_l for k in ("no change", "zero confirmed",
                                         "zero pool", "quiet"))
    if prev_hash and pool_hash == prev_hash and not quiet_ok:
        fail("data/players.csv is byte-identical to the last published build "
             f"({pool_hash[:12]}). Either this pull changed nothing — in which "
             "case say so explicitly in the freshness --note, naming the "
             "sources swept — or the pull did not actually land. A build that "
             "republishes an unchanged pool under a fresh date is the failure "
             "this gate exists to catch.")

    # gate 5: the deck's JUDGMENT layer rides outside every other check
    # (audit F15/F19/F35). It is hand-authored prose that renders to the
    # owner as the stated reason to fade a player, it was byte-identical
    # across four stamped pulls and ~11 republishes, and its own `date` is
    # never rendered anywhere in the page.
    # The block is a JS object literal (unquoted keys, comments), not JSON, so
    # it is read by targeted regex rather than a parser.
    deck_src = open(DECK, encoding="utf-8").read()
    jm = re.search(r"const JUDGMENT = \{(.*?)\n\};", deck_src, re.S)
    if not jm:
        fail("JUDGMENT block not found — deck markup drifted; do not hand-edit")
    jdate = re.search(r'date:\s*"(\d{4}-\d{2}-\d{2})"', jm.group(1))
    if not jdate:
        fail("JUDGMENT block carries no `date:` field — cannot tell whether "
             "the layer was re-authored with this pull")
    if jdate.group(1) != fresh["date"]:
        fail(f"JUDGMENT layer is dated {jdate.group(1)} but the pool is "
             f"{fresh['date']}. SKILL.md §1d requires the judgment layer to be "
             "re-authored in the same pass as the data — it rides on the card "
             "as the stated reason to fade a player. Re-author it and its "
             "`date`, or delete the entries that no longer hold.")
    pmatch = re.search(r"\n  players: \{(.*?)\n  \},?\n", jm.group(1), re.S)
    if pmatch:
        pool_names = {p["player"] for p in players_raw}
        named = re.findall(r'^\s{4}"([^"]+)":', pmatch.group(1), re.M)
        orphans = [n for n in named if n not in pool_names]
        if orphans:
            fail(f"JUDGMENT names absent from the pool: {orphans[:5]} — an "
                 "entry for an undraftable player renders a rationale for a "
                 "row that does not exist.")

    # build the embedded pool
    players = hoops.zscores(players_raw)
    archetypes.prime(players, hoops.availability)
    pool = [{
        "n": p["player"], "t": p["team"], "p": p["pos"].replace('"', ""),
        "note": p.get("note") or "", "av": hoops.availability(p),
        "z": {c: round(p["z"][c], 6) for c in hoops.CATS},
        # raw per-game stats (E9 ship 2026-08-04): the ΔECW weekly model
        # consumes raw rates, not z — order: tpm,pts,reb,ast,stl,blk,tov,
        # fg_pct,fga,ft_pct,fta (see RAW_COLS in the engine block)
        "r": [round(float(p[c]), 4) for c in
              ("tpm", "pts", "reb", "ast", "stl", "blk", "tov",
               "fg_pct", "fga", "ft_pct", "fta")],
        # archetype layer (codified 2026-07-30): profile code, out-of-
        # position flags, style coordinate — display-only consumers
        **dict(zip(("ar", "fx", "sy"), archetypes.classify(p))),
    } for p in players]
    data = json.dumps(pool, separators=(",", ":"))

    html = open(DECK, encoding="utf-8").read()
    html, n1 = re.subn(r"const PLAYERS = \[.*?\];",
                       "const PLAYERS = " + data + ";", html, count=1,
                       flags=re.S)
    html, n2 = re.subn(r'const BUILD_PULL = "[^"]*";',
                       f'const BUILD_PULL = "{fresh["date"]}";', html, count=1)
    # what the last sweep changed, shown by the Daily-sweep button panel
    note = json.dumps(fresh.get("note") or "")
    # whole-line anchor (the JSON note contains semicolons) and a callable
    # replacement (the JSON may contain backslash escapes re.sub would eat);
    # the declaration line must carry no trailing comment
    html, n2b = re.subn(r"const BUILD_NOTE = .*",
                        lambda m: f"const BUILD_NOTE = {note};", html, count=1)
    # the visible header stamp renders from BUILD_PULL at runtime; the footer
    # prose date is soft-synced (narrative text, shape may change)
    html, n3 = re.subn(r"Pool refreshed \d{4}-\d{2}-\d{2}",
                       f"Pool refreshed {fresh['date']}", html, count=1)
    if not (n1 == 1 and n2 == 1 and n2b == 1):
        fail(f"injection anchors not found (players={n1}, build_pull={n2}, "
             f"build_note={n2b}) — deck markup drifted; do not hand-edit "
             "anchors")
    if n3 == 0:
        print("note: footer prose date anchor not found (soft sync skipped)")

    manifest = {
        "built": today, "pool": len(pool),
        "pool_sha256": pool_hash,
        "verification_mode": ver.get("mode"),
        "evidence_date": ver.get("evidence_date"),
        "unmatched": ver.get("unmatched_count"),
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
    if f"const BUILD_NOTE = {note};" not in back:
        fail("post-write integrity check failed — BUILD_NOTE not synced")

    print(f"deck built: {len(pool)} players · pull {fresh['date']} · "
          f"pool {pool_hash[:12]} · injection round-trip OK")
    if ver.get("mode") != "direct-complete":
        print(f"  PARTIAL VERIFICATION — {ver.get('checked')}/{len(pool)} rows "
              f"checked against data/rosters_official.json (authored "
              f"{ver.get('evidence_date')}), not an independent live source.")
    else:
        print(f"  verification direct-complete: {ver.get('checked')}/{len(pool)} "
              "rows against all 30 official rosters")
    print("safe to publish docs/draft-deck.html")


if __name__ == "__main__":
    main()
