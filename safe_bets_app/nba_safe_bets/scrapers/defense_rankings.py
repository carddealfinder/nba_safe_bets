import requests
import pandas as pd

URL = "https://www.basketball-reference.com/leagues/NBA_2024_ratings.html"


def get_defense_rankings():
    """Scrapes defensive efficiency metrics from Basketball Reference with fallback handling."""
    try:
        df_list = pd.read_html(URL)
    except Exception as e:
        print("[DEFENSE ERROR] Could not read HTML:", e)
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    if not df_list:
        print("[DEFENSE ERROR] No tables returned.")
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    df = df_list[0]  # usually the ratings table

    # DEBUG: print first few column names
    print("[DEFENSE] Columns found:", list(df.columns))

    # Flexible detection of columns — Basketball Reference changes formats often
    col_map = {}

    # TEAM NAME COLUMN
    for c in df.columns:
        if "Team" in c or "team" in c.lower():
            col_map["team"] = c
            break

    # DEFENSE / DRtg column
    for c in df.columns:
        if "DRtg" in c or "Def" in c or "def" in c.lower():
            col_map["points"] = c
            break

    # Rebounds proxy (ORB% or DRB% depending what exists)
    for c in df.columns:
        if "ORB%" in c or "DRB%" in c or "RB%" in c:
            col_map["rebounds"] = c
            break

    # Assists proxy (AST% or AST/TO)
    for c in df.columns:
        if "AST" in c:
            col_map["assists"] = c
            break

    # Threes proxy (3P% or Opp 3P%)
    for c in df.columns:
        if "3P" in c:
            col_map["threes"] = c
            break

    # If ANY required metric missing → return safe empty DataFrame
    required = ["team", "points", "rebounds", "assists", "threes"]
    if not all(x in col_map for x in required):
        print("[DEFENSE ERROR] Could not map required columns. Found map:", col_map)
        return pd.DataFrame(columns=required)

    # Rename dynamically and return
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
