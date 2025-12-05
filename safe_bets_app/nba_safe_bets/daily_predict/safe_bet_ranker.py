import pandas as pd
import numpy as np


def rank_safe_bets(predictions_dict):
    """
    predictions_dict = {
        "points": [(player_id, prob_over)],
        "rebounds": [...],
        ...
    }
    """

    rows = []
    for stat, preds in predictions_dict.items():
        for pid, prob in preds:
            rows.append({
                "player_id": pid,
                "stat": stat,
                "prob_over": prob
            })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Rank by highest probability
    df["rank"] = df["prob_over"].rank(ascending=False, method="first")

    df = df.sort_values("rank").reset_index(drop=True)

    return df
