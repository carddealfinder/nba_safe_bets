import os
import sys
import streamlit as st

PACKAGE_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, ".."))

if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import prediction engine: {e}")
    st.stop()

st.title("🏀 NBA Safe Bets — AI Daily Predictor")

MODEL_DIR = os.path.join(PACKAGE_ROOT, "nba_safe_bets", "models", "trained")

if st.button("Run Daily Predictions"):
    st.write("⏳ Running prediction engine…")

    try:
        predictions, merged = daily_predict(model_dir=MODEL_DIR)
        st.success("Done!")
        st.dataframe(predictions)

        with st.expander("Raw Features"):
            st.dataframe(merged)

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
