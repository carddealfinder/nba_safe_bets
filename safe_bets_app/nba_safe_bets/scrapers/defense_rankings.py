import requests
import pandas as pd


URL = "https://www.basketball-reference.com/leagues/NBA_2024_ratings.html"


def get_defense_rankings():
    """Scrapes defense efficiency per team."""
    try:
        df_list = pd.read_html(URL)
    except Exception as e:
        print("[DEFENSE ERROR]", e)
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    df = df_list[0]

    df = df.rename(columns={
        "Team": "team",
        "DRtg": "points",
        "ORB%": "rebounds",
        "AST%": "assists",
        "3P%": "threes"
    })

    return df[["team", "points", "rebounds", "assists", "threes"]]
