import os
import sys
import streamlit as st

# --------------------------------------------------------------------
# FIX: Ensure project root is always importable (local + Streamlit Cloud)
# --------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# --------------------------------------------------------------------
# NOW imports work the same everywhere
# --------------------------------------------------------------------
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts

# --------------------------------------------------------------------
# PAGE SETUP
# --------------------------------------------------------------------
st.set_page_config(page_title="NBA Safe Bets", layout="wide")
st.title("🏀 NBA Safe Bets — Daily Prediction Engine")


# --------------------------------------------------------------------
# RUN PREDICTIONS
# --------------------------------------------------------------------
try:
    predictions, players_df = daily_predict()
except Exception as e:
    st.error(f"❌ Prediction engine crashed: {e}")
    st.stop()


# --------------------------------------------------------------------
# SHOW RESULTS
# --------------------------------------------------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

if predictions is None or predictions.empty:
    st.warning("⚠ No predictions available.")
else:
    render_bet_table(predictions)


# --------------------------------------------------------------------
# PLAYER PROFILES
# --------------------------------------------------------------------
st.subheader("📊 Player Profiles")

if predictions is None or predictions.empty:
    st.info("Run predictions to load player profiles.")
else:
    render_player_card(predictions, players_df)
