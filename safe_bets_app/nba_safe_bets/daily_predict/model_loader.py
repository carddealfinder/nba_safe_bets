import os
import xgboost as xgb


def get_default_model_dir():
    """
    Compute the path to /models/trained based on the location of THIS file.
    Works on both local machines and Streamlit Cloud.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # This file is in: .../nba_safe_bets/daily_predict/
    # Models are in:   .../nba_safe_bets/models/trained/
    model_dir = os.path.abspath(
        os.path.join(current_dir, "..", "models", "trained")
    )

    print(f"[MODEL LOADER] Computed default model directory: {model_dir}")
    return model_dir


def load_models(model_dir=None):
    """
    Loads the XGBoost models stored as .json files in the trained directory.
    Returns a dictionary of models keyed by stat type.
    """

    if model_dir is None:
        model_dir = get_default_model_dir()

    print(f"[MODEL LOADER] Looking for models in: {model_dir}")

    if not os.path.exists(model_dir):
        print(f"[MODEL ERROR] Model directory does NOT exist: {model_dir}")
        return {}

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
