import requests
import pandas as pd
from nba_safe_bets.utils.retry import safe_request
from nba_safe_bets.utils.logging_config import log

BASE_URL = "https://api.balldontlie.io/v1/season_averages"


def get_season_averages(player_id):
    """
    Returns season averages for a player.
    Returns a DataFrame with columns including pts, reb, ast, fg3m
    """

    params = {"player_ids[]": player_id}

    log(f"[SEASON AVG] Fetching season averages for player {player_id}")

    r = safe_request(BASE_URL, params=params)
    if r is None:
        log(f"[SEASON AVG ERROR] Failed to fetch season averages for {player_id}")
        return pd.DataFrame()

    data = r.json()
    if "data" not in data or len(data["data"]) == 0:
        log(f"[SEASON AVG] No season averages found for {player_id}")
        return pd.DataFrame()

    row = data["data"][0]

    df = pd.DataFrame([{
        "pts": row.get("pts", 0),
        "reb": row.get("reb", 0),
        "ast": row.get("ast", 0),
        "fg3m": row.get("fg3m", 0),
    }])

    return df
