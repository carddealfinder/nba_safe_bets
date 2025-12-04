import pandas as pd

SUPPORTED_STATS = [
    "points",
    "rebounds",
    "assists",
    "threes",
    "points_rebounds",
    "points_assists",
    "rebounds_assists",
    "pra"
]


def build_features(player_row, matchup, injuries):
    """
    Build the feature vector for models.
    This is intentionally simple — you can add more features later.
    """

    features = {
        "player_id": player_row.get("player_id", None),
        "opponent_def_rating": matchup.get("def_rating", 0),
        "minutes_last_5": player_row.get("minutes_5", 0),
        "usage_rate": player_row.get("usage", 0),
        "injury_flag": injuries.get(player_row.get("player_id"), 0)
    }

    return pd.DataFrame([features])


def attach_stat_line(df_props):
    """
    For DK props, only keep stats we support.
    """
    return df_props[df_props["stat"].isin(SUPPORTED_STATS)].reset_index(drop=True)
