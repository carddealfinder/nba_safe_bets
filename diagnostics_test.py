import os
import pandas as pd

# --- SCRAPERS ---
from safe_bets_app.nba_safe_bets.scrapers.balldontlie_players import get_player_list
from safe_bets_app.nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from safe_bets_app.nba_safe_bets.scrapers.injury_report import get_injury_report
from safe_bets_app.nba_safe_bets.scrapers.defense_rankings import get_defense_rankings
from safe_bets_app.nba_safe_bets.scrapers.nba_game_logs import get_last_n_games
from safe_bets_app.nba_safe_bets.scrapers.nba_player_info import get_season_averages

# --- DAILY FEATURE PIPELINE ---
from safe_bets_app.nba_safe_bets.daily_predict.daily_feature_builder import build_daily_features

# --- MODEL LOADING & PREDICTION ---
from safe_bets_app.nba_safe_bets.daily_predict.model_loader import load_models
from safe_bets_app.nba_safe_bets.daily_predict.safe_bet_ranker import rank_safe_bets


print("\n==============================")
print("🔍 STARTING DIAGNOSTICS TEST")
print("==============================\n")


# --------------------------------------------------------
# 1️⃣ SCRAPER TESTS
# --------------------------------------------------------

print("📌 Testing Scrapers...\n")

players = get_player_list()
print("Players Loaded:", players.shape)

schedule = get_todays_schedule()
print("Today's Schedule Loaded:", schedule.shape)

injuries = get_injury_report()
print("Injury Report Loaded:", injuries.shape)

defense = get_defense_rankings()
print("Defense Rankings Loaded:", defense.shape)

# Test game log scraper
print("\n📌 Testing game logs + season averages...")
if len(players) > 0:
    pid = int(players.iloc[0]["id"])
    logs = get_last_n_games(pid, n=10)
    avg = get_season_averages(pid)
    print(f"Last 10 Logs Shape: {logs.shape}")
    print(f"Season Averages Shape: {avg.shape}")
else:
    print("⚠ No players available to test logs.")


# --------------------------------------------------------
# 2️⃣ FEATURE BUILDING TEST
# --------------------------------------------------------

print("\n📌 Building Daily Features...")

merged = build_daily_features()
print("Merged DF Shape:", merged.shape)
print("\nMerged Columns:", merged.columns.tolist())

required = ["id", "points", "rebounds", "assists", "threes", "injury_factor", "game_id"]

missing = [c for c in required if c not in merged.columns]
if missing:
    print("\n❌ Missing required columns:", missing)
else:
    print("\n✅ All required feature columns present.")

feature_df = merged[required].copy()
print("\nFeature DF Preview:\n", feature_df.head())


# --------------------------------------------------------
# 3️⃣ MODEL LOAD TEST
# --------------------------------------------------------

print("\n📌 Loading Models...\n")

MODEL_DIR = os.path.join(
    os.path.dirname(__file__),
    "safe_bets_app",
    "nba_safe_bets",
    "models",
    "trained"
)

models = load_models(MODEL_DIR)
print("Models Loaded:", list(models.keys()))

if len(models) == 0:
    print("❌ No models loaded — check your trained/ directory.")
else:
    print("✅ Models successfully loaded.\n")


# --------------------------------------------------------
# 4️⃣ PREDICTION TEST
# --------------------------------------------------------

print("📌 Running Prediction Test...")

try:
    preds = rank_safe_bets(feature_df, models)
    print("\nPrediction Output:\n", preds.head())
    print("\n✅ Predictions completed successfully!")

except Exception as e:
    print("\n❌ Prediction engine failed:", e)


print("\n==============================")
print("🎉 DIAGNOSTICS COMPLETE")
print("==============================\n")
