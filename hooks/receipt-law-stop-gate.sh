#!/usr/bin/env bash
# receipt-law-stop-gate — mechanical enforcement for the receipt law (INC-9).
#
# Event: Stop. Fires when the assistant is about to end its turn.
#
# What it detects is NOT a phrase. It is a CONTRADICTION between two things the
# hook can both read: the turn's claim and the turn's record.
#
#   claim   — the final answer says it could not verify / confirm something
#   record  — that same answer names no attempt and no failure mode
#
# An inability claim with no receipt reads as a limit when it may be a decision.
# That is INC-9 exactly, and unlike "is this task trivial?" it is a textual
# question a script can answer. Which is why this hook may BLOCK where the repo's
# other hooks are advisory-only (hooks/README): the house rule against blocking
# exists because a hook cannot judge triviality — this one never has to.
#
# DESIGN CORRECTION, 2026-08-12, recorded because the first version was wrong:
# the gate originally passed any turn in which some verification tool had run.
# Tested against the real incident, that ALLOWED it — the founding session ran
# three searches, stopped, and then wrote "couldn't verify" about eight items it
# had never touched. "Some tool ran" proves nothing about a specific claim. The
# receipt is owed per claim, not per turn, so the tool count now only enriches
# the message and never grants a pass.
#
# It does NOT fire when:
#   - a receipt is present (an attempt or a failure mode is named)  -> honest ATTEMPTED-FAILED
#   - the phrase appears only inside code fences, inline code, or a quote
#   - it already blocked once this turn, or the model is already continuing
#
# Fails OPEN on every error: a hook that breaks sessions is worse than the defect
# it guards. Any parse problem, missing file, or unexpected shape exits 0 silently.
#
# Install (user scope):
#   1. cp hooks/receipt-law-stop-gate.sh ~/.claude/hooks/ && chmod +x it
#   2. Merge into ~/.claude/settings.json:
#      {"hooks":{"Stop":[{"hooks":[{"type":"command",
#        "command":"bash ~/.claude/hooks/receipt-law-stop-gate.sh","timeout":10}]}]}}
#   3. Pipe-test: bash hooks/selftest-receipt-law.sh  (expects 10/10 PASS)
#
# Surface note: Claude Code only. claude.ai has no hook layer, so on that surface
# the receipt law is carried by the custom-instructions block instead
# (instructions/claude-ai-custom-instructions.md, standing principles).
#
# Status: PROPOSED 2026-08-12, pipe-tested, NOT wired into any settings.json.
# Behavioral A/B: experiments/hypothesis-2026-08-11-gap-provenance.md.
set -u
input=$(cat)

# The script goes in a variable, the event goes on stdin. Two heredocs both
# claiming stdin would feed the event to python as its source text.
gate=$(cat <<'PY'
import json, os, re, sys

def allow():           # fail-open / no-op
    sys.exit(0)

try:
    ev = json.load(sys.stdin)
except Exception:
    allow()

# Loop guard: never block a continuation we ourselves caused.
if ev.get("stop_hook_active"):
    allow()

path = ev.get("transcript_path") or ""
sid  = ev.get("session_id") or "nosession"
if not path or not os.path.exists(path):
    allow()

try:
    entries = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
except Exception:
    allow()

# --- turn boundary: the last REAL user prompt ---------------------------------
# Tool results also arrive as type "user", but with a list content; a typed
# prompt has a string content. That distinction is the turn marker.
start, turn_id = 0, "0"
for i, e in enumerate(entries):
    if e.get("type") != "user":
        continue
    content = (e.get("message") or {}).get("content")
    if isinstance(content, str):
        start, turn_id = i, str(e.get("promptId") or e.get("uuid") or i)

turn = entries[start + 1:]

# --- the claim: assistant prose from this turn --------------------------------
said, tools = [], []
for e in turn:
    if e.get("type") != "assistant":
        continue
    for blk in (e.get("message") or {}).get("content") or []:
        if not isinstance(blk, dict):
            continue
        if blk.get("type") == "text":
            said.append(blk.get("text") or "")
        elif blk.get("type") == "tool_use":
            tools.append(blk.get("name") or "")

text = "\n".join(said)
if not text.strip():
    allow()

# --- the record: how much looking up happened this turn? ----------------------
# NOT an allow-gate. The founding incident ran three searches, stopped, and then
# wrote "couldn't verify" about eight items it had never touched — so "some tool
# ran" proves nothing about THIS claim. The receipt is owed per claim, not per
# turn. The count only enriches the message.
VERIFY_TOOLS = {"WebSearch", "WebFetch", "Read", "Grep", "Glob", "Bash",
                "Task", "Agent", "NotebookRead"}
n_lookups = sum(1 for t in tools if t in VERIFY_TOOLS or t.startswith("mcp__"))

# --- sanitize: the rule must not fire on text that merely DISCUSSES the rule ---
clean = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)   # fenced blocks
clean = re.sub(r"\x60[^\x60\n]*\x60", " ", clean)          # inline code
clean = re.sub(r"^\s*>.*$", " ", clean, flags=re.MULTILINE)  # blockquotes

