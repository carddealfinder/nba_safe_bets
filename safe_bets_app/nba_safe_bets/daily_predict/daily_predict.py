import pandas as pd
import datetime
import traceback

# Scrapers
from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.vegas_odds import get_dk_odds

# Feature builder
from nba_safe_bets.daily_predict.daily_feature_builder import (
    build_daily_feature_set
)

# Model loader (NEW VERSION using dynamic model_dir)
from nba_safe_bets.daily_predict.model_loader import load_models

# Ranking logic
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    """
    Runs the full daily prediction pipeline:
    - Scrape players, schedule, injuries, defense, and odds
    - Build features
    - Load ML models
    - Predict props
    - Rank safest bets
    """

    print("\n🔍 DEBUG: Starting Daily Prediction Engine")

    try:
        # ------------------------
        # 1. Load all raw data
        # ------------------------
        players = get_player_list()
        print(f"Players DF Shape: {players.shape}")

        schedule = get_todays_schedule()
        print(f"Schedule DF Shape: {schedule.shape}")

        injuries = get_injury_report()
        print(f"Injury DF Shape: {injuries.shape}")

        defense = get_defense_rankings()
        print(f"Defense DF Shape: {defense.shape}")

        dk_odds = get_dk_odds()
        print(f"DraftKings Odds Shape: {dk_odds.shape}")

        if dk_odds.empty:
            print("⚠ No odds available — continuing without lines.")

        # ------------------------
        # 2. Build Daily Features
        # ------------------------
        merged_df = build_daily_feature_set(
            players_df=players,
            schedule_df=schedule,
            injury_df=injuries,
            defense_df=defense,
            dk_df=dk_odds
        )

        print(f"Merged DF Shape: {merged_df.shape}")

        # ------------------------
        # 3. Load Models
        # ------------------------
        models = load_models()  # Now auto-locates correct trained/ folder

        if not models:
            raise RuntimeError("❌ No models found!")

        # ------------------------
        # 4. Prepare feature dataframe
        # ------------------------
        required_cols = ["id", "game_id", "injury_factor"]
        stat_targets = ["points", "rebounds", "assists", "threes"]

        for stat in stat_targets:
            if stat not in merged_df.columns:
                merged_df[stat] = 0  # filler until real stats are added

        feature_cols = required_cols + stat_targets

        feature_df = merged_df[feature_cols].copy()
        print(f"Feature DF Shape: {feature_df.shape}")

        # ------------------------
        # 5. Make predictions
        # ------------------------
        predictions = {}

        for stat in stat_targets:
            model = models.get(stat)
            if model is None:
                print(f"⚠ Model missing for {stat}, skipping.")
                continue

            try:
                preds = model.predict(feature_df)
                predictions[stat] = preds
                merged_df[f"pred_{stat}"] = preds
            except Exception as e:
                print(f"Prediction error for {stat}: {e}")

        # ------------------------
        # 6. Rank safest bets
        # ------------------------
        if not predictions:
            raise RuntimeError("❌ No predictions generated.")

        ranked = rank_safe_bets(merged_df)
        print("🎯 Predictions & rankings complete!")

        return ranked

    except Exception as e:
        print(f"❌ Prediction engine crashed: {e}")
        traceback.print_exc()
        return None
