import pandas as pd

def add_prop_labels(df):
    """
    Creates binary labels for all alternate totals.
    """

    # Points lines
    pts_lines = [5, 10, 15, 20, 25, 30, 35]
    for line in pts_lines:
        df[f"HIT_PTS_{line}"] = (df["PTS"] >= line).astype(int)

    # Rebounds lines
    reb_lines = [4, 6, 8, 10, 12, 14]
    for line in reb_lines:
        df[f"HIT_REB_{line}"] = (df["REB"] >= line).astype(int)

    # Assists lines
    ast_lines = [2, 4, 6, 8, 10, 12]
    for line in ast_lines:
        df[f"HIT_AST_{line}"] = (df["AST"] >= line).astype(int)

    # 3PM lines
    three_lines = [1, 2, 3, 4, 5]
    for line in three_lines:
        df[f"HIT_3PM_{line}"] = (df["FG3M"] >= line).astype(int)

    return df
