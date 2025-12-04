import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.balldontlie.io/v1"

def get_schedule(date=None):
    """Returns today's NBA games from BallDontLie."""
    if date is None:
        date = datetime.today().strftime("%Y-%m-%d")

    url = f"{BASE_URL}/games"
    params = {"dates[]": date, "per_page": 100}

    r = requests.get(url, params=params, timeout=10)
    if r.status_code != 200:
        print("[ERROR] Failed to fetch schedule:", r.text)
        return pd.DataFrame()

    games = r.json().get("data", [])
    if not games:
        print("⚠ No games returned for date:", date)
        return pd.DataFrame()

    df = pd.DataFrame(games)
    return df[["id", "home_team", "visitor_team"]]
