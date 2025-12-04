import requests
import pandas as pd

URL = "https://www.basketball-reference.com/leagues/NBA_2024_ratings.html"


def normalize_col(col):
    """Normalize column names whether they are strings or tuples."""
    if isinstance(col, tuple):   # MultiIndex column
        col = " ".join([str(c) for c in col if c and c != ""])  # join parts
    return str(col).strip()


def get_defense_rankings():
    """Scrape defensive metrics with full dynamic MultiIndex-safe handling."""
    try:
        df_list = pd.read_html(URL, header=0)
    except Exception as e:
        print("[DEFENSE ERROR] Could not read HTML:", e)
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    if not df_list:
        print("[DEFENSE ERROR] No tables returned.")
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    df = df_list[0]

    # Normalize ALL columns (handles tuple MultiIndex)
    df.columns = [normalize_col(c) for c in df.columns]

    print("[DEFENSE] Columns found:", df.columns.tolist())

    col_map = {}

    # TEAM COLUMN
    for c in df.columns:
        if "team" in c.lower():
            col_map["team"] = c
            break

    # DEFENSE RATING
    for c in df.columns:
        if "drtg" in c.lower() or "def" in c.lower():
            col_map["points"] = c
            break

    # REBOUNDS
    for c in df.columns:
        if "orb" in c.lower() or "drb" in c.lower() or "reb" in c.lower():
            col_map["rebounds"] = c
            break

    # ASSISTS
    for c in df.columns:
        if "ast" in c.lower():
            col_map["assists"] = c
            break

    # THREES
    for c in df.columns:
        if "3p" in c.lower():
            col_map["threes"] = c
            break

    required = ["team", "points", "rebounds", "assists", "threes"]

    if not all(r in col_map for r in required):
        print("[DEFENSE ERROR] Missing required mapped columns:", col_map)
        return pd.DataFrame(columns=required)

    # Rename into a standard output format
    df = df.rename(columns={
        col_map["team"]: "team",
        col_map["points"]: "points",
        col_map["rebounds"]: "rebounds",
        col_map["assists"]: "assists",
        col_map["threes"]: "threes",
    })

    result = df[["team", "points", "rebounds", "assists", "threes"]].copy()

    print("[DEFENSE] Final shape:", result.shape)
    return result
