import requests
import pandas as pd


DK_URL = "https://sportsbook.draftkings.com/api/sportscontent/v1/leagues/4/events"  # NBA


def get_draftkings_odds():
    try:
        r = requests.get(DK_URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("[DK ERROR]", e)
        return pd.DataFrame(columns=["player", "stat", "line"])

    data = r.json()
    events = data.get("events", [])

    rows = []

    for ev in events:
        markets = ev.get("offerCategories", [{}])[0].get("offerSubcategoryDescriptors", [])
        for m in markets:
            for offer in m.get("offerSubcategory", {}).get("offers", []):
                for outcome in offer:
                    rows.append({
                        "player": outcome.get("participant"),
                        "stat": m.get("subcategoryName"),
                        "line": outcome.get("line", None)
                    })

    return pd.DataFrame(rows)
