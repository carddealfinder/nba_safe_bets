import pandas as pd


def add_context_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add opponent strength, injury adjustments, pace, etc."""
    if df.empty:
        return df

    df["is_home"] = df["team"] == df["team"]  # placeholder
    df["injury_factor"] = df["injury_status"].notna().astype(int)

    return df
