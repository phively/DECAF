import FuzzyMatch as fm


def test_remove_company_suffixes():
    assert fm.remove_company_suffixes("Samsung, Ltd.") == "Samsung"
    assert fm.remove_company_suffixes("ACME Corp") == "ACME"
    assert fm.remove_company_suffixes("Perfect Partners, LLC") == "Perfect Partners"


# Company name fuzzy matching
def test_fuzzy_match_pairwise():
    assert fm.fuzzy_match_pairwise("abcde", "abcde") == 100
    assert fm.fuzzy_match_pairwise("abcxy", "abcde") == 60
    assert (
        fm.fuzzy_match_pairwise("Andrews Banking Corp", "andrews advisory group, llc")
        == 55
    )


# Threshold scoring
def test_score_threshold():
    assert fm.score_threshold(80)
    assert fm.score_threshold(80, threshold_high=79)
    assert fm.score_threshold(80, 0)
    assert fm.score_threshold(60, 59.9)
    assert not fm.score_threshold(79)
    assert not fm.score_threshold(80, 81)
    assert not fm.score_threshold(99, 100)
    assert not fm.score_threshold(99, 99.99)
    # High and low
    assert fm.score_threshold(80, threshold_high=80, threshold_low=60)
    assert fm.score_threshold(50, 51, 49) is None
    assert not fm.score_threshold(50, 60, 50)
    # Invalid thresholds
    assert fm.score_threshold(50, -1) is None
    assert fm.score_threshold(50, 101) is None
