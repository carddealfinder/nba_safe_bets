import requests
import pandas as pd
from nba_safe_bets.utils.logging_config import log

DK_URL = "https://sportsbook.draftkings.com/api/sportscontent/v1/leagues/3/events"

def get_dk_odds():
    """
    Fetches DraftKings NBA prop odds.
    If DK blocks requests or returns HTML, JSON, or connection errors, 
    we return a SAFE empty dataframe with the correct structure.
    """

    log("[DK] Fetching DraftKings odds...")

    empty_df = pd.DataFrame(columns=["player", "stat_type", "line"])

    try:
        r = requests.get(DK_URL, timeout=10)
    except Exception as e:
        log(f"[DK ERROR] Request failed: {e}")
        return empty_df

    # DK often returns HTML → we must guard against JSON decode failures
    try:
        data = r.json()
    except Exception:
        log("[DK ERROR] Non-JSON response received")
        return empty_df

    if "events" not in data:
        log("[DK ERROR] No 'events' key found in DK response")
        return empty_df

    rows = []

    for event in data["events"]:
        markets = event.get("offerCategories", [])
        for cat in markets:
            offers = cat.get("offerSubcategoryDescriptors", [])
            for sub in offers:
                for market in sub.get("offerSubcategory", {}).get("offers", []):
                    for outcome in market.get("outcomes", []):
                        player = outcome.get("participant")
                        line = outcome.get("line")
                        stat = market.get("label")

                        if not player or line is None or not stat:
                            continue

                        rows.append({
                            "player": player,
                            "stat_type": stat.lower(),
                            "line": float(line),
                        })

    if not rows:
        log("[DK] No odds parsed from API. Returning empty DF.")
        return empty_df

    df = pd.DataFrame(rows)
    log(f"[DK] Loaded odds: {df.shape}")

    return df
