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
# MAIN DAILY ENGINE
# ---------------------------------------------------------
def daily_predict():
    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # ---------------------------------------------------------
    # 1. Load player list
    # ---------------------------------------------------------
    players = get_player_list()

    print("Players DF Shape:", players.shape)

    if players is None or players.empty:
        print("❌ Player list EMPTY — NBA API returned no data")
        return []

    # Guarantee schema consistency
    if "PLAYER_ID" not in players.columns:
        print("⚠️ PLAYER_ID missing — generating fallback IDs")
        players["PLAYER_ID"] = range(len(players))

    if "PLAYER_NAME" not in players.columns:
        players["PLAYER_NAME"] = "Unknown Player"

    # ---------------------------------------------------------
    # 2. Load defense rankings
    # ---------------------------------------------------------
    defense = get_all_defense_rankings()
    print("Defense keys:", list(defense.keys()))

    # ---------------------------------------------------------
    # 3. Load injuries
    # ---------------------------------------------------------
    injuries = get_injury_report()
    if injuries is None or not isinstance(injuries, pd.DataFrame):
        print("⚠️ Injury report invalid — using empty DataFrame")
        injuries = pd.DataFrame(columns=["PLAYER_ID", "INJURY", "STATUS"])

    print("Injury DF Shape:", injuries.shape)

    # ---------------------------------------------------------
    # 4. Load schedule (back-to-back, travel, opponent)
    # ---------------------------------------------------------
    schedule = get_schedule()

    if schedule is None:
        print("⚠️ Schedule scraper returned None — using empty DataFrame")
        schedule = pd.DataFrame()

    elif not isinstance(schedule, pd.DataFrame):
        print(f"⚠️ Schedule type invalid ({type(schedule)}). Converting to DataFrame...")
        try:
            schedule = pd.DataFrame(schedule)
        except Exception:
            schedule = pd.DataFrame()

    print("Schedule DF Shape:", schedule.shape)

    # ---------------------------------------------------------
    # 5. Load Vegas odds
    # ---------------------------------------------------------
    vegas = get_daily_vegas_lines()

    if vegas is None or not isinstance(vegas, pd.DataFrame):
        print("⚠️ Vegas odds invalid — using empty DataFrame")
        vegas = pd.DataFrame(columns=["game", "line", "total"])

    print("Vegas DF Shape:", vegas.shape)

    # ---------------------------------------------------------
    # 6. Load trained ML models
    # ---------------------------------------------------------
    models = load_all_models()
    print("Models loaded:", list(models.keys()))

    # ---------------------------------------------------------
    # 7. Generate predictions for every player
    # ---------------------------------------------------------
    results = []
    print("🔧 Generating predictions...")

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

            # Skip if no features were built
            if features is None or not isinstance(features, pd.DataFrame) or features.empty:
                continue

            prediction_row = {
                "PLAYER_ID": pid,
                "PLAYER_NAME": row.get("PLAYER_NAME", "Unknown"),
                "TEAM_ID": row.get("TEAM_ID", None),
            }

            # Apply ML models
            for stat_name, model in models.items():
                try:
                    prediction_row[stat_name] = model.predict(features)[0]
                except Exception as e:
                    print(f"⚠️ Model failed for {stat_name}: {e}")
                    prediction_row[stat_name] = None

            results.append(prediction_row)

        except Exception as e:
            print(f"❌ Error processing player {pid}: {e}")
            continue

    # ---------------------------------------------------------
    # 8. Convert to DataFrame
    # ---------------------------------------------------------
    if not results:
        print("⚠️ No predictions generated.")
        return []

    predictions_df = pd.DataFrame(results)
    print("Final Prediction DF Head:")
    print(predictions_df.head())

    # ---------------------------------------------------------
    # 9. Compute safest bet rankings
    # ---------------------------------------------------------
    ranked = rank_safe_bets(predictions_df)

    print("🏆 Ranking complete!")
    return ranked
