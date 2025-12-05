import os
import sys
import streamlit as st

# ------------------------------------------------------------
# FIX IMPORTS: add project root to sys.path
# ------------------------------------------------------------
APP_ROOT = os.path.dirname(os.path.abspath(__file__))      # safe_bets_app/
PROJECT_ROOT = os.path.dirname(APP_ROOT)                   # nba_safe_bets/

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ------------------------------------------------------------
# Correct imports
# ------------------------------------------------------------
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts


# ------------------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------------------
st.set_page_config(page_title="NBA Safest Bets", layout="wide")

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and model outputs.")


# ------------------------------------------------------------
# RUN PREDICTION ENGINE
# ------------------------------------------------------------
try:
    results, debug_log = daily_predict()

    with st.expander("🔍 DEBUG LOG"):
        st.text(debug_log)

    if results is None or results.empty:
        st.error("⚠ No predictions available.")
    else:
        st.success("Predictions generated successfully!")
        render_bet_table(results)

except Exception as e:
    st.error(f"❌ Prediction engine crashed: {e}")
