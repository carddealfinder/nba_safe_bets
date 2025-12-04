import os
import joblib
from sklearn.dummy import DummyRegressor
import numpy as np

MODEL_NAMES = ["points", "rebounds", "assists", "threes"]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ensure_dir(BASE_DIR)

print("Saving dummy models to:", BASE_DIR)

for name in MODEL_NAMES:
    model = DummyRegressor(strategy="mean")
    model.fit(np.array([[1], [2], [3]]), np.array([5, 5, 5]))  # Always predicts 5

    out_path = os.path.join(BASE_DIR, f"{name}_model.pkl")
    joblib.dump(model, out_path)

    print(f"Created: {out_path}")
