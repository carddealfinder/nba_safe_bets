import pandas as pd
import requests


def get_draftkings_lines():
    """Fetches DraftKings prop lines. Returns empty DF if API fails."""

    url = "https://api.dk-content.com/v1/odds/nba-player-props"

    try:
        r = requests.get(url, timeout=10)
        if r.headers.get("Content-Type", "").startswith("application/json"):
            data = r.json()
        else:
            raise ValueError("Non-JSON response")
    except Exception as e:
        print(f"[DK ERROR] Non-JSON response received")
        return pd.DataFrame(columns=["id", "prop_stat", "line"])

    rows = []

    for entry in data.get("players", []):
        pid = entry.get("player_id")
        for prop in entry.get("props", []):
            rows.append({
                "id": pid,
                "prop_stat": prop.get("type"),
                "line": prop.get("line")
            })

    df = pd.DataFrame(rows)
    print("[DK] Loaded odds:", df.shape)
    return df
