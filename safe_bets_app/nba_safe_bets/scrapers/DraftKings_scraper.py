import requests
import pandas as pd

DK_URL = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648?format=json"  
# 42648 = NBA event group

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://sportsbook.draftkings.com",
    "Referer": "https://sportsbook.draftkings.com/leagues/basketball/nba",
    "Accept-Language": "en-US,en;q=0.9"
}


def get_draftkings_odds():
    """Scrape NBA player prop lines from DraftKings."""
    try:
        resp = requests.get(DK_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[DK ERROR] Could not reach DK API: {e}")
        return pd.DataFrame(columns=["player", "stat", "line"])

    try:
        data = resp.json()
    except Exception:
        print("[DK ERROR] JSON decode failed — site may be blocking requests.")
        return pd.DataFrame(columns=["player", "stat", "line"])

    # Data lives in "eventGroup" → "offerCategories"
    event_group = data.get("eventGroup", {})
    offer_categories = event_group.get("offerCategories", [])

    rows = []

    for cat in offer_categories:
        subcats = cat.get("offerSubcategoryDescriptors", [])
        for sub in subcats:
            stat_name = sub.get("subcategoryName", "")

            offers = sub.get("offerSubcategory", {}).get("offers", [])
            for offer_list in offers:
                for offer in offer_list:
                    outcome = offer.get("outcomes", [{}])[0]

                    rows.append({
                        "player": outcome.get("participant"),
                        "stat": stat_name,
                        "line": outcome.get("line", None)
                    })

    df = pd.DataFrame(rows).dropna(subset=["player", "stat"])
    print(f"[DK] Loaded odds: {df.shape}")

    return df
