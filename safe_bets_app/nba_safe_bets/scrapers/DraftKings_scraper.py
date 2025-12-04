import requests
import pandas as pd

DK_URL = "https://sportsbook.draftkings.com/api/sportscontent/v1/leagues/4/events"  # NBA


def get_draftkings_odds():
    """Fetch DraftKings odds safely with bot-protection headers + JSON validation."""
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    try:
        r = requests.get(DK_URL, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print("[DK ERROR] Request failed:", e)
        return pd.DataFrame(columns=["player", "stat", "line"])

    # --- Validate the response is JSON ---
    try:
        data = r.json()
    except Exception:
        print("[DK ERROR] Non-JSON response (HTML likely).")
        return pd.DataFrame(columns=["player", "stat", "line"])

    events = data.get("events", [])
    rows = []

    for ev in events:
        categories = ev.get("offerCategories", [])
        if not categories:
            continue

        # Each category contains subcategories
        for subcat in categories[0].get("offerSubcategoryDescriptors", []):
            subcat_name = subcat.get("subcategoryName")

            offers = subcat.get("offerSubcategory", {}).get("offers", [])
            for offer in offers:
                for outcome in offer:
                    rows.append({
                        "player": outcome.get("participant"),
                        "stat": subcat_name,
                        "line": outcome.get("line")
                    })

    df = pd.DataFrame(rows)
    print(f"[DK] Loaded odds: {df.shape}")
    return df
