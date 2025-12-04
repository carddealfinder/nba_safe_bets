import pandas as pd
import streamlit as st

# Scrapers
from nba_safe_bets.scrapers.nba_player_info import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.defense_rankings import get_all_defense_rankings


# Feature builder
from nba_safe_bets.daily_predict.daily_feature_builder import build_features_for_player

# Model loader
from nba_safe_bets.daily_predict.model_loader import load_all_models


def daily_predict():

    st.write("🔍 DEBUG: Starting Daily Prediction Engine")

    # 1. Players
    players = get_player_list()
    st.write("Players DF Shape:", players.shape)

    if players.empty:
        st.error("Player list is empty — cannot continue.")
        return pd.DataFrame()

    # 2. Defense
    defense = get_all_defense_rankings()
    st.write("Defense keys:", list(defense.keys()))

    # 3. Injuries
    injuries = get_injury_report()
    st.write("Injury DF Shape:", injuries.shape)

    # 4. Schedule
    schedule = get_schedule()
    st.write("Schedule DF Shape:", schedule.shape)

    # 5. Vegas odds
    vegas = get_daily_vegas_lines()
    if isinstance(vegas, list):
        vegas = pd.DataFrame(vegas)
    st.write("Vegas DF Shape:", vegas.shape)

    # 6. Load ML models
    models = load_all_models()
    st.write("Models Loaded:", list(models.keys()))

    # If no models exist → we fallback to baseline scoring
    use_models = len(models) > 0

    # ============================================================================
    # 7. Generate Feature Rows
    # ============================================================================
    feature_rows = []

    for _, row in players.iterrows():
        f = build_features_for_player(row, defense, injuries, schedule)
        feature_rows.append(f)

    feature_df = pd.concat(feature_rows, ignore_index=True)
    st.write("Feature DF Shape:", feature_df.shape)

    # ============================================================================
    # 8. Make Predictions
    # ============================================================================

    results = []

    for _, f_row in feature_df.iterrows():

        # For REAL models
        if use_models:
            pred_points = models["points_model"].predict([[f_row["recent_points_avg"]]])[0]
            pred_reb = models["rebounds_model"].predict([[f_row["recent_rebounds_avg"]]])[0]
            pred_ast = models["assists_model"].predict([[f_row["recent_assists_avg"]]])[0]
            pred_3pt = models["threes_model"].predict([[f_row["recent_threes_avg"]]])[0]
        else:
            # Synthetic probabilities until real models are trained
            pred_points = f_row["recent_points_avg"] / 30
            pred_reb = f_row["recent_rebounds_avg"] / 15
            pred_ast = f_row["recent_assists_avg"] / 12
            pred_3pt = f_row["recent_threes_avg"] / 8

        # Add predictions
        results.append({
            "player": f_row["PLAYER_ID"],
            "stat": "points",
            "line": 20.5,
            "final_prob": pred_points,
            "ml_prob": pred_points * 0.9,
            "weighted_prob": pred_points * 0.8,
            "safety_score": pred_points * 100,
        })

    result_df = pd.DataFrame(results)
    st.write("Final Prediction DF Head:", result_df.head())

    return result_df.sort_values("safety_score", ascending=False).head(25)
