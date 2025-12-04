import streamlit as st

# Daily prediction engine
from nba_safe_bets.daily_predict.daily_predict import daily_predict

# UI components
from nba_safe_bets.dashboard.components.bet_table import render_bet_table
from nba_safe_bets.dashboard.components.player_card import render_player_card
from nba_safe_bets.dashboard.components.charts import render_player_charts



# ---------------------------------------------------------
# 🔧 PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="NBA Safe Bets Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏀 NBA Top 25 Safest Bets (Daily Prediction Engine)")
st.caption("Automatically generated predictions based on stats, matchups, injuries, odds, and player context.")


# ---------------------------------------------------------
# 🐞 DEBUG PANEL (Collapsible)
# ---------------------------------------------------------
with st.expander("🔍 DEBUG LOG (click to expand)"):
    if "debug_log" in st.session_state:
        st.text(st.session_state["debug_log"])
    else:
        st.write("App initialized. Waiting to run prediction engine.")


# ---------------------------------------------------------
# 🚀 RUN PREDICTION ENGINE
# ---------------------------------------------------------
run_btn = st.button("⚡ Run Prediction Engine", type="primary")

if run_btn:
    st.session_state["debug_log"] = ""
    st.write("Running daily_predict()...")

    try:
        preds = daily_predict()
        st.session_state["predictions"] = preds
        st.session_state["debug_log"] += "\ndaily_predict() executed successfully.\n"
    except Exception as e:
        st.error("❌ Prediction engine crashed.")
        st.exception(e)
        st.stop()


# ---------------------------------------------------------
# 📊 FETCH PREDICTIONS
# ---------------------------------------------------------
preds = st.session_state.get("predictions")

if preds is not None and isinstance(preds, pd.DataFrame) and not preds.empty:

    # ---------------------------------------------------------
    # 🎛️ SIDEBAR FILTERS
    # ---------------------------------------------------------
    st.sidebar.header("🔎 Filter Safe Bets")

    # Team filter
    teams = sorted(preds["team"].dropna().unique())
    team_filter = st.sidebar.multiselect("Filter by Team:", teams, default=[])

    # Stat Type filter
    stat_types = sorted(preds["stat"].dropna().unique())
    stat_filter = st.sidebar.multiselect("Filter by Stat Type:", stat_types, default=[])

    # Minimum final probability
    min_prob = st.sidebar.slider(
        "Minimum Final Probability (%)",
        min_value=0,
        max_value=100,
        value=60
    ) / 100.0

    # Minimum safety score
    min_safety = st.sidebar.slider(
        "Minimum Safety Score",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        step=0.1
    )

    # ---------------------------------------------------------
    # Apply Filters
    # ---------------------------------------------------------
    filtered = preds.copy()

    if team_filter:
        filtered = filtered[filtered["team"].isin(team_filter)]

    if stat_filter:
        filtered = filtered[filtered["stat"].isin(stat_filter)]

    filtered = filtered[
        (filtered["final_prob"] >= min_prob) &
        (filtered["safety_score"] >= min_safety)
    ]

    st.session_state["filtered_predictions"] = filtered

else:
    st.session_state["filtered_predictions"] = None


# ---------------------------------------------------------
# 🧮 DISPLAY FILTERED BET TABLE
# ---------------------------------------------------------
st.subheader("🔒 Top 25 Safest Bets Today")

filtered_preds = st.session_state.get("filtered_predictions")

if filtered_preds is None or filtered_preds.empty:
    st.warning("No predictions available after applying filters.")
else:
    render_bet_table(filtered_preds.head(25))


# ---------------------------------------------------------
# 🧍 PLAYER PROFILES SECTION
# ---------------------------------------------------------
st.subheader("📊 Player Profiles")

if filtered_preds is None or filtered_preds.empty:
    st.info("Prediction results required to display player profiles.")
    st.stop()

top_n = st.slider("Number of player profiles to show", 5, 25, 10)

top_players = filtered_preds.head(top_n)

cols = st.columns(3)

for i, (_, row) in enumerate(top_players.iterrows()):
    with cols[i % 3]:
        render_player_card(row)

