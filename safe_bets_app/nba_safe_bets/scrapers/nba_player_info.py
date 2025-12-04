import pandas as pd
import requests

# Cloud-safe NBA player list (public JSON)
PLAYER_LIST_URL = "https://raw.githubusercontent.com/bttmly/nba/master/data/players.json"

def get_player_list():
    """
    Returns a DataFrame with columns:
    PLAYER_ID, PLAYER_NAME, TEAM_ID
    using a public GitHub-hosted NBA dataset.
    """
    try:
        r = requests.get(PLAYER_LIST_URL, timeout=10)
        data = r.json()
    except Exception as e:
        print("[ERROR] Failed to fetch player list:", e)
        return pd.DataFrame(columns=["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"])

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Ensure required columns
    if "playerId" not in df or "firstName" not in df or "lastName" not in df:
        print("[ERROR] Player dataset missing required fields.")
        return pd.DataFrame(columns=["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"])

    # Build expected schema
    df["PLAYER_ID"] = df["playerId"]
    df["PLAYER_NAME"] = df["firstName"] + " " + df["lastName"]

    # TEAM ID not included → fill null (your model can handle this)
    df["TEAM_ID"] = None

    return df[["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]]
