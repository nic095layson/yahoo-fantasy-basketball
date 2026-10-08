#!/usr/bin/env python3
"""Standing repeat-name market check (owner decision D-RN-1, 2026-10-08).

Born from the owner's question of 2026-10-08: is the card siloed — recommending
the same names draft after draft? The mocks cannot answer that alone. Every mock
is graded with the same projection lines the card reads, so a line that flatters
one player makes the card take him in every room AND grades the pick well; the
repeat-name audit (2026-09-29) showed the card reacts to the roster, not that its
lines are right. The only check on a flattering line is outside evidence. The
rule, from the owner's yes: any player who is the card's top pick in 5 or more
mocks while sitting 25+ places away from the market gets an outside-source check
at every refresh.

  default            replay every graded mock (the MOCKS registry of
                     arena/mocks/live_retro.py, with a saved state) on the page
                     with the deck's own engine (arena/mocks/live_deckcard.py —
                     the card exactly as the page computes it, priced-only from
                     round 11 included), count for each player the mocks in
                     which he is the card's 🎯 at one or more owner turns, and
                     flag every player at MIN_MOCKS or more whose value rank and
                     market rank — the two numbers the card prints — sit MIN_GAP
                     or more places apart, or who has no Yahoo price. Print the
                     ready-to-paste section: per flagged name the outside ranks
                     on file (the kit's newest Yahoo projection-rank, Hashtag,
                     Rotoworld 9-cat and RotoBaller files), the cells
                     of his line outside all three outside per-game projections,
                     and the verdict.
  --check-report P   verify the after-report at P carries a "Repeat-name market
                     check" section with one table row per flagged name. Exit 1
                     naming each flagged name without a row (DATA-PULL.md).
  --json PATH        write the run record (page sha256, mocks, the 🎯 at every
                     owner turn of every mock, counts, flagged rows).
  --cards DIR        read pre-made replays (DIR/m<N>.json, live_deckcard.py's
                     output) instead of replaying — the suite's fixtures.
  --keep-cards DIR   keep this run's replays in DIR.

Verdict — the 10/06 cross-source rule (D-RW-1, after-report-2026-10-06-rotoworld):
LINE QUESTIONED when three or more outside ranks exist and every one sits MIN_GAP
or more places from our value rank on the same side (re-derive the line at the
next projection pass, two dated outlets); SOURCES SPLIT otherwise (the line
holds). A name a list leaves out counts as one place past the list's end.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PAGE = os.path.join(ROOT, "docs", "draft-deck.html")
POOL = os.path.join(ROOT, "data", "players.csv")
STATES = os.path.join(ROOT, "arena", "data", "states")
RETRO = os.path.join(ROOT, "arena", "mocks", "live_retro.py")
REPLAY = os.path.join(ROOT, "arena", "mocks", "live_deckcard.py")
KIT_DEFAULT = os.environ.get("KIT_REPO") or os.path.join(ROOT, "..", "fantasy-basketball-2026-27")

MIN_MOCKS = 5    # owner, 2026-10-08
MIN_GAP = 25     # owner, 2026-10-08 — the D-RW-1 bar
HEADING = "Repeat-name market check"

# Outside rank lists (kit report/market/, newest file of each family):
# (label, filename pattern, name column, rank column). The kit's consensus-*.csv is
# deliberately absent: it averages OUR board rank with Yahoo's, so it is not outside
# evidence (in the first run, 2026-10-08, it alone held PJ Washington's line, which
# all four independent sources question). Yahoo's ADP/XRank is the market column itself.
RANK_SOURCES = [
    ("Yahoo Rank", r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv", "player", "yrank"),
    ("Hashtag", r"hashtag-\d{4}-\d{2}-\d{2}\.csv", "player", "rank"),
    ("Rotoworld", r"rotoworld-9cat-\d{4}-\d{2}-\d{2}\.csv", "Player", "Rank"),
    ("RotoBaller", r"rotoballer-\d{4}-\d{2}-\d{2}\.csv", "player", "src_rank"),
]
# Outside per-game lines for the cell check: (label, pattern, name column, column prefix, % scale)
LINE_SOURCES = [
    ("Yahoo", r"yahoo-proj-\d{4}-\d{2}-\d{2}\.csv", "player", "", 1.0),
    ("Hashtag", r"hashtag-\d{4}-\d{2}-\d{2}\.csv", "player", "", 1.0),
    ("RotoBaller", r"rotoballer-\d{4}-\d{2}-\d{2}\.csv", "player", "src_", 100.0),
]
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]


def fold(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'’]", "", s)
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()


def graded_mocks():
    """The MOCKS registry keys, read as text: live_retro.py runs at import."""
    src = open(RETRO, encoding="utf-8").read()
    i = src.index("MOCKS = {")
    depth = 0
    for j in range(i, len(src)):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                break
    keys = [int(k) for k in re.findall(r"^\s+(\d+): dict\(", src[i:j + 1], re.M)]
    return [m for m in keys if os.path.exists(os.path.join(STATES, f"draft_state_{m}.json"))]


def replay(mocks, page, outdir):
    cards, failed = {}, {}
    for m in mocks:
        out = os.path.join(outdir, f"m{m}.json")
        r = subprocess.run([sys.executable, REPLAY, str(m), page, out],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode != 0 or not os.path.exists(out):
            tail = (r.stderr or r.stdout).strip().splitlines()
            failed[m] = f"replay exit {r.returncode}: {tail[-1] if tail else 'no output'}"
            continue
        cards[m] = json.load(open(out, encoding="utf-8"))
    return cards, failed


def load_cards(d):
    cards, failed = {}, {}
    for f in sorted(glob.glob(os.path.join(d, "m*.json"))):
        m = int(re.search(r"m(\d+)\.json$", f).group(1))
        try:
            turns = json.load(open(f, encoding="utf-8"))
            if not isinstance(turns, list):
                raise ValueError("not a list of turns")
            cards[m] = turns
        except ValueError as e:
            failed[m] = f"replay unreadable: {e}"
    return cards, failed


def targets(turns):
    """The card's 🎯 at each owner turn: the row the deck marks, else its rank 1."""
    out = []
    for t in turns:
        rows = t.get("rows") or []
        if rows:
            tg = next((r for r in rows if r.get("target")), None) or min(rows, key=lambda r: r["rank"])
            out.append((t["pick"], tg))
    return out


