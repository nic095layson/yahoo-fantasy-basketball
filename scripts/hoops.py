#!/usr/bin/env python3
"""hoops — in-Claude fantasy basketball analyzer and draft tool.

No accounts, no APIs. Player projections live in data/players.csv (editable);
this script turns them into 9-cat z-score values and provides:

    rank            Overall rankings, punt-aware:  rank --punt FT%,TO
    profile         Category strengths of a set of players (a roster)
    trade           Evaluate a trade:  trade --send "A,B" --get "C"
    find            Look up players by name fragment
    freshness       Show or stamp the daily data refresh (--stamp --note)
    validate        Check the pool for missing consensus players
    draft init      Start a draft:  draft init --teams 12 --size 15 --slot 4
    draft turn      ONE-SHOT live-draft turn: log announced picks
                    ("Jokic; my:Wemby"; numeric prefixes correct/backfill)
                    and emit the full decision card
    draft resync    Wipe the board and rebuild it from a pasted pick list
    draft fix       Correct any logged pick:  draft fix 15 "Name"
    draft pick      Log a single pick (between-turn use)
    draft best      Best available, punt-aware, annotated with your needs
    draft status    Your roster, build profile, per-category rank vs field
    draft rosters   Every team's roster so far
    draft matrix    Category z-totals for all teams; where you lead/trail
    draft vs        Head-to-head category comparison vs one opponent
    draft undo      Take back the last logged pick

Categories: FG%, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO (TO inverted).
Percentage categories are volume-weighted (impact = (pct - league pct) * attempts).
Values are z-scores over the player pool: +1.0 = one standard deviation better
than average in that category. State for a live draft sits in ./draft_state.json.
"""

import argparse
import csv
import datetime
import json
import math
import os
import re
import sys
import unicodedata

DATA_PATH = os.environ.get(
    "HOOPS_DATA",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "..", "data", "players.csv"))
FRESH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "data", "freshness.json")
STATE_PATH = os.environ.get("HOOPS_DRAFT_STATE", "draft_state.json")

# Owner's league positional slots (layout confirmed 2026-07-12):
# PG, SG, G, SF, PF, F, C, C — plus 2 Util and 3 BN, which any player
# fills. Leagues with other layouts get an approximate feasibility guard.
POSITIONAL_SLOTS = (
    ("PG", ("PG",)), ("SG", ("SG",)), ("G", ("PG", "SG")),
    ("SF", ("SF",)), ("PF", ("PF",)), ("F", ("SF", "PF")),
    ("C", ("C",)), ("C", ("C",)),
)

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
COUNT_COLS = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast",
              "ST": "stl", "BLK": "blk", "TO": "tov"}


# --------------------------------------------------------------------------
# Data freshness — the daily-refresh rule
# --------------------------------------------------------------------------

