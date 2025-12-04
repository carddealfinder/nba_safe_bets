import streamlit as st
import pandas as pd
import traceback

# -------------------------------------------------------------------
# Correct imports for Streamlit Cloud (must include safe_bets_app)
# -------------------------------------------------------------------
from safe_bets_app.nba_safe_bets.daily_predict.daily_predict import daily_predict
from safe_bets_app.nba_safe_bets.dashboard.components.bet_table import render_bet_table
from safe_bets_app.nba_safe_bets.dashboard.components.player_card import render_player_card
from safe_bets_app.nba_safe_bets.dashboard.components.charts import render_charts

# -------------------------------------------------------------------
# PAGE SETUP
# -------------------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bet Engine",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")

debug_logs = []


def log_debug(msg):
    debug_logs.append(msg)


# -------------------------------------------------------------------
# RUN PREDICTIONS
# -------------------------------------------------------------------
st.subheader("Running daily_predict()...")

try:
    preds = daily_predict(debug_log_fn=log_debug)
    st.success("daily_predict() executed successfully!")
except Exception as e:
    st.error(f"Prediction engine failed.\n\n{e}")
    debug_logs.append(traceback.format_exc())
    preds = None

# -------------------------------------------------------------------
# DEBUG LOG DISPLAY
# -------------------------------------------------------------------
with st.expander("🔍 DEBUG LOG (click to expand)"):
    if debug_logs:
        for line in debug_logs:
            st.text(line)
    else:
        st.text("No debug logs recorded yet.")

# -------------------------------------------------------------------
# RESULTS
# -------------------------------------------------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

if preds is None or not isinstance(preds, pd.DataFrame) or preds.empty:
    st.warning("No predictions available.")
else:
    st.success("Predictions generated!")
    render_bet_table(preds.head(25))

# -------------------------------------------------------------------
# PLAYER PROFILES
# -------------------------------------------------------------------
st.subheader("📊 Player Profiles")

if preds is None or preds.empty:
    st.info("Prediction results required to display player profiles.")
else:
    render_player_card(preds)
