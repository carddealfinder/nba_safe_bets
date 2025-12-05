import os
import xgboost as xgb


def load_models(model_dir):
    """
    Loads the XGBoost models stored as .json files
    in the trained directory.
    """

    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    models = {}
    stat_names = ["points", "rebounds", "assists", "threes"]

    for stat in stat_names:
        filename = f"{stat}_model.json"
        full_path = os.path.join(model_dir, filename)

        if not os.path.exists(full_path):
            print(f"[MODEL WARNING] Missing model: {filename}")
            continue

        try:
            model = xgb.XGBRegressor()
            model.load_model(full_path)
            models[stat] = model
            print(f"[MODEL LOADER] Loaded {stat} model.")
        except Exception as e:
            print(f"[MODEL ERROR] Could not load {stat}: {e}")

    print(f"[MODEL LOADER] Final model keys: {list(models.keys())}")
    return models
