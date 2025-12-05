import pandas as pd
import numpy as np

from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.injury_report import get_injury_report
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.nba_game_logs import get_last_n_games, get_season_averages


# -----------------------------
# HYBRID FEATURE BUILDER (A3)
# -----------------------------
def get_player_stats_hybrid(player_id, last_n=10):
    """
    Returns last-10-game averages when possible; 
    otherwise season averages.
    """

    # Try last N games first
    logs = get_last_n_games(player_id, n=last_n)
    if logs is not None and not logs.empty:
        return {
            "points": logs["pts"].mean(),
            "rebounds": logs["reb"].mean(),
            "assists": logs["ast"].mean(),
            "threes": logs["fg3m"].mean(),
        }

    # Fallback: season averages
    s_avg = get_season_averages(player_id)
    if s_avg is not None and not s_avg.empty:
        row = s_avg.iloc[0]
        return {
            "points": row.get("pts", 0),
            "rebounds": row.get("reb", 0),
            "assists": row.get("ast", 0),
            "threes": row.get("fg3m", 0),
        }

    # Fallback: zeros
    return {
        "points": 0,
        "rebounds": 0,
        "assists": 0,
        "threes": 0,
    }


# -----------------------------
# MAIN FEATURE BUILDER
# -----------------------------
def build_daily_features():
    print("\n[FEATURE BUILDER] Starting daily feature build...")

    # 1️⃣ Players
    players_df = get_player_list()
    if players_df.empty:
        print("[FEATURE BUILDER] ERROR — No players loaded.")
        return pd.DataFrame()

    # 2️⃣ Schedule
    schedule_df = get_todays_schedule()
    schedule_df = schedule_df.rename(columns={"id": "game_id"})

    # Map player teams → today's matching game_id
    schedule_map = {}
    for _, row in schedule_df.iterrows():
        schedule_map[row["home_team"]] = row["game_id"]
        schedule_map[row["visitor_team"]] = row["game_id"]

    players_df["game_id"] = players_df["team"].map(schedule_map).fillna(0).astype(int)

    # 3️⃣ Injury Report
    injury_df = get_injury_report()
    injury_df = injury_df.rename(columns={"player_id": "id"}) if not injury_df.empty else pd.DataFrame()

    players_df = players_df.merge(injury_df[["id", "status"]] if not injury_df.empty else pd.DataFrame(),
                                  on="id", how="left")

    players_df["injury_factor"] = players_df["status"].notna().astype(int)

    # 4️⃣ Stats for each player (Hybrid method)
    stat_rows = []
    print("[FEATURE BUILDER] Fetching stats for each player...")

    for _, row in players_df.iterrows():
        stats = get_player_stats_hybrid(row["id"])
        stat_rows.append({
            "id": row["id"],
            "game_id": row["game_id"],
            "injury_factor": row["injury_factor"],
            **stats
        })

    feature_df = pd.DataFrame(stat_rows)

    # Ensure final column order
    feature_df = feature_df[
        ["id", "points", "rebounds", "assists", "threes", "injury_factor", "game_id"]
    ]

    print("[FEATURE BUILDER] Final Feature Shape:", feature_df.shape)
    print(feature_df.head())

    return feature_df
