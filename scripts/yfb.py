#!/usr/bin/env python3
"""yfb — Yahoo Fantasy Basketball CLI.

A single-file, stdlib-only client for the Yahoo Fantasy Sports API (NBA),
designed to be driven by Claude Code via the `fantasy-basketball` skill.

Commands:
    auth            Run the OAuth2 authorization-code flow and cache tokens.
    leagues         List your NBA fantasy leagues for the active season.
    standings       League standings (requires --league).
    roster          Your team's roster (requires --team, or --league to resolve it).
    matchup         Current-week head-to-head matchup (requires --team).
    free-agents     Top available free agents (requires --league).
    status          Show auth/config state without calling the API.

Global flags:
    --demo          Use bundled sample data instead of the live API. No
                    credentials needed; useful for testing and demos.
    --json          Emit raw JSON instead of formatted tables (for piping).

Credentials (create an app at https://developer.yahoo.com/apps/ with
Fantasy Sports read scope):
    env  YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET, or
    file ~/.config/yfb/credentials.json  {"client_id": "...", "client_secret": "..."}

Token cache: ~/.config/yfb/token.json (chmod 600, auto-refreshed).
"""

import argparse
import base64
import json
import os
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://fantasysports.yahooapis.com/fantasy/v2"
AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
# Must match the Redirect URI registered on the Yahoo app. The browser will
# fail to load this address after approval — the code is in the address bar.
REDIRECT_URI = os.environ.get("YFB_REDIRECT_URI", "https://localhost:8080")
CONFIG_DIR = os.path.expanduser(os.environ.get("YFB_CONFIG_DIR", "~/.config/yfb"))
TOKEN_PATH = os.path.join(CONFIG_DIR, "token.json")
CREDS_PATH = os.path.join(CONFIG_DIR, "credentials.json")
NBA_GAME_CODE = "nba"


# --------------------------------------------------------------------------
# Credentials and token cache
# --------------------------------------------------------------------------

