# ==========================================
# streamlit_app.py  (Option A - PATH FIX)
# ==========================================

import sys
import os

# --- FIX PYTHON PATH FOR STREAMLIT CLOUD ---
ROOT = os.path.dirname(os.path.abspath(__file__))        # /safe_bets_app
PARENT = os.path.dirname(ROOT)                           # repo root
PACKAGE_ROOT = os.path.join(ROOT, "nba_safe_bets")       # /safe_bets_app/nba_safe_bets

# Add paths if missing
for p in [ROOT, PARENT, PACKAGE_ROOT]:
    if p not in sys.path:
        sys.path.append(p)

# --- STREAMLIT START ---
import streamlit as st
import pandas as pd

from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.charts import render_probability_distribution
from nba_safe_bets.dashboard.components.player_card import render_player_card


# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="NBA Safe Bets AI Engine",
    layout="wide",
    page_icon="🏀"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.caption("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")


# ==========================================
# DEBUG EXPANDER
# ==========================================
debug_expander = st.expander("🔍 DEBUG LOG (click to expand)")
debug_buffer = []


def debug(msg):
    debug_buffer.append(msg)


# ==========================================
# RUN PREDICTION ENGINE BUTTON
# ==========================================
st.divider()
if st.button("🚀 Run Prediction Engine", type="primary"):
    debug("Running daily_predict()...")

    try:
        preds = daily_predict(debug)
        st.session_state["preds"] = preds
        debug("daily_predict() executed successfully.")
    except Exception as e:
        debug(f"❌ daily_predict() crashed: {e}")
        st.error(f"Prediction Engine Error: {e}")
        preds = None

else:
    preds = st.session_state.get("preds", None)
    debug("App initialized. Waiting to run prediction engine.")


# Push logs into UI
debug_expander.write("```\n" + "\n".join(debug_buffer) + "\n```")


# ==========================================
# SAFEST BETS TABLE
# ==========================================
st.subheader("🔒 Top 25 Safest Bets Today")

if preds is None or not isinstance(preds, pd.DataFrame) or preds.empty:
    st.info("No predictions available.")
else:
    render_bet_table(preds)


# ==========================================
# PLAYER PROFILES
# ==========================================
st.subheader("📊 Player Profiles")

if preds is None or preds.empty:
    st.info("Prediction results required to display player profiles.")
else:
    # Pick top 8 players for cards
    top_players = preds.groupby("player").head(1).head(8)

    cols = st.columns(4)
    idx = 0

    for _, row in top_players.iterrows():
        with cols[idx % 4]:
            render_player_card(row)
        idx += 1


# ==========================================
# PROBABILITY DISTRIBUTION CHARTS
# ==========================================
st.subheader("📈 Probability Distributions")

if preds is None or preds.empty:
    st.info("Run predictions to visualize probability curves.")
else:
    render_probability_distribution(preds)
