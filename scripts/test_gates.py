#!/usr/bin/env python3
"""Publish-gate regression suite — the gates must be seen to FIRE.

    python3 scripts/test_gates.py

Round 4 (audit 2026-08-10) found that two of the A4 gates shipped never having
been observed failing: gate 5's JUDGMENT orphan check was dead code (its regex
could never match the deck), and gate 1b's own prescribed bypass could not
satisfy it. A gate that has never been seen red is untested by definition —
this suite runs every gate to refusal AND to acceptance in a scratch copy of
the repo. Case IDs reference `analysis_2026-08-10_findings_table.md`.

Runs offline (ESPN is expected blocked → verify runs fallback-partial).
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


def run(cwd, *args):
    r = subprocess.run([sys.executable, *args], capture_output=True,
                       text=True, cwd=cwd)
    return r.stdout + r.stderr, r.returncode


def fresh_copy():
    tmp = tempfile.mkdtemp(prefix="gates-")
    dst = os.path.join(tmp, "repo")
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(
        ".git", "results", "__pycache__"))
    # arena/results + mocks excluded for speed; recreate what the tools need
    os.makedirs(os.path.join(dst, "arena", "results"), exist_ok=True)
    return dst


def prime(repo, pool_changes=None):
    """Re-date the evidence to today, verify, stamp — the legitimate path."""
    today = datetime.date.today().isoformat()
    ev = os.path.join(repo, "data", "rosters_official.json")
    d = json.load(open(ev))
    d["date"] = today
    json.dump(d, open(ev, "w"), indent=2)
    out, rc = run(repo, "scripts/verify_rosters.py")
    assert rc == 0, out[:400]
    args = ["scripts/hoops.py", "freshness", "--stamp",
            "--rosters-verified", "test", "--note", "gate-suite prime"]
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


def main():
    print("publish-gate regression suite\n")
    today = datetime.date.today().isoformat()

    # ---------- baseline: the honest path builds ------------------------
    repo = fresh_copy()
    prime(repo, pool_changes=["--no-pool-changes"])
    redate_judgment(repo)
    out, rc = run(repo, "scripts/build_deck.py")
    check("baseline: honest quiet-day build succeeds", out,
          must_have=["safe to publish"], want_exit=0, got_exit=rc)

    # gate 4 arms itself on that build; a second identical build must refuse
    out, rc = run(repo, "scripts/build_deck.py")
    check("R4-F22 gate 4 armed: unchanged pool + no-changes flag still builds",
          out, must_have=["safe to publish"], want_exit=0, got_exit=rc)

    # ---------- R4-F05/R3: unmatched rows and the recorded bypass -------
    with open(os.path.join(repo, "data", "players.csv"), "a") as f:
        f.write("Testy McTest,ZZZ,PG,0.42,5.0,0.8,1.0,0.5,4.0,1.5,1.5,"
                "0.4,0.1,0.8,\n")
    out, rc = run(repo, "scripts/verify_rosters.py")
    check("R4-F05 unmatched row without the flag still hard-fails", out,
          must_have=["UNMATCHED (1): Testy McTest"], want_exit=1, got_exit=rc)
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
    out, rc = run(repo2, "scripts/build_deck.py")
    check("R4-F22 no pool_changes assertion -> build refuses (no silent skip)",
          out, must_have=["pool_changes", "BUILD REFUSED"],
          want_exit=1, got_exit=rc)
    prime(repo2, pool_changes=["--no-pool-changes"])
    redate_judgment(repo2)
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

    # ---------- R4-F24: --quick must not clobber committed evidence -----
    repo3 = fresh_copy()
    decoy = os.path.join(repo3, "arena", "results",
                         "bench_weight_study_quick_out.json")
    json.dump({"seasons_per_seed": 9999, "seeds": [1]}, open(decoy, "w"))
    out, rc = run(repo3, "arena/mocks/bench_weight_study.py", "--quick")
    check("R4-F24 --quick refuses to overwrite mismatched evidence, fast",
          out, must_have=["refus"], want_exit=1, got_exit=rc)

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
