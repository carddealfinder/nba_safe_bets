import requests
import pandas as pd
from datetime import date

BASE = "https://api.balldontlie.io/v1"


def get_schedule():
    """Loads today's NBA games."""
    today = date.today().isoformat()
    url = f"{BASE}/games?dates[]={today}&per_page=100"

    print("🔍 Fetching schedule from BallDontLie:", today)

    r = requests.get(url)

    if r.status_code != 200:
        print("[ERROR] schedule API:", r.text)
        return pd.DataFrame()

    games = r.json()["data"]

    if not games:
        print("[WARNING] No NBA games today.")
        return pd.DataFrame()

    rows = []
    for g in games:
        rows.append({
            "game_id": g["id"],
            "home_team": g["home_team"]["full_name"],
            "visitor_team": g["visitor_team"]["full_name"],
            "home_team_id": g["home_team"]["id"],
            "visitor_team_id": g["visitor_team"]["id"],
        })

    return pd.DataFrame(rows)