def load_credentials():
    cid = os.environ.get("YAHOO_CLIENT_ID")
    csec = os.environ.get("YAHOO_CLIENT_SECRET")
    if cid and csec:
        return cid, csec
    if os.path.isfile(CREDS_PATH):
        with open(CREDS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("client_id") and data.get("client_secret"):
            return data["client_id"], data["client_secret"]
    return None, None


def save_private_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def load_token():
    if os.path.isfile(TOKEN_PATH):
        with open(TOKEN_PATH, encoding="utf-8") as f:
            return json.load(f)
    return None


def token_request(payload, cid, csec):
    basic = base64.b64encode(f"{cid}:{csec}".encode()).decode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=urllib.parse.urlencode(payload).encode(),
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        tok = json.load(resp)
    tok["obtained_at"] = int(time.time())
    save_private_json(TOKEN_PATH, tok)
    return tok


def get_access_token():
    cid, csec = load_credentials()
    if not (cid and csec):
        sys.exit(
            "No Yahoo API credentials found.\n"
            "Set YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET or create "
            f"{CREDS_PATH}\n"
            "Create an app (Fantasy Sports, read) at https://developer.yahoo.com/apps/"
        )
    tok = load_token()
    if tok is None:
        sys.exit("Not authorized yet. Run: yfb.py auth")
    expires_at = tok.get("obtained_at", 0) + int(tok.get("expires_in", 3600))
    if time.time() > expires_at - 120:
        tok = token_request(
            {"grant_type": "refresh_token",
             "refresh_token": tok["refresh_token"],
             "redirect_uri": REDIRECT_URI},
            cid, csec,
        )
    return tok["access_token"]


def cmd_auth(_args):
    cid, csec = load_credentials()
    if not (cid and csec):
        sys.exit(
            "Missing credentials. Set YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET "
            f"or create {CREDS_PATH} first."
        )
    url = AUTH_URL + "?" + urllib.parse.urlencode(
        {"client_id": cid, "redirect_uri": REDIRECT_URI, "response_type": "code"}
    )
    print("1. Open this URL in a browser, sign in, and click Agree:\n")
    print(f"   {url}\n")
    print(f"2. Your browser will then try to load {REDIRECT_URI} and show a")
    print("   'can't connect' error page. That is EXPECTED — the code you need")
    print("   is in the address bar, after `code=`.")
    raw = input("3. Paste the full URL from the address bar (or just the code): ").strip()
    if not raw:
        sys.exit("No code entered; aborting.")
    if "code=" in raw:
        query = urllib.parse.urlparse(raw).query or raw
        code = urllib.parse.parse_qs(query).get("code", [raw])[0]
    else:
        code = raw
    token_request(
        {"grant_type": "authorization_code", "code": code,
         "redirect_uri": REDIRECT_URI},
        cid, csec,
    )
    print(f"\nAuthorized. Token cached at {TOKEN_PATH}")


# --------------------------------------------------------------------------
# Yahoo API access and JSON un-nesting
# --------------------------------------------------------------------------

def api_get(path):
    """GET an API path (relative to API_BASE) and return parsed JSON."""
    token = get_access_token()
    sep = "&" if "?" in path else "?"
    url = f"{API_BASE}/{path}{sep}format=json"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        sys.exit(f"Yahoo API error {e.code} for {url}\n{body}")


def merge_fragments(node):
    """Yahoo represents one object as a list of single-key dicts; merge them."""
    if isinstance(node, dict):
        return node
    merged = {}
    for frag in node or []:
        if isinstance(frag, dict):
            merged.update(frag)
    return merged


def iter_collection(node):
    """Yield items from a Yahoo collection dict keyed by "0", "1", ... + "count"."""
    if not isinstance(node, dict):
        return
    for key in sorted(node, key=lambda k: int(k) if k.isdigit() else -1):
        if key.isdigit():
            yield node[key]


# --------------------------------------------------------------------------
# Live-data fetchers (each returns plain, simplified structures)
# --------------------------------------------------------------------------

def fetch_leagues():
    raw = api_get(f"users;use_login=1/games;game_keys={NBA_GAME_CODE}/leagues")
    leagues = []
    users = raw["fantasy_content"]["users"]
    for user_wrap in iter_collection(users):
        user = merge_fragments(user_wrap["user"])
        for game_wrap in iter_collection(user.get("games", {})):
            game = merge_fragments(game_wrap["game"])
            for league_wrap in iter_collection(game.get("leagues", {})):
                lg = merge_fragments(league_wrap["league"])
                leagues.append({
                    "league_key": lg.get("league_key"),
                    "name": lg.get("name"),
                    "num_teams": lg.get("num_teams"),
                    "scoring_type": lg.get("scoring_type"),
                    "current_week": lg.get("current_week"),
                    "season": lg.get("season"),
                })
    return leagues


def fetch_standings(league_key):
    raw = api_get(f"league/{league_key}/standings")
    league = merge_fragments(raw["fantasy_content"]["league"])
    rows = []
    teams = merge_fragments(league.get("standings", [])).get("teams", {})
    for team_wrap in iter_collection(teams):
        team = merge_fragments(team_wrap["team"][0] if isinstance(team_wrap["team"][0], list) else team_wrap["team"])
        # team payload is [ [fragments...], {"team_standings": ...} ]
        parts = team_wrap["team"]
        info = merge_fragments(parts[0]) if isinstance(parts[0], list) else merge_fragments(parts)
        standings = {}
        for part in parts[1:]:
            if isinstance(part, dict) and "team_standings" in part:
                standings = part["team_standings"]
        outcome = standings.get("outcome_totals", {})
        rows.append({
            "rank": standings.get("rank"),
            "team": info.get("name"),
            "team_key": info.get("team_key"),
            "wins": outcome.get("wins"),
            "losses": outcome.get("losses"),
            "ties": outcome.get("ties"),
            "pct": outcome.get("percentage"),
        })
    rows.sort(key=lambda r: int(r["rank"] or 99))
    return {"league": league.get("name"), "rows": rows}


def _simplify_player(parts):
    info = merge_fragments(parts[0]) if parts and isinstance(parts[0], list) else merge_fragments(parts)
    name = info.get("name", {})
    extra = {}
    for part in parts[1:] if isinstance(parts, list) else []:
        if isinstance(part, dict):
            extra.update(part)
    pos = extra.get("selected_position")
    if pos:
        pos = merge_fragments(pos).get("position")
    ownership = extra.get("percent_owned")
    if isinstance(ownership, list):
        ownership = merge_fragments(ownership).get("value")
    return {
        "player_key": info.get("player_key"),
        "name": name.get("full") if isinstance(name, dict) else name,
        "team": info.get("editorial_team_abbr"),
        "positions": info.get("display_position"),
        "status": info.get("status", ""),
        "slot": pos,
        "percent_owned": ownership,
    }


def fetch_roster(team_key):
    raw = api_get(f"team/{team_key}/roster/players")
    team = merge_fragments(raw["fantasy_content"]["team"][0])
    roster = raw["fantasy_content"]["team"][1]["roster"]
    players = merge_fragments(roster).get("0", {}).get("players", {}) \
        if isinstance(roster, dict) and "0" in roster else merge_fragments(roster).get("players", {})
    out = []
    for player_wrap in iter_collection(players):
        out.append(_simplify_player(player_wrap["player"]))
    return {"team": team.get("name"), "team_key": team_key, "players": out}


def fetch_matchup(team_key):
    raw = api_get(f"team/{team_key}/matchups")
    parts = raw["fantasy_content"]["team"]
    info = merge_fragments(parts[0])
    matchups = merge_fragments(parts[1:]).get("matchups", {})
    current = None
    for m_wrap in iter_collection(matchups):
        m = m_wrap.get("matchup", {})
        if str(m.get("status")) in ("midevent", "preevent"):
            current = m
            break
        current = m  # fall back to the last one seen
    if current is None:
        return {"team": info.get("name"), "matchup": None}
    sides = []
    teams = merge_fragments(current.get("0", current)).get("teams", {})
    for t_wrap in iter_collection(teams):
        t_parts = t_wrap["team"]
        t_info = merge_fragments(t_parts[0])
        stats = {}
        for part in t_parts[1:]:
            if isinstance(part, dict) and "team_stats" in part:
                for s_wrap in iter_collection(part["team_stats"].get("stats", {})):
                    s = s_wrap.get("stat", {})
                    stats[s.get("stat_id")] = s.get("value")
        sides.append({"team": t_info.get("name"), "stats": stats})
    return {
        "team": info.get("name"),
        "week": current.get("week"),
        "status": current.get("status"),
        "sides": sides,
    }


def fetch_free_agents(league_key, count=15, sort="AR"):
    raw = api_get(
        f"league/{league_key}/players;status=FA;sort={sort};count={count}"
        ";out=percent_owned"
    )
    league = merge_fragments(raw["fantasy_content"]["league"])
    players = {}
    for part in raw["fantasy_content"]["league"]:
        if isinstance(part, dict) and "players" in part:
            players = part["players"]
    out = []
    for player_wrap in iter_collection(players):
        out.append(_simplify_player(player_wrap["player"]))
    return {"league": league.get("name"), "players": out}


# --------------------------------------------------------------------------
# Demo data — realistic shapes, no network, no credentials
# --------------------------------------------------------------------------

DEMO = {
    "leagues": [
        {"league_key": "466.l.12345", "name": "Hardwood Heroes", "num_teams": 12,
         "scoring_type": "head", "current_week": 13, "season": "2025"},
        {"league_key": "466.l.67890", "name": "Office Ballers", "num_teams": 10,
         "scoring_type": "roto", "current_week": 13, "season": "2025"},
    ],
    "standings": {
        "league": "Hardwood Heroes",
        "rows": [
            {"rank": 1, "team": "Nikola's Jokers", "team_key": "466.l.12345.t.3", "wins": 78, "losses": 22, "ties": 8, "pct": ".759"},
            {"rank": 2, "team": "Layson's Lakers", "team_key": "466.l.12345.t.1", "wins": 70, "losses": 30, "ties": 8, "pct": ".685"},
            {"rank": 3, "team": "Wemby's World", "team_key": "466.l.12345.t.7", "wins": 66, "losses": 36, "ties": 6, "pct": ".639"},
            {"rank": 4, "team": "Luka Doncic Fan Club", "team_key": "466.l.12345.t.5", "wins": 60, "losses": 42, "ties": 6, "pct": ".583"},
        ],
    },
    "roster": {
        "team": "Layson's Lakers",
        "team_key": "466.l.12345.t.1",
        "players": [
            {"player_key": "466.p.6030", "name": "Luka Doncic", "team": "LAL", "positions": "PG,SG", "status": "", "slot": "PG", "percent_owned": 100},
            {"player_key": "466.p.5768", "name": "Devin Booker", "team": "PHX", "positions": "PG,SG", "status": "", "slot": "SG", "percent_owned": 99},
            {"player_key": "466.p.6407", "name": "Paolo Banchero", "team": "ORL", "positions": "PF,SF", "status": "", "slot": "SF", "percent_owned": 98},
            {"player_key": "466.p.5352", "name": "Anthony Davis", "team": "DAL", "positions": "PF,C", "status": "DTD", "slot": "PF", "percent_owned": 100},
            {"player_key": "466.p.6018", "name": "Chet Holmgren", "team": "OKC", "positions": "PF,C", "status": "", "slot": "C", "percent_owned": 99},
            {"player_key": "466.p.6746", "name": "Amen Thompson", "team": "HOU", "positions": "PG,SF", "status": "", "slot": "G", "percent_owned": 95},
            {"player_key": "466.p.6470", "name": "Jalen Williams", "team": "OKC", "positions": "SG,SF", "status": "", "slot": "F", "percent_owned": 97},
            {"player_key": "466.p.6163", "name": "Alperen Sengun", "team": "HOU", "positions": "C", "status": "", "slot": "UTIL", "percent_owned": 99},
            {"player_key": "466.p.6595", "name": "Jaime Jaquez Jr.", "team": "MIA", "positions": "SF,PF", "status": "", "slot": "BN", "percent_owned": 61},
            {"player_key": "466.p.6828", "name": "Stephon Castle", "team": "SAS", "positions": "PG,SG", "status": "O", "slot": "IL", "percent_owned": 74},
        ],
    },
    "matchup": {
        "team": "Layson's Lakers",
        "week": 13,
        "status": "midevent",
        "sides": [
            {"team": "Layson's Lakers", "stats": {"5": "0.482", "8": "0.815", "10": "41", "12": "312", "15": "118", "16": "72", "17": "21", "18": "14", "19": "38"}},
            {"team": "Wemby's World", "stats": {"5": "0.474", "8": "0.779", "10": "48", "12": "298", "15": "101", "16": "88", "17": "26", "18": "31", "19": "42"}},
        ],
    },
    "free_agents": {
        "league": "Hardwood Heroes",
        "players": [
            {"player_key": "466.p.6902", "name": "Kel'el Ware", "team": "MIA", "positions": "C", "status": "", "slot": None, "percent_owned": 58},
            {"player_key": "466.p.6612", "name": "Keyonte George", "team": "UTA", "positions": "PG,SG", "status": "", "slot": None, "percent_owned": 52},
            {"player_key": "466.p.6580", "name": "Toumani Camara", "team": "POR", "positions": "SF,PF", "status": "", "slot": None, "percent_owned": 49},
            {"player_key": "466.p.6337", "name": "Jose Alvarado", "team": "NOP", "positions": "PG", "status": "DTD", "slot": None, "percent_owned": 31},
            {"player_key": "466.p.6871", "name": "Donovan Clingan", "team": "POR", "positions": "C", "status": "", "slot": None, "percent_owned": 44},
        ],
    },
}

# Stat-id → label map for the 9-cat default (Yahoo NBA stat ids).
STAT_LABELS = {
    "5": "FG%", "8": "FT%", "10": "3PTM", "12": "PTS", "15": "REB",
    "16": "AST", "17": "ST", "18": "BLK", "19": "TO",
}


# --------------------------------------------------------------------------
# Output formatting
# --------------------------------------------------------------------------

def print_table(rows, columns):
    """columns: list of (header, key) pairs."""
    if not rows:
        print("(no rows)")
        return
    widths = [max(len(h), *(len(str(r.get(k, "") or "")) for r in rows))
              for h, k in columns]
    header = "  ".join(h.ljust(w) for (h, _), w in zip(columns, widths))
    print(header)
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(r.get(k, "") or "").ljust(w)
                        for (_, k), w in zip(columns, widths)))


