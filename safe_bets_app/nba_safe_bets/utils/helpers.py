import re
import pandas as pd


# ---------------------------------------------------------
# SAFE NUMBER PARSING
# ---------------------------------------------------------
def try_float(x, default=None):
    """Convert value to float safely."""
    try:
        return float(x)
    except:
        return default


# ---------------------------------------------------------
# AMERICAN ODDS → IMPLIED PROBABILITY
# ---------------------------------------------------------
def american_to_probability(odds):
    """
    Converts American odds (-110, +140, etc) to implied probability.
    Returns a float between 0 and 1.
    """
    try:
        odds = float(odds)
    except:
        return None

    # negative odds (favorite)
    if odds < 0:
        return (-odds) / ((-odds) + 100)

    # positive odds (underdog)
    return 100 / (odds + 100)


# ---------------------------------------------------------
# PLAYER NAME CLEANING & STANDARDIZATION
# ---------------------------------------------------------
def normalize_name(name: str):
    """
    Clean up player names to maintain consistency across scrapers.
    """
    if not isinstance(name, str):
        return name

    # Remove extra spaces, punctuation
    name = name.strip()
    name = re.sub(r"\s+", " ", name)

    # Title case
    return name.title()


# ---------------------------------------------------------
# MERGE SAFE (avoid crashes)
# ---------------------------------------------------------
def safe_merge(left: pd.DataFrame, right: pd.DataFrame, on: str, how="left"):
    """
    Merge two DataFrames safely—if right is empty, returns left unchanged.
    """
    if right is None or len(right) == 0:
        return left.copy()

    return left.merge(right, on=on, how=how)


# ---------------------------------------------------------
# NORMALIZE STAT KEYS
# ---------------------------------------------------------
STAT_KEY_MAP = {
    "pts": "points",
    "points": "points",
    "reb": "rebounds",
    "rebs": "rebounds",
    "rebounds": "rebounds",
    "ast": "assists",
    "assists": "assists",
    "3pt": "threes",
    "3pm": "threes",
    "threes": "threes",
    "three_pointers_made": "threes",
}


def normalize_stat_key(stat: str):
    """
    Convert multiple stat label versions to the expected unified keys.
    Example:
        "pts" → "points"
        "3PM" → "threes"
    """
    if stat is None:
        return None

    stat_lower = str(stat).strip().lower()
    return STAT_KEY_MAP.get(stat_lower, stat_lower)


# ---------------------------------------------------------
# PRETTY PRINTING & DEBUG UTILITIES
# ---------------------------------------------------------
def debug_df(df: pd.DataFrame, name: str):
    """
    Print DataFrame shape and head for debugging.
    """
    print(f"\n--- DEBUG: {name} ---")
    if df is None:
        print("❌ DataFrame is NONE")
        return

    print("Shape:", df.shape)
    if df.shape[0] > 0:
        print(df.head())
    else:
        print("⚠️ DataFrame is EMPTY")


# ---------------------------------------------------------
# NORMALIZE PLAYER IDs (DraftKings uses DK IDs; BDL uses numeric)
# ---------------------------------------------------------
def normalize_player_id(pid):
    """
    Convert any player ID into a consistent string key.
    """
    if pid is None:
        return None
    return str(pid).strip()

def safe_get(obj, path, default=None):
    """
    Safely extract a nested field from a dict using a list of keys.
    
    Example:
        safe_get(data, ["player", "team", "full_name"])
    """
    current = obj
    for key in path:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
