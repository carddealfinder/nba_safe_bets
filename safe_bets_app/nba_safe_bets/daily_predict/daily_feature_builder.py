import pandas as pd


def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    df = players_df.copy()

    # --- LEFT MERGES ON player_id ---
    if not schedule_df.empty:
        df = df.merge(schedule_df, on="player_id", how="left")

    if not injury_df.empty:
        df = df.merge(injury_df, on="player_id", how="left")

    if not defense_df.empty:
        df = df.merge(defense_df, on="team", how="left")

    if not dk_df.empty:
        df = df.merge(dk_df, on="player_id", how="left")

    # Fill missing columns
    df.fillna(0, inplace=True)

    # Final feature columns
    df["injury_factor"] = (df["injury_status"] != 0).astype(int)

    return df
