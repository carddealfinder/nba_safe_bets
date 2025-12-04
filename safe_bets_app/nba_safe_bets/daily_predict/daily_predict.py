import pandas as pd
import streamlit as st

from nba_safe_bets.scrapers.nba_player_info import get_player_list
from nba_safe_bets.scrapers.defense_rankings import get_all_defense_rankings
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.schedule_scraper import get_schedule
from nba_safe_bets.scrapers.vegas_odds import get_daily_vegas_lines
from nba_safe_bets.daily_predict.model_loader import load_all_models
from nba_safe_bets.daily_predict.daily_feature_builder import build_features_for_player
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    st.write("### 🔍 DEBUG: Starting Daily Prediction Engine")

    # ---------------------------------------
    # 1. Load Players
    # ---------------------------------------
    players = get_player_list()
    st.write("Players DF Shape:", players.shape)
    st.write(players.head())

    if players.empty:
        st.error("❌ Player list is EMPTY — NBA API returned no data.")
        return []

    # ---------------------------------------
    # 2. Defense Rankings
    # ---------------------------------------
    defense = get_all_defense_rankings()
    st.write("Defense keys:", list(defense.keys()))

    # ---------------------------------------
    # 3. Injury Report
    # ---------------------------------------
    injuries = get_injury_report() or pd.DataFrame()
    st.write("Injury DF Shape:", injuries.shape)

    # ---------------------------------------
    # 4. Schedule
    # ---------------------------------------
    schedule = get_schedule() or pd.DataFrame()
    st.write("Schedule DF Shape:", schedule.shape)

    # ---------------------------------------
    # 5. Vegas Odds
    # ---------------------------------------
    vegas = get_daily_vegas_lines() or pd.DataFrame()
    st.write("Vegas DF Shape:", vegas.shape)

    # ---------------------------------------
    # 6. Load Models
    # ---------------------------------------
    models = load_all_models()
    st.write("Models Loaded:", list(models.keys()))

    # ---------------------------------------
    # 7. Generate Predictions
    # ---------------------------------------
    results = []
    count_features = 0
    count_predictions = 0

    for idx, row in players.iterrows():
        pid = row.get("PLAYER_ID")
        if not pid:
            continue

        features = build_features_for_player(
            player_row=row,
            defense=defense,
            injuries=injuries,
            schedule=schedule,
            vegas=vegas
        )

        if features is None or features.empty:
            continue

        count_features += 1

        prediction_row = {}
        for stat_name, model in models.items():
            try:
                prediction_row[stat_name] = model.predict(features)[0]
            exc
