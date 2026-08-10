---
name: draft-arena
description: Run the self-play draft tournament in arena/ — twelve strategy personalities draft against each other on the frozen October 2025 snapshot, seasons are Monte-Carlo simulated, and championship rates grade the system's draft logic. Use when the user says "run the arena," "arena tournament," "self-play draft," "mock draft against itself," "strategy lab," or asks to test/evolve the draft system's strategies. Do NOT use for live or practice drafts with the user picking (that is the fantasy-basketball skill), and do NOT let arena work modify the production engine, data, or skill without an explicit council-audited codification step.
---

# Draft Arena (self-play testing)

The arena's sole purpose is testing the system's draft analysis and league simulation — it is deliberately isolated in `arena/` so the production tool stays lean. Read `arena/README.md` first. Everything runs off the frozen 2025-10-21 snapshot (no hindsight, 2025 rookie class, opening-night injuries); never point it at the live dataset and never edit production files from arena work.

## Procedure

0. **Live practice** ("draft against the bots", "practice draft"): `python3 arena/arena.py live --slot N` — eleven personalities fill the other seats and write into the production draft state, pausing at the user's turns; present the standard §3 calculated card there — the fantasy-basketball SKILL's format: adjusted values in stated units, flags, one committed recommendation, NO confidence percentages (retired 2026-08-09) — via the production `draft turn` flow, mirror protocol, all owner rules, log the user's pick, re-run `live`. This is the 11-managers-plus-user mode.
1. **Slot adaptation**: `python3 arena/arena.py slots` (champ% per strategy x draft slot; best-per-slot table) and `python3 arena/arena.py cadence [--slot N]` (average tier/position drain between a slot's consecutive turns — the snake's 16-pick/6-pick rhythm). Both write JSON intel to `arena/results/` for draft-night use. Re-run after any strategy change.
2. **Run**: `python3 arena/arena.py tournament --seasons 200 --seed <n>` (~2s). Vary seeds across runs; one seed is one sample, not a conclusion.
3. **Read the board**: championship% is the metric that matters; playoff% shows floor. Slot rotation already removes draft-position luck.
4. **Strategy lab (the Fable 5 part)**: analyze WHY the board looks the way it does — trace which categories the winners locked, where the losers' value leaked (injury availability, punt incoherence, positional walls). Then author or mutate strategies in `arena/arena.py`'s STRATEGIES table with reasoned parameter changes, and re-run. Prefer several parallel hypotheses per generation over one tweak at a time.
5. **Codify only through the gate**: a finding becomes a production change (scripts/hoops.py weights, fantasy-basketball skill guidance) only after (a) it holds across 3+ seeds, (b) a council-style adversarial review, and (c) the owner is shown the before/after. Log accepted findings in `arena/results/` as dated markdown.

## Rules

- Championships over value: never grade strategies by draft-day z totals.
- The `market` strategy exists to model ordinary league-mates — keep at least 2-3 non-optimized personalities in every field so winners beat realism, not just other theorists.
- Report honestly when the production `council` strategy loses — that is the arena working, not failing.
- Big runs (thousands of seasons, many generations) are cheap (~2s per tournament); iterate freely, but keep `arena/results/` curated — commit findings, not noise.

## When NOT to use this skill

- The user is drafting (live or mock, human in the loop) → **fantasy-basketball** skill.
- General fantasy questions, trades, rankings → **fantasy-basketball** skill.

## Provenance and maintenance

Built 2026-07-12. Snapshot facts (rosters/injuries as of 2025-10-21) documented in arena/README.md; regenerate via the transform in git history if the base pool schema changes. Re-verify with `python3 arena/arena.py tournament --seasons 100 --seed 1` (expect a full board in ~2s). Update when: the production scorer changes (mirror it in the `council` strategy), the league format changes (TEAMS/ROUNDS/WEEKS constants), or phase-2 evolution replaces the baseline hill-climb.
