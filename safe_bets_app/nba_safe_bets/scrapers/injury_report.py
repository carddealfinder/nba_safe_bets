import requests
import pandas as pd


def get_injury_report():
    url = "https://cdn.nba.com/static/json/injury/injury_report.json"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return pd.DataFrame(columns=["player_id", "injury_status"])

        data = r.json().get("league", {}).get("standard", [])

        rows = []
        for p in data:
            rows.append({
                "player_id": p["personId"],
                "injury_status": 1
            })

        return pd.DataFrame(rows)

    except:
        return pd.DataFrame(columns=["player_id", "injury_status"])
