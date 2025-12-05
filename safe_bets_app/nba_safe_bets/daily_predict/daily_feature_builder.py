import pandas as pd


def normalize_schedule(schedule_df):
    """
    Converts schedules into a safe, uniform format:
    team | game_id
    """
    if schedule_df.empty:
        print("[SCHEDULE] No schedule available → using empty normalized schedule")
        return pd.DataFrame(columns=["team", "game_id"])

    # Handle cases where schedule scraper returns home/away fields
    if "home_team" in schedule_df.columns and "away_team" in schedule_df.columns:
        print("[SCHEDULE] Normalizing schedule dataframe (home/away → team rows)")

        home = schedule_df[["home_team", "game_id"]].rename(columns={"home_team": "team"})
        away = schedule_df[["away_team", "game_id"]].rename(columns={"away_team": "team"})

        normalized = pd.concat([home, away], ignore_index=True)
        return normalized

    # Already in correct format?
    if "team" in schedule_df.columns and "game_id" in schedule_df.columns:
        return schedule_df[["team", "game_id"]]

    print("[SCHEDULE WARNING] Unexpected schedule format → skipping")
    return pd.DataFrame(columns=["team", "game_id"])



def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    """
    Combines all scraper sources into a unified feature dataframe.
    Ensures missing data does NOT break the system.
    """

    print("[FEATURE BUILDER] Building merged feature set...")

    df = players_df.copy()

    # Guarantee required columns
    df["injury_status"] = "ACTIVE"
    df["injury_factor"] = 0.0
    df["game_id"] = 0

    # -------------------------
    # 1. Injury merge
    # -------------------------
    if not injury_df.empty:
        injury_df = injury_df.rename(columns={"player_id": "id"})
        df = df.merge(injury_df, on="id", how="left")

        df["injury_status"] = df["injury_status_y"].fillna("ACTIVE")
        df["injury_factor"] = df["injury_factor"].fillna(0)

        df.drop(columns=["injury_status_x", "injury_status_y"], errors="ignore", inplace=True)
    else:
        print("[FEATURE BUILDER] No injury report → defaulting to healthy")

    # -------------------------
    # 2. Schedule merge
    # -------------------------
    normalized_sched = normalize_schedule(schedule_df)

    if not normalized_sched.empty:
        df = df.merge(normalized_sched, on="team", how="left")
        df["game_id"] = df["game_id"].fillna(0)
    else:
        print("[FEATURE BUILDER] Schedule empty → all game_id=0")

    # -------------------------
    # 3. Defense merge
    # -------------------------
    if not defense_df.empty:
        df = df.merge(defense_df, on="team", how="left")
    else:
        print("[FEATURE BUILDER] No defense data → filling default rating")
        df["def_rating"] = 110.0

    # -------------------------
    # 4. Odds merge
    # -------------------------
    if not dk_df.empty:
        df = df.merge(dk_df, left_on="id", right_on="player_id", how="left")
    else:
        print("[FEATURE BUILDER] No odds available → skipping DK merge")

    # -------------------------
    # 5. Required stat columns
    # -------------------------
    required_stats = ["points", "rebounds", "assists", "threes"]
    for col in required_stats:
        if col not in df.columns:
            df[col] = 0.0

    df.fillna(0, inplace=True)

    print(f"[FEATURE BUILDER] Final merged shape: {df.shape}")
    return df
