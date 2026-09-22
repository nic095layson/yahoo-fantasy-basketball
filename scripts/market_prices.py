#!/usr/bin/env python3
"""Yahoo prices for the deck's Mkt rank — F8 (2026-09-22; owner decision
2026-09-21 "use Yahoo Mkt price"; the 2026-08-21 work order's gated step 5).

Price = Yahoo ADP where Yahoo lists one, else Yahoo XRank, else none. Source:
the newest report/market/yahoo-YYYY-MM-DD.csv in the kit checkout
(player,team,pos,xrank,adp — the owner's dated paste). build_deck bakes the
price into each PLAYERS row (`mkt`, `mktsrc`) and writes data/market-snapshot.csv,
which is what the Python twin (arena.market_ranks) reads for parity. Priced
players rank by price; the internal model orders only the unpriced tail. No
file: the deck falls back to the internal model for everyone, loudly.
"""
import csv
import datetime
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from check_planes import norm, KIT_DEFAULT  # noqa: E402

SNAPSHOT = os.path.join(ROOT, "data", "market-snapshot.csv")
STALE_DAYS = 14
DRIFT_TOP = 120


def newest_yahoo_file(kit_dir=KIT_DEFAULT):
    files = sorted(glob.glob(os.path.join(kit_dir, "report", "market", "yahoo-????-??-??.csv")))
    return files[-1] if files else None


def file_date(path):
    m = re.search(r"yahoo-(\d{4}-\d{2}-\d{2})\.csv$", path or "")
    return m.group(1) if m else None


def load_yahoo(path):
    """{norm(name): {"name", "price", "source"}} — ADP first, else XRank."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            price, source = None, None
            for col, label in (("adp", "ADP"), ("xrank", "XR")):
                try:
                    price, source = float(r[col]), label
                    break
                except (TypeError, ValueError, KeyError):
                    continue
            if price is not None:
                out[norm(r["player"])] = {"name": r["player"], "price": price, "source": source}
    return out


def join(players, prices):
    """Attach `_mkt`/`_mktsrc` to each pool row; returns (priced, unpriced) counts."""
    n = 0
    for p in players:
        hit = prices.get(norm(p["player"]))
        p["_mkt"] = hit["price"] if hit else None
        p["_mktsrc"] = hit["source"] if hit else None
        n += hit is not None
    return n, len(players) - n


def drift(players_top, prices, joined_keys):
    """Unpriced top-board names that match an UNJOINED Yahoo name on surname +
    first three letters: a spelling, not a missing price. Refuse-class."""
    def key(k):
        t = k.split()
        return (t[-1], t[0][:3]) if t else (k, "")
    spare = {key(k): v["name"] for k, v in prices.items() if k not in joined_keys}
    out = []
    for p in players_top:
        if p.get("_mkt") is None:
            k = key(norm(p["player"]))
            if k in spare:
                out.append(f"{p['player']} (deck) vs {spare[k]} (Yahoo)")
    return out


def write_snapshot(players, date, dest=SNAPSHOT):
    with open(dest, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["player", "price", "source", "date"])
        for p in players:
            if p.get("_mkt") is not None:
                w.writerow([p["player"], p["_mkt"], p["_mktsrc"], date])


def load_snapshot(path=SNAPSHOT):
    """{deck player name: price} or None when no snapshot exists."""
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return {r["player"]: float(r["price"]) for r in csv.DictReader(f)}


def age_days(date, today=None):
    today = today or datetime.date.today()
    return (today - datetime.date.fromisoformat(date)).days
