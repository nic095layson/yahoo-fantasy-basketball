"""Canonicalize the owner-provided draft boards for all three real seasons
into arena/draft_boards.json: season -> [{pick, player, team, manager}].
Team->manager identity map from league_intel §12 / profiles.json."""
import json, os, unicodedata

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

MGR = {
 # 2025-26
 "JAMAL AL-QUETA": "David", "Gotta Be Bamonte": "Robby", "HalleLuka Amen": "Martin",
 "Itsy Bitsy Spida": "Oblena", "All guards no defense": "Kevin",
 "Devin Minutes in Heaven": "Noah", "IM SO HORT": "Cayas", "John's Cool Team": "John",
 "Not hurt just SARR": "Hegi", "The Konclave": "Will", "ur my only hope Anti-wan": "Kyle",
 "Wing Chun Wemby": "JCo",
 # 2024-25
 "David's Demure Team": "David", "Put Me in Coach": "Robby", "Sales & Markkanen": "Martin",
 "Match My Freak": "Oblena", "Day to Davis": "Kevin", "Poop and Scoot Streaks": "Noah",
 "BALLSACK LAVINE": "Cayas", "John's Matchless Team": "John",
 "Quickley Luk-a Fox and a Kat!!": "Hegi", "LAME TIME": "Will",
 "Jericho's Incredible Team": "Kyle", "MOO DURANT": "JCo",
 # 2023-24
 "LayBron": "David", "Poole-ootan Party": "Robby", "Martin you're him!": "Martin",
 "D.O.L.L.A.": "Oblena", "The Big Deuce": "Kevin", "Strokin my Saboner": "Noah",
 "REBUILDING SZN": "Cayas", "Steph BoyArdee": "John", "Sing to me Paolo": "Hegi",
 "TEAM MENISCUS TEAR": "Will", "Last Place HumilAyton": "Kyle", "Beats by Dray": "JCo",
}

# (round-major pick lists; team per pick explicit — no snake math needed)
S2526_ORDER = ["Not hurt just SARR", "Wing Chun Wemby", "HalleLuka Amen", "JAMAL AL-QUETA",
 "The Konclave", "ur my only hope Anti-wan", "Itsy Bitsy Spida", "All guards no defense",
 "John's Cool Team", "Devin Minutes in Heaven", "IM SO HORT", "Gotta Be Bamonte"]
S2526 = [
 ["Nikola Jokić","Victor Wembanyama","Luka Dončić","Shai Gilgeous-Alexander","Giannis Antetokounmpo","Anthony Edwards","Karl-Anthony Towns","Cade Cunningham","Anthony Davis","Devin Booker","Trae Young","Domantas Sabonis"],
 ["Bam Adebayo","Jalen Williams","James Harden","Tyrese Maxey","Stephen Curry","Donovan Mitchell","Evan Mobley","Kevin Durant","Jalen Brunson","Amen Thompson","Alperen Şengün","Josh Giddey"],
 ["Zion Williamson","LeBron James","Jalen Johnson","Jaren Jackson Jr.","Austin Reaves","Dyson Daniels","Chet Holmgren","LaMelo Ball","Scottie Barnes","Cooper Flagg","Franz Wagner","Jaylen Brown"],
 ["Jarrett Allen","Derrick White","Paolo Banchero","Trey Murphy III","Pascal Siakam","Myles Turner","Ivica Zubac","Brandon Miller","Jamal Murray","Jalen Duren","Jimmy Butler III","Ja Morant"],
 ["Deandre Ayton","Desmond Bane","Brandon Ingram","OG Anunoby","Deni Avdija","Lauri Markkanen","Coby White","Payton Pritchard","Miles Bridges","Ausar Thompson","De'Aaron Fox","Zach LaVine"],
 ["Jalen Green","Nikola Vučević","Bennedict Mathurin","Julius Randle","DeMar DeRozan","Walker Kessler","Shaedon Sharpe","Mark Williams","Kristaps Porziņģis","Andrew Nembhard","Darius Garland","Immanuel Quickley"],
 ["Alex Sarr","Rudy Gobert","Joel Embiid","Kawhi Leonard","Matas Buzelis","John Collins","Jordan Poole","Michael Porter Jr.","Jakob Poeltl","RJ Barrett","Cam Thomas","Devin Vassell"],
 ["Christian Braun","Paul George","Naz Reid","Josh Hart","Kel'el Ware","Mikal Bridges","Anfernee Simons","Onyeka Okongwu","Donovan Clingan","Isaiah Hartenstein","Jrue Holiday","Andrew Wiggins"],
 ["Toumani Camara","Nic Claxton","Cameron Johnson","Tari Eason","Jaden Ivey","Santi Aldama","Yves Missi","Tyler Herro","Aaron Gordon","Keyonte George","Jabari Smith Jr.","Dillon Brooks"],
 ["Bradley Beal","Reed Sheppard","Dereck Lively II","Tobias Harris","Jaden McDaniels","Klay Thompson","CJ McCollum","Brandin Podziemski","Herbert Jones","Jalen Suggs","D'Angelo Russell","Kevin Porter Jr."],
 ["Aaron Nesmith","Kyle Kuzma","Kyshawn George","Brook Lopez","Cason Wallace","Norman Powell","Ace Bailey","Bobby Portis","Jeremy Sochan","Stephon Castle","Yang Hansen","Zaccharie Risacher"],
 ["Collin Sexton","Malik Monk","P.J. Washington","De'Andre Hunter","Quentin Grimes","Jaylen Wells","Nikola Jović","Neemias Queta","Donte DiVincenzo","Rui Hachimura","Dejounte Murray","Sam Hauser"],
 ["Cam Whitmore","Alex Caruso","Isaiah Collier","Gary Trent Jr.","Kon Knueppel","Nickeil Alexander-Walker","Bub Carrington","Draymond Green","Jaime Jaquez Jr.","Keegan Murray","Jayson Tatum","Obi Toppin"],
]

