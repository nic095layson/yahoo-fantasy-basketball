"""Parse a Basketball-Reference per-game table (downloaded HTML, untrusted) into per-player rows.
Combined rows (2TM/3TM) come first on B-Ref, so the first row per player is the season total."""
import re, html as H
COLS = {"games":"gp","fga_per_g":"fga","fg_pct":"fg_pct","fg3_per_g":"tpm","fta_per_g":"fta","ft_pct":"ft_pct","trb_per_g":"reb","ast_per_g":"ast","stl_per_g":"stl","blk_per_g":"blk","tov_per_g":"tov","pts_per_g":"pts","team_name_abbr":"team","pos":"pos","mp_per_g":"mpg","games_started":"gs"}
def parse(path):
    t = open(path, encoding="utf-8").read()
    out = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        if 'data-stat="name_display"' not in row: continue
        cells = dict(re.findall(r'<t[dh][^>]*data-stat="([^"]+)"[^>]*>(.*?)</t[dh]>', row, re.S))
        name = H.unescape(re.sub(r"<[^>]+>", "", cells.get("name_display", ""))).strip()
        if not name or name == "Player": continue
        d = {"player": name}
        for k, v in COLS.items():
            raw = H.unescape(re.sub(r"<[^>]+>", "", cells.get(k, ""))).strip()
            if v in ("team", "pos"): d[v] = raw
            else:
                try: d[v] = float(raw) if raw else 0.0
                except ValueError: d[v] = 0.0
        if name not in out: out[name] = d
    return out
