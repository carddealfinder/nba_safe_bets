import requests
import pandas as pd
from datetime import datetime
from nba_safe_bets.utils.helpers import (
    normalize_name,
    normalize_stat_key,
    american_to_probability,
    try_float
)


DK_URL = (
    "https://sportsbook-us-il.draftkings.com//sites/US-IL-SB/api/"
    "v5/eventgroups/84240/categories/116/statistics.json"
)

# 84240 = NBA Event Group
# 116 = Player Props (Points, Rebounds, Assists, Threes, etc.)


# ---------------------------------------------------------
# FETCH RAW DATA FROM DRAFTKINGS
# ---------------------------------------------------------
def fetch_draftkings_raw():
    """
    Fetch raw NBA player prop markets from DraftKings.
    Returns JSON (dict) or None.
    """
    try:
        r = requests.get(DK_URL, timeout=10)

        if r.status_code != 200:
            print(f"[DK ERROR] Status {r.status_code}: {r.text[:200]}")
            return None

        return r.json()

    except Exception as e:
        print("[DK ERROR] Exception while requesting DraftKings:", e)
        return None


# ---------------------------------------------------------
# PARSE INDIVIDUAL PLAYER PROP MARKET
# ---------------------------------------------------------
def parse_market(stat_type, market):
    """
    Parse a single DraftKings market into multiple rows:
    (one for each available line option)
    """

    outcomes = market.get("outcomes", [])
    results = []

    for outcome in outcomes:
        player = normalize_name(outcome.get("participant"))
        line = try_float(outcome.get("line"))
        odds = try_float(outcome.get("oddsAmerican"))
        implied = american_to_probability(odds)

        if player is None or line is None:
            continue

        results.append({
            "player": player,
            "stat": normalize_stat_key(stat_type),
            "line": line,
            "odds": odds,
            "implied_prob": implied,
            "dk_event_id": market.get("providerEventId"),
            "market_name": stat_type
        })

    return results


# ---------------------------------------------------------
# MAIN SCRAPER
# ---------------------------------------------------------
def get_draftkings_props():
    """
    Fetch + parse DraftKings props for Points / Rebounds / Assists / Threes.

    Returns: DataFrame with normalized prop markets.
    """

    print("\n[DK] Fetching DraftKings NBA props...")
    raw = fetch_draftkings_raw()

    if raw is None:
        print("[DK] No data received.")
        return pd.DataFrame()

    categories = raw.get("eventGroup", {}).get("categories", [])
    if not categories:
        print("[DK] No categories found in API response.")
        return pd.DataFrame()

    all_props = []

    # Loop over each category and capture props
    for cat in categories:
        cat_name = cat.get("name", "").lower()

        # Only grab key stat categories
        if any(key in cat_name for key in ["points", "rebounds", "assists", "3-point"]):

            stat_key = None
            if "points" in cat_name:
                stat_key = "points"
            elif "rebounds" in cat_name:
                stat_key = "rebounds"
            elif "assists" in cat_name:
                stat_key = "assists"
            elif "3-point" in cat_name:
                stat_key = "threes"

            markets = cat.get("offerSubcategoryDescriptors", [])
            for subcat in markets:
                offers = subcat.get("offerSubcategory", {}).get("offers", [])
                for offer in offers:
                    market_name = offer.get("label", "")
                    outcomes = offer.get("outcomes", [])

                    market_obj = {
                        "providerEventId": offer.get("providerEventId"),
                        "outcomes": outcomes
                    }

                    # Parse outcomes
                    parsed = parse_market(stat_key, market_obj)
                    all_props.extend(parsed)

    if len(all_props) == 0:
        print("[DK] Parsed 0 props.")
        return pd.DataFrame()

    df = pd.DataFrame(all_props)

    # Remove missing values
    df = df.dropna(subset=["player", "stat", "line"]).reset_index(drop=True)

    print(f"[DK] Parsed {len(df)} prop lines.")
    return df


# ---------------------------------------------------------
# Script Testing Hook
# ---------------------------------------------------------
if __name__ == "__main__":
    df = get_draftkings_props()
    print("\n--- DraftKings Props ---")
    print(df.head(20))
