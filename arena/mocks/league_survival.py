#!/usr/bin/env python3
"""The price-only survival model against the owner's OWN league (D40-2, 2026-10-01).

Inputs: Yahoo's pre-draft ranks for 2025-26 (the Dan Titus 10/16 column the owner pasted,
arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt — 199 names, rank = row) and the
league's resolved 2025-26 draft (arena/draft_boards.json["2025-26"], 156 picks, manager per
pick). Rows: at each of the owner's thirteen turns, every ranked player still on the board
(the owner's own pick excluded) with rank <= pick + WINDOW, predicted to survive to the
owner's next turn by P = Phi((rank - N) / max(floor, k * rank)) (hoops.survival_prob's form)
and observed. Scores the shipped parameters (k 0.30, floor 8 — fit on 98 public-room rows,
2026-09-22), a grid, leave-one-turn-out, the base rate; writes the result file.

    python3 arena/mocks/league_survival.py arena/results/league_survival_2025-26.json [--window 60]
"""
import json, math, os, re, statistics, sys, unicodedata
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import hoops  # noqa: E402
RAW = os.path.join(REPO, "arena", "data", "league_predraft_ranks_2025-26_raw_2026-10-01.txt")
OUT = sys.argv[1]
WINDOW = int(sys.argv[sys.argv.index("--window") + 1]) if "--window" in sys.argv else 60
SUFFIX = {"jr", "sr", "ii", "iii", "iv"}


def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "").replace("-", " ")
    toks = [t for t in s.split() if t not in SUFFIX]
    return " ".join(toks)


def phi(x):
    """The engine's own normal CDF (Abramowitz-Stegun 7.1.26, bit-identical to the deck's JS)."""
    return hoops._norm_cdf_as(x)


def surv(rank, n, k, floor):
    return min(0.99, max(0.01, phi((rank - n) / max(floor, k * rank))))


