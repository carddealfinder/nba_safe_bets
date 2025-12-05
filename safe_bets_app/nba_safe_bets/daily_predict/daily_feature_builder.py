import pandas as pd


def build_daily_features(players_df, schedule_df, injury_df, defense_df, odds_df):
    df = players_df.copy()

    # -----------------------------
    # Injury mapping
    # -----------------------------
    if not injury_df.empty:
        injury_map = dict(zip(injury_df["player"], injury_df["status"]))
        df["injury_status"] = df["first_name"] + " " + df["last_name"]
        df["injury_status"] = df["injury_status"].map(injury_map)
    else:
        df["injury_status"] = None

    df["injury_factor"] = df["injury_status"].notna().astype(int)

    # -----------------------------
    # Minimal fake stat features (will replace with real schedule merges)
    # -----------------------------
    df["points"] = 12
    df["rebounds"] = 5
    df["assists"] = 4
    df["threes"] = 2
    df["game_id"] = 0

    # -----------------------------
    # Fill NA safely
    # -----------------------------
    df.fillna(0, inplace=True)

    # Final columns required by ML models
    return df[
        ["id", "points", "rebounds", "assists", "threes",
         "injury_factor", "game_id", "first_name", "last_name", "team", "injury_status"]
    ]
