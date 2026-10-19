#!/usr/bin/env python3
"""Shared prompt classifier for the governance hooks (governance-trigger.py, governance-enforce.py).

One file so the advisory trigger and the blocking gate can never disagree about what counts as
governed work. Every pattern is pinned by hooks/selftest-governance-classify.py; change a pattern
and the fixture must still pass, including the should-stay-silent set.

Classes and the governor each one routes to:
  analysis    -> adversarial-verify   (an analysis, recommendation, forecast, backtest the owner will rely on)
  review      -> adversarial-verify   (check this / is this right / ready to ship)
  build       -> plan-gate            (build, create, implement, refactor, draft something)
  dispute     -> adversarial-verify + scope-fence
                 (the owner questions or disputes the work's method, data or result; the answer is an
                  assessment, never a fix — INC-2026-10-13-01)
  requirement -> scope-fence          (advisory only: "X is critical" states a requirement, it does not
                  authorize building X — scope-fence rule 4; never enforced by the Stop gate)

History: the 2026-07-15 classifier (three classes) stayed SILENT on three of the four owner messages of
the 2026-10-12 incident and FIRED on "what time zone is the draft in?" because `draft (a|the|me)?` matched
"draft in". Both are fixed here and pinned. 2026-10-13.
"""
import re

PATTERNS = {
    "analysis": re.compile(
        r"\b(analy[sz]\w*|advis\w*|advice|recommend\w*|forecast\w*|predict\w*|assess\w*|evaluat\w*|outlook"
        r"|backtest\w*|dissertation|is this a (good|sound|bad)\b|worth (buying|investing|it)\b"
        r"|when will\b.{0,40}\b(hit|reach|cross|top|bottom)"
        r"|should (i|we)\b.{0,60}\b(invest|buy|sell|adopt|switch|migrate|choose|pick|hire))", re.I),
    "review": re.compile(
        r"\b(review|double.?check|check (this|my|the|it)|is this (correct|right|safe|ready)|ready to ship"
        r"|before i (ship|run|deploy|merge)|sanity.?check|looks? (right|good|correct))\b", re.I),
    "build": re.compile(
        r"\b(build|create|implement|migrat(e|es|ing)\b|refactor\w*|rewrite|design (a|an|the)"
        r"|draft (a|an|the|me|us|this|some|one)\b|write (a|an|the|me|us)\b|set ?up|configure|scaffold"
        r"|stand up|wire up)\b", re.I),
    "dispute": re.compile(
        r"(\bi (don'?t|do not|dont) agree\b|\bi disagree\b"
        r"|\b(not|n'?t|never) (being |been )?(taken|factored|accounted) (into account|in|for)\b"
        r"|\bconcerns? (about|with)\b.{0,80}\b(integrity|method\w*|data|model\w*|logic|test\w*|number\w*|result\w*|accuracy)"
        r"|\b(was|were|is|are) (this|that|it|these|those|the \w+)\b.{0,30}\bfollowed\b"
        r"|\bare you (still |actually |really )?(following|using|applying|taking)\b"
        r"|\b(your|the) (logic|method\w*|model\w*|test\w*|decision\w*|reasoning|numbers?|results?)\b.{0,50}\b(wrong|regress\w*|flawed|incorrect|off|irrelevant|damag\w*)"
        r"|\b(data|computational|system) integrity\b"
        r"|\bwhy (did|do|does|is|are|was|were|has|have) (you|it|the (model|method|board|system|tool|engine|projection\w*|rank\w*|card))\b)", re.I),
    "requirement": re.compile(
        r"\b(is|are) (critical|essential|non-?negotiable|mandatory|required|a hard requirement|a must)\b", re.I),
}

GOVERNORS_FOR = {
    "analysis": ("adversarial-verify",),
    "review": ("adversarial-verify",),
    "build": ("plan-gate",),
    "dispute": ("adversarial-verify", "scope-fence"),
    "requirement": ("scope-fence",),
}

# Classes the Stop gate may block on. "requirement" is advisory only: a requirement statement
# has no deliverable to gate, and blocking it would be ceremony (architecture-contract invariant 5).
ENFORCED = ("analysis", "review", "build", "dispute")


HARNESS_MARKERS = ("[SYSTEM NOTIFICATION", "<task-notification>", "<wake ", "<agent-message", "<webhook-payload")


def classify(prompt: str):
    """Return the list of matched class names, in a stable order.

    Harness-generated prompts (background-task notifications, wake envelopes, subagent hand-backs)
    are never owner requests, so they classify as nothing: on 2026-10-13 the trigger fired on a
    task-failure notification whose text happened to contain a build verb."""
    p = (prompt or "").strip()
    if not p or any(m in p for m in HARNESS_MARKERS):
        return []
    return [name for name, rx in PATTERNS.items() if rx.search(p)]


def governors(classes):
    """Deduplicated governors for the given classes, in first-seen order."""
    out = []
    for c in classes:
        for g in GOVERNORS_FOR.get(c, ()):
            if g not in out:
                out.append(g)
    return out
