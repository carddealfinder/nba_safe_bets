import re
import unicodedata
from difflib import SequenceMatcher


def normalize_name(name: str) -> str:
    """
    Convert any player name format to lowercase, alphabetic, no punctuation.
    Examples:
        "Tatum, Jayson" → "jayson tatum"
        "J. Tatum"      → "j tatum"
        "Évan Fournier" → "evan fournier"
    """
    if not isinstance(name, str):
        return ""

    # Remove accents
    name = unicodedata.normalize("NFKD", name)
    name = "".join([c for c in name if not unicodedata.combining(c)])

    # Replace commas / periods
    name = name.replace(",", " ").replace(".", " ")

    # Strip extra spaces
    name = re.sub(r"\s+", " ", name).strip().lower()

    return name


def similarity(a: str, b: str) -> float:
    """
    Similarity ratio between two normalized names.
    Uses difflib — lightweight and very accurate for this task.
    """
    return SequenceMatcher(None, a, b).ratio()


def match_player(name: str, player_df):
    """
    Given a player name from DraftKings, match to the player's row
    in the Balldontlie / NBA player list DataFrame.

    player_df must contain:
        - player_name column (string)
        - player_id column (numeric)
    """

    if player_df is None or len(player_df) == 0:
        return None

    target = normalize_name(name)

    best_score = 0
    best_row = None

    for _, row in player_df.iterrows():
        candidate = normalize_name(row.get("PLAYER_NAME", row.get("player_name", "")))

        score = similarity(target, candidate)

        if score > best_score:
            best_score = score
            best_row = row

    # Threshold tuning: 0.75 catches "J. Tatum" → "Jayson Tatum"
    if best_score < 0.70:
        return None

    return best_row
