import os
import pickle


def load_all_models():
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "trained")
    model_dir = os.path.abspath(model_dir)

    models = {}
    if not os.path.exists(model_dir):
        print("[ERROR] Model directory not found:", model_dir)
        return models

    for filename in os.listdir(model_dir):
        if filename.endswith(".pkl"):
            stat_name = filename.replace(".pkl", "")

            try:
                with open(os.path.join(model_dir, filename), "rb") as f:
                    models[stat_name] = pickle.load(f)
            except Exception as e:
                print(f"[ERROR] Could not load model {filename}: {e}")

    return models
