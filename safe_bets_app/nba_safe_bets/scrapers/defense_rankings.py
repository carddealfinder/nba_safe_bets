import pandas as pd
import requests


def get_defense_rankings():
    """Scrapes defense rankings (returns fallback zeros if API fails)."""

    url = "https://www.basketball-reference.com/leagues/NBA_2025_ratings.json"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception:
        print("[DEFENSE] Failed to load rankings. Using fallback.")
        return pd.DataFrame(columns=["team", "def_rating", "pace", "rank", "points_allowed"])

    rows = []

    for team, val in data.items():
        rows.append({
            "team": team,
            "def_rating": val.get("def_rating", 0),
            "pace": val.get("pace", 0),
            "rank": val.get("rank", 0),
            "points_allowed": val.get("pts_allowed", 0)
        })

    df = pd.DataFrame(rows)
    print("[DEFENSE] Loaded rankings:", df.shape)
    return df
