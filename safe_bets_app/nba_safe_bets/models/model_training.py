import xgboost as xgb
import pandas as pd
import os

def train_xgb_model(X: pd.DataFrame, y: pd.Series, output_path: str):
    model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss"
    )

    model.fit(X, y)

    # Save XGBoost model in JSON format (Streamlit Cloud safe)
    model.save_model(output_path)

    return model
