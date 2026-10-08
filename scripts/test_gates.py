#!/usr/bin/env python3
"""Publish-gate regression suite — the gates must be seen to FIRE.

    python3 scripts/test_gates.py

Round 4 (audit 2026-08-10) found that two of the A4 gates shipped never having
been observed failing: gate 5's JUDGMENT orphan check was dead code (its regex
could never match the deck), and gate 1b's own prescribed bypass could not
satisfy it. A gate that has never been seen red is untested by definition —
this suite runs every gate to refusal AND to acceptance in a scratch copy of
the repo. Case IDs reference `analysis_2026-08-10_findings_table.md`.

Runs offline: HOOPS_VERIFY_OFFLINE pins verify to the evidence file (ESPN's feed may answer since 2026-10-01; the cases need the file).
Repo files are never touched; everything happens in a temp copy. ~60s.
"""
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
FAILURES = []
CASES = 0


def check(name, out, must_have=(), must_not=(), want_exit=None, got_exit=None):
    global CASES
    CASES += 1
    bad = [f"missing: {s}" for s in must_have if s not in out]
    bad += [f"forbidden: {s}" for s in must_not if s in out]
    if want_exit is not None and got_exit != want_exit:
        bad.append(f"exit {got_exit}, wanted {want_exit}")
    if bad:
        FAILURES.append((name, bad, out.strip()[:700]))
        print(f"  FAIL  {name}")
    else:
        print(f"  ok    {name}")


def run(cwd, *args, kit=None):
    env = dict(os.environ)
    env["KIT_REPO"] = kit or os.path.join(os.path.dirname(cwd), "kit")  # F7
    # The suite's cases mutate the evidence file to make the gates fire, so
    # verify must read it, not ESPN's live feed — which first answered from
    # this environment on 2026-10-01 and left the suite red twice (three
    # suffix-form rows unmatched, then a mid-loop TLS timeout).
    env["HOOPS_VERIFY_OFFLINE"] = "1"
    r = subprocess.run([sys.executable, *args], capture_output=True,
                       text=True, cwd=cwd, env=env)
    return r.stdout + r.stderr, r.returncode


def fresh_copy():
    tmp = tempfile.mkdtemp(prefix="gates-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(
        ".git", "results", "__pycache__"))
    # arena/results + mocks excluded for speed; recreate what the tools need
    os.makedirs(os.path.join(dst, "arena", "results"), exist_ok=True)
    # F7/F8: the committed snapshots belong to the REAL kit; the synthesized
    # kit beside this copy defines its own baseline on its first build
    for snap in ("kit-snapshot.csv", "market-snapshot.csv"):
        try:
            os.remove(os.path.join(dst, "data", snap))
        except FileNotFoundError:
            pass
    fake_kit(dst)
    return dst


