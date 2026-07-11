#!/usr/bin/env python3
"""hoops — in-Claude fantasy basketball analyzer and draft tool.

No accounts, no APIs. Player projections live in data/players.csv (editable);
this script turns them into 9-cat z-score values and provides:

    rank            Overall rankings, punt-aware:  rank --punt FT%,TO
    profile         Category strengths of a set of players (a roster)
    trade           Evaluate a trade:  trade --send "A,B" --get "C"
    find            Look up players by name fragment
    draft init      Start a draft:  draft init --teams 12 --slot 5
    draft pick      Log a pick:  draft pick "Jokic"   (add --mine for yours)
    draft best      Best available, punt- and need-aware
    draft status    Round/pick, your roster, category profile
    draft undo      Take back the last logged pick

Categories: FG%, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO (TO inverted).
Percentage categories are volume-weighted (impact = (pct - league pct) * attempts).
Values are z-scores over the player pool: +1.0 = one standard deviation better
than average in that category. State for a live draft sits in ./draft_state.json.
"""

import argparse
import csv
import json
import math
import os
import sys

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "data", "players.csv")
STATE_PATH = os.environ.get("HOOPS_DRAFT_STATE", "draft_state.json")

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
COUNT_COLS = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast",
              "ST": "stl", "BLK": "blk", "TO": "tov"}


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


def match_player(players, query, taken=None):
    q = query.strip().lower()
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
    return (f"{head}{p['player']:<24} {p['team']:<3} {p['pos']:<6} "
            f"val {total_value(p, punt):+6.2f}   {zs}{note}")


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
    pool = players
    if args.pos:
        pool = [p for p in pool if args.pos.upper() in p["pos"].upper()]
    pool = sorted(pool, key=lambda p: -total_value(p, punt))
    print(f"Rankings (punting: {', '.join(punt) or 'nothing'}"
          + (f"; position: {args.pos.upper()}" if args.pos else "") + ")\n")
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


def my_next_pick(state):
    """Next overall pick number that belongs to my slot (snake order)."""
    teams, slot = state["teams"], state["slot"]
    n = len(state["picks"])
    while True:
        rnd, idx = divmod(n, teams)
        pick_slot = idx + 1 if rnd % 2 == 0 else teams - idx
        if pick_slot == slot:
            return n + 1
        n += 1


def cmd_draft(args, players):
    if args.draft_cmd == "init":
        if os.path.isfile(STATE_PATH) and not args.force:
            sys.exit(f"{STATE_PATH} already exists — add --force to restart.")
        state = {"teams": args.teams, "slot": args.slot, "size": args.size,
                 "punt": list(parse_punt(args.punt)), "picks": [], "mine": []}
        save_state(state)
        print(f"Draft started: {args.teams} teams, you pick from slot {args.slot}, "
              f"{args.size} rounds, punting: {', '.join(state['punt']) or 'nothing'}.")
        print(f"State: {os.path.abspath(STATE_PATH)}")
        return

    state = load_state()
    taken = set(state["picks"])
    punt = tuple(state["punt"])

    if args.draft_cmd == "pick":
        p = match_player(players, args.player, taken=taken)
        state["picks"].append(p["player"])
        if args.mine:
            state["mine"].append(p["player"])
        save_state(state)
        overall = len(state["picks"])
        rnd = (overall - 1) // state["teams"] + 1
        who = "YOU" if args.mine else "someone"
        print(f"Pick {overall} (round {rnd}): {p['player']} → {who}. "
              f"{'Your next pick: #' + str(my_next_pick(state)) if not args.mine else ''}")

    elif args.draft_cmd == "undo":
        if not state["picks"]:
            sys.exit("Nothing to undo.")
        last = state["picks"].pop()
        if state["mine"] and state["mine"][-1] == last:
            state["mine"].pop()
        save_state(state)
        print(f"Undid: {last}")

    elif args.draft_cmd == "best":
        pool = [p for p in players if p["player"] not in taken]
        if args.pos:
            pool = [p for p in pool if args.pos.upper() in p["pos"].upper()]
        override = parse_punt(args.punt) if args.punt else punt
        pool = sorted(pool, key=lambda p: -total_value(p, override))
        print(f"Best available (punting: {', '.join(override) or 'nothing'}"
              + (f"; position: {args.pos.upper()}" if args.pos else "")
              + f") — your next pick is #{my_next_pick(state)}\n")
        for i, p in enumerate(pool[:args.top], 1):
            print(fmt_row(p, override, rank=i))

    elif args.draft_cmd == "status":
        overall = len(state["picks"])
        rnd = overall // state["teams"] + 1
        print(f"Draft: {overall} picks made (round {rnd} of {state['size']}), "
              f"your next pick: #{my_next_pick(state)}\n")
        mine = [match_player(players, n) for n in state["mine"]]
        if mine:
            slots = ", ".join(sorted({p["pos"] for p in mine}))
            print(f"Your roster ({len(mine)}): "
                  + ", ".join(p["player"] for p in mine) + f"  [{slots}]\n")
            print_profile(mine, punt, label="Your build")
        else:
            print("Your roster: empty.")


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

    d = sub.add_parser("draft", help="live draft tracker")
    dsub = d.add_subparsers(dest="draft_cmd", required=True)

    di = dsub.add_parser("init", help="start a draft")
    di.add_argument("--teams", type=int, default=12)
    di.add_argument("--slot", type=int, required=True, help="your draft position (1-based)")
    di.add_argument("--size", type=int, default=13, help="rounds/roster size")
    di.add_argument("--punt", help="planned punt categories")
    di.add_argument("--force", action="store_true", help="overwrite existing draft")

    dp = dsub.add_parser("pick", help="log a pick")
    dp.add_argument("player")
    dp.add_argument("--mine", action="store_true", help="this pick is yours")

    dsub.add_parser("undo", help="take back the last pick")

    db = dsub.add_parser("best", help="best available")
    db.add_argument("--pos")
    db.add_argument("--punt", help="override the draft's punt setting")
    db.add_argument("--top", type=int, default=12)

    dsub.add_parser("status", help="draft state, your roster and build")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
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
