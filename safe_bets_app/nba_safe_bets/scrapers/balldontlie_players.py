import os
import requests
import pandas as pd

BASE_URL = "https://api.balldontlie.io/v1/players"


def get_player_list(per_page=100):
    key = os.getenv("BALDONTLIE_API_KEY")

    print(f"[BDL] Key exists? {bool(key)}")

    headers = {"Authorization": key}  # ✔ Correct Balldontlie header

    page = 1
    players = []

    while True:
        try:
            r = requests.get(
                BASE_URL,
                params={"per_page": per_page, "page": page},
                headers=headers,
                timeout=10
            )
            r.raise_for_status()
        except Exception as e:
            print(f"[BDL ERROR] Failed on page {page}: {e}")
            break

        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            break

        for p in data["data"]:
            players.append({
                "id": p["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "team": p["team"]["full_name"] if p.get("team") else None
            })

        if not data.get("meta", {}).get("next_page"):
            break

        page += 1

    df = pd.DataFrame(players)
    return df
