import pandas as pd
from .context_features import add_context_features


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct numerical feature matrix used by the model.
    Adds contextual features first, then selects numeric columns only.
    """

    if df is None or df.empty:
        return pd.DataFrame()

    # Add contextual derived features (injuries, home/away, etc.)
    df = add_context_features(df)

    # Select only numeric columns for model input
    num_df = df.select_dtypes(include=["number"]).copy()

    # Fill missing values
    num_df = num_df.fillna(0)

    return num_df