INABILITY = re.compile(
    r"could ?n[o']?t (verify|confirm|check|determine|find out)"
    r"|can ?n[o']?t (verify|confirm|determine)"
    r"|cannot (verify|confirm|determine)"
    r"|unable to (verify|confirm|determine)"
    r"|no data (exists|is available)"
    r"|(remain|are|is|left) (unverified|unconfirmed)"
    r"|not (verifiable|possible to verify)",
    re.IGNORECASE)

m = INABILITY.search(clean)
if not m:
    allow()

# --- the receipt: was an attempt and a failure mode named? --------------------
RECEIPT = re.compile(
    r"searched|search(ed)? for|looked up|queried|fetched|tried to (fetch|load|open|reach)"
    r"|ran |returned no|no results|404|403|timed out|timeout|paywall|rate.?limit"
    r"|blocked|requires (a )?(login|account|subscription)|behind a login"
    r"|javascript.rendered|not (in|within) my training|after my (training )?cut.?off"
    r"|permission|not (approved|granted)|did not check|didn't check|by choice",
    re.IGNORECASE)
if RECEIPT.search(clean):
    allow()

# --- once per turn ------------------------------------------------------------
tmp = os.environ.get("TMPDIR", "/tmp")
sentinel = os.path.join(tmp, "receipt-law-gate-%s-%s" % (sid, turn_id))
if os.path.exists(sentinel):
    allow()
try:
    open(sentinel, "w").close()
except Exception:
    allow()

phrase = m.group(0)
record = ("no lookup ran this turn at all"
          if n_lookups == 0 else
          "%d lookup(s) ran this turn, but none of them is cited for this claim"
          % n_lookups)
print(json.dumps({
    "decision": "block",
    "reason": (
        'Receipt law (adversarial-verify rule 6): this answer says "%s" and names '
        "no attempt and no failure mode — %s. An unreceipted inability reads as a "
        "limit when it may be a decision, which is the INC-9 defect.\n\n"
        "Do one of these before ending the turn:\n"
        "  1. Run the check. If it is cheap, this is almost always the right move.\n"
        '  2. Write "did not check" instead of "could not verify", and say why '
        "(cost, time, tool budget) — a stated choice the reader can override.\n"
        "  3. If it genuinely cannot be resolved, name what you searched and why "
        "it cannot settle the question — that is a receipt, and it ships.\n\n"
        "If the item is load-bearing, option 2 is not a deliverable state: resolve "
        "it or withdraw the conclusion it supports (Step 6, the gap audit)."
    ) % (phrase, record)
}))
PY
)
printf '%s' "$input" | python3 -c "$gate" 2>/dev/null || exit 0
exit 0
