import pandas as pd

URL = "https://www.basketball-reference.com/leagues/NBA_2024_ratings.html"


def get_defense_rankings():
    """Load team defense metrics from Basketball Reference safely."""
    try:
        df_list = pd.read_html(URL)
    except Exception as e:
        print("[DEFENSE ERROR] Could not read HTML:", e)
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    # Pick the first table (defensive ratings)
    df = df_list[0].copy()

    # Flatten multi-index columns if they exist
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(c) for c in col if c]) for col in df.columns]

    # Create lowercase-safe column list
    cols = {col.lower(): col for col in df.columns}

    # Extract closest matching columns
    team_col = next((v for k, v in cols.items() if "team" in k), None)
    drtg_col = next((v for k, v in cols.items() if "drtg" in k), None)
    orb_col = next((v for k, v in cols.items() if "orb" in k), None)
    ast_col = next((v for k, v in cols.items() if "ast" in k), None)
    three_col = next((v for k, v in cols.items() if "3p" in k or "3p%" in k), None)

    if not team_col:
        print("[DEFENSE ERROR] Team column not found")
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    # Build cleaned output even if some columns missing
    out = pd.DataFrame()
    out["team"] = df[team_col]

    out["points"] = df[drtg_col] if drtg_col else 0
    out["rebounds"] = df[orb_col] if orb_col else 0
    out["assists"] = df[ast_col] if ast_col else 0
    out["threes"] = df[three_col] if three_col else 0

    print("[DEFENSE] Loaded rankings:", out.shape)
    return out
