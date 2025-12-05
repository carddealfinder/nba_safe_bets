import pandas as pd

def rank_safe_bets(df, model_dict):
    df = df.copy()

    df["pred_points"] = df.get("points_avg", 0)
    df["pred_rebounds"] = df.get("rebounds_avg", 0)
    df["pred_assists"] = df.get("assists_avg", 0)
    df["pred_threes"] = df.get("threes_avg", 0)

    df["score"] = (
        df["pred_points"] * 0.4 +
        df["pred_rebounds"] * 0.2 +
        df["pred_assists"] * 0.3 +
        df["pred_threes"] * 0.1
    )

    return df.sort_values("score", ascending=False)
