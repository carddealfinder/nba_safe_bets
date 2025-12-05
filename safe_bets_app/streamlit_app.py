import os
import sys
import streamlit as st

# ----------------------------------------------------------
# PATH FIXES — ALWAYS SAFE FOR STREAMLIT CLOUD
# ----------------------------------------------------------
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT))

if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

st.write(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")
st.write(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

# ----------------------------------------------------------
# IMPORT DAILY ENGINE (Safe Import Wrapper)
# ----------------------------------------------------------
try:
    from nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import prediction engine: {e}")
    raise


# ----------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------
st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.caption("This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day.")


# ----------------------------------------------------------
# RUN ENGINE
# ----------------------------------------------------------
st.subheader("⏳ Running prediction engine… This may take 5–10 seconds.")

try:
    merged_df, feature_df, ranked_df = daily_predict()
except Exception as e:
    st.error(f"❌ Prediction failed: {e}")
    st.stop()


# ----------------------------------------------------------
# DISPLAY RESULTS
# ----------------------------------------------------------
st.success("✨ Predictions completed successfully!")

st.subheader("📌 Full Merged Feature Data")
st.dataframe(merged_df, use_container_width=True)

st.subheader("📊 Model Features")
st.dataframe(feature_df, use_container_width=True)

st.subheader("🏆 Ranked Safe Bets")
st.dataframe(ranked_df, use_container_width=True)

