import streamlit as st
import pandas as pd
import plotly.express as px

from safe_bets_app.nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts


# =========================================
# DEBUG LOG CAPTURE
# =========================================
debug_messages = []

def log_debug(msg):
    debug_messages.append(str(msg))


# =========================================
# STREAMLIT UI
# =========================================
st.set_page_config(
    page_title="NBA Safe Bets",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")
st.divider()

# -----------------------------
# RUN PREDICTION ENGINE
# -----------------------------
with st.spinner("Running daily_predict()..."):
    try:
        preds = daily_predict(debug_log_fn=log_debug)
        st.success("daily_predict() executed successfully!")
    except Exception as e:
        st.error(f"Prediction engine failed.\n\n{e}")
        st.code(traceback.format_exc())
        preds = None

# -----------------------------
# DEBUG LOG PANEL
# -----------------------------
with st.expander("🔍 DEBUG LOG (click to expand)"):
    if debug_messages:
        for m in debug_messages:
            st.text(m)
    else:
        st.write("No debug logs recorded yet.")

# -----------------------------
# TOP 25 BET OUTPUT
# -----------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

if preds is None or not isinstance(preds, pd.DataFrame) or preds.empty:
    st.warning("No predictions available.")
else:
    render_bet_table(preds)

    # -----------------------------
    # Player Profiles
    # -----------------------------
    st.subheader("📊 Player Profiles")

    for _, row in preds.head(10).iterrows():
        render_player_card(row)

    # -----------------------------
    # Charts
    # -----------------------------
    st.subheader("📈 Visual Insights")
    render_charts(preds)
