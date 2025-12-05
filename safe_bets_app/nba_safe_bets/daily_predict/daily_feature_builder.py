import pandas as pd
from nba_safe_bets.utils.logging_config import log

def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    log("[FEATURE BUILDER] Building merged feature set...")

    df = players_df.copy()

    df = df.merge(schedule_df, on="team", how="left")

    df["injury_status"] = "HEALTHY"
    if not injury_df.empty:
        df = df.merge(injury_df, left_on="full_name", right_on="player", how="left")
        df["injury_status"].fillna("HEALTHY", inplace=True)

    df["injury_factor"] = df["injury_status"].apply(lambda x: 0.4 if x != "HEALTHY" else 1.0)

    needed_cols = ["points_avg", "rebounds_avg", "assists_avg", "threes_avg"]
    for c in needed_cols:
        df[c] = 10  # constant placeholder

    return df
