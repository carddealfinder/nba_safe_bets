import requests
import pandas as pd

BASE = "https://api.balldontlie.io/v1"


def get_all_defense_rankings():
    """
    Computes basic defensive ranking:
    Lower points allowed = better defense
    """

    print("🔍 Computing defensive rankings from game logs...")

    url = f"{BASE}/games?per_page=100"
    r = requests.get(url)

    if r.status_code != 200:
        print("[ERROR] Defense ranking API:", r.text)
        return {}

    games = r.json()["data"]

    allowed = {}

    for g in games:
        home = g["home_team"]["id"]
        visitor = g["visitor_team"]["id"]

        allowed.setdefault(home, []).append(g["visitor_team_score"])
        allowed.setdefault(visitor, []).append(g["home_team_score"])

    avg_allowed = {team: sum(vals) / len(vals) for team, vals in allowed.items()}

    return {
        "points": avg_allowed,
        "rebounds": {},
        "assists": {},
        "threes": {},
    }
