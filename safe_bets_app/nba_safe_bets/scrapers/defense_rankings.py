import requests
import pandas as pd

NBA_DEFENSE_URL = (
    "https://stats.nba.com/stats/leaguedashteamstats"
    "?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment="
    "&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0"
    "&OpponentTeamID=0&Outcome=&PORound=&PaceAdjust=N&PerMode=PerGame"
    "&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N"
    "&Rank=N&Season=2024-25&SeasonSegment=&SeasonType=Regular+Season"
    "&ShotClockRange=&StarterBench=&TeamID=&TwoWay=&VsConference="
    "&VsDivision="
)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.nba.com/",
    "Origin": "https://www.nba.com"
}


def get_defense_rankings():
    """Retrieve team defensive stats from NBA stats API."""
    try:
        r = requests.get(NBA_DEFENSE_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("[DEFENSE ERROR] Could not fetch NBA defensive stats:", e)
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    try:
        json_data = r.json()
    except Exception:
        print("[DEFENSE ERROR] Failed to decode JSON")
        return pd.DataFrame(columns=["team", "points", "rebounds", "assists", "threes"])

    rows = json_data.get("resultSets", [])[0]
    headers = rows.get("headers", [])
    data = rows.get("rowSet", [])

    df = pd.DataFrame(data, columns=headers)

    # Keep and rename important defensive metrics
    df = df.rename(columns={
        "TEAM_NAME": "team",
        "DEF_RATING": "points",
        "DREB_PCT": "rebounds",
        "AST_RATIO": "assists",
        "OPP_EFG_PCT": "threes"
    })

    df = df[["team", "points", "rebounds", "assists", "threes"]]

    print(f"[DEFENSE] Loaded defense rankings: {df.shape}")

    return df
