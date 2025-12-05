import os
import pandas as pd

from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.DraftKings_scraper import get_dk_props

from nba_safe_bets.processors.feature_builder import build_features
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


# --------------------------------------------------------------------
# MODEL DIRECTORY RESOLUTION (works both locally & on Streamlit Cloud)
# --------------------------------------------------------------------
MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),  # go up from daily_predict/
    "models",
    "trained"
)

print(f"[MODEL DIR RESOLVED] {MODEL_DIR}")


def daily_predict():
    """Runs the end-to-end daily prediction pipeline."""

    print("\n🔍 DEBUG: Starting Daily Prediction Engine")

    # -----------------------------
    # 1. Fetch Players
    # -----------------------------
    players_df = get_player_list()
    print("Players DF Shape:", players_df.shape)

    # -----------------------------
    # 2. Fetch Schedule
    # -----------------------------
    schedule_df = get_todays_schedule()
    print("Schedule DF Shape:", schedule_df.shape)

    # -----------------------------
    # 3. Fetch Injuries
    # -----------------------------
    injury_df = get_injury_report()
    print("Injury DF Shape:", injury_df.shape)

    # -----------------------------
    # 4. Fetch Defense Rankings
    # -----------------------------
    defense_df = get_defense_rankings()
    print("Defense DF Shape:", defense_df.shape)

    # -----------------------------
    # 5. Fetch Vegas / DK Lines
    # -----------------------------
    dk_df = get_dk_props()
    print("DraftKings Odds Shape:", dk_df.shape)

    if dk_df.empty:
        print("⚠ No odds available — continuing without lines.")

    # -----------------------------
    # 6. Merge Data
    # -----------------------------
    merged = players_df.copy()
    merged["game_id"] = 111  # placeholder for now until schedule mapping final

    print("Merged DF Shape:", merged.shape)

    # -----------------------------
    # 7. Build ML-ready Features
    # -----------------------------
    features = build_features(merged)
    print("Feature DF Shape:", features.shape)

    # -----------------------------
    # 8. Load Models
    # -----------------------------
    print(f"[MODEL LOADER] Looking for models in: {MODEL_DIR}")

    models = load_models(MODEL_DIR)
    print("Models Loaded:", list(models.keys()))

    if not models:
        print("⚠ No models available — cannot predict.")
        return pd.DataFrame()

    # -----------------------------
    # 9. Run Predictions
    # -----------------------------
    predictions = {}
    for stat, model in models.items():
        try:
            predictions[stat] = model.predict_proba(features)[:, 1]
        except Exception as e:
            print(f"[PREDICT ERROR] {stat}: {e}")

    if not predictions:
        print("⚠ Could not generate any predictions.")
        return pd.DataFrame()

    # -----------------------------
    # 10. Rank Safe Bets
    # -----------------------------
    results_df = rank_safe_bets(merged, predictions)
    print("\n🔒 Top 25 Safest Bets Today")
    print(results_df.head(25))

    return results_df