def main():
    ranks, names = {}, {}
    for line in open(RAW, encoding="utf-8").read().splitlines()[1:]:
        m = re.match(r"^(\d+)\t(.+?) \(([A-Z]{2,3}) - ([A-Z,]+)\)(?:\t(\d+))?$", line)
        assert m, line
        rk, nm = int(m.group(1)), m.group(2)
        assert m.group(5) is None or int(m.group(5)) == rk, line   # the rank column equals the row number
        ranks[norm(nm)] = rk; names[norm(nm)] = nm
    assert len(ranks) == 199
    board = json.load(open(os.path.join(REPO, "arena", "draft_boards.json")))["2025-26"]
    assert len(board) == 156 and [b["pick"] for b in board] == list(range(1, 157))
    owner = [b["pick"] for b in board if b["manager"] == "David"]
    assert len(owner) == 13, owner
    drafted_at = {}
    unmatched = []
    for b in board:
        key = norm(b["player"])
        if key in ranks:
            drafted_at[key] = b["pick"]
        else:
            unmatched.append(dict(pick=b["pick"], player=b["player"], manager=b["manager"]))
    matched = len(drafted_at)
    # shipped-parameter check against hoops.survival_prob (same form)
    assert abs(surv(87, 90, 0.30, 8) - hoops.survival_prob(87, 90)) < 1e-12

    def rows_for(window):
        rows = []
        for i, n in enumerate(owner):
            n2 = owner[i + 1] if i + 1 < len(owner) else None
            if n2 is None:
                continue
            own_pick = norm(board[n - 1]["player"])
            for key, rk in ranks.items():
                if key == own_pick or rk > n + window:
                    continue
                da = drafted_at.get(key)
                if da is not None and da < n:
                    continue   # already gone before this turn
                alive = da is None or da >= n2
                rows.append(dict(turn=n, next=n2, name=names[key], rank=rk, drafted_at=da, alive=alive))
        return rows

    def brier(rows, k, floor):
        return statistics.mean((surv(r["rank"], r["next"], k, floor) - (1 if r["alive"] else 0)) ** 2 for r in rows)

    def bands(rows, k, floor):
        out = []
        for lo, hi in ((0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)):
            sub = [r for r in rows if lo <= surv(r["rank"], r["next"], k, floor) < hi]
            if sub:
                out.append(dict(band=f"[{lo},{min(hi, 1.0)})", n=len(sub),
                                mean_pred=round(statistics.mean(surv(r["rank"], r["next"], k, floor) for r in sub), 3),
                                realized=round(sum(r["alive"] for r in sub) / len(sub), 3)))
        return out

    KS, FLOORS = (0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50), (4, 6, 8, 10, 12, 16)
    result = dict(date="2026-10-01", decision="D40-2", window=WINDOW, ranks=len(ranks), picks=156, matched=matched,
                  unmatched=unmatched, owner_turns=owner, shipped=dict(k=0.30, floor=8))
    for label, window in (("main", WINDOW), ("narrow", 30)):
        rows = rows_for(window)
        realized = sum(r["alive"] for r in rows) / len(rows)
        base = statistics.mean((realized - (1 if r["alive"] else 0)) ** 2 for r in rows)
        grid = sorted((round(brier(rows, k, f), 4), k, f) for k in KS for f in FLOORS)
        shipped = brier(rows, 0.30, 8)
        # leave-one-turn-out: fit the grid on the other turns, test on the held-out turn
        loto = []
        for n in owner[:-1]:
            fit = [r for r in rows if r["turn"] != n]; test = [r for r in rows if r["turn"] == n]
            if not test:
                continue
            bk, bf = min(((brier(fit, k, f), k, f) for k in KS for f in FLOORS))[1:]
            loto.append(dict(turn=n, k=bk, floor=bf, n=len(test), test_brier=round(brier(test, bk, bf), 4),
                             shipped_brier=round(brier(test, 0.30, 8), 4)))
        loto_fit = statistics.mean(x["test_brier"] for x in loto); loto_ship = statistics.mean(x["shipped_brier"] for x in loto)
        chips = {}
        for name, lo, hi in (("BUY NOW (<=0.20)", 0, 0.2000001), ("TOSS-UP (0.20-0.40)", 0.2000001, 0.40), ("quiet (>=0.60)", 0.60, 1.01)):
            sub = [r for r in rows if lo <= surv(r["rank"], r["next"], 0.30, 8) < hi]
            chips[name] = dict(n=len(sub), alive=sum(r["alive"] for r in sub), mean_pred=round(statistics.mean(surv(r["rank"], r["next"], 0.30, 8) for r in sub), 3) if sub else None)
        deep = [r for r in rows if r["rank"] - r["turn"] >= 24]
        result[label] = dict(rows=len(rows), realized=round(realized, 3), base_rate_brier=round(base, 4), shipped_brier=round(shipped, 4),
                             grid_best=grid[:6], loto=loto, loto_fit_brier=round(loto_fit, 4), loto_shipped_brier=round(loto_ship, 4),
                             bands_shipped=bands(rows, 0.30, 8), bands_best=bands(rows, grid[0][1], grid[0][2]), chips_shipped=chips,
                             deep_rows=dict(n=len(deep), alive=sum(r["alive"] for r in deep),
                                            mean_pred=round(statistics.mean(surv(r["rank"], r["turn"] and r["next"], 0.30, 8) for r in deep), 3) if deep else None))
        if label == "main":
            result["rows_main"] = rows
    # the league's reach/fall profile: pick minus rank for every matched pick, by manager
    diffs = [(b["pick"] - ranks[norm(b["player"])], b["manager"]) for b in board if norm(b["player"]) in ranks]
    by_mgr = {}
    for d, m in diffs:
        by_mgr.setdefault(m, []).append(d)
    result["league_profile"] = dict(matched_picks=len(diffs), mean_pick_minus_rank=round(statistics.mean(d for d, _ in diffs), 1),
                                    median=statistics.median(d for d, _ in diffs),
                                    reaches_24plus=sum(1 for d, _ in diffs if d <= -24), falls_24plus=sum(1 for d, _ in diffs if d >= 24),
                                    by_manager={m: dict(n=len(v), mean=round(statistics.mean(v), 1), reaches_24plus=sum(1 for d in v if d <= -24)) for m, v in sorted(by_mgr.items())})
    # pre-stated decision rule (A3): propose league parameters only if LOTO beats the shipped by >= 0.01
    mm = result["main"]
    result["decision_rule"] = dict(rule="propose league parameters only if leave-one-turn-out Brier beats the shipped parameters by >= 0.01",
                                   loto_fit=mm["loto_fit_brier"], loto_shipped=mm["loto_shipped_brier"],
                                   propose=(mm["loto_shipped_brier"] - mm["loto_fit_brier"]) >= 0.01)
    json.dump(result, open(OUT, "w"), indent=1)
    print(f"ranks {len(ranks)} · picks 156 · matched {matched} · unmatched {len(unmatched)}: {[u['player'] for u in unmatched][:12]}")
    print(f"owner turns {owner}")
    for label in ("main", "narrow"):
        m = result[label]
        print(f"[{label}] rows {m['rows']} realized {m['realized']} | Brier shipped {m['shipped_brier']} base {m['base_rate_brier']} grid-best {m['grid_best'][0]} | LOTO fit {m['loto_fit_brier']} vs shipped {m['loto_shipped_brier']}")
        print("   bands (shipped):", m["bands_shipped"])
        print("   chips (shipped):", m["chips_shipped"])
        print("   deep rows (rank 24+ below the pick):", m["deep_rows"])
    print("league profile:", {k: v for k, v in result["league_profile"].items() if k != "by_manager"})
    for mgr, v in result["league_profile"]["by_manager"].items():
        print(f"   {mgr:<8} n {v['n']:>2} mean pick-rank {v['mean']:>6} reaches 24+ {v['reaches_24plus']}")
    print("decision rule:", result["decision_rule"])


if __name__ == "__main__":
    main()
