import pandas as pd

def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    df = players_df.copy()

    # ---- ALWAYS ENSURE injury_status COLUMN EXISTS ----
    # If injury_df is empty, create a blank one with zeros
    if injury_df is None or injury_df.empty:
        injury_df = pd.DataFrame({
            "player_id": df["player_id"],
            "injury_status": 0
        })

    # ---- MERGES USING player_id ----
    if not schedule_df.empty:
        df = df.merge(schedule_df, on="player_id", how="left")

    df = df.merge(injury_df, on="player_id", how="left")  # <-- always safe now

    if not defense_df.empty:
        df = df.merge(defense_df, on="team", how="left")

    if not dk_df.empty:
        df = df.merge(dk_df, on="player_id", how="left")

    # ---- FILL MISSING VALUES ----
    df.fillna(0, inplace=True)

    # ---- INJURY FACTOR FEATURE ----
    df["injury_factor"] = (df["injury_status"] != 0).astype(int)

    return df
