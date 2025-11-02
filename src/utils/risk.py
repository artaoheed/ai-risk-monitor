from __future__ import annotations
import numpy as np

def score_to_0_100(anomaly_scores):
    # Normalize anomaly scores to 0..100 using rank-based method
    ranks = np.argsort(np.argsort(anomaly_scores)).astype(float)
    scaled = 100.0 * ranks / max(len(anomaly_scores)-1, 1)
    return scaled
