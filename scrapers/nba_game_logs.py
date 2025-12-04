import requests
import pandas as pd
import time
from utils.retry import safe_request

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
}

def get_player_game_logs(player_id, season):
    """
    Fetch game logs for a single player in a specific season.
    """
    url = "https://stats.nba.com/stats/playergamelog"
    params = {
        "PlayerID": player_id,
        "Season": season,
        "SeasonType": "Regular Season"
    }

    data = safe_request(url, params=params, headers=HEADERS)
    if data is None:
        return pd.DataFrame()

    rows = data["resultSets"][0]["rowSet"]
    headers = data["resultSets"][0]["headers"]

    df = pd.DataFrame(rows, columns=headers)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    df["PLAYER_ID"] = player_id
    df["SEASON"] = season

    return df
