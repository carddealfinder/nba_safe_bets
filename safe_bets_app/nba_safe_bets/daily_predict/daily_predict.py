import pandas as pd
from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.DraftKings_scraper import fetch_dk_props
from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_feature_set
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict(model_dir):
    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # --------------------------------------------------------------
    # 1. Scrape data
    # --------------------------------------------------------------
    players = get_player_list()
    print("Players DF Shape:", players.shape)

    schedule = get_todays_schedule()
    print("Schedule DF Shape:", schedule.shape)

    injuries = get_injury_report()
    print("Injury DF Shape:", injuries.shape)

    defense = get_defense_rankings()
    print("Defense DF Shape:", defense.shape)

    dk_odds = fetch_dk_props()
    print("DraftKings Odds Shape:", dk_odds.shape)

    if dk_odds.empty:
        print("⚠ No odds available — continuing without lines.")

    # --------------------------------------------------------------
    # 2. Build features
    # --------------------------------------------------------------
    merged_df = build_daily_feature_set(
        players_df=players,
        schedule_df=schedule,
        injury_df=injuries,
        defense_df=defense,
        dk_df=dk_odds
    )
    print("Merged DF Shape:", merged_df.shape)

    # --------------------------------------------------------------
    # 3. Load Models
    # --------------------------------------------------------------
    models = load_models(model_dir)
    if not models:
        raise RuntimeError("❌ No models found!")

    # --------------------------------------------------------------
    # 4. Run predictions
    # --------------------------------------------------------------
    predictions = rank_safe_bets(merged_df, models)

    return predictions, merged_df
