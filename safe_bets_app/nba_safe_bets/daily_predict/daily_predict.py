import os
import pandas as pd

from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.DraftKings_scraper import get_dk_odds

from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_feature_set
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # ------------------------------------------------------------------
    # SCRAPE DATA
    # ------------------------------------------------------------------
    players = get_player_list()
    schedule = get_todays_schedule()
    injuries = get_injury_report()
    defense = get_defense_rankings()
    dk_odds = get_dk_odds()

    print(f"Players DF Shape: {players.shape}")
    print(f"Schedule DF Shape: {schedule.shape}")
    print(f"Injury DF Shape: {injuries.shape}")
    print(f"Defense DF Shape: {defense.shape}")
    print(f"DraftKings Odds Shape: {dk_odds.shape}")

    if schedule is None or len(schedule) == 0:
        print("⚠ No schedule data — continuing with placeholder game_id = 999999")
        schedule = pd.DataFrame({
            "team": players["team"].unique(),
            "game_id": 999999
        })

    # ------------------------------------------------------------------
    # BUILD FEATURES
    # ------------------------------------------------------------------
    merged_df, feature_df = build_daily_feature_set(
        players_df=players,
        schedule_df=schedule,
        injury_df=injuries,
        defense_df=defense,
        dk_df=dk_odds
    )

    print("Merged DF Shape:", merged_df.shape)
    print("Feature DF Shape:", feature_df.shape)

    # ------------------------------------------------------------------
    # LOAD MODELS
    # ------------------------------------------------------------------
    MODEL_DIR = os.path.join(
        os.path.dirname(__file__),
        "..", "models", "trained"
    )
    MODEL_DIR = os.path.abspath(MODEL_DIR)

    models = load_models(MODEL_DIR)

    if not models:
        print("❌ No models available — cannot predict.")
        return None

    # ------------------------------------------------------------------
    # RUN PREDICTIONS
    # ------------------------------------------------------------------
    preds = rank_safe_bets(models, feature_df)
    return preds, merged_df, feature_df
