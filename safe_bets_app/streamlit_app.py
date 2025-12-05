import os
import sys
import streamlit as st

# --------------------------------------------------------------
#  PATH FIXES FOR LOCAL & STREAMLIT CLOUD
# --------------------------------------------------------------
PACKAGE_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, ".."))

if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

print(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")
print(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

# --------------------------------------------------------------
# IMPORT ENGINE
# --------------------------------------------------------------
try:
    from nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import prediction engine: {e}")
    st.stop()

# --------------------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------------------
st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write("This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day.")

# Get model dir inside repo
MODEL_DIR = os.path.join(PACKAGE_ROOT, "nba_safe_bets", "models", "trained")

if st.button("Run Daily Predictions"):
    st.write("⏳ Running prediction engine… This may take 5–10 seconds.")

    try:
        predictions, merged_df = daily_predict(model_dir=MODEL_DIR)
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        st.stop()

    st.success("✅ Predictions generated!")
    st.dataframe(predictions)

    with st.expander("📊 Raw Feature Data"):
        st.dataframe(merged_df)
