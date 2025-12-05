import pandas as pd


def rank_safe_bets(df, models):
    result_rows = []

    for _, row in df.iterrows():
        pid = row["player_id"]

        entry = {
            "player_id": pid,
            "player": f"{row['first_name']} {row['last_name']}",
            "team": row["team"],
        }

        # Predict stats
        for stat, model in models.items():
            try:
                X = row[["injury_factor", "def_rating", "team_game_count"]].values.reshape(1, -1)
                entry[f"pred_{stat}"] = float(model.predict(X)[0])
            except:
                entry[f"pred_{stat}"] = None

        result_rows.append(entry)

    df_out = pd.DataFrame(result_rows)

    # Rank safest by lowest predicted variance (proxy)
    df_out["safety_score"] = (
        df_out["pred_points"].fillna(0) * 0.4 +
        df_out["pred_rebounds"].fillna(0) * 0.2 +
        df_out["pred_assists"].fillna(0) * 0.3 +
        df_out["pred_threes"].fillna(0) * 0.1
    )

    return df_out.sort_values("safety_score", ascending=False)
