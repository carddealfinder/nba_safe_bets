import requests
import pandas as pd
from nba_safe_bets.utils.logging_config import log

DK_URL = "https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/42648/categories/"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

# ---------------------------------------------------
# Fallback odds if DraftKings blocks the request
# ---------------------------------------------------
def fallback_odds():
    log("[DK FALLBACK] Using emergency fallback odds.")
    return pd.DataFrame(columns=["player_id", "stat", "line", "book"])


# ---------------------------------------------------
# Main odds scraper — this MUST exist for imports
# ---------------------------------------------------
def get_dk_odds():
    """
    Scrapes DraftKings odds. If unavailable (403, 429, invalid JSON),
    returns a fallback empty DF instead of crashing daily_predict.
    """

    try:
        log("[DK] Fetching DraftKings odds...")

        response = requests.get(DK_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except Exception:
            log("[DK ERROR] Non-JSON response received")
            return fallback_odds()

        markets = data.get("eventGroup", {}).get("offerCategories", [])
        rows = []

        for cat in markets:
            category_name = cat.get("name", "")
            for sub in cat.get("offerSubcategoryDescriptors", []):
                for offer in sub.get("offerSubcategory", {}).get("offers", []):
                    for item in offer:
                        player = item.get("label", "")
                        line = item.get("oddsDecimal", None)

                        if not player or line is None:
                            continue

                        # Example stat mapping
                        if "Points" in category_name:
                            stat = "points"
                        elif "Rebounds" in category_name:
                            stat = "rebounds"
                        elif "Assists" in category_name:
                            stat = "assists"
                        elif "3-Pointers" in category_name:
                            stat = "threes"
                        else:
                            continue

                        rows.append({
                            "player_id": None,    # matched later by fuzzy name mapper
                            "stat": stat,
                            "line": line,
                            "book": "DraftKings",
                        })

        df = pd.DataFrame(rows)
        log(f"[DK] Loaded odds: {df.shape}")

        return df if not df.empty else fallback_odds()

    except Exception as e:
        log(f"[DK ERROR] {e}")
        return fallback_odds()