def fake_kit(repo):
    """F7: a kit checkout beside the repo copy whose projection lines equal the
    pool's and whose GP encodes the deck's exclusion class — the state in which
    the cross-plane gate must pass. Cases mutate it to see the gate fire."""
    import csv
    kit = os.path.join(os.path.dirname(repo), "kit")
    os.makedirs(os.path.join(kit, "report"), exist_ok=True)
    with open(os.path.join(repo, "data", "players.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(os.path.join(kit, "report", "projections-2026-27.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "team", "pos", "gp", "mpg", "fgp", "fga", "ftp", "fta",
                    "tpm", "pts", "reb", "ast", "stl", "blk", "tov"])
        for r in rows:
            tag = re.split(r"[\s(]", (r.get("note") or "").lower(), 1)[0]
            excluded = tag.startswith("out-") or (not tag.endswith("-risk") and "recovery" in tag)
            w.writerow([r["player"], r["team"], r["pos"], 15 if excluded else 72, 30,
                        r["fg_pct"], r["fga"], r["ft_pct"], r["fta"], r["tpm"], r["pts"],
                        r["reb"], r["ast"], r["stl"], r["blk"], r["tov"]])
    # F8: a Yahoo price file — ADP for the first 150 pool rows, XRank only
    # for the next 50, nothing for the rest (the unpriced tail)
    os.makedirs(os.path.join(kit, "report", "market"), exist_ok=True)
    with open(os.path.join(kit, "report", "market", "yahoo-2026-09-15.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["player", "team", "pos", "xrank", "adp"])
        for i, r in enumerate(rows[:200]):
            w.writerow([r["player"], r["team"], r["pos"], i + 1, (i + 1) if i < 150 else ""])
    return kit


def prime(repo, pool_changes=None):
    """Re-date the evidence to today, verify, stamp — the legitimate path."""
    today = datetime.date.today().isoformat()
    ev = os.path.join(repo, "data", "rosters_official.json")
    d = json.load(open(ev))
    d["date"] = today
    json.dump(d, open(ev, "w"), indent=2)
    out, rc = run(repo, "scripts/verify_rosters.py")
    note = "gate-suite prime"
    if rc != 0 and "mismatches: 0" in out and "UNMATCHED (" in out:
        # WO-2 (2026-10-01): the evidence file now mirrors ESPN's live feed, so
        # a pool row the feed has not posted yet (a day-old camp signee) is
        # UNMATCHED here too, never a mismatch. The real pull exempts such
        # rows by name with --allow-unmatched and says so in the stamp note;
        # the prime walks the same path. A MISMATCH still fails the prime.
        out, rc = run(repo, "scripts/verify_rosters.py", "--allow-unmatched")
        note += " (unmatched rows exempted by name, 0 mismatches)"
    assert rc == 0, out[:400]
    args = ["scripts/hoops.py", "freshness", "--stamp",
            "--rosters-verified", "test", "--note", note]
    if pool_changes is not None:
        args += pool_changes
    return run(repo, *args)


def redate_judgment(repo):
    today = datetime.date.today().isoformat()
    p = os.path.join(repo, "docs", "draft-deck.html")
    s = open(p, encoding="utf-8").read()
    if f'const JUDGMENT = {{\n  date: "{today}"' in s:
        return  # already re-dated (idempotent for repeated primes)
    s2 = re.sub(r'(const JUDGMENT = \{\n  date: )"\d{4}-\d{2}-\d{2}"',
                rf'\g<1>"{today}"', s, count=1)
    assert s2 != s, "JUDGMENT date anchor not found"
    open(p, "w", encoding="utf-8").write(s2)


def set_colophon_count(repo, n):
    """Gate 6: a test that mutates the pool size must keep the colophon
    truthful — the same discipline the gate enforces on real pulls."""
    p = os.path.join(repo, "docs", "draft-deck.html")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"\b\d+ rows\b", f"{n} rows", s)
    s = re.sub(r"\b\d{3,}/\d{3,}\b", f"{n}/{n}", s)
    s = re.sub(r"\b\d+-player pool\b", f"{n}-player pool", s)
    open(p, "w", encoding="utf-8").write(s)


def redate_colophon(repo):
    """Gate 6 (F4/D-S6) requires the colophon to narrate today's pull."""
    today = datetime.date.today()
    p = os.path.join(repo, "docs", "draft-deck.html")
    s = open(p, encoding="utf-8").read()
    s2 = re.sub(r"This refresh \(\d{1,2}/\d{1,2}",
                f"This refresh ({today.month}/{today.day}", s, count=1)
    assert "This refresh (" in s2, "colophon refresh anchor not found"
    open(p, "w", encoding="utf-8").write(s2)


def main():
    print("publish-gate regression suite\n")
    today = datetime.date.today().isoformat()

    # ---------- baseline: the honest path builds ------------------------
    repo = fresh_copy()
    prime(repo, pool_changes=["--no-pool-changes"])
    redate_judgment(repo)
    redate_colophon(repo)
    out, rc = run(repo, "scripts/build_deck.py")
    check("baseline: honest quiet-day build succeeds", out,
          must_have=["safe to publish"], want_exit=0, got_exit=rc)

    # gate 4 arms itself on that build; a second identical build must refuse
    out, rc = run(repo, "scripts/build_deck.py")
    check("R4-F22 gate 4 armed: unchanged pool + no-changes flag still builds",
          out, must_have=["safe to publish"], want_exit=0, got_exit=rc)

    # ---------- 2026-08-26 pull: malformed row (unquoted comma) ----------
    # An unquoted comma in `note` overflowed into DictReader's restkey and the
    # deck PUBLISHED Sharpe's note truncated at that comma. availability()
    # reads the leading tag only, so the math never moved and no gate caught it.
    pool_path = os.path.join(repo, "data", "players.csv")
    saved = open(pool_path, encoding="utf-8").read()
    with open(pool_path, "a") as f:
        f.write("Comma Guy,ZZZ,PG,0.42,5.0,0.8,1.0,0.5,4.0,1.5,1.5,"
                "0.4,0.1,0.8,knee-recovery (8/24, ~6mo)\n")
    out, rc = run(repo, "scripts/hoops.py", "validate")
    check("a comma-split row fails loudly instead of truncating a note", out,
          must_have=["Comma Guy", "extra field"], want_exit=1, got_exit=rc)
    with open(pool_path, "w", encoding="utf-8") as f:  # same row, quoted
        f.write(saved + 'Comma Guy,ZZZ,PG,0.42,5.0,0.8,1.0,0.5,4.0,1.5,1.5,'
                '0.4,0.1,0.8,"knee-recovery (8/24, ~6mo)"\n')
    out, rc = run(repo, "scripts/hoops.py", "validate")
    check("the same row QUOTED loads with its note intact", out,
          must_not=["extra field"])
    with open(pool_path, "w", encoding="utf-8") as f:
        f.write(saved)

    # ---------- R4-F05/R3: unmatched rows and the recorded bypass -------
    with open(os.path.join(repo, "data", "players.csv"), "a") as f:
        f.write("Testy McTest,ZZZ,PG,0.42,5.0,0.8,1.0,0.5,4.0,1.5,1.5,"
                "0.4,0.1,0.8,\n")
    out, rc = run(repo, "scripts/verify_rosters.py")
    # WO-2: the count is no longer always 1 (a camp signee the feed lacks is
    # unmatched too); the case tests that an unmatched row hard-fails.
    check("R4-F05 unmatched row without the flag still hard-fails", out,
          must_have=["UNMATCHED (", "Testy McTest"], want_exit=1, got_exit=rc)
    out, rc = run(repo, "scripts/verify_rosters.py", "--allow-unmatched")
    ver = json.load(open(os.path.join(repo, "data",
                                      "roster_verification.json")))
    check("R4-F05 --allow-unmatched records itself in the artifact",
          out + f" [allow={ver.get('allow_unmatched')}]",
          must_have=["[allow=True]"], want_exit=0, got_exit=rc)
    out, rc = run(repo, "scripts/hoops.py", "freshness", "--stamp",
                  "--rosters-verified", "test",
                  "--note", "gate-suite: Testy added",
                  "--pool-changes", "added Testy McTest")
    assert rc == 0, out[:400]
    # pool grew by Testy; gate 6 checks prose. Count at RUNTIME, never a
    # literal — a hardcoded size stales the moment the real pool changes
    # (2026-09-21: pool 255 -> 264 broke the old `256`; same class as the
    # test_draft surname fixture that staled on the Mark Williams exclusion).
    n_pool = sum(1 for _ in open(os.path.join(repo, "data", "players.csv"))) - 1
    set_colophon_count(repo, n_pool)
    out, rc = run(repo, "scripts/build_deck.py")
    check("R4-F05 gate 1b accepts the RECORDED bypass, loudly", out,
          must_have=["safe to publish", "Testy McTest"],
          want_exit=0, got_exit=rc)

    # ---------- R4-F21: gate 5's orphan check must actually fire --------
    p = os.path.join(repo, "docs", "draft-deck.html")
    s = open(p, encoding="utf-8").read()
    anchor = "\n  players: {\n"
    assert anchor in s
    s = s.replace(anchor, anchor + '    "Fake Orphan Player": '
                  '{ adj: -0.5, why: "gate-suite mutation" },\n', 1)
    open(p, "w", encoding="utf-8").write(s)
    out, rc = run(repo, "scripts/hoops.py", "freshness", "--stamp",
                  "--rosters-verified", "test",
                  "--note", "gate-suite: orphan case", "--no-pool-changes")
    assert rc == 0, out[:400]
    out, rc = run(repo, "scripts/build_deck.py")
    check("R4-F21 JUDGMENT orphan mutation is REFUSED by name", out,
          must_have=["Fake Orphan Player"], want_exit=1, got_exit=rc)

    # ---------- R4-F22: gate 4's explicit-assertion semantics -----------
    repo2 = fresh_copy()
    prime(repo2)  # stamp WITHOUT any pool_changes flag
    redate_judgment(repo2)
    redate_colophon(repo2)
    out, rc = run(repo2, "scripts/build_deck.py")
    check("R4-F22 no pool_changes assertion -> build refuses (no silent skip)",
          out, must_have=["pool_changes", "BUILD REFUSED"],
          want_exit=1, got_exit=rc)
    prime(repo2, pool_changes=["--no-pool-changes"])
    redate_judgment(repo2)
    redate_colophon(repo2)
    out, rc = run(repo2, "scripts/build_deck.py")
    assert rc == 0, out[:400]
    # now claim changes happened while the pool is byte-identical
    prime(repo2, pool_changes=["--pool-changes", "big trade (a lie)"])
    out, rc = run(repo2, "scripts/build_deck.py")
    check("R4-F22 'changed' assertion vs identical pool -> contradiction refused",
          out, must_have=["BUILD REFUSED"], want_exit=1, got_exit=rc)
    # keyword-in-prose must no longer bypass: a note containing 'quiet' but
    # no structured flag
    out, rc = run(repo2, "scripts/hoops.py", "freshness", "--stamp",
                  "--rosters-verified", "test",
                  "--note", "quiet on injuries; MAJOR trade pending")
    assert rc == 0, out[:400]
    out, rc = run(repo2, "scripts/build_deck.py")
    check("R4-F22 the word 'quiet' in prose no longer publishes", out,
          must_have=["BUILD REFUSED"], want_exit=1, got_exit=rc)

    # ---------- F4/D-S6 (2026-09-08): gate 6 colophon truth checks ------
    # The Data paragraph drifted two consecutive pulls (narrated the 8/18
    # pull, counted 254 rows against a 255-row pool, claimed a lifted hold
    # was still on). Gate 6 must refuse a count that contradicts the pool
    # and a narration of the wrong pull — and accept the corrected page.
    repo4 = fresh_copy()
    prime(repo4, pool_changes=["--no-pool-changes"])
    redate_judgment(repo4)
    redate_colophon(repo4)
    p4 = os.path.join(repo4, "docs", "draft-deck.html")
    saved4 = open(p4, encoding="utf-8").read()
    n_rows = saved4.count("\n") and len(  # actual pool size, from the CSV
        open(os.path.join(repo4, "data", "players.csv"),
             encoding="utf-8").read().strip().splitlines()) - 1
    wrong = saved4.replace(f"{n_rows} rows", f"{n_rows - 1} rows", 1)
    assert wrong != saved4, "colophon row-count token not found"
    open(p4, "w", encoding="utf-8").write(wrong)
    out, rc = run(repo4, "scripts/build_deck.py")
    check("F4 gate 6: colophon row count contradicting the pool is REFUSED",
          out, must_have=["colophon count", str(n_rows - 1)],
          want_exit=1, got_exit=rc)
    stale = re.sub(r"This refresh \(\d{1,2}/\d{1,2}",
                   "This refresh (1/1", saved4, count=1)
    open(p4, "w", encoding="utf-8").write(stale)
    out, rc = run(repo4, "scripts/build_deck.py")
    check("F4 gate 6: colophon narrating the WRONG pull is REFUSED", out,
          must_have=["narrates the wrong pull"], want_exit=1, got_exit=rc)
    open(p4, "w", encoding="utf-8").write(saved4)
    out, rc = run(repo4, "scripts/build_deck.py")
    check("F4 gate 6: the corrected colophon builds", out,
          must_have=["safe to publish"], want_exit=0, got_exit=rc)

    # ---------- R4-F24: --quick must not clobber committed evidence -----
    repo3 = fresh_copy()
    decoy = os.path.join(repo3, "arena", "results",
                         "bench_weight_study_quick_out.json")
    json.dump({"seasons_per_seed": 9999, "seeds": [1]}, open(decoy, "w"))
    out, rc = run(repo3, "arena/mocks/bench_weight_study.py", "--quick")
    check("R4-F24 --quick refuses to overwrite mismatched evidence, fast",
          out, must_have=["refus"], want_exit=1, got_exit=rc)

    # ---------- 2026-09-21 pull: unicode in a pool note ------------------
    # json.dumps escapes non-ASCII to \uXXXX; a raw re.subn replacement
    # template rejects that ("bad escape \u"). Seen RED on the live 9/21
    # build (the Doncic em-dash note crashed the PLAYERS injection); the fix
    # is the callable-replacement pattern build_deck already uses for
    # BUILD_NOTE. This case pins it.
    repo4 = fresh_copy()
    pl = os.path.join(repo4, "data", "players.csv")
    rows = open(pl, encoding="utf-8").read().splitlines()
    rows[-1] = rows[-1].rsplit(",", 1)[0] + ",\u00e9-note \u2014 unicode survives injection"
    open(pl, "w", encoding="utf-8").write("\n".join(rows) + "\n")
    prime(repo4, pool_changes=["--pool-changes", "unicode-note regression case"])
    redate_judgment(repo4)
    redate_colophon(repo4)
    out, rc = run(repo4, "scripts/build_deck.py")
    check("non-ASCII pool note survives the PLAYERS injection", out,
          must_have=["safe to publish"], must_not=["bad escape"],
          want_exit=0, got_exit=rc)

    # ---------- F7 (2026-09-21): cross-plane consistency gate ------------
    # Mock 51: the kit's 9/16 bench downgrade of Sheppard never reached the
    # deck; the owner drafted him off the stale row. The gate refuses on team,
    # exclusion class, spelling drift, and a line that moved on one plane
    # since the last build without moving on the other (waivable by name,
    # recorded in the manifest). Lines otherwise differ by design.
    repo7 = fresh_copy()
    prime(repo7, pool_changes=["--no-pool-changes"])
    redate_judgment(repo7)
    redate_colophon(repo7)
    proj7 = os.path.join(os.path.dirname(repo7), "kit", "report", "projections-2026-27.csv")
    deck7 = os.path.join(repo7, "docs", "draft-deck.html")
    out, rc = run(repo7, "scripts/build_deck.py")
    check("F7 baseline: kit lines equal the pool -> builds and reports the planes", out,
          must_have=["safe to publish", "planes:"], want_exit=0, got_exit=rc)
    check("F7 baseline wrote data/kit-snapshot.csv",
          "present" if os.path.exists(os.path.join(repo7, "data", "kit-snapshot.csv")) else "absent",
          must_have=["present"])
    orig7 = open(proj7, encoding="utf-8").read()
    open(proj7, "w", encoding="utf-8").write(orig7.replace("Nikola Jokic,DEN,", "Nikola Jokic,LAL,", 1))
    out, rc = run(repo7, "scripts/build_deck.py")
    check("F7 team mismatch is REFUSED by name", out,
          must_have=["BUILD REFUSED", "Nikola Jokic", "team"], want_exit=1, got_exit=rc)
    rows7 = orig7.splitlines()
    j = next(i for i, l in enumerate(rows7) if l.startswith("Nikola Jokic,"))
    parts = rows7[j].split(",")
    parts[3] = "10"
    rows7[j] = ",".join(parts)
    open(proj7, "w", encoding="utf-8").write("\n".join(rows7) + "\n")
    out, rc = run(repo7, "scripts/build_deck.py")
    check("F7 exclusion-class mismatch (kit GP 10, deck playable) is REFUSED", out,
          must_have=["BUILD REFUSED", "Nikola Jokic", "exclusion"], want_exit=1, got_exit=rc)
    parts[3] = "72"
    parts[10] = "35.0"  # pts: the kit re-derives a line the deck never received
    rows7[j] = ",".join(parts)
    open(proj7, "w", encoding="utf-8").write("\n".join(rows7) + "\n")
    out, rc = run(repo7, "scripts/build_deck.py")
    check("F7 a kit re-derivation not carried to the deck is REFUSED (the Sheppard case)", out,
          must_have=["BUILD REFUSED", "Nikola Jokic", "pts"], want_exit=1, got_exit=rc)
    out, rc = run(repo7, "scripts/build_deck.py", "--planes-waive", "Nikola Jokic: gate-suite waiver")
    check("F7 the same re-derivation with a recorded waiver builds", out,
          must_have=["safe to publish", "waived"], want_exit=0, got_exit=rc)
    m7 = re.search(r"<!-- build-manifest (\{.*?\}) -->", open(deck7, encoding="utf-8").read())
    check("F7 the waiver is recorded in the build manifest", m7.group(1) if m7 else "",
          must_have=["Nikola Jokic"])
    # ---------- WO-1 (2026-10-01): stat-line drift between the planes -----
    # The kit's Jokic line now differs from the pool's (pts 35.0 vs the pool's)
    # and both snapshots carry it, so propagation is clean. Lines differ by
    # design (184 of 314 shared rows on 2026-10-01, Lillard 17.0 vs 24.0 pts
    # among them), so the gate REPORTS them as a warning and counts them in
    # the manifest; --planes-lines-strict (the final build) refuses.
    out, rc = run(repo7, "scripts/build_deck.py")
    check("WO-1 a differing stat line is REPORTED as a warning and the build still passes", out,
          must_have=["safe to publish", "lines 1", "Nikola Jokic"], want_exit=0, got_exit=rc)
    m7 = re.search(r"<!-- build-manifest (\{.*?\}) -->", open(deck7, encoding="utf-8").read())
    check("WO-1 the manifest carries the differing-lines count", m7.group(1) if m7 else "",
          must_have=['"lines": 1'])
    out, rc = run(repo7, "scripts/build_deck.py", "--planes-lines-strict")
    check("WO-1 --planes-lines-strict REFUSES on the same line", out,
          must_have=["BUILD REFUSED", "lines", "Nikola Jokic"], want_exit=1, got_exit=rc)
    out, rc = run(repo7, "scripts/build_deck.py", kit=os.path.join(os.path.dirname(repo7), "no-such-kit"))
    check("F7 a missing kit checkout is REFUSED", out,
          must_have=["BUILD REFUSED", "kit"], want_exit=1, got_exit=rc)
    out, rc = run(repo7, "scripts/build_deck.py", "--no-plane-check", "gate-suite: kit unavailable",
                  kit=os.path.join(os.path.dirname(repo7), "no-such-kit"))
    check("F7 a recorded bypass builds and the manifest carries it", out,
          must_have=["safe to publish", "bypass"], want_exit=0, got_exit=rc)
    m7 = re.search(r"<!-- build-manifest (\{.*?\}) -->", open(deck7, encoding="utf-8").read())
    check("F7 the bypass reason is in the manifest", m7.group(1) if m7 else "",
          must_have=["kit unavailable"])

    # ---------- F8 (2026-09-22): Yahoo prices into the Mkt rank -----------
    # Owner decision 2026-09-21 ("use Yahoo Mkt price"); the 8/21 work order's
    # gated step 5. The build bakes ADP-else-XRank from the kit's newest paste,
    # writes data/market-snapshot.csv for the Python twin, records the file in
    # the manifest, refuses when a spelling strands a top-board name, warns on
    # a stale file, and falls back to the internal model loudly with no file.
    repo8 = fresh_copy()
    prime(repo8, pool_changes=["--no-pool-changes"])
    redate_judgment(repo8)
    redate_colophon(repo8)
    yfile = os.path.join(os.path.dirname(repo8), "kit", "report", "market", "yahoo-2026-09-15.csv")
    deck8 = os.path.join(repo8, "docs", "draft-deck.html")
    snap8 = os.path.join(repo8, "data", "market-snapshot.csv")
    manifest8 = lambda: (re.search(r"<!-- build-manifest (\{.*?\}) -->", open(deck8, encoding="utf-8").read()) or re.search("()", "")).group(1)
    out, rc = run(repo8, "scripts/build_deck.py")
    check("F8 baseline: the build bakes Yahoo prices and reports the file", out,
          must_have=["safe to publish", "market: yahoo-2026-09-15.csv"], want_exit=0, got_exit=rc)
    check("F8 manifest records the price file and the priced count", manifest8(),
          must_have=["yahoo-2026-09-15", '"priced": 200'])
    check("F8 snapshot written with the 200 priced rows",
          str(sum(1 for _ in open(snap8, encoding="utf-8")) - 1) if os.path.exists(snap8) else "absent",
          must_have=["200"])
    out, rc = run(repo8, "scripts/check_parity.py")
    check("F8 parity item 6: market ranks agree in the built copy, PRICED", out,
          must_have=["PARITY: EXACT MATCH", "market ranks compared"], must_not=["(priced 0)"],
          want_exit=0, got_exit=rc)
    y8 = open(yfile, encoding="utf-8").read()
    open(yfile, "w", encoding="utf-8").write(y8.replace("Nikola Jokic,", "Nik Jokic,", 1))
    out, rc = run(repo8, "scripts/build_deck.py")
    check("F8 a price-file spelling that strands a top-board name is REFUSED", out,
          must_have=["BUILD REFUSED", "Jokic"], want_exit=1, got_exit=rc)
    open(yfile, "w", encoding="utf-8").write(y8)
    stale8 = yfile.replace("2026-09-15", "2026-01-01")
    os.rename(yfile, stale8)
    out, rc = run(repo8, "scripts/build_deck.py")
    check("F8 a stale price file warns and still builds", out,
          must_have=["safe to publish", "days old"], want_exit=0, got_exit=rc)
    os.rename(stale8, yfile)
    os.remove(yfile)
    out, rc = run(repo8, "scripts/build_deck.py")
    check("F8 no price file: builds on the internal model, loudly", out,
          must_have=["safe to publish", "no Yahoo price file"], want_exit=0, got_exit=rc)
    check("F8 no price file: manifest records market null and the snapshot is gone",
          manifest8() + (" snapshot-absent" if not os.path.exists(snap8) else " snapshot-present"),
          must_have=['"market": null', "snapshot-absent"])

    # D-RN-1 (owner 2026-10-08): the standing repeat-name market check. A player who is the
    # card's 🎯 in MIN_MOCKS (5) or more graded mocks while his value rank and market rank sit
    # MIN_GAP (25) or more places apart — or who has no Yahoo price — is flagged for an
    # outside-source check at every refresh, and --check-report refuses a report without a row
    # for him. Synthetic replays (--cards) pin both boundaries: exactly 5 mocks and exactly 25
    # places flag; 4 mocks or 24 places do not; the 🎯 marker wins over rank 1.
    print("\n[D-RN-1] repeat-name market check")
    repo_rn = fresh_copy()
    kit_rn = os.path.join(os.path.dirname(repo_rn), "kit")
    src_rn = open(os.path.join(repo_rn, "docs", "draft-deck.html"), encoding="utf-8").read()
    data_rn = re.search(r'<script id="data">([\s\S]*?)</script>', src_rn).group(1)
    players_rn = json.loads(re.search(r"const PLAYERS = (\[.*?\]);\n", data_rn, re.S).group(1))
    priced = [p["n"] for p in players_rn if p.get("mkt")]
    unpriced = [p["n"] for p in players_rn if not p.get("mkt") and p.get("av", 0) > 0]
    X, Z, W, U = priced[0], priced[1], priced[2], unpriced[0]
    ranks_rn = {X: (30, 55), Z: (40, 64), W: (20, 80), U: (100, 110)}

    def row_rn(n, rank, target=True):
        v, m = ranks_rn[n]
        return {"rank": rank, "n": n, "target": target, "valRank": v, "mkt": m}

    turns_rn = {
        1: [[X], [Z], [W]],
        2: [[X], [Z], [U], [W]],
        3: [[X], [Z], [U], [W]],
        4: [[X], [Z], [U], [W]],
        5: [[X], [Z], [U]],
        6: [[W, Z], [U]],  # rank 1 is W but the 🎯 is Z: the marker decides, so W stays at 4 mocks
    }
    cards_rn = os.path.join(os.path.dirname(repo_rn), "cards")
    os.makedirs(cards_rn)
    for m, turns in turns_rn.items():
        out_turns = []
        for i, names in enumerate(turns):
            rows = ([row_rn(names[0], 1)] if len(names) == 1
                    else [row_rn(names[0], 1, target=False), row_rn(names[1], 2, target=True)])
            out_turns.append({"pick": 10 + i, "rows": rows})
        json.dump(out_turns, open(os.path.join(cards_rn, f"m{m}.json"), "w"))
    open(os.path.join(cards_rn, "m7.json"), "w").write("{not json")  # a replay that cannot be read
    rn_json = os.path.join(os.path.dirname(repo_rn), "rn.json")
    out, rc = run(repo_rn, "scripts/repeat_market_check.py", "--cards", cards_rn,
                  "--kit", kit_rn, "--json", rn_json, kit=kit_rn)
    check("RN: 5 mocks and 25 places flag; no Yahoo price flags; an unreadable replay is named",
          out, must_have=["FLAGGED", X, U, "no Yahoo price", "6 of 7 mocks", "mock 7"],
          must_not=[W], want_exit=0, got_exit=rc)
    try:
        rec = json.load(open(rn_json, encoding="utf-8"))
        got = "flagged=" + "|".join(sorted(r["player"] for r in rec["flagged"]))
        got += " counts=" + "|".join(f"{n}:{rec['counts'].get(n)}" for n in (X, Z, W, U))
    except (OSError, ValueError, KeyError) as e:
        got = f"no record: {e}"
    check("RN: the record flags exactly the boundary cases (24 places and 4 mocks do not flag)",
          got, must_have=["flagged=" + "|".join(sorted([X, U])), f"{X}:5", f"{Z}:6", f"{W}:4", f"{U}:5"])

    def report_rn(name, body):
        p = os.path.join(os.path.dirname(repo_rn), f"report-{name}.md")
        open(p, "w", encoding="utf-8").write("# After-report\n\n" + body + "\n## Bounds\n\nnone\n")
        return p

    table_rn = ("## Repeat-name market check\n\n| player | mocks | verdict |\n|---|---|---|\n"
                f"| {X} | 5 | SOURCES SPLIT |\n| {U} | 5 | SOURCES SPLIT |\n")
    out, rc = run(repo_rn, "scripts/repeat_market_check.py", "--cards", cards_rn, "--kit", kit_rn,
                  "--check-report", report_rn("ok", table_rn), kit=kit_rn)
    check("RN --check-report: every flagged name has a row, PASS", out,
          must_have=["REPEAT-NAME CHECK: PASS"], want_exit=0, got_exit=rc)
    only_x = ("## Repeat-name market check\n\n| player | mocks | verdict |\n|---|---|---|\n"
              f"| {X} | 5 | SOURCES SPLIT |\n\n{U} is discussed in prose but has no row.\n")
    out, rc = run(repo_rn, "scripts/repeat_market_check.py", "--cards", cards_rn, "--kit", kit_rn,
                  "--check-report", report_rn("missing", only_x), kit=kit_rn)
    check("RN --check-report: a flagged name without a table row FAILS and is named", out,
          must_have=["REPEAT-NAME CHECK: FAIL", U], want_exit=1, got_exit=rc)
    out, rc = run(repo_rn, "scripts/repeat_market_check.py", "--cards", cards_rn, "--kit", kit_rn,
                  "--check-report", report_rn("noheading", "## Open-item receipts\n\n| a | b |\n|---|---|\n"),
                  kit=kit_rn)
    check("RN --check-report: a report without the section FAILS", out,
          must_have=["REPEAT-NAME CHECK: FAIL", "no 'Repeat-name market check' section"],
          want_exit=1, got_exit=rc)

    print()
    if FAILURES:
        for name, bad, out in FAILURES:
            print(f"\nFAILED: {name}")
            for b in bad:
                print(f"  {b}")
            print("  --- output ---")
            for line in out.splitlines()[:14]:
                print(f"  {line}")
        print(f"\n{len(FAILURES)} of {CASES} cases FAILED")
        sys.exit(1)
    print(f"all {CASES} cases passed")


if __name__ == "__main__":
    main()