def read_freshness():
    try:
        with open(FRESH_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def check_freshness():
    """Warn loudly (stderr) when the data hasn't been refreshed today."""
    today = datetime.date.today().isoformat()
    info = read_freshness()
    last = info.get("date", "never") if info else "never"
    if last == today:
        return
    print(
        "!" * 72 + "\n"
        f"! DATA FRESHNESS RULE: projections last refreshed {last}; "
        f"today is {today}.\n"
        "! Before any analysis: web-search current NBA rosters, trades, and\n"
        "! injuries for the players involved, update data/players.csv (stats,\n"
        "! team, note column), then record the refresh:\n"
        "!     python3 scripts/hoops.py freshness --stamp --note 'what changed'\n"
        + "!" * 72, file=sys.stderr)


# Consensus-relevant players that must exist in the pool. A missing name
# here means the dataset lost a draftable player (the Markkanen incident,
# 2026-07-11). Checked on every freshness stamp and via `validate`.
MUST_HAVE = [
    "Nikola Jokic", "Victor Wembanyama", "Shai Gilgeous-Alexander",
    "Luka Doncic", "Giannis Antetokounmpo", "Anthony Davis",
    "Cade Cunningham", "Anthony Edwards", "Kevin Durant", "Jalen Williams",
    "Chet Holmgren", "Evan Mobley", "Donovan Mitchell", "Devin Booker",
    "Tyrese Maxey", "Karl-Anthony Towns", "Domantas Sabonis",
    "Alperen Sengun", "Jalen Brunson", "Trae Young", "Ja Morant",
    "Jaren Jackson Jr.", "Stephen Curry", "Bam Adebayo", "Cooper Flagg",
    "Scottie Barnes", "Franz Wagner", "Paolo Banchero", "Jalen Johnson",
    "Amen Thompson", "LeBron James", "Jaylen Brown", "Ivica Zubac",
    "De'Aaron Fox", "Jamal Murray", "James Harden", "Zion Williamson",
    "Kawhi Leonard", "Tyler Herro", "Desmond Bane", "Derrick White",
    "Jimmy Butler", "LaMelo Ball", "Darius Garland", "Josh Giddey",
    "Dyson Daniels", "Devin Vassell", "Jalen Duren", "Rudy Gobert",
    "Jarrett Allen", "Walker Kessler", "Myles Turner", "Deandre Ayton",
    "Mark Williams", "Kristaps Porzingis", "Joel Embiid", "Nikola Vucevic",
    "Lauri Markkanen", "Tyrese Haliburton", "Jayson Tatum", "Kyrie Irving",
    "Damian Lillard", "Fred VanVleet", "Dejounte Murray", "Paul George",
    "Brandon Ingram", "Zach LaVine", "DeMar DeRozan", "Jalen Green",
    "Norman Powell", "Cam Thomas", "Coby White", "Austin Reaves",
    "CJ McCollum", "Anfernee Simons", "Immanuel Quickley", "Jalen Suggs",
    "Jrue Holiday", "D'Angelo Russell", "OG Anunoby", "Mikal Bridges",
    "Trey Murphy III", "Michael Porter Jr.", "Pascal Siakam",
    "Julius Randle", "Tari Eason", "Aaron Gordon", "Payton Pritchard",
    "Josh Hart", "Alex Sarr", "Zach Edey", "Donovan Clingan",
    "Isaiah Hartenstein", "Kel'el Ware", "Miles Bridges", "Brandon Miller",
    "RJ Barrett", "Deni Avdija", "Shaedon Sharpe", "Reed Sheppard",
    "Andrew Nembhard", "Stephon Castle", "VJ Edgecombe", "Dylan Harper",
    "Keyonte George", "Naz Reid", "Brook Lopez", "Donte DiVincenzo",
    # 2026 draft class (owner law 2026-07-22: every June draft adds its
    # consensus fantasy-relevant rookies here so the stamp fails until
    # the pool carries them)
    "AJ Dybantsa", "Darryn Peterson", "Cameron Boozer", "Caleb Wilson",
    # 2026-07-27 completeness sync vs the draft-kit top-200 (all inside the
    # 156-pick draftable universe; ported with sourced provenance)
    "Jerami Grant", "Yaxel Lendeborg", "Alex Caruso", "Kyle Filipowski",
    "Jared McCain", "Ayo Dosunmu", "Luguentz Dort", "Derik Queen",
]


def validate_pool(players):
    """Return list of MUST_HAVE names missing from the pool."""
    have = {p["player"] for p in players}
    return [n for n in MUST_HAVE if n not in have]


def cmd_freshness(args):
    if args.stamp:
        missing = [] if args.force else validate_pool(load_players())
        if missing:
            print("⚠ POOL INCOMPLETE — missing consensus players:")
            for n in missing:
                print(f"    {n}")
            print("Add them to data/players.csv (retired players keep a row "
                  "with note out-retired), or bypass with --force.")
            sys.exit(1)
        # Roster validation lock v2 (owner law 2026-07-23, hardened after the
        # Hachimura miss — a quiet FA signing that a headline sweep missed):
        # the stamp requires TODAY'S mechanical verification artifact from
        # scripts/verify_rosters.py with zero mismatches. That script
        # cross-references every pool row against NBA/ESPN official roster
        # data — complete when the environment's network policy allows
        # site.api.espn.com, evidence-file fallback until then.
        ver_mode = None
        if not args.force:
            vp = os.path.join(os.path.dirname(FRESH_PATH),
                              "roster_verification.json")
            ok = False
            try:
                with open(vp, encoding="utf-8") as f:
                    v = json.load(f)
                ver_mode = v.get("mode")
                ok = (v.get("date") == datetime.date.today().isoformat()
                      and not v.get("mismatches"))
            except (OSError, ValueError):
                ok = False
            if not ok:
                print("⚠ ROSTER VALIDATION LOCK — stamp refused.")
                print("Run: python3 scripts/verify_rosters.py  (per-player")
                print("cross-reference against NBA/ESPN official rosters).")
                print("The stamp requires today's roster_verification.json")
                print("with zero mismatches. --force bypasses with a stated")
                print("reason in --note.")
                sys.exit(1)
            if ver_mode == "fallback-partial":
                print("note: roster verification is fallback-partial — allow "
                      "site.api.espn.com in the environment network policy "
                      "for the complete direct pull.")
        stamp = {"date": datetime.date.today().isoformat(),
                 "note": args.note or "refreshed"}
        # Structured pool-motion assertion (R4-F22, 2026-08-10): gate 4 used
        # to scan the prose note for keywords like "quiet", which any
        # sentence could satisfy by accident. The assertion is now a
        # deliberate flag, or absent.
        if args.pool_changes is not None:
            stamp["pool_changes"] = {"changed": True, "note": args.pool_changes}
        elif args.no_pool_changes:
            stamp["pool_changes"] = {"changed": False, "note": ""}
        if args.rosters_verified or ver_mode:
            stamp["rosters_verified"] = {
                "date": stamp["date"],
                "mode": ver_mode or "forced",
                "sources": args.rosters_verified or "scripts/verify_rosters.py"}
        with open(FRESH_PATH, "w", encoding="utf-8") as f:
            json.dump(stamp, f, indent=2)
        print(f"Freshness stamped: {stamp['date']} — {stamp['note']} "
              f"(pool complete: {len(MUST_HAVE)} consensus names present"
              + (f"; rosters verified: {stamp['rosters_verified']['mode']}"
                 if "rosters_verified" in stamp
                 else "; rosters NOT verified (--force)")
              + ")")
    else:
        info = read_freshness()
        if info:
            print(f"Last refresh: {info.get('date')} — {info.get('note', '')}")
        else:
            print("Never refreshed.")
        check_freshness()


# --------------------------------------------------------------------------
# Data loading and valuation
# --------------------------------------------------------------------------

NUMERIC_COLS = ("fg_pct", "fga", "ft_pct", "fta",
                "tpm", "pts", "reb", "ast", "stl", "blk", "tov")


def load_players():
    with open(DATA_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows, 2):  # row 1 is the header
        for k in NUMERIC_COLS:
            try:
                r[k] = float(r[k])
            except (TypeError, ValueError):
                # SKILL.md §9 has the operator editing this file between
                # turns; a bare float() raised a traceback naming neither the
                # row nor the column (audit F53). `validate` catches it too,
                # since it loads the pool the same way.
                sys.exit(f"data/players.csv row {i} "
                         f"({r.get('player') or '?'}): column {k!r} is "
                         f"{r.get(k)!r}, not a number. Fix that cell — every "
                         "command, draft turn included, loads this file.")
    return rows


DRAFTABLE = 156  # 12 teams x 13 rounds — the draftable universe


def zscores(players):
    """Attach per-category z-scores, standardized over the DRAFTABLE pool.

    Codified 2026-07-30 (9-CAT math audit, findings_2026-07-30): league
    percentage baselines, means, and stds come from the top-156
    draftable fixed point rather than the full pool — the ~90
    sub-replacement rows shifted every baseline by 0.16-0.40 sigma and
    mispriced the top-100 by up to 14 ranks. The fixed-point parameters
    are applied to ALL rows so undrafted players still carry comparable
    z's, and the z-sum's zero sits at replacement level, which is what
    the availability haircut in adj_value taxes.
    """
    def params_over(pool):
        n = len(pool)
        lg_fg = (sum(p["fg_pct"] * p["fga"] for p in pool)
                 / (sum(p["fga"] for p in pool) or 1))
        lg_ft = (sum(p["ft_pct"] * p["fta"] for p in pool)
                 / (sum(p["fta"] for p in pool) or 1))
        stats = {"FG%": [(p["fg_pct"] - lg_fg) * p["fga"] for p in pool],
                 "FT%": [(p["ft_pct"] - lg_ft) * p["fta"] for p in pool]}
        for cat, col in COUNT_COLS.items():
            stats[cat] = [p[col] for p in pool]
        prm = {}
        for cat, vals in stats.items():
            m = sum(vals) / n
            s = math.sqrt(sum((v - m) ** 2 for v in vals) / n) or 1.0
            prm[cat] = (m, s)
        return lg_fg, lg_ft, prm

    def apply(lg_fg, lg_ft, prm):
        for p in players:
            p["_fg_imp"] = (p["fg_pct"] - lg_fg) * p["fga"]
            p["_ft_imp"] = (p["ft_pct"] - lg_ft) * p["fta"]
            vals = {"FG%": p["_fg_imp"], "FT%": p["_ft_imp"]}
            for cat, col in COUNT_COLS.items():
                vals[cat] = p[col]
            p["z"] = {}
            for cat, v in vals.items():
                m, s = prm[cat]
                z = (v - m) / s
                p["z"][cat] = -z if cat == "TO" else z

    # Pass 0 over the full pool seeds the board; then iterate to the
    # top-156-by-value fixed point (audit: converges in one step).
    apply(*params_over(players))
    seen = set()
    for _ in range(5):
        avail = [p for p in players if availability(p) > 0]
        top = sorted(avail, key=lambda p: -total_value(p))[:DRAFTABLE]
        key = frozenset(p["player"] for p in top)
        if key in seen:
            break
        seen.add(key)
        apply(*params_over(top))
    return players


def total_value(p, punt=()):
    return sum(z for cat, z in p["z"].items() if cat not in punt)


def note_tag(note):
    """Leading tag of a note — the machine-readable half. Everything from
    the first space or parenthesis onward is prose for humans (F16/A17;
    unified across all consumers 2026-08-10, R4-F23 — five substring
    parsers had survived the A17 fix)."""
    return re.split(r"[\s(]", (note or "").lower(), 1)[0]


def availability(p):
    """Injury multiplier from the note column (owner's rule).

    out-*        -> 0.0: season-ending; excluded from all boards
    *recovery*   -> 0.0: serious-injury recovery; excluded from all boards
    *risk*       -> 0.78: chronic availability concern; downgraded

    Owner ruling 2026-07-12 (supersedes the same-day 0.60 discount):
    recovery-flagged players are REMOVED from the pool, not priced —
    three live-arena drafts at three slots each stacked the identical
    four discounted recovery stars, and real 2025-26 recovery players
    delivered ~9% of games. No discount polices concentration; exclusion
    does. Re-entry is via the daily refresh: when news confirms a
    returnee is fully back and playing, re-tag `inj-<reason>-risk`
    (first season back) or clear the note — only then are they
    draftable. Risk 0.78 (from 0.85) is arena-calibrated vs real
    2025-26 games played; it stays above the raw realized ratio because
    missed games are partly replaceable via streaming.
    """
    # The status tier is read from the LEADING tag only — everything from the
    # first space or parenthesis onward is prose for humans (audit 2026-08-09,
    # F16). The previous version tested `"recovery" in note` against the whole
    # string and tested it BEFORE `"risk"`, so a note like
    #   inj-achilles-risk (recovery on track)
    # silently deleted the player from every board and every draft candidate
    # list — no warning, no count, just gone. All four re-entered returnees
    # (Haliburton, Lillard, Irving, VanVleet) carry `inj-*-risk (first season
    # back)` parentheticals, one word away from this; Haliburton ranks ~top-12
    # by adjusted value.
    tag = note_tag(p.get("note"))
    if tag.startswith("out-"):
        return 0.0
    if tag.endswith("-recovery"):
        return 0.0
    if tag.endswith("-risk") or tag == "risk" or tag == "inj-risk":
        return 0.78
    if "recovery" in tag:
        return 0.0
    if "risk" in tag:
        return 0.78
    return 1.0


def adj_value(p, punt=()):
    """Injury-adjusted value used for ranking boards (never boosts negatives)."""
    tv = total_value(p, punt)
    av = availability(p)
    return tv * av if tv > 0 else tv


def parse_punt(arg):
    if not arg:
        return ()
    valid = {c.upper(): c for c in CATS}
    punts = []
    for raw in arg.split(","):
        key = raw.strip().upper().replace("STL", "ST").replace("TOV", "TO")
        if key not in valid:
            sys.exit(f"Unknown category {raw!r}. Valid: {', '.join(CATS)}")
        punts.append(valid[key])
    return tuple(punts)


# Common nicknames — draft chatter under a pick clock uses these.
NICKNAMES = {
    "sga": "shai gilgeous-alexander", "kat": "karl-anthony towns",
    "jjj": "jaren jackson", "dame": "damian lillard",
    "ant": "anthony edwards", "melo": "lamelo ball",
    "pg13": "paul george", "pg": "paul george", "joker": "nikola jokic",
    "the joker": "nikola jokic", "spida": "donovan mitchell",
    "greek freak": "giannis", "book": "devin booker",
    "klaw": "kawhi leonard", "wemby": "wembanyama",
    "dlo": "d'angelo russell", "naw": "nickeil alexander-walker",
    "kd": "kevin durant", "ad": "anthony davis", "cp3": "chris paul",
    "steph": "stephen curry", "bron": "lebron james",
    "lebron": "lebron james", "zu": "ivica zubac", "fvv": "fred vanvleet",
    "kpj": "kevin porter", "mpj": "michael porter", "og": "og anunoby",
    "jdub": "jalen williams", "scoot": "scoot henderson",
}


NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def fold(s):
    """Lowercase and strip diacritics: Jokić → jokic, Şengün → sengun.

    Live feeds are pasted from Yahoo/ESPN/NBA.com, which render accents the
    pool does not carry. Audit 2026-08-09 (F27): eight accented names matched
    nothing, were logged as UNKNOWN, and the board went on recommending them
    as available. Both pools are pure ASCII, so folding changes nothing for
    names already in them.
    """
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower())
                   if not unicodedata.combining(c))


