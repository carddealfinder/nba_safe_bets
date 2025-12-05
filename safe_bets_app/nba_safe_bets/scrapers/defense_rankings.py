import pandas as pd
from nba_safe_bets.utils.logging_config import log

def get_defense_rankings():
    """Always returns a full 30-team ranking table."""
    try:
        # Insert real API later
        raise Exception("No real API yet")
    except:
        default = pd.DataFrame({
            "team": [],
            "def_pts": [],
            "def_reb": [],
            "def_ast": [],
            "def_3pt": []
        })
        return default
