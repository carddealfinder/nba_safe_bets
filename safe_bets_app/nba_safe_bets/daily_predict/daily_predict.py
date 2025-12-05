import pandas as pd
from nba_safe_bets.scrapers.player_info import get_player_info
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.vegas_odds import get_dk_odds

from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_feature_set
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets

MODEL_DIR = "safe_bets_app/nba_safe_bets/models/trained"

def daily_predict():
    players = get_player_info()
    schedule = get_todays_schedule()
    injuries = get_injury_report()
    defense = get_defense_rankings()
    dk = get_dk_odds()

    merged = build_daily_feature_set(players, schedule, injuries, defense, dk)

    feature_df = merged[[
        "full_name", "team", "points_avg", "rebounds_avg",
        "assists_avg", "threes_avg", "injury_factor"
    ]]

    models = load_models(MODEL_DIR)

    result = rank_safe_bets(feature_df, models)
    return merged, feature_df, result
