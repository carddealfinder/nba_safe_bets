import streamlit as st

from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_charts


def run_dashboard(df):
    st.header("📊 NBA Safe Bets Dashboard")

    render_charts(df)

    st.subheader("🔒 High-Confidence Bets")
    render_bet_table(df)

    st.subheader("🧍 Player Profiles")
    render_player_card(df)
