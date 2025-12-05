import pandas as pd


def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    """
    Combines all scraper sources into a unified feature dataframe.
    Ensures missing data does NOT break the system.
    """

    print("[FEATURE BUILDER] Building merged feature set...")

    # ------------------------
    # 1. Base player table
    # ------------------------
    df = players_df.copy()

    # Guarantee baseline required columns
    df["injury_status"] = "ACTIVE"
    df["injury_factor"] = 0.0
    df["game_id"] = None

    # ------------------------
    # 2. Injury merge
    # ------------------------
    if not injury_df.empty:
        injury_df = injury_df.rename(columns={"player_id": "id"})
        df = df.merge(injury_df, on="id", how="left")

        # Injury normalization
        df["injury_status"] = df["injury_status_y"].fillna("ACTIVE")
        df["injury_factor"] = df["injury_factor"].fillna(0)

        df.drop(columns=["injury_status_x", "injury_status_y"], errors="ignore", inplace=True)
    else:
        print("[FEATURE BUILDER] Injury report empty → Using default injury_factor=0")

    # ------------------------
    # 3. Schedule merge
    # ------------------------
    if not schedule_df.empty:
        df = df.merge(schedule_df, on="team", how="left")
        df["game_id"] = df["game_id"].fillna(0)
    else:
        print("[FEATURE BUILDER] Schedule empty → setting all game_id=0")
        df["game_id"] = 0

    # ------------------------
    # 4. Defense merge
    # ------------------------
    if not defense_df.empty:
        df = df.merge(defense_df, on="team", how="left")
    else:
        print("[FEATURE BUILDER] Defense rankings empty → filling with league-average values")
        df["def_rating"] = 110.0

    # ------------------------
    # 5. Odds merge
    # ------------------------
    if not dk_df.empty:
        df = df.merge(dk_df, left_on="id", right_on="player_id", how="left")
    else:
        print("[FEATURE BUILDER] No DraftKings odds → skipping odds merge")

    # ------------------------
    # 6. Fill missing columns
    # ------------------------
    required_stats = ["points", "rebounds", "assists", "threes"]
    for col in required_stats:
        if col not in df.columns:
            df[col] = 0.0

    # Cleanup
    df.fillna(0, inplace=True)

    print(f"[FEATURE BUILDER] Final merged shape: {df.shape}")
    return df
