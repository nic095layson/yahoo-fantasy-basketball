#!/usr/bin/env python3
"""Build data/market_adp.json from the bundled consensus feed.

Real average draft position (ADP) for deck-pool players, keyed by the deck's
own player names. Consumed by build_deck.py (injected as `const ADP`) and by
arena.market_ranks / the deck's marketRanks — replacing the circular
z-score-derived market proxy with a genuinely exogenous room price.

Source: data/market/hashtag-2026-08-21.csv (Hashtag Basketball consensus ADP;
provenance in data/market/provenance.csv). Only players whose name resolves to
a deck-pool row get an ADP; everyone else falls back to the proxy inside
marketRanks, so a partial match is expected and safe — this script reports the
unmatched-but-ranked feed players rather than hiding them.

Name matching reuses the accent/punctuation normalizer plus the confirmed
alias set the kit-side join settled on 2026-08-21 (surname+team verified before
each alias was added — a wrong merge is worse than a miss).
"""
import csv
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FEED = os.path.join(ROOT, "data", "market", "hashtag-2026-08-21.csv")
POOL = os.path.join(ROOT, "data", "players.csv")
OUT = os.path.join(ROOT, "data", "market_adp.json")

NAME_ALIAS = {
    "cameron johnson": "cam johnson",
    "alexandre sarr": "alex sarr",
    "herbert jones": "herb jones",
    "nicolas claxton": "nic claxton",
}


def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", " ", s)
    s = " ".join(s.split())
    return NAME_ALIAS.get(s, s)


def main():
    pool = {}
    with open(POOL) as f:
        for r in csv.DictReader(f):
            pool[norm(r["player"])] = r["player"]

    feed = {}
    with open(FEED) as f:
        for r in csv.DictReader(f):
            try:
                feed[norm(r["player"])] = (r["player"], float(r["adp"]))
            except (KeyError, ValueError):
                continue

    adp, unmatched = {}, []
    for key, (feed_name, val) in feed.items():
        if key in pool:
            adp[pool[key]] = val
        else:
            unmatched.append((val, feed_name))

    # deterministic key order so the file diffs cleanly across rebuilds
    ordered = {k: adp[k] for k in sorted(adp, key=lambda n: (adp[n], n))}
    with open(OUT, "w") as f:
        json.dump(ordered, f, indent=0, ensure_ascii=True)
        f.write("\n")

    print("market_adp.json: %d deck players matched to ADP (of %d pool rows)"
          % (len(adp), len(pool)))
    unmatched.sort()
    print("feed players with ADP but no pool row: %d (they fall back to proxy)"
          % len(unmatched))
    for val, name in unmatched[:15]:
        print("  ADP %.1f  %s" % (val, name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
