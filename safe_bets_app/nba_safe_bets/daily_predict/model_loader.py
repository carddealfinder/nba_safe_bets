import os
import pickle

SUPPORTED_STATS = [
    "points",
    "rebounds",
    "assists",
    "threes",
    "points_rebounds",
    "points_assists",
    "rebounds_assists",
    "pra"
]

MODEL_DIR = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "models", "trained"
)

def load_models():
    models = {}

    for stat in SUPPORTED_STATS:
        path = os.path.join(MODEL_DIR, f"{stat}_model.pkl")

        if not os.path.exists(path):
            print(f"[WARNING] No model found for {stat} — using dummy probability model.")
            models[stat] = DummyModel()
            continue

        try:
            with open(path, "rb") as f:
                models[stat] = pickle.load(f)
            print(f"Loaded: {stat}_model.pkl")

        except Exception as e:
            print(f"[ERROR] Failed loading model for {stat}: {e}")
            models[stat] = DummyModel()

    return models


# -----------------------
# Dummy fallback model
# -----------------------
class DummyModel:
    def predict_proba(self, X):
        # Always return 0.5 probability — neutral baseline
        import numpy as np
        return np.array([[0.5, 0.5] for _ in range(len(X))])
