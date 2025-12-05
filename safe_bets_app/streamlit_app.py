import os
import sys
import streamlit as st

# ==============================================================
# PATH FIX (runs safely even on Streamlit Cloud)
# ==============================================================
try:
    PACKAGE_ROOT = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, ".."))

    if PACKAGE_ROOT not in sys.path:
        sys.path.append(PACKAGE_ROOT)
    if PROJECT_ROOT not in sys.path:
        sys.path.append(PROJECT_ROOT)

    print(f"[PATH FIX] Added PACKAGE_ROOT: {PACKAGE_ROOT}")
    print(f"[PATH FIX] Added PROJECT_ROOT: {PROJECT_ROOT}")

except Exception as e:
    print(f"[PATH FIX ERROR] {e}")


# ==============================================================
# IMPORT DAILY ENGINE (WITH SAFE WRAPPER)
# ==============================================================
try:
    from safe_bets_app.nba_safe_bets.daily_predict.daily_predict import daily_predict
except Exception as e:
    st.error(f"❌ Failed to import prediction engine: {e}")
    raise


# ==============================================================
# STREAMLIT UI
# ==============================================================
st.set_page_config(page_title="NBA Safe Bets — AI Predictor", layout="wide")

st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write(
    "This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day."
)

st.divider()

# ==============================================================
# RUN ENGINE WHEN USER CLICKS BUTTON
# ==============================================================
if st.button("⚡ Run Predictions"):
    with st.spinner("⏳ Running prediction engine… This may take 5–10 seconds."):

        try:
            results = daily_predict()
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            st.stop()

        # ----------------------------
        # Error from engine
        # ----------------------------
        if results.get("error"):
            st.error(f"❌ {results['error']}")
            st.dataframe(results.get("features", {}))
            st.stop()

        features = results["features"]
        preds = results["predictions"]

        # ----------------------------
        # Display Feature Table
        # ----------------------------
        st.subheader("📊 Feature Dataset (Input to Models)")
        if features is not None and len(features) > 0:
            st.dataframe(features, use_container_width=True)
        else:
            st.warning("⚠ No features were generated.")

        # ----------------------------
        # Display Predictions
        # ----------------------------
        st.subheader("🎯 Model Predictions")
        if preds is not None and len(preds) > 0:
            st.dataframe(preds, use_container_width=True)
        else:
            st.warning("⚠ No predictions were generated. (Likely no models were loaded.)")

        # ----------------------------
        # Show model availability
        # ----------------------------
        model_dir = "safe_bets_app/nba_safe_bets/models/trained"
        if os.path.exists(model_dir):
            model_files = [
                f for f in os.listdir(model_dir) if f.endswith(".json")
            ]
            st.info(f"📦 Models found: {len(model_files)} — {model_files}")
        else:
            st.warning("⚠ Model directory not found. Expected: /models/trained/")


# ==============================================================
# FOOTER
# ==============================================================
st.divider()
st.caption("Powered by NBA Safe Bets — Machine Learning Prediction Engine")
