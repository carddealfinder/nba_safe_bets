import pandas as pd


def rank_safe_bets(df):
    # Example naive ranking — replace with your real logic later
    df["confidence"] = df.mean(axis=1, numeric_only=True)
    df = df.sort_values("confidence", ascending=False)
    return df.head(25)
