import requests
import pandas as pd

DK_URL = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/4?format=json"


def get_draftkings_odds():
    """Fetch DraftKings prop markets safely with HTML/JSON fallback."""
    try:
        r = requests.get(DK_URL, timeout=10)
        text = r.text.strip()

        # If response is not JSON, abort safely
        if not text.startswith("{"):
            print("[DK ERROR] Non-JSON response received")
            return pd.DataFrame(columns=["player", "stat", "line"])

        data = r.json()
    except Exception as e:
        print("[DK ERROR]", e)
        return pd.DataFrame(columns=["player", "stat", "line"])

    event_groups = data.get("eventGroup", {}).get("offerCategories", [])
    rows = []

    for cat in event_groups:
        for subcat in cat.get("offerSubcategoryDescriptors", []):
            stat_name = subcat.get("subcategoryName")
            offers = subcat.get("offerSubcategory", {}).get("offers", [])

            for offer in offers:
                for outcome in offer:
                    rows.append({
                        "player": outcome.get("participant"),
                        "stat": stat_name,
                        "line": outcome.get("line")
                    })

    df = pd.DataFrame(rows)
    print("[DK] Loaded odds:", df.shape)
    return df
