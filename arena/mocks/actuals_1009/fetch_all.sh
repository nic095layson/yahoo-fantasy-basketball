#!/bin/bash
# Fetch four seasons of per-game actuals from two outlets into the untrusted dir; write a manifest (url, utc time, http code, bytes, sha256).
DL="${1:?usage: fetch_all.sh DL_DIR (a fresh, empty directory for the untrusted pages)}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
M=$DL/manifest.tsv; : > $M
get() { # name url
  local out=$DL/$1; local code; code=$(curl -sS -L -m 90 -A "$UA" "$2" -o "$out" -w "%{http_code}" 2>/dev/null)
  if [ "$code" = "429" ] || [ "$code" = "000" ]; then sleep 20; code=$(curl -sS -L -m 90 -A "$UA" "$2" -o "$out" -w "%{http_code}" 2>/dev/null); fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$(date -u +%FT%TZ)" "$code" "$(stat -c %s "$out" 2>/dev/null)" "$(sha256sum "$out" | cut -c1-64)" >> $M
  echo "$1 $code $(stat -c %s "$out")"
}
for y in 2023 2024 2025 2026; do
  get bref_$y.html "https://www.basketball-reference.com/leagues/NBA_${y}_per_game.html"; sleep 4
done
for y in 2023 2024 2025 2026; do
  for p in $(seq 1 12); do
    get espn_${y}_p$p.json "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/statistics/byathlete?region=us&lang=en&contentorigin=espn&isqualified=false&limit=50&page=$p&season=$y&seasontype=2&sort=offensive.avgPoints:desc"
    sleep 0.5
  done
done
echo "== fetch done $(date -u +%T)"
