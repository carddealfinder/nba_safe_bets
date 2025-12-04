import pandas as pd

from ..scrapers.balldontlie_players import get_player_list
from ..scrapers.schedule_scraper import get_daily_schedule
from ..scrapers.injury_report import get_injury_report
from ..scrapers.defense_rankings import get_defense_rankings
from ..scrapers.DraftKings_scraper import get_draftkings_odds

from .model_loader import load_models
from .safe_bet_ranker import rank_safe_bets

from ..processors.feature_builder import build_features


def daily_predict(debug_log_fn=None):
    log = debug_log_fn or (lambda msg: None)

    log("🔍 DEBUG: Starting Daily Prediction Engine")

    # --------------------------
    # SCRAPE DATA
    # --------------------------
    players = get_player_list()
    log(f"Players DF Shape: {players.shape}")

    schedule = get_daily_schedule()
    log(f"Schedule DF Shape: {schedule.shape}")

    injuries = get_injury_report()
    log(f"Injury DF Shape: {injuries.shape}")

    defense = get_defense_rankings()
    log(f"Defense DF Shape: {defense.shape}")

    odds = get_draftkings_odds()
    log(f"DraftKings Odds Shape: {odds.shape}")

    if odds.empty:
        log("⚠ No odds available — continuing without lines.")

    # --------------------------
    # MERGE ALL SOURCES
    --------------------------
    df = players.copy()
    df = df.merge(schedule, on="team", how="left")
    df = df.merge(injuries, on="id", how="left")
    df = df.merge(defense, on="team", how="left")
    df = df.merge(odds, left_on="last_name", right_on="player", how="left")

    log(f"Merged DF Shape: {df.shape}")

    # --------------------------
    # BUILD FEATURES
    --------------------------
    features = build_features(df)
    log(f"Feature DF Shape: {features.shape}")

    # --------------------------
    # LOAD MODELS
    --------------------------
    models = load_models()
    log(f"Models Loaded: {list(models.keys())}")

    if not models:
        log("⚠ No models available — cannot predict.")
        return None

    # --------------------------
    # RUN PREDICTIONS
    --------------------------
    preds = rank_safe_bets(df, features, models)
    return preds

