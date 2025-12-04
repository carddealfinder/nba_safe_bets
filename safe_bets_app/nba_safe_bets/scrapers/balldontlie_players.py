import os
import requests
import pandas as pd

BASE_URL = "https://api.balldontlie.io/v1/players"


def get_player_list(per_page=100):
    """Fetch ALL players from Balldontlie using proper pagination."""

    api_key = os.getenv("BALDONTLIE_API_KEY")

    if not api_key:
        print("[BDL ERROR] No BALDONTLIE_API_KEY environment variable found.")
        return pd.DataFrame()

    # Balldontlie uses query param ?key=API_KEY
    headers = {}  # No Authorization header
    players = []
    page = 1

    print("[BDL] Starting player download...")

    while True:
        print(f"[BDL] Fetching page {page}")

        params = {
            "page": page,
            "per_page": per_page,
            "key": api_key   # ← THIS IS THE FIX
        }

        try:
            r = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"[BDL ERROR] Player API request failed: {e}")
            break

        data = r.json()

        # Extract players
        if "data" not in data or len(data["data"]) == 0:
            print("[BDL] No more player data found.")
            break

        for p in data["data"]:
            players.append({
                "id": p["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "team": p["team"]["full_name"] if p["team"] else None
            })

        # Pagination flag
        meta = data.get("meta", {})
        if not meta.get("has_more", False):
            break

        page += 1

    df = pd.DataFrame(players)
    print(f"[BDL] Loaded players: {df.shape}")
    return df
