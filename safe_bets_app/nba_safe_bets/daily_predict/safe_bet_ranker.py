import pandas as pd


def rank_safe_bets(df):
    """
    Ranks the safest bets based on prediction confidence.
    If odds are missing, fallback to predicted performance.
    """

    print("[RANKER] Ranking safest bets...")

    required_pred_cols = ["pred_points", "pred_rebounds", "pred_assists", "pred_threes"]
    for col in required_pred_cols:
        if col not in df.columns:
            df[col] = 0.0

    # Simplified ranking metric:
    #   higher predicted production → safer overs
    df["safety_score"] = (
        df["pred_points"] * 0.4 +
        df["pred_rebounds"] * 0.2 +
        df["pred_assists"] * 0.2 +
        df["pred_threes"] * 0.2
    )

    ranked = df.sort_values("safety_score", ascending=False).head(30)

    print("[RANKER] Ranking generated!")
    return ranked
