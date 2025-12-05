import pandas as pd
import requests

DK_URL = "https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/42648?format=json"

def get_dk_odds():
    """
    Safely fetches DK odds.
    Always returns a DataFrame with columns:
        id, points_line, rebounds_line, assists_line, threes_line
    If data cannot be fetched, returns an empty DataFrame.
    """

    print("[DK] Fetching DraftKings odds...")

    try:
        r = requests.get(DK_URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[DK ERROR] Request failed: {e}")
        return pd.DataFrame(columns=[
            "id", "points_line", "rebounds_line", "assists_line", "threes_line"
        ])

    try:
        data = r.json()
    except Exception:
        print("[DK ERROR] Non-JSON response received")
        return pd.DataFrame(columns=[
            "id", "points_line", "rebounds_line", "assists_line", "threes_line"
        ])

    # ------------------------------------------------------------------
    # Extract markets safely
    # ------------------------------------------------------------------
    markets = []

    try:
        events = data.get("eventGroup", {}).get("events", [])
    except Exception:
        events = []

    for ev in events:
        pid = ev.get("teamName", "")  # placeholder—DK odds not tied to BDL id
        markets.append({
            "id": pid,  # You can later map names → BDL ids using fuzzy matching
            "points_line": 0,
            "rebounds_line": 0,
            "assists_line": 0,
            "threes_line": 0,
        })

    df = pd.DataFrame(markets)

    print(f"[DK] Loaded odds shape: {df.shape}")
    return df
