import requests
import pandas as pd
from datetime import datetime


def get_todays_schedule():
    """Returns dataframe of today's NBA games."""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[SCHEDULE] Fetching schedule for {today}")

    url = f"https://api.balldontlie.io/v1/games?dates[]={today}"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("data", [])
    except Exception as e:
        print(f"[SCHEDULE ERROR] {e}")
        return pd.DataFrame(columns=["team", "opponent", "game_id"])

    rows = []

    for g in data:
        home = g["home_team"]["full_name"]
        away = g["visitor_team"]["full_name"]
        game_id = g["id"]

        rows.append({"team": home, "opponent": away, "game_id": game_id})
        rows.append({"team": away, "opponent": home, "game_id": game_id})

    df = pd.DataFrame(rows)
    print("[SCHEDULE] Loaded games:", df.shape)
    return df
