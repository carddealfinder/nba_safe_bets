import streamlit as st
import pandas as pd
import traceback

# -------------------------------------------------------------------
# Correct absolute imports based on your repo structure
# -------------------------------------------------------------------
from safe_bets_app.nba_safe_bets.daily_predict.daily_predict import daily_predict
from safe_bets_app.nba_safe_bets.dashboard.components.bet_table import render_bet_table
from safe_bets_app.nba_safe_bets.dashboard.components.player_card import render_player_card
from safe_bets_app.nba_safe_bets.dashboard.components.charts import render_charts


# -------------------------------------------------------------------
# DEBUG LOGGING BUFFER
# -------------------------------------------------------------------
debug_logs = []

def log_debug(msg: str):
    """Append a debug message into the UI log buffer."""
    debug_logs.append(msg)


# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")
st.divider()


# -------------------------------------------------------------------
# RUN DAILY PREDICT ENGINE
# -------------------------------------------------------------------
st.write("### Running daily_predict()...")

preds = None

try:
    preds = daily_predict(debug_log_fn=log_debug)
    st.success("daily_predict() executed successfully!")

except Exception as e:
    st.error("Prediction engine failed. See debug logs below.")
    log_debug("--- ERROR ---")
    log_debug(str(e))
    log_debug(traceback.format_exc())


# -------------------------------------------------------------------
# DEBUG LOG VISIBILITY
# -------------------------------------------------------------------
with st.expander("🔍 DEBUG LOG (click to expand)", expanded=False):
    if not debug_logs:
        st.write("No debug logs recorded yet.")
    else:
        for line in debug_logs:
            st.text(line)


# -------------------------------------------------------------------
# VALIDATE PREDICTION DATA
# -------------------------------------------------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

if preds is None:
    st.warning("Prediction engine returned **None** — cannot display results.")
    st.stop()

if not isinstance(preds, pd.DataFrame):
    st.error("daily_predict() did not return a DataFrame.")
    st.stop()

if preds.empty:
    st.warning("No predictions available.")
    st.stop()

# Ensure ranking columns exist
if "confidence" not in preds.columns:
    preds["confidence"] = 0.0

# Trim to top 25
top25 = preds.sort_values("confidence", ascending=False).head(25)
render_bet_table(top25)


# -------------------------------------------------------------------
# PLAYER CARDS
# -------------------------------------------------------------------
st.subheader("📊 Player Profiles")

if "player_name" not in preds.columns:
    st.info("Prediction results missing player_name field — cannot build profiles.")
else:
    for _, row in top25.iterrows():
        render_player_card(row)


# -------------------------------------------------------------------
# CHARTS
# -------------------------------------------------------------------
st.subheader("📈 Analytics & Visualizations")
render_charts(preds)

