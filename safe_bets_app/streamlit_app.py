import streamlit as st

# Correct imports for nested package structure
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_player_charts

st.set_page_config(page_title="NBA Safest Bets", layout="wide")

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.write("Automatically generated predictions based on stats, matchups, injuries, and trends.")

# Button to manually run prediction engine
if st.button("Run Prediction Engine"):
    st.session_state["predictions"] = daily_predict()

# If predictions exist, show them
if "predictions" in st.session_state:
    preds = st.session_state["predictions"]

    # Convert list → DataFrame if needed
    import pandas as pd
    if isinstance(preds, list):
        preds = pd.DataFrame(preds)

    st.subheader("🔒 Top 25 Safest Bets Today")
    render_bet_table(preds)

    st.subheader("📊 Player Profiles")
    for _, row in preds.head(5).iterrows():
        render_player_card(row)
        render_player_charts(row)

else:
    st.info("Click **Run Prediction Engine** to generate predictions.")

