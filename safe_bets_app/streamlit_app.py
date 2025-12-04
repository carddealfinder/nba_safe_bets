import streamlit as st
import pandas as pd

# Import prediction engine
from nba_safe_bets.daily_predict.daily_predict import daily_predict

# Dashboard components
from nba_safe_bets.nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.nba_safe_bets.dashboard.components.charts import render_player_charts


# =====================================================================
# STREAMLIT UI SETUP
# =====================================================================

st.set_page_config(
    page_title="NBA Safe Bets",
    layout="wide",
    page_icon="🏀"
)

st.title("🏀 NBA Top 25 Safest Bets")
st.caption("Automated predictions using DraftKings props, injuries, matchup context & ML models.")

# ---------------------------------------------------------------------
# RUN PREDICTION ENGINE
# ---------------------------------------------------------------------

if st.button("🔮 Run Prediction Engine"):
    st.session_state["predictions"] = daily_predict()


# If nothing has been run yet → show placeholder
if "predictions" not in st.session_state:
    st.info("Click **Run Prediction Engine** to generate today's safest bets.")
    st.stop()

preds = st.session_state["predictions"]

# If output is empty → display clean message
if preds is None or len(preds) == 0 or not isinstance(preds, pd.DataFrame):
    st.warning("No predictions available. Try again later.")
    st.stop()


# =====================================================================
# 1. DISPLAY TOP 25 SAFE BETS
# =====================================================================

st.subheader("🔒 Top 25 Safest Bets Today")

try:
    render_bet_table(preds.head(25))
except Exception as e:
    st.error(f"Error rendering bet table: {e}")


# =====================================================================
# 2. PLAYER DETAIL CARDS + CHARTS
# =====================================================================

st.subheader("📊 Player Profiles")

top_players = preds.head(5)

for _, row in top_players.iterrows():
    try:
        render_player_card(row)
        render_player_charts(row)
        st.markdown("---")
    except Exception as e:
        st.error(f"Could not render player card: {e}")


# =====================================================================
# DEBUG PANEL (COLLAPSIBLE)
# =====================================================================

with st.expander("🔍 DEBUG LOG"):
    try:
        st.write("### Raw Prediction Data")
        st.dataframe(preds)
    except Exception as e:
        st.error(f"Debug log unavailable: {e}")
