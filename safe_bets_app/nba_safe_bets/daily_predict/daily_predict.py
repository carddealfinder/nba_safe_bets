import pandas as pd

# Scrapers
from nba_safe_bets.scrapers.nba_player_info import get_player_list
from nba_safe_bets.scrapers.defense_rankings import get_all_defense_rankings
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.schedule_scraper import get_schedule
from nba_safe_bets.scrapers.vegas_odds import get_daily_vegas_lines

# ML + Feature pipeline
from nba_safe_bets.daily_predict.model_loader import load_all_models
from nba_safe_bets.daily_predict.daily_feature_builder import build_features_for_player
from nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


def daily_predict():
    print("🔍 DEBUG: Starting Daily Prediction Engine")

    # ---------------------------------------------------------
    # 1. Load Player List
    # ---------------------------------------------------------
    players = get_player_list()
    print("Players DF Shape:", players.shape)

    if players.empty:
        print("❌ Player list is EMPTY — NBA API returned no data.")
        return pd.DataFrame()

    # Guarantee PLAYER_ID column exists
    if "PLAYER_ID" not in players.columns:
        print("⚠️ PLAYER_ID missing — creating fallback null column.")
        players["PLAYER_ID"] = None

    # ---------------------------------------------------------
    # 2. Load Defense Rankings
    # ---------------------------------------------------------
    print("Loading defense rankings...")
    defense = get_all_defense_rankings()
    print("Defense keys:\n", list(defense.keys()))

    # ---------------------------------------------------------
    # 3. Load Injury Data
    # ---------------------------------------------------------
    print("Loading injuries...")
    injuries = get_injury_report()
    if injuries is None:
        injuries = pd.DataFrame(columns=["PLAYER_ID", "STATUS"])
    print("Injury DF Shape:", injuries.shape)

    # ---------------------------------------------------------
    # 4. Load Schedule
    # ---------------------------------------------------------
    print("Loading schedule...")
    schedule = get_schedule()
    if schedule is None:
        schedule = pd.DataFrame()
    print("Schedule DF Shape:", schedule.shape)

    # ---------------------------------------------------------
    # 5. Load Vegas lines
    # ---------------------------------------------------------
    print("Loading Vegas odds...")
    vegas = get_daily_vegas_lines()
    if vegas is None:
        vegas = pd.DataFrame(columns=["game", "line", "total"])
    print("Vegas DF Shape:", vegas.shape)

    # ---------------------------------------------------------
    # 6. Load ML Models
    # ---------------------------------------------------------
    print("Loading ML models...")
    models = load_all_models()
    print("Models Loaded:", list(models.keys()))

    # ---------------------------------------------------------
    # 7. Feature Building + Predictions
    # ---------------------------------------------------------
    predictions = []
    print("Generating predictions...")

    for idx, row in players.iterrows():

        pid = row.get("PLAYER_ID", None)
        if pid is None:
            continue

        try:
            # Build contextual features
            features = build_features_for_player(
                player_row=row,
                defense=defense,
                injuries=injuries,
                schedule=schedule,
                vegas=vegas
            )

            if features is None or features.empty:
                continue

            # Build prediction row
            pred = {
                "PLAYER_ID": pid,
                "PLAYER_NAME": row.get("PLAYER_NAME", "Unknown"),
                "TEAM_ID": row.get("TEAM_ID", None),
            }

            # Run all ML models
            for stat_name, model in models.items():
                try:
                    pred[stat_name] = float(model.predict(features)[0])
                except Exception as e:
                    print(f"[ERROR] Model failed for {pid} {stat_name}: {e}")
                    pred[stat_name] = None

            predictions.append(pred)

        except Exception as e:
            print(f"[ERROR] Failed on player {pid}: {e}")
            continue

    # ---------------------------------------------------------
    # 8. Convert to DataFrame
    # ---------------------------------------------------------
    if not predictions:
        print("⚠️ No predictions generated.")
        return pd.DataFrame()

    prediction_df = pd.DataFrame(predictions)
    print("Final Prediction DF Shape:", prediction_df.shape)

    # ---------------------------------------------------------
    # 9. Rank safest bets
    # ---------------------------------------------------------
    ranked = rank_safe_bets(prediction_df)
    print("Finished ranking safe bets.")

    return ranked
