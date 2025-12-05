import pandas as pd
import xgboost as xgb
import os


MODEL_DIR = os.path.join(os.path.dirname(__file__), "trained")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_FILES = {
    "points": "points_model.json",
    "rebounds": "rebounds_model.json",
    "assists": "assists_model.json",
    "threes": "threes_model.json"
}


def train_dummy_xgb_model(name: str):
    """Train a minimal but valid XGBoost classifier model."""

    print(f"🔧 Training model for: {name}")

    # Create dummy training data
    X = pd.DataFrame({
        "feature1": [0, 1, 0, 1],
        "feature2": [1, 1, 0, 0],
        "feature3": [0.2, 0.9, 0.1, 0.8]
    })

    y = [0, 1, 0, 1]

    # Convert to DMatrix
    dtrain = xgb.DMatrix(X, label=y)

    # Simple booster
    params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss"
    }

    model = xgb.train(params, dtrain, num_boost_round=20)

    # Save as .json
    out_path = os.path.join(MODEL_DIR, MODEL_FILES[name])
    model.save_model(out_path)

    print(f"✅ Saved model: {out_path}")


def train_all_models():
    print("==============================================")
    print("  TRAINING ALL XGBOOST MODELS FOR SAFE BETS")
    print("==============================================")

    for key in MODEL_FILES.keys():
        train_dummy_xgb_model(key)

    print("\n🎉 All XGBoost models trained successfully!\n")


if __name__ == "__main__":
    train_all_models()
