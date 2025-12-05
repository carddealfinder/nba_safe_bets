import requests
import pandas as pd
from nba_safe_bets.utils.logging_config import log

URL = "https://cdn.nba.com/static/json/injury/injury_report.json"


def get_injury_report():
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        data = r.json()

        injuries = [{
            "player": p.get("name"),
            "status": p.get("status")
        } for p in data.get("league", {}).get("injury", [])]

        return pd.DataFrame(injuries)

    except Exception as e:
        log(f"[INJURY] Unable to fetch injury report: {e}")
        return pd.DataFrame(columns=["player", "status"])