def surname_key(name):
    """Last name-bearing token, ignoring a trailing suffix.

    Audit 2026-08-09 (F22): keying the fuzzy stage on the raw last token made
    "jr" the key for 14 players, so typo tolerance was dead for all of them —
    and "jacksn" resolved to a single candidate, GG Jackson, logging silently
    in place of Jaren Jackson Jr.
    """
    parts = [t for t in fold(name).replace(".", "").split()
             if t not in NAME_SUFFIXES]
    return parts[-1] if parts else ""


def match_candidates(players, query):
    """All plausible matches for a name. Priority: exact full name >
    nickname > exact word (first/last name) > substring > fuzzy (typo
    tolerance: Siakim→Siakam) — so 'Ayton' hits Deandre Ayton, never
    P-ayton Pritchard, and 'Hart' hits Josh Hart, not Hartenstein."""
    import difflib
    q = fold(query.strip())
    # draft_state_48 follow-up: pasted names often carry a trailing team tag
    # — "Mikal Bridges (PHX)", "Wembanyama (SAS)" — from Yahoo/ESPN/Sleeper.
    # Strip a trailing parenthetical so the paste still resolves; keep the
    # original if the parens were the whole string.
    q = re.sub(r"\s*\([^)]*\)\s*$", "", q).strip() or q
    q = NICKNAMES.get(q, q)
    # Degenerate segments never match (audit 2026-08-09, F02). A lone '.',
    # '-', apostrophe, or an empty `my:` used to reach the substring stage,
    # match most of the pool, and log the best remaining player as a
    # CONFIRMED pick — '.' logged Jaren Jackson Jr., a bare `my:` logged
    # Wembanyama to the owner's own slot. Nickname resolution runs first so
    # two-letter nicknames (kd, ad, og, zu) still work.
    # Real name tokens are exempt (audit 2026-08-10, R4-F06): seven pool
    # players' actual first names are two letters — CJ, GG, Ja, AJ, PJ, RJ,
    # VJ — and the bare length guard rejected all of them as junk. Any query
    # exactly matching a legitimate >=2-char alphabetic token of a pool name
    # passes to the normal match stages.
    name_tokens = {t for p in players
                   for t in fold(p["player"]).replace(".", "").split()
                   if len(t) >= 2 and t.isalpha()}
    if (len(q) < 3 or not any(c.isalpha() for c in q)) and q not in name_tokens:
        return []
    subs = [p for p in players if fold(p["player"]) == q]
    if not subs:
        subs = [p for p in players
                if q in fold(p["player"]).replace(".", "").split()]
    if not subs:
        subs = [p for p in players if q in fold(p["player"])]
    if not subs:  # first-name prefix + surname: "d white" -> Derrick White,
        # "ky george" -> Kyshawn George. The tool's own shared-surname hint
        # ("first initial + surname") relied on this and silently matched
        # nothing before (draft_state_46). Surname is exact and the first name
        # must start with the prefix, so it stays specific: "d white" is
        # Derrick, never Coby.
        toks = q.split()
        if len(toks) == 2:
            pre, sur = toks
            subs = [p for p in players
                    if surname_key(p["player"]) == sur
                    and fold(p["player"]).split()[0].startswith(pre)]
    if not subs:  # typo fallback: fuzzy, SURNAME-only, first letter must
        # agree (Collins never becomes Rollins; Siakim still finds Siakam)
        hits = set()
        for p in players:
            last = surname_key(p["player"])
            if q[:1] == last[:1] and difflib.get_close_matches(
                    q, [last], n=1, cutoff=0.8):
                hits.add(p["player"])
        subs = [p for p in players if p["player"] in hits]
    if not subs and "," in q:
        # Yahoo player tables sort "Last, First" — "Bridges, Mikal". As a
        # final fallback, swap a single comma-separated pair and retry.
        parts = [s.strip() for s in q.split(",")]
        if len(parts) == 2 and all(parts):
            subs = match_candidates(players, parts[1] + " " + parts[0])
    return subs


def match_player(players, query, taken=None):
    subs = match_candidates(players, query)
    if not subs:
        sys.exit(f"No player matching {query!r}. Try `find {query}`.")
    if len(subs) > 1:
        names = ", ".join(p["player"] for p in subs[:6])
        sys.exit(f"Ambiguous {query!r}: {names}. Be more specific.")
    p = subs[0]
    if taken is not None and p["player"] in taken:
        sys.exit(f"{p['player']} is already off the board.")
    return p


# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------

def fmt_row(p, punt=(), rank=None):
    zs = " ".join(f"{cat}:{p['z'][cat]:+.1f}" for cat in CATS if cat not in punt)
    head = f"{rank:>3}. " if rank else ""
    note = f"  [{p['note']}]" if p.get("note") else ""
    shown = adj_value(p, punt)
    marker = "*" if shown != total_value(p, punt) else " "
    return (f"{head}{p['player']:<24} {p['team']:<3} {p['pos']:<6} "
            f"val {shown:+6.2f}{marker}  {zs}{note}")


def print_profile(players_subset, punt=(), label="Roster"):
    if not players_subset:
        print("(no players)")
        return
    print(f"{label} — {len(players_subset)} players; category z totals "
          f"(punting: {', '.join(punt) or 'nothing'})\n")
    totals = {cat: sum(p["z"][cat] for p in players_subset) for cat in CATS}
    for cat in CATS:
        t = totals[cat]
        tag = " (punted)" if cat in punt else ""
        bar = "#" * min(20, int(abs(t) * 2))
        sign = "+" if t >= 0 else "-"
        print(f"  {cat:<5} {t:+6.2f}  {sign}{bar}{tag}")
    kept = [c for c in CATS if c not in punt]
    strong = sorted(kept, key=lambda c: -totals[c])[:3]
    weak = sorted(kept, key=lambda c: totals[c])[:3]
    print(f"\n  strongest: {', '.join(strong)}   weakest: {', '.join(weak)}")


