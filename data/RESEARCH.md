# Baseline research: top-210 player pool (built 2026-07-11)

## What this is
`players.csv` is the 2026-27 draft baseline: ~210 fantasy-relevant players
with per-game 9-cat lines reflecting 2025-26 season production, teams as of
the July 2026 free-agency moves known on 2026-07-11, and mechanical injury
notes (`out-*` = excluded, `*-recovery` = 0.7x, `*-risk` = 0.85x).

## Method
1. **Ranking methodology**: volume-weighted z-scores over the pool (the
   Basketball Monster approach), computed by `scripts/hoops.py` — the pool IS
   the ranking; no hand-ordered list is stored.
2. **Stat lines**: 2025-26 per-game production, from assistant season
   knowledge through Jan 2026, adjusted for known late-season/offseason
   developments surfaced by web search on 2026-07-11.
3. **Consensus cross-check**: top-tier ordering verified against search
   digests of Yahoo Sports 9-cat draft rankings, NBA.com final top-150
   2025-26, RotoWire/CBS/ESPN breakout-bust coverage. Engine top-4
   (Wembanyama, Jokic, SGA, Luka) matches that consensus.
4. **July 2026 roster moves encoded**: Giannis→MIA; Jaylen Brown→PHI;
   Paul George→BOS; LaMelo→MIN; Ja Morant→POR; Kessler→LAL (S&T);
   Ayton→WAS; Porzingis re-signed GSW; Finney-Smith→CHA; Oubre→IND;
   Lillard→POR (achilles recovery, targets 2026-27 return); Wemby max
   extension SAS; LeBron UNSIGNED (CLE/MIA/PHI per reports) — flagged
   `unsigned-fa-monitor`; Kawhi trade on hold pending NBA investigation.
5. **Recoveries for 2026-27**: Tatum, Haliburton (achilles), Kyrie, VanVleet
   (ACL), Lillard (achilles) — stat lines are their last healthy season,
   discounted 0.7x by the engine.

## Known limits (refresh before draft night)
- Bulk stat sites (Basketball-Reference, NBA.com, ESPN, Yahoo) were
  403-blocked at this environment's gateway; per-game lines are
  knowledge-based, not scraped — spot-check the top 50 when access allows.
- The Athletic/The Ringer are paywalled; not directly consulted.
- Yahoo multi-position eligibility for 2026-27 is not published yet;
  `pos` values are best current estimates.
- LeBron's destination, the Kawhi investigation, and late free agency will
  move values — daily-refresh rule covers this.
