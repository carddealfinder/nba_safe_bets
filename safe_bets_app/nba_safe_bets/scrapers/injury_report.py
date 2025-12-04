import requests
import pandas as pd

# Placeholder endpoint — replace with real source if available
INJURY_URL = "https://cdn.nba.com/static/json/injury/injury_2024.json"


def get_injury_report():
    try:
        r = requests.get(INJURY_URL, timeout=10)
        r.raise_for_status()
    except Exception:
        print("[INJURY] Unable to fetch injury report.")
        return pd.DataFrame(columns=["id", "injury_status", "injury_desc"])

    payload = r.json().get("league", {}).get("standard", [])
    rows = []

    for p in payload:
        rows.append({
            "id": p.get("personId"),
            "injury_status": p.get("status"),
            "injury_desc": p.get("detail")
        })

    return pd.DataFrame(rows)
