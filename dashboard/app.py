import streamlit as st
import pandas as pd

from daily_predict.daily_predict import daily_predict
from dashboard.components.bet_table import render_bet_table
from dashboard.components.player_card import render_player_card
from dashboard.components.charts import render_player_charts

st.set_page_config(
    page_title="NBA Safe Bets Dashboard",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")

# Sidebar
st.sidebar.header("Controls")
refresh = st.sidebar.button("🔄 Refresh Predictions")

# Get predictions
if "predictions" not in st.session_state or refresh:
    with st.spinner("Running daily prediction engine..."):
        st.session_state["predictions"] = daily_predict()

df = st.session_state["predictions"]

st.subheader("📊 Top 25 Safest Prop Bets Today")
render_bet_table(df)

# Player selection
player_id = st.selectbox(
    "Select a player to view details:",
    options=df["player"].unique(),
    format_func=lambda x: str(x)
)

player_data = df[df["player"] == player_id]

if len(player_data) > 0:
    st.subheader("👤 Player Breakdown")
    render_player_card(player_data)

    st.subheader("📈 Trends & Charts")
    render_player_charts(player_data)
