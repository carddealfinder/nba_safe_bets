$path = "C:\Users\srmic\nba_safe_bets\safe_bets_app\nba_safe_bets\models\trained\create_dummy_models.py"

@"
import os
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# Folder inside repo
MODEL_DIR = os.path.dirname(__file__)

models_to_create = {
    "points_model.pkl": 12.5,
    "rebounds_model.pkl": 5.8,
    "assists_model.pkl": 4.1,
    "threes_model.pkl": 2.2
}

def create_dummy_regressor(constant_value):
    """
    Creates a dummy model that always predicts a constant number.
    Useful for testing the ML pipeline.
    """
    X = np.array([[0], [1], [2], [3], [4], [5]])
    y = np.full_like(X, constant_value, dtype=float)

    model = LinearRegression()
    model.fit(X, y)

    return model

def main():
    print("Creating dummy models in:", MODEL_DIR)
    
    for filename, constant_value in models_to_create.items():
        model = create_dummy_regressor(constant_value)
        path = os.path.join(MODEL_DIR, filename)

        with open(path, "wb") as f:
            pickle.dump(model, f)

        print(f"✔ Created {filename} (predicts ~{constant_value})")

    print("All dummy models created successfully.")

if __name__ == "__main__":
    main()
"@ | Set-Content -Path $path
