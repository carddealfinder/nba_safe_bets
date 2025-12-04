import streamlit as st
import pandas as pd

from ..daily_predict.daily_predict import daily_predict
from .components.bet_table import render_bet_table
from .components.player_card import render_player_card
from .components.charts import render_bar_chart


def run_dashboard():
    st.title("🔒 Top 25 Safest Bets Today")

    preds = st.session_state.get("predictions")

    if preds is None or preds.empty:
        st.write("No predictions available.")
        return

    render_bet_table(preds)

    st.subheader("📊 Player Profiles")
    for _, row in preds.head(5).iterrows():
        render_player_card(row)
        render_bar_chart(row)
