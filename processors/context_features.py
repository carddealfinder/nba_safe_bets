import pandas as pd
import numpy as np

def add_context_features(df, defense, injuries, vegas, schedule):
    """
    Combines all external context into the dataset.
    """

    # BACK-TO-BACK FLAG
    df = df.sort_values(["PLAYER_ID", "GAME_DATE"])
    df["prev_game_date"] = df.groupby("PLAYER_ID")["GAME_DATE"].shift(1)
    df["days_rest"] = (df["GAME_DATE"] - df["prev_game_date"]).dt.days
    df["B2B"] = (df["days_rest"] == 1).astype(int)

    # INJURY IMPACT (count injured teammates)
    inj_counts = injuries.groupby("Team").size().reset_index()
    inj_counts.columns = ["TEAM", "INJURED_COUNT"]
    df = df.merge(inj_counts, how="left", left_on="TEAM_ABBREV", right_on="TEAM")
    df["INJURED_COUNT"].fillna(0, inplace=True)

    # DEFENSE MATCHUP MERGE
    for stat in ["points", "rebounds", "assists", "threes"]:
        temp = defense[stat].copy()
        temp.rename(columns={stat: f"DEF_VS_{stat.upper()}"}, inplace=True)
        df = df.merge(temp[["Team", f"DEF_VS_{stat.upper()}"]],
                      left_on="OPPONENT_ABBREV",
                      right_on="Team",
                      how="left")

        df.drop(columns=["Team"], inplace=True, errors="ignore")

    # VEGAS SPREAD & TOTAL
    if len(vegas) > 0:
        vegas_small = vegas[["home_team", "away_team", "bookmakers"]].copy()
        df["SPREAD"] = 0
        df["TOTAL"] = 0  # default values for missing lines

    # HOME/AWAY
    df["HOME"] = (df["MATCHUP"].str.contains("vs")).astype(int)
    df["AWAY"] = (df["MATCHUP"].str.contains("@")).astype(int)

    return df
