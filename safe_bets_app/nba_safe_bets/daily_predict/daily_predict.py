import pandas as pd
import streamlit as st

from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_daily_schedule
from nba_safe_bets.scrapers.injury_report import get_injuries
from nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from nba_safe_bets.scrapers.DraftKings_scraper import get_draftkings_odds

from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    st.write("🔍 DEBUG: Starting Daily Prediction Engine")

    # -------------------------
    # 1. LOAD PLAYER LIST
    # -------------------------
    players = get_player_list()
    st.write("Players DF Shape:", players.shape)

    if players.empty:
        st.error("Player list is empty — cannot continue.")
        return None

    # -------------------------
    # 2. LOAD DAILY SCHEDULE
    # -------------------------
    schedule = get_daily_schedule()
    st.write("Schedule DF Shape:", getattr(schedule, 'shape', 'N/A'))

    if isinstance(schedule, list):
        schedule = pd.DataFrame(schedule)

    # -------------------------
    # 3. LOAD INJURY REPORTS
    # -------------------------
    injuries = get_injuries()
    st.write("Injury DF Shape:", injuries.shape)

    # -------------------------
    # 4. DEFENSE RANKINGS
    # -------------------------
    defense = get_defense_rankings()
    st.write("Defense DF Shape:", defense.shape)

    # -------------------------
    # 5. DRAFTKINGS ODDS
    # -------------------------
    dk_odds = get_draftkings_odds()
    st.write("DraftKings Odds Shape:", dk_odds.shape)

    # -------------------------
    # 6. LOAD MODELS
    # -------------------------
    models = load_models()
    st.write("Models Loaded:", list(models.keys()))

    if not models:
        st.error("❌ No models loaded — cannot generate predictions.")
        return None

    # -------------------------
    # 7. GENERATE PREDICTIONS
    # -------------------------

    merged = players.copy()
    merged["projected_score"] = 0.0
    merged["model_name"] = "dummy"

    for model_name, model in models.items():
        preds = model.predict([[0]])  # dummy prediction
        merged.loc[merged.index, "projected_score"] += preds[0]

    # -------------------------
    # 8. RANK SAFE BETS
    # -------------------------
    ranked = rank_safe_bets(merged)

    st.write("Final Prediction DF:")
    st.dataframe(ranked.head())

    return ranked
