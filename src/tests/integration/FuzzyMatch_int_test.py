import FuzzyMatch as fm
import ComposeFunction as cf
import pandas as pd

path = "src/tests/"


# Load data
def load_match_data():
    companies = pd.read_csv(path + "data/fuzzy_match_companies.csv")
    return companies


# Manually specified cleaning pipeline
def company_cleaning_pipeline(dat_in):
    fns = [
        "StringFormat.to_lower",
        "StringFormat.trim_whitespace",
        "StringFormat.strip_non_ascii",
        "StringFormat.strip_punctuation",
        "FuzzyMatch.remove_company_suffixes",
    ]
    return cf.eval_functions_list(dat_in, fns)


def test_company_cleaning_pipeline():
    assert company_cleaning_pipeline("ACME, Corp.") == "acme"


def test_company_fuzzy_match():
    # Load data
    companies = load_match_data()
    ref_name = companies["reference_name"]
    new_name = companies["new_name"]

    # Test output


def test_company_fuzzy_match_from_config():
    # Load data
    assert 1 == 1
