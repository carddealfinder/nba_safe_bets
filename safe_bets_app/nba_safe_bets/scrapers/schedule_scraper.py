import requests
import pandas as pd
from datetime import date


def get_todays_schedule():
    today = date.today().isoformat()

    url = "https://api.balldontlie.io/v1/games"
    params = {"dates[]": today}

    r = requests.get(url, params=params)
    if r.status_code != 200:
        return pd.DataFrame(columns=["player_id", "team", "game_id"])

    games = r.json().get("data", [])
    rows = []

    for game in games:
        for player in game.get("players", []):
            rows.append({
                "player_id": player["id"],
                "team": player.get("team"),
                "game_id": game["id"]
            })

    return pd.DataFrame(rows)
