import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# Correct import path now that nba_safe_bets is a package
# ---------------------------------------------------------
from nba_safe_bets.daily_predict.daily_predict import daily_predict

# ---------------------------------------------------------
# Streamlit Page Settings
# ---------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets - AI Prediction Engine",
    layout="wide",
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.caption("Powered by matchup data, injuries, rest days, defense rankings, and ML models.")
st.divider()

# ---------------------------------------------------------
# Run Prediction Engine (Once Only)
# ---------------------------------------------------------
if "predictions" not in st.session_state:

    with st.spinner("Running prediction engine... this may take 20–40 seconds ⏳"):
        try:
            preds = daily_predict()
            st.session_state["predictions"] = preds
        except Exception as e:
            st.error("❌ Prediction engine failed. Check logs in Streamlit Cloud.")
            st.write(e)
            st.stop()

# Load from session
preds = st.session_state.get("predictions")

# ---------------------------------------------------------
# Validate Predictions
# ---------------------------------------------------------
if preds is None or len(preds) == 0:
    st.error("No predictions available.")
    st.stop()

# Ensure DataFrame
if not isinstance(preds, pd.DataFrame):
    preds = pd.DataFrame(preds)

# ---------------------------------------------------------
# Ranking Logic (ensure confidence exists)
# ---------------------------------------------------------
if "confidence" not in preds.columns:
    try:
        preds["confidence"] = preds.mean(axis=1, numeric_only=True)
    except Exception:
        preds["confidence"] = 0

preds = preds.sort_values("confidence", ascending=False).reset_index(drop=True)
preds.index = preds.index + 1  # Make ranking start at 1

# ---------------------------------------------------------
# Display Top 25 Safest Bets
# ---------------------------------------------------------
st.subheader("🔒 Safest Bets Today (Top 25)")
st.dataframe(preds, use_container_width=True, hide_index=False)

st.divider()

# ---------------------------------------------------------
# Raw Debug Data
# ---------------------------------------------------------
with st.expander("🔍 Raw Prediction Output (Debug)"):
    st.write(preds)
