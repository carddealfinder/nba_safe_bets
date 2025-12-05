import pandas as pd
import requests
from nba_safe_bets.utils.logging_config import log


INJURY_URL = "https://cdn.nba.com/static/json/injury/injury_report.json"


def get_injury_report():
    """
    Returns a DataFrame with columns:
        id (may be None if we cannot match)
        injury_status (string)

    Ensures compatibility with feature builder.
    """

    try:
        r = requests.get(INJURY_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log(f"[INJURY] Unable to fetch injury report: {e}")
        return pd.DataFrame(columns=["id", "injury_status"])

    if "league" not in data or "standard" not in data["league"]:
        return pd.DataFrame(columns=["id", "injury_status"])

    records = []
    for p in data["league"]["standard"]:
        player_id = p.get("personId")  # this is sometimes a numeric string
        status = p.get("injuryStatus", "Unknown")

        # Normalize player_id → int or None
        try:
            player_id = int(player_id)
        except:
            player_id = None

        records.append({
            "id": player_id,
            "injury_status": status
        })

    df = pd.DataFrame(records)
    return df[["id", "injury_status"]]
