import requests
import pandas as pd
from nba_safe_bets.utils.logging_config import log

DK_API = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648?format=json"


def get_dk_odds():
    """
    Always returns a DataFrame, even on failure.

    Columns returned:
    - player
    - stat_type
    - line
    """

    log("[DK] Fetching DraftKings odds...")

    try:
        r = requests.get(DK_API, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log(f"[DK ERROR] Request failed: {e}")
        log("[DK FALLBACK] Returning empty odds dataframe.")

        return pd.DataFrame(columns=["player", "stat_type", "line"])

    # ----------------------------------------------------------------------
    # DK JSON parsing varies wildly; to keep the engine safe:
    # We return an EMPTY standardized DF until real parsing is implemented.
    # ----------------------------------------------------------------------

    log("[DK] Loaded DK data (raw), but returning fallback standardized table.")

    return pd.DataFrame(columns=["player", "stat_type", "line"])