S2425_ORDER = ["LAME TIME", "Sales & Markkanen", "Put Me in Coach", "John's Matchless Team",
 "Quickley Luk-a Fox and a Kat!!", "Match My Freak", "Day to Davis", "MOO DURANT",
 "David's Demure Team", "Poop and Scoot Streaks", "BALLSACK LAVINE", "Jericho's Incredible Team"]
S2425 = [
 ["Victor Wembanyama","Nikola Jokić","Jayson Tatum","Shai Gilgeous-Alexander","Luka Dončić","Giannis Antetokounmpo","Anthony Davis","Tyrese Haliburton","Anthony Edwards","Trae Young","Stephen Curry","James Harden"],
 ["Domantas Sabonis","Joel Embiid","LaMelo Ball","Chet Holmgren","Kevin Durant","Scottie Barnes","Donovan Mitchell","Karl-Anthony Towns","LeBron James","Devin Booker","Jalen Brunson","Damian Lillard"],
 ["Evan Mobley","Lauri Markkanen","Jaren Jackson Jr.","Tyrese Maxey","De'Aaron Fox","Alperen Şengün","Jalen Williams","Cade Cunningham","Paul George","Fred VanVleet","Desmond Bane","Bam Adebayo"],
 ["Paolo Banchero","Kawhi Leonard","Jalen Johnson","Jaylen Brown","DeMar DeRozan","Pascal Siakam","Ja Morant","Dejounte Murray","Franz Wagner","Rudy Gobert","Myles Turner","Mikal Bridges"],
 ["Josh Giddey","Kyrie Irving","Jarrett Allen","Zion Williamson","Jalen Duren","Derrick White","Julius Randle","Nikola Vučević","Jamal Murray","Deandre Ayton","Nic Claxton","Jimmy Butler III"],
 ["Brandon Ingram","Michael Porter Jr.","Tobias Harris","Brandon Miller","Miles Bridges","D'Angelo Russell","Isaiah Hartenstein","Immanuel Quickley","Jrue Holiday","Darius Garland","Tyler Herro","Kyle Kuzma"],
 ["Bradley Beal","Jalen Suggs","Collin Sexton","Keegan Murray","Brook Lopez","RJ Barrett","Jonathan Kuminga","Jabari Smith Jr.","Zach LaVine","Jordan Poole","Anfernee Simons","Cam Thomas"],
 ["Bogdan Bogdanović","Clint Capela","Ivica Zubac","Trey Murphy III","Jonas Valančiūnas","Coby White","Austin Reaves","OG Anunoby","Jakob Poeltl","Devin Vassell","Alex Caruso","Jalen Green"],
 ["Daniel Gafford","Draymond Green","John Collins","Jerami Grant","Klay Thompson","Josh Hart","Naz Reid","CJ McCollum","Bobby Portis","Herbert Jones","Jusuf Nurkić","Terry Rozier"],
 ["Onyeka Okongwu","Donte DiVincenzo","Walker Kessler","Aaron Gordon","Mark Williams","Keyonte George","Zach Edey","Trayce Jackson-Davis","Amen Thompson","Brandin Podziemski","Jaime Jaquez Jr.","Jaden Ivey"],
 ["Malik Monk","Dereck Lively II","Deni Avdija","Kelly Oubre Jr.","Cameron Johnson","P.J. Washington","Norman Powell","Buddy Hield","Chris Paul","Khris Middleton","Ausar Thompson","Kentavious Caldwell-Pope"],
 ["Al Horford","Ben Simmons","Scoot Henderson","Marcus Smart","Kristaps Porziņģis","Tyus Jones","Jaden McDaniels","Caris LeVert","Jeremy Sochan","Andrew Wiggins","Jordan Clarkson","Kelly Olynyk"],
 ["Dyson Daniels","Alex Sarr","Keldon Johnson","Russell Westbrook","Wendell Carter Jr.","Dennis Schröder","Precious Achiuwa","Kevin Porter Jr.","Mike Conley","Grayson Allen","Harrison Barnes","Rui Hachimura"],
]

