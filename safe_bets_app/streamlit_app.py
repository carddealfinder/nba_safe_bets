import streamlit as st
import pandas as pd
import traceback

# --- ABSOLUTE IMPORTS FOR STREAMLIT CLOUD ---
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts


# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets",
    layout="wide",
    page_icon="🏀"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")


# ----------------------------------------------------
# DEBUG LOG CAPTURE
# ----------------------------------------------------
debug_messages = []

def log_debug(msg):
    """Collect messages that daily_predict() will send back."""
    debug_messages.append(str(msg))


# ----------------------------------------------------
# RUN ENGINE BUTTON
# ----------------------------------------------------
if "predictions" not in st.session_state:
    st.session_state["predictions"] = None

if st.button("🔄 Run Prediction Engine"):
    st.write("Running daily_predict()...")

    try:
        preds = daily_predict(debug_log_fn=log_debug)
        st.session_state["predictions"] = preds
        st.success("daily_predict() executed successfully!")

    except Exception as e:
        st.error("Prediction engine failed.")
        st.code(traceback.format_exc())


preds = st.session_state.get("predictions", None)


# ----------------------------------------------------
# DEBUG LOG SECTION
# ----------------------------------------------------
with st.expander("🔍 DEBUG LOG (click to expand)"):
    if len(debug_messages) == 0:
        st.write("No debug logs recorded yet.")
    else:
        for line in debug_messages:
            st.text(line)


# ----------------------------------------------------
# TOP 25 SAFE BETS — SAFE CHECKS ADDED
# ----------------------------------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

if (
    preds is None
    or not isinstance(preds, pd.DataFrame)
    or preds.empty
):
    st.write("No predictions available.")
else:
    render_bet_table(preds)


# ----------------------------------------------------
# PLAYER PROFILES
# ----------------------------------------------------
st.subheader("📊 Player Profiles")

if (
    preds is None
    or not isinstance(preds, pd.DataFrame)
    or preds.empty
):
    st.write("Prediction results required to display player profiles.")
else:
    # Show top 5 players only
    top_players = preds.head(5)

    for _, row in top_players.iterrows():
        render_player_card(row)


# ----------------------------------------------------
# CHARTS (Only shown if predictions exist)
# ----------------------------------------------------
if (
    preds is not None
    and isinstance(preds, pd.DataFrame)
    and not preds.empty
):
    st.subheader("📈 Prediction Charts Overview")
    render_charts(preds)