def emit(args, data, render):
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        render(data)


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_status(_args):
    cid, _ = load_credentials()
    tok = load_token()
    print(f"credentials: {'found' if cid else 'MISSING'} "
          f"(env or {CREDS_PATH})")
    if tok:
        expires_at = tok.get("obtained_at", 0) + int(tok.get("expires_in", 3600))
        state = "valid" if time.time() < expires_at else "expired (will auto-refresh)"
        print(f"token:       cached at {TOKEN_PATH} — {state}")
    else:
        print("token:       none — run `yfb.py auth`")


def cmd_leagues(args):
    data = DEMO["leagues"] if args.demo else fetch_leagues()
    emit(args, data, lambda d: print_table(d, [
        ("LEAGUE KEY", "league_key"), ("NAME", "name"), ("TEAMS", "num_teams"),
        ("SCORING", "scoring_type"), ("WEEK", "current_week"), ("SEASON", "season"),
    ]))


def cmd_standings(args):
    data = DEMO["standings"] if args.demo else fetch_standings(args.league)
    def render(d):
        print(f"Standings — {d['league']}\n")
        print_table(d["rows"], [
            ("#", "rank"), ("TEAM", "team"), ("W", "wins"), ("L", "losses"),
            ("T", "ties"), ("PCT", "pct"), ("TEAM KEY", "team_key"),
        ])
    emit(args, data, render)


