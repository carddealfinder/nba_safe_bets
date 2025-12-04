import pandas as pd
import streamlit as st

from nba_safe_bets.scrapers.nba_player_info import get_player_list
from nba_safe_bets.scrapers.defense_rankings import get_all_defense_rankings
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.schedule_scraper import get_schedule
from nba_safe_bets.scrapers.vegas_odds import get_daily_vegas_lines

from nba_safe_bets.daily_predict.model_loader import load_all_models
from nba_safe_bets.daily_predict.daily_feature_builder import build_features_for_player
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


# ---------------------------------------------------------
# MAIN PREDICTION ENGINE
# ---------------------------------------------------------
def daily_predict():
    print("\n================ DAILY_PREDICT START ================\n")
    st.write("🔍 DEBUG: Entered daily_predict()")

    # ---------------------------------------------------------
    # 1. LOAD PLAYER LIST
    # ---------------------------------------------------------
    players = get_player_list()
    st.write("Players DF Shape:", players.shape)

    if players is None or players.empty:
        st.error("❌ Player list is EMPTY — NBA API returned nothing")
        return pd.DataFrame()

    if "PLAYER_ID" not in players.columns:
        players["PLAYER_ID"] = range(len(players))

    if "PLAYER_NAME" not in players.columns:
        players["PLAYER_NAME"] = "Unknown"

    # ---------------------------------------------------------
    # 2. LOAD DEFENSE RANKINGS
    # ---------------------------------------------------------
    defense = get_all_defense_rankings()
    st.write("Defense keys:", list(defense.keys()))

    # ---------------------------------------------------------
    # 3. LOAD INJURY REPORT
    # ---------------------------------------------------------
    injuries = get_injury_report()
    if injuries is None or not isinstance(injuries, pd.DataFrame):
        st.warning("⚠ Injury report invalid — using empty DF")
        injuries = pd.DataFrame(columns=["PLAYER_ID", "STATUS"])

    st.write("Injury DF Shape:", injuries.shape)

    # ---------------------------------------------------------
    # 4. LOAD SCHEDULE
    # ---------------------------------------------------------
    schedule = get_schedule()

    if schedule is None:
        st.warning("⚠ Schedule returned None — converting to empty DF")
        schedule = pd.DataFrame()

    elif not isinstance(schedule, pd.DataFrame):
        st.warning(f"⚠ Schedule type = {type(schedule)} — converting")
        try:
            schedule = pd.DataFrame(schedule)
        except:
            schedule = pd.DataFrame()

    st.write("Schedule DF Shape:", schedule.shape)

    # ---------------------------------------------------------
    # 5. LOAD VEGAS ODDS
    # ---------------------------------------------------------
    vegas = get_daily_vegas_lines()

    if vegas is None or not isinstance(vegas, pd.DataFrame):
        st.warning("⚠ Vegas odds invalid — using empty DF")
        vegas = pd.DataFrame(columns=["game", "line", "total"])

    st.write("Vegas DF Shape:", vegas.shape)

    # ---------------------------------------------------------
    # 6. LOAD MODELS
    # ---------------------------------------------------------
    models = load_all_models()
    st.write("Models Loaded:", list(models.keys()))

    # ---------------------------------------------------------
    # 7. GENERATE PREDICTIONS
    # ---------------------------------------------------------
    results = []

    st.write("🔧 Generating predictions...")

    for idx, row in players.iterrows():

        pid = row.get("PLAYER_ID")
        if pid is None:
            continue

        try:
            features = build_features_for_player(
                player_row=row,
                defense=defense,
                injuries=injuries,
                schedule=schedule,
                vegas=vegas
            )

            if features is None or not isinstance(features, pd.DataFrame) or features.empty:
                continue

            prediction_row = {
                "PLAYER_ID": pid,
                "PLAYER_NAME": row.get("PLAYER_NAME", "Unknown"),
                "TEAM_ID": row.get("TEAM_ID"),
            }

            for stat_name, model in models.items():
                try:
                    prediction_row[stat_name] = model.predict(features)[0]
                except Exception as e:
                    print(f"Model failure for {stat_name}: {e}")
                    prediction_row[stat_name] = None

            results.append(prediction_row)

        except Exception as e:
            print(f"Player error {pid}: {e}")
            continue

    # ---------------------------------------------------------
    # 8. BUILD PREDICTION DATAFRAME
    # ---------------------------------------------------------
    if not results:
        st.warning("⚠ No predictions generated.")
        return pd.DataFrame()

    predictions_df = pd.DataFrame(results)
    st.write("Final Prediction DF:", predictions_df.head())

    # ---------------------------------------------------------
    # 9. RANK SAFEST BETS
    # ---------------------------------------------------------
    ranked = rank_safe_bets(predictions_df)
    st.write("Ranked bets:", ranked.head() if not ranked.empty else "empty")

    print("\n================ DAILY_PREDICT END ================\n")

    return ranked
