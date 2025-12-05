import os
import xgboost as xgb

def load_models(model_dir):
    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    models = {}
    for stat in ["points", "rebounds", "assists", "threes"]:
        path = os.path.join(model_dir, f"{stat}_model.json")
        if not os.path.exists(path):
            print(f"[MODEL WARNING] Missing: {path}")
            continue

        try:
            m = xgb.XGBRegressor()
            m.load_model(path)
            models[stat] = m
        except Exception as e:
            print(f"[MODEL ERROR] Could not load {stat}: {e}")

    print(f"[MODEL LOADER] Final model keys: {list(models.keys())}")
    return models
