import streamlit as st
import pandas as pd
import traceback

# --- ABSOLUTE IMPORTS FOR STREAMLIT CLOUD ---
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts


st.set_page_config(
    page_title="NBA Safe Bets",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Storage for logs
if "debug_logs" not in st.session_state:
    st.session_state["debug_logs"] = []


def log(msg):
    """Append message to the debug log."""
    st.session_state["debug_logs"].append(str(msg))


# -------------------------------------------------------------------
# PAGE HEADER
# -------------------------------------------------------------------
st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")
st.divider()


# -------------------------------------------------------------------
# RUN ENGINE
# -------------------------------------------------------------------
if st.button("🚀 Run Prediction Engine"):
    st.session_state["debug_logs"].clear()

    try:
        st.write("Running daily_predict()...")
        preds = daily_predict()   # No extra args!

        st.session_state["predictions"] = preds
        st.success("daily_predict() executed successfully!")

    except Exception as e:
        st.error("Prediction engine failed.")
        log("ENGINE ERROR:\n" + traceback.format_exc())
        st.session_state["predictions"] = pd.DataFrame()


# -------------------------------------------------------------------
# DEBUG LOG PANEL
# -------------------------------------------------------------------
with st.expander("🔍 DEBUG LOG (click to expand)"):
    if st.session_state["debug_logs"]:
        for line in st.session_state["debug_logs"]:
            st.text(line)
    else:
        st.write("No debug logs recorded yet.")


# -------------------------------------------------------------------
# PROCESS RESULTS
# -------------------------------------------------------------------
preds = st.session_state.get("predictions", pd.DataFrame())

st.divider()
st.header("🔒 Top 25 Safest Bets Today")

if preds is None or preds.empty or not isinstance(preds, pd.DataFrame):
    st.warning("No predictions available.")
else:
    render_bet_table(preds)

    # -------------------------------------------------------------------
    # CHARTS
    # -------------------------------------------------------------------
    st.divider()
    st.header("📈 Visualization")
    try:
        render_charts(preds)
    except Exception as e:
        st.error("Failed to render charts.")
        log("CHART ERROR:\n" + traceback.format_exc())

    # -------------------------------------------------------------------
    # PLAYER PROFILES
    # -------------------------------------------------------------------
    st.divider()
    st.header("📊 Player Profiles")

    try:
        for _, row in preds.iterrows():
            render_player_card(row)
    except Exception as e:
        st.error("Failed to render player cards.")
        log("CARD ERROR:\n" + traceback.format_exc())
