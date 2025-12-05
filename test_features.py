import pandas as pd

# Import your real feature builder
from safe_bets_app.nba_safe_bets.processors.feature_builder import build_features

# -------------------------------------------------------
# Fake merged dataframe including required columns
# -------------------------------------------------------
fake = pd.DataFrame({
    "id": [1],
    "team": ["Lakers"],
    "first_name": ["LeBron"],
    "last_name": ["James"],
    "points": [25],
    "rebounds": [7],
    "assists": [8],
    "threes": [2],
    "injury_status": [None],      # REQUIRED BY context_features.py
    "injury_factor": [0],         # ok to include
    "game_id": [111],
})

# -------------------------------------------------------
# Run feature pipeline
# -------------------------------------------------------
features = build_features(fake)

# -------------------------------------------------------
# Show the resulting feature names
# -------------------------------------------------------
print("\nFEATURE COLUMNS:")
print(features.columns.tolist())

print("\nFEATURE DF:")
print(features)
