import requests
import pandas as pd


BASE = "https://api.balldontlie.io/v1"
HEADERS = {"Authorization": ""}  # optional free tier key


def get_player_list():
    """
    Loads ALL active + inactive players from BallDontLie.
    BallDontLie returns paginated results, so we loop.
    """

    print("🔍 Using BallDontLie API for players...")

    players = []
    page = 1

    while True:
        url = f"{BASE}/players?page={page}&per_page=100"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            print("[ERROR] Player API failed:", r.text)
            break

        data = r.json()

        players.extend(data["data"])

        if page >= data["meta"]["total_pages"]:
            break

        page += 1

    if not players:
        print("[ERROR] No player data returned.")
        return pd.DataFrame()

    df = pd.DataFrame(players)

    return df[["id", "first_name", "last_name", "team"]].rename(
        columns={"id": "PLAYER_ID"}
    )
