import os
import sys
import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# FIX PYTHON PATH FOR STREAMLIT CLOUD + LOCAL DEV
# -------------------------------------------------------------------
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_ROOT)

if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

st.write(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")
st.write(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

# -------------------------------------------------------------------
# IMPORT DAILY PREDICTION ENGINE
# -------------------------------------------------------------------
try:
    from nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import daily_predict: {e}")
    st.stop()

# -------------------------------------------------------------------
# PAGE UI SETUP
# -------------------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets — AI Predictor",
    layout="wide"
)

st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write("This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day.")

# -------------------------------------------------------------------
# RUN PREDICTION ENGINE ON DEMAND
# -------------------------------------------------------------------
if st.button("🔮 Run Daily Prediction Now"):
    st.info("⏳ Running prediction engine… This may take 5–10 seconds.")

    try:
        results = daily_predict()

        if results is None or isinstance(results, str):
            st.error(f"❌ Prediction failed: {results}")
            st.stop()

        if isinstance(results, pd.DataFrame):
            st.success("✅ Predictions ready!")
            st.write(results)
        else:
            st.warning("⚠ Prediction engine returned no DataFrame. Check logs.")
            st.write(results)

    except Exception as e:
        st.error(f"❌ Prediction engine crashed: {e}")

# -------------------------------------------------------------------
# DEBUG PANEL
# -------------------------------------------------------------------
with st.expander("🛠 Debug Output"):
    st.code("Prediction engine imports successful and UI ready.")

