import FuzzyMatch as fm
import pandas as pd

path = "src/tests/"


def test_remove_company_suffixes():
    assert fm.remove_company_suffixes("Samsung, Ltd.") == "Samsung"
    assert fm.remove_company_suffixes("ACME Corp") == "ACME"
    assert fm.remove_company_suffixes("Perfect Partners, LLC") == "Perfect Partners"


# Company name fuzzy matching
def test_fuzzy_match_company():
    companies = pd.read_csv(path + "data/fuzzy_match_companies.csv")
    ref_name = companies["reference_name"]
    new_name = companies["new_name"]
