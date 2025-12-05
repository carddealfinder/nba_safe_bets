import os
import requests
import pandas as pd


BASE_URL = "https://api.balldontlie.io/v1/players"


def get_player_list():
    key = os.getenv("BALDONTLIE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"} if key else {}

    players = []
    page = 1

    while True:
        r = requests.get(BASE_URL, params={"page": page, "per_page": 100}, headers=headers)
        if r.status_code != 200:
            break

        data = r.json().get("data", [])
        if not data:
            break

        for p in data:
            players.append({
                "player_id": p["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "team": p["team"]["full_name"] if p.get("team") else None
            })

        meta = r.json().get("meta", {})
        if not meta.get("has_more"):
            break
        page += 1

    return pd.DataFrame(players)
