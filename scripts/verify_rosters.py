#!/usr/bin/env python3
"""Roster verification (owner law 2026-07-23, hardened after the Hachimura
miss): every freshness pull cross-references the pool's team column against
NBA/ESPN official roster data, per player, mechanically.

Two modes:
  direct-complete  — fetches all 30 rosters from ESPN's public JSON API
                     (site.api.espn.com). Requires the environment's network
                     policy to allow that domain; the complete guarantee.
  fallback-partial — when the API is unreachable (sandbox policy denial),
                     reads data/rosters_official.json, an evidence file the
                     Cowork refresh populates from NBA/ESPN-sourced
                     verification. Partial coverage, honestly marked.

Writes data/roster_verification.json; `hoops.py freshness --stamp` HARD-FAILS
unless that file is dated today with zero mismatches. Exit 1 on mismatches.
"""
import datetime
import json
import os
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
POOL = os.path.join(DATA, "players.csv")
EVIDENCE = os.path.join(DATA, "rosters_official.json")
OUT = os.path.join(DATA, "roster_verification.json")

ESPN_TEAMS = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"
ESPN_ROSTER = ESPN_TEAMS + "/{tid}/roster"
ESPN_ABBR = {"GS": "GSW", "SA": "SAS", "NO": "NOP", "NY": "NYK",
             "UTAH": "UTA", "WSH": "WAS"}


def norm(name):
    s = unicodedata.normalize("NFD", name)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace(".", "").replace("'", "").replace("-", " ").strip()


def load_pool():
    import csv
    with open(POOL, encoding="utf-8") as f:
        return [(r["player"], r["team"]) for r in csv.DictReader(f)]


def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "hoops-verify/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def try_direct():
    """All 30 official rosters via ESPN's public API. Returns {ABBR: [names]}
    or None if the network policy blocks the domain.

    The failure is REPORTED, not swallowed (audit 2026-08-09, F01): a bare
    `except: return None` made a transient timeout indistinguishable from a
    policy denial, so an intermittent network fault silently downgraded the
    run to the evidence-file mode behind one advisory line.
    """
    try:
        teams = fetch_json(ESPN_TEAMS)
    except Exception as e:
        print(f"verify_rosters: direct ESPN pull unavailable — {type(e).__name__}: {e}",
              file=sys.stderr)
        return None
    rosters = {}
    entries = teams["sports"][0]["leagues"][0]["teams"]
    for e in entries:
        t = e["team"]
        abbr = ESPN_ABBR.get(t["abbreviation"], t["abbreviation"])
        data = fetch_json(ESPN_ROSTER.format(tid=t["id"]))
        rosters[abbr] = [a["displayName"] for a in data.get("athletes", [])]
    return rosters


def load_fallback():
    if not os.path.exists(EVIDENCE):
        return None, None
    ev = json.load(open(EVIDENCE, encoding="utf-8"))
    return ev.get("teams", {}), ev


def main():
    # Unmatched rows now FAIL by default (audit F01): a pool row on no
    # official roster used to land in `unmatched`, which is never a mismatch,
    # so a fabricated team ("Bronny James,ZZZ") exited 0 and passed both
    # gates — exempting exactly the rows most likely to be wrong, the newly
    # added ones. `--strict` is retained as a no-op alias; the bypass is now
    # explicit and must carry a reason.
    allow_unmatched = "--allow-unmatched" in sys.argv
    ev = None
    rosters = try_direct()
    if rosters is not None:
        mode, source = "direct-complete", "site.api.espn.com (all 30 rosters)"
    else:
        rosters, ev = load_fallback()
        if rosters is None:
            print("verify_rosters: direct API blocked by the environment's "
                  "network policy AND no data/rosters_official.json evidence "
                  "file exists.")
            print("Fix either way: (a) allow site.api.espn.com in the Claude "
                  "environment's network policy for the complete direct pull, "
                  "or (b) have the refresh write the evidence file from "
                  "NBA/ESPN-sourced verification.")
            sys.exit(2)
        mode = "fallback-partial"
        source = ev.get("source", "data/rosters_official.json")

    where = {}   # normalized player name -> official team
    for abbr, names in rosters.items():
        for n in names:
            where[norm(n)] = abbr

    pool = load_pool()
    mismatches, unmatched, checked = [], [], 0
    for player, team in pool:
        key = norm(player)
        official = where.get(key)
        if team == "FA":
            checked += 1
            if official:
                mismatches.append({"player": player, "pool": "FA",
                                   "official": official,
                                   "why": "listed FA but appears on a roster"})
            continue
        if official is None:
            unmatched.append(player)
            continue
        checked += 1
        if official != team:
            mismatches.append({"player": player, "pool": team,
                               "official": official})

    # THE CENTRAL FIX (audit 2026-08-09, F01/F04). `date` used to be
    # today() unconditionally — a date this script stamps on itself. Every
    # downstream gate then checked that self-written date and reported green,
    # so the whole pipeline could be walked end to end having done zero
    # research. In fallback mode the artifact now inherits the EVIDENCE
    # file's own date, so `freshness --stamp` and `build_deck.py` (both of
    # which require date == today) fail until data/rosters_official.json is
    # RE-AUTHORED by that day's pull. Re-dating the evidence is a deliberate
    # act that means "I checked today"; nothing re-dates it automatically.
    # `checked_at` keeps the mechanical run time, which is a different fact.
    today = datetime.date.today().isoformat()
    ev_date = (ev or {}).get("date") if mode == "fallback-partial" else today
    result = {
        "date": ev_date or "unknown",
        "checked_at": today,
        "evidence_date": ev_date,
        "mode": mode,
        "source": source,
        "teams_covered": len(rosters),
        "pool_size": len(pool),
        "checked": checked,
        "mismatches": mismatches,
        "unmatched_count": len(unmatched),
        "unmatched": unmatched[:40],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"roster verification [{mode}] via {source}")
    print(f"  teams covered: {len(rosters)}  pool rows checked: {checked}/{len(pool)}"
          f"  unmatched: {len(unmatched)}")
    if mismatches:
        print("  MISMATCHES:")
        for m in mismatches:
            print(f"    {m['player']}: pool={m['pool']} official={m['official']}")
        sys.exit(1)
    print("  mismatches: 0")
    if mode == "fallback-partial":
        print("  PARTIAL VERIFICATION — checked against data/rosters_official"
              f".json (authored {ev_date}), not an independent live source.")
        print("  Allow site.api.espn.com in the environment network policy for "
              "the complete direct guarantee.")
        if ev_date != today:
            print(f"  STALE EVIDENCE: the evidence file is dated {ev_date}, "
                  f"today is {today}. This artifact inherits {ev_date}, so the "
                  "freshness stamp and the deck build will REFUSE until that "
                  "file is re-authored by today's pull. That is the gate "
                  "working: nothing here has checked the world today.")
    if unmatched:
        print(f"  UNMATCHED ({len(unmatched)}): "
              + ", ".join(unmatched[:8])
              + (f" … +{len(unmatched) - 8} more" if len(unmatched) > 8 else ""))
        print("  These rows sit on no official roster — verify each, or pass "
              "--allow-unmatched with the reason recorded in the stamp note.")
        if not allow_unmatched:
            sys.exit(1)


if __name__ == "__main__":
    main()
