# Post-mortem — live draft simulation, 2026-07-12

Exercise: 127-pick live draft sim, frozen 2025-10-21 snapshot, David at slot 7
feeding picks turn-by-turn through Cowork. Final board verified clean (127
picks, zero duplicate players, all 11 of David's picks correctly attributed,
one intentional placeholder). But it took 2 undos, 2 fixes, and 1 manual
state edit to get there. Every incident below is traceable to a pick number.

## Incidents

### INC-1 — Feed collision → 4 corrupted picks (#40–43). Severity: HIGH
**What happened.** David fed "White / Murray / Adebayo / Lebron"; my logging
command executed but its result was lost in the interface (David saw
"running command" with no visible outcome; I saw an error and no output).
David, reasonably, re-sent those four names plus two new ones. I re-ran all
six. The four duplicates did NOT get skipped: the engine's overlap guard
("already off the board") only fires when a name resolves to the same
already-drafted player — but surname-only inputs re-resolve. With Derrick
White drafted, "White" resolved to Coby White; with Jamal Murray drafted,
"Murray" resolved to Dejounte. Two phantom picks shifted the snake, putting
Garland in David's #42 slot and Jaylen Brown at #43.
**Root causes.** (a) A tool call whose result is lost still mutates state —
I treated "no result" as "nothing happened." (b) The engine's duplicate
guard is bypassed by ambiguous surnames. (c) I re-sent a feed without
verifying state first.
**Detection & repair.** Adebayo/Lebron's skip warnings exposed it; `draft
status` + direct state read confirmed; 2× `undo` + 2× `fix` repaired it.
Fully recovered, ~90 seconds of draft time lost.

### INC-2 — Same trigger, zero damage (#48–53). Severity: none (lesson applied)
Second lost tool result on a 6-name bulk feed. This time I read the state
file BEFORE re-acting: all six picks had logged. No re-send, no damage.
This is the fix for INC-1 working, and the basis of Fix-1 below.

### INC-3 — "Collins" → Ryan Rollins (#89). Severity: MEDIUM
Fuzzy matcher crossed surnames: "Collins" → "Rollins" (assumed over Collin
Sexton — a first-name match; both wrong). Real intent John Collins is absent
from the 219-player pool. Two defects: (a) the matcher prefers a wrong-
surname edit-distance match over declaring UNKNOWN; (b) `draft fix N` cannot
set an UNKNOWN placeholder for an out-of-pool player — I had to hand-edit
the state JSON, which the speed rule rightly treats as a draft-night no-go.

### INC-4 — Self-referential "assumed over" echo (#114). Severity: cosmetic
"Sharpe" logged Shaedon with flag "(assumed over Shaedon Sharpe)" — the echo
prints the winning candidate instead of the losing one (Day'Ron). Harmless
but erodes trust in exactly the flag corrections depend on.

### What worked (keep)
Typo fuzzy-matching earned its keep: Siakim→Siakam, Hartentien→Hartenstein,
Okonwu→Okongwu, Shroeder→Schroder — 4 saves, zero errors. Explicit
duplicate feeds were skipped safely twice (Adebayo/LeBron; David's re-sent
Eason). Numeric correction ("89 John Collins") and undo/fix behaved as
documented. Card latency was seconds — comfortably inside a 45s clock.

## David's reported issue: input during "running command" isn't registered

From my side, messages sent mid-command arrive appended to the running turn
— I received and processed two that way (#29–30 "Ball/Chet", #40 feed). The
loss mode is narrower but nastier: when my command's RESULT is lost, the
interface shows me nothing, David sees no mirror lines, and his next message
lands on a board whose true state neither of us has seen. It's not that his
input is ignored — it's that a lost result desynchronizes us, and his next
input then gets processed against a stale mental model. The fix is not
"type slower"; it's making every logging action idempotent (Fix-1) so a
re-send after silence is always safe.

## Proposed fixes (none applied — approval per item)

**Fix-1 — Verify-state-first, always (my procedure + skill doc). Prevents INC-1.**
Every logging action starts by reading the state file's pick count and
tail, diffing against the incoming feed, and sending only unlogged names —
inside the same single bash invocation, so the speed rule holds. If a
result is ever lost, the next action self-heals instead of double-logging.
Codify as a numbered rule in the fantasy-basketball skill's draft protocol.

**Fix-2 — Surname-collision guard (engine, scripts/hoops.py). Prevents INC-1's engine half.**
If a fed name's best match is already drafted, SKIP with a warning — even
when a lesser fuzzy candidate exists. Drafting the lesser candidate then
requires a fuller name ("Coby White"). One rule, and the Coby/Dejounte
misattribution class disappears. Risk: a legitimate "White" meaning Coby
after Derrick is gone gets skipped once and needs a retype — acceptable;
wrong-log costs undos, skip costs one message.

**Fix-3 — Cross-surname fuzzy floor + UNKNOWN via fix (engine). Prevents INC-3.**
(a) Never fuzzy-match across surnames when similarity is below a strict
threshold — prefer logging `UNKNOWN: <raw name>` (attribution stays intact,
correctable later). (b) Support `draft fix N "UNKNOWN: Name"` so
placeholders are settable through the CLI, not JSON surgery.

**Fix-4 — Assumed-over echo (engine, one line). Fixes INC-4.**
Print the losing candidate, not the winner.

**Fix-5 — Pool-gap audit (data). Reduces INC-3 recurrence.**
John Collins (a rosterable NBA regular in Oct 2025) is missing from a pool
that carries −0.25-val players. Post-approval: audit the snapshot (and the
production 2026-27 pool) against a top-250 list; add missing rows with
labeled estimates.

**Fix-6 — Protocol constants (skill doc). Owner-directed.**
Update the fantasy-basketball skill: 45-second clock (currently says 60);
pre-stage the card from 3 picks out ("hot" rule — worked well tonight);
during bulk feeds prefer first initial + surname for common surnames
(this draft alone had ambiguous White, Murray, Robinson, Ball, Bridges,
Sharpe, Collins, Thompson).

## Priority

Fix-1 tonight (procedure — no code, biggest single risk eliminated);
Fix-2 and Fix-3 before the next live run (engine, ~30 lines total);
Fix-4/5/6 with the same commit. All engine/skill edits shown as before/after
diffs for approval per the codification gate.

## Resolution (added post-review)

All six fixes were implemented upstream (commit `404afc8`; arena live-mode
fix in `e871a3a`) and behaviorally verified in-session: collision guard
HALTS the batch with a fuller-name instruction; absent names quarantine as
UNKNOWN; `--expect <pre-feed count>` is the state handshake (mismatch →
nothing logged, tail printed); arena live assigns 11 unique managers.
`--expect` semantics: it asserts the pick count BEFORE the feed, not the
batch size.
