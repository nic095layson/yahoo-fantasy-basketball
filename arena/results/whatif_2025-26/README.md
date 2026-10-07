# What if the card had drafted your 2025-26 team? — the league redrafted from seat 4, graded on what the season then did

**Owner request (2026-10-07, verbatim):** "Conduct the draft with yourself, but you're drafting in my seat (#4). Draft using your 9Cat fantasy skillset, and used the changed pick for the other 11 personalities with their tendencies from past draft data I've provided to you. Then simulate the season with the team and rosters you drafted, and let me know the differences in winning, and your findings."

**Method.** The real 2025-26 draft (156 picks, `arena/data/league_draft_2025-26_raw_2026-10-01.txt`; seats from the team-name map: 1 Hegi, 2 JCo, 3 Martin, 4 you, 5 Will, 6 Kyle, 7 Oblena, 8 Kevin, 9 John, 10 Noah, 11 Cayas, 12 Robby) was replayed with the deck's own engine (v49, rev 269c522): the owner at seat 4 takes the card's #1 at every turn (`rankCard(decwScores(cardPool))`), the eleven league-mates draft with `managerScores` (the E18 profiles as shipped, Yahoo's own rank as the value axis from round 7) in their real seats, 30 seeded rooms (`redraft_rooms.json`; room 1000 is the canonical one shown here). Knowledge at draft time = the pool on file for 2025-10-21 (220 rows; six late picks absent from it were added on their 2024-25 Basketball-Reference lines, Yang Hansen on a rookie-center placeholder) and Yahoo's pre-draft ranks of 10/16 (180 of 200 resolved). Season outcome = every man's actual 2025-26 Basketball-Reference per-game line scaled by games played over 82 (no in-season moves; Haliburton, Irving, Lillard, VanVleet and Brogdon at zero); the grade is the arena's weekly model and 18,000 CRN seasons on the league's real eight-team bracket, exactly as every mock is graded. Two rulers: **ex ante** (the draft-time lines) and **ex post** (the actual lines).

## 1. The headline

| roster of seat 4 | ruler | ECW (rank of 12) | favored | title % (rank) | playoff % | category ranks (weekly) |
|---|---|---|---|---|---|---|
| your real draft | ex ante | 5.476 (1) | 11 of 11 | **37.37** (1) | 99.95 | FG% 5 · FT% 2 · 3PTM 5 · PTS 2 · REB 12 · AST 11 · ST 1 · BLK 2 · TO 1 |
| the card's draft (room 1000) | ex ante | 5.447 (1) | 11 of 11 | **33.68** (1) | 99.87 | FG% 5 · FT% 5 · 3PTM 1 · PTS 7 · REB 5 · AST 11 · ST 4 · BLK 2 · TO 1 |
| your real draft | ex post | 6.074 (1) | 11 of 11 | **42.51** (1) | 100.00 | FG% 8 · FT% 1 · 3PTM 2 · PTS 3 · REB 8 · AST 7 · ST 1 · BLK 4 · TO 3 |
| the card's draft (room 1000) | ex post | 5.898 (1) | 11 of 11 | **32.77** (1) | 100.00 | FG% 12 · FT% 6 · 3PTM 1 · PTS 5 · REB 3 · AST 6 · ST 1 · BLK 1 · TO 6 |

Across the 30 rooms, the card's seat-4 roster — ex ante: ECW 5.682 median (range 5.360–5.889), rank 1 in 30 of 30 rooms, title odds 42.44% median (range 32.10–50.48), beating the real roster's 37.37% in 24 of 30. Ex post: ECW 6.299 median (range 5.056–6.534), rank 1 in 22 of 30 rooms, title odds 54.30% median (range 4.97–71.15), beating the real roster's 42.51% in 20 of 30.

**Against your real opponents** — every card roster dropped into the real room with the eleven real rosters unchanged (a hypothetical that isolates the roster from the room; 6,000 CRN seasons per roster, seed 11):

