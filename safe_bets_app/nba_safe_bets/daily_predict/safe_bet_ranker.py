import pandas as pd
from nba_safe_bets.utils.logging_config import log


def rank_safe_bets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ranks players by “safest bets”, based on:

    - predicted stats (pred_points, pred_assists...)
    - vegas line (points_line, etc.)
    - gap = prediction - line
    - injury factor (down-weight injured players)
    - defense difficulty (down-weight tough matchups)

    Works even if odds OR model predictions are missing.
    """

    log("[RANKER] Ranking safe bets...")

    required_pred_cols = [
        "pred_points", "pred_rebounds", "pred_assists", "pred_threes"
    ]

    # Ensure prediction columns exist
    for col in required_pred_cols:
        if col not in df.columns:
            log(f"[RANKER WARNING] Missing prediction column: {col} → filling with 0")
            df[col] = 0

    # Ensure lines exist
    line_cols = {
        "points": "points_line",
        "rebounds": "rebounds_line",
        "assists": "assists_line",
        "threes": "threes_line",
    }
    for stat, col in line_cols.items():
        if col not in df.columns:
            log(f"[RANKER WARNING] Missing line column: {col} → filling with 0")
            df[col] = 0

    # Compute gaps
    for stat, line_col in line_cols.items():
        pred_col = f"pred_{stat}"
        gap_col = f"gap_{stat}"
        df[gap_col] = df[pred_col] - df[line_col]

    # Injury factor: missing = assume healthy
    if "injury_factor" not in df.columns:
        df["injury_factor"] = 0

    # Defense adjustment: lower is harder, missing = neutral
    if "defense_difficulty" not in df.columns:
        df["defense_difficulty"] = 1.0

    # Compute a safety score
    df["safety_score"] = (
        df["gap_points"] * 0.4 +
        df["gap_rebounds"] * 0.2 +
        df["gap_assists"] * 0.2 +
        df["gap_threes"] * 0.2
    )

    # Penalize for injuries
    df["safety_score"] *= (1 - df["injury_factor"] * 0.5)

    # Penalize for defense difficulty
    df["safety_score"] *= df["defense_difficulty"]

    # Sort best → worst
    ranked = df.sort_values("safety_score", ascending=False).reset_index(drop=True)

    log(f"[RANKER] Ranking complete: {ranked.shape} rows")
    return ranked
