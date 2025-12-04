import streamlit as st
import pandas as pd

def render_bet_table(df):
    df_display = df[[
        "player", "stat", "line", "final_prob", "ml_prob", 
        "weighted_prob", "safety_score"
    ]].copy()

    df_display["final_prob"] = df_display["final_prob"].round(3)
    df_display["ml_prob"] = df_display["ml_prob"].round(3)
    df_display["weighted_prob"] = df_display["weighted_prob"].round(3)
    df_display["safety_score"] = df_display["safety_score"].round(1)

    st.dataframe(
        df_display,
        use_container_width=True,
        height=600
    )
