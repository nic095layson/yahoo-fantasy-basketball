#!/usr/bin/env python3
"""hoops — in-Claude fantasy basketball analyzer and draft tool.

No accounts, no APIs. Player projections live in data/players.csv (editable);
this script turns them into 9-cat z-score values and provides:

    rank            Overall rankings, punt-aware:  rank --punt FT%,TO
    profile         Category strengths of a set of players (a roster)
    trade           Evaluate a trade:  trade --send "A,B" --get "C"
    find            Look up players by name fragment
    draft init      Start a draft:  draft init --teams 12 --slot 5
    draft pick      Log a pick — the picking team is inferred from snake
                    order, so every team's roster builds automatically
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
import sys

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "players.csv")
FRESH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "data", "freshness.json")
STATE_PATH = os.environ.get("HOOPS_DRAFT_STATE", "draft_state.json")

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


def cmd_freshness(args):
    if args.stamp:
        stamp = {"date": datetime.date.today().isoformat(),
                 "note": args.note or "refreshed"}
        with open(FRESH_PATH, "w", encoding="utf-8") as f:
            json.dump(stamp, f, indent=2)
        print(f"Freshness stamped: {stamp['date']} — {stamp['note']}")
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

def load_players():
    with open(DATA_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("fg_pct", "fga", "ft_pct", "fta",
                  "tpm", "pts", "reb", "ast", "stl", "blk", "tov"):
            r[k] = float(r[k])
    return rows


def zscores(players):
    """Attach per-category z-scores and a punt-independent value dict."""
    n = len(players)

    def mean_std(vals):
        m = sum(vals) / n
        var = sum((v - m) ** 2 for v in vals) / n
        return m, math.sqrt(var) or 1.0

    # Volume-weighted percentage impact
    lg_fg = sum(p["fg_pct"] * p["fga"] for p in players) / sum(p["fga"] for p in players)
    lg_ft = sum(p["ft_pct"] * p["fta"] for p in players) / sum(p["fta"] for p in players)
    for p in players:
        p["_fg_imp"] = (p["fg_pct"] - lg_fg) * p["fga"]
        p["_ft_imp"] = (p["ft_pct"] - lg_ft) * p["fta"]

    stats = {"FG%": [p["_fg_imp"] for p in players],
             "FT%": [p["_ft_imp"] for p in players]}
    for cat, col in COUNT_COLS.items():
        stats[cat] = [p[col] for p in players]

    for cat, vals in stats.items():
        m, s = mean_std(vals)
        for p, v in zip(players, vals):
            z = (v - m) / s
            p.setdefault("z", {})[cat] = -z if cat == "TO" else z
    return players


def total_value(p, punt=()):
    return sum(z for cat, z in p["z"].items() if cat not in punt)


def availability(p):
    """Injury multiplier from the note column (owner's rule).

    out-*        -> 0.0: season-ending; excluded from all boards
    *recovery*   -> 0.7: returning from serious injury; value downgraded
    *risk*       -> 0.85: chronic availability concern; mild downgrade
    """
    note = (p.get("note") or "").lower()
    if note.startswith("out") or "out-for-season" in note:
        return 0.0
    if "recovery" in note:
        return 0.7
    if "risk" in note:
        return 0.85
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
    "pg13": "paul george", "joker": "nikola jokic",
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


def match_player(players, query, taken=None):
    q = query.strip().lower()
    q = NICKNAMES.get(q, q)
    exact = [p for p in players if p["player"].lower() == q]
    subs = exact or [p for p in players if q in p["player"].lower()]
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
          + (f"; {dropped} out-for-season excluded" if dropped else "")
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
              "(pool is the top ~125; add rows for deeper players).")
        return
    for p in sorted(hits, key=lambda p: -total_value(p)):
        print(fmt_row(p))


# --------------------------------------------------------------------------
# Draft state and commands
# --------------------------------------------------------------------------

def load_state():
    if not os.path.isfile(STATE_PATH):
        sys.exit("No draft in progress here. Start one: draft init --teams 12 --slot 5")
    with open(STATE_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


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
    """Next overall pick number that belongs to my slot (snake order)."""
    teams, slot = state["teams"], state["slot"]
    n = len(state["picks"])
    while True:
        if team_of_pick(n, teams) == slot:
            return n + 1
        n += 1


def positions_of(p):
    return [s.strip() for s in p["pos"].replace('"', "").split(",")]


def build_rosters(state, players):
    by_name = {p["player"]: p for p in players}
    rosters = {slot: [] for slot in range(1, state["teams"] + 1)}
    for pk in state["picks"]:
        rosters[pk["slot"]].append(by_name[pk["player"]])
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


def cmd_draft(args, players):
    if args.draft_cmd == "init":
        if os.path.isfile(STATE_PATH) and not args.force:
            sys.exit(f"{STATE_PATH} already exists — add --force to restart.")
        state = {"teams": args.teams, "slot": args.slot, "size": args.size,
                 "punt": list(parse_punt(args.punt)), "picks": []}
        save_state(state)
        print(f"Draft started: {args.teams} teams, you pick from slot {args.slot}, "
              f"{args.size} rounds, punting: {', '.join(state['punt']) or 'nothing'}.")
        print(f"State: {os.path.abspath(STATE_PATH)}")
        return

    state = normalize_picks(load_state())
    picks = state["picks"]
    taken = {pk["player"] for pk in picks}
    punt = tuple(state["punt"])
    teams, myslot = state["teams"], state["slot"]

    if args.draft_cmd == "pick":
        p = match_player(players, args.player, taken=taken)
        if availability(p) == 0.0:
            print(f"warning: {p['player']} is marked OUT for the season "
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
        tail = "" if slot == myslot else f"  Your next pick: #{my_next_pick(state)}"
        print(f"Pick {n + 1} (round {rnd}): {p['player']} → Team {slot}{you}.{tail}")

    elif args.draft_cmd == "undo":
        if not picks:
            sys.exit("Nothing to undo.")
        last = picks.pop()
        save_state(state)
        print(f"Undid: {last['player']} (Team {last['slot']})")

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
              + f") — your next pick is #{my_next_pick(state)}"
              + (f"; your weakest kept cats: {', '.join(weakest)}" if weakest else "")
              + "\n")
        for i, p in enumerate(pool[:args.top], 1):
            line = fmt_row(p, override, rank=i)
            if weakest:
                line += "   helps " + " ".join(
                    f"{c}:{p['z'][c]:+.1f}" for c in weakest)
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
        # One-shot live-draft turn: log all announced picks, then emit the
        # full decision card. Bad names are reported, never fatal.
        errors = []
        for raw in [s.strip() for s in (args.picks or "").split(";") if s.strip()]:
            mine = raw.lower().startswith("my:")
            name = raw[3:].strip() if mine else raw
            try:
                p = match_player(players, name, taken=taken)
            except SystemExit as e:
                errors.append(str(e))
                continue
            n = len(picks)
            slot = myslot if mine else team_of_pick(n, teams)
            picks.append({"player": p["player"], "slot": slot})
            taken.add(p["player"])
            you = " (YOU)" if slot == myslot else ""
            print(f"  ✓ #{n + 1} R{n // teams + 1}: {p['player']} → T{slot}{you}")
        save_state(state)
        for e in errors:
            print(f"  ⚠ NOT LOGGED: {e}")

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

        print(f"\nYOUR PICK: #{my_next_pick(state)} | roster {len(mine_r)}/{state['size']}"
              + (f" | weakest: {', '.join(weakest)}" if weakest else "")
              + (f" | punting: {', '.join(override)}" if override else ""))
        pos_counts = {}
        for p in mine_r:
            for ps in positions_of(p):
                pos_counts[ps] = pos_counts.get(ps, 0) + 1
        if pos_counts:
            print("your positions: " + " ".join(
                f"{k}:{v}" for k, v in sorted(pos_counts.items())))
        print()
        for i, p in enumerate(pool[:args.top], 1):
            line = fmt_row(p, override, rank=i)
            if weakest:
                line += "   helps " + " ".join(
                    f"{c}:{p['z'][c]:+.1f}" for c in weakest)
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
              f"your next pick: #{my_next_pick(state)}\n")
        mine = build_rosters(state, players)[myslot]
        if not mine:
            print("Your roster: empty.")
            return
        slots = ", ".join(sorted({p["pos"] for p in mine}))
        print(f"Your roster ({len(mine)}): "
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

    fr = sub.add_parser("freshness", help="show or stamp the daily data refresh")
    fr.add_argument("--stamp", action="store_true",
                    help="record that data was refreshed today")
    fr.add_argument("--note", help="what was updated in this refresh")

    d = sub.add_parser("draft", help="live draft tracker")
    dsub = d.add_subparsers(dest="draft_cmd", required=True)

    di = dsub.add_parser("init", help="start a draft")
    di.add_argument("--teams", type=int, default=12)
    di.add_argument("--slot", type=int, required=True, help="your draft position (1-based)")
    di.add_argument("--size", type=int, default=15, help="rounds/roster size")
    di.add_argument("--punt", help="planned punt categories")
    di.add_argument("--force", action="store_true", help="overwrite existing draft")

    dp = dsub.add_parser("pick", help="log a pick (team inferred from snake order)")
    dp.add_argument("player")
    dp.add_argument("--mine", action="store_true",
                    help="assert this pick is yours (sanity-checks snake order)")
    dp.add_argument("--slot", type=int,
                    help="override the picking team (keepers, traded picks)")

    dsub.add_parser("undo", help="take back the last pick")

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

    dsub.add_parser("status", help="your roster, build profile, rank vs field")
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
    main()
