import requests
import pandas as pd

BASE_URL = "https://api.balldontlie.io/v1"
HEADERS = {"Accept": "application/json"}

def get_player_list():
    """Returns all NBA players (first 500) from BallDontLie."""
    players = []
    page = 1

    while True:
        url = f"{BASE_URL}/players"
        params = {"per_page": 100, "page": page}

        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print("[ERROR] Failed to fetch players:", r.text)
            break

        data = r.json()
        players.extend(data["data"])

        if page >= data["meta"]["total_pages"]:
            break

        page += 1

    if not players:
        print("❌ No player data returned from BallDontLie API")
        return pd.DataFrame()

    df = pd.DataFrame(players)
    df = df.rename(columns={
        "id": "PLAYER_ID",
        "first_name": "first_name",
        "last_name": "last_name",
        "team": "team"
    })

    df["PLAYER_NAME"] = df["first_name"] + " " + df["last_name"]
    df["TEAM_ID"] = df["team"].apply(lambda x: x.get("abbreviation") if isinstance(x, dict) else None)

    return df[["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]]
