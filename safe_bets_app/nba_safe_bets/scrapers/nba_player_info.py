import pandas as pd
from nba_safe_bets.utils.logging_config import log

# ✔ Use balldontlie scraper (correct module)
from nba_safe_bets.scrapers.balldontlie_players import get_player_list


def get_player_info():
    """
    Returns a cleaned dataframe of all NBA players with ids and names.
    This now uses the Balldontlie API through get_player_list().
    """

    try:
        log("[PLAYER INFO] Fetching player list...")
        df = get_player_list()
    except Exception as e:
        log(f"[PLAYER INFO ERROR] Failed to load players: {e}")
        return pd.DataFrame(columns=["id", "first_name", "last_name", "team"])

    if df is None or df.empty:
        log("[PLAYER INFO] Player list empty — returning fallback.")
        return pd.DataFrame(columns=["id", "first_name", "last_name", "team"])

    df = df.copy()
    df["full_name"] = df["first_name"] + " " + df["last_name"]

    return df[["id", "first_name", "last_name", "full_name", "team"]]
