import os
import pickle

def load_models():
    """Load all trained stat models from /models/trained directory."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    trained_dir = os.path.join(base_dir, "models", "trained")

    trained_dir = os.path.abspath(trained_dir)
    print("[MODEL LOADER] Looking in:", trained_dir)

    if not os.path.exists(trained_dir):
        print("[MODEL LOADER ERROR] Directory not found")
        return {}

    models = {}

    for filename in os.listdir(trained_dir):
        if filename.endswith(".pkl"):
            stat = filename.replace("_model.pkl", "")
            full_path = os.path.join(trained_dir, filename)

            try:
                with open(full_path, "rb") as f:
                    models[stat] = pickle.load(f)
                print(f"[MODEL LOADER] Loaded: {filename}")
            except Exception as e:
                print(f"[MODEL ERROR] Could not load {filename}: {e}")

    print("[MODEL LOADER] Total models loaded:", len(models))
    return models