| seat-4 roster | ruler | ECW median (range) | title % median (range) | beats your real roster |
|---|---|---|---|---|
| your real roster | ex ante | 5.476 | 36.83 | — |
| the 30 card rosters | ex ante | 5.777 (5.513–5.850) | 44.39 (34.57–47.73) | 23 of 30 |
| the 20 that opened with Gilgeous-Alexander (your real pick) | ex ante | 5.800 (5.639–5.850) | 45.25 (39.53–47.73) | 20 of 20 |
| the 10 that opened with Dončić (Gilgeous-Alexander gone at #3) | ex ante | 5.559 (5.513–5.741) | 36.21 (34.57–41.43) | 3 of 10 |
| your real roster | ex post | 6.074 | 42.10 | — |
| the 30 card rosters | ex post | 6.242 (5.004–6.510) | 51.18 (8.32–64.43) | 23 of 30 |
| the 20 that opened with Gilgeous-Alexander (your real pick) | ex post | 6.347 (5.913–6.510) | 54.05 (34.98–64.43) | 19 of 20 |
| the 10 that opened with Dončić (Gilgeous-Alexander gone at #3) | ex post | 5.861 (5.004–6.169) | 36.17 (8.32–56.30) | 4 of 10 |

**The thirty rooms** (own room = the card's roster against the eleven bots of that room; vs real room = the same roster against your real opponents):

| room | card's first pick | own room ex ante ECW / title % | own room ex post ECW / title % (rank) | vs real room ex ante title % | vs real room ex post ECW / title % |
|---|---|---|---|---|---|
| 1017 | Shai Gilgeous-Alexander | 5.615 / 41.03 | 6.471 / 58.13 (1) | 45.05 | 6.510 / 64.43 |
| 1024 | Shai Gilgeous-Alexander | 5.623 / 41.75 | 6.497 / 71.15 (1) | 42.30 | 6.444 / 62.17 |
| 1013 | Shai Gilgeous-Alexander | 5.712 / 45.25 | 6.534 / 61.90 (1) | 44.37 | 6.429 / 61.05 |
| 1001 | Shai Gilgeous-Alexander | 5.729 / 46.52 | 6.444 / 56.08 (1) | 45.25 | 6.410 / 60.75 |
| 1025 | Shai Gilgeous-Alexander | 5.696 / 42.65 | 6.489 / 66.05 (1) | 45.25 | 6.410 / 60.75 |
| 1027 | Shai Gilgeous-Alexander | 5.764 / 45.28 | 6.487 / 69.08 (1) | 45.25 | 6.410 / 60.75 |
| 1007 | Shai Gilgeous-Alexander | 5.616 / 42.07 | 6.437 / 61.15 (1) | 44.42 | 6.455 / 60.28 |
| 1016 | Shai Gilgeous-Alexander | 5.691 / 43.75 | 6.416 / 60.97 (1) | 45.87 | 6.421 / 58.67 |
| 1009 | Shai Gilgeous-Alexander | 5.789 / 44.67 | 6.464 / 46.70 (1) | 45.60 | 6.386 / 56.52 |
| 1029 | Luka Doncic | 5.590 / 38.17 | 6.109 / 49.33 (1) | 40.40 | 6.169 / 56.30 |
| 1006 | Shai Gilgeous-Alexander | 5.737 / 46.35 | 6.501 / 69.93 (1) | 45.87 | 6.420 / 54.75 |
| 1010 | Shai Gilgeous-Alexander | 5.705 / 43.27 | 6.238 / 48.57 (1) | 45.03 | 6.283 / 53.35 |
| 1026 | Shai Gilgeous-Alexander | 5.688 / 44.02 | 6.295 / 42.32 (2) | 45.03 | 6.283 / 53.35 |
| 1028 | Shai Gilgeous-Alexander | 5.609 / 42.23 | 6.454 / 56.78 (1) | 39.53 | 6.307 / 53.30 |
| 1002 | Shai Gilgeous-Alexander | 5.792 / 45.50 | 6.358 / 56.97 (1) | 47.73 | 6.242 / 51.18 |
| 1011 | Shai Gilgeous-Alexander | 5.881 / 49.37 | 6.296 / 63.43 (1) | 47.73 | 6.242 / 51.18 |
| 1020 | Shai Gilgeous-Alexander | 5.777 / 48.55 | 6.301 / 63.28 (1) | 47.73 | 6.242 / 51.18 |
| 1021 | Shai Gilgeous-Alexander | 5.889 / 50.48 | 6.427 / 67.57 (1) | 47.73 | 6.242 / 51.18 |
| 1023 | Shai Gilgeous-Alexander | 5.677 / 43.23 | 6.369 / 65.92 (1) | 43.52 | 6.197 / 49.25 |
| 1019 | Luka Doncic | 5.622 / 40.12 | 6.008 / 39.67 (2) | 41.17 | 6.023 / 48.35 |
| 1014 | Shai Gilgeous-Alexander | 5.562 / 42.17 | 6.155 / 52.52 (1) | 40.10 | 6.115 / 48.33 |
| 1003 | Luka Doncic | 5.458 / 36.15 | 6.017 / 49.53 (1) | 35.02 | 5.987 / 44.38 |
| 1004 | Luka Doncic | 5.483 / 37.10 | 6.054 / 41.35 (2) | 35.02 | 5.987 / 44.38 |
| 1000 | Luka Doncic | 5.447 / 34.78 | 5.898 / 32.92 (1) | 34.57 | 5.923 / 39.22 |
| 1018 | Shai Gilgeous-Alexander | 5.790 / 47.48 | 6.046 / 37.98 (1) | 46.67 | 5.913 / 34.98 |
| 1022 | Luka Doncic | 5.706 / 41.32 | 5.827 / 26.08 (2) | 41.43 | 5.798 / 33.12 |
| 1008 | Luka Doncic | 5.360 / 32.10 | 5.601 / 23.53 (2) | 34.85 | 5.615 / 24.77 |
| 1005 | Luka Doncic | 5.428 / 36.43 | 5.542 / 24.75 (2) | 35.87 | 5.474 / 19.87 |
| 1015 | Luka Doncic | 5.494 / 34.72 | 5.538 / 4.97 (4) | 36.55 | 5.488 / 19.80 |
| 1012 | Luka Doncic | 5.527 / 38.42 | 5.056 / 7.42 (4) | 36.82 | 5.004 / 8.32 |

## 2. The two rosters, man by man

Draft-time value rank = 9-cat z-sum rank on the 2025-10-21 pool; Yahoo = pre-draft rank 10/16; actual = z-sum rank on the 2025-26 lines scaled by games.

**Your real picks**

| pick | player | draft-time value | Yahoo | actual rank | actual z | GP |
|---|---|---|---|---|---|---|
| #4 | Shai Gilgeous-Alexander | 3 | 3 | 2 | +9.89 | 68 |
| #21 | Jalen Brunson | 42 | 19 | 31 | +2.64 | 74 |
| #28 | Jaren Jackson Jr. | 17 | 27 | 95 | -1.66 | 48 |
| #45 | Jamal Murray | 22 | 30 | 7 | +6.76 | 75 |
| #52 | OG Anunoby | 30 | 74 | 36 | +2.33 | 67 |
| #69 | Kristaps Porzingis | 40 | 45 | 170 | -4.93 | 32 |
| #76 | Kawhi Leonard | 28 | 41 | 5 | +7.52 | 65 |
| #93 | Donovan Clingan | 90 | 92 | 20 | +4.18 | 77 |
| #100 | Tari Eason | 47 | 93 | 115 | -2.69 | 60 |
| #117 | Herbert Jones | 84 | 109 | 136 | -3.29 | 56 |
| #124 | Brook Lopez | 60 | 135 | 93 | -1.57 | 75 |
| #141 | Donte DiVincenzo | 111 | 113 | 44 | +1.83 | 82 |
| #148 | Gary Trent Jr. | 177 | 181 | 183 | -6.43 | 65 |
| | sum of z | +18.81 | | | +14.58 | |

**The card's picks (room 1000)**

| pick | player | draft-time value | Yahoo | actual rank | actual z | GP |
|---|---|---|---|---|---|---|
| #4 | Luka Doncic | 4 | 4 | 10 | +5.79 | 64 |
| #21 | Derrick White | 27 | 31 | 19 | +4.22 | 77 |
| #28 | Nikola Vucevic | 25 | 56 | 62 | +0.50 | 64 |
| #45 | OG Anunoby | 30 | 74 | 36 | +2.33 | 67 |
| #52 | Onyeka Okongwu | 56 | 101 | 23 | +3.20 | 74 |
| #69 | Cameron Johnson | 48 | 99 | 124 | -2.94 | 54 |
| #76 | Tari Eason | 47 | 93 | 115 | -2.69 | 60 |
| #93 | Brook Lopez | 60 | 135 | 93 | -1.57 | 75 |
| #100 | Reed Sheppard | 79 | 119 | 28 | +2.98 | 82 |
| #117 | PJ Washington | 99 | — | 117 | -2.73 | 56 |
| #124 | Aaron Gordon | 100 | 130 | 173 | -5.16 | 36 |
| #141 | VJ Edgecombe | 103 | 157 | 39 | +2.10 | 75 |
| #148 | Kon Knueppel | 123 | 171 | 29 | +2.97 | 81 |
| | sum of z | +11.00 | | | +9.00 | |

The card's Top-5 at each of its turns, with what you took there in the real room:

| turn | 🎯 | the rest of the Top-5 | your real pick at that turn |
|---|---|---|---|
| #4 | Luka Doncic | Tyrese Maxey, Karl-Anthony Towns, Anthony Edwards, Donovan Mitchell | Shai Gilgeous-Alexander |
| #21 | Derrick White | Nikola Vucevic, Trey Murphy III, OG Anunoby, Amen Thompson | Jalen Brunson |
| #28 | Nikola Vucevic | OG Anunoby, Trey Murphy III, Domantas Sabonis, Myles Turner | Jaren Jackson Jr. |
| #45 | OG Anunoby | Tari Eason, Walker Kessler, Jakob Poeltl, Cooper Flagg | Jamal Murray |
| #52 | Onyeka Okongwu | Jakob Poeltl, Tari Eason, Christian Braun, Brook Lopez | OG Anunoby |
| #69 | Cameron Johnson | Tari Eason, Jalen Suggs, Brook Lopez, Mikal Bridges | Kristaps Porzingis |
| #76 | Tari Eason | Brook Lopez, Mikal Bridges, Kel'el Ware, Jalen Suggs | Kawhi Leonard |
| #93 | Brook Lopez | Kel'el Ware, Jalen Suggs, Josh Hart, CJ McCollum | Donovan Clingan |
| #100 | Reed Sheppard | CJ McCollum, Kel'el Ware, Cason Wallace, Aaron Gordon | Tari Eason |
| #117 | PJ Washington | Jaden McDaniels, Aaron Gordon, Cason Wallace, Quentin Grimes | Herbert Jones |
| #124 | Aaron Gordon | Cason Wallace, Quentin Grimes, Malik Monk, VJ Edgecombe | Brook Lopez |
| #141 | VJ Edgecombe | Jabari Smith Jr., Bilal Coulibaly, Kon Knueppel, Dylan Harper | Donte DiVincenzo |
| #148 | Kon Knueppel | Bilal Coulibaly, Kelly Oubre Jr., Keon Ellis, Collin Sexton | Gary Trent Jr. |

Where your real men went in the redraft: Shai Gilgeous-Alexander #3 to Martin; Jalen Brunson #29 to Will; Jaren Jackson Jr. #18 to Oblena; Jamal Murray #24 to Hegi; OG Anunoby #45 to David; Kristaps Porzingis #42 to Oblena; Kawhi Leonard #35 to Cayas; Donovan Clingan #98 to JCo; Tari Eason #76 to David; Herbert Jones #111 to Noah; Brook Lopez #93 to David; Donte DiVincenzo #115 to Kyle; Gary Trent Jr. undrafted. Where the card's men went in the real room: Luka Doncic #3 to Martin; Derrick White #38 to Cayas; Nikola Vucevic #62 to Cayas; OG Anunoby #52 to David; Onyeka Okongwu #92 to Will; Cameron Johnson #99 to Martin; Tari Eason #100 to David; Brook Lopez #124 to David; Reed Sheppard #110 to Cayas; PJ Washington #135 to Noah; Aaron Gordon #105 to John; VJ Edgecombe undrafted; Kon Knueppel #149 to Will.

## 3. The room around you

The redraft reproduced 7 of the real room's 156 picks at the same number (Jokić #1 to Hegi and Wembanyama #2 to JCo among them); in room 1000 Martin took Gilgeous-Alexander at #3, which is why the card's first pick is Dončić — across the 30 rooms the card opened with Gilgeous-Alexander 20 times and Dončić 10.

**Ex ante, all twelve seats (room 1000):**

| seat | manager | ECW | title % | playoff % |
|---|---|---|---|---|
| 4 | **you** | 5.447 | 33.68 | 99.87 |
| 1 | Hegi | 4.989 | 17.46 | 95.77 |
| 3 | Martin | 4.749 | 11.98 | 90.91 |
| 2 | JCo | 4.699 | 11.48 | 89.26 |
| 8 | Kevin | 4.540 | 7.32 | 79.11 |
| 10 | Noah | 4.540 | 6.22 | 73.48 |
| 7 | Oblena | 4.232 | 2.42 | 51.59 |
| 9 | John | 4.232 | 2.68 | 51.43 |
| 6 | Kyle | 4.183 | 2.04 | 49.31 |
| 12 | Robby | 4.178 | 1.94 | 42.74 |
| 5 | Will | 4.127 | 1.49 | 37.99 |
| 11 | Cayas | 4.084 | 1.29 | 38.53 |

**Ex post, all twelve seats (room 1000):**

| seat | manager | ECW | title % | playoff % |
|---|---|---|---|---|
| 4 | **you** | 5.898 | 32.77 | 100.00 |
| 1 | Hegi | 5.863 | 25.99 | 100.00 |
| 8 | Kevin | 5.740 | 21.14 | 100.00 |
| 11 | Cayas | 5.479 | 9.82 | 99.99 |
| 3 | Martin | 5.418 | 9.83 | 99.97 |
| 6 | Kyle | 4.029 | 0.19 | 71.02 |
| 2 | JCo | 3.961 | 0.14 | 65.83 |
| 5 | Will | 3.760 | 0.03 | 44.89 |
| 9 | John | 3.740 | 0.02 | 46.16 |
| 12 | Robby | 3.718 | 0.04 | 43.21 |
| 10 | Noah | 3.575 | 0.01 | 28.59 |
| 7 | Oblena | 2.818 | 0.00 | 0.34 |

## 4. Calibration — the real rosters on the real lines

Graded on the actual lines, the twelve real draft rosters rank by ECW: David 6.074, Will 5.836, Kevin 5.457, Martin 5.226, John 4.572, Kyle 4.384, Noah 4.336, Hegi 4.307, JCo 4.285, Oblena 4.255, Cayas 2.908, Robby 2.361. Your real roster is 1st on the model, at 6.074 expected categories a week against the 5.722 you actually won per week over the 18 regular-season weeks (103-58-1, the league's best record); Martin's champion roster sits 4th at 5.226, which is the bracket-variance story the scored weeks already told (three 5-4 playoff weeks).

| real roster | model ECW (ex post) | model title % | real finish |
|---|---|---|---|
| David | 6.074 | 42.51 | 6th after a round-1 exit (103-58-1, best record) |
| Will | 5.836 | 28.26 | 2nd |
| Kevin | 5.457 | 15.98 | — |
| Martin | 5.226 | 9.60 | champion (78-82-2 regular season) |
| John | 4.572 | 1.11 | — |
| Kyle | 4.384 | 0.64 | — |
| Noah | 4.336 | 0.63 | — |
| Hegi | 4.307 | 0.43 | — |
| JCo | 4.285 | 0.55 | 3rd |
| Oblena | 4.255 | 0.29 | — |
| Cayas | 2.908 | 0.00 | — |
| Robby | 2.361 | 0.00 | — |

## 5. Findings

1. **The exercise turns on pick 4, and there the card agrees with you.** In 20 of 30 rooms Martin took Dončić at #3 as he did in the real room and the card took Gilgeous-Alexander — your real pick; in the other 10 Martin took Gilgeous-Alexander and the card opened with Dončić. Those two branches are different seasons: against your real opponents on what actually happened, the Gilgeous-Alexander rosters win the title in 54.0 percent of seasons (median; 19 of 20 above your real roster's 42.1), the Dončić rosters in 36.2 (4 of 10 above). Room 1000, the pre-registered canonical seed, happens to be a Dončić room, which is why the headline table understates the typical card draft.
2. **With the same first pick, the card's roster would have beaten the one you drafted on both rulers** — at draft time 45.2 against 36.8 percent, and on the season that happened 54.0 against 42.1, with expected category wins 6.35 against 6.07 a week. It does it with less star value, not more: the card's rosters carry a lower 9-cat z-sum than yours (+9.0 against +14.6 on actual lines) and win on balance — your real roster conceded rebounds and assists at draft time (12th and 11th of 12 in the weekly model) and FG% on the actual lines (8th); the card's never does.
3. **Your real draft's hits were real, and large.** Gilgeous-Alexander finished #2 in 9-cat on the actual lines, Kawhi Leonard #5 on 65 games (the card never took him in 30 rooms — his inj-risk tag prices him at 0.78 availability, and that is the one place the tag cost you nothing and the card something), Jamal Murray #7, Donovan Clingan #20, Donte DiVincenzo #44. The misses were Porziņģis (#170, 32 games), Jaren Jackson Jr. (#95, 48 games), Gary Trent Jr. (#183) and Herbert Jones (#136). The card's typical roster (room 1006: Shai Gilgeous-Alexander, Nikola Vucevic, Trey Murphy III, OG Anunoby, Christian Braun, Michael Porter Jr., Onyeka Okongwu, Cameron Johnson, Kel'el Ware, Jaden McDaniels, Brook Lopez, VJ Edgecombe, Kon Knueppel) hit on Shai Gilgeous-Alexander (#2), Trey Murphy III (#17), OG Anunoby (#36), Onyeka Okongwu (#23), Kel'el Ware (#30), VJ Edgecombe (#39), Kon Knueppel (#29), and missed on Nikola Vučević (#62; the card takes him in every one of the 30 rooms, in round 2 in 28 of them, because the 2025-10-21 pool carried his 2024-25 line), Christian Braun (#164, 44 games), Cameron Johnson (#124).
4. **The model is honest about last season.** On the actual lines it ranks the twelve real rosters with yours first (6.074 expected categories a week against the 5.72 you actually won; 103-58-1 was the league's best record), Will second (he finished second), Martin's champion roster fourth at 9.6 percent title odds — the title went through three 5-4 playoff weeks, which is the bracket-variance story your scored weeks already told and the reason the arena grades on the real eight-team bracket. Your real roster's 100 percent playoff rate and 42.1 percent title odds say the same thing: the best regular-season team in this league wins the title well under half the time.
5. **What it says for the 14th.** The card's edge over your real draft is a middle-round edge — category coverage from round 2 on — and its first pick agreed with you. Its biggest miss (Vučević) is a lines problem, not a logic problem: the engine is only as good as the pool it ranks, which is what the WO-5 preseason refresh is for. And the one systematic cost in the other direction is the injury-risk tag: Kawhi at 0.78 availability was a profit for you and a pass for the card; D61-1/D67-1 (Lillard's tag) is the same question this season.
6. **The room.** The redraft reproduced 7 of the real room's 156 picks at the same number — Jokić to Hegi at #1 and Wembanyama to JCo at #2 among them — and the bots' own ex-post standings in the canonical room (Hegi, Kevin, Cayas, Martin behind you) are a model of the league, not the league: Cayas and Robby, whom the model ranks last on their real rosters, are the two seats whose first three picks played the fewest games: Cayas opened with Trae Young (15 games, 9-cat #205), Jalen Williams (33 games, 9-cat #168), Franz Wagner (34 games, 9-cat #167) and Robby with Domantas Sabonis (19 games, 9-cat #194), Bam Adebayo (73 games, 9-cat #22), Jaylen Brown (71 games, 9-cat #46); their rosters averaged 50.3 and 47.8 games played per man against 58.7 for the league. The five men who missed the whole season (Haliburton, Irving, Lillard, VanVleet, Brogdon) were drafted by nobody.

## Bounds

- The eleven bots are the E18 profiles, built from three seasons that include this one: their tendencies are partly in-sample here, and they are stochastic (30 rooms, one shown).
- Draft-time knowledge is the pool on file for 2025-10-21 and Yahoo's 10/16 ranks, not the lines you actually drafted on; the card's picks are the engine's, with no judgment layer.
- Actual production is per-game × games played / 82 with no in-season moves, so every roster carries its injuries in full and nobody streams; real managers did both. The five men who missed the whole season score zero.
- A redraft changes every other roster too, so the ex-post comparison is between two different leagues; only the owner's seat is compared with the real season, and the real season had trades and waivers this exercise cannot see.
- The weekly model and the bracket are the arena's (18,000 CRN seasons, seeds 11/23/47); the model's ECW is against the average opponent, not your actual schedule.

## Provenance

- Inputs: `arena/data/league_draft_2025-26_raw_2026-10-01.txt`, `arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt`, `arena/data/players_2025-10-21.csv`, `arena/data/weekly_matchups_2025-26.csv`; Basketball-Reference per-game tables for 2025-26 and 2024-25 fetched 2026-10-07 (parsed with `arena/mocks/whatif/bref.py`).
- Artifacts in `arena/results/whatif_2025-26/`: `pool_draft_time.csv`, `pool_actual_2025-26.csv`, `actual_gp_2025-26.json`, `redraft_rooms.json` (30 rooms with the card's Top-5 at every owner turn), `draft_state_real_2025-26.json`, `real_draft_2025-26.json`, `grades_2025-26.json`; scripts in `arena/mocks/whatif/` (`build_inputs.py`, `actual_lines.py`, `draft2025.mjs`, `grade2025.py`, `compare_picks.py`).
