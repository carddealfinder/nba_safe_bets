import os
import xgboost as xgb

def load_models(model_dir):
    models = {}
    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    # List JSON model files
    model_files = [f for f in os.listdir(model_dir) if f.endswith("_model.json")]
    print(f"[MODEL LOADER] Files found: {model_files}")

    for file in model_files:
        stat_name = file.replace("_model.json", "")  # points, rebounds, assists, threes
        model_path = os.path.join(model_dir, file)

        try:
            booster = xgb.Booster()
            booster.load_model(model_path)
            models[stat_name] = booster
            print(f"[MODEL LOADER] Loaded model: {stat_name}")

        except Exception as e:
            print(f"[MODEL ERROR] Failed to load {stat_name}: {e}")

    print(f"[MODEL LOADER] Final model keys: {list(models.keys())}")
    return models
