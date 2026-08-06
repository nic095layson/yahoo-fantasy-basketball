# Mock 36 debrief — slot 1, declared punt FT%/3PTM/TO (2026-08-05)

State: `arena/data/states/draft_state_mock36.json` (upload md5 e22f72f6).
Regenerate: `python3 arena/mocks/season_sim_mock36.py` →
`arena/results/season_sim_mock36_out.json`. 18,000 seasons (6,000 × seeds
11/23/47). Per-turn replay: `arena/results/m36_replay.json`. Same
instrument caveats as mocks 31–35 (pre-E14 bracket, unfit weekly
constants, ~0.45× room texture).

## Headline — the best owner build ever measured

| Metric | Value | Rank | Prior owner best |
|---|---|---|---|
| Champ% | **31.18** (30.67/31.20/31.67 per-seed) | **1 of 12** | 29.82 (m24) |
| Playoff% | 93.4 | 1 | — |
| ECW/week | **5.06** | 1 | — |
| Kept-total, 9 cats | +4.56 | 2 | — |

**First owner build above the winners' ECW bar (≥4.90).** The room's #2
(15.58%) and #3 (14.13%) are strong seats; this build doubles them. The
only higher number in the whole ledger is the m28 hindsight oracle
(34.58%) — this is a real draft, not an oracle.

Roster: Wemby, Giannis, Harden, Sheppard, Sengun, Mikal Bridges, Braun,
Wallace, Vucevic, Nesmith, Nembhard, Ellis, Horford.

## How it was built: the card's spine + the owner's stars

Card agreement: actual pick in shipped Top-5 at **11/13** turns, and the
card's **exact #1 at 10/13** — including every single pick from R6
through R13 (Bridges, Braun, Wallace, Vucevic, Nesmith, Nembhard, Ellis,
Horford). The three deviations were all early star-power injections the
card ranked lower:

- R2: **Giannis** over Bane
- R3: **Harden** over Derrick White
- R5: **Sengun** over Cameron Johnson

This is the collaboration pattern the ledger has been looking for since
m27: the card supplying a coherent value spine, the owner overriding
exactly where name-brand ceiling beats rank. It is also a major
out-of-sample SUCCESS for the blend50 ordering (kill-rule counter:
success, not failure).

## Category shape

| Kept | FG% | PTS | REB | AST | ST | BLK |
|---|---|---|---|---|---|---|
| rank | **1** | 9 | 7 | 7 | 6 | **1** |

| Punted | FT% | 3PTM | TO |
|---|---|---|---|
| rank | 12 | 9 | **5 (+2.02z)** |

Two elite anchors (FG%, BLK), four live middle cats, and — the notable
wrinkle — **the declared TO punt never materialized**: the role-player
shell (Braun, Nesmith, Nembhard, Ellis, Wallace, Horford) is so low-TO
that it absorbs Wemby/Giannis/Harden's turnovers to a rank-5 category.
ECW 5.06 is the arithmetic of six-going-on-seven live categories.

## Punt audit

Declared FT%/3PTM/TO ranks **#12 of 84** possible 3-cat punts for this
roster (kept-z +6.66); optimal was FT%/3PTM/PTS (+10.69). A mild
mock-32-pattern miss (punting a cat the roster actually wins) — but this
time harmless, for two measured reasons: the ordering ignores the box
entirely (E20), and the build's strength never depended on the punt frame.
The kept-z metric also under-rates this roster (rank 2 on 9-cat, rank 1
on ECW) — more evidence that ECW, not kept-z, is the yardstick.

Dead-kept-cat check (m34/m35 pattern): PTS sits at rank 9 (−2.01z) —
weak but not punted-cluster dead, and with six other live cats the build
carries margin the 5-cat m35 shape lacked.

## Read

Slot 1 + card spine + three star deviations + a low-TO shell = the
blueprint. For October: this is the strongest evidence yet for the
working doctrine — follow the card from the mid-rounds on, spend
judgment early on ceiling, and let roster construction (not the punt
box) decide which categories die. Mock 36 joins the punted screening set
(E21, now six: 22, 31, 32, 34, 35, 36).

## LEDGER row

`| 36 | 1 | 31.18 | 93.4 | 1 | 12 | ECW 5.06 — BEST OWNER BUILD EVER
(prior best m24 29.82; first above the 4.90 winners' bar; only the m28
hindsight oracle is higher). Card's exact #1 followed 10/13 incl. all of
R6–R13; deviations were Giannis/Harden/Sengun star injections. Declared
punt #12 of 84 (TO punt never bound — role shell held TO to rank 5).
blend50 out-of-sample SUCCESS (`season_sim_mock36.py`, `m36_replay.json`) |`
