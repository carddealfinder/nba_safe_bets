import os
import pickle

def load_all_models():
    # Show working directory
    print("[DEBUG] CWD:", os.getcwd())

    # Show where THIS file is
    print("[DEBUG] model_loader.py location:", os.path.abspath(__file__))

    # Compute model directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.abspath(os.path.join(current_dir, "..", "models", "trained"))

    print("[DEBUG] Expecting model directory at:", model_dir)
    print("[DEBUG] Directory exists:", os.path.isdir(model_dir))

    if os.path.isdir(model_dir):
        print("[DEBUG] Directory contents:", os.listdir(model_dir))
    else:
        print("[DEBUG] Directory NOT FOUND.")

    models = {}

    if not os.path.isdir(model_dir):
        print("[ERROR] Model directory does not exist.")
        return models

    # Load .pkl files
    for filename in os.listdir(model_dir):
        if filename.endswith(".pkl"):
            stat_name = filename.replace("_model.pkl", "")
            fpath = os.path.join(model_dir, filename)

            print(f"[DEBUG] Attempting to load {filename}")

            try:
                with open(fpath, "rb") as f:
                    models[stat_name] = pickle.load(f)
                print(f"[DEBUG] Loaded {stat_name}")
            except Exception as e:
                print(f"[ERROR] Failed to load {filename}: {e}")

    print("[DEBUG] Final models loaded:", list(models.keys()))
    return models
