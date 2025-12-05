import os
import xgboost as xgb


def load_models(model_dir):
    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    models = {}
    stat_names = ["points", "rebounds", "assists", "threes"]

    for stat in stat_names:
        path = os.path.join(model_dir, f"{stat}_model.json")

        if not os.path.exists(path):
            print(f"[MODEL WARNING] Missing model for {stat}")
            continue

        model = xgb.XGBRegressor()
        model.load_model(path)
        models[stat] = model

    return models
