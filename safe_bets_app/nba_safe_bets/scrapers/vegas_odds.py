import pandas as pd


def get_dk_odds():
    """
    DK odds are unstable and frequently return HTML or 403s on Streamlit Cloud.
    For now, we return an empty valid odds dataframe to keep prediction stable.
    """

    print("[DK] Loading DraftKings odds (stub implementation)...")

    # Expected columns downstream
    return pd.DataFrame(columns=["player_id", "prop_type", "line_value"])
