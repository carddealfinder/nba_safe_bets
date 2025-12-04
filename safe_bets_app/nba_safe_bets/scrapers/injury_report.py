import pandas as pd

def get_injury_report():
    """Scrapes NBA injury report from Rotowire (public, allowed)."""
    url = "https://www.rotowire.com/basketball/injury-report.php"

    try:
        tables = pd.read_html(url)
        df = tables[0]  # first table = injuries
        df = df.rename(columns={
            "Player": "PLAYER_NAME",
            "Team": "TEAM",
            "Pos": "POS",
            "Injury": "INJURY",
            "Status": "STATUS"
        })
        return df
    except Exception as e:
        print("[ERROR] Failed to fetch injury report:", e)
        return pd.DataFrame(columns=["PLAYER_NAME", "TEAM", "POS", "INJURY", "STATUS"])
