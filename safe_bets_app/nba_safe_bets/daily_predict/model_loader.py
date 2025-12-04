import os
import pickle


def load_all_models():
    # Compute correct absolute path to /models/trained/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.abspath(os.path.join(current_dir, "..", "models", "trained"))

    print(f"[DEBUG] Looking for models in: {model_dir}")

    models = {}

    if not os.path.isdir(model_dir):
        print(f"[ERROR] Model directory does NOT exist: {model_dir}")
        return models

    files = os.listdir(model_dir)
    print(f"[DEBUG] Files in model directory: {files}")

    for filename in files:
        if filename.endswith(".pkl"):
            stat_name = filename.replace("_model.pkl", "")  # Normalize naming
            fpath = os.path.join(model_dir, filename)

            try:
                with open(fpath, "rb") as f:
                    models[stat_name] = pickle.load(f)
                print(f"[DEBUG] Loaded model: {filename} -> {stat_name}")
            except Exception as e:
                print(f"[ERROR] Could not load model {filename}: {e}")

    print(f"[DEBUG] Models successfully loaded: {list(models.keys())}")
    return models