S2324_ORDER = ["REBUILDING SZN", "Sing to me Paolo", "Beats by Dray", "TEAM MENISCUS TEAR",
 "LayBron", "Last Place HumilAyton", "Martin you're him!", "The Big Deuce",
 "Strokin my Saboner", "Steph BoyArdee", "D.O.L.L.A.", "Poole-ootan Party"]
S2324 = [
 ["Nikola Jokić","Giannis Antetokounmpo","Tyrese Haliburton","Joel Embiid","Shai Gilgeous-Alexander","Kevin Durant","Luka Dončić","Jayson Tatum","LaMelo Ball","Stephen Curry","Damian Lillard","Anthony Davis"],
 ["Devin Booker","Trae Young","Anthony Edwards","Domantas Sabonis","Jaren Jackson Jr.","Donovan Mitchell","Kyrie Irving","Lauri Markkanen","Karl-Anthony Towns","Jimmy Butler III","Mikal Bridges","Cade Cunningham"],
 ["Victor Wembanyama","Bam Adebayo","Paul George","DeMar DeRozan","LeBron James","Walker Kessler","Pascal Siakam","Dejounte Murray","Jaylen Brown","Jalen Brunson","Desmond Bane","Kawhi Leonard"],
 ["Jordan Poole","Darius Garland","Kristaps Porziņģis","Myles Turner","Jamal Murray","Evan Mobley","Deandre Ayton","James Harden","De'Aaron Fox","Zion Williamson","Paolo Banchero","Chet Holmgren"],
 ["Alperen Şengün","Jrue Holiday","Nic Claxton","Julius Randle","OG Anunoby","Rudy Gobert","Brandon Ingram","Nikola Vučević","Josh Giddey","Zach LaVine","Tyrese Maxey","Fred VanVleet"],
 ["Jarrett Allen","Jalen Williams","Cameron Johnson","Anfernee Simons","Franz Wagner","Devin Vassell","Ja Morant","Ben Simmons","Tyler Herro","Bradley Beal","Andrew Wiggins","Scottie Barnes"],
 ["Marcus Smart","D'Angelo Russell","Chris Paul","Jerami Grant","Jabari Smith Jr.","Klay Thompson","Austin Reaves","Jalen Green","Kyle Kuzma","Brook Lopez","Mark Williams","Khris Middleton"],
 ["CJ McCollum","Buddy Hield","Michael Porter Jr.","Markelle Fultz","Jakob Poeltl","Tyus Jones","Jalen Duren","Daniel Gafford","Terry Rozier","Clint Capela","Mitchell Robinson","Tobias Harris"],
 ["Spencer Dinwiddie","Jordan Clarkson","Draymond Green","Onyeka Okongwu","Scoot Henderson","Keegan Murray","Jaden McDaniels","Jusuf Nurkić","Jonas Valančiūnas","Gary Trent Jr.","John Collins","Robert Williams III"],
 ["Aaron Gordon","Bruce Brown","Tre Jones","Derrick White","Russell Westbrook","Wendell Carter Jr.","Bennedict Mathurin","P.J. Washington","Ausar Thompson","Keldon Johnson","Kevon Looney","Shaedon Sharpe"],
 ["RJ Barrett","Steven Adams","Zach Collins","Kentavious Caldwell-Pope","De'Anthony Melton","Josh Hart","Brandon Miller","Obi Toppin","Trey Murphy III","Immanuel Quickley","Ivica Zubac","Rui Hachimura"],
 ["Collin Sexton","Herbert Jones","Christian Wood","Deni Avdija","Kevin Huerter","Coby White","Dennis Schröder","Malik Monk","Tari Eason","Mike Conley","Jaden Ivey","Jeremy Sochan"],
 ["Miles Bridges","Alex Caruso","Paul Reed","Kyle Anderson","Jarace Walker","Duncan Robinson","Bojan Bogdanović","Julian Strawther","Naz Reid","Ayo Dosunmu","Bobby Portis","Bogdan Bogdanović"],
]

# 24-25/23-24 have explicit team-per-pick in the source; encoded here via
# snake over the round-1 order, which the source confirms round by round.
out = {}
for season, order, rounds in (("2025-26", S2526_ORDER, S2526),
                              ("2024-25", S2425_ORDER, S2425),
                              ("2023-24", S2324_ORDER, S2324)):
    picks = []
    n = 0
    for r, names in enumerate(rounds):
        seq = order if r % 2 == 0 else order[::-1]
        for k, nm in enumerate(names):
            n += 1
            picks.append({"pick": n, "player": nm, "team": seq[k], "manager": MGR[seq[k]]})
    assert len(picks) == 156
    out[season] = picks
json.dump(out, open("arena/draft_boards.json", "w"), indent=1, ensure_ascii=False)
print("arena/draft_boards.json written:", {k: len(v) for k, v in out.items()})
