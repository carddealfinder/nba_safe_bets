import pandas as pd
from utils.logging_config import log
from scrapers.nba_player_info import get_player_list
from scrapers.nba_game_logs import get_player_game_logs
from scrapers.defense_rankings import get_all_defense_rankings
from scrapers.injury_report import get_injury_report
from scrapers.vegas_odds import get_vegas_odds
from scrapers.schedule_scraper import get_schedule

from daily_predict.model_loader import load_all_models
from daily_predict.daily_feature_builder import build_daily_features
from daily_predict.safe_bet_ranker import compute_final_probability, compute_safety_score, rank_safest_props


def daily_predict():
    log.info("🚀 Running daily NBA prediction engine...")

    # 1. Context data
    defense = get_all_defense_rankings()
    injuries = get_injury_report()
    vegas = get_vegas_odds(api_key="YOUR_API_KEY_HERE")
    schedule = get_schedule()

    # 2. Players
    players = get_player_list("2024-25")

    # 3. Get last 20 games for each player
    logs = []
    for pid in players["PLAYER_ID"]:
        df = get_player_game_logs(pid, "2024-25")
        if len(df) > 0:
            logs.append(df.tail(20))

    if not logs:
        log.error("No game logs found for today.")
        return

    df = pd.concat(logs, ignore_index=True)

    # 4. Build features
    df, X = build_daily_features(df, defense, injuries, vegas, schedule)

    # 5. Load ML models
    models = load_all_models()
    results = []

    # 6. Predict each prop-line
    for key, model in models.items():
        stat, line = key.split("_")

        ml_prob = model.predict_proba(X)[:, 1]
        weighted = df[f"prob_{stat}"]

        final_prob = compute_final_probability(weighted, ml_prob)

        # compute safety score
        for i, row in df.iterrows():
            score = compute_safety_score(
                final_prob[i],
                row["PTS_std"],           # consistency proxy
                row["MIN_last10"],        # minutes stability
                row["DEF_VS_POINTS"]      # matchup difficulty proxy
            )

            results.append({
                "player": row["PLAYER_ID"],
                "stat": stat,
                "line": line,
                "ml_prob": ml_prob[i],
                "weighted_prob": weighted[i],
                "final_prob": final_prob[i],
                "safety_score": score
            })

    # 7. Get Top 25 safest bets today
    top25 = rank_safest_props(results)
    log.info("🎉 TOP 25 SAFEST BETS GENERATED!")
    print(top25)

    return top25


if __name__ == "__main__":
    daily_predict()
