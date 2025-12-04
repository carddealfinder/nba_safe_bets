import os
import requests
import pandas as pd

# Debug print to verify Streamlit Cloud sees the secret
print("🔍 DEBUG: BALDONTLIE_API_KEY from env:", os.getenv("BALDONTLIE_API_KEY"))

API_KEY = os.getenv("BALDONTLIE_API_KEY")
BASE_URL = "https://api.balldontlie.io/v1/players"


def get_player_list(per_page=100):
    """Fetches full NBA player list from BallDontLie API."""
    
    if not API_KEY:
        print("[BDL ERROR] Missing BALDONTLIE_API_KEY")
        return pd.DataFrame()

    players = []
    page = 1

    while True:
        print(f"[BDL] Fetching page {page}")

        try:
            resp = requests.get(
                BASE_URL,
                params={"page": page, "per_page": per_page},
                headers={"Authorization": API_KEY},
                timeout=10,
            )
            resp.raise_for_status()
        except Exception as e:
            print(f"[BDL ERROR] Player request failed: {e}")
            break

        data = resp.json()

        if "data" not in data or len(data["data"]) == 0:
            break

        players.extend(data["data"])
        page += 1

        if page > data.get("meta", {}).get("total_pages", 1):
            break

    if not players:
        print("[BDL] Loaded players: (0,0)")
        return pd.DataFrame()

    df = pd.DataFrame(players)

    df = df[["id", "first_name", "last_name", "team"]]
    df["team"] = df["team"].apply(lambda t: t.get("full_name") if isinstance(t, dict) else None)

    print(f"[BDL] Loaded players: {df.shape}")

    return df
