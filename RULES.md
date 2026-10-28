# RULES — read at session start (both repos carry this page; one page, no more)

Adopted 2026-10-15 from the Co-GM self-audit (`report/plans/co-gm-self-audit-2026-10-15.md`
§2 L1–L5, §4 D2/D3; incidents I1–I13). These sit inside the global governors
(plan-gate → scope-fence → adversarial-verify) and never override them.

1. **Plan-gate before any consequential action.** Emit the gate to the owner — goal,
   knowns, assumptions, success criteria, phases — *before* the work, not inside it.
2. **A question gets an assessment, not a build.** A stated requirement ("X is critical")
   says what the work must respect; it is not a build order. (I10)
3. **Every run parameter is stated before the run.** Window, sample, threshold, seed,
   source: one line to the owner, before the run that uses it. A parameter inherited from a
   file's extent or a script's default is a choice nobody made — say it. (I10/R3)
4. **No data is written from memory.** A team, position, stat line, minutes, games, status
   or roster value needs a dated fetched record or an owner paste, pinned in the repo. (I1, I8)
5. **Red-first.** Every fix lands with a test that failed before the fix and passes after;
   every gate has been seen red. (LESSONS 19)
6. **No hand-typed figures.** Writers read records. Monte-Carlo figures run twice (two
   seeds); odds carry their error.
7. **gates.json or no merge.** Every gate run goes through `scripts/gates.py` (kit), which
   writes each gate's PASS line and exit code to `gates.json`; a gate that exits 0 without
   its PASS line is a FAIL (the 10/15 empty-log near-miss). Every PR body quotes
   `gates.json`; a merge whose head commit lacks a PASS `gates.json` is refused.
8. **Disputed stays disputed.** A result the owner disputed is carried only as DISPUTED in
   `OPEN.md`. Re-read `OPEN.md` after every compaction; a summary may not promote an OPEN
   item to a finding. (I10/R6)
9. **Publish** only after a fresh read of the live artifact and a byte-verify of the served
   page; never during a live room. (LESSONS 21)
10. **Scope.** The session's scope is its prompt (Session 1: items 1–8 of plan §6).
    Anything else noticed goes on the after-report's decision sheet, not into the build.
11. **Runner changes travel downstream (kit; owner 2026-10-28).** When a main-session change
    alters what the runner's scheduled tasks run, read, write, commit or report (a step, an
    output, a PASS/HALT line, a source pin, a retry), the same session, before it calls the
    work done: reads both stored task prompts (`get_trigger`); drafts each edited prompt with
    its diff against the stored text, byte count and sha256; hands the owner one paste-ask for
    the runner's conversation with what changed and what the next runs should show; and after
    the paste, reads both tasks back and confirms byte equality. The tasks take prompt edits
    only from the conversation they post into, so the paste is the owner's; never route it
    through another session. A code-only change still reaches the runner (each run merges
    main) and is named for it. Every after-report carries a "Runner impact" line: none,
    code-only (with what the next runs should show), or a prompt edit with its read-back
    state. Work with a prompt edit is not done until the read-back matches.

**Urgency rule (L1).** A finding that touches more than 25% of the top 150 within 7 days of
a lock is raised to the owner the same day, not queued. (I8)

**Where things are.** Gate runner: kit `scripts/gates.py` (`--quote` prints the PR-body
block; `--verify` refuses a stale or failing `gates.json`). Disputes and unanswered owner
questions: `OPEN.md`. Lessons: deck `LESSONS.md`.
