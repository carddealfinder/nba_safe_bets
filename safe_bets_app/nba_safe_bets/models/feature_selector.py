import pandas as pd

FEATURE_COLUMNS = [
    # Rolling averages
    "PTS_last10", "REB_last10", "AST_last10", "FG3M_last10",
    "PTS_last20", "REB_last20", "AST_last20", "FG3M_last20",

    # Consistency
    "PTS_std", "REB_std", "AST_std", "FG3M_std",

    # Minutes
    "MIN_last10", "MIN_std",

    # Weighted baseline probabilities
    "prob_pts", "prob_reb", "prob_ast", "prob_3pm",

    # Context Features
    "B2B", "days_rest",
    "INJURED_COUNT",
    
    "HOME", "AWAY",

    # Defensive matchup
    "DEF_VS_POINTS",
    "DEF_VS_REBOUNDS",
    "DEF_VS_ASSISTS",
    "DEF_VS_THREES",

    # Vegas (optional)
    "SPREAD",
    "TOTAL",
]

def select_features(df):
    """
    Returns only columns used for ML training/prediction.
    """
    cols = [c for c in FEATURE_COLUMNS if c in df.columns]
    return df[cols].fillna(0)
