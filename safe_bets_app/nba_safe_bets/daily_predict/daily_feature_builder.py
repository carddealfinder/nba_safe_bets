import pandas as pd


def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    """
    Build the full daily feature set by merging:
      - Players
      - Schedule
      - Injuries
      - Defense rankings
      - DraftKings odds (optional)
    """

    print("🔧 [FEATURE] Building daily feature set...")

    # --------------------------------------------------------------
    # 1. Base players
    # --------------------------------------------------------------
    df = players_df.copy()

    # --------------------------------------------------------------
    # 2. Schedule (merge by team_name instead of 'team')
    # --------------------------------------------------------------
    if not schedule_df.empty:
        df = df.merge(
            schedule_df.rename(columns={"team": "team_name"}),
            on="team_name",
            how="left"
        )

    # --------------------------------------------------------------
    # 3. Injuries
    # --------------------------------------------------------------
    if not injury_df.empty:
        df = df.merge(
            injury_df.rename(columns={"player_id": "id"}),
            on="id",
            how="left"
        )
        df["injury_factor"] = df["injury_status"].notna().astype(int)
    else:
        df["injury_status"] = ""
        df["injury_factor"] = 0

    # --------------------------------------------------------------
    # 4. Defense rankings (merge by team_name)
    # --------------------------------------------------------------
    if not defense_df.empty:
        df = df.merge(
            defense_df.rename(columns={"team": "team_name"}),
            on="team_name",
            how="left"
        )
    else:
        df["defense_rank"] = 15  # neutral placeholder

    # --------------------------------------------------------------
    # 5. DraftKings Odds
    # --------------------------------------------------------------
    if not dk_df.empty:
        df = df.merge(dk_df, on="id", how="left")
    else:
        df["points_line"] = 0
        df["rebounds_line"] = 0
        df["assists_line"] = 0
        df["threes_line"] = 0

    # --------------------------------------------------------------
    # 6. Clean + standardize dtypes safely
    # --------------------------------------------------------------
    df = df.fillna(0).infer_objects(copy=False)

    # --------------------------------------------------------------
    # 7. Final: ensure required fields exist
    # --------------------------------------------------------------
    required_cols = [
        "id",
        "team_name",
        "injury_factor",
        "points_line",
        "rebounds_line",
        "assists_line",
        "threes_line"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    print(f"🔧 [FEATURE] Final feature set shape: {df.shape}")
    return df
