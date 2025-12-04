import streamlit as st
import pandas as pd

# Correct import path for Streamlit Cloud
from daily_predict.daily_predict import daily_predict

st.set_page_config(
    page_title="NBA Safe Bets - AI Prediction Engine",
    layout="wide"
)

# -------------------------------
# TITLE
# -------------------------------
st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.caption("Powered by machine learning, matchup data, injuries, rest, defense rankings, and Vegas odds.")

st.divider()

# -------------------------------
# RUN PREDICTIONS (ONE-TIME)
# -------------------------------
if "predictions" not in st.session_state:

    with st.spinner("Running daily prediction engine... this may take up to 20–40 seconds ⏳"):
        try:
            preds = daily_predict()
            st.session_state["predictions"] = preds
        except Exception as e:
            st.error("❌ Prediction engine failed. Check logs in Streamlit Cloud.")
            st.stop()

# Load stored predictions
preds = st.session_state.get("predictions", None)

# -------------------------------
# DISPLAY RESULTS
# -------------------------------
if preds is None or len(preds) == 0:
    st.error("No predictions were generated today. Data source or model may be missing.")
    st.stop()

st.subheader("🔒 Safest Prop Bets Today")
st.write("Ranked using historical volatility, matchup strength, injury context, rest disadvantage, and ML model consistency.")

# Ensure DataFrame
if not isinstance(preds, pd.DataFrame):
    preds = pd.DataFrame(preds)

# Add ranking column if missing
if "confidence" not in preds.columns:
    preds["confidence"] = preds.mean(axis=1, numeric_only=True)

preds = preds.sort_values("confidence", ascending=False).reset_index(drop=True)
preds.index = preds.index + 1  # rank starting at 1

st.dataframe(
    preds,
    use_container_width=True,
    hide_index=False
)

st.divider()

# -------------------------------
# RAW DATA (Optional Toggle)
# -------------------------------
with st.expander("🔍 View Raw Prediction Output (Debug)"):
    st.write(preds)
