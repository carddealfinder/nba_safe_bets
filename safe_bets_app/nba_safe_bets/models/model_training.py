import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from models.feature_selector import select_features

from utils.logging_config import log

DATASET_PATH = "data/processed/training_dataset.parquet"
MODEL_OUTPUT_DIR = "models/trained"

# All alternate lines we train models for
PROP_LINES = {
    "PTS": [5, 10, 15, 20, 25, 30, 35],
    "REB": [4, 6, 8, 10, 12, 14],
    "AST": [2, 4, 6, 8, 10, 12],
    "3PM": [1, 2, 3, 4, 5]
}

def train_single_model(df, stat, line):
    """
    Trains and saves an XGBoost classifier for a given stat-line (ex: PTS_10).
    """
    label_col = f"HIT_{stat}_{line}"

    if label_col not in df.columns:
        log.error(f"Label column {label_col} missing.")
        return

    X = select_features(df)
    y = df[label_col]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, shuffle=True, random_state=42
    )

    model = xgb.XGBClassifier(
        n_estimators=350,
        learning_rate=0.06,
        max_depth=6,
        subsample=0.75,
        colsample_bytree=0.75,
        eval_metric="logloss"
    )

    # Train
    log.info(f"Training model for {stat} {line}+ …")
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    log.info(f"{stat} {line}+ AUC = {auc:.3f}")

    # Save model
    path = f"{MODEL_OUTPUT_DIR}/xgb_{stat.lower()}_{line}.model"
    model.save_model(path)
    log.info(f"✔ Saved model: {path}")

def train_all_models():
    log.info("🚀 Starting ML training for ALL PROP LINES…")

    # Ensure model folder exists
    os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

    # Load the processed dataset
    df = pd.read_parquet(DATASET_PATH)
    log.info(f"✔ Loaded dataset ({len(df)} rows).")

    # Train every model
    for stat, lines in PROP_LINES.items():
        for line in lines:
            train_single_model(df, stat, line)

    log.info("🎉 All ML models trained and saved!")


if __name__ == "__main__":
    train_all_models()
