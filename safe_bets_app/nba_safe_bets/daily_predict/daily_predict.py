import os
import pandas as pd
from .daily_feature_builder import build_daily_features
from .model_loader import load_models
from .safe_bet_ranker import rank_safe_bets

# Scrapers
from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.vegas_odds import get_dk_odds


def daily_predict():
    print("\n🔍 DEBUG: Starting Daily Prediction Engine")

    # -----------------------------
    # SCRAPE DATA
    # -----------------------------
    players = get_player_list()
    print(f"Players DF Shape: {players.shape}")

    schedule = get_todays_schedule()
    print(f"Schedule DF Shape: {schedule.shape}")

    injuries = get_injury_report()
    print(f"Injury DF Shape: {injuries.shape}")

    defense = get_defense_rankings()
    print(f"Defense DF Shape: {defense.shape}")

    odds = get_dk_odds()
    if odds.empty:
        print("⚠ No odds available — continuing without lines.")
    print(f"DraftKings Odds Shape: {odds.shape}")

    # -----------------------------
    # BUILD DAILY MERGED FEATURES
    # -----------------------------
    merged = build_daily_features(
        players_df=players,
        schedule_df=schedule,
        injury_df=injuries,
        defense_df=defense,
        odds_df=odds
    )

    print(f"Merged DF Shape: {merged.shape}")

    if merged is None or merged.empty:
        return "❌ No merged data to build features."

    # -----------------------------
    # LOAD MODELS
    # -----------------------------
    MODEL_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models",
        "trained",
    )

    models = load_models(MODEL_DIR)
    print(f"Models Loaded: {list(models.keys())}")

    if not models:
        return "❌ No models found!"

    # -----------------------------
    # SAFE BET RANKING
    # -----------------------------
    predictions = rank_safe_bets(merged, models)

    return predictions