def page_players(page):
    src = open(page, encoding="utf-8").read()
    data = re.search(r'<script id="data">([\s\S]*?)</script>', src).group(1)
    return json.loads(re.search(r"const PLAYERS = (\[.*?\]);\n", data, re.S).group(1))


def newest(kit, pattern):
    files = sorted(f for f in glob.glob(os.path.join(kit, "report", "market", "*.csv"))
                   if re.fullmatch(pattern, os.path.basename(f)))
    return files[-1] if files else None


def outside_ranks(kit):
    lists = {}
    for label, pat, ncol, rcol in RANK_SOURCES:
        f = newest(kit, pat)
        if not f:
            continue
        ranks = {}
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            try:
                ranks.setdefault(fold(r[ncol]), int(float(r[rcol])))
            except (KeyError, TypeError, ValueError):
                continue
        if ranks:
            lists[label] = (os.path.basename(f), ranks, max(ranks.values()))
    return lists


def outside_lines(kit):
    lines = {}
    for label, pat, ncol, pre, scale in LINE_SOURCES:
        f = newest(kit, pat)
        if not f:
            continue
        d = {}
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            try:
                d[fold(r[ncol])] = {c: float(r[pre + c]) / (scale if c.endswith("pct") else 1.0) for c in CATS}
            except (KeyError, TypeError, ValueError):
                continue
        lines[label] = (os.path.basename(f), d)
    return lines


def our_lines():
    out = {}
    for r in csv.DictReader(open(POOL, encoding="utf-8")):
        try:
            out[fold(r["player"])] = {c: float(r[c]) for c in CATS}
        except (KeyError, ValueError):
            continue
    return out


def cells_outside(ours, refs):
    """Cells of our line outside [min, max] of every outside line (all three required)."""
    if ours is None or len(refs) < 3:
        return None
    out = []
    for c in CATS:
        vals = [d[c] for d in refs]
        lo, hi = min(vals), max(vals)
        tol = 0.005 if c.endswith("pct") else max(0.1, 0.05 * hi)
        if not (lo - tol <= ours[c] <= hi + tol):
            fmt = (lambda v: f"{v:.3f}".lstrip("0")) if c.endswith("pct") else (lambda v: f"{v:g}")
            out.append(f"{c} {fmt(ours[c])} vs {fmt(lo)}-{fmt(hi)}")
    return out


