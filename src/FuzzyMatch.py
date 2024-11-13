from cleanco import basename
from fuzzywuzzy import fuzz
import numpy as np
import logging


# Remove company suffixes
def remove_company_suffixes(company_name):
    """Removes common company suffixes with cleanco."""
    return basename(company_name)


# Pairwise fuzzy match using WRatio
def fuzzy_match_pairwise(new_str, ref_str):
    """WRatio fuzzywuzzy match score between two strings."""
    if type(new_str) is str:
        return fuzz.WRatio(new_str, ref_str)
    else:
        out = list()
        for x, y in zip(new_str, ref_str):
            out.append(fuzz.WRatio(x, y))
    return out


# Threshold scoring
def score_threshold(score, threshold_high=80, threshold_low=None):
    """Return True when score >= threshold_high.
    If threshold_low exists, tl < score < th returns None."""
    # Check valid threshold
    if not 0 <= threshold_high <= 100:
        logging.exception("Invalid threshold, must be in range [0, 100]")
        return
    # Shortcut if no low threshold
    if threshold_low is None:
        return score >= threshold_high
    # Return None if score in indeterminate range
    try:
        if threshold_low < score < threshold_high:
            return None
        return score >= threshold_high
    except ValueError:
        return np.where(
            (threshold_low < score) & (score < threshold_high),
            None,
            score >= threshold_high,
        )
