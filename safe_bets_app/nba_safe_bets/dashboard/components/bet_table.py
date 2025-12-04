import streamlit as st
import pandas as pd

def render_bet_table(df: pd.DataFrame):

    expected_cols = [
        "player", "stat", "line", "final_prob",
        "ml_prob", "weighted_prob", "safety_score"
    ]

    # If DataFrame is empty
    if df is None or df.empty:
        st.warning("No predictions available.")
        return

    # Find missing columns
    missing = [c for c in expected_cols if c not in df.columns]

    # If columns are missing → fallback to simple table
    if missing:
        st.warning(f"Prediction engine ran, but missing expected columns: {missing}")
        st.dataframe(df)
        return

    # Otherwise show the fully formatted table
    df_display = df[expected_cols].copy()

    st.dataframe(
        df_display.style.format({
            "final_prob": "{:.2%}",
            "ml_prob": "{:.2%}",
            "weighted_prob": "{:.2%}",
            "safety_score": "{:.2f}"
        }),
        use_container_width=True
    )
