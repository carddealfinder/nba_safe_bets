import pandas as pd

URLS = {
    "points": "https://www.fantasypros.com/nba/defense-vs-position.php",
    "rebounds": "https://www.fantasypros.com/nba/defense-vs-position-reb.php",
    "assists": "https://www.fantasypros.com/nba/defense-vs-position-ast.php",
    "threes": "https://www.fantasypros.com/nba/defense-vs-position-3pm.php"
}

def fetch_defense_table(stat_type):
    url = URLS[stat_type]
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Position", "Team", stat_type]
    return df

def get_all_defense_rankings():
    dfs = {}
    for stat in URLS:
        dfs[stat] = fetch_defense_table(stat)
    return dfs
