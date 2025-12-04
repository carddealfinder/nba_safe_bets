import os
import pickle

def load_models(debug_log_fn=print):
    """
    Load all .pkl models from the trained/ directory
    regardless of whether app runs locally or on Streamlit Cloud.
    """

    # Directory containing THIS file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Correct trained model directory using relative path
    trained_dir = os.path.join(current_dir, "..", "models", "trained")

    trained_dir = os.path.abspath(trained_dir)

    debug_log_fn(f"[MODEL LOADER] Looking for models in: {trained_dir}")

    if not os.path.exists(trained_dir):
        debug_log_fn("[MODEL LOADER ERROR] Directory does not exist")
        return {}

    model_files = [f for f in os.listdir(trained_dir) if f.endswith(".pkl")]
    debug_log_fn(f"[MODEL LOADER] Files found: {model_files}")

    models = {}

    for filename in model_files:
        path = os.path.join(trained_dir, filename)
        stat = filename.replace("_model.pkl", "")

        try:
            with open(path, "rb") as f:
                models[stat] = pickle.load(f)
            debug_log_fn(f"[MODEL LOADER] Loaded: {filename}")

        except Exception as e:
            debug_log_fn(f"[MODEL LOADER ERROR] Failed to load {filename}: {e}")

    debug_log_fn(f"[MODEL LOADER] Final model keys: {list(models.keys())}")

    return models
