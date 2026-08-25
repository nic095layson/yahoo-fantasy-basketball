#!/usr/bin/env python3
"""Live-draft smoke suite — run before every draft, real or mock.

    python3 scripts/test_draft.py

Zero tests existed for the draft loop until 2026-08-09 (audit F64), which is
how the defects below reached a system two audits deep. Each case names the
audit finding it pins. Stdlib only; runs in a scratch dir; ~15s.

Exit 0 = every case passed. Any failure prints the case, the expectation, and
the actual output.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOOPS = os.path.join(HERE, "hoops.py")
FAILURES = []
CASES = 0


def run(state, *args, expect_fail=False):
    env = dict(os.environ, HOOPS_DRAFT_STATE=state)
    r = subprocess.run([sys.executable, HOOPS, *args], capture_output=True,
                       text=True, env=env)
    if expect_fail and r.returncode == 0:
        return r.stdout + r.stderr + "\n[UNEXPECTED SUCCESS]"
    return r.stdout + r.stderr


def check(name, out, must_have=(), must_not=()):
    global CASES
    CASES += 1
    bad = [s for s in must_have if s not in out] + \
          [f"(forbidden) {s}" for s in must_not if s in out]
    if bad:
        FAILURES.append((name, bad, out.strip()[:900]))
        print(f"  FAIL  {name}")
    else:
        print(f"  ok    {name}")


def fresh(state, slot=4, size=13, teams=12):
    for suffix in ("", ".bak", ".tmp"):
        try:
            os.remove(state + suffix)
        except OSError:
            pass
    run(state, "draft", "init", "--teams", str(teams), "--size", str(size),
        "--slot", str(slot))


def main():
    global CASES
    tmp = tempfile.mkdtemp(prefix="hoops-test-")
    st = os.path.join(tmp, "ds.json")
    try:
        print("live-draft smoke suite\n")

        # F02 — degenerate feed segments must never fabricate a pick
        fresh(st)
        out = run(st, "draft", "turn", "Nikola Jokic; .; -", "--top", "0")
        check("F02 punctuation segments log UNKNOWN, not a real player", out,
              must_have=["#1 R1: Nikola Jokic", "UNKNOWN"],
              must_not=["Jaren Jackson Jr. → T2",
                        "Shai Gilgeous-Alexander → T3"])

        fresh(st)
        out = run(st, "draft", "turn", "Nikola Jokic; my:; Victor Wembanyama",
                  "--top", "0")
        check("F02 a bare 'my:' does not hand you the board's best player", out,
              must_have=["UNKNOWN"],
              must_not=["Victor Wembanyama → T4"])

        # F02 — but two-letter nicknames must still resolve
        fresh(st)
        out = run(st, "draft", "turn", "KD; AD; OG; Zu", "--top", "0")
        check("F02 two-letter nicknames survive the length guard", out,
              must_have=["Kevin Durant", "Anthony Davis", "OG Anunoby",
                         "Ivica Zubac"])

        # F27 — accented feeds (Yahoo/ESPN render what the pool does not carry)
        fresh(st)
        out = run(st, "draft", "turn",
                  "Nikola Jokić; Luka Dončić; "
                  "Alperen Şengün", "--top", "0")
        check("F27 accented names match instead of becoming UNKNOWN", out,
              must_have=["Nikola Jokic", "Luka Doncic", "Alperen Sengun"],
              must_not=["UNKNOWN"])

        # F22 — suffixed players must be reachable by the fuzzy typo stage
        fresh(st)
        out = run(st, "draft", "turn", "jacksn; porrter; livley", "--top", "0")
        check("F22 typos on Jr./II names resolve to the right player", out,
              must_have=["Jaren Jackson Jr.", "Porter Jr.",
                         "Dereck Lively II"])

        # F31 — the correction echo must show the OLD name on the left
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; SGA; my:Luka", "--top", "0")
        out = run(st, "draft", "fix", "2", "Anthony Edwards")
        check("F31 draft fix echoes the prior name, not the new one", out,
              must_have=["Victor Wembanyama → Anthony Edwards"])

        # F30 — --slot range is validated on BOTH fix branches
        out = run(st, "draft", "fix", "3", "UNKNOWN #3", "--slot", "99",
                  expect_fail=True)
        check("F30 out-of-range --slot is refused on the UNKNOWN branch", out,
              must_have=["--slot must be between 1 and 12"])
        check("F30 state stays loadable after the refusal",
              run(st, "draft", "status"), must_have=["Draft:"],
              must_not=["Traceback"])

        # F29 — UNKNOWNs are counted, banner persists on every later card
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; SGA; my:Nobody McNobody",
            "--top", "0")
        out = run(st, "draft", "turn", "Trae Young", "--top", "0")
        check("F29 UNKNOWN banner persists past the batch that caused it", out,
              must_have=["of YOUR picks are UNKNOWN", "roster 1/13"])

        # F52 — no phantom picks past the end of the draft
        fresh(st)
        big = "; ".join(["Jokic"] * 1)
        run(st, "draft", "turn", big, "--top", "0")
        import json
        with open(st) as f:
            s = json.load(f)
        s["picks"] = [{"player": f"UNKNOWN #{i + 1}", "slot": (i % 12) + 1}
                      for i in range(156)]
        with open(st, "w") as f:
            json.dump(s, f)
        out = run(st, "draft", "turn", "Trae Young", "--top", "0")
        check("F52 turn refuses to log pick 157", out,
              must_have=["draft is already complete"])
        out = run(st, "draft", "pick", "Trae Young", expect_fail=True)
        check("F52 pick refuses too", out, must_have=["Draft is complete"])

        # F36 — RESYNC has a mechanism
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby", "--top", "0")
        out = run(st, "draft", "resync",
                  "Jokic; Wemby; SGA; my:Luka; Cade Cunningham", "--top", "0")
        check("F36 resync rebuilds the board from a paste", out,
              must_have=["RESYNC: cleared 2", "#5 R1: Cade Cunningham"])
        out = run(st, "draft", "status", "--tail", "3")
        check("F36 status --tail prints the SYNC tail", out,
              must_have=["Last 3 picks", "#5 R1: Cade Cunningham"])

        # R4-F01 — resync's recovery file must hold the PRIOR board, and an
        # empty paste must be refused. The shipped A5 resync saved twice in
        # one command, so the one-generation .bak ended up holding the WIPED
        # board while the command printed a reassurance that it survived.
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; SGA; my:Luka; Cade Cunningham;"
            " Trae Young", "--top", "0")
        out = run(st, "draft", "resync",
                  "Jokic; Wemby; SGA; my:Luka; Cade Cunningham; Trae Young; "
                  "Anthony Edwards", "--top", "0")
        import json as _json
        pre_path = st + ".pre-resync"
        ok_file = os.path.isfile(pre_path)
        prior = (_json.load(open(pre_path)) if ok_file else {}).get("picks", [])
        check("R4-F01 resync names a recovery file that exists", out,
              must_have=["pre-resync"], must_not=[".bak holds the prior board"])
        check("R4-F01 the recovery file holds the PRIOR 6-pick board",
              f"picks={len(prior)}", must_have=["picks=6"])
        out = run(st, "draft", "resync", "", "--top", "0", expect_fail=True)
        with open(st) as f:
            n_after = len(_json.load(f)["picks"])
        check("R4-F01 empty paste is refused and clears nothing",
              out + f" [picks_after={n_after}]",
              must_have=["RESYNC refused", "[picks_after=7]"])

        # INSERT-AT-N (owner feature 2026-08-24): insert a MISSED pick at #P and
        # shift #P..end down one, recomputing snake slots. Everything downstream
        # re-derives from state["picks"], so a canonical picks array is the job.
        fresh(st)
        run(st, "draft", "turn",
            "Jokic; Wemby; Luka; SGA; Anthony Edwards; Tyrese Haliburton",
            "--top", "0")
        out = run(st, "draft", "insert", "3", "Cade Cunningham")
        picks = _json.load(open(st))["picks"]
        check("INSERT echoes the inserted player and the shift", out,
              must_have=["inserted Cade Cunningham at #3", "shifted"])
        check("INSERT places the new pick at #3 and shifts the tail",
              f"#3={picks[2]['player']} #4={picks[3]['player']} n={len(picks)}",
              must_have=["#3=Cade Cunningham", "#4=Luka Doncic", "n=7"])
        check("INSERT recomputes snake slots positionally",
              "slots_ok=" + str(all(picks[i]["slot"] == i + 1 for i in range(7))),
              must_have=["slots_ok=True"])
        check("INSERT leaves picks before P untouched",
              f"#1={picks[0]['player']} #2={picks[1]['player']}",
              must_have=["#1=Nikola Jokic", "#2=Victor Wembanyama"])
        pre = st + ".pre-insert"
        prior = (_json.load(open(pre)) if os.path.isfile(pre) else {}).get("picks", [])
        check("INSERT saves a pre-insert recovery file holding the prior board",
              f"exists={os.path.isfile(pre)} picks={len(prior)}",
              must_have=["exists=True", "picks=6"])
        out = run(st, "draft", "insert", "999", "Jrue Holiday", expect_fail=True)
        check("INSERT refuses an out-of-range position", out,
              must_have=["out of range"])
        out = run(st, "draft", "insert", "2", "Nikola Jokic", expect_fail=True)
        check("INSERT refuses an already-drafted player", out,
              must_have=["already off the board"])
        out = run(st, "draft", "insert", "2", "Zzzq Nobody Nomatch")
        check("INSERT logs an UNKNOWN placeholder on no match", out,
              must_have=["UNKNOWN"])
        # keeper / non-snake board → refuse and route to RESYNC
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; Luka", "--top", "0")
        _s = _json.load(open(st)); _s["picks"][1]["slot"] = 9
        _json.dump(_s, open(st, "w"))
        out = run(st, "draft", "insert", "2", "Jrue Holiday", expect_fail=True)
        check("INSERT refuses a keeper/non-snake board, routing to RESYNC", out,
              must_have=["non-snake slot", "resync"])
        # full draft → refuse
        fresh(st)
        _s = _json.load(open(st))
        _s["picks"] = [{"player": f"UNKNOWN #{i + 1}", "slot": (i % 12) + 1}
                       for i in range(156)]
        _json.dump(_s, open(st, "w"))
        out = run(st, "draft", "insert", "5", "Jrue Holiday", expect_fail=True)
        check("INSERT refuses when the draft is full", out,
              must_have=["draft is full"])
        # both-triggers: the "N+ Name" token inserts inside a turn feed too
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; Luka; SGA", "--top", "0")
        out = run(st, "draft", "turn", "3+ Cade Cunningham", "--top", "0")
        _p = _json.load(open(st))["picks"]
        check("INSERT token 'N+ Name' inserts and shifts in a turn feed",
              out + f" #3={_p[2]['player']} #4={_p[3]['player']} n={len(_p)}",
              must_have=["inserted Cade Cunningham at #3", "#3=Cade Cunningham",
                         "#4=Luka Doncic", "n=5"])

        # R4-F06 — two-letter real first names must resolve; the <3-char
        # guard shipped rejecting CJ/GG/Ja/AJ/PJ/RJ/VJ as degenerate.
        fresh(st)
        out = run(st, "draft", "turn", "CJ; GG; Ja; PJ; RJ; VJ; AJ",
                  "--top", "0")
        check("R4-F06 two-letter first-name tokens resolve", out,
              must_have=["CJ McCollum", "GG Jackson", "Ja Morant",
                         "PJ Washington", "RJ Barrett", "VJ Edgecombe",
                         "AJ Dybantsa"],
              must_not=["UNKNOWN"])
        # ...while genuinely degenerate segments stay blocked
        fresh(st)
        out = run(st, "draft", "turn", "Jokic; .; a; j", "--top", "0")
        check("R4-F06 degenerate segments still blocked", out,
              must_have=["#1 R1: Nikola Jokic"],
              must_not=["#2 R1: J", "#3 R1: "])

        # F55 — a corrupt state file explains itself and the .bak restores
        shutil.copy(st, st + ".good")
        with open(st, "w") as f:
            f.write('{"teams": 12, "slot"')
        out = run(st, "draft", "status", expect_fail=True)
        check("F55 corrupt state prints recovery, not a traceback", out,
              must_have=["DRAFT STATE CORRUPT", ".bak"],
              must_not=["Traceback"])
        shutil.copy(st + ".bak", st)
        check("F55 the .bak is loadable", run(st, "draft", "status"),
              must_have=["Draft:"], must_not=["Traceback"])
        shutil.copy(st + ".good", st)

        # Guards that predate this suite must still hold.
        fresh(st)
        run(st, "draft", "turn", "Jokic; Wemby; SGA; my:Luka", "--top", "0")
        check("lesson 1 --expect mismatch logs nothing",
              run(st, "draft", "turn", "Trae Young", "--expect", "2",
                  expect_fail=True),
              must_have=["STATE MISMATCH", "Nothing was logged"])
        out = run(st, "draft", "turn", "White", "--top", "0")
        check("ambiguity still auto-resolves with its flag", out,
              must_have=["Derrick White", "assumed over"])
        # draft_state_46 fix: the best namesake (Derrick) is now drafted, so a
        # bare "White" resolves to the LAST one still available (Coby) instead
        # of halting — the "George at pick 109" repair. Old lesson 2 halted
        # here; that halt is what buried the owner mid-draft.
        check("bare surname resolves to the last available namesake",
              run(st, "draft", "turn", "White", "--top", "0"),
              must_have=["Coby White", "already drafted"],
              must_not=["HALTED"])
        out = run(st, "draft", "turn",
                  "1- Trae Young; 2- Bam Adebayo; 3- Alperen Sengun",
                  "--top", "0", expect_fail=True)
        check("3-correction halt rolls the batch back", out,
              must_have=["HALTED", "NO changes from this batch"])
        with open(st) as f:
            names = [p["player"] for p in json.load(f)["picks"][:3]]
        check("3-correction rollback left the board untouched",
              " ".join(names),
              must_have=["Nikola Jokic", "Victor Wembanyama",
                         "Shai Gilgeous-Alexander"])
        # ...but with 2+ namesakes still available AND the best one drafted, a
        # bare surname stays a HALT — genuine ambiguity, the Coby/Dejounte
        # scar. Jalen Williams is the top Williams; drafting him leaves Mark
        # and Ziaire, so "Williams" cannot be auto-resolved.
        fresh(st)
        run(st, "draft", "turn", "Jalen Williams", "--top", "0")
        check("surname collision still halts when 2+ namesakes remain",
              run(st, "draft", "turn", "Williams", "--top", "0",
                  expect_fail=True),
              must_have=["HALTED", "already drafted"])
        # first-name prefix + surname now resolves what the hint promised, and
        # the draft_state_46 scenario end-to-end: two Georges gone, "George"
        # lands the third.
        fresh(st)
        run(st, "draft", "turn", "Paul George; Keyonte George", "--top", "0")
        check("prefix+surname resolves a shared surname (Ky George)",
              run(st, "draft", "turn", "Ky George", "--top", "0"),
              must_have=["Kyshawn George"], must_not=["HALTED", "ambiguous"])
        fresh(st)
        run(st, "draft", "turn", "Paul George; Keyonte George", "--top", "0")
        check("bare surname lands the last George (draft_state_46 #109)",
              run(st, "draft", "turn", "George", "--top", "0"),
              must_have=["Kyshawn George", "already drafted"],
              must_not=["HALTED"])
        fresh(st)
        run(st, "draft", "turn", "Jokic; Trae Young", "--top", "0")
        check("a re-sent drafted name is skipped, never double-logged",
              run(st, "draft", "turn", "Jokic; Trae Young", "--top", "0"),
              must_have=["skipped", "already off the board"])

        # Speed rule: the live turn card must stay well inside the 45s clock.
        fresh(st)
        sys.path.insert(0, HERE)
        import hoops
        pool = [p for p in sorted(hoops.zscores(hoops.load_players()),
                                  key=lambda p: -hoops.adj_value(p))
                if hoops.availability(p) > 0][:155]
        feed = "; ".join(("my:" if hoops.team_of_pick(i, 12) == 4 else "")
                         + p["player"] for i, p in enumerate(pool))
        run(st, "draft", "turn", feed, "--expect", "0", "--top", "0")
        t0 = time.time()
        out = run(st, "draft", "turn", "", "--expect", "155", "--top", "8")
        ms = (time.time() - t0) * 1000
        check("a full-state turn card still renders", out,
              must_have=["YOUR PICK", "vs field", "top rival"])
        CASES += 1
        if ms > 1500:
            FAILURES.append(("turn card speed", [f"{ms:.0f}ms > 1500ms"], ""))
            print(f"  FAIL  turn card at 155 picks took {ms:.0f}ms")
        else:
            print(f"  ok    turn card at 155 picks: {ms:.0f}ms "
                  "(process incl. interpreter start)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if FAILURES:
        for name, bad, out in FAILURES:
            print(f"\nFAILED: {name}")
            for b in bad:
                print(f"  missing: {b}")
            if out:
                print("  --- output ---")
                for line in out.splitlines():
                    print(f"  {line}")
        print(f"\n{len(FAILURES)} of {CASES} cases FAILED")
        sys.exit(1)
    print(f"all {CASES} cases passed")


if __name__ == "__main__":
    main()
