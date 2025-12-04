import requests
import pandas as pd
from nba_safe_bets.utils.retry import safe_request   # ✅ FIXED IMPORT

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_player_list(season="2024-25"):
    url = "https://stats.nba.com/stats/commonallplayers"

    params = {
        "LeagueID": "00",
        "Season": season,
        "IsOnlyCurrentSeason": 1
    }

    data = safe_request(url, params=params, headers=HEADERS)
    if data is None:
        return pd.DataFrame()

    rows = data["resultSets"][0]["rowSet"]
    headers = data["resultSets"][0]["headers"]

    df = pd.DataFrame(rows, columns=headers)
    df.rename(columns={
        "PERSON_ID": "PLAYER_ID",
        "DISPLAY_FIRST_LAST": "PLAYER_NAME"
    }, inplace=True)

    # Only return required columns
    return df[["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]]
