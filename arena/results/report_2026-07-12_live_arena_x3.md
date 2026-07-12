# Live-Arena ×3 — System-Integrity Report (post-discount rules)

**Date:** 2026-07-12 · **Operator:** Claude (Cowork session), user seat run strictly per the fantasy-basketball skill
**Repo state:** `03da7f9` — "Deepen injury discounts per arena calibration (owner-approved)"
**Pre-flight:** LESSONS.md read first. Verified `scripts/hoops.py availability()` = recovery ×0.60 / risk ×0.78, and the skill's "Healthy tiebreak (codified 2026-07-12, arena-calibrated)" present. First verification of the session FAILED (repo still had 0.7/0.85 and no tiebreak rule); run was halted and David pulled via GitHub Desktop; re-verification passed before any draft started.

---

## 1. Run parameters and slots

| Parameter | Value |
|---|---|
| Format | 12 teams × 15 rounds = 180 picks, arena defaults |
| Mode | `python3 arena/arena.py live --slot N` (11 AI personalities + user seat) |
| Slots (drawn from OS entropy, one per band) | **early = 1, middle = 6, late = 10** |
| Arena seeds per draft | 101 / 102 / 103 (chosen for reproducibility, recorded here) |
| Turn protocol | per skill: `draft turn` only, `--expect <pre-feed pick count>` on **every** feed (card calls and log calls); mirror-only for bot picks; confidence boards at user turns; no analysis commands, web searches, or CSV edits mid-draft |
| Data | cards priced from live `data/players.csv` (freshness stamped 2026-07-11 — not refreshed, per mission constraint of no CSV edits; arena bots price from the frozen 2025-10-21 snapshot by design) |
| Tournament baseline | `tournament --seasons 200 --seed 1 --seeds 3 --rotations 3` → fixed seed list [1, 98, 195], 21,600 seasons/strategy |

Turn mechanics in live mode: the arena advances bots and pauses at the user's pick; the card comes from an empty feed `draft turn "" --expect N`, the pick is logged with `draft turn "my:Name" --expect N`. All 90 `draft turn` commands (45 card calls + 45 log calls) carried `--expect`. Draft-state files were isolated per draft via `HOOPS_DRAFT_STATE` under `arena/results/` (see incident I-2).

---

## 2. Per-draft operation log

Notation: **val** = injury-adjusted z-total from the card (`*` = discounted); "old rules" = pre-2026-07-12 (×0.85 risk / ×0.70 recovery, no healthy tiebreak). "CHANGED" marks picks where the old rules would demonstrably have produced a different pick (mechanism in parentheses). Compounding multipliers (×0.85 2nd / ×0.70 3rd concurrent recovery) applied by the operator per the skill; the card supplies the [2nd+ recovery bet] tag.

### Draft 1 — slot 1, seed 101 (picks 1, 24, 25, 48, 49, 72, 73, 96, 97, 120, 121, 144, 145, 168, 169)

