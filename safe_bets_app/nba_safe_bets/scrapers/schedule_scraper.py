# nba_safe_bets/scrapers/schedule_scraper.py
import pandas as pd
import requests
from datetime import datetime
from nba_safe_bets.utils.logging_config import log

BDL_SCHEDULE = "https://api.balldontlie.io/v1/games"
API_KEY = "free"  # No key needed

def get_todays_schedule():
    """Returns normalized schedule rows:
        team, opp_team, game_id
    """

    date = datetime.today().strftime("%Y-%m-%d")
    params = {"dates[]": date}
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        r = requests.get(BDL_SCHEDULE, params=params, headers=headers, timeout=8)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log(f"[SCHEDULE ERROR] {e}")
        return pd.DataFrame(columns=["team", "opp_team", "game_id"])

    rows = []
    for g in data.get("data", []):
        gid = g.get("id")
        home = g["home_team"]["abbreviation"]
        away = g["visitor_team"]["abbreviation"]

        rows.append({"team": home, "opp_team": away, "game_id": gid})
        rows.append({"team": away, "opp_team": home, "game_id": gid})

    return pd.DataFrame(rows)
