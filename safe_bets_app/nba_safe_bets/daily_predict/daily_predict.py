import pandas as pd

# --- SCRAPERS ---
from ..scrapers.balldontlie_players import get_player_list
from ..scrapers.schedule_scraper import get_daily_schedule
from ..scrapers.injury_report import get_injury_report
from ..scrapers.defense_rankings import get_defense_rankings
from ..scrapers.DraftKings_scraper import get_draftkings_odds

# --- MODELS ---
from .model_loader import load_models

# --- FEATURE PIPELINE ---
from ..processors.feature_builder import build_features
from .safe_bet_ranker import rank_safe_bets


def daily_predict(debug_log_fn=None):
    \"\"\"Runs the daily prediction pipeline end-to-end.\"\"\"

    def log(msg):
        print(msg)
        if debug_log_fn:
            debug_log_fn(msg)

    log("🔍 DEBUG: Starting Daily Prediction Engine")

    players = get_player_list()
    log(f"Players DF Shape: {players.shape}")
    if players.empty:
        log("❌ Player list empty — stopping.")
        return None

    schedule = get_daily_schedule()
    log(f"Schedule DF Shape: {schedule.shape}")
    if schedule.empty:
        log("⚠ No games today — prediction aborted.")
        return None

    injuries = get_injury_report()
    log(f"Injury DF Shape: {injuries.shape}")

    defense = get_defense_rankings()
    log(f"Defense DF Shape: {defense.shape}")

    odds = get_draftkings_odds()
    log(f"DraftKings Odds Shape: {odds.shape}")
    if odds.empty:
        log("⚠ No odds available — continuing without lines.")
        odds["line"] = None

    merged = players.merge(schedule, on="team", how="left")
    merged = merged.merge(injuries, on="id", how="left")
    merged = merged.merge(defense, on="team", how="left")

    if "player" in odds.columns:
        odds = odds.rename(columns={"player": "full_name"})
        merged["full_name"] = merged["first_name"] + " " + merged["last_name"]
        merged = merged.merge(odds, on="full_name", how="left")

    log(f"Merged DF Shape: {merged.shape}")

    features = build_features(merged)
    log(f"Feature DF Shape: {features.shape}")

    models = load_models()
    log(f"Models Loaded: {list(models.keys())}")
    if not models:
        log("⚠ No models available — cannot predict.")
        return None

    for stat, model in models.items():
        try:
            merged[f"pred_{stat}"] = model.predict_proba(features)[:, 1]
        except Exception as e:
            log(f"[PREDICT ERROR] {stat}: {e}")

    ranked = rank_safe_bets(merged)
    log("Prediction pipeline finished successfully.")

    return ranked
