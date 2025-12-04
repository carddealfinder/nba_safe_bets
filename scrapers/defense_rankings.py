import pandas as pd

URLS = {
    "points": "https://www.fantasypros.com/nba/defense-vs-position.php",
    "rebounds": "https://www.fantasypros.com/nba/defense-vs-position-reb.php",
    "assists": "https://www.fantasypros.com/nba/defense-vs-position-ast.php",
    "threes": "https://www.fantasypros.com/nba/defense-vs-position-3pm.php"
}


def fetch_defense_table(stat_type):
    url = URLS[stat_type]

    try:
        tables = pd.read_html(url)
    except Exception as e:
        print(f"Error reading HTML for {stat_type}: {e}")
        return pd.DataFrame(columns=["Position", "Team", stat_type])

    if not tables:
        print(f"No tables found for {stat_type}")
        return pd.DataFrame(columns=["Position", "Team", stat_type])

    df = tables[0]

    # Normalize to the first 3 columns
    if df.shape[1] < 3:
        print(f"Table for {stat_type} has too few columns: {df.shape}")
        return pd.DataFrame(columns=["Position", "Team", stat_type])

    # Keep ONLY the first 3 columns because FantasyPros sometimes adds extras
    df = df.iloc[:, :3]

    # Rename them safely
    df.columns = ["Position", "Team", stat_type]

    return df


def get_all_defense_rankings():
    dfs = {}
    for stat in URLS:
        dfs[stat] = fetch_defense_table(stat)
    return dfs
