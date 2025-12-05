import os
import requests
import pandas as pd

BASE_URL = "https://api.balldontlie.io/v1/players"


def get_player_list(per_page=100):
    """Fetch all player metadata from BallDontLie API."""
    key = os.getenv("BALDONTLIE_API_KEY")

    print(f"[BDL] Key exists? {bool(key)}")

    headers = {"Authorization": f"Bearer {key}"} if key else {}

    players = []
    page = 1

    while True:
        try:
            r = requests.get(
                BASE_URL,
                params={"page": page, "per_page": per_page},
                headers=headers,
                timeout=10
            )
            r.raise_for_status()
        except Exception as e:
            print(f"[BDL ERROR] {e}")
            break

        data = r.json()
        items = data.get("data", [])

        if not items:
            break

        for p in items:
            players.append({
                "id": p["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "team": p.get("team", {}).get("full_name"),
            })

        if not data.get("meta", {}).get("has_more", False):
            break

        page += 1

    df = pd.DataFrame(players)
    print("[BDL] Loaded players:", df.shape)
    return df
