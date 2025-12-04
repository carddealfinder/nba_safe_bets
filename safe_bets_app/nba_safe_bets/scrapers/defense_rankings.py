import pandas as pd

NBA_TEAM_PTS_ALLOWED = "https://www.nba.com/stats/teams/defense?Season=2024-25&SeasonType=Regular%20Season"

def get_all_defense_rankings():
    """Scrapes defensive rankings from NBA.com HTML (safe)."""
    try:
        tables = pd.read_html(NBA_TEAM_PTS_ALLOWED)
        df = tables[0]
        df = df.rename(columns={"Team": "TEAM", "PTS": "POINTS_ALLOWED"})
        df["TEAM"] = df["TEAM"].str.replace("*", "", regex=False)
        return {"points": df}
    except Exception as e:
        print("[ERROR] Unable to scrape defensive rankings:", e)
        return {"points": pd.DataFrame()}
