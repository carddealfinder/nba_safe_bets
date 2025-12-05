i# nba_safe_bets/scrapers/vegas_odds.py
import pandas as pd
import requests
from nba_safe_bets.utils.logging_config import log

DK_URL = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648?format=json"

def get_dk_odds():
    """Returns a normalized odds dataframe with *at least* team lines or fallback."""
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(DK_URL, headers=headers, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        markets = data.get("eventGroup", {}).get("offerCategories", [])
        rows = []

        for cat in markets:
            for offer in cat.get("offerSubcategoryDescriptors", []):
                for event in offer.get("offerSubcategory", {}).get("offers", []):
                    for selection in event:
                        rows.append({
                            "player": selection.get("label", None),
                            "prop": selection.get("outcomeType", None),
                            "line": selection.get("line", None)
                        })

        if rows:
            return pd.DataFrame(rows)

    except Exception as e:
        log(f"[DK ERROR] Request failed: {e}")

    # ----------------------
    # EMERGENCY FALLBACK
    # ----------------------
    return pd.DataFrame({
        "player": [],
        "prop": [],
        "line": []
    })

