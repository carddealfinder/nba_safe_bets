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
    """
    Main prediction engine.
    Returns:
        preds (DataFrame or None)
        debug_messages (list of str)
    """

    def log(msg):
        """Internal logger → collects messages for Streamlit."""
        if debug_log_fn:
            debug_log_fn(str(msg))
        print(msg)

    log("🔍 DEBUG: Starting Daily Prediction Engine")

    debug_messages = []

    # -----------------------------
    # Load players
    # -----------------------------
    players = get_player_list()
    log(f"Players DF Shape: {players.shape}")

    if players.empty:
        log("Player list is empty — cannot continue.")
        return None, debug_messages

    # -----------------------------
    # Load schedule
    # -----------------------------
    schedule = get_daily_schedule()
    log(f"Schedule DF Shape: {schedule.shape}")

    if schedule.empty:
        log("Schedule empty — no games today.")
        return None, debug_messages

    # -----------------------------
    # Load injuries
    # -----------------------------
    injuries = get_injury_report()
    log(f"Injury DF Shape: {injuries.shape}")

    # -----------------------------
    # Load defense rankings
    # -----------------------------
    defense = get_defense_rankings()
    log(f"Defense DF Shape: {defense.shape}")

    # -----------------------------
    # Load DraftKings odds
    # -----------------------------
    odds = get_draftkings_odds()
    log(f"DraftKings Odds Shape: {odds.shape}")

    if odds.empty:
        log("⚠ No odds available — continuing without lines.")

    # -----------------------------
    # Combine all data
    # -----------------------------
    df = players.merge(schedule, on="team", how="left")
    df = df.merge(injuries, on="id", how="left")
    df = df.merge(defense, on="team", how="left")

    if not odds.empty:
        df = df.merge(odds, on="player", how="left")

    log(f"Merged DF Shape: {df.shape}")

    # -----------------------------
    # Build numerical features
    # -----------------------------
    features = build_features(df)
    log(f"Feature DF Shape: {features.shape}")

    # -----------------------------
    # Load trained models
    # -----------------------------
    models = load_models()
    log(f"Models Loaded: {list(models.keys())}")

    if not models:
        log("⚠ No models available — cannot predict.")
        return None, debug_messages

    # -----------------------------
    # Rank bets
    # -----------------------------
    preds = rank_safe_bets(df, features, models)
    log(f"Prediction DF Shape: {preds.shape}")

    if preds.empty:
        log("No predictions produced.")
        return None, debug_messages

    # Return top 25
    preds = preds.sort_values("safety_score", ascending=False).head(25)

    return preds, debug_messages
