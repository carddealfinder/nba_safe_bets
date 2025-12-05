import pandas as pd

def rank_safe_bets(models, feature_df):
    predictions = []

    for idx, row in feature_df.iterrows():
        pid = row["id"]
        pred = {"id": pid}

        for stat, model in models.items():
            try:
                X = row[["points", "rebounds", "assists", "threes",
                         "injury_factor", "game_id"]].values.reshape(1, -1)
                pred[stat] = model.predict(X)[0]
            except Exception:
                pred[stat] = None

        predictions.append(pred)

    df = pd.DataFrame(predictions)
    return df
