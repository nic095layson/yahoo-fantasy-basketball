#!/usr/bin/env python3
"""Open-item enumeration for the data pull (fix F1/F6, adopted 2026-09-08).

Born from two misses on the same player two weeks apart. The 8/26 pull missed
Bennedict Mathurin's team change because unresolved situations living in the
JUDGMENT layer never got targeted searches; the post-mortem's fix (search every
flagged name) was run by hand on 8/27, 9/1 and 9/2 — then silently skipped for
3 of 8 names on 9/8, and one of the skipped names was Mathurin, whose situation
had just moved again (the 9/8 NOP-MEM trade). A checklist nothing audits is a
suggestion. This script makes the list mechanical and the execution checkable:

  default          parse docs/draft-deck.html's JUDGMENT block, flag every card
                   whose rationale carries an UNRESOLVED marker (the refinement
                   validated 2026-09-02: unresolved markers only, not any
                   transaction word — 18 flagged fell to 8 with zero loss), and
                   print a ready-to-fill "Open-item receipts" table. Also print
                   the implied TEAM WATCH SET (fix F3): the flagged players'
                   teams plus counterparties named in their rationales — trades
                   about a player's situation often never name the player
                   (the 9/8 miss was exactly this shape).

  --tags           print the pool's availability-tag inventory (fix F6): the
                   excluded set (out-*/*-recovery) and the risk set (*-risk).
                   The injury sweep diffs "returning player" coverage against
                   this list BOTH directions — returning-but-untagged is how
                   Jamal Murray shipped unpriced on 9/8.

  --check-report P verify the after-report at path P carries one receipts row
                   per flagged name under an "Open-item receipts" heading.
                   Exit 1 naming every flagged name without a receipt — a
                   flagged name with no receipt means the pull is incomplete
                   (DATA-PULL.md section 2).
"""
import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DECK = os.path.join(ROOT, "docs", "draft-deck.html")
POOL = os.path.join(ROOT, "data", "players.csv")

# Unresolved markers ONLY (validated 2026-09-02 against the hand triage of
# 9/1: this set flags the genuinely-open 8 and drops the 10 resolved trades
# the naive any-transaction-word scan over-selected).
UNRESOLVED = [
    "unsigned", "not signed", "still a free agent", "free agent", "on hold",
    "pending", "standoff", "non-guarantee", "non-guaranteed",
    "qualifying offer", "restricted", "no timetable", "unresolved",
    "awaiting", "undecided", "camp deal", "could run into", "investigation",
    "inquiry", "holdout", "trade request", "stalemate", "yet to sign",
    "no deal", "open question", "week-to-week", "re-check", "watch",
    "cleared but", "not yet executed", "awaiting execution",
    # Added 2026-09-08, first run of this script: the freshly re-authored
    # Kawhi and Mathurin cards described open situations in phrasings the
    # lexicon above did not cover, and both silently dropped off the flagged
    # list. The enumerator is lexicon-based, not a mind reader — so (a) these
    # phrasings joined the lexicon, and (b) DATA-PULL.md now carries the
    # authoring contract: a card describing an OPEN situation must include at
    # least one marker phrase from this list.
    "not formally executed", "yet to be finalized", "expected to be finalized",
    "reprice checkpoint",
]

TEAM_CODES = re.compile(
    r"\b(ATL|BOS|BKN|CHA|CHI|CLE|DAL|DEN|DET|GSW|HOU|IND|LAC|LAL|MEM|MIA|"
    r"MIL|MIN|NOP|NYK|OKC|ORL|PHI|PHX|POR|SAC|SAS|TOR|UTA|WAS)\b")


def judgment_entries():
    src = open(DECK, encoding="utf-8").read()
    m = re.search(r"const JUDGMENT = \{(.*?)\n\};", src, re.S)
    if not m:
        print("ERROR: JUDGMENT block not found in docs/draft-deck.html")
        sys.exit(2)
    date = re.search(r'date:\s*"([^"]+)"', m.group(1))
    entries = re.findall(
        r'"([^"]+)":\s*\{\s*adj:\s*(-?[\d.]+),\s*why:\s*"((?:[^"\\]|\\.)*)"',
        m.group(1))
    return (date.group(1) if date else "?"), entries


