import pandas as pd

# ----------------------------------------------------------------------
# Team Defense Ranking Extractor
# ----------------------------------------------------------------------
def compute_defense_rankings(def_stats_df):
    """
    Accepts a DataFrame of team defensive stats from Balldontlie-like structure:
    Columns expected: team, opp_pts, opp_ast, opp_reb, opp_fg3m
    Returns rank tables for each category.
    """
    if def_stats_df is None or def_stats_df.empty:
        return {
            "points": None,
            "assists": None,
            "rebounds": None,
            "threes": None
        }

    ranks = {}

    ranks["points"]   = def_stats_df.sort_values("opp_pts").reset_index(drop=True)
    ranks["assists"]  = def_stats_df.sort_values("opp_ast").reset_index(drop=True)
    ranks["rebounds"] = def_stats_df.sort_values("opp_reb").reset_index(drop=True)
    ranks["threes"]   = def_stats_df.sort_values("opp_fg3m").reset_index(drop=True)

    # Add rank number
    for key, df in ranks.items():
        df["rank"] = df.index + 1

    return ranks


# ----------------------------------------------------------------------
# Game Pace Rating
# ----------------------------------------------------------------------
def compute_pace_rating(team_pace_df, team_name):
    """
    Returns the pace score (possessions per game) for a team.
    """
    if team_pace_df is None or team_pace_df.empty:
        return None

    row = team_pace_df[team_pace_df["team"] == team_name]
    if row.empty:
        return None

    return float(row.iloc[0]["pace"])


# ----------------------------------------------------------------------
# Projected Possessions (simple possession formula)
# ----------------------------------------------------------------------
def estimate_possessions(team1_pace, team2_pace):
    """
    Simple average pace model.
    """
    if team1_pace is None or team2_pace is None:
        return None

    return round((team1_pace + team2_pace) / 2, 1)


# ----------------------------------------------------------------------
# Usage Boost Estimator
# ----------------------------------------------------------------------
def estimate_usage_boost(injury_df, player_team):
    """
    Rough heuristic:
    If multiple starters on the player's team are OUT,
    usage goes up slightly.
    """
    if injury_df is None or injury_df.empty:
        return 0.0

    injured = injury_df[(injury_df["team"] == player_team) & (injury_df["status"] == "Out")]

    if injured.empty:
        return 0.0

    count = len(injured)

    # Basic rule-of-thumb scaling
    boost = min(0.02 * count, 0.10)  # Max +10% usage

    return round(boost, 3)
