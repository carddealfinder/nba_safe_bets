import os
import pandas as pd

from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.vegas_odds import get_dk_odds

from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_feature_set
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets
from nba_safe_bets.daily_predict.model_loader import load_models


def daily_predict():
    """
    Orchestrates the daily prediction engine:
    - loads players
    - loads injury report
    - loads schedule
    - loads defense rankings
    - loads DK odds
    - merges everything and builds features
    - loads models
    - generates predictions + safe bet rankings
    """

    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # -----------------------------
    # 1. Load Players
    # -----------------------------
    players = get_player_list()
    print(f"Players DF Shape: {players.shape}")

    if players.empty:
        raise ValueError("Player list is empty — cannot continue")

    # -----------------------------
    # 2. Load Schedule
    # -----------------------------
    schedule = get_todays_schedule()
    print(f"Schedule DF Shape: {schedule.shape}")

    # -----------------------------
    # 3. Load Injury Report
    # -----------------------------
    injury_df = get_injury_report()
    print(f"Injury DF Shape: {injury_df.shape}")

    # -----------------------------
    # 4. Defense Rankings
    # -----------------------------
    defense_df = get_defense_rankings()
    print(f"Defense DF Shape: {defense_df.shape}")

    # -----------------------------
    # 5. Vegas Odds
    # -----------------------------
    dk_odds = get_dk_odds()
    print(f"DraftKings Odds Shape: {dk_odds.shape}")

    if dk_odds.empty:
        print("⚠ No odds available — continuing without lines.")

    # -----------------------------
    # 6. Build Features
    # -----------------------------
    merged_df = build_daily_feature_set(
        players_df=players,
        schedule_df=schedule,
        injury_df=injury_df,
        defense_df=defense_df,
        dk_df=dk_odds
    )

    print(f"Merged DF Shape: {merged_df.shape}")

    # Required columns for features
    feature_cols = [
        "id", "points", "rebounds", "assists", "threes",
        "injury_factor", "game_id"
    ]

    # Guarantee feature safety
    for col in feature_cols:
        if col not in merged_df.columns:
            print(f"[FEATURE WARNING] Missing feature column: {col} → defaulting to 0")
            merged_df[col] = 0

    feature_df = merged_df[feature_cols].copy()
    print(f"Feature DF Shape: {feature_df.shape}")

    # -----------------------------
    # 7. Load Models
    # -----------------------------
    model_dir = os.path.join(
        os.path.dirname(__file__),
        "..", "models", "trained"
    )
    model_dir = os.path.abspath(model_dir)

    models = load_models(model_dir)
    print(f"Models Loaded: {list(models.keys())}")

    if not models:
        raise ValueError("❌ No models found — cannot predict.")

    # -----------------------------
    # 8. Generate Predictions
    # -----------------------------
    preds = {}

    for stat, model in models.items():
        try:
            preds[stat] = model.predict(feature_df)
        except Exception as e:
            print(f"[PRED ERROR] Failed to predict {stat}: {e}")
            preds[stat] = [0] * len(feature_df)

    # Add predictions into main DF
    for stat in preds:
        merged_df[f"pred_{stat}"] = preds[stat]

    # -----------------------------
    # 9. Rank Bets
    # -----------------------------
    ranked = rank_safe_bets(merged_df)

    print("🔮 Prediction engine complete.")
    return ranked, merged_df, feature_df