# --------------------------------------------------------------------------
# Standalone analysis commands
# --------------------------------------------------------------------------

def cmd_rank(args, players):
    punt = parse_punt(args.punt)
    pool = [p for p in players if availability(p) > 0]
    dropped = len(players) - len(pool)
    if args.pos:
        pool = [p for p in pool if args.pos.upper() in p["pos"].upper()]
    pool = sorted(pool, key=lambda p: -adj_value(p, punt))
    print(f"Rankings (punting: {', '.join(punt) or 'nothing'}"
          + (f"; position: {args.pos.upper()}" if args.pos else "")
          + (f"; {dropped} unavailable (out/recovery) excluded" if dropped else "")
          + ")\n* = injury-adjusted value\n")
    for i, p in enumerate(pool[:args.top], 1):
        print(fmt_row(p, punt, rank=i))


def cmd_profile(args, players):
    punt = parse_punt(args.punt)
    subset = [match_player(players, name) for name in args.players.split(",")]
    print_profile(subset, punt)


def cmd_trade(args, players):
    punt = parse_punt(args.punt)
    send = [match_player(players, n) for n in args.send.split(",")]
    get = [match_player(players, n) for n in args.get.split(",")]
    print("Trade evaluation (z-score deltas for YOUR team; + = you improve)\n")
    print(f"  send: {', '.join(p['player'] for p in send)}")
    print(f"  get:  {', '.join(p['player'] for p in get)}\n")
    net = 0.0
    for cat in CATS:
        delta = sum(p["z"][cat] for p in get) - sum(p["z"][cat] for p in send)
        tag = " (punted — ignore)" if cat in punt else ""
        if cat not in punt:
            net += delta
        print(f"  {cat:<5} {delta:+6.2f}{tag}")
    print(f"\n  net value: {net:+.2f} "
          f"({'you win on raw value' if net > 0 else 'you lose raw value' if net < 0 else 'even'};"
          " weigh roster fit and category needs on top of this)")


def cmd_find(args, players):
    q = args.query.strip().lower()
    hits = [p for p in players if q in p["player"].lower()]
    if not hits:
        print(f"No players matching {args.query!r} in data/players.csv "
              "(pool is the top ~210; add rows for deeper players).")
        return
    for p in sorted(hits, key=lambda p: -total_value(p)):
        print(fmt_row(p))


# --------------------------------------------------------------------------
# Draft state and commands
# --------------------------------------------------------------------------

def load_state():
    if not os.path.isfile(STATE_PATH):
        sys.exit("No draft in progress here. Start one: draft init --teams 12 --slot 5")
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        bak = STATE_PATH + ".bak"
        hint = (f"Restore the pick before last:  cp {bak} {STATE_PATH}"
                if os.path.isfile(bak) else
                'No .bak found — rebuild from the draft room:  '
                'draft resync "Name; Name; my:Name; ..."')
        sys.exit(f"⚠ DRAFT STATE CORRUPT — {STATE_PATH}: {e}\n{hint}")


def save_state(state):
    """Atomic write, keeping one generation of backup (audit 2026-08-09, F55).

    The previous version truncated the live state file in place, so an
    interrupted write mid-draft was the one way to produce the corrupt file
    load_state now reports — with nothing to fall back to.
    """
    if os.path.isfile(STATE_PATH):
        try:
            with open(STATE_PATH, encoding="utf-8") as src, \
                    open(STATE_PATH + ".bak", "w", encoding="utf-8") as dst:
                dst.write(src.read())
        except OSError:
            pass  # a failed backup must never block logging the pick itself
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, STATE_PATH)


def is_unknown(pk):
    return str(pk["player"]).upper().startswith("UNKNOWN")


def unknown_picks(state, slot=None):
    """Pick numbers standing in as UNKNOWN placeholders, optionally one slot."""
    return [i + 1 for i, pk in enumerate(state["picks"])
            if is_unknown(pk) and (slot is None or pk["slot"] == slot)]


def picks_owned(state, slot):
    """True pick count for a slot, INCLUDING UNKNOWN placeholders.

    Audit 2026-08-09 (F29): build_rosters drops UNKNOWNs, so every
    roster-derived number silently under-counted for the rest of the draft —
    a 7-pick roster printed "roster 3/13" and the feasibility guard reported
    "6 picks left" with 2 remaining.
    """
    return sum(1 for pk in state["picks"] if pk["slot"] == slot)


def team_of_pick(n, teams):
    """Which slot owns 0-based overall pick n in a snake draft."""
    rnd, idx = divmod(n, teams)
    return idx + 1 if rnd % 2 == 0 else teams - idx


def normalize_picks(state):
    """Accept legacy string picks; store {player, slot} objects."""
    teams = state["teams"]
    state["picks"] = [
        pk if isinstance(pk, dict) else
        {"player": pk, "slot": team_of_pick(i, teams)}
        for i, pk in enumerate(state["picks"])
    ]
    return state


def my_next_pick(state):
    """Next overall pick that belongs to my slot, or None once the draft is
    over — it used to count on into rounds that do not exist (audit F52)."""
    teams, slot = state["teams"], state["slot"]
    for n in range(len(state["picks"]), teams * state["size"]):
        if team_of_pick(n, teams) == slot:
            return n + 1
    return None


def next_pick_label(state):
    n = my_next_pick(state)
    return f"#{n}" if n else "— none left, draft complete"


def positions_of(p):
    return [s.strip() for s in p["pos"].replace('"', "").split(",")]


def build_rosters(state, players):
    by_name = {p["player"]: p for p in players}
    rosters = {slot: [] for slot in range(1, state["teams"] + 1)}
    stray = set()
    for pk in state["picks"]:
        p = by_name.get(pk["player"])  # UNKNOWN placeholders are skipped
        if p is None:
            continue
        if pk["slot"] not in rosters:  # out-of-range slot: degrade, never
            stray.add(pk["slot"])      # crash mid-draft (audit F30)
            continue
        rosters[pk["slot"]].append(p)
    if stray:
        print(f"⚠ picks logged to slot(s) {sorted(stray)} outside 1-"
              f"{state['teams']} are excluded — fix with: draft fix N "
              '"Name" --slot K', file=sys.stderr)
    return rosters


def roster_totals(roster):
    return {cat: sum(p["z"][cat] for p in roster) for cat in CATS}


def my_category_ranks(state, players):
    """My rank per category across all teams (1 = best; TO already inverted)."""
    rosters = build_rosters(state, players)
    totals = {slot: roster_totals(r) for slot, r in rosters.items()}
    mine = totals[state["slot"]]
    return {cat: 1 + sum(1 for s, t in totals.items()
                         if s != state["slot"] and t[cat] > mine[cat])
            for cat in CATS}, totals


def insert_pick(state, players, P, name):
    """Insert a MISSED pick at 1-indexed #P and shift #P..end down one,
    recomputing snake slots positionally. Mutates state['picks'] and returns an
    echo string. Raises ValueError(msg) on any refuse condition. Everything
    downstream (rosters, category ranks, board) re-derives from state['picks'],
    so a canonical picks array is the whole job. Owner decisions 2026-08-24:
    refuse-and-route to RESYNC on any keeper/trade (non-snake) board; callers
    snapshot before calling."""
    picks = state["picks"]
    teams = state["teams"]
    maxp = teams * state["size"]
    if not 1 <= P <= maxp:
        raise ValueError(f"insert #{P} out of range (1-{maxp}).")
    if len(picks) >= maxp:
        raise ValueError(f"draft is full ({maxp} picks) — nothing to insert; fix "
                         'a slot with draft fix N "Name", or RESYNC.')
    if P > len(picks) + 1:
        raise ValueError(f"insert #{P}: only {len(picks)} pick(s) logged — insert "
                         f"at #{len(picks) + 1} or earlier (no mid-air gaps), or RESYNC.")
    manual = [i + 1 for i, pk in enumerate(picks)
              if pk["slot"] != team_of_pick(i, teams)]
    if manual:
        raise ValueError(f"insert refused: pick(s) {manual} carry a non-snake slot "
                         "(keeper/trade/out-of-order); a positional re-shift would "
                         'corrupt them. Rebuild with: draft resync "<full list>".')
    if name.upper().startswith("UNKNOWN"):
        resolved = name
    elif not match_candidates(players, name):
        resolved = f"UNKNOWN #{P}"
    else:
        try:
            resolved = match_player(players, name,
                                    taken={pk["player"] for pk in picks})["player"]
        except SystemExit as e:            # match_player exits on ambiguous/taken
            raise ValueError(str(e))
    idx = P - 1
    picks.insert(idx, {"player": resolved, "slot": team_of_pick(idx, teams)})
    for i in range(idx, len(picks)):       # re-derive snake slots for the shifted tail
        picks[i]["slot"] = team_of_pick(i, teams)
    shifted = len(picks) - 1 - idx
    tail = (f"; #{P}–#{len(picks) - 1} → #{P + 1}–#{len(picks)} "
            f"({shifted} shifted, slots recomputed)") if shifted else ""
    return f"✎ inserted {resolved} at #{P} → Team {picks[idx]['slot']}{tail}"


