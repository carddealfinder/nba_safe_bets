import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

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

MODEL_DIR = os.path.join(os.path.dirname(__file__), "trained")


def train_stat_model(stat_name, df):
    """
    Train any stat category (including combo stats).
    df must contain:
        - features (whatever your feature builder outputs)
        - target column named f"{stat_name}_target"
    """

    target_col = f"{stat_name}_target"

    if target_col not in df.columns:
        print(f"[SKIP] {stat_name}: No target column found.")
        return

    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200)
    model.fit(X_train, y_train)

    # Save
    out_path = os.path.join(MODEL_DIR, f"{stat_name}_model.pkl")
    with open(out_path, "wb") as f:
        pickle.dump(model, f)

    print(f"✓ Trained + saved {stat_name} model → {out_path}")


def train_all_models(df):
    """Train all 8 stat models using the same dataset."""
    for stat in SUPPORTED_STATS:
        train_stat_model(stat, df)
