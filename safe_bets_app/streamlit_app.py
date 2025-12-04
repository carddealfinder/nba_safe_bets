import streamlit as st
import pandas as pd

# Import prediction engine
from nba_safe_bets.daily_predict.daily_predict import daily_predict
# UI components
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card

st.set_page_config(page_title="NBA Safe Bets", layout="wide")

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, and trends.")

# ---------------------------------------------------------
# DEBUG PANEL
# ---------------------------------------------------------
debug_expander = st.expander("🔍 DEBUG LOG (click to expand)", expanded=True)
debug_expander.write("App initialized. Waiting to run prediction engine.")

# ---------------------------------------------------------
# Run Prediction Engine
# ---------------------------------------------------------
if st.button("Run Prediction Engine 🚀"):
    debug_expander.write("Running daily_predict()...")

    try:
        preds = daily_predict()
        debug_expander.write("daily_predict() executed successfully.")
        debug_expander.write("RAW OUTPUT:")
        debug_expander.write(preds)
    except Exception as e:
        st.error(f"🔥 Prediction Engine CRASHED: {e}")
        debug_expander.write(f"❌ CRASH: {e}")
        preds = []

else:
    preds = []

# ---------------------------------------------------------
# Display Predictions Table
# ---------------------------------------------------------
st.header("🔒 Top 25 Safest Bets Today")

if isinstance(preds, pd.DataFrame) and not preds.empty:
    render_bet_table(preds)
else:
    st.warning("No predictions available.")

# ---------------------------------------------------------
# Player Profiles — Simple Debug-Friendly Version
# ---------------------------------------------------------
st.header("📊 Player Profiles")

if isinstance(preds, pd.DataFrame) and not preds.empty:
    players = preds["player"].unique()
    selected = st.selectbox("Choose a player", players)

    player_df = preds[preds["player"] == selected]

    try:
        render_player_card(player_df)
    except Exception as e:
        st.error(f"Player card failed: {e}")
else:
    st.info("Prediction results required to display player profiles.")
