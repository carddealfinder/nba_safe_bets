import sys, os
import streamlit as st
import pandas as pd

# Add safe_bets_app root to Python path
sys.path.append(os.path.dirname(__file__))

# Now imports work
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(
    page_title="NBA Safest Bets",
    layout="wide",
    page_icon="🏀"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")
st.markdown("---")

# Debug log collector
if "debug_log" not in st.session_state:
    st.session_state["debug_log"] = ""

def log_debug(msg: str):
    st.session_state["debug_log"] += msg + "\n"


# -----------------------------
# Run the Prediction Engine
# -----------------------------
if st.button("🚀 Run Prediction Engine"):
    st.session_state["debug_log"] = ""
    log_debug("Running daily_predict()...")

    try:
        preds = daily_predict(debug_log_fn=log_debug)
        st.session_state["predictions"] = preds
        log_debug("daily_predict() executed successfully.\n")
    except Exception as e:
        log_debug(f"[ERROR] {e}")
        st.error("Prediction engine failed. See debug logs below.")
        preds = None


# Debug log UI
with st.expander("🔍 DEBUG LOG (click to expand)"):
    st.text(st.session_state["debug_log"])


# -----------------------------
# Display Predictions
# -----------------------------
st.markdown("## 🔒 Top 25 Safest Bets Today")

preds = st.session_state.get("predictions", None)

if preds is None or not isinstance(preds, pd.DataFrame) or preds.empty:
    st.warning("No predictions available.")
else:
    try:
        render_bet_table(preds)
    except Exception as e:
        st.error(f"Error displaying bet table: {e}")


# -----------------------------
# Player Profiles
# -----------------------------
st.markdown("---")
st.markdown("## 📊 Player Profiles")

if preds is None or preds.empty:
    st.info("Prediction results required to display player profiles.")
else:
    # Show top 5
    top_players = preds["player"].unique()[:5]

    cols = st.columns(5)
    for i, player in enumerate(top_players):
        with cols[i]:
            row = preds[preds["player"] == player].iloc[0]
            try:
                render_player_card(row)
            except Exception as e:
                st.error(f"Error rendering player card: {e}")
