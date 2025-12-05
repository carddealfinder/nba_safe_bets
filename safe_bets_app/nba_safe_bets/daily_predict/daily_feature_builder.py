import pandas as pd

def build_daily_feature_set(players_df, schedule_df, injury_df, defense_df, dk_df):
    df = players_df.copy()

    # ----------------------------------------------------------------
    # Ensure missing fields exist
    # ----------------------------------------------------------------
    if "points" not in df: df["points"] = 0
    if "rebounds" not in df: df["rebounds"] = 0
    if "assists" not in df: df["assists"] = 0
    if "threes" not in df: df["threes"] = 0

    # ----------------------------------------------------------------
    # Injury merge
    # ----------------------------------------------------------------
    if injury_df is not None and len(injury_df) > 0:
        df = df.merge(injury_df, on="id", how="left")
    else:
        df["injury_status"] = None

    df["injury_factor"] = df["injury_status"].notna().astype(int)

    # ----------------------------------------------------------------
    # Defense merge
    # ----------------------------------------------------------------
    if defense_df is not None and len(defense_df) > 0:
        df = df.merge(defense_df, on="team", how="left")

    # ----------------------------------------------------------------
    # Odds merge
    # ----------------------------------------------------------------
    if dk_df is not None and len(dk_df) > 0:
        df = df.merge(dk_df, on="id", how="left")

    # ----------------------------------------------------------------
    # Schedule merge — ensures game_id exists
    # ----------------------------------------------------------------
    if "team" in schedule_df:
        df = df.merge(schedule_df, on="team", how="left")
    else:
        df["game_id"] = 999999

    if "game_id" not in df:
        df["game_id"] = 999999

    # ----------------------------------------------------------------
    # Final cleanup
    # ----------------------------------------------------------------
    df.fillna(0, inplace=True)
    df = df.infer_objects()

    feature_df = df[
        ["id", "points", "rebounds", "assists", "threes",
         "injury_factor", "game_id"]
    ].copy()

    return df, feature_df
