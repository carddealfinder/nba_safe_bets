import os
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.balldontlie.io/v1/games"


def get_todays_schedule():
    key = os.getenv("BALDONTLIE_API_KEY")
    headers = {"Authorization": key}

    today = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"[SCHEDULE] Fetching schedule for {today}")

    try:
        r = requests.get(
            BASE_URL,
            params={"dates[]": today, "per_page": 100},
            headers=headers,
            timeout=10
        )
        r.raise_for_status()
        data = r.json()

        if "data" not in data:
            return pd.DataFrame(columns=["game_id", "home_team", "away_team"])

        games = [{
            "game_id": g["id"],
            "home_team": g["home_team"]["full_name"],
            "away_team": g["visitor_team"]["full_name"]
        } for g in data["data"]]

        return pd.DataFrame(games)

    except Exception as e:
        print(f"[SCHEDULE ERROR] {e}")
        return pd.DataFrame(columns=["game_id", "home_team", "away_team"])
