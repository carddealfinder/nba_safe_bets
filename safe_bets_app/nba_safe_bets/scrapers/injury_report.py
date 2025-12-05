import pandas as pd
import requests


def get_injury_report():
    """Returns injury report dataframe (empty if API unavailable)."""

    url = "https://cdn.nba.com/static/json/injury/injury_report.json"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("league", {}).get("standard", [])
    except Exception as e:
        print(f"[INJURY] Unable to fetch injury report: {e}")
        return pd.DataFrame(columns=["player_id", "injury_status"])

    rows = []
    for p in data:
        rows.append({
            "player_id": int(p.get("personId", 0)),
            "injury_status": p.get("comment", None)
        })

    df = pd.DataFrame(rows)
    print("[INJURY] Loaded injury report:", df.shape)
    return df
