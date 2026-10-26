"""One hand-set constant moved at a time, for the kit's assumption sweep (kit scripts/redteam/sweep.py) and the season
simulator (arena/mocks/league_sim.py --patch). One module so the two cannot drift (kit owner 2026-10-26, "build the
real-schedule re-measurement"); the four kinds are the sweep's, moved here verbatim:

  const  {NAME: value}   set arena.NAME (an unknown name is an error)
  avail  [healthy, risk] the weekly availability tiers 0.88 and 0.75 replaced
  cv     factor          every category of arena.SEASON_CV scaled
  games  value           the 3.5 games/week literal inside team_week_model replaced (no literal found is an error)

Apply to a freshly imported (or reloaded) arena module, before anything reads SEASON_CV or builds a team model."""
import inspect


def apply(arena, patch):
    for k, v in (patch.get("const") or {}).items():
        if not hasattr(arena, k):
            raise AttributeError(f"patch names arena.{k}, which the live engine does not have")
        setattr(arena, k, v)
    if "avail" in patch:
        h, r = patch["avail"]
        orig = arena.weekly_availability
        arena.weekly_availability = lambda p, h=h, r=r, orig=orig: (
            r if orig(p) == 0.75 else h if orig(p) == 0.88 else orig(p))
    if "cv" in patch:
        # the season headline's per-game variation is SEASON_CV since D-ZS-3 (arena.CV is the frozen draft engine's)
        arena.SEASON_CV = {c: v * patch["cv"] for c, v in arena.SEASON_CV.items()}
    if "games" in patch:
        # the 3.5 games/week is a literal inside team_week_model, not a module constant: re-compile the
        # function with the literal replaced, in arena's own namespace
        src = inspect.getsource(arena.team_week_model)
        g = patch["games"]
        new = src.replace("g = 3.5 * a", f"g = {g} * a").replace("g_var = 3.5 * a", f"g_var = {g} * a")
        if new == src:
            raise RuntimeError("games patch found no 3.5 literal in team_week_model")
        exec(compile(new, arena.__file__, "exec"), vars(arena))
    return arena
