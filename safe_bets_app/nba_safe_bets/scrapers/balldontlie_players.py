import os
import requests
import pandas as pd

BASE_URL = "https://api.balldontlie.io/v1/players"

def get_player_list(per_page=100):
    """Fetch ALL NBA players through the Balldontlie API."""
    key = os.getenv("BALDONTLIE_API_KEY")

    # 🔍 DEBUG: Show whether key exists on Streamlit Cloud
    print(f"[BDL DEBUG] API key loaded? {bool(key)}")
    print(f"[BDL DEBUG] Key length: {len(key) if key else 0}")

    if not key:
        print("[BDL ERROR] Missing BALDONTLIE_API_KEY")
        return pd.DataFrame()

    headers = {"Authorization": f"Bearer {key}"}

    players = []
    page = 1

    print("[BDL] Starting player download...")

    while True:
        print(f"[BDL] Fetching page {page}")

        params = {"page": page, "per_page": per_page}

        try:
            r = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
            r.raise_for_status()
        except Exception as e:
            print(f"[BDL ERROR] Player API request failed: {e}")
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

        # stop if end of pages
        if not data.get("meta", {}).get("has_more", False):
            break

        page += 1

    df = pd.DataFrame(players)
    print(f"[BDL] Loaded players: {df.shape}")
    return df
