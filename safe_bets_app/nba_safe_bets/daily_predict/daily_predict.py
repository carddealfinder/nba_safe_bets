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

    # ---------------------------------------
    # 1. Load Players
    # ---------------------------------------
    players = get_player_list()
    print("Players DF Shape:", players.shape)

    if players.empty:
        print("ERROR: Player list is EMPTY")
        return []

    # ---------------------------------------
    # 2. Defense Rankings
    # ---------------------------------------
    defense = get_all_defense_rankings()
    print("Defense keys:", defense.keys())

    # ---------------------------------------
    # 3. Injuries
    # ---------------------------------------
    injuries = get_injury_report() or pd.DataFrame()
    print("Injury DF Shape:", injuries.shape)

    # ---------------------------------------
    # 4. Schedule
    # ---------------------------------------
    schedule = get_schedule() or pd.DataFrame()
    print("Schedule DF Shape:", schedule.shape)

    # ---------------------------------------
    # 5. Vegas
    # ---------------------------------------
    vegas = get_daily_vegas_lines() or pd.DataFrame()
    print("Vegas DF Shape:", vegas.shape)

    # ---------------------------------------
    # 6. Models
    # ---------------------------------------
    models = load_all_models()
    print("Models Loaded:", list(models.keys()))

    # ---------------------------------------
    # 7. Generate Predictions
    # ---------------------------------------
    results = []
    count_features = 0
    count_predictions = 0

    for idx, row in players.iterrows():
        pid = row.get("PLAYER_ID")
        if not pid:
            continue

        features = build_features_for_player(
            player_row=row,
            defense=defense,
            injuries=injuries,
            schedule=schedule,
            vegas=vegas
        )

        if features is None or features.empty:
            continue

        count_features += 1

        prediction_row = {}
        for stat_name, model in models.items():
            try:
                prediction_row[stat_name] = model.predict(features)[0]
            except Exception as e:
                print(f"[MODEL ERROR] Player {pid}, stat {stat_name}: {e}")
                prediction_row[stat_name] = None

        prediction_row["PLAYER_ID"] = pid
        prediction_row["PLAYER_NAME"] = row.get("PLAYER_NAME")
        prediction_row["TEAM_ID"] = row.get("TEAM_ID")

        results.append(prediction_row)
        count_predictions += 1

    print("Players with built features:", count_features)
    print("Players with predictions:", count_predictions)

    if count_predictions == 0:
        print("ERROR: No predictions were created.")
        return []

    predictions_df = pd.DataFrame(results)
    print("Predictions DF Shape:", predictions_df.shape)

    ranked = rank_safe_bets(predictions_df)
    print("Ranked Output Type:", type(ranked))

    print("=== END PREDICTION ENGINE ===")
    return ranked
