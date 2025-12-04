import pandas as pd
import numpy as np

def safe_merge(left, right, left_on, right_on=None, how="left"):
    """
    Wrapper around merge that avoids column overlap errors and logs issues.
    """
    if right_on is None:
        right_on = left_on

    # Remove duplicate columns before merge
    common_cols = set(left.columns).intersection(set(right.columns))
    common_cols -= set([left_on, right_on])

    right = right.drop(columns=list(common_cols), errors="ignore")

    merged = left.merge(right, how=how, left_on=left_on, right_on=right_on)
    return merged


def normalize_column(df, col):
    """
    Normalizes a column to 0-1 range.
    """
    if df[col].max() == df[col].min():
        df[col] = 0
    else:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df
