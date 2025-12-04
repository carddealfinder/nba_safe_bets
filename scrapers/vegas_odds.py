import requests
import pandas as pd

def get_vegas_odds(api_key):
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"

    params = {
        "apiKey": api_key,
        "regions": "us",
        "markets": "spreads,totals"
    }

    r = requests.get(url, params=params)
    if r.status_code != 200:
        return pd.DataFrame()

    try:
        data = r.json()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
