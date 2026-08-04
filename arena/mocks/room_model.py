"""Room model from the REAL 2025-26 draft board vs the arena's frozen
October 2025 snapshot: per-manager reach index (pick number minus 9-cat
value rank). Positive mean = drafts below value (points/name/upside bias);
near zero = value-anchored."""
import sys, os, unicodedata

os.chdir("/home/user/yahoo-fantasy-basketball")
sys.path = [os.path.abspath("scripts")] + sys.path
import hoops
hoops.DATA_PATH = os.path.abspath("arena/data/players_2025-10-21.csv")
players = hoops.zscores(hoops.load_players())
avail = [p for p in players if hoops.availability(p) > 0]
by_adj = sorted(avail, key=lambda p: -hoops.adj_value(p))
vrank = {p["player"]: i + 1 for i, p in enumerate(by_adj)}


def norm(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode()
    n = n.replace(".", "").replace("'", "").lower()
    for suf in (" jr", " iii", " ii", " iv"):
        if n.endswith(suf):
            n = n[: -len(suf)]
    return " ".join(n.split())


vnorm = {norm(k): v for k, v in vrank.items()}

# (pick, player, team) from the owner-provided 2025-26 board, snake slot order:
ORDER1 = ["Not hurt just SARR", "Wing Chun Wemby", "HalleLuka Amen", "JAMAL AL-QUETA",
          "The Konclave", "ur my only hope Anti-wan", "Itsy Bitsy Spida",
          "All guards no defense", "John's Cool Team", "Devin Minutes in Heaven",
          "IM SO HORT", "Gotta Be Bamonte"]
ROUNDS = [
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
picks = []  # (overall, player, team)
n = 0
for r, names in enumerate(ROUNDS):
    order = ORDER1 if r % 2 == 0 else ORDER1[::-1]
    for k, name in enumerate(names):
        n += 1
        picks.append((n, name, order[k]))

teams = {}
unmatched = []
for pn, name, team in picks:
    v = vnorm.get(norm(name))
    if v is None:
        unmatched.append((pn, name, team))
        continue
    teams.setdefault(team, []).append((pn, name, v, pn - v))

print(f"matched {sum(len(v) for v in teams.values())}/156 picks against the frozen Oct-2025 pool; unmatched {len(unmatched)}")
for pn, name, team in unmatched:
    print(f"   unmatched: #{pn:3} {name} ({team})")
print(f"\n{'team':<26} {'n':>3} {'mean reach':>10} {'early(R1-6) reach':>18}  read")
rows = []
for t, ps in teams.items():
    mean = sum(d for *_, d in ps) / len(ps)
    early = [d for pn, _, _, d in ps if pn <= 72]
    me = sum(early) / len(early) if early else 0
    rows.append((t, len(ps), mean, me))
for t, k, mean, me in sorted(rows, key=lambda r: -r[2]):
    # reach = pick - value_rank: POSITIVE = beats value (takes fallers), NEGATIVE = reaches past it
    read = "value-anchored" if abs(me) <= 6 else ("beats value (takes fallers)" if me > 0 else "reaches past value (name/points/rookie hype)")
    own = "  <== OWNER" if "JAMAL" in t else ""
    print(f"{t:<26} {k:>3} {mean:>+10.1f} {me:>+18.1f}  {read}{own}")
