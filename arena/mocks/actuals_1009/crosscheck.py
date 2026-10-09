#!/usr/bin/env python3
"""Cross-check the two outlets' per-game lines per season and write the verified record.
  crosscheck.py OUT  (reads OUT/bref_pergame_<s>.csv + OUT/espn_pergame_<s>.csv; writes OUT/actuals_<s>.csv,
  OUT/disagreements_<s>.csv, OUT/unmatched_<s>.csv, OUT/crosscheck_summary.json)
Agreement: gp exact; per-game counting fields |bref - espn| <= 0.0501 (bref prints one decimal);
percentages |bref - espn| <= 0.000501 (bref prints three). Minutes (mpg) are informational only
(the outlets round total minutes differently); a blank bref percentage with zero attempts equals ESPN's 0.
Classes: VERIFIED = every field within rounding; NOTED = gp equal and every deviation <= 0.1 per game
(<= 0.002 on a percentage) — kept, with the cells named in `note`; CONFLICT = anything larger — excluded
and listed. The record row carries ESPN's unrounded values (4 dp), bref's spelling and team, ESPN's team.
Name join: fold (NFKD, no punctuation, lower, suffixes jr/sr/ii/iii/iv dropped), then for the leftovers
(surname, first three letters) when unique on both sides, then (surname, espn team == bref team) when unique, then the same tokens in another order.
"""
import csv, json, os, sys, unicodedata
OUT = sys.argv[1]
SEASONS = ["2022-23", "2023-24", "2024-25", "2025-26"]
NUM = ["mpg", "fga", "fgm", "fta", "ftm", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
PCT = ["fg_pct", "ft_pct"]
SUFFIX = {"jr", "sr", "ii", "iii", "iv", "v"}
TEAM_ALIAS = {"PHO": "PHX", "BRK": "BKN", "CHO": "CHA", "GSW": "GS", "NOP": "NO", "NYK": "NY", "SAS": "SA", "UTA": "UTAH", "WAS": "WSH"}

def fold(s):
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = s.replace(".", "").replace("'", "").replace("’", "").replace("-", " ").lower()
    toks = [t for t in s.split() if t not in SUFFIX]
    return " ".join(toks)

def key3(f):
    t = f.split()
    return (t[-1], t[0][:3]) if len(t) >= 2 else (f, "")

def load(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))

def agree(b, e, field):
    tol = 0.000501 if field in PCT else 0.0501
    if field in PCT and b[field] == "" and float(e[field]) == 0.0:
        return True, 0.0, 0.0  # no attempts: bref prints a blank, ESPN a zero
    try:
        return abs(float(b[field]) - float(e[field])) <= tol, float(b[field]), float(e[field])
    except ValueError:
        return (b[field] == e[field]), b[field], e[field]

def noted_ok(field, vb, ve):
    if field == "gp": return False
    try: return abs(float(vb) - float(ve)) <= (0.002 if field in PCT else 0.1)
    except (TypeError, ValueError): return False

