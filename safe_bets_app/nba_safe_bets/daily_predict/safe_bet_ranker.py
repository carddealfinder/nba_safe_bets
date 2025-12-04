import pandas as pd
import numpy as np


def rank_safe_bets(models: dict, merged_df: pd.DataFrame, features_df: pd.DataFrame):
    """
    Run ML predictions + compute final risk score.
    Returns ranked top bets.
    """

    if merged_df.empty or features_df.empty:
        print("[RANKER] Empty dataset — skipping.")
        return pd.DataFrame()

    rows = []

    for stat_name, model in models.items():
        try:
            probs = model.predict_proba(features_df)[:, 1]
        except Exception as e:
            print(f"[RANKER ERROR] Model '{stat_name}' failed: {e}")
            continue

        for idx, prob in enumerate(probs):
            rows.append({
                "player": merged_df.iloc[idx]["first_name"] + " " + merged_df.iloc[idx]["last_name"],
                "team": merged_df.iloc[idx].get("team"),
                "opponent": merged_df.iloc[idx].get("opponent"),
                "stat": stat_name,
                "line": merged_df.iloc[idx].get("line"),
                "final_prob": float(prob),
                "safety_score": float(prob * 100)
            })

    df = pd.DataFrame(rows)

    if df.empty:
        print("[RANKER] No predictions created.")
        return df

    # Sort by safest → riskiest
    df = df.sort_values("safety_score", ascending=False)

    return df.head(25)
