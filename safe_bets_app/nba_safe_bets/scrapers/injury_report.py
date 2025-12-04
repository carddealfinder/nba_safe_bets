import pandas as pd

def get_injury_report():
    print("⚠️ BallDontLie has no injury API — returning empty injury list.")
    return pd.DataFrame(columns=["player_id", "status", "comment"])
