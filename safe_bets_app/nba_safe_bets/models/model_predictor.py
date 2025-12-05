from nba_safe_bets.daily_predict.model_loader import load_models


def run_model_predictions(feature_df, model_dir):
    models = load_models(model_dir)
    results = {}

    if not models:
        print("⚠ No models found — prediction aborted.")
        return results

    for name, model in models.items():
        try:
            preds = model.predict(feature_df)
            results[name] = preds
            print(f"[PREDICT] {name}: {len(preds)} predictions")
        except Exception as e:
            print(f"[PREDICT ERROR] {name}: {e}")

    return results
