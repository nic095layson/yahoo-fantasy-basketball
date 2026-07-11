# 🏀 Yahoo Fantasy Basketball for Claude Code

A Claude Code-native fantasy basketball assistant. One stdlib-only Python CLI
(`scripts/yfb.py`) talks to the Yahoo Fantasy Sports API; one Claude Code skill
(`.claude/skills/fantasy-basketball/`) teaches Claude when and how to drive it.
Ask Claude "who should I start this week?" and it fetches your real roster and
matchup, then gives a committed recommendation.

## Synopsis

**The problem.** Fantasy basketball decisions (start/sit, waivers, punt
strategy) need live league data plus judgment. Yahoo's API has both OAuth2
friction and a notoriously nested JSON format; no one wants to hand-roll that
per question.

**The system.** Three layers:

1. **Data layer — `scripts/yfb.py`.** Single-file, stdlib-only Python. Handles
   the OAuth2 authorization-code flow (code copied from the redirect URL), token
   caching + auto-refresh (`~/.config/yfb/token.json`, chmod 600), and
   flattening Yahoo's fragment-list JSON into plain tables or `--json` output.
   Subcommands: `auth`, `status`, `leagues`, `standings`, `roster`, `matchup`,
   `free-agents`. A `--demo` flag runs every command on bundled sample data —
   no credentials, no network.
2. **Skill layer — `.claude/skills/fantasy-basketball/SKILL.md`.** The trigger
   contract ("my roster", "waiver wire", "who should I start"…) plus the
   playbook: resolve league/team keys once, fetch before analyzing, respect
   H2H-vs-roto format, flag injury statuses, commit to recommendations.
3. **Judgment layer — Claude.** The API gives facts; Claude adds the analysis
   the numbers don't: category math for your specific matchup, pickup targets
   that fit your build, punt-strategy fit.

**Security posture.** Read-scope Yahoo app; secrets live in env vars or
gitignored files; tokens are never printed or committed.

## Quick start

```bash
# No credentials? See it work immediately:
python3 scripts/yfb.py --demo leagues
python3 scripts/yfb.py --demo roster
python3 scripts/yfb.py --demo matchup
python3 scripts/yfb.py --demo free-agents

# Live setup (once):
# 1. Create an app at https://developer.yahoo.com/apps/  (Fantasy Sports, read)
export YAHOO_CLIENT_ID=...
export YAHOO_CLIENT_SECRET=...
python3 scripts/yfb.py auth          # open URL, approve, paste redirect URL back
python3 scripts/yfb.py leagues       # your real leagues
```

Then in Claude Code, just ask: *"Check my matchup — which categories am I
losing and who on the wire fixes them?"*

## Repo layout

```
yahoo-fantasy-basketball/
├── README.md
├── scripts/
│   └── yfb.py                       # stdlib-only Yahoo API CLI
├── .claude/skills/fantasy-basketball/
│   └── SKILL.md                     # trigger + playbook for Claude Code
├── evals/
│   └── evals.json                   # test prompts for the skill
└── .gitignore                       # keeps credentials/tokens out of git
```

## Install the skill globally (optional)

To use the skill from any directory, copy it to your personal skills folder:

```bash
cp -r .claude/skills/fantasy-basketball ~/.claude/skills/
```

(When working inside this project folder, Claude Code discovers it
automatically.)

## Notes

- NBA game code `nba` resolves to the current season automatically.
- The matchup command scores 9-cat H2H with turnovers correctly inverted.
- Yahoo API reference: https://developer.yahoo.com/fantasysports/guide/