def cmd_draft(args, players):
    if args.draft_cmd == "init":
        if os.path.isfile(STATE_PATH) and not args.force:
            sys.exit(f"{STATE_PATH} already exists — add --force to restart.")
        if args.teams < 2 or args.size < 1:
            sys.exit("--teams must be >= 2 and --size >= 1.")
        if not 1 <= args.slot <= args.teams:
            sys.exit(f"--slot must be between 1 and {args.teams}.")
        state = {"teams": args.teams, "slot": args.slot, "size": args.size,
                 "punt": list(parse_punt(args.punt)), "picks": []}
        save_state(state)
        total = args.teams * args.size
        print(f"Draft started: {args.teams} teams x {args.size} rounds = "
              f"{total} total picks (last pick #{total}), you pick from "
              f"slot {args.slot}, punting: "
              f"{', '.join(state['punt']) or 'nothing'}.")
        print("CONFIRM the teams x rounds product with the owner before "
              "pick 1 (ledger lesson #7).")
        print(f"State: {os.path.abspath(STATE_PATH)}")
        return

    state = normalize_picks(load_state())
    # RESYNC (SKILL.md §4): wipe the board and rebuild it from a pasted pick
    # list. The keyword was in the protocol with no mechanism behind it, so
    # the sequence had to be improvised live (audit F36). Snake attribution
    # re-derives positionally, so `my:` markers are optional in a complete
    # in-order paste. The prior board survives in draft_state.json.bak.
    resync_prior = None
    if args.draft_cmd == "resync":
        # Audit 2026-08-10 (R4-F01, critical): resync saves twice in one
        # command, so the one-generation .bak ended up holding the WIPED
        # board while the message promised the prior one survived — an empty
        # paste destroyed a live draft irrecoverably. The prior board now
        # goes to a dedicated one-shot file BEFORE anything is cleared, an
        # empty paste is refused outright, and the 3-correction rollback
        # snapshot is the PRE-wipe board, so a halted resync restores the
        # original board instead of an empty one.
        segs = [s for s in (args.picks or "").split(";") if s.strip()]
        if not segs:
            sys.exit("RESYNC refused: 0 parsed names in the paste — nothing "
                     "was cleared and the board is untouched. Paste the "
                     "room's pick list, semicolon-separated.")
        resync_prior = [dict(pk) for pk in state["picks"]]
        pre_path = STATE_PATH + ".pre-resync"
        with open(pre_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        prior = len(state["picks"])
        state["picks"] = []
        save_state(state)
        print(f"RESYNC: cleared {prior} logged pick(s); rebuilding from the "
              f"paste. Prior board saved to {os.path.abspath(pre_path)} — "
              f"restore with: cp {os.path.abspath(pre_path)} "
              f"{os.path.abspath(STATE_PATH)}")
        args.draft_cmd = "turn"

    picks = state["picks"]
    taken = {pk["player"] for pk in picks}
    punt = tuple(state["punt"])
    teams, myslot = state["teams"], state["slot"]

    if args.draft_cmd == "pick":
        if args.slot and not 1 <= args.slot <= teams:
            sys.exit(f"--slot must be between 1 and {teams}.")
        if len(picks) >= teams * state["size"]:
            sys.exit(f"Draft is complete — {len(picks)} of "
                     f"{teams * state['size']} picks logged. Nothing more to "
                     'append; correct a pick with: draft fix N "Name"')
        p = match_player(players, args.player, taken=taken)
        if availability(p) == 0.0:
            print(f"warning: {p['player']} is flagged unavailable "
                  f"({p.get('note')}) — logging the pick anyway.")
        n = len(picks)
        derived = team_of_pick(n, teams)
        slot = args.slot or (myslot if args.mine else derived)
        if args.mine and derived != myslot and not args.slot:
            print(f"note: snake order says pick {n + 1} belongs to Team "
                  f"{derived}; logging to you (Team {myslot}) anyway. Use "
                  "--slot for other out-of-order picks (keepers, trades).")
        picks.append({"player": p["player"], "slot": slot})
        save_state(state)
        rnd = n // teams + 1
        you = " (YOU)" if slot == myslot else ""
        tail = "" if slot == myslot else f"  Your next pick: {next_pick_label(state)}"
        print(f"Pick {n + 1} (round {rnd}): {p['player']} → Team {slot}{you}.{tail}")

    elif args.draft_cmd == "undo":
        if not picks:
            sys.exit("Nothing to undo.")
        last = picks.pop()
        save_state(state)
        print(f"Undid: {last['player']} (Team {last['slot']})")

    elif args.draft_cmd == "fix":
        idx = args.number - 1
        if not 0 <= idx < len(picks):
            sys.exit(f"Pick #{args.number} not logged yet ({len(picks)} picks).")
        # --slot is validated for BOTH branches before anything is written:
        # the UNKNOWN branch used to skip the range check, persisting a bad
        # slot that detonated as an unhandled KeyError in build_rosters the
        # moment the placeholder was fixed to a real player (audit F30).
        if args.slot and not 1 <= args.slot <= teams:
            sys.exit(f"--slot must be between 1 and {teams}.")
        # Copy, don't alias: printing old["player"] after mutating the same
        # dict showed the NEW name on both sides of the arrow, so the
        # before/after echo SKILL.md §5 mandates could never verify a
        # mistyped pick number (audit F31).
        old = dict(picks[idx])
        if args.player.upper().startswith("UNKNOWN"):
            # out-of-pool player: keep attribution with a labeled placeholder
            picks[idx]["player"] = args.player
            if args.slot:
                picks[idx]["slot"] = args.slot
            save_state(state)
            print(f"✎ #{args.number}: {old['player']} → {args.player} "
                  f"(T{picks[idx]['slot']}, out-of-pool placeholder)")
            return
        others = {pk["player"] for i, pk in enumerate(picks) if i != idx}
        p = match_player(players, args.player, taken=others)
        picks[idx]["player"] = p["player"]
        if args.slot:
            picks[idx]["slot"] = args.slot
        save_state(state)
        print(f"✎ #{args.number}: {old['player']} → {p['player']} "
              f"(T{picks[idx]['slot']})")

    elif args.draft_cmd == "insert":
        prior = [dict(pk) for pk in picks]   # snapshot the pre-insert board
        try:
            msg = insert_pick(state, players, args.number, args.player)
        except ValueError as e:
            sys.exit(str(e))                 # refused: nothing changed, no snapshot written
        pre_path = STATE_PATH + ".pre-insert"
        with open(pre_path, "w", encoding="utf-8") as f:
            json.dump({**state, "picks": prior}, f, indent=2)
        save_state(state)
        print(f"{msg}. Prior board saved to {os.path.abspath(pre_path)} "
              f"(restore: cp {os.path.abspath(pre_path)} {os.path.abspath(STATE_PATH)}).")

    elif args.draft_cmd == "best":
        pool = [p for p in players
                if p["player"] not in taken and availability(p) > 0]
        if args.pos:
            pool = [p for p in pool if args.pos.upper() in p["pos"].upper()]
        override = parse_punt(args.punt) if args.punt else punt
        pool = sorted(pool, key=lambda p: -adj_value(p, override))
        # Annotate how each candidate helps my weakest kept categories.
        mine = build_rosters(state, players)[myslot]
        weakest = []
        if mine:
            totals = roster_totals(mine)
            kept = [c for c in CATS if c not in override]
            weakest = sorted(kept, key=lambda c: totals[c])[:2]
        print(f"Best available (punting: {', '.join(override) or 'nothing'}"
              + (f"; position: {args.pos.upper()}" if args.pos else "")
              + f") — your next pick is {next_pick_label(state)}"
              + (f"; your weakest kept cats: {', '.join(weakest)}" if weakest else "")
              + "\n")
        for i, p in enumerate(pool[:args.top], 1):
            line = fmt_row(p, override, rank=i)
            if weakest:
                good = [c for c in weakest if p["z"][c] > 0]
                bad = [c for c in weakest if p["z"][c] <= 0]
                if good:
                    line += "   helps " + " ".join(
                        f"{c}:{p['z'][c]:+.1f}" for c in good)
                if bad:
                    line += "   hurts " + " ".join(
                        f"{c}:{p['z'][c]:+.1f}" for c in bad)
            print(line)

    elif args.draft_cmd == "rosters":
        rosters = build_rosters(state, players)
        for slot in range(1, teams + 1):
            r = rosters[slot]
            you = " (YOU)" if slot == myslot else ""
            val = sum(total_value(p, punt) for p in r)
            names = ", ".join(p["player"] for p in r) or "(no picks yet)"
            print(f"Team {slot}{you} — kept-cat value {val:+.1f}: {names}")

    elif args.draft_cmd == "matrix":
        ranks, totals = my_category_ranks(state, players)
        header = "TEAM      " + "".join(f"{c:>7}" for c in CATS) + "    KEPT"
        print(f"Category z-totals by team (TO inverted: higher is better; "
              f"you are Team {myslot})\n\n{header}")
        for slot in range(1, teams + 1):
            t = totals[slot]
            kept = sum(v for c, v in t.items() if c not in punt)
            star = "*" if slot == myslot else " "
            print(f"T{slot:<2}{star}      "
                  + "".join(f"{t[c]:>+7.1f}" for c in CATS)
                  + f"  {kept:>+7.1f}")
        kept_cats = [c for c in CATS if c not in punt]
        print("\nYour rank: " + "  ".join(
            f"{c} {ranks[c]}/{teams}" for c in kept_cats))
        winning = [c for c in kept_cats if ranks[c] <= max(1, teams // 3)]
        losing = [c for c in kept_cats if ranks[c] > teams - teams // 3]
        print(f"leading: {', '.join(winning) or '-'}   "
              f"trailing: {', '.join(losing) or '-'}"
              + (f"   punted: {', '.join(punt)}" if punt else ""))

    elif args.draft_cmd == "vs":
        if not 1 <= args.team <= teams or args.team == myslot:
            sys.exit(f"--team must be an opponent slot between 1 and {teams}.")
        rosters = build_rosters(state, players)
        a, b = roster_totals(rosters[myslot]), roster_totals(rosters[args.team])
        wins = losses = 0
        print(f"You (Team {myslot}) vs Team {args.team} — category z-totals\n")
        for cat in CATS:
            tag = " (punted)" if cat in punt else ""
            lead = "you" if a[cat] > b[cat] else ("them" if b[cat] > a[cat] else "tied")
            if cat not in punt and a[cat] != b[cat]:
                wins += lead == "you"
                losses += lead == "them"
            print(f"  {cat:<5} you {a[cat]:+6.2f}  them {b[cat]:+6.2f}  → {lead}{tag}")
        print(f"\nKept categories: you lead {wins}–{losses}")

    elif args.draft_cmd == "turn":
        if args.expect is not None and args.expect != len(picks):
            tail = ", ".join(f"#{len(picks)-i} {pk['player']}"
                             for i, pk in enumerate(reversed(picks[-3:])))
            sys.exit(f"⚠ STATE MISMATCH: {len(picks)} picks logged, you "
                     f"expected {args.expect}. Last: {tail}. Nothing was "
                     "logged — reconcile, then resend only unlogged names.")
        # One-shot live-draft turn: log all announced picks, then emit the
        # full decision card. Leading pick numbers ("77- Name", "Pick 77,
        # Name") are authoritative: a number matching an existing pick is a
        # correction; a number past the next slot back-fills UNKNOWN
        # placeholders so snake attribution never drifts. A name that fails
        # to match logs an UNKNOWN placeholder (fix later: draft fix N
        # "Name") instead of silently shifting every later pick.
        import re
        errors = []
        corrections = 0
        # Rollback point for the 3-correction drift halt. During a resync the
        # snapshot is the PRE-wipe board (R4-F01): a halted resync must
        # restore the original board, not the freshly-emptied one.
        snapshot = (resync_prior if resync_prior is not None
                    else [dict(pk) for pk in picks])
        max_pick = teams * state["size"]
        for raw in [s.strip() for s in (args.picks or "").split(";") if s.strip()]:
            mi = re.match(r"^(?:pick\s*)?#?(\d+)\s*\+\s*(.+)$", raw)  # insert token: "108+ Queta"
            if mi:
                ibody = mi.group(2).strip()
                iname = ibody[3:].strip() if ibody.lower().startswith("my:") else ibody
                try:
                    print("  " + insert_pick(state, players, int(mi.group(1)), iname))
                except ValueError as e:
                    errors.append(str(e))
                    continue
                taken = {pk["player"] for pk in picks}  # tail shifted — rebuild taken set
                continue
            # A leading pick number may be separated from the name by a
            # punctuation mark OR just whitespace: "44- Herro", "44 Herro",
            # "pick 75 Mikal Bridges" all mean pick N. Space-only used to fall
            # through as a literal, unmatchable query — draft_state_48: typing
            # "75 Mikal Bridges" logged five straight UNKNOWNs mid-draft.
            m = re.match(r"^(?:pick\s*)?#?(\d+)(?:\s*[-—.,:]\s*|\s+)(.+)$", raw, re.I)
            num, body = (int(m.group(1)), m.group(2).strip()) if m else (None, raw)
            mine = body.lower().startswith("my:")
            name = body[3:].strip() if mine else body

            if num is not None and not 1 <= num <= max_pick:
                errors.append(f"ignored {raw!r}: pick number out of range "
                              f"(1-{max_pick})")
                continue

            if num is not None and num <= len(picks):  # explicit correction
                idx = num - 1
                old = picks[idx]["player"]
                others = {pk["player"] for i, pk in enumerate(picks) if i != idx}
                try:
                    p = match_player(players, name, taken=others)
                except SystemExit as e:
                    errors.append(f"fix #{num}: {e}")
                    continue
                if p["player"] == picks[idx]["player"]:
                    print(f"  ✓ #{num} unchanged ({p['player']})")
                    continue
                corrections += 1
                if corrections >= 3:
                    state["picks"] = snapshot
                    save_state(state)
                    sys.exit(f"⚠ HALTED at {raw!r}: 3+ corrections in one "
                             "batch suggests numbering drift, not fixes. "
                             "NO changes from this batch were applied. Run "
                             "`draft status`, verify against the draft room, "
                             "then resend the whole batch.")
                picks[idx]["player"] = p["player"]
                taken.discard(old)
                taken.add(p["player"])
                print(f"  ✎ #{num} corrected: {old} → {p['player']}")
                continue

            while num is not None and len(picks) + 1 < num:  # gap: back-fill
                g = len(picks)
                picks.append({"player": f"UNKNOWN #{g + 1}",
                              "slot": team_of_pick(g, teams)})
                print(f"  ⚠ #{g + 1} UNKNOWN (gap) — fill with: "
                      f"draft fix {g + 1} \"Name\"")

            if len(picks) >= max_pick:  # audit F52: no phantom round 14
                errors.append(f"ignored {name!r}: draft is already complete "
                              f"({max_pick} picks logged)")
                continue

            n = len(picks)
            slot = myslot if mine else team_of_pick(n, teams)
            # A my: that lands off the snake permanently transfers a pick from
            # a rival to the owner and corrupts both rosters plus every
            # vs-field line. `draft pick --mine` has always warned; the
            # one-command live path did not (audit F32). --expect cannot see
            # it — a misattributed my: leaves the pick COUNT correct.
            if mine and team_of_pick(n, teams) != myslot:
                errors.append(
                    f"#{n + 1} logged to YOU, but snake order says Team "
                    f"{team_of_pick(n, teams)} — verify before your next turn "
                    f'(draft fix {n + 1} "Name" --slot K)')
            # Ambiguity auto-resolves by draft context: the best available
            # candidate is who gets drafted at this point; flag the guess.
            all_c = match_candidates(players, name)
            cands = [c for c in all_c if c["player"] not in taken]
            exact = [c for c in cands
                     if c["player"].lower() == name.strip().lower()]
            best_all = max(all_c, key=adj_value) if all_c else None
            if len(cands) > 1 and not exact and best_all and \
                    best_all["player"] in taken:
                # Surname collision with 2+ still AVAILABLE: the best match is
                # drafted and more than one namesake remains, so we can't tell
                # which — logging a lesser candidate caused the Coby/Dejounte
                # misattributions. HALT so numbering stays true. When exactly
                # one namesake is left it is unambiguous (see below), so a bare
                # "George" after two Georges are gone logs the third instead of
                # halting (draft_state_46: pick 109 died on this).
                save_state(state)
                alts = ", ".join(c["player"] for c in cands[:3])
                sys.exit(f"⚠ HALTED at {name!r}: best match "
                         f"{best_all['player']} is already drafted. If you "
                         f"meant {alts}, resend the REST of this feed using "
                         "the fuller name. Nothing after this name was "
                         "logged.")
            if cands:
                p = exact[0] if exact else max(cands, key=adj_value)
                picks.append({"player": p["player"], "slot": slot})
                taken.add(p["player"])
                you = " (YOU)" if slot == myslot else ""
                note = ""
                losers = [c["player"] for c in cands if c is not p]
                gone = [c["player"] for c in all_c
                        if c["player"] in taken and c["player"] != p["player"]]
                if losers:
                    more = f" +{len(losers) - 2} more" if len(losers) > 2 else ""
                    note = f"  (assumed over {', '.join(losers[:2])}{more})"
                    if len(cands) > 4:  # audit F02: a broad query still
                        note += "  ⚠ WIDE MATCH — verify"  # resolves, loudly
                elif gone and not exact:
                    # resolved a shared surname to the last one still available
                    note = (f"  (only {p['player'].split()[0]} left; "
                            f"{', '.join(gone[:2])} already drafted)")
                print(f"  ✓ #{n + 1} R{n // teams + 1}: {p['player']} → "
                      f"T{slot}{you}{note}")
            elif all_c:
                # every match already drafted: duplicate feed — skip, no pick
                errors.append(f"skipped {name!r}: already off the board "
                              "(no pick logged)")
            else:
                picks.append({"player": f"UNKNOWN #{n + 1}", "slot": slot})
                errors.append(f"#{n + 1} logged as UNKNOWN ({name!r}: no match)"
                              f" — fix with: draft fix {n + 1} \"Name\"")
        save_state(state)
        for e in errors:
            print(f"  ⚠ {e}")

        rosters = build_rosters(state, players)
        mine_r = rosters[myslot]
        override = parse_punt(args.punt) if args.punt else punt
        kept = [c for c in CATS if c not in override]
        weakest = []
        if mine_r:
            totals = roster_totals(mine_r)
            weakest = sorted(kept, key=lambda c: totals[c])[:2]

        pool = [p for p in players
                if p["player"] not in taken and availability(p) > 0]
        if args.pos:
            pool = [p for p in pool if args.pos.upper() in p["pos"].upper()]
        pool.sort(key=lambda p: -adj_value(p, override))

        owned = picks_owned(state, myslot)
        my_unknown = unknown_picks(state, myslot)
        print(f"\nYOUR PICK: {next_pick_label(state)} | roster {owned}/{state['size']}"
              + (f" | weakest: {', '.join(weakest)}" if weakest else "")
              + (f" | punting: {', '.join(override)}" if override else ""))
        # The UNKNOWN warning used to print once, in the batch where it
        # happened, and never again — so the phantom roster spots stayed
        # invisible for the rest of the draft (audit F29).
        if my_unknown:
            print(f"⚠ {len(my_unknown)} of YOUR picks are UNKNOWN "
                  f"(#{', #'.join(str(u) for u in my_unknown)}) — the counts, "
                  "position tally and category ranks below EXCLUDE them. Fix: "
                  'draft fix N "Name"')
        pos_counts = {}
        for p in mine_r:
            for ps in positions_of(p):
                pos_counts[ps] = pos_counts.get(ps, 0) + 1
        if pos_counts:
            print("your positions: " + " ".join(
                f"{k}:{v}" for k, v in sorted(pos_counts.items())))
        # Feasibility guard (council rule): position only hard-matters when a
        # required slot could become unfillable with the picks remaining.
        # Maximum bipartite matching of the roster onto POSITIONAL_SLOTS —
        # one player per slot, multi-position players assigned where needed.
        slot_match = {}  # roster index -> slot index

        def _augment(si, seen):
            for pi, pl in enumerate(mine_r):
                if pi in seen or not any(
                        e in positions_of(pl)
                        for e in POSITIONAL_SLOTS[si][1]):
                    continue
                seen.add(pi)
                if pi not in slot_match or _augment(slot_match[pi], seen):
                    slot_match[pi] = si
                    return True
            return False

        unfilled = [POSITIONAL_SLOTS[si][0]
                    for si in range(len(POSITIONAL_SLOTS))
                    if not _augment(si, set())]
        remaining = state["size"] - owned  # true count, UNKNOWNs included
        if unfilled and remaining - len(unfilled) <= 2:
            print(f"⚠ FEASIBILITY: open slots {'/'.join(unfilled)}, "
                  f"{remaining} picks left — cover these soon")
        # Owner soft rules (subordinate to winning potential):
        # NBA-team stacking cap (avoid 3+ from one team) and position lean.
        team_counts = {}
        for p in mine_r:
            team_counts[p["team"]] = team_counts.get(p["team"], 0) + 1
        stacked = {k: v for k, v in team_counts.items() if v >= 2}
        if stacked:
            print("NBA-team stacks: " + " ".join(
                f"{k}:{v}" for k, v in sorted(stacked.items())))
        g_ct = pos_counts.get("PG", 0) + pos_counts.get("SG", 0)
        f_ct = pos_counts.get("SF", 0) + pos_counts.get("PF", 0)
        if len(mine_r) >= 5 and abs(g_ct - f_ct) >= 4:
            lean = f"{f_ct}F vs {g_ct}G" if f_ct > g_ct else f"{g_ct}G vs {f_ct}F"
            print(f"⚠ LEAN: {lean} — flag for roster balance")
        print()
        for i, p in enumerate(pool[:args.top], 1):
            line = fmt_row(p, override, rank=i)
            # "helps" must only name categories the player actually helps
            # (audit 2026-08-09, F65): it printed every weak category with its
            # raw z, so a candidate who makes your worst category WORSE read as
            # "helps BLK:-0.7". Negatives are now labelled as what they are.
            if weakest:
                good = [c for c in weakest if p["z"][c] > 0]
                bad = [c for c in weakest if p["z"][c] <= 0]
                if good:
                    line += "   helps " + " ".join(
                        f"{c}:{p['z'][c]:+.1f}" for c in good)
                if bad:
                    line += "   hurts " + " ".join(
                        f"{c}:{p['z'][c]:+.1f}" for c in bad)
            if team_counts.get(p["team"], 0) >= 2:
                line += f"  [would be 3rd {p['team']}]"
            print(line)

        if mine_r:
            ranks, tots = my_category_ranks(state, players)
            print("\nvs field: " + "  ".join(
                f"{c}:{ranks[c]}" for c in kept))
            rival = max((s for s in tots if s != myslot),
                        key=lambda s: sum(v for c, v in tots[s].items()
                                          if c not in override))
            edge = [c for c in kept if tots[myslot][c] > tots[rival][c]]
            print(f"top rival: T{rival} — you lead them in "
                  f"{len(edge)}/{len(kept)} kept cats "
                  f"({', '.join(edge) or 'none'})")

    elif args.draft_cmd == "status":
        overall = len(picks)
        rnd = overall // teams + 1
        print(f"Draft: {overall} picks made (round {rnd} of {state['size']}), "
              f"your next pick: {next_pick_label(state)}\n")
        if args.tail:
            print(f"Last {min(args.tail, overall)} picks (the SYNC tail):")
            for i in range(max(0, overall - args.tail), overall):
                pk = picks[i]
                you = " (YOU)" if pk["slot"] == myslot else ""
                print(f"  #{i + 1} R{i // teams + 1}: {pk['player']} "
                      f"→ T{pk['slot']}{you}")
            print()
        stray = unknown_picks(state)
        if stray:
            print(f"⚠ {len(stray)} UNKNOWN placeholder(s) on the board: "
                  f"#{', #'.join(str(u) for u in stray)}\n")
        mine = build_rosters(state, players)[myslot]
        owned = picks_owned(state, myslot)
        if not mine:
            print(f"Your roster: empty ({owned} picks logged)."
                  if owned else "Your roster: empty.")
            return
        slots = ", ".join(sorted({p["pos"] for p in mine}))
        gap = (f" + {owned - len(mine)} UNKNOWN"
               if owned > len(mine) else "")
        print(f"Your roster ({len(mine)}{gap}): "
              + ", ".join(p["player"] for p in mine) + f"  [{slots}]\n")
        print_profile(mine, punt, label="Your build")
        ranks, _ = my_category_ranks(state, players)
        kept_cats = [c for c in CATS if c not in punt]
        print("\n  vs field:  " + "  ".join(
            f"{c} {ranks[c]}/{teams}" for c in kept_cats))


def build_parser():
    p = argparse.ArgumentParser(prog="hoops.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("rank", help="overall rankings")
    r.add_argument("--punt", help="categories to punt, e.g. FT%%,TO")
    r.add_argument("--pos", help="filter by position, e.g. C")
    r.add_argument("--top", type=int, default=30)

    pr = sub.add_parser("profile", help="category profile of a player set")
    pr.add_argument("--players", required=True, help='comma-separated names')
    pr.add_argument("--punt")

    t = sub.add_parser("trade", help="evaluate a trade")
    t.add_argument("--send", required=True, help='players you give, comma-separated')
    t.add_argument("--get", required=True, help='players you receive')
    t.add_argument("--punt")

    f = sub.add_parser("find", help="look up players by name fragment")
    f.add_argument("query")

    sub.add_parser("validate", help="check pool for missing consensus players")

    fr = sub.add_parser("freshness", help="show or stamp the daily data refresh")
    fr.add_argument("--stamp", action="store_true",
                    help="record that data was refreshed today")
    fr.add_argument("--note", help="what was updated in this refresh")
    fr.add_argument("--rosters-verified", metavar="SOURCES",
                    help="record that team assignments were cross-referenced "
                         "against NBA/ESPN transaction records this pull "
                         "(required for --stamp; the roster validation lock)")
    fr.add_argument("--force", action="store_true",
                    help="stamp even if the pool validator finds missing names "
                         "or rosters are unverified (state the reason in --note)")
    pc = fr.add_mutually_exclusive_group()
    pc.add_argument("--pool-changes", metavar="DESC",
                    help="assert this pull CHANGED data/players.csv, and why "
                         "(build gate 4 reads this, R4-F22)")
    pc.add_argument("--no-pool-changes", action="store_true",
                    help="deliberately assert this pull changed nothing in "
                         "data/players.csv (the quiet-day path; a keyword in "
                         "the prose note no longer counts)")

    d = sub.add_parser("draft", help="live draft tracker")
    dsub = d.add_subparsers(dest="draft_cmd", required=True)

    di = dsub.add_parser("init", help="start a draft")
    di.add_argument("--teams", type=int, default=12)
    di.add_argument("--slot", type=int, required=True, help="your draft position (1-based)")
    di.add_argument("--size", type=int, default=13,
                    help="rounds/roster size (owner's league: 13)")
    di.add_argument("--punt", help="planned punt categories")
    di.add_argument("--force", action="store_true", help="overwrite existing draft")

    dp = dsub.add_parser("pick", help="log a pick (team inferred from snake order)")
    dp.add_argument("player")
    dp.add_argument("--mine", action="store_true",
                    help="assert this pick is yours (sanity-checks snake order)")
    dp.add_argument("--slot", type=int,
                    help="override the picking team (keepers, traded picks)")

    dsub.add_parser("undo", help="take back the last pick")

    df = dsub.add_parser("fix", help='correct any logged pick: fix 44 "Herro"')
    df.add_argument("number", type=int, help="pick number to correct")
    df.add_argument("player")
    df.add_argument("--slot", type=int, help="also reassign the team slot")

    din = dsub.add_parser("insert",
                          help='insert a MISSED pick and shift the rest down: '
                               'insert 108 "Queta"')
    din.add_argument("number", type=int, help="1-indexed position to insert at")
    din.add_argument("player")

    db = dsub.add_parser("best", help="best available, need-annotated")
    db.add_argument("--pos")
    db.add_argument("--punt", help="override the draft's punt setting")
    db.add_argument("--top", type=int, default=12)

    dt = dsub.add_parser("turn",
                         help="ONE-SHOT: log picks + full decision card")
    dt.add_argument("picks", nargs="?", default="",
                    help='semicolon-separated names in draft order; '
                         'prefix your own with "my:", e.g. '
                         '"Jokic; my:Booker; Curry"')
    dt.add_argument("--top", type=int, default=8)
    dt.add_argument("--pos")
    dt.add_argument("--punt", help="override the draft's punt setting")
    dt.add_argument("--expect", type=int,
                    help="picks already logged; abort with a state tail if "
                         "reality differs (re-send safety after a lost result)")

    dr = dsub.add_parser("resync",
                         help="wipe the board and rebuild it from a pasted "
                              "pick list (SKILL.md §4 RESYNC)")
    dr.add_argument("picks", nargs="?", default="",
                    help="semicolon-separated names in draft order")
    dr.add_argument("--top", type=int, default=8)
    dr.add_argument("--pos")
    dr.add_argument("--punt")
    dr.set_defaults(expect=None)

    ds = dsub.add_parser("status",
                         help="your roster, build profile, rank vs field")
    ds.add_argument("--tail", type=int, metavar="N", default=0,
                    help="also print the last N picks (the SYNC tail)")
    dsub.add_parser("rosters", help="every team's roster so far")
    dsub.add_parser("matrix", help="category z-totals for all teams + your ranks")

    dv = dsub.add_parser("vs", help="head-to-head category comparison vs one opponent")
    dv.add_argument("--team", type=int, required=True, help="opponent slot number")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "freshness":
        cmd_freshness(args)
        return
    if args.command == "validate":
        missing = validate_pool(load_players())
        if missing:
            print("⚠ POOL INCOMPLETE — missing: " + ", ".join(missing))
            sys.exit(1)
        print(f"pool complete: all {len(MUST_HAVE)} consensus names present")
        return
    # Speed rule: live-draft commands never print the stale banner (a draft
    # is no time to refresh data). Staleness is enforced at `draft init`.
    if args.command != "draft" or args.draft_cmd == "init":
        check_freshness()
    players = zscores(load_players())
    if args.command == "rank":
        cmd_rank(args, players)
    elif args.command == "profile":
        cmd_profile(args, players)
    elif args.command == "trade":
        cmd_trade(args, players)
    elif args.command == "find":
        cmd_find(args, players)
    elif args.command == "draft":
        cmd_draft(args, players)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:  # output piped to head etc. — not an error
        sys.exit(0)
