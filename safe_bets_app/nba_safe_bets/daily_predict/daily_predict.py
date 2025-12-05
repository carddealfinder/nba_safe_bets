import os
import sys
import pandas as pd

# --------------------------------------------------------------------
# FIX: Ensure imports resolve from project root (local + Streamlit Cloud)
# --------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# --------------------------------------------------------------------
# Imports (now stable)
# --------------------------------------------------------------------
from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.DraftKings_scraper import get_draftkings_lines

from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_features
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


# --------------------------------------------------------------------
# MAIN DAILY PREDICTION ENGINE
# --------------------------------------------------------------------
def daily_predict():
    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # ----------------------------------------------------------------
    # SCRAPER INPUTS
    # ----------------------------------------------------------------
    players_df = get_player_list()
    print("Players DF Shape:", players_df.shape)

    schedule_df = get_todays_schedule()
    print("Schedule DF Shape:", schedule_df.shape)

    injury_df = get_injury_report()
    print("Injury DF Shape:", injury_df.shape)

    defense_df = get_defense_rankings()
    print("Defense DF Shape:", defense_df.shape)

    odds_df = get_draftkings_lines()
    print("DraftKings Odds Shape:", odds_df.shape)

    if odds_df.empty:
        print("⚠ No odds available — continuing without lines.")

    # ----------------------------------------------------------------
    # MERGE DATASETS
    # ----------------------------------------------------------------
    merged = build_daily_features(
        players_df,
        schedule_df,
        injury_df,
        defense_df,
        odds_df
    )

    print("Merged DF Shape:", merged.shape)

    # ----------------------------------------------------------------
    # BUILD FEATURE MATRIX
    # ----------------------------------------------------------------
    feature_df = merged[["id", "points", "rebounds", "assists", "threes", "injury_factor", "game_id"]].copy()
    print("Feature DF Shape:", feature_df.shape)

    # ----------------------------------------------------------------
    # LOAD MODELS
    # ----------------------------------------------------------------
    MODEL_DIR = os.path.join(ROOT_DIR, "nba_safe_bets", "models", "trained")
    models = load_models(MODEL_DIR)

    print("Models Loaded:", list(models.keys()))

    if not models:
        print("⚠ No models available — cannot predict.")
        return None, players_df

    # ----------------------------------------------------------------
    # MAKE MODEL PREDICTIONS
    # ----------------------------------------------------------------
    preds = {"player_id": merged["id"]}

    for stat_name, model in models.items():
        try:
            preds[stat_name] = model.predict(feature_df)
        except Exception as e:
            print(f"[PREDICT ERROR] {stat_name}: {e}")
            preds[stat_name] = [None] * len(feature_df)

    pred_df = pd.DataFrame(preds)

    # ----------------------------------------------------------------
    # RANK SAFE BETS
    # ----------------------------------------------------------------
    final_df = rank_safe_bets(pred_df, merged)

    return final_df, players_df
