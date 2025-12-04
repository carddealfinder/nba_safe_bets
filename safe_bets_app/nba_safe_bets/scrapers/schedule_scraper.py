import requests

URL = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"

def get_schedule():
    """
    Returns the full NBA season schedule JSON.
    """
    r = requests.get(URL)
    try:
        data = r.json()
        return data["leagueSchedule"]["gameDates"]
    except:
        return []
