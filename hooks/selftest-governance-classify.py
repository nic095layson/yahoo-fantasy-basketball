#!/usr/bin/env python3
"""Fixture test for the governance classifier and the two hooks built on it.

Pins (a) the four owner messages of the 2026-10-12 incident as governed work, (b) a should-stay-silent
set including the "draft in" over-fire the 2026-07-15 classifier had, (c) the trigger's output shape,
and (d) the Stop gate's block/allow behaviour on synthetic transcripts. Exit 1 on any mismatch.

Run: python3 hooks/selftest-governance-classify.py        (the guard runs it too)
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from govclass import classify, governors  # noqa: E402

# --- (a) + (b): classification fixture -------------------------------------------------------
CASES = [
    # incident messages, 2026-10-12 (verbatim from after-report-2026-10-13-scope-fence.md)
    ("I don't agree that career averages are being taken into account. Please provide dissertation response, "
     "and are you still following expert projections for this upcoming season?", {"adversarial-verify", "scope-fence"}),
    ("Usage on new team is critical and essential to data computation and modeling.", {"scope-fence"}),
    ("I understand that you are still running your tests. I have concerns about system computational integrity, "
     "as I do not agree with the 20 year test. Majority of players in the NBA (fantasy relevance) have under an "
     "8 year playing career. Data that goes back 20 years is irrelevant and I do not see the significance as the "
     "game, rules, pacing have all changed in that span.", {"adversarial-verify", "scope-fence"}),
    ("We have rules, such as scope-fence in your operating procedure. Was this followed when you decided to "
     "implement 20 year data? I want to ensure your logic and decision making is not regressing and damaging "
     "data integrity.", {"adversarial-verify", "scope-fence", "plan-gate"}),
    # governed work from the house eval sets (abbreviated), should fire
    ("Analyze whether we should migrate our auth to JWTs and recommend an approach.", {"adversarial-verify", "plan-gate"}),
    ("Build a script that processes the three sample files and outputs valid JSON.", {"plan-gate"}),
    ("Can you double-check this migration before I run it in prod?", {"adversarial-verify"}),
    ("Why does the board rank Sabonis above Jokic? I don't agree.", {"adversarial-verify", "scope-fence"}),
    # should stay silent
    ("what's 15% of 80?", set()),
    ("thanks, that's all for tonight", set()),
    ("what time zone is the draft in?", set()),          # 2026-07-15 classifier fired on "draft in"
    ("why is the sky blue?", set()),
    ("ok sounds good, go ahead", set()),
    ("what's the default PostgreSQL port?", set()),
    ("who did the Lakers draft last year?", set()),
    ("[SYSTEM NOTIFICATION - NOT USER INPUT]\n<task-notification>Background command \"rerun the fixture and build the pack\" failed</task-notification>", set()),
    # slash-command echoes are harness text, not the owner (red-team 2026-10-19, attack G5)
    ("<command-name>/model</command-name>\n<command-message>model</command-message>\n<command-args>claude-x</command-args>", set()),
    ("<local-command-stdout>Set model to `claude-x`. Now build the pack.</local-command-stdout>", set()),
]

# Owner prompts the classifier does not match: the advisory cue tier (2026-10-19, D-SV-3 option c)
# fires on a substantive one and stays silent on a short acknowledgement. Never enforced by the gate.
CUE_CASES = [
    ("Please provide new instructions for me to copy and paste, and also the new Skill MD please.", True),
    ("Proceed with all fixes and push.", True),  # sealed set A01, missed by the patterns
    ("re-pasted instructions complete", False),
    ("ok sounds good, go ahead", False),
    ("what's 15% of 80?", False),
    ("thanks, that's all for tonight", False),
]


def run(cmd, stdin_text):
    r = subprocess.run(cmd, input=stdin_text, capture_output=True, text=True)
    return r.stdout.strip()


def main():
    fails = 0
    for text, expected in CASES:
        got = set(governors(classify(text)))
        ok = got == expected
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} classify: {text[:58]!r:62} -> {sorted(got)}" + ("" if ok else f"  expected {sorted(expected)}"))

    # --- (c): trigger output shape ----------------------------------------------------------
    out = run(["python3", os.path.join(HERE, "governance-trigger.py")], json.dumps({"prompt": CASES[0][0]}))
    shaped = False
    try:
        j = json.loads(out)
        h = j["hookSpecificOutput"]
        shaped = h["hookEventName"] == "UserPromptSubmit" and "assessment, not a fix" in h["additionalContext"]
    except Exception:
        pass
    fails += 0 if shaped else 1
    print(f"  {'ok  ' if shaped else 'FAIL'} trigger: dispute message -> UserPromptSubmit additionalContext with the assessment rule")
    # Changed 2026-10-19 (D-SV-3 option c): the trigger now CUES on this prompt — advisory only, the cue
    # text licenses answering directly — where before it was silent. Enforcement silence on it is still
    # pinned above (classify -> set()) and by the gate's trivia row. Was "-> silent" 2026-10-13 to 2026-10-19.
    out = run(["python3", os.path.join(HERE, "governance-trigger.py")], json.dumps({"prompt": "what time zone is the draft in?"}))
    ok = "Governance cue" in out and "auto-trigger" not in out
    fails += 0 if ok else 1
    print(f"  {'ok  ' if ok else 'FAIL'} trigger: 'draft in' trivia -> advisory cue, never the auto-trigger")
    # build class: no "skip if trivial" line (red-team 2026-10-19: taken in 4/4 live build runs, so the
    # governor loaded only after the Stop block; plan-gate's own triage rule is the valve now)
    out = run(["python3", os.path.join(HERE, "governance-trigger.py")], json.dumps({"prompt": CASES[5][0]}))
    ok = "Load plan-gate" in out and "genuinely trivial" not in out
    fails += 0 if ok else 1
    print(f"  {'ok  ' if ok else 'FAIL'} trigger: build prompt -> asks for plan-gate with no skip clause")
    for text, want in CUE_CASES:
        out = run(["python3", os.path.join(HERE, "governance-trigger.py")], json.dumps({"prompt": text}))
        got = "Governance cue" in out
        ok = got == want and ("auto-trigger" not in out)
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} trigger cue tier: {text[:50]!r:54} -> {'cue' if got else 'silent'}" + ("" if ok else f"  expected {'cue' if want else 'silent'}"))

    # --- (d): Stop gate on synthetic transcripts ----------------------------------------------
    def transcript(prompt, skill_loaded, list_content=False, meta_after=False, notification_after=None,
                   skill_args=None, answer="answer", tool=None, echo_after=None):
        u = {"type": "user", "message": {"role": "user", "content": ([{"type": "text", "text": prompt}] if list_content else prompt)}}
        a_blocks = [{"type": "text", "text": answer}]
        if tool:
            a_blocks.insert(0, {"type": "tool_use", "name": tool, "input": {"command": "x"}})
        if skill_loaded:
            inp = {"skill": skill_loaded}
            if skill_args:
                inp["args"] = skill_args
            a_blocks.insert(0, {"type": "tool_use", "name": "Skill", "input": inp})
        a = {"type": "assistant", "message": {"role": "assistant", "content": a_blocks}}
        rows = [u, a]
        if echo_after:
            # a /model or similar slash command echoed into the transcript as a string user entry
            rows.append({"type": "user", "message": {"role": "user", "content": echo_after}})
            rows.append({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "done"}]}})
        if notification_after:
            # a background task finishing mid-turn arrives as a user entry with harness text, then the
            # assistant finishes; before 2026-10-13 the gate took this text as "the prompt" and allowed
            rows.append({"type": "user", "message": {"role": "user", "content": notification_after}})
            rows.append({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "done"}]}})
        if meta_after:
            # what the harness writes after a Skill load: the skill's own text as an isMeta user entry
            # (its text reads as governed work: "analyze", "review", "assess") and a hook-feedback entry
            rows.append({"type": "user", "isMeta": True, "message": {"role": "user", "content": [{"type": "text", "text": "Base directory for this skill: /x. # Adversarial-Verify. Grade, review, assess and analyze the deliverable before delivering."}]}})
            rows.append({"type": "user", "isMeta": True, "message": {"role": "user", "content": "Stop hook feedback:\nsomething"}})
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w") as fh:
            fh.write("".join(json.dumps(r) + "\n" for r in rows))
        return path

    gate = os.path.join(HERE, "governance-enforce.py")
    checks = [
        ("governed (incident 23:41), no load, string content -> BLOCK", transcript(CASES[0][0], None), "block"),
        ("governed (incident 23:41), no load, list content -> BLOCK", transcript(CASES[0][0], None, True), "block"),
        ("governed, synced copy loaded -> ALLOW", transcript(CASES[0][0], "anthropic-skills:adversarial-verify"), "allow"),
        # changed 2026-10-19 (red-team attack G4): a dispute needs adversarial-verify AND scope-fence;
        # one of the two no longer passes. Was "-> ALLOW" from 2026-10-13 to 2026-10-19.
        ("dispute, scope-fence only -> BLOCK (needs adversarial-verify too)", transcript(CASES[0][0], "scope-fence"), "block"),
        ("dispute, both loaded -> ALLOW", transcript(CASES[0][0], "scope-fence", skill_args="x"), "allow_if_both"),
        ("governed, unrelated Skill whose ARGS name plan-gate -> BLOCK (red-team G3)",
         transcript(CASES[5][0], "red-team", skill_args="skip plan-gate here"), "block"),
        ("governed build, /model echo as the latest user string -> BLOCK (red-team G5)",
         transcript(CASES[5][0], None, echo_after="<command-name>/model</command-name>\n<command-message>model</command-message>"), "block"),
        ("review-class trivia, no tools, short answer -> ALLOW (D-SV-5, 2026-10-19)",
         transcript("quick sanity check: 2+2=4, right?", None, answer="Yes, 4."), "allow"),
        ("review-class, no tools, long answer -> BLOCK",
         transcript("quick sanity check: 2+2=4, right?", None, answer="Yes. " * 120), "block"),
        ("review-class, short answer but a tool ran -> BLOCK",
         transcript("quick sanity check: 2+2=4, right?", None, answer="Yes, 4.", tool="Bash"), "block"),
        ("governed, loaded, then isMeta skill-text + hook-feedback entries (live A/B 2026-10-13) -> ALLOW", transcript(CASES[0][0], "adversarial-verify", meta_after=True), "allow"),
        ("governed, NOT loaded, isMeta entries present -> BLOCK", transcript(CASES[0][0], None, meta_after=True), "block"),
        ("requirement only (advisory) -> ALLOW", transcript(CASES[1][0], None), "allow"),
        ("trivia -> ALLOW", transcript("what time zone is the draft in?", None), "allow"),
        ("governed, NOT loaded, task notification arrives mid-turn -> BLOCK (red-first 2026-10-13)",
         transcript(CASES[0][0], None, notification_after="<task-notification>\n<status>completed</status>\n</task-notification>"), "block"),
        ("governed, NOT loaded, system-notification banner mid-turn -> BLOCK (red-first 2026-10-13)",
         transcript(CASES[0][0], None, notification_after="[SYSTEM NOTIFICATION - NOT USER INPUT]\nThis is an automated background-task event"), "block"),
        ("governed, loaded before a mid-turn notification -> ALLOW",
         transcript(CASES[0][0], "adversarial-verify", notification_after="<task-notification>\n<status>completed</status>\n</task-notification>"), "allow"),
    ]
    for label, path, want in checks:
        if want == "allow_if_both":
            # rewrite the transcript so both governors are loaded, then expect allow
            rows = [json.loads(l) for l in open(path)]
            rows[1]["message"]["content"].insert(0, {"type": "tool_use", "name": "Skill", "input": {"skill": "anthropic-skills:adversarial-verify"}})
            with open(path, "w") as fh:
                fh.write("".join(json.dumps(r) + "\n" for r in rows))
            want = "allow"
        out = run(["python3", gate], json.dumps({"transcript_path": path, "stop_hook_active": False}))
        got = "block" if (out and json.loads(out).get("decision") == "block") else "allow"
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} gate: {label}" + ("" if ok else f"  (got {got})"))
        os.unlink(path)
    # loop safety
    path = transcript(CASES[0][0], None)
    out = run(["python3", gate], json.dumps({"transcript_path": path, "stop_hook_active": True}))
    ok = out == ""
    fails += 0 if ok else 1
    print(f"  {'ok  ' if ok else 'FAIL'} gate: stop_hook_active -> ALLOW (loop-safe)")
    os.unlink(path)

    total = len(CASES) + 3 + len(CUE_CASES) + len(checks) + 1
    print(f"== {total - fails} passed, {fails} failed ==")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
