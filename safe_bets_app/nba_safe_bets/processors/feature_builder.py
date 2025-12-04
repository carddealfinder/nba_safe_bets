import pandas as pd
import numpy as np

def add_rolling_features(df):
    """
    Adds rolling means and rolling standard deviations for
    points, rebounds, assists, 3PM, and minutes.
    """

    df = df.sort_values(["PLAYER_ID", "GAME_DATE"])

    # Rolling averages (last 10)
    df["PTS_last10"] = df.groupby("PLAYER_ID")["PTS"].transform(lambda x: x.rolling(10, min_periods=3).mean())
    df["REB_last10"] = df.groupby("PLAYER_ID")["REB"].transform(lambda x: x.rolling(10, min_periods=3).mean())
    df["AST_last10"] = df.groupby("PLAYER_ID")["AST"].transform(lambda x: x.rolling(10, min_periods=3).mean())
    df["FG3M_last10"] = df.groupby("PLAYER_ID")["FG3M"].transform(lambda x: x.rolling(10, min_periods=3).mean())

    # Rolling averages (last 20)
    df["PTS_last20"] = df.groupby("PLAYER_ID")["PTS"].transform(lambda x: x.rolling(20, min_periods=5).mean())
    df["REB_last20"] = df.groupby("PLAYER_ID")["REB"].transform(lambda x: x.rolling(20, min_periods=5).mean())
    df["AST_last20"] = df.groupby("PLAYER_ID")["AST"].transform(lambda x: x.rolling(20, min_periods=5).mean())
    df["FG3M_last20"] = df.groupby("PLAYER_ID")["FG3M"].transform(lambda x: x.rolling(20, min_periods=5).mean())

    # Rolling standard deviation (consistency)
    df["PTS_std"] = df.groupby("PLAYER_ID")["PTS"].transform(lambda x: x.rolling(10, min_periods=3).std())
    df["REB_std"] = df.groupby("PLAYER_ID")["REB"].transform(lambda x: x.rolling(10, min_periods=3).std())
    df["AST_std"] = df.groupby("PLAYER_ID")["AST"].transform(lambda x: x.rolling(10, min_periods=3).std())
    df["FG3M_std"] = df.groupby("PLAYER_ID")["FG3M"].transform(lambda x: x.rolling(10, min_periods=3).std())

    # Minutes stability
    df["MIN_last10"] = df.groupby("PLAYER_ID")["MINUTES"].transform(lambda x: x.rolling(10, min_periods=3).mean())
    df["MIN_std"] = df.groupby("PLAYER_ID")["MINUTES"].transform(lambda x: x.rolling(10, min_periods=3).std())

    return df
