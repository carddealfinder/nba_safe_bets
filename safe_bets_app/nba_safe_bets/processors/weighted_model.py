import numpy as np


def weighted_prediction(probs: list[float]) -> float:
    """Combine probabilities from models with equal weights."""
    if not probs:
        return 0.0
    return float(np.mean(probs))