summary = {}
for s in SEASONS:
    B = load(os.path.join(OUT, f"bref_pergame_{s}.csv")); E = load(os.path.join(OUT, f"espn_pergame_{s}.csv"))
    bf = {}; ef = {}
    for r in B: bf.setdefault(fold(r["player"]), []).append(r)
    for r in E: ef.setdefault(fold(r["player"]), []).append(r)
    pairs, how = [], {"fold": 0, "key3": 0, "team": 0}
    used_e = set()
    for k, rows in bf.items():
        if k in ef and len(rows) == 1 and len(ef[k]) == 1:
            pairs.append((rows[0], ef[k][0], "fold")); used_e.add(k); how["fold"] += 1
    left_b = [r for k, rows in bf.items() if k not in used_e for r in rows]
    left_e = {k: rows[0] for k, rows in ef.items() if k not in used_e and len(rows) == 1}
    # pass 2: (surname, first3) unique on both sides
    e3 = {}
    for k, r in left_e.items(): e3.setdefault(key3(k), []).append((k, r))
    b3 = {}
    for r in left_b: b3.setdefault(key3(fold(r["player"])), []).append(r)
    taken = set()
    for k3, brs in b3.items():
        if len(brs) == 1 and len(e3.get(k3, [])) == 1:
            ek, er = e3[k3][0]
            pairs.append((brs[0], er, "key3")); taken.add(ek); how["key3"] += 1
    left_b = [r for r in left_b if not any(r is p[0] for p in pairs)]
    left_e = {k: r for k, r in left_e.items() if k not in taken}
    # pass 3: surname + team (bref team mapped to espn code), unique
    et = {}
    for k, r in left_e.items(): et.setdefault((k.split()[-1], r["team"]), []).append((k, r))
    taken = set()
    for r in left_b:
        bt = TEAM_ALIAS.get(r["team"], r["team"]); kk = (fold(r["player"]).split()[-1], bt)
        if len(et.get(kk, [])) == 1:
            ek, er = et[kk][0]
            if ek not in taken:
                pairs.append((r, er, "team")); taken.add(ek); how["team"] += 1
    left_b = [r for r in left_b if not any(r is p[0] for p in pairs)]
    left_e = {k: r for k, r in left_e.items() if k not in taken}
    # pass 4: the same tokens in another order (bref "Cui Yongxi", ESPN "Yongxi Cui"), unique
    et = {}
    for k, r in left_e.items(): et.setdefault(tuple(sorted(k.split())), []).append((k, r))
    taken = set()
    for r in left_b:
        kk = tuple(sorted(fold(r["player"]).split()))
        if len(et.get(kk, [])) == 1 and et[kk][0][0] not in taken:
            ek, er = et[kk][0]
            pairs.append((r, er, "tokens")); taken.add(ek); how["tokens"] = how.get("tokens", 0) + 1
    left_b = [r for r in left_b if not any(r is p[0] for p in pairs)]
    left_e = {k: r for k, r in left_e.items() if k not in taken}
    verified, disagreements, n_noted, n_conflict = [], [], 0, 0
    for b, e, h in pairs:
        bad = []
        if b["gp"] != e["gp"]: bad.append(("gp", b["gp"], e["gp"]))
        for f in [x for x in NUM if x != "mpg"] + PCT:
            ok, vb, ve = agree(b, e, f)
            if not ok: bad.append((f, vb, ve))
        status = "verified" if not bad else ("noted" if all(noted_ok(f, vb, ve) for f, vb, ve in bad) else "conflict")
        for f, vb, ve in bad:
            disagreements.append({"player": b["player"], "espn_player": e["player"], "team": b["team"], "field": f, "bref": vb, "espn": ve, "class": status, "join": h})
        if status == "conflict":
            n_conflict += 1
            continue
        n_noted += status == "noted"
        row = {"player": b["player"], "team": b["team"], "espn_team": e["team"], "gp": b["gp"], "join": h, "status": status,
               "note": "; ".join(f"{f} bref {vb} espn {ve}" for f, vb, ve in bad)}
        for f in NUM + PCT: row[f] = e[f]
        verified.append(row)
    cols = ["player", "team", "espn_team", "gp"] + NUM + PCT + ["join", "status", "note"]
    with open(os.path.join(OUT, f"actuals_{s}.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(sorted(verified, key=lambda r: (r["player"], r["team"])))
    with open(os.path.join(OUT, f"disagreements_{s}.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["player", "espn_player", "team", "field", "bref", "espn", "class", "join"]); w.writeheader(); w.writerows(sorted(disagreements, key=lambda r: (r["player"], r["field"])))
    with open(os.path.join(OUT, f"unmatched_{s}.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["side", "player", "team", "gp", "pts"])
        for r in sorted(left_b, key=lambda r: r["player"]): w.writerow(["bref", r["player"], r["team"], r["gp"], r["pts"]])
        for k, r in sorted(left_e.items(), key=lambda kv: kv[1]["player"]): w.writerow(["espn", r["player"], r["team"], r["gp"], r["pts"]])
    dis_players = sorted({d["player"] for d in disagreements})
    byfield = {}
    for d in disagreements: byfield[d["field"]] = byfield.get(d["field"], 0) + 1
    summary[s] = {"bref_rows": len(B), "espn_rows": len(E), "matched": len(pairs), "join": how,
                  "recorded": len(verified), "verified_clean": len(verified) - n_noted, "noted": n_noted, "conflict": n_conflict,
                  "players_with_disagreement": len(dis_players), "disagreeing_cells": len(disagreements),
                  "cells_by_field": byfield, "unmatched_bref": len(left_b), "unmatched_espn": len(left_e),
                  "disagreeing_players": dis_players[:40],
                  "unmatched_bref_names": [r["player"] for r in sorted(left_b, key=lambda r: -float(r["pts"] or 0))][:25],
                  "unmatched_espn_names": [r["player"] for r in sorted(left_e.values(), key=lambda r: -float(r["pts"] or 0))][:25]}
    print(f"{s}: bref {len(B)} espn {len(E)} matched {len(pairs)} {how} | recorded {len(verified)} (clean {len(verified) - n_noted}, noted {n_noted}), conflict {n_conflict} | cells {len(disagreements)} {byfield} | unmatched bref {len(left_b)} espn {len(left_e)}")
json.dump(summary, open(os.path.join(OUT, "crosscheck_summary.json"), "w"), indent=1)
