import numpy as np
import pandas as pd

def compute_weighted_probabilities(df):
    """
    Adds weighted statistical baseline probabilities for
    PTS/REB/AST/3PM props.
    """

    # Base weighted model: 50% last10, 30% last20, 20% season avg
    def weighted(a10, a20, season):
        return (0.5 * a10) + (0.3 * a20) + (0.2 * season)

    # Points
    df["prob_pts"] = weighted(df["PTS_last10"], df["PTS_last20"], df["PTS"])

    # Rebounds
    df["prob_reb"] = weighted(df["REB_last10"], df["REB_last20"], df["REB"])

    # Assists
    df["prob_ast"] = weighted(df["AST_last10"], df["AST_last20"], df["AST"])

    # 3PM
    df["prob_3pm"] = weighted(df["FG3M_last10"], df["FG3M_last20"], df["FG3M"])

    # Normalize to 0–1 range
    df["prob_pts"] = df["prob_pts"] / df["prob_pts"].max()
    df["prob_reb"] = df["prob_reb"] / df["prob_reb"].max()
    df["prob_ast"] = df["prob_ast"] / df["prob_ast"].max()
    df["prob_3pm"] = df["prob_3pm"] / df["prob_3pm"].max()

    return df
