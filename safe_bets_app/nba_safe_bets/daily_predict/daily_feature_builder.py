import pandas as pd
from nba_safe_bets.scrapers.balldontlie_players import get_player_list
from nba_safe_bets.scrapers.schedule_scraper import get_todays_schedule
from nba_safe_bets.scrapers.injury_report import get_injury_report


def build_daily_features():
    """
    Returns a merged dataframe with placeholder stats so the model
    pipeline does not crash if stats are unavailable.
    """

    players = get_player_list()
    schedule = get_todays_schedule()
    injuries = get_injury_report()

    print("Players DF Shape:", players.shape)
    print("Schedule DF Shape:", schedule.shape)
    print("Injury DF Shape:", injuries.shape)

    # --- Merge Players + Injuries ---
    df = players.merge(injuries, on="id", how="left")

    # injury factor = 1 if player appears in injury report
    df["injury_factor"] = df["injury_status"].notna().astype(int)

    # --------------------------------------------------------------
    # TEMPORARY PLACEHOLDER GAME STATS (PREVENTS MODEL CRASH)
    # --------------------------------------------------------------
    # Later these will be replaced with real stats from game_logs
    df["points"] = 0
    df["rebounds"] = 0
    df["assists"] = 0
    df["threes"] = 0

    # --------------------------------------------------------------
    # ASSIGN GAME ID (fallback = 0 if player's team not scheduled)
    # --------------------------------------------------------------
    df["game_id"] = 0
    if not schedule.empty:
        # build mapping from team → game_id
        team_to_game = {}
        for _, row in schedule.iterrows():
            team_to_game[row["home_team"]] = row["game_id"]
            team_to_game[row["visitor_team"]] = row["game_id"]

        df["game_id"] = df["team"].map(team_to_game).fillna(0).astype(int)

    # Clean up missing values
    df.fillna(0, inplace=True)

    print("Merged DF Shape:", df.shape)
    return df
