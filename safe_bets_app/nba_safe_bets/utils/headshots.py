import requests

def get_player_headshot_url(player_id: int, player_name: str = ""):
    """
    Returns the URL for the player's headshot using:
    1. NBA CDN (official)
    2. Balldontlie CDN fallback
    3. Placeholder avatar
    
    Player_id must be the NBA player ID for official CDN.
    """

    # -----------------------------------------------------
    # 1️⃣ NBA Official CDN (best quality)
    # -----------------------------------------------------
    nba_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"

    try:
        r = requests.get(nba_url, timeout=3)
        if r.status_code == 200:
            return nba_url
    except:
        pass  # try next option


    # -----------------------------------------------------
    # 2️⃣ Balldontlie Fallback (name-based)
    # -----------------------------------------------------
    if player_name:
        slug = (
            player_name.lower()
            .replace(".", "")
            .replace("'", "")
            .replace(" ", "-")
        )
        bdl_url = f"https://cdn.balldontlie.io/images/headshots/{slug}.png"

        try:
            r = requests.get(bdl_url, timeout=3)
            if r.status_code == 200:
                return bdl_url
        except:
            pass


    # -----------------------------------------------------
    # 3️⃣ Final fallback — blank avatar
    # -----------------------------------------------------
    return "https://cdn-icons-png.flaticon.com/512/848/848043.png"
