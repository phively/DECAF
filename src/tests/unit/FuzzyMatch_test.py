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
