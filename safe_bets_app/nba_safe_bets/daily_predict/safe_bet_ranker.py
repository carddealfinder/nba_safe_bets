import pandas as pd


def rank_safe_bets(pred_df, merged_df):
    """
    Combines predictions with merged dataset and produces a ranked list of safe bets.
    """

    df = merged_df.copy()
    pred_cols = [c for c in pred_df.columns if c != "player_id"]

    # --------------------------
    # Merge predicted values
    # --------------------------
    df = df.merge(pred_df, left_on="id", right_on="player_id", how="left")
    df.drop(columns=["player_id"], inplace=True)

    # --------------------------
    # Build safety score
    # Weighted simple example (can tune later)
    # --------------------------
    df["safety_score"] = (
        df.get("points", 0) * 0.4 +
        df.get("rebounds", 0) * 0.2 +
        df.get("assists", 0) * 0.2 +
        df.get("threes", 0) * 0.2
    )

    # Push injured players lower
    df["safety_score"] -= df["injury_factor"] * 5

    # --------------------------
    # Sort best bets
    # --------------------------
    df = df.sort_values("safety_score", ascending=False)

    # Keep top 25
    return df.head(25)
