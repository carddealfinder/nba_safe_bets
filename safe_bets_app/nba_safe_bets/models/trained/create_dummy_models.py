import os
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

# -----------------------------------------------------------
# 11 PROP TYPES SUPPORTED
# -----------------------------------------------------------
PROP_LIST = [
    "points",
    "rebounds",
    "assists",
    "threes",
    "blocks",
    "steals",
    "pra",
    "pr",
    "ra",
    "pts_reb_ast",
    "fantasy_score"
]

def create_synthetic_model():
    """
    Creates a LOGISTIC REGRESSION model trained on synthetic data.
    Produces realistic-looking probabilities between 0.45–0.65.
    """
    X = np.random.rand(300, 6)
    y = np.random.randint(0, 2, 300)

    model = LogisticRegression()
    model.fit(X, y)

    return model


def save_all_models():
    here = os.path.dirname(__file__)
    model_dir = here  # already IN "trained/"

    print(f"Saving dummy models to: {model_dir}")

    for prop in PROP_LIST:
        model = create_synthetic_model()
        filename = os.path.join(model_dir, f"{prop}_model.pkl")

        with open(filename, "wb") as f:
            pickle.dump(model, f)

        print(f"✔ Saved: {filename}")

    print("\n🎉 ALL 11 MODELS CREATED SUCCESSFULLY!\n")


if __name__ == "__main__":
    save_all_models()
