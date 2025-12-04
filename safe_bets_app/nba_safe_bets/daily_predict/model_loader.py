import os
import pickle

def load_all_models():
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "trained")
    model_dir = os.path.abspath(model_dir)

    print("🔍 Looking for models in:", model_dir)

    models = {}
    if not os.path.exists(model_dir):
        print("[ERROR] Model dir missing:", model_dir)
        return models

    for f in os.listdir(model_dir):
        if f.endswith(".pkl"):
            name = f.replace(".pkl", "")
            try:
                with open(os.path.join(model_dir, f), "rb") as h:
                    models[name] = pickle.load(h)
            except Exception as e:
                print("Model failed:", f, e)

    print("Loaded models:", list(models.keys()))
    return models