| Pick | Board top (val) | Chosen | Confidence board (as issued) | Rule notes |
|---|---|---|---|---|
| #1 | Wembanyama +13.00 | **Wembanyama** | Wemby 88, Jokic 82, SGA 80 | no flags; >5% gap |
| #24 | Murray +3.84 vs Haliburton +3.76* | **Jamal Murray** | Murray 68, Hali 66 (coin flip), Vucevic 62, White 61 | **CHANGED (tiebreak)** — old adj Hali +4.39 = clear #1; new value within 2% → healthy preferred |
| #25 | Haliburton +3.76* vs Vucevic +3.71 | **Vucevic** | Vucevic 67, Hali 63 (coin flip), Murphy 62, Sabonis 60 | **CHANGED (tiebreak)** — 1.3% gap; Vucevic also hits weakest cats (TO, FG%) |
| #48 | Haliburton +3.76* | **Haliburton** | Hali 72 [1st recovery bet], Flagg 62, Tatum 58, Herro 56 | tiebreak N/A — nearest healthy 42% back; flagged player clearly wins per rule |
| #49 | Tatum +2.68* [2nd bet] vs Flagg +2.38 | **Flagg** | Flagg 64, Tatum 60 (coin flip), Herro 58, Garland 55 | **CHANGED (compounding+tiebreak)** — Tatum eff +2.28 < Flagg; old eff +2.66 would take Tatum |
| #72 | Tatum +2.68* [2nd bet] | **Tatum** | Tatum 61, Sheppard 55, Pritchard 54, Siakam 53 | eff +2.28 still 42% clear of best healthy — compounding priced, holds |
| #73 | Lillard +2.34* [3rd bet] vs Sheppard +1.61 | **Sheppard** | Sheppard 58, Pritchard 56, Lillard 55 (coin flip), Suggs 52 | **CHANGED (compounding+tiebreak)** — Dame eff +1.64 ≈ Sheppard +1.61 → healthy; old eff +1.91 would take Dame |
| #96 | Lillard +2.34* [3rd bet] | **Lillard** | Lillard 60, Avdija 51, McDaniels 48, Powell 47 | eff +1.64 ≈ 4× best healthy (+0.43) — 3rd recovery bet admitted (see §5-P3) |
| #97 | VanVleet +0.52* [4th bet] vs field | **McDaniels** | McDaniels 55, Avdija 54 (coin flip), PJW 51, FVV 48 | 4th-bet multiplier UNDEFINED in skill (extrapolated ×0.55); contested-TO fit decided |
| #120 | VanVleet +0.52* [4th bet] | **VanVleet** | FVV 54, Nesmith 48, DiVincenzo 47 | eff +0.29 still +0.8z clear of best healthy (−0.49) → **4th recovery bet admitted** (§5-P1) |
| #121 | DiVincenzo −0.49 vs Nesmith −0.53 | **Nesmith** | Nesmith 53, DDV 52 (coin flip), C.Thomas 48, Ellis 47 | contested-TO gain over position tiebreak |
| #144 | Sharpe −1.28 | **Sharpe** | Sharpe 55, Alvarado 48, Melton 47, Harper 45 | [would be 3rd IND] fired on Oubre ✓ |
| #145 | Melton −1.49* [inj-risk] vs Alvarado −1.59 | **Alvarado** | Alvarado 54, Melton 52 (coin flip), Oubre 47, Podziemski 46 | **CHANGED (tiebreak only)** — negatives are never discounted, so 0.10z tie decided purely by the new healthy preference; old rules → Melton |
| #168 | Wells −2.32 vs Hachimura −2.34 | **Hachimura** | Rui 53, Wells 52 (coin flip), Toppin 48, Black 47 | TO +1.4 = biggest contested gain |
| #169 | Wells −2.32 | **Wells** | Wells 56, Dick 50, Black 49, Clifford 47 | final pick |

Result: FG% 9 · FT% 3 · 3PTM 3 · PTS 5 · REB 6 · AST 6 · ST 2 · BLK 4 · TO 4 (vs field). Incidents: none from the engine; see I-1/I-3 (observations).

### Draft 2 — slot 6, seed 102 (picks 6, 19, 30, 43, 54, 67, 78, 91, 102, 115, 126, 139, 150, 163, 174)

