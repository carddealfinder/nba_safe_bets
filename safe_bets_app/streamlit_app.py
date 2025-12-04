import streamlit as st
import pandas as pd

# --- Imports from your package ---
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.charts import render_charts
from nba_safe_bets.dashboard.components.player_card import render_player_card

# -------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------
st.set_page_config(
    page_title="NBA Top 25 Safest Bets",
    layout="wide"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.caption("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")

# -------------------------------------------------
# Debug Log Collection
# -------------------------------------------------
debug_messages = []

def append_debug(msg: str):
    """Callback to collect logs for UI display."""
    debug_messages.append(str(msg))

# -------------------------------------------------
# Run Prediction Button
# -------------------------------------------------
if st.button("🔮 Run Prediction Engine"):
    st.write("Running daily_predict()...")

    try:
        preds, debug_output = daily_predict(debug_log_fn=append_debug)
    except TypeError as e:
        st.error("Prediction engine failed. daily_predict() signature mismatch.")
        st.code(str(e))
        preds = None
        debug_output = []

    # Add internal logs collected from debug_log_fn
    debug_messages.extend(debug_output if isinstance(debug_output, list) else [])

    # Display Debug Logs
    with st.expander("🔍 DEBUG LOG (click to expand)", expanded=False):
        for line in debug_messages:
            st.text(line)

    # -------------------------------------------------
    # Predictions Table
    # -------------------------------------------------
    st.header("🔒 Top 25 Safest Bets Today")

    if preds is None or not isinstance(preds, pd.DataFrame) or preds.empty:
        st.warning("No predictions available.")
    else:
        preds = preds.head(25)
        render_bet_table(preds)

    # -------------------------------------------------
    # Player Profiles
    # -------------------------------------------------
    st.header("📊 Player Profiles")

    if preds is None or preds.empty:
        st.info("Prediction results required to display player profiles.")
    else:
        for _, row in preds.iterrows():
            render_player_card(row)

# -------------------------------------------------
# Initial State View Before Running
# -------------------------------------------------
else:
    st.info("Click **Run Prediction Engine** to generate today's safest NBA bets.")
