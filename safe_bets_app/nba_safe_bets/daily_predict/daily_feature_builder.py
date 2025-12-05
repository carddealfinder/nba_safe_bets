import pandas as pd


def build_daily_features(players_df, schedule_df, injury_df, defense_df, odds_df):
    """
    Merge all the scraped datasets and calculate injury_factor.
    """

    df = players_df.copy()

    # --------------------------
    # Merge schedule
    # --------------------------
    if not schedule_df.empty:
        df = df.merge(schedule_df, on="team", how="left")

    # --------------------------
    # Merge injuries
    # --------------------------
    if "injury_status" not in injury_df.columns:
        injury_df["injury_status"] = None

    df = df.merge(injury_df[["player_id", "injury_status"]], left_on="id", right_on="player_id", how="left")

    df.drop(columns=["player_id"], errors="ignore", inplace=True)

    # Injury factor: 1 = injured, 0 = healthy
    df["injury_factor"] = df["injury_status"].notna().astype(int)

    # --------------------------
    # Merge defense rankings (by opponent team)
    # --------------------------
    if not defense_df.empty:
        df = df.merge(defense_df, left_on="opponent", right_on="team", how="left", suffixes=("", "_def"))

    # --------------------------
    # Merge DraftKings odds
    # --------------------------
    if not odds_df.empty:
        df = df.merge(odds_df, on="id", how="left")

    # --------------------------
    # Fill NaNs
    # --------------------------
    df.fillna(0, inplace=True)

    return df
