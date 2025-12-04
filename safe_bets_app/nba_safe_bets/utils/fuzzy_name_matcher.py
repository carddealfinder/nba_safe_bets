import pandas as pd
from rapidfuzz import process, fuzz


class PlayerNameMatcher:
    """
    Provides robust fuzzy name matching for DraftKings -> Player IDs (Balldontlie)
    """

    def __init__(self, players_df):
        """
        players_df must contain:
            PLAYER_ID, PLAYER_NAME
        """
        self.players_df = players_df
        self.name_list = players_df["PLAYER_NAME"].tolist()

    def match(self, raw_name, score_cutoff=80):
        """
        Returns PLAYER_ID for the best fuzzy match.
        If no match above score_cutoff, returns None.
        """
        if not isinstance(raw_name, str):
            return None

        match_name, score, idx = process.extractOne(
            raw_name,
            self.name_list,
            scorer=fuzz.token_sort_ratio
        )

        if score < score_cutoff:
            return None

        # return matched player's ID
        return self.players_df.iloc[idx]["PLAYER_ID"]

    def add_ids_to_dataframe(self, df, name_column="player_name"):
        """
        Takes any DF with a name column and adds PLAYER_ID.
        Useful for DK props, injury reports, logs, etc.
        """
        df = df.copy()

        df["PLAYER_ID"] = df[name_column].apply(self.match)

        missing = df["PLAYER_ID"].isna().sum()
        if missing > 0:
            print(f"[FUZZY MATCH WARNING] {missing} players could not be matched.")

        return df
