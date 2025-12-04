import pandas as pd

EXPECTED_STATS = ["points", "rebounds", "assists", "threes"]

def rank_safe_bets(df):
    """
    Convert wide prediction DataFrame into long-form bet rows
    and compute placeholder probabilities so Streamlit can render the table.
    """

    if df is None or df.empty:
        print("⚠️ No prediction data available for ranking.")
        return pd.DataFrame()

    rows = []
    for _, row in df.iterrows():
        for stat in EXPECTED_STATS:
            value = row.get(stat)

            # Skip missing model predictions
            if value is None:
                continue

            rows.append({
                "player": row.get("PLAYER_NAME", "Unknown"),
                "player_id": row.get("PLAYER_ID"),
                "team": row.get("TEAM_ID"),

                "stat": stat,
                "line": round(value * 0.8, 1),        # placeholder line
                "ml_prob": round(min(0.98, value / (value + 5)), 3),  # placeholder
                "final_prob": round(min(0.98, value / (value + 4)), 3),
                "weighted_prob": round(min(0.98, value / (value + 3)), 3),
                "safety_score": round(min(100, value * 10), 1)
            })

    if not rows:
        print("⚠️ No stat rows generated — check model output")
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)

    # Sort descending by safest bets
    df_out = df_out.sort_values("safety_score", ascending=False).head(25)

    print("Ranked Bet Rows Head:")
    print(df_out.head())

    return df_out
