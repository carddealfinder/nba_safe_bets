# nba_safe_bets/scrapers/injury_report.py
import pandas as pd
import requests
from nba_safe_bets.utils.logging_config import log

URL = "https://cdn.nba.com/static/json/injury/injury_report.json"

def get_injury_report():
    try:
        resp = requests.get(URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        rows = []
        for t in data.get("league", {}).get("injuryReport", []):
            for p in t.get("players", []):
                rows.append({
                    "player": p.get("firstName", "") + " " + p.get("lastName", ""),
                    "injury_status": p.get("status", "QUESTIONABLE")
                })

        return pd.DataFrame(rows)

    except Exception as e:
        log(f"[INJURY] Unable to fetch injury report: {e}")

    # Fallback
    return pd.DataFrame(columns=["player", "injury_status"])