def cmd_roster(args):
    data = DEMO["roster"] if args.demo else fetch_roster(args.team)
    def render(d):
        print(f"Roster — {d['team']} ({d['team_key']})\n")
        print_table(d["players"], [
            ("SLOT", "slot"), ("PLAYER", "name"), ("NBA", "team"),
            ("POS", "positions"), ("STATUS", "status"), ("OWN%", "percent_owned"),
        ])
    emit(args, data, render)


def cmd_matchup(args):
    data = DEMO["matchup"] if args.demo else fetch_matchup(args.team)
    def render(d):
        if not d.get("sides"):
            print(f"No matchup found for {d['team']}.")
            return
        print(f"Week {d['week']} matchup ({d['status']})\n")
        a, b = d["sides"][0], d["sides"][1]
        stat_ids = [s for s in STAT_LABELS if s in a["stats"] or s in b["stats"]]
        rows = []
        a_wins = b_wins = 0
        for sid in stat_ids:
            av, bv = a["stats"].get(sid, "-"), b["stats"].get(sid, "-")
            try:
                fa, fb = float(av), float(bv)
                lower_is_better = STAT_LABELS[sid] == "TO"
                a_leads = fa < fb if lower_is_better else fa > fb
                lead = a["team"] if a_leads else (b["team"] if fa != fb else "tied")
                if fa != fb:
                    a_wins += a_leads
                    b_wins += not a_leads
            except (TypeError, ValueError):
                lead = "?"
            rows.append({"cat": STAT_LABELS[sid], "a": av, "b": bv, "lead": lead})
        print_table(rows, [
            ("CAT", "cat"), (a["team"], "a"), (b["team"], "b"), ("LEADER", "lead"),
        ])
        print(f"\nCategory score: {a['team']} {a_wins} — {b_wins} {b['team']}")
    emit(args, data, render)


