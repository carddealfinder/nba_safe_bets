import os
import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.balldontlie.io/v1/games"


def get_daily_schedule():
    """Retrieve today's NBA schedule using proper authenticated API request."""
    
    api_key = os.getenv("BALDONTLIE_API_KEY")
    if not api_key:
        print("[SCHEDULE ERROR] Missing BALDONTLIE_API_KEY environment variable")
        return pd.DataFrame()

    headers = {"Authorization": f"Bearer {api_key}"}

    today = datetime.now().strftime("%Y-%m-%d")

    params = {
        "start_date": today,
        "end_date": today,
        "per_page": 100
    }

    print(f"[SCHEDULE] Fetching schedule for {today}")

    try:
        r = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[SCHEDULE ERROR] {e}")
        return pd.DataFrame()

    data = r.json().get("data", [])

    if not data:
        print("[SCHEDULE] API returned 0 games.")
        return pd.DataFrame()

    rows = []

    for g in data:
        home = g["home_team"]["full_name"]
        away = g["visitor_team"]["full_name"]

        rows.append({
            "game_id": g["id"],
            "team": home,
            "opponent": away
        })
        rows.append({
            "game_id": g["id"],
            "team": away,
            "opponent": home
        })

    df = pd.DataFrame(rows)
    print("[SCHEDULE] Loaded games:", df.shape)

    return df
