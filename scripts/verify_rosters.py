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

WO-2 (2026-10-01): a direct-mode run RE-AUTHORS the evidence file's teams
from the live feed (date = today, a `reauthored` block records the source),
so the fallback file mirrors the last live truth instead of only what the
pulls wrote — it had carried Gabe Vincent on ATL for three months while he
was unsigned. The `source` narrative is left alone. The name fold drops
generational suffixes (ESPN lists 'Jimmy Butler III', 'Ronald Holland II')
and carries the planes gate's aliases. HOOPS_VERIFY_OFFLINE (the gate suite)
skips the fetch and therefore never re-authors.

Writes data/roster_verification.json; `hoops.py freshness --stamp` HARD-FAILS
unless that file is dated today with zero mismatches. Exit 1 on mismatches.
"""
import datetime
import json
import os
import sys
import time
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


SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}
ALIASES = {"ron holland": "ronald holland", "herb jones": "herbert jones",
           "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton",
           "alex sarr": "alexandre sarr"}  # twin of check_planes.ALIASES


def norm(name):
    s = unicodedata.normalize("NFD", name)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().replace(".", "").replace("'", "").replace("-", " ").strip()
    s = " ".join(t for t in s.split() if t not in SUFFIXES)  # WO-2: 'Jimmy Butler III' == 'Jimmy Butler'
    return ALIASES.get(s, s)


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
    if os.environ.get("HOOPS_VERIFY_OFFLINE"):
        # The gate suite pins itself to the evidence-file mode: its cases
        # mutate data/rosters_official.json to make the gates fire, which the
        # live feed would ignore. Set by scripts/test_gates.py only (2026-10-01,
        # the first day site.api.espn.com answered from this environment).
        print("verify_rosters: HOOPS_VERIFY_OFFLINE set — direct ESPN pull "
              "skipped on request; evidence-file mode", file=sys.stderr)
        return None
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
        # Per-team fetches ride the same proxy; on 2026-10-01 a TLS handshake
        # timed out mid-loop and escaped as a traceback (the gate suite's
        # second run). Three tries with backoff, then REPORT and fall back —
        # the same contract as the first fetch (F01: reported, not swallowed).
        data, last = None, None
        for attempt in range(3):
            try:
                data = fetch_json(ESPN_ROSTER.format(tid=t["id"]))
                break
            except Exception as exc:
                last = exc
                time.sleep(2 * (attempt + 1))
        if data is None:
            print(f"verify_rosters: direct ESPN pull failed on {abbr} after 3 tries — "
                  f"{type(last).__name__}: {last}; evidence-file mode", file=sys.stderr)
            return None
        rosters[abbr] = [a["displayName"] for a in data.get("athletes", [])]
    return rosters


def reauthor_evidence(rosters, today):
    """WO-2: direct mode rewrites the evidence file's teams from the live feed.
    The `source` narrative (the pulls' history) is preserved; `teams` and
    `date` become the feed's; a `reauthored` block records when and from where."""
    ev = {}
    if os.path.exists(EVIDENCE):
        ev = json.load(open(EVIDENCE, encoding="utf-8"))
    ev["date"] = today
    ev["teams"] = {abbr: sorted(names) for abbr, names in sorted(rosters.items())}
    ev["reauthored"] = {"date": today, "source": "site.api.espn.com (all 30 rosters, direct-complete)",
                        "rosters": len(rosters), "names": sum(len(v) for v in rosters.values())}
    with open(EVIDENCE, "w", encoding="utf-8") as f:
        json.dump(ev, f, ensure_ascii=False, indent=1)
    return ev


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
        reauthor_evidence(rosters, datetime.date.today().isoformat())
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
        # R4-F05 (2026-08-10): the bypass must live in the ARTIFACT, not the
        # exit code — build_deck's gate 1b reads this field, so the exemption
        # is recorded, auditable, and deliberate rather than a flag that
        # changed nothing downstream.
        "allow_unmatched": allow_unmatched,
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
