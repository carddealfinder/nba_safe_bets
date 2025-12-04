import os
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logging_config import log

# Scrapers
from scrapers.nba_player_info import get_player_list
from scrapers.nba_game_logs import get_player_game_logs
from scrapers.defense_rankings import get_all_defense_rankings
from scrapers.injury_report import get_injury_report
from scrapers.vegas_odds import get_vegas_odds
from scrapers.schedule_scraper import get_schedule

# Processors
from processors.feature_builder import add_rolling_features
from processors.label_builder import add_prop_labels
from processors.context_features import add_context_features
from processors.weighted_model import compute_weighted_probabilities

# Utils
from utils.helpers import safe_merge


# ------------------------------------------------------
# 1. Ensure folder structure
# ------------------------------------------------------
def create_folders():
    folders = [
        "data", 
        "data/raw", 
        "data/processed", 
        "scrapers",
        "processors",
        "utils",
        "models"
    ]
    for f in folders:
        os.makedirs(f, exist_ok=True)
    log.info("✔ All folders verified/created.")


# ------------------------------------------------------
# 2. Fetch all player IDs for a season
# ------------------------------------------------------
def fetch_all_players():
    players = get_player_list("2024-25")
    players = players[["PLAYER_ID", "PLAYER_NAME"]]
    log.info(f"✔ Retrieved {len(players)} active players.")
    return players


# ------------------------------------------------------
# 3. Multi-threaded scraping of player logs per season
# ------------------------------------------------------
def scrape_season_logs(season, players):
    log.info(f"📘 Starting scraping for season {season}...")

    results = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {
            executor.submit(get_player_game_logs, pid, season): pid
            for pid in players["PLAYER_ID"]
        }

        for future in as_completed(futures):
            pid = futures[future]
            try:
                df = future.result()
                if not df.empty:
                    results.append(df)
            except Exception as e:
                log.error(f"Error fetching logs for player {pid}: {e}")

    if results:
        logs_df = pd.concat(results, ignore_index=True)
        save_path = f"data/raw/logs_{season.replace('-', '_')}.parquet"
        logs_df.to_parquet(save_path)
        log.info(f"✔ Saved raw logs for {season} → {save_path}")
        return logs_df

    log.warning(f"⚠ No logs scraped for season {season}")
    return pd.DataFrame()


# ------------------------------------------------------
# 4. Merge all seasons into one dataset
# ------------------------------------------------------
def merge_all_seasons():
    seasons = ["2022-23", "2023-24", "2024-25"]
    dfs = []

    for s in seasons:
        path = f"data/raw/logs_{s.replace('-', '_')}.parquet"
        if os.path.exists(path):
            df = pd.read_parquet(path)
            dfs.append(df)

    if not dfs:
        log.error("❌ No season logs found.")
        return pd.DataFrame()

    combined = pd.concat(dfs, ignore_index=True)
    log.info(f"✔ Merged {len(combined)} total player-game rows across seasons.")
    return combined


# ------------------------------------------------------
# 5. Clean + standardize columns
# ------------------------------------------------------
def clean_logs(df):
    rename_map = {
        "MATCHUP": "MATCHUP",
        "MIN": "MINUTES",
        "FG3M": "FG3M",
        "REB": "REB",
        "AST": "AST",
        "PTS": "PTS"
    }

    df.rename(columns=rename_map, inplace=True)
    return df


# ------------------------------------------------------
# 6. Apply processors
# ------------------------------------------------------
def build_features(df):
    log.info("📊 Adding rolling features...")
    df = add_rolling_features(df)

    log.info("📊 Adding weighted baseline probabilities...")
    df = compute_weighted_probabilities(df)

    return df


# ------------------------------------------------------
# 7. Apply context (injuries, defense, schedule, vegas)
# ------------------------------------------------------
def add_context(df):
    log.info("📚 Loading context data...")

    defense = get_all_defense_rankings()
    injuries = get_injury_report()
    vegas = get_vegas_odds(api_key="YOUR_API_KEY_HERE")  # Optional
    schedule = get_schedule()

    log.info("📊 Merging context features...")
    df = add_context_features(df, defense, injuries, vegas, schedule)

    return df


# ------------------------------------------------------
# 8. Add labels (alternate totals)
# ------------------------------------------------------
def add_labels(df):
    log.info("🏷 Adding alt-line labels...")
    df = add_prop_labels(df)
    return df


# ------------------------------------------------------
# 9. Save final dataset
# ------------------------------------------------------
def save_final_dataset(df):
    path = "data/processed/training_dataset.parquet"
    df.to_parquet(path)
    log.info(f"✔ Final training dataset saved → {path}")


# ------------------------------------------------------
# MASTER FUNCTION
# ------------------------------------------------------
def build_training_dataset():
    log.info("🚀 Starting full training dataset builder...")

    create_folders()

    # Step 1: Get players
    players = fetch_all_players()

    # Step 2: Scrape logs for each season
    for season in ["2022-23", "2023-24", "2024-25"]:
        scrape_season_logs(season, players)

    # Step 3: Merge seasons
    df = merge_all_seasons()

    if df.empty:
        log.error("❌ No data to process — exiting.")
        return

    # Step 4: Clean logs
    df = clean_logs(df)

    # Step 5: Build rolling + weighted features
    df = build_features(df)

    # Step 6: Add contextual features
    df = add_context(df)

    # Step 7: Add alt-line labels
    df = add_labels(df)

    # Step 8: Save final dataset
    save_final_dataset(df)

    log.info("🎉 TRAINING DATASET BUILD COMPLETE!")


# ------------------------------------------------------
# Run script
# ------------------------------------------------------
if __name__ == "__main__":
    build_training_dataset()
