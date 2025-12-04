import requests
import pandas as pd
from datetime import datetime


BASE_URL = "https://api.balldontlie.io/v1/games"


def get_daily_schedule():
    """Retrieve today's NBA schedule."""
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        r = requests.get(BASE_URL, params={"dates[]": today, "per_page": 100}, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[SCHEDULE ERROR] {e}")
        return pd.DataFrame()

    data = r.json().get("data", [])
    rows = []

    for g in data:
        rows.append({
            "game_id": g["id"],
            "team": g["home_team"]["full_name"],
            "opponent": g["visitor_team"]["full_name"]
        })
        rows.append({
            "game_id": g["id"],
            "team": g["visitor_team"]["full_name"],
            "opponent": g["home_team"]["full_name"]
        })

    return pd.DataFrame(rows)