| Pick | Board top (val) | Chosen | Confidence board | Rule notes |
|---|---|---|---|---|
| #6 | AD +5.48* [inj-risk] vs KAT +5.47 | **Towns** | KAT 62, AD 61 (coin flip), Edwards 58, Holmgren 56 | **CHANGED (tiebreak)** — 0.01z apart; old adj AD +5.97 = clear #1 |
| #19 | Durant +3.95 vs Murray +3.84 | **Jamal Murray** | Murray 60, KD 58 (coin flip), Hali 56, J.Johnson 55 | both healthy; AST/ST/PTS fit + KD's −1.5 TO |
| #30 | Haliburton +3.76* | **Haliburton** | Hali 64 [1st bet], Bane 60, F.Wagner 57, Giddey 55 | 8.5% gap — outside band, flagged clearly wins |
| #43 | Tatum +2.68* [2nd bet] vs Flagg +2.38 | **Flagg** | Flagg 62, Tatum 59 (coin flip), Barnes 57, Bam 56 | **CHANGED (compounding+tiebreak)** — mirrors D1 #49 |
| #54 | Tatum +2.68* [2nd bet] vs Herro +2.25 | **Herro** | Herro 58, Tatum 57 (coin flip), Garland 55, Ball 52 | **CHANGED — and the session's clearest RULE-CHURN case**: band on *adjusted* value (16% gap → doesn't fire) vs *compounded judgment* (+2.28, 1.3% gap → fires). Resolved toward calibration intent (variance = unpriced downside). See §5-P2 |
| #67 | Tatum +2.68* [2nd bet] | **Tatum** | Tatum 60, Sheppard 54, Lillard 53, Pritchard 52 | eff +2.28, 42% clear — holds |
| #78 | Lillard +2.34* [3rd bet] vs Sheppard +1.61 | **Sheppard** | Sheppard 57, Lillard 55 (coin flip), Pritchard 54, D.Murray 51 | **CHANGED** — identical to D1 #73 (rule fires consistently) |
| #91 | Lillard +2.34* [3rd bet] | **Lillard** | Lillard 58, Wallace 51, H.Jones 50, McCollum 49 | eff +1.64 vs +0.71 best healthy — admitted |
| #102 | VanVleet +0.52* [4th bet] vs +0.13 field | **PJ Washington** | PJW 53, FVV 50, Vassell 49, K.Murray 47 | contested REB/BLK/TO beat FVV's locked-cat (FT%/3PTM/AST all rank ≤2) value — no tiebreak needed |
| #115 | VanVleet +0.52* [4th bet] | **VanVleet** | FVV 52, Collins 49, Nesmith 48, DDV 47 | eff +0.29 vs −0.44 best healthy → 4th bet admitted again (§5-P1) |
| #126 | NAW −0.71 … Ellis −0.73 | **Keon Ellis** | Ellis 52, Buzelis 51 (coin flip), NAW 50, Knueppel 49 | TO +1.4 into rank 8 |
| #139 | Portis −0.92 | **Portis** | Portis 58, Aldama 54, T.Harris 50, Horford 48 | REB rank 9 + fills 2nd C |
| #150 | Alvarado −1.59 vs Oubre −1.66 | **Oubre** | Oubre 52, Alvarado 51 (coin flip), Podziemski 49, Hunter 47 | Alvarado's ST feeds locked rank 2; −1.3 REB bleeds contested. [would be 3rd DAL] fired on Russell ✓ |
| #163 | Sexton −2.21 … Stewart −2.35 | **Isaiah Stewart** | Stewart 56, Sexton 50, Risacher 48, Rui 48 | deep-round specialist (BLK/REB/TO all contested) |
| #174 | Toppin −2.36 [3rd IND] vs K.George −2.39 | **Kyshawn George** | George 50, Toppin 49 (coin flip), LeVert 48, Dick 48 | soft 3rd-TEAM rule broke a genuine near-tie — worked as designed (advisory, not veto) |

Result: FG% 11 · FT% 4 · 3PTM 2 · PTS 7 · REB 5 · AST 4 · ST 2 · BLK 7 · TO 4. Incidents: none from the engine.

### Draft 3 — slot 10, seed 103 (picks 10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154, 159, 178)