def verdict(val_rank, ranks):
    if len(ranks) < 3:
        return f"TOO FEW SOURCES ({len(ranks)} outside ranks on file)"
    below = sum(1 for r in ranks if r - val_rank >= MIN_GAP)   # they rank him lower: we are higher
    above = sum(1 for r in ranks if val_rank - r >= MIN_GAP)   # they rank him higher: we are lower
    n = len(ranks)
    if below == n:
        return f"LINE QUESTIONED: all {n} outside ranks sit {MIN_GAP}+ places below ours; re-derive at the next projection pass (two dated outlets)"
    if above == n:
        return f"LINE QUESTIONED: all {n} outside ranks sit {MIN_GAP}+ places above ours; re-derive at the next projection pass (two dated outlets)"
    return f"SOURCES SPLIT: {max(below, above)} of {n} sit {MIN_GAP}+ places on one side; the line holds"


def compute(args):
    page = os.path.abspath(args.page)
    if args.cards:
        cards, failed = load_cards(args.cards)
        mocks = sorted(set(cards) | set(failed))
    else:
        mocks = graded_mocks()
        outdir = args.keep_cards or tempfile.mkdtemp(prefix="rn-cards-")
        os.makedirs(outdir, exist_ok=True)
        cards, failed = replay(mocks, page, outdir)
    priced = {p["n"]: p.get("mkt") for p in page_players(page)}
    per_mock, counts, rowinfo = {}, {}, {}
    for m in sorted(cards):
        tg = targets(cards[m])
        per_mock[m] = [[pick, r["n"]] for pick, r in tg]
        for n in {r["n"] for _, r in tg}:
            counts[n] = counts.get(n, 0) + 1
        for _, r in tg:
            rowinfo.setdefault(r["n"], r)
    lists = outside_ranks(args.kit)
    lines = outside_lines(args.kit)
    ours_all = our_lines()
    flagged, near = [], []
    for n, k in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        if k < MIN_MOCKS:
            continue
        r = rowinfo[n]
        val, mkt = r.get("valRank"), r.get("mkt")
        no_price = not priced.get(n)
        gap = abs(val - mkt) if (val is not None and mkt is not None) else None
        if not no_price and (gap is None or gap < MIN_GAP):
            near.append(dict(player=n, mocks=k, value_rank=val, market_rank=mkt, gap=gap))
            continue
        f = fold(n)
        ranks, shown = [], {}
        for label, (_, rk, last) in lists.items():
            v = rk.get(f)
            shown[label] = str(v) if v is not None else f">{last}"
            ranks.append(v if v is not None else last + 1)
        refs = [d[f] for _, d in lines.values() if f in d]
        cells = cells_outside(ours_all.get(f), refs)
        flagged.append(dict(player=n, mocks=k, value_rank=val, market_rank=mkt, gap=gap, no_price=no_price,
                            outside=shown, cells=cells, verdict=verdict(val, ranks)))
    return dict(page=page, page_sha256=hashlib.sha256(open(page, "rb").read()).hexdigest(),
                mocks=mocks, replayed=sorted(cards), failed={str(k): v for k, v in failed.items()},
                thresholds=dict(min_mocks=MIN_MOCKS, min_gap=MIN_GAP),
                rank_files={k: v[0] for k, v in lists.items()}, line_files={k: v[0] for k, v in lines.items()},
                targets={str(k): v for k, v in per_mock.items()}, counts=counts, flagged=flagged, near_misses=near)


