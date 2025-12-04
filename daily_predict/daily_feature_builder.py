import pandas as pd
from processors.feature_builder import add_rolling_features
from processors.context_features import add_context_features
from processors.weighted_model import compute_weighted_probabilities
from models.feature_selector import select_features

def build_daily_features(df, defense, injuries, vegas, schedule):
    # Rolling + Standard deviations
    df = add_rolling_features(df)

    # Weighted baseline
    df = compute_weighted_probabilities(df)

    # Context (injuries, defense, Vegas, B2B)
    df = add_context_features(df, defense, injuries, vegas, schedule)

    # Select only ML-ready features
    X = select_features(df)
    return df, X
