import requests
import pandas as pd
import os

def get_daily_vegas_lines(api_key=None):
    # Allow env var override
    if api_key is None:
        api_key = os.getenv("ODDS_API_KEY")

    if not api_key:
        print("[WARNING] No Odds API key found. Returning empty Vegas data.")
        return pd.DataFrame(columns=["game", "line", "total"])

    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

    params = {
        "apiKey": api_key,
        "regions": "us",
        "markets": "spreads,totals"
    }

    try:
        r = requests.get(url, params=params)
        if r.status_code != 200:
            print("[ERROR] Vegas API error:", r.text)
            return pd.DataFrame(columns=["game", "line", "total"])

        data = r.json()
        return pd.DataFrame(data)

    except Exception as e:
        print("[ERROR] Failed to fetch Vegas odds:", e)
        return pd.DataFrame(columns=["game", "line", "total"])