def section(rec):
    n_all, n_ok = len(rec["mocks"]), len(rec["replayed"])
    labels = [l for l, *_ in RANK_SOURCES if l in rec["rank_files"]]
    out = [f"## {HEADING}", "",
           f"Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in {MIN_MOCKS}+ of the graded mocks, replayed on "
           f"this page (sha256 {rec['page_sha256'][:12]}), with {MIN_GAP}+ places between the value rank and "
           f"the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. "
           f"Replays: {n_ok} of {n_all} mocks"
           + (" (failed: " + "; ".join(f"mock {k}: {v}" for k, v in rec["failed"].items()) + ")" if rec["failed"] else "")
           + ". Outside ranks: " + (", ".join(f"{k} `{v}`" for k, v in rec["rank_files"].items()) or "none on file")
           + ". Cells: our per-game line against "
           + (", ".join(f"`{v}`" for v in rec["line_files"].values()) or "no outside lines on file")
           + " (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats).", ""]
    if rec["flagged"]:
        out += ["| player | 🎯 in mocks | value rank | market rank | " + " | ".join(labels)
                + " | cells outside all three projections | verdict |",
                "|---|---|---|---|" + "---|" * len(labels) + "---|---|"]
        for f in rec["flagged"]:
            mk = "no Yahoo price" if f["no_price"] else str(f["market_rank"])
            cells = "—" if f["cells"] is None else ("none" if not f["cells"] else "; ".join(f["cells"]))
            out.append(f"| {f['player']} | {f['mocks']} of {n_ok} | {f['value_rank']} | {mk} | "
                       + " | ".join(f["outside"].get(l, "—") for l in labels) + f" | {cells} | {f['verdict']} |")
    else:
        out.append(f"No player is flagged: none is the card's 🎯 in {MIN_MOCKS}+ mocks with a {MIN_GAP}+ place gap.")
    if rec["near_misses"]:
        out += ["", f"Near misses (the 🎯 in {MIN_MOCKS}+ mocks, under {MIN_GAP} places): "
                + "; ".join(f"{x['player']} ({x['mocks']} mocks, value {x['value_rank']}, market {x['market_rank']})"
                            for x in rec["near_misses"]) + "."]
    return "\n".join(out) + "\n"


def check_report(path, rec):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("#") and HEADING in ln), None)
    if start is None:
        print(f"REPEAT-NAME CHECK: FAIL — no '{HEADING}' section in {os.path.basename(path)}")
        return 1
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    body = []
    for ln in lines[start + 1:]:
        if ln.startswith("#") and len(ln) - len(ln.lstrip("#")) <= level:
            break
        body.append(ln)
    rows = [fold(ln.strip().strip("|").split("|")[0]) for ln in body
            if ln.strip().startswith("|") and not set(ln.strip()) <= set("|-: ")]
    missing = [f["player"] for f in rec["flagged"] if fold(f["player"]) not in rows]
    if missing:
        print(f"REPEAT-NAME CHECK: FAIL — {os.path.basename(path)}: flagged name(s) with no row in the "
              f"'{HEADING}' table: " + ", ".join(missing))
        return 1
    print(f"REPEAT-NAME CHECK: PASS — {os.path.basename(path)}: {len(rec['flagged'])} flagged name(s), "
          f"each with a row ({len(rec['replayed'])} of {len(rec['mocks'])} mocks replayed)")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--page", default=PAGE)
    ap.add_argument("--kit", default=KIT_DEFAULT)
    ap.add_argument("--cards")
    ap.add_argument("--keep-cards")
    ap.add_argument("--json")
    ap.add_argument("--check-report", metavar="PATH")
    args = ap.parse_args()
    rec = compute(args)
    if len(rec["failed"]) > 2:
        print(f"REPEAT-NAME CHECK: STOP — {len(rec['failed'])} of {len(rec['mocks'])} mocks failed to replay; "
              "the counts cannot be trusted: " + "; ".join(f"mock {k}: {v}" for k, v in rec["failed"].items()))
        sys.exit(2)
    if args.json:
        json.dump(rec, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if args.check_report:
        sys.exit(check_report(args.check_report, rec))
    print(f"{len(rec['replayed'])} of {len(rec['mocks'])} mocks replayed; "
          + (("failed: " + "; ".join(f"mock {k}: {v}" for k, v in rec["failed"].items()) + "; ") if rec["failed"] else "")
          + f"{len(rec['flagged'])} FLAGGED, {len(rec['near_misses'])} near miss(es)")
    for f in rec["flagged"]:
        print(f"  FLAGGED {f['player']}: the 🎯 in {f['mocks']} mocks, value {f['value_rank']}, market "
              + ("no Yahoo price" if f["no_price"] else str(f["market_rank"])) + f" — {f['verdict']}")
    print()
    print(section(rec))


if __name__ == "__main__":
    main()
