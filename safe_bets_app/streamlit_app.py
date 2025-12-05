import os
import sys
import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# PATH FIX — Works both locally & on Streamlit Cloud
# -------------------------------------------------------------------

PACKAGE_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, ".."))

if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)
    print(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    print(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

# -------------------------------------------------------------------
# IMPORT PREDICTION ENGINE
# -------------------------------------------------------------------

from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.utils.logging_config import log


# -------------------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------------------

st.set_page_config(page_title="NBA Safe Bets — AI Predictor", layout="wide")

st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write(
    "This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day."
)

st.divider()

# -------------------------------------------------------------------
# RUN ENGINE BUTTON
# -------------------------------------------------------------------

if st.button("🚀 Run Daily Predictor", type="primary"):
    st.write("⏳ Running prediction engine… This may take 5–10 seconds.")

    try:
        results = daily_predict()
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        log(f"[STREAMLIT ERROR] {e}")
        st.stop()

    # -------------------------------------------------------------------
    # RESULTS VALIDATION
    # -------------------------------------------------------------------

    if results is None:
        st.error("❌ Prediction returned no results.")
        st.stop()

    if isinstance(results, dict) and "error" in results:
        st.error(f"❌ Engine Error: {results['error']}")
        st.stop()

    if isinstance(results, pd.DataFrame) and results.empty:
        st.warning("⚠ No ranked bets available — check logs.")
        st.stop()

    # -------------------------------------------------------------------
    # DISPLAY TOP SAFEST BETS
    # -------------------------------------------------------------------

    st.success("🎉 Prediction Complete!")
    st.subheader("🔥 Top Safe Bets Today")

    st.dataframe(
        results.head(25),
        use_container_width=True,
        hide_index=True,
    )

    # -------------------------------------------------------------------
    # OPTIONAL DEBUG SECTION
    # -------------------------------------------------------------------

    with st.expander("🛠 Debug Details"):
        st.write("### Raw Prediction Output")
        st.dataframe(results, use_container_width=True, hide_index=True)


# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------

st.divider()
st.caption("Built with ❤️ using Python, Streamlit, and XGBoost.")
