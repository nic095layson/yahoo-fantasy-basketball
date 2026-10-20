#!/usr/bin/env bash
# session-doctrine — SessionStart hook for the compaction and resume boundaries.
#
# Why it exists (INC-2026-10-13-01): in a three-week cloud session, 28 compactions each re-attached
# plan-gate and adversarial-verify with an OLD task's arguments, and one compaction summary carried a
# result the owner had just disputed forward as an established finding. Nothing told the model that the
# re-attached text was stale, that the dispute was still open, or that the once-per-session reminders
# (plan-gate-first-write, scope-fence) had already spent themselves weeks earlier.
#
# On `compact`: re-arm the once-per-session reminder hooks (delete their sentinels for this session id)
#               and inject the post-compaction protocol below.
# On `resume`:  inject a one-line reminder that governors are loaded per task, not per session.
# On `startup` / `clear`: silent — the project CLAUDE.md carries the doctrine at startup.
#
# Advisory, never blocking. Fails open on any error. Claude Code only (claude.ai has no hook layer).
# Wiring: .claude/settings.json -> SessionStart, matcher "compact|resume". Pipe-tested 2026-10-13.
set -u
input=$(cat 2>/dev/null || true)
# python3, not jq: with no jq on PATH this hook emitted nothing and re-armed nothing, silently
# (red-team 2026-10-19, attack S3; D-GF-8). python3 is already required by the pack's other hooks.
src=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("source") or "")' 2>/dev/null || echo "")
sid=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("session_id") or "nosession")' 2>/dev/null || echo nosession)

emit() {
  # $1 = context text. Emitted as SessionStart additionalContext.
  python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":sys.argv[1]}}))' "$1" 2>/dev/null
}

case "$src" in
  compact)
    rm -f "${TMPDIR:-/tmp}/plan-gate-reminder-${sid}" "${TMPDIR:-/tmp}/scope-fence-reminder-${sid}" 2>/dev/null || true
    emit "Post-compaction protocol (from the project's operating rules). (1) Governor text that survived the compaction is bound to the task it was loaded for; it does not count as loaded for the current request. Before the next consequential action, load the governor afresh with the Skill tool. (2) Anything the owner disputed or objected to before the compaction is still disputed: list the open objections in one line before continuing, and do not treat a disputed result as a finding. (3) Any data window, sample, or method choice already in flight is restated to the owner in one line before the next run that uses it. (4) The first-write reminders have been re-armed for this session."
    ;;
  resume)
    emit "Resumed session (from the project's operating rules): governors are loaded per task, not per session. For the next non-trivial request, load plan-gate before acting and adversarial-verify before delivering, even if their text is already in context from earlier work."
    ;;
  *)
    ;;
esac
exit 0
