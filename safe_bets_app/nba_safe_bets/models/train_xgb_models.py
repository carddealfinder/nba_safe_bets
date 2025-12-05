import pandas as pd
import numpy as np
import xgboost as xgb
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "trained")
os.makedirs(MODEL_DIR, exist_ok=True)

# ------------------------------------------------------------
# Synthetic training data matching the EXACT feature columns
# ------------------------------------------------------------
df = pd.DataFrame({
    "id": np.arange(1, 501),
    "points": np.random.randint(5, 40, 500),
    "rebounds": np.random.randint(0, 15, 500),
    "assists": np.random.randint(0, 12, 500),
    "threes": np.random.randint(0, 8, 500),
    "injury_factor": np.random.randint(0, 2, 500),
    "game_id": np.random.randint(100, 500, 500),
})

FEATURES = ["id", "points", "rebounds", "assists", "threes", "injury_factor", "game_id"]

# Create slightly noisy targets
df["target_points"] = df["points"] + np.random.normal(0, 3, 500)
df["target_rebounds"] = df["rebounds"] + np.random.normal(0, 2, 500)
df["target_assists"] = df["assists"] + np.random.normal(0, 2, 500)
df["target_threes"] = df["threes"] + np.random.normal(0, 1, 500)

targets = {
    "points": "target_points",
    "rebounds": "target_rebounds",
    "assists": "target_assists",
    "threes": "target_threes",
}

# ------------------------------------------------------------
# Train XGBoost models
# ------------------------------------------------------------
print("Training models using features:", FEATURES)

for name, target in targets.items():
    print(f"\nTraining model: {name}")

    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
    )

    model.fit(df[FEATURES], df[target])

    output_path = os.path.join(MODEL_DIR, f"{name}_model.json")
    model.save_model(output_path)

    print(f"Saved model → {output_path}")

print("\n🎉 Training complete! New models generated successfully.")
