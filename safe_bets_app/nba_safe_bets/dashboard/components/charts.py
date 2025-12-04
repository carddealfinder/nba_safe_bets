import streamlit as st
import plotly.express as px
import pandas as pd

def render_player_charts(df):
    fig = px.bar(
        df,
        x="stat",
        y=["weighted_prob", "ml_prob", "final_prob"],
        barmode="group",
        title="Probability Comparison (Weighted vs ML vs Final)",
        labels={"value": "Probability", "stat": "Prop Type"}
    )

    st.plotly_chart(fig, use_container_width=True)
