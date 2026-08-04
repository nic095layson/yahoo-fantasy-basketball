# The returning-injury class — capability dossier for 2026-27 (2026-08-04)

Owner directive (2026-08-04): "we have many injured players returning. This
is very essential to understand their prior seasons, to know how valuable
they can be this upcoming season. Tatum, Haliburton, Lillard, Kyrie, and
FVV to name a few."

**Status: the system already prices all five from their last healthy
season.** The pool carries each player's prior-capability per-game rates
(2024-25, their last full year) — so their z-scores and value reflect what
they can do, not the lost year — with the injury priced through three
mechanical layers:

- `hoops.availability`: `-risk` note → value ×0.78 (recovery/out → excluded
  entirely until news re-tags them, owner ruling 2026-07-12);
- the ΔECW weekly model: risk tier → 0.75 expected weekly availability
  (~2.6 of 3.5 games) plus the matching variance;
- `marketRanks`: risk ×0.95 market fade (real Yahoo ADP replaces this
  synthetic fade at the October sync).

## The five, in draft-relevance order

**Tyrese Haliburton (IND, PG, 26) — Achilles, first season back.**
Ruptured the right Achilles in Game 7 of the 2025 Finals; missed all of
2025-26. Prior capability (24-25, in the pool): 18.6 pts / 9.2 ast / 3.0
3PM / 1.4 st on .473 FG% and .851 FT% with only 1.6 TO — the league's
outlier assist-to-turnover engine and a top-10 9-cat player at peak (led
the NBA in assists in 23-24, two All-NBA seasons). The BEST return
prognosis of the five: age 26, and his game runs on pace, vision, and
shooting rather than rim burst — the skills Achilles tears tax least.
CAUTION: the value model currently ranks him ~top-12 even after the 0.78
haircut (observed in this session's draft sims). If Indiana announces a
minutes cap or slow ramp, that is OVERpriced; if he's a full go, it's
roughly right. Highest-priority September verification of the five.

**Jayson Tatum (BOS, SF/PF, 28) — Achilles, second year post-injury.**
Ruptured the right Achilles May 2025 (playoffs); his note carries no
"first season back" tag and the real 2025-26 room stashed him in R13 —
he is further along the curve than the other four. Prior capability
(24-25, in the pool): 26.8 pts / 8.7 reb / 6.0 ast / 3.2 3PM — five-time
All-NBA volume engine across PTS/REB/3PM with real AST. Age 28 in year
two post-Achilles is the Durant template (year two back = full re-ascent).
The 0.78 haircut is likely CONSERVATIVE by October; September verifies
his 25-26 game log and role, then eases the tag toward plain risk or
clear.

**Kyrie Irving (DAL, PG/SG, 34) — ACL, first season back.**
Tore the left ACL March 2025 while playing at an MVP-adjacent level
post-Luka-trade; the pull data has him missing all of 2025-26. Prior
capability (24-25, in the pool): 24.7 pts / 2.7 3PM on .473 FG% and .916
FT% — the elite two-percentage anchor. ACL at 34 beats Achilles at 34:
his craft-and-touch game ages gracefully and the efficiency should
survive; the risk is GAMES PLAYED (Dallas load management), which the
0.78 tier and the weekly 0.75 availability already model. Priced about
right; per-game value largely intact when he plays.

**Damian Lillard (POR, PG, 36) — Achilles, first season back, worst cohort.**
2025 was brutal: a deep-vein thrombosis episode in March, then a ruptured
left Achilles in the April playoffs; waived-and-stretched by Milwaukee,
signed home to Portland; missed all of 2025-26. Prior capability (in the
pool): 24.0 pts / 7.0 ast / 3.0 3PM / .920 FT% — seven-time All-NBA, elite
FT%+3PM. But age-36 Achilles returns are the WORST historical cohort
(Kobe cliff, Wall, Cousins); the bankable skills (FT%, pull-up 3s) age
well while the separation burst that feeds his FG% does not. **This is
the name-trap of the draft:** exactly the brand the room's market-chasers
(Robby adp 0.70, Hegi 0.65) overpay for. Our 0.78 may still be generous —
September should consider a deeper tier for 33+ Achilles returns. Let
someone else pay for the name.

**Fred VanVleet (HOU, PG, 32) — ACL, first season back.**
Tore the right ACL in September 2025, missed all of 2025-26. Prior
capability (24-25, in the pool): 14.1 pts / 5.6 ast / 2.5 3PM / 1.6 st on
a genuinely bad .374 FG% — his 9-cat case is 3PM/AST/ST with low TO, and
his FG% is a standing drag. Age 32 ACL is fine medically; the bigger risk
is ROLE — Houston's backcourt moved on around him during the lost year.
Mid-to-late-round at best; the profile is streamable insurance, not a
core piece. Lowest ceiling of the five.

## The rest of the returning class (already tagged in the pool)

| Player | Tag | Read |
|---|---|---|
| Walker Kessler | shoulder-risk, first season back | season-ended-early big; blocks profile intact |
| Dejounte Murray | achilles-risk (14 games last season) | partial 25-26 return already logged |
| Jaren Jackson Jr. | knee-risk (PVNS surgery) | rare procedure — verify camp status in September |
| Trey Murphy III | shoulder-risk (season ended early) | young wing, standard re-entry |
| De'Andre Hunter | eye-risk (retinal surgery) | monitor only |
| Bradley Beal | hip-risk (6 games 25-26; unsigned) | no team = no value until signed |
| Jimmy Butler | acl-recovery Jan-26 (return ~2027) | **EXCLUDED** (av 0) per owner recovery rule |
| Donte DiVincenzo | achilles-recovery (late 26-27 at best) | **EXCLUDED** |
| Moses Moody | patellar-recovery (no timeline) | **EXCLUDED** |
| Steven Adams | ankle-recovery (out indefinitely) | **EXCLUDED** |

(Chronic-risk vets — Embiid, Kawhi, AD, Curry, LeBron, Zion, PG, etc. —
keep their standing `inj-risk` 0.78 and are not part of the returnee
question.)

## What this means for October, and the September work (E19)

1. **The returnees are where the market-vs-value rift will be widest.**
   The real 2025-26 room drafted Embiid and Kawhi in R7 and stashed Tatum
   in R13; name-brand returnees are precisely what the room's
   market-chasers reach for. Our synthesized rankings (the owner's Q14
   "secret sauce") pricing prior capability × honest availability is the
   edge — IF the availability numbers are current.
2. **E19 (new, September):** per-returnee verification wave during camp —
   minutes restrictions, preseason usage, beat reports — then re-tag:
   clear / keep 0.78 / deepen. Evaluate an age-conditioned Achilles tier
   (36-year-old Dame ≠ 26-year-old Haliburton at the same 0.78) in the
   arena before any engine change; feature freeze respected until then.
3. **October ADP sync:** compare real Yahoo ADP to our returnee values;
   the deck should surface per-returnee EDGE (our rank vs market) on the
   card — Haliburton/Tatum likely value, Dame likely trap, priced live on
   draft night.
