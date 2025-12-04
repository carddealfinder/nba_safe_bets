import pandas as pd

from nba_safe_bets.processors.context_features import (
    compute_defense_rankings,
    compute_pace_rating,
    estimate_possessions,
    estimate_usage_boost
)

# ================================================================
# SHAP-Lite Explanation Function
# ================================================================
def explain_bet(row):
    """
    Returns a dictionary with contribution weights for:
    - cover_prob
    - matchup_score
    - pace
    - usage_boost
    """

    factors = {
        "cover_prob": row.get("cover_prob", 0),
        "matchup_score": row.get("matchup_score", 0),
        "pace": row.get("pace", 0) or 0,
        "usage_boost": row.get("usage_boost", 0)
    }

    # Normalize to 0–1 scale (avoid divide by zero)
    max_val = max(factors.values()) or 1

    explanation = {
        key: round(val / max_val, 3)
        for key, val in factors.items()
    }

    return explanation


# ================================================================
# MAIN RANKING MODULE
# ================================================================
def rank_bets(
    stats_df,
    defense_df,
    pace_df,
    injuries_df
):
    """
    stats_df columns required:
        player, player_id, team, opponent, stat, line, cover_prob

    Enriches with matchup metrics + final score + SHAP-lite explanation.
    """

    if stats_df is None or stats_df.empty:
        return pd.DataFrame()

    # ----------------------------------------------------------
    # Defense Rank Tables
    # ----------------------------------------------------------
    defense_ranks = compute_defense_rankings(defense_df)

    ranked_rows = []

    for _, row in stats_df.iterrows():
        team = row["team"]
        opp = row["opponent"]
        stat = row["stat"]

        # ---------------------------
        # DEFENSE RANK
        # ---------------------------
        def_rank = None
        if defense_ranks.get(stat) is not None:
            dr = defense_ranks[stat]
            m = dr[dr["team"] == opp]
            if not m.empty:
                def_rank = int(m.iloc[0]["rank"])

        # ---------------------------
        # PACE / POSSESSIONS
        # ---------------------------
        pace_team = compute_pace_rating(pace_df, team)
        pace_opp = compute_pace_rating(pace_df, opp)
        possessions = estimate_possessions(pace_team, pace_opp)

        # ---------------------------
        # USAGE BOOST
        # ---------------------------
        usage_boost = estimate_usage_boost(injuries_df, team)

        ranked_rows.append({
            **row,
            "def_rank": def_rank,
            "pace": possessions,
            "usage_boost": usage_boost
        })

    out = pd.DataFrame(ranked_rows)

    # ----------------------------------------------------------
    # Matchup Score Calculation
    # ----------------------------------------------------------
    def matchup_score(r):
        score = 0.0

        # Defense rank → tougher defenses penalize score
        if r["def_rank"] is not None:
            score += (31 - r["def_rank"]) / 30 * 30   # max 30 points

        # Pace score → values usually 90–110 mapped to 0–20
        if r["pace"] is not None:
            score += min(r["pace"] / 120, 1) * 20

        # Usage boost → max +10
        score += r["usage_boost"] * 10

        return round(score, 3)

    out["matchup_score"] = out.apply(matchup_score, axis=1)

    # ----------------------------------------------------------
    # Final score weighting
    # ----------------------------------------------------------
    out["final_score"] = (
        out["cover_prob"] * 0.60 +
        out["matchup_score"] / 100 * 0.30 +
        out["usage_boost"] * 0.10
    )

    out = out.sort_values("final_score", ascending=False).reset_index(drop=True)

    # ----------------------------------------------------------
    # SHAP-Lite Explanation
    # ----------------------------------------------------------
    out["explain_factors"] = out.apply(lambda r: explain_bet(r), axis=1)

    return out
