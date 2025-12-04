import os
import pickle


def load_models():
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "trained")
    model_dir = os.path.abspath(model_dir)

    models = {}

    if not os.path.exists(model_dir):
        print("[ERROR] Model directory missing:", model_dir)
        return models

    for name in os.listdir(model_dir):
        if not name.endswith(".pkl"):
            continue

        path = os.path.join(model_dir, name)
        key = name.replace("_model.pkl", "")

        try:
            with open(path, "rb") as f:
                models[key] = pickle.load(f)
        except Exception as e:
            print(f"[ERROR] Cannot load model {name}: {e}")

    return models
