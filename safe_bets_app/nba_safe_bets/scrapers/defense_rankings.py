import pandas as pd

URLS = {
    "points": "https://www.fantasypros.com/nba/defense-vs-position.php",
    "rebounds": "https://www.fantasypros.com/nba/defense-vs-position-reb.php",
    "assists": "https://www.fantasypros.com/nba/defense-vs-position-ast.php",
    "threes": "https://www.fantasypros.com/nba/defense-vs-position-3pm.php"
}


def safe_empty(stat_type):
    """Return an empty, correctly-shaped DataFrame."""
    return pd.DataFrame(columns=["Position", "Team", stat_type])


def fetch_defense_table(stat_type):
    url = URLS[stat_type]

    # -------------------------------
    # 1. Read HTML safely
    # -------------------------------
    try:
        tables = pd.read_html(url)
    except Exception as e:
        print(f"[ERROR] Unable to read HTML for {stat_type}: {e}")
        return safe_empty(stat_type)

    # -------------------------------
    # 2. Validate returned tables
    # -------------------------------
    if not isinstance(tables, list) or len(tables) == 0:
        print(f"[ERROR] No HTML tables found for {stat_type}")
        return safe_empty(stat_type)

    df = tables[0]

    if not isinstance(df, pd.DataFrame):
        print(f"[ERROR] Table for {stat_type} is not a DataFrame")
        return safe_empty(stat_type)

    # -------------------------------
    # 3. Ensure the table has enough columns
    # -------------------------------
    if df.shape[1] < 3:
        print(f"[ERROR] Too few columns for {stat_type}: {df.shape}")
        return safe_empty(stat_type)

    # -------------------------------
    # 4. Trim to first 3 columns only
    # -------------------------------
    try:
        df = df.iloc[:, :3]
    except Exception as e:
        print(f"[ERROR] Failed to trim table for {stat_type}: {e}")
        return safe_empty(stat_type)

    # -------------------------------
    # 5. Rename columns safely
    # -------------------------------
    try:
        df.columns = ["Position", "Team", stat_type]
    except Exception as e:
        print(f"[ERROR] Failed column rename for {stat_type}: {e}")
        return safe_empty(stat_type)

    return df


def get_all_defense_rankings():
    dfs = {}
    for stat in URLS:
        dfs[stat] = fetch_defense_table(stat)
    return dfs
