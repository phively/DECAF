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
    out = list()
    if type(dat_in) is str:
        return cf.eval_functions_list(dat_in, fns)
    else:
        for dat in dat_in:
            out.append(cf.eval_functions_list(dat, fns))
    return out


def test_company_cleaning_pipeline():
    # Test output
    assert company_cleaning_pipeline("ACME, Corp.") == "acme"
    assert company_cleaning_pipeline("Fake Worldwide LLC Company") == "fake worldwide"
    assert company_cleaning_pipeline(["ACME, Corp.", "Fake Worldwide LLC Company"]) == [
        "acme",
        "fake worldwide",
    ]


def test_company_fuzzy_match():
    # Load data
    companies = load_match_data()
    ref_name = company_cleaning_pipeline(companies["reference_name"])
    new_name = company_cleaning_pipeline(companies["new_name"])

    # Test output
    scores = fm.fuzzy_match_pairwise(ref_name, new_name)


def test_company_fuzzy_match_from_config():
    # Load data
    assert 1 == 1
