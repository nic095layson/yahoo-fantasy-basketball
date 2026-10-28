# yahoo-fantasy-basketball — a domain-layer project

Governed by the operating doctrine of `nic095layson/claude-core-skills`. The block
below is that doctrine's cloud-safe copy (`instructions/project-doctrine-block.md`
there); `~/.claude/CLAUDE.md` does not exist in cloud containers, so nothing here
depends on it.

Within the governed process, this project's domain rules apply: read `LESSONS.md`
before live drafts or arena work, and the two project skills under
`.claude/skills/` (`draft-arena`, `fantasy-basketball`) carry the domain procedure.
Core on top, domain within.

---- BEGIN BLOCK ----

## Operating doctrine (every session, every surface)

The core governors run on every non-trivial request here — **plan-gate** before the
first consequential action, **scope-fence** during the work, **adversarial-verify**
before delivering — and they are **loaded with the Skill tool, never applied from
memory**. Governor text already in context from an earlier task or from a compaction
does not count as loaded. Source of truth: `nic095layson/claude-core-skills`.

Four rules this project binds every session to, in addition to the governors:

1. **A question gets an assessment, not a fix.** When the owner asks whether something
   is right, or disagrees with a result, the deliverable is the assessment. A fix,
   candidate, rewrite, or dry run — even in scratch — waits until the owner asks for it.
2. **Method parameters are stated before the run.** Any data window, sample, cutoff,
   era, or baseline an analysis runs on is named to the owner in one line before the run
   that uses it, with its basis. A parameter inherited from a file's extent or a script's
   default is an assumption, not a choice.
3. **A stated requirement is not a build order.** "X is critical" says what the work
   must respect; it authorizes nothing new.
4. **Decisions come as options.** When there is a decision for the owner to make, offer
   2–4 options, each with a brief plain-language explanation, the recommended one listed
   first and marked "(Recommended)". Where the surface has clickable choices (Claude Code:
   the AskUserQuestion tool, with a preview card when comparing options helps), use them;
   otherwise a numbered list. Not for trivial choices or ones with an obvious default (state
   the default in one line), and never in an unattended run, where nobody is there to click:
   record the open decision in the report instead.

Communication (owner preferences, 2026-10-28; they shorten how things are said and never
remove a gate, a check or an honest caveat): the owner is a visual learner — show, don't
narrate. Between tool calls write nothing (one heartbeat line at most on a long task; a
surprise — a failed check, a result that contradicts the plan, a blocker — is said at once,
in one line). Tables for comparisons, options, statuses and before→after; text diagrams for
flows; bold the one line that matters, short bullets beneath; rendered charts and artifacts
only on request. A required plan is shown before acting as one compact table — Goal ·
Method / parameters · Done when · If it breaks — which is plan-gate's accepted compact form
here. A final answer is: the outcome in one bold line, a table or before→after, only the
caveats that matter, and what the owner needs to do next.

After a compaction: list the owner's open objections in one line before continuing;
a result the owner disputed stays disputed; reload the governors before the next
consequential action.

Enforcement: this repository's `.claude/settings.json` wires the governance hooks
(prompt trigger, Stop gate, first-write reminders, compaction protocol). They run in
Claude Code sessions that start inside this one repository, on the web included. A
cloud session with several repositories attached reads only plugin keys from each
repository's settings, not hooks (Claude Code settings documentation, read 2026-10-13);
there, this file and the plugin route carry the doctrine.

---- END BLOCK ----
