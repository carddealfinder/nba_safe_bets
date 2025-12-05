import pandas as pd
from nba_safe_bets.utils.logging_config import log
from nba_safe_bets.utils.bdl_loader import load_players

def get_player_info():
    df = load_players()
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    return df
