import pandas as pd

from nba_safe_bets.scrapers.nba_player_info import get_player_list
from nba_safe_bets.scrapers.defense_rankings import get_all_defense_rankings
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.schedule_scraper import get_schedule
from nba_safe_bets.scrapers.vegas_odds import get_daily_vegas_lines

from nba_safe_bets.daily_predict.model_loader import load_all_models
from nba_safe_bets.daily_predict.daily_feature_builder import build_features_for_player
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


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

    if "PLAYER_ID" not in players.columns:
        print("[WARNING] PLAYER_ID missing — creating fallback column")
        players["PLAYER_ID"] = None

    # ---------------------------------------------------------
    # 2. Defense rankings
    # ---------------------------------------------------------
    print("Loading defense rankings...")
    defense = get_all_defense_rankings()

    # ---------------------------------------------------------
    # 3. Injuries
    # ---------------------------------------------------------
    injuries = get_injury_report()
    if injuries is None:
        injuries = pd.DataFrame()

    # ---------------------------------------------------------
    # 4. Schedule
    # ---------------------------------------------------------
    schedule = get_schedule()
    if schedule is None:
        schedule = pd.DataFrame()

    # ---------------------------------------------------------
    # 5. Vegas odds
    # ---------------------------------------------------------
    vegas = get_daily_vegas_lines()
    if vegas is None:
        vegas = pd.DataFrame()

    # ---------------------------------------------------------
    # 6. Load ML models
    # ---------------------------------------------------------
    print("Loading models...")
    models = load_all_models()

    # ---------------------------------------------------------
    # 7. Predict per-player
    # ---------------------------------------------------------
    results = []

    for _, row in players.iterrows():
        pid = row.get("PLAYER_ID", None)
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

            if features is None or features.empty:
                continue

            prediction_row = {}
            for stat_name, model in models.items():
                try:
                    prediction_row[stat_name] = model.predict(features)[0]
                except Exception as e:
                    print(f"[ERROR] Model failed for {stat_name}: {e}")
                    prediction_row[stat_name] = None

            prediction_row["PLAYER_ID"] = pid
            prediction_row["PLAYER_NAME"] = row.get("PLAYER_NAME", "Unknown")
            prediction_row["TEAM_ID"] = row.get("TEAM_ID", None)

            results.append(prediction_row)

        except Exception as e:
            print(f"[ERROR] Failed processing player {pid}: {e}")
            continue

    if not results:
        print("[WARNING] No predictions generated.")
        return []

    predictions_df = pd.DataFrame(results)
    return rank_safe_bets(predictions_df)