def flagged():
    date, entries = judgment_entries()
    out = []
    for name, adj, why in entries:
        low = why.lower()
        hits = sorted({k for k in UNRESOLVED if k in low})
        if hits:
            out.append((name, adj, hits, why))
    return date, out


def pool_rows():
    with open(POOL, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leading_tag(note):
    note = (note or "").strip()
    if not note:
        return ""
    return note.split(";")[0].strip().split(" ")[0]


def cmd_default():
    date, items = flagged()
    print(f"JUDGMENT dated {date} — {len(items)} open item(s) flagged\n")
    print("Every flagged name gets a DEDICATED search this pull, and the")
    print("after-report gets one receipts row per name (DATA-PULL.md §2).\n")
    print("## Open-item receipts")
    print()
    print("| player | query run | dated finding |")
    print("|---|---|---|")
    for name, adj, hits, _why in items:
        print(f"| {name} (adj {adj}; {', '.join(hits[:3])}) |  |  |")
    teams = set()
    rows = {r["player"]: r for r in pool_rows()}
    for name, _adj, _hits, why in items:
        if name in rows:
            teams.add(rows[name]["team"])
        teams.update(TEAM_CODES.findall(why))
    teams.discard("FA")  # an unsigned player's next team is unknown by definition
    print(f"\nTEAM WATCH SET (fix F3 — one team-shaped news query each): "
          f"{', '.join(sorted(teams)) or '(none)'}")
    print("A trade about a flagged player's cap room or depth chart may never")
    print("name the player; only a team-shaped query catches it (9/8 NOP-MEM).")


def cmd_tags():
    excluded, risk = [], []
    for r in pool_rows():
        t = leading_tag(r.get("note"))
        if not t:
            continue
        if t.startswith("out-") or "recovery" in t:
            excluded.append((r["player"], r["team"], r["note"]))
        elif "risk" in t:
            risk.append((r["player"], r["team"], r["note"]))
    print("Availability-tag inventory (fix F6). Diff BOTH directions against")
    print("this pull's returning-player coverage: a name in the coverage but")
    print("not below is how Jamal Murray shipped unpriced (2026-09-08).\n")
    print(f"EXCLUDED (out-*/recovery, availability 0.0) — {len(excluded)}:")
    for p, t, n in excluded:
        print(f"  {p:24s} {t:4s} {n}")
    print(f"\nRISK (availability 0.78) — {len(risk)}:")
    for p, t, n in risk:
        print(f"  {p:24s} {t:4s} {n}")


def cmd_check_report(path):
    date, items = flagged()
    try:
        report = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"RECEIPTS CHECK FAILED — cannot read report: {e}")
        sys.exit(1)
    m = re.search(r"^#+ .*Open-item receipts.*$", report, re.M | re.I)
    if not m:
        print("RECEIPTS CHECK FAILED — the report has no 'Open-item receipts' "
              "section. Run this script with no arguments for the required "
              "table; a flagged name with no receipt means the pull is "
              "incomplete.")
        sys.exit(1)
    tail = report[m.end():]
    nxt = re.search(r"^## ", tail, re.M)
    section = tail[:nxt.start()] if nxt else tail
    # The receipt must sit in the PLAYER column (first cell), not merely
    # appear somewhere in a row — on the first behavioral test of this
    # check, a deleted player cell slipped through because the player's
    # name survived inside the query column's text.
    first_cells = [ln.strip().split("|")[1].strip()
                   for ln in section.splitlines()
                   if ln.strip().startswith("|") and ln.count("|") >= 2]
    missing = [name for name, *_ in items
               if not any(name in cell for cell in first_cells)]
    if missing:
        print(f"RECEIPTS CHECK FAILED — {len(missing)} flagged name(s) have no "
              f"receipts row: {', '.join(missing)}. Each needs a dedicated "
              "search and a dated finding before the pull is complete.")
        sys.exit(1)
    print(f"receipts check PASS — all {len(items)} flagged names carry a "
          f"receipts row in {os.path.basename(path)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tags", action="store_true")
    ap.add_argument("--check-report", metavar="PATH")
    args = ap.parse_args()
    if args.tags:
        cmd_tags()
    elif args.check_report:
        cmd_check_report(args.check_report)
    else:
        cmd_default()


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:  # `| head` closing the pipe is not an error
        sys.stderr.close()
