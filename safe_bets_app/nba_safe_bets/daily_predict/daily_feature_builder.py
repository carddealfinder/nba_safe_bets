import pandas as pd
import numpy as np

"""
This module builds a simple feature set for every player.
Later you can replace synthetic stats with real API game logs.
"""


def build_features_for_player(player_row, defense_rankings, injuries, schedule):
    """
    Given a player, return a row of features the model can use.

    player_row = row from the players DataFrame

    Returns synthetic but realistic stats so the prediction engine
    can run end-to-end without errors.
    """

    player_id = player_row["PLAYER_ID"]
    team = player_row["team"]
    team_name = None

    if isinstance(team, dict):
        team_name = team.get("full_name")
    else:
        team_name = None

    # --- Synthetic baseline inputs ---
    features = {
        "PLAYER_ID": player_id,
        "team_name": team_name,
        "recent_points_avg": np.random.uniform(8, 28),
        "recent_rebounds_avg": np.random.uniform(2, 12),
        "recent_assists_avg": np.random.uniform(1, 9),
        "recent_threes_avg": np.random.uniform(0, 4),
    }

    # --- Add defense ranking if available ---
    if defense_rankings and "points" in defense_rankings:
        features["opp_def_points"] = np.random.uniform(102, 118)
    else:
        features["opp_def_points"] = 110.0

    # --- Injury flag ---
    injured = injuries[injuries["player_id"] == player_id]
    features["is_injured"] = 1 if len(injured) > 0 else 0

    # --- Game availability ---
    features["has_game_today"] = 1 if not schedule.empty else 0

    return pd.DataFrame([features])

