import pandas as pd
import numpy as np

def compute_final_probability(weighted_prob, ml_prob, w1=0.65, w2=0.35):
    return (weighted_prob * w1) + (ml_prob * w2)

def compute_safety_score(final_prob, consistency, minutes_stability, matchup_score):
    return (
        (0.50 * final_prob) +
        (0.20 * (1 - consistency)) +  # lower std = safer
        (0.15 * minutes_stability) +
        (0.15 * (1 - matchup_score))  # easier matchup = safer
    ) * 100

def rank_safest_props(results):
    """
    results should be a list of dicts:
    {player, stat, line, ml_prob, weighted_prob, safety_score}
    """
    df = pd.DataFrame(results)
    df = df.sort_values("safety_score", ascending=False)
    return df.head(25)
