import pandas as pd


def get_defense_rankings():
    # Fallback: minimal structure
    return pd.DataFrame({
        "team": [],
        "def_rating": []
    })
