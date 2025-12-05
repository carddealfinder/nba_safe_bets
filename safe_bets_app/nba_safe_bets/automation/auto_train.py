"""
AUTO-TRAINER: Rebuilds training dataset + retrains XGBoost models.
Runs safely on both local machine and Streamlit Cloud.

Schedule: Nightly (2:00 AM)
"""

import os
import sys
import pandas as pd
from datetime import datetime

from nba_safe_bets.models.train_xgb_models import train_all_models
from nba_safe_bets.build_training_dataset import build_training_dataset

LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "auto_train_log.txt"
)


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def main():
    log("🚀 AUTO-TRAIN STARTED")

    try:
        log("📦 Rebuilding training dataset...")
        df = build_training_dataset()
        log(f"Training dataset built → Shape: {df.shape}")

    except Exception as e:
        log(f"❌ ERROR building dataset: {e}")
        return

    try:
        log("🎯 Training all models...")
        train_all_models(df)
        log("✅ Models retrained successfully!")

    except Exception as e:
        log(f"❌ ERROR training models: {e}")
        return

    log("🏁 AUTO-TRAIN FINISHED")


if __name__ == "__main__":
    main()