| Pick | Board top (val) | Chosen | Confidence board | Rule notes |
|---|---|---|---|---|
| #10 | Holmgren +4.79 vs Mobley +4.76 | **Holmgren** | Chet 60, Mobley 59 (coin flip), Cade 57, Daniels 56 | all healthy |
| #15 | JJJ +4.41 vs Mitchell +4.38 | **Mitchell** | Mitchell 61, JJJ 57, Butler 57, J.Williams 56 | Mitchell hits all four weak cats; JJJ feeds locked BLK |
| #34 | Haliburton +3.76* vs Bane +3.44 | **Haliburton** | Hali 63 [1st bet], Bane 60, Booker 57, Reaves 55 | 8.5% — outside band. New flag observed: LeBron [unsigned-fa-monitor], team FA (I-6) |
| #39 | Reaves +2.96 vs Kawhi +2.78* [inj-risk] | **Reaves** | Reaves 58, Kawhi 55, LeBron 54, Bam 53, Tatum 52 | **CHANGED (discount)** — old adj Kawhi +3.03 > Reaves; new +2.78 puts healthy on top. (Session interruption occurred at this turn — recovered clean, I-5) |
| #58 | Tatum +2.68* [2nd bet] | **Tatum** | Tatum 60, Markkanen 54, Ware 52, Lopez 51 | eff +2.28, 39% clear |
| #63 | Lillard +2.34* [3rd bet] vs Sheppard/Ware | **Kel'el Ware** | Ware 57, Sheppard 55 (coin flip), Lillard 54 (coin flip), Fox 53 | **CHANGED** — old rules: Dame eff +1.91 tops both; new eff +1.64 ties Sheppard (tiebreak demotes) and Ware's contested FG%/REB/BLK triple-fit wins the slot |
| #82 | Lillard +2.34* [3rd bet] vs Sheppard +1.61 | **Sheppard** | Sheppard 56, Lillard 54 (coin flip), Pritchard 53, D.Murray 51 | **CHANGED** — third draft running, same mechanism (D1 #73, D2 #78) |
| #87 | Lillard +2.34* [3rd bet] | **Lillard** | Lillard 58, D.Murray 52, Ayton 50, Wallace 49 | eff +1.64, 73% clear — admitted |
| #106 | VanVleet +0.52* [4th bet] vs Gafford +0.11 | **Gafford** | Gafford 57, Gordon 51, FVV 50, K.Murray 48 | ⚠ LEAN fired (7G vs 3F) ✓ — LEAN + contested FG%/BLK/REB beat the 4th bet on merit |
| #111 | VanVleet +0.52* [4th bet] | **Camara** | Camara 53, K.Murray 52 (coin flip), FVV 49, Edgecombe 48 | ST rescue + LEAN rebalance |
| #130 | VanVleet +0.52* [4th bet] vs Nembhard −0.83 | **VanVleet** | FVV 53, Portis 49, Nembhard 48, Randle 47 | eff +0.29, 1.1z clear → 4th bet admitted in **all three drafts** (§5-P1) |
| #135 | Ball −0.79 [inj-risk] vs Portis −0.92 | **Portis** | Portis 54, Ball 51 (coin flip), Aldama 51, Beal 47 | **CHANGED (tiebreak only)** — negatives undiscounted; 0.13z tie → healthy. [would be 3rd POR] fired on Holiday & Sharpe ✓ |
| #154 | Hunter −1.85 vs Nurkic −2.08 | **Nurkic** | Nurkic 53, Hunter 52 (coin flip), Watson 49, Bogdanovic 47 | contested REB/FG% over locked-TO value |
| #159 | Bailey −2.17 … Watson −2.19 | **Watson** | Watson 53, Bailey 51 (coin flip), Sexton 49, Rui 48 | BLK specialist |
| #178 | Clifford −2.41 [rookie-proj] | **Strus** | Strus 52, Clifford 51 (coin flip), O'Neale 51, Trent 49 | 3PTM into contested rank 6 |

Result: FG% 10 · FT% 4 · 3PTM 5 · PTS 10 · REB 7 · AST 5 · ST 8 · BLK 6 · TO 3. Incidents: I-5 (session interruption, recovered).

### Incident register (all drafts)

