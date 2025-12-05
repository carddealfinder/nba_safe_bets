import os, sys

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(PACKAGE_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import os
import pandas as pd

from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_features
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    print("\n🔍 DEBUG: Starting Daily Prediction Engine")

    # Build feature matrix
    feature_df = build_daily_features()
    if feature_df.empty:
        print("⚠ No features generated.")
        return pd.DataFrame(), pd.DataFrame()

    # Load models
    model_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "trained"
    )
    print("[MODEL LOADER] Using model dir:", model_dir)

    models = load_models(model_dir)

    predictions = {
        "points": [],
        "rebounds": [],
        "assists": [],
        "threes": [],
    }

    # Predict
    for stat, model in models.items():
        try:
            probs = model.predict_proba(
                feature_df[["points", "rebounds", "assists", "threes", "injury_factor", "game_id"]]
            )[:, 1]

            for pid, prob in zip(feature_df["id"], probs):
                predictions[stat].append((pid, float(prob)))

        except Exception as e:
            print(f"[PREDICT ERROR] {stat}: {e}")

    ranked_df = rank_safe_bets(predictions)

    return ranked_df, feature_df
