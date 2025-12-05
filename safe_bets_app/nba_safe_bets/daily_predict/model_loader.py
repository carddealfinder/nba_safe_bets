print("[DEBUG] model_loader.py loaded from:", __file__)

import os
import xgboost as xgb

def load_models():
    """
    Loads all XGBoost models from the trained/ directory.
    Works locally and on Streamlit Cloud.
    """

    # Determine directory of THIS file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Models are in: ../models/trained/
    model_dir = os.path.join(base_dir, "..", "models", "trained")
    model_dir = os.path.abspath(model_dir)

    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    if not os.path.isdir(model_dir):
        print("[MODEL ERROR] Model directory not found!")
        return {}

    models = {}
    model_names = ["points", "rebounds", "assists", "threes"]

    # Load JSON models only
    for name in model_names:
        json_file = os.path.join(model_dir, f"{name}_model.json")

        if not os.path.exists(json_file):
            print(f"[MODEL WARNING] Missing {name}_model.json")
            continue

        try:
            model = xgb.XGBClassifier()
            model.load_model(json_file)
            models[name] = model
            print(f"[MODEL LOADER] Loaded {name} model.")
        except Exception as e:
            print(f"[MODEL ERROR] Failed to load {name}: {e}")

    print(f"[MODEL LOADER] Final model keys: {list(models.keys())}")
    return models
