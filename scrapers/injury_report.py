import pandas as pd

URL = "https://www.rotowire.com/basketball/nba-injury-report.php"

def get_injury_report():
    """
    Returns Rotowire injury table.
    """
    try:
        tables = pd.read_html(URL)
        df = tables[0]
        df.columns = ["Player", "Team", "Status", "Injury", "Notes"]
        return df
    except:
        return pd.DataFrame(columns=["Player", "Team", "Status", "Injury", "Notes"])
