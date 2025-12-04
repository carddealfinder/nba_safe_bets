import pandas as pd
from scrapers.nba_player_info import get_player_list
from scrapers.defense_rankings import get_all_defense_rankings
from scrapers.injury_report import get_injury_report
from scrapers.schedule_scraper import get_schedule
from scrapers.vegas_odds import get_daily_vegas_lines
from daily_predict.model_loader import load_all_models
from daily_predict.daily_feature_builder import build_features_for_player
from daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    print("=== START DAILY PREDICTION ENGINE ===")

    # ---------------------------------------------------------
    # 1. Load player list
    # ---------------------------------------------------------
    players = get_player_list()

    print("PLAYER DF COLUMNS:", players.columns.tolist())
    print("PLAYER DF HEAD:\n", players.head())

    if players.empty:
        print("[ERROR] Player list is empty. NBA API failed or was blocked.")
        return []

    # Guarantee PLAYER_ID exists (in case scraper schema changes)
    if "PLAYER_ID" not in players.columns:
        print("[WARNING] PLAYER_ID column missing. Creating fallback column.")
        players["PLAYER_ID"] = None

    # ---------------------------------------------------------
    # 2. Load defense rankings
    # ---------------------------------------------------------
    print("Loading defense rankings...")
    defense = get_all_defense_rankings()

    print("Defense keys loaded:", defense.keys())

    # ---------------------------------------------------------
    # 3. Load injury data
    # ---------------------------------------------------------
    print("Loading injuries...")
    injuries = get_injury_report()
    if injuries is None:
        injuries = pd.DataFrame()
    print("Injury DF columns:", injuries.columns.tolist())

    # ---------------------------------------------------------
    # 4. Load schedule (rest days, back-to-back, opponents)
    # ---------------------------------------------------------
    print("Loading schedule...")
    schedule = get_schedule()
    if schedule is None:
        schedule = pd.DataFrame()
    print("Schedule DF columns:", schedule.columns.tolist())

    # ---------------------------------------------------------
    # 5. Load Vegas lines
    # ---------------------------------------------------------
    print("Loading Vegas odds...")
    vegas = get_daily_vegas_lines()
    if vegas is None:
        vegas = pd.DataFrame()
    print("Vegas DF columns:", vegas.columns.tolist())

    # ---------------------------------------------------------
    # 6. Load trained ML models (points, rebounds, assists, threes)
    # ---------------------------------------------------------
    print("Loading ML models...")
    models = load_all_models()
    print("Loaded models:", list(models.keys()))

    # ---------------------------------------------------------
    # 7. Build features & predictions for each player
    # ---------------------------------------------------------
    results = []
    print("Generating predictions...")

    for idx, row in players.iterrows():
        pid = row.get("PLAYER_ID", None)
        if pid is None:
            continue  # skip invalid rows

        try:
            # Build all contextual features for this player
            features = build_features_for_player(
                player_row=row,
                defense=defense,
                injuries=injuries,
                schedule=schedule,
                vegas=vegas
            )

            # If feature builder returns None → skip
            if features is None or features.empty:
                continue

            # Apply machine learning models
            prediction_row = {}
            for stat_name, model in models.items():
                try:
                    prediction_row[stat_name] = model.predict(features)[0]
                except Exception as e:
                    print(f"[ERROR] Model failed for stat {stat_name}: {e}")
                    prediction_row[stat_name] = None

            prediction_row["PLAYER_ID"] = pid
            prediction_row["PLAYER_NAME"] = row.get("PLAYER_NAME", "Unknown")
            prediction_row["TEAM_ID"] = row.get("TEAM_ID", None)

            results.append(prediction_row)

        except Exception as e:
            print(f"[ERROR] Failed processing player {pid}: {e}")
            continue

    # ---------------------------------------------------------
    # 8. Convert predictions to DataFrame
    # ---------------------------------------------------------
    if not results:
        print("[WARNING] No predictions were generated.")
        return []

    predictions_df = pd.DataFrame(results)
    print("FINAL PREDICTION DF:\n", predictions_df.head())

    # ---------------------------------------------------------
    # 9. Rank safest bets
    # ---------------------------------------------------------
    ranked = rank_safe_bets(predictions_df)

    print("=== END DAILY PREDICTION ENGINE ===")
    return ranked
