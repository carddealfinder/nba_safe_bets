def get_player_list(season="2024-25"):
    url = "https://stats.nba.com/stats/commonallplayers"

    params = {
        "LeagueID": "00",
        "Season": season,
        "IsOnlyCurrentSeason": 1
    }

    data = safe_request(url, params=params, headers=HEADERS)

    # ----------------------------
    # Handle API failure
    # ----------------------------
    if data is None:
        print("[ERROR] NBA API blocked or returned no data for players.")
        # Return empty but properly structured DataFrame
        return pd.DataFrame(columns=["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"])

    try:
        rows = data["resultSets"][0]["rowSet"]
        headers = data["resultSets"][0]["headers"]
    except Exception as e:
        print("[ERROR] Unexpected NBA API structure:", e)
        return pd.DataFrame(columns=["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"])

    df = pd.DataFrame(rows, columns=headers)

    df.rename(columns={
        "PERSON_ID": "PLAYER_ID",
        "DISPLAY_FIRST_LAST": "PLAYER_NAME"
    }, inplace=True)

    # Ensure columns exist even if missing from the API
    if "PLAYER_ID" not in df.columns:
        df["PLAYER_ID"] = None
    if "PLAYER_NAME" not in df.columns:
        df["PLAYER_NAME"] = ""
    if "TEAM_ID" not in df.columns:
        df["TEAM_ID"] = None

    return df[["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]]