| # | Class | Detail | Engine response | Resolution |
|---|---|---|---|---|
| I-0 | Pre-flight halt (correct) | First repo verification found OLD discounts (0.7/0.85) and no tiebreak rule | n/a — operator halt per mission instruction | David pulled via GitHub Desktop; re-verified 0.60/0.78 + tiebreak at `03da7f9` before any draft. **The system working, not failing.** |
| I-1 | Near-miss (doc/UX) | `draft turn "my:X" --expect N` emits a decision card computed **before** the arena bots advance — at D1 #24 that pre-bot card still showed Jokic available | As coded — the card reflects state at command time | Operator rule adopted: only the post-`live` card is authoritative. No wrong pick resulted. Candidate for a doc note (§5-P5) |
| I-2 | Environment | `rm draft_state.json` in the mounted repo → "Operation not permitted" (sandbox restriction, not engine) | n/a | Per-draft `HOOPS_DRAFT_STATE=arena/results/live_slotN.json` (env var honored by both arena.py and hoops.py; also keeps the repo root clean) |
| I-3 | Doc tension | Skill speed rule says "exactly ONE command per turn"; arena live mode's own pause banner instructs a card call (`draft turn ""`) **plus** a log call per turn | n/a | Followed the arena's documented two-call pattern, `--expect` on both. Zero state drift across all 90 calls. Codify the carve-out (§5-P4) |
| I-4 | Watch item — did NOT occur | Stale-data banner (freshness stamped 2026-07-11, drafts run 07-12) leaking into draft commands | Banner correctly suppressed on every one of 96 draft-family commands (90 turn + 3 status + 3 matrix) | None needed — suppression boundary held ✓ |
| I-5 | Session interruption | Tool result lost at D3 pick #39 (card already displayed, pick not yet logged) | n/a | Applied LESSONS #1: verified state before re-sending (`draft status` → 38 picks, roster intact, no double-log), then proceeded. `--expect 38` on the log call confirmed. Zero corruption |
| I-6 | Doc gap (minor) | `[unsigned-fa-monitor]` flag (LeBron, team FA) not in the skill's bracket-flag taxonomy | Card rendered it fine | Relayed the flag verbatim per general rule; add to skill flag list when next edited (§5-P6) |
| I-7 | CLI quirk (minor) | `tournament --out X.json` treats X.json as a **directory**, writing `X.json/tournament_seed1.json` | As coded | Cosmetic; gitignored either way (§5-P7) |
| I-8 | Cross-pool check (clean) | Bots draft from frozen 2025-10-21 snapshot while cards price from live 2026 CSV — checked all 495 bot picks for names missing from the live pool | 0 missing in all three drafts | No action. Risk remains theoretical if either pool diverges (§5-P8) |

Not observed anywhere in 540 picks / 96 engine commands: `--expect` mismatch, surname-collision HALT, correction-drift HALT, UNKNOWN quarantine, ambiguity auto-resolve ("assumed over"), numbering drift, duplicate-feed skip, feasibility warning (⚠ slot-unfillable), slow or malformed card output. The negative incident classes simply had no trigger conditions this session — all feeds were operator-typed full names against a paused engine, which is the easy case; this run does NOT re-validate the collision/drift machinery under adversarial name feeds (see §3).

---

## 3. Integrity verdict

**Every documented rule that had a trigger condition fired, and fired consistently across all three slots.**

