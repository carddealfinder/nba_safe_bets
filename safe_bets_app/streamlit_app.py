import os
import sys
import streamlit as st

# --------------------------------------------------------------------
# PATH FIXES FOR BOTH LOCAL + STREAMLIT CLOUD
# --------------------------------------------------------------------
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PACKAGE_ROOT)

if PACKAGE_ROOT not in sys.path:
    sys.path.append(PACKAGE_ROOT)
    print(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    print(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

# --------------------------------------------------------------------
# IMPORT DAILY ENGINE
# --------------------------------------------------------------------
try:
    from nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import prediction engine: {e}")
    raise

# --------------------------------------------------------------------
# STREAMLIT UI
# --------------------------------------------------------------------
st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write(
    "This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day."
)

if st.button("Run Prediction Engine"):
    st.info("⏳ Running prediction engine… This may take 5–10 seconds.")

    try:
        result = daily_predict()

        if result is None:
            st.error("❌ Prediction failed — engine returned None")
        else:
            predictions, merged_df, feature_df = result

            if predictions is None or len(predictions) == 0:
                st.warning("⚠ Prediction engine returned no results.")
            else:
                st.success("✅ Predictions Generated!")
                st.dataframe(predictions)

            with st.expander("Debug Info — Merged DataFrame"):
                st.dataframe(merged_df)

            with st.expander("Debug Info — Feature DataFrame"):
                st.dataframe(feature_df)

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
