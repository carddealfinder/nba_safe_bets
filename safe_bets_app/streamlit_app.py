# ============================================================================
# Fix Python path so that 'nba_safe_bets' package is importable everywhere
# ============================================================================
import os, sys

# Path to directory containing THIS file:
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to directory containing the package "nba_safe_bets"
PACKAGE_ROOT = CURRENT_DIR   # because streamlit_app.py sits inside safe_bets_app/

if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)
    print("[PATH FIX] Added PACKAGE_ROOT to sys.path:", PACKAGE_ROOT)

import os
import streamlit as st
import pandas as pd

# Daily prediction engine
from nba_safe_bets.daily_predict.daily_predict import daily_predict
from nba_safe_bets.daily_predict.model_loader import load_models
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets
from nba_safe_bets.daily_predict.daily_feature_builder import build_daily_features

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets",
    page_icon="🏀",
    layout="wide",
)

st.title("🏀 NBA Safe Bets — AI Daily Predictor")
st.write("This app scrapes NBA data, builds features, loads ML models, and ranks the safest prop bets of the day.")


# ------------------------------------------------------------
# MODEL DIRECTORY
# ------------------------------------------------------------
MODEL_DIR = os.path.join(
    os.path.dirname(__file__),
    "nba_safe_bets",
    "models",
    "trained"
)


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Controls")
    run_prediction = st.button("🔮 Run Daily Prediction")
    show_debug = st.checkbox("Show Debug Output", value=False)
    st.markdown("---")
    st.caption("Models loaded from:")
    st.code(MODEL_DIR)


# ------------------------------------------------------------
# MAIN LOGIC
# ------------------------------------------------------------

def run_engine():
    """Executes the entire prediction pipeline with UI feedback."""

    st.subheader("⏳ Building Daily Features...")

    try:
        merged = build_daily_features()
        st.success(f"Features built! Shape: {merged.shape}")
    except Exception as e:
        st.error(f"❌ Failed to build features: {e}")
        return None, None, None

    required_cols = ["id", "points", "rebounds", "assists", "threes", "injury_factor", "game_id"]
    missing = [c for c in required_cols if c not in merged.columns]

    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        if show_debug:
            st.write(merged.head())
        return None, None, None

    feature_df = merged[required_cols].copy()

    st.subheader("📦 Loading Models...")

    try:
        models = load_models(MODEL_DIR)
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None, feature_df, None

    if len(models) == 0:
        st.error("❌ No models found!")
        return None, feature_df, None

    st.success(f"Loaded models: {list(models.keys())}")

    st.subheader("🔮 Generating Predictions...")

    try:
        preds = rank_safe_bets(feature_df, models)
        st.success("Predictions generated!")
        return preds, feature_df, merged

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
        return None, feature_df, merged



# ------------------------------------------------------------
# EXECUTE WHEN BUTTON CLICKED
# ------------------------------------------------------------
if run_prediction:
    with st.spinner("Running daily engine..."):
        preds, features, merged = run_engine()

    if preds is not None:
        st.subheader("🏆 Safe Bet Rankings")
        st.dataframe(preds, use_container_width=True)

    if show_debug:
        st.subheader("🛠 Debug Info")
        st.write("Merged DF:", merged.head() if merged is not None else "None")
        st.write("Feature DF:", features.head() if features is not None else "None")
else:
    st.info("Click **Run Daily Prediction** to generate today's recommended prop picks.")


# End of streamlit_app.py