- `--expect` handshake: present on 100% of feeds (45 card calls + 45 log calls); zero mismatches; correctly validated recovery after the I-5 interruption. Post-run mechanical audit: all three states hold exactly 180 picks, user picks sit at the exact snake positions for slots 1/6/10, zero UNKNOWNs, zero duplicate names.
- Injury-adjusted pricing: `*` values matched 0.60/0.78 math at every check (e.g., AD 7.03 raw → +5.48; Hali 6.27 raw → +3.76).
- `[2nd+ recovery bet]` tag: appeared exactly when roster recovery count ≥1, all drafts.
- Healthy tiebreak: fired in 9 turns, decided 8 picks, applied identically in equivalent situations across drafts (D1 #73 ≡ D2 #78 ≡ D3 #82).
- Soft rules: [would be 3rd TEAM] fired 6 times (IND, DAL, POR), correctly advisory — it broke exactly one near-tie (D2 #174) and vetoed nothing. ⚠ LEAN fired once (D3 #106, 7G/3F) and correctly informed without overriding.
- Stale-banner suppression boundary: held across ~140 draft-family commands (I-4).
- Deep-draft phase shift (position-weight → specialist at ~R11): observable in the boards and applied.

**Rules churning against each other — two real cases, one resolved, one open:**

1. **Tiebreak band's reference value (OPEN — §5-P2).** At D2 #54 the ~5% band does not fire against Tatum's adjusted value (+2.68, 16% gap to Herro) but does fire against his recovery-compounded judgment (+2.28, 1.3% gap). The skill defines the band on "adjusted value" but defines compounding as a separate operator-side multiplication, so the two rules genuinely disagree about the comparison number. Resolved in-draft toward the calibration intent (prefer healthy); this needs codification.
2. **Healthy tiebreak vs "clearly wins contested categories" carve-out (RESOLVED in practice).** At D1 #24, Haliburton was within 2% on value but clearly better in the two weakest categories. Read strictly, the carve-out could swallow the tiebreak in almost every tie (near-ties usually differ in category shape). Applied the narrow reading — the carve-out rescues flagged players who clearly win on *value*, not on fit alone — consistently in all similar turns. Recommend writing that reading down (§5-P2).

**Honest performance note (the system working, not the operator excelling):** the council-style user seat produced no dominant roster. D1 profiles as a BLK/ST/FT% build (leads 8/9 cats over its top rival but sits mid-pack in PTS/REB league-wide); D2 locked 3PTM/ST/TO/AST but punted FG% de facto (11/12) without ever committing to the punt; D3 is the most balanced and least top-heavy (best rank: TO 3). The fresh baseline below still has `council` mid-table (9.28%), ~5 points behind `safe_floor` — consistent with the arena's standing finding that availability discipline beats clever weighting, and consistent with these three rosters each carrying four recovery bets.

---

## 4. Effect of the new discounts

**Concrete picks changed (13 of 45 user turns, 29%):**

| Draft | Picks changed vs old ×0.85/×0.70 | Mechanism |
|---|---|---|
| D1 (slot 1) | #24 Murray (not Hali), #25 Vucevic (not Hali), #49 Flagg (not Tatum), #73 Sheppard (not Dame), #145 Alvarado (not Melton) | tiebreak ×2, compounding+tiebreak ×2, tiebreak-on-negatives ×1 |
| D2 (slot 6) | #6 KAT (not AD), #43 Flagg (not Tatum), #54 Herro (not Tatum), #78 Sheppard (not Dame) | tiebreak ×1, compounding+tiebreak ×3 |
| D3 (slot 10) | #39 Reaves (not Kawhi), #63 Ware (not Dame), #82 Sheppard (not Dame), #135 Portis (not Ball) | discount ×1, compounding+tiebreak ×2, tiebreak ×1 |

The healthy tiebreak was the deciding mechanism in 8 of the 13 (it fired in 9 turns total; at D1 #24/#25 the deepened discount alone had already closed the gap the tiebreak then broke). Net directional effect: **every changed pick moved from a flagged player to a healthy one** — the rules never churned in the opposite direction.

**What the discounts did and did not change in roster composition:**

- **Risk-flagged players: eliminated.** 0 across all three rosters. Old-rule boards would have taken AD (#6) and Kawhi (#39) outright; Melton, Ball, Beal, Smart were all demoted at tie-points. The ×0.78 + tiebreak combination is doing exactly what the calibration intended (risk-flagged played 51% of games vs 75% assumed).
- **Recovery-flagged players: unchanged in count, later in position.** All three rosters converged on the **identical four recovery players** — Haliburton, Tatum, Lillard, VanVleet — because after the deepened ×0.60 they still out-price the healthy shelf at the point it collapses (rounds 4–11). The 2nd/3rd/4th concurrent bets were each admitted on a clear compounded-value gap (§2). Flagged-player count per roster: **4 of 15 (27%), 4× the recovery concentration the "drafts as a favorite" principle contemplates** — and the calibration data says recovery players actually played ~9% of games vs the 60% the discount assumes. The discount deepening moved these players from rounds 2–4 (old boards) to rounds 4–11 (observed) but did not stop the accumulation. This is the report's central finding: **×0.60 prices the mean; nothing on the draft side prices the concentration.**
- The one countervailing force observed: contested-category weighting + LEAN beat the 4th bet on merit twice (D2 #102, D3 #106/#111) — but only when a healthy specialist happened to fit multiple weak categories; it is not a reliable guard.

**Fresh tournament baseline (post-discount arena pricing) vs old:**

`tournament --seasons 200 --seed 1 --seeds 3 --rotations 3` → seeds [1, 98, 195], 21,600 seasons/strategy. Raw board: `arena/results/tournament_postdiscount_2026-07-12.json/tournament_seed1.json`.

| Strategy | NEW champ% (±spread) | OLD champ% (README baseline) | Δ |
|---|---|---|---|
| safe_floor | **14.20** (±1.29) | 14.9 (±0.9) | −0.7 |
| stars | 10.78 (±1.28) | 10.1 | +0.7 |
| punt_ft | 10.39 (±1.04) | 10.2 | +0.2 |
| bpa_pure | 10.16 (±1.29) | 9.9 | +0.3 |
| punt_ft_to | 9.44 (±2.53) | — | |
| scarcity | 9.37 (±0.15) | — | |
| **council** | **9.28** (±1.31) | 8.4 (±1.7) | **+0.9** |
| slot_filler | 9.09 (±0.50) | — | |
| specialist | 6.15 (±1.14) | — | |
| market | 4.82 (±2.90) | — | |
| punt_ast | 4.46 (±0.99) | — | |
| upside | 1.85 (±0.53) | 2.8 | −0.9 |

Reading, honestly: council's +0.9 and safe_floor's −0.7 are both **within cross-seed spread** — per the statistician's own audit rule (gaps under ~2 points need ~10 seeds), treat the deltas as directionally encouraging, not established. What IS solid: **safe_floor remains ~3.4–5 points clear of the field after the discounts** — deepening the mean-price did not close the availability gap, which independently corroborates the concentration finding above. (Old and new boards also differ by rotation scheme — the README baseline aggregated differently — one more reason not to over-read small deltas.)

---

## 5. Proposed fixes / codification candidates — ALL GATED

Nothing below was changed this session. `scripts/hoops.py`, `data/`, and both skills are untouched. Each item requires the codification gate: 3+ seeds, adversarial review, owner sign-off.

- **P1 (GATED, highest value): price recovery concentration, or cap it.** Evidence: identical 4-recovery convergence in 3/3 drafts at 3 different slots; calibration says recovery ≈9% games played vs 60% assumed; safe_floor's persistent ~4-point lead. Candidate designs to arena-test: (a) steeper operator compounding (e.g. ×0.75/×0.5/×0.3 for 2nd/3rd/4th), (b) a hard soft-rule "max 2 concurrent recovery bets absent a >2× value gap", (c) pricing variance directly in `adj_value` (LESSONS #5's "variance needs its own price"). Test all three as arena strategies before touching production.
- **P2 (GATED): define the tiebreak band's reference number.** Codify: the ~5% band compares the healthy candidate against the flagged candidate's **fully compounded judgment** (adjusted value × concentration multiplier), and the "clearly wins contested categories" carve-out applies only when the flagged player clearly wins on that same number — fit alone doesn't invoke it. This is the reading applied consistently this session (D2 #54; D1 #24).
- **P3 (GATED): define multipliers beyond the 3rd concurrent recovery bet.** The skill stops at ×0.7/3rd; a 4th arose in all three drafts and required an undocumented extrapolation (×0.55 used, stated each time).
- **P4 (GATED, skill wording): carve out arena live mode in the speed rule.** "Exactly ONE command" should read "exactly one *feed*; in arena live mode the empty-feed card call plus the my: log call, each with --expect, constitute one turn." Matches the arena's own pause banner (I-3).
- **P5 (GATED, doc note): post-log cards are pre-bot in live mode** — add one line to the arena README: "only the card printed after the latest `live` call is authoritative" (I-1).
- **P6 (GATED, doc note): add `[unsigned-fa-monitor]` to the skill's flag taxonomy** (I-6).
- **P7 (GATED, cosmetic): `tournament --out` treats the path as a directory** — either document or fix to write the file named (I-7).
- **P8 (GATED, monitoring): add a startup cross-pool check to live mode** — warn if any frozen-snapshot name is absent from the live CSV (0 today, but silent roster-total drift if the pools diverge) (I-8).

---

*Report written by the Cowork session of 2026-07-12. Raw artifacts: `arena/results/draft{1,2,3}_slot{1,6,10}_status.txt`, `arena/results/live_state_slot1_2026-07-12.json`, `arena/results/live_slot{6,10}.json`, `arena/results/tournament_postdiscount_2026-07-12.json/`. State files and raw JSON are gitignored; this report and LESSONS.md are the committed record.*
