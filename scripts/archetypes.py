"""Archetype classification — codified 2026-07-30 (gap study G3, council-ratified).

Pinned constants from the verified study (PCA of the 9x9 z-correlation
matrix over the 241 draftable players; all thresholds are pool quantiles
of the measured projections). Deterministic, display-only consumers:
build_deck.py bakes the outputs into the deck's PLAYERS rows (`ar`
archetype code, `fx` out-of-position flags, `sy` style coordinate).
Classification is PROFILE, not position (Wembanyama and Jokic classify
ALPHA — their guard-side production is why they are picks 1-2).

Re-derive the constants only alongside a z-model change (P3-class) or a
September data refresh: scratchpad g3_axes.py / g3_classify.py are the
generators; gauntlet-verified counts 61 BIG / 21 ALPHA / 36 GEN /
19 3D / 104 Balanced.
"""

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]

# PC1 "style" (big + / guard -), PC2 "usage" — 42.3% / 26.6% of variance
STYLE_PC1 = {"FG%": 0.364, "FT%": -0.362, "3PTM": -0.431, "PTS": -0.316,
             "REB": 0.274, "AST": -0.373, "ST": -0.227, "BLK": 0.284,
             "TO": 0.323}
USAGE_PC2 = {"FG%": 0.323, "FT%": -0.155, "3PTM": -0.093, "PTS": 0.417,
             "REB": 0.486, "AST": 0.324, "ST": 0.219, "BLK": 0.336,
             "TO": -0.432}

T = {  # pool-quantile thresholds (draftable pool, 2026-07-30)
    "style_big": 0.6005, "style_big_lean": 0.1896,
    "style_guard": -0.3701, "style_guard_lean": -0.2376,
    "usage_alpha": 1.0024, "usage_low": 0.1055,
    "to_heavy": -0.3914, "to_median": 0.445,
    "ast_elite": 0.3702, "tpm_med": -0.0803, "tpm_elite": 0.4331,
    "st_60": -0.2647, "blk_60": -0.2816,
    "stocks_elite": 0.0585, "ft_elite": 0.2733, "to_glue": 0.5844,
}

BIG_POS = {"C", "PF"}
GUARD_POS = {"PG", "SG"}


_COLSTATS = None  # (mu, sd) per cat over the draftable pool, set by prime()


def prime(players, availability):
    """Compute per-cat column stats over the av>0 pool. The study's PCA
    projections run on STANDARDIZED z columns (correlation-matrix PCA);
    projecting raw z inflates the heavy-tailed cats (BLK skew +2.4) and
    misclassifies ~40 players — verified against the study counts."""
    global _COLSTATS
    av = [p for p in players if availability(p) > 0]
    n = len(av)
    stats = {}
    for c in CATS:
        vals = [p["z"][c] for p in av]
        m = sum(vals) / n
        var = sum((v - m) ** 2 for v in vals) / n
        stats[c] = (m, var ** 0.5 or 1.0)
    _COLSTATS = stats


_EIG_SD = {"style": 3.811 ** 0.5, "usage": 2.393 ** 0.5}  # unit-variance PC scores


def _proj(z, loadings, eig_key):
    raw = sum(loadings[c] * (z[c] - _COLSTATS[c][0]) / _COLSTATS[c][1]
              for c in CATS)
    return raw / _EIG_SD[eig_key]


def classify(p):
    """(archetype_code, flags, style) for one hoops player row (post-zscores).

    Style/usage project standardized columns (call prime() first); flag
    thresholds compare RAW z (the study's honor-roll values are raw z).
    """
    if _COLSTATS is None:
        raise RuntimeError("archetypes.prime(players, availability) not called")
    z = p["z"]
    style = _proj(z, STYLE_PC1, "style")
    usage = _proj(z, USAGE_PC2, "usage")

    # first-match-wins (order is part of the codified spec)
    if style >= T["style_big"]:
        ar = "BIG"
    elif usage >= T["usage_alpha"] and z["TO"] <= T["to_heavy"]:
        ar = "ALPHA"
    elif style <= T["style_guard"] and z["AST"] >= T["ast_elite"]:
        ar = "GEN"
    elif (z["3PTM"] >= T["tpm_med"] and
          (z["ST"] >= T["st_60"] or z["BLK"] >= T["blk_60"]) and
          usage <= T["usage_low"] and z["TO"] >= T["to_median"]):
        ar = "3D"
    else:
        ar = ""  # Balanced renders nothing

    primary = (p["pos"].replace('"', "").split(",")[0].strip() or "").upper()
    fx = []
    if primary in BIG_POS and z["AST"] >= T["ast_elite"]:
        fx.append("AST-from-big")
    if primary in GUARD_POS and (z["ST"] + z["BLK"]) / 2 >= T["stocks_elite"]:
        fx.append("stocks-from-guard")
    if primary in BIG_POS and z["3PTM"] >= T["tpm_elite"]:
        fx.append("3s-from-big")
    if primary in BIG_POS and z["FT%"] >= T["ft_elite"]:
        fx.append("FT-from-big")
    tv = sum(z[c] for c in CATS)
    if tv > 0 and z["TO"] >= T["to_glue"]:
        fx.append("low-TO-glue")
    return ar, fx, round(style, 2)
