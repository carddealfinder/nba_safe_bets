import requests
import pandas as pd
from nba_safe_bets.utils.retry import safe_request
from nba_safe_bets.utils.logging_config import log

BASE_URL = "https://api.balldontlie.io/v1/stats"


def get_last_n_games(player_id, n=10):
    """
    Pulls last N game logs for a player using balldontlie stats endpoint.
    Returns a DataFrame with columns: pts, reb, ast, fg3m
    """

    headers = {}
    api_key = None

    try:
        import os
        api_key = os.getenv("BALDONTLIE_API_KEY")
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}
    except:
        pass

    params = {
        "player_ids[]": player_id,
        "per_page": n,
        "sort": "game.date",     # newest first
    }

    log(f"[GAME LOGS] Fetching last {n} games for player {player_id}")

    r = safe_request(BASE_URL, params=params, headers=headers)
    if r is None:
        log(f"[GAME LOGS ERROR] Failed to load logs for player {player_id}")
        return pd.DataFrame()

    data = r.json()

    if "data" not in data or len(data["data"]) == 0:
        log(f"[GAME LOGS] No game logs for player {player_id}")
        return pd.DataFrame()

    rows = []
    for g in data["data"]:
        rows.append({
            "pts": g.get("pts", 0),
            "reb": g.get("reb", 0),
            "ast": g.get("ast", 0),
            "fg3m": g.get("fg3m", 0),
        })

    return pd.DataFrame(rows)