def cmd_free_agents(args):
    data = DEMO["free_agents"] if args.demo else fetch_free_agents(
        args.league, count=args.count, sort=args.sort)
    def render(d):
        print(f"Top free agents — {d['league']}\n")
        print_table(d["players"], [
            ("PLAYER", "name"), ("NBA", "team"), ("POS", "positions"),
            ("STATUS", "status"), ("OWN%", "percent_owned"),
            ("PLAYER KEY", "player_key"),
        ])
    emit(args, data, render)


def build_parser():
    p = argparse.ArgumentParser(prog="yfb.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--demo", action="store_true",
                   help="use bundled sample data (no credentials or network)")
    p.add_argument("--json", action="store_true",
                   help="emit raw JSON instead of tables")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("auth", help="run OAuth2 flow and cache tokens")
    sub.add_parser("status", help="show auth/config state")
    sub.add_parser("leagues", help="list your NBA leagues")

    s = sub.add_parser("standings", help="league standings")
    s.add_argument("--league", required=False, help="league_key, e.g. 466.l.12345")

    r = sub.add_parser("roster", help="team roster")
    r.add_argument("--team", required=False, help="team_key, e.g. 466.l.12345.t.1")

    m = sub.add_parser("matchup", help="current-week matchup")
    m.add_argument("--team", required=False, help="team_key")

    fa = sub.add_parser("free-agents", help="top available free agents")
    fa.add_argument("--league", required=False, help="league_key")
    fa.add_argument("--count", type=int, default=15)
    fa.add_argument("--sort", default="AR",
                    help="AR=actual rank, OR=overall rank, PTS, etc.")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    needs = {"standings": "league", "roster": "team",
             "matchup": "team", "free-agents": "league"}
    key = needs.get(args.command)
    if key and not args.demo and not getattr(args, key, None):
        sys.exit(f"--{key} is required for `{args.command}` "
                 "(or pass --demo for sample data)")
    dispatch = {
        "auth": cmd_auth,
        "status": cmd_status,
        "leagues": cmd_leagues,
        "standings": cmd_standings,
        "roster": cmd_roster,
        "matchup": cmd_matchup,
        "free-agents": cmd_free_agents,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
