import os
import pandas as pd

from nba_safe_bets.utils.retry import safe_request
from nba_safe_bets.utils.helpers import safe_get

BASE_URL = "https://api.balldontlie.io/v1/stats"


def fetch_game_logs(player_id, per_page=100):
    """Download historical game logs for a player."""
    url = BASE_URL
    headers = {"Authorization": f"Bearer {os.getenv('BALDONTLIE_API_KEY')}"}

    logs = []
    page = 1

    while True:
        params = {
            "player_ids[]": player_id,
            "per_page": per_page,
            "page": page
        }

        resp = safe_request(url, params=params, headers=headers)
        if resp is None:
            break

        data = resp.json()
        entries = data.get("data", [])
        if not entries:
            break

        for g in entries:
            logs.append({
                "player_id": safe_get(g, ["player", "id"]),
                "game_id": safe_get(g, ["game", "id"]),
                "points": safe_get(g, ["pts"]),
                "rebounds": safe_get(g, ["reb"]),
                "assists": safe_get(g, ["ast"]),
                "threes": safe_get(g, ["fg3m"]),
            })

        if not data.get("meta", {}).get("has_more", False):
            break

        page += 1

    return pd.DataFrame(logs)


def build_training_dataset(player_ids):
    """Build dataset for model training."""
    frames = []

    for pid in player_ids:
        df = fetch_game_logs(pid)
        if df is not None and not df.empty:
            frames.append(df)

    if frames:
        return pd.concat(frames, ignore_index=True)

    return pd.DataFrame()
