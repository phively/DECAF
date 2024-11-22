import FuzzyMatch as fm
import ComposeFunction as cf
import ConfigReader as cr
import DatafileIO as dio
import pandas as pd
import numpy as np


path = "src/DECAF/tests/"


# Load data
def load_match_data():
    companies = dio.load_file(path + "data/fuzzy_match_companies.csv")
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

    # Append and check scores
    companies["scores"] = fm.fuzzy_match_pairwise(ref_name, new_name)
    companies["result"] = np.where(companies["scores"] >= 80, "match", "new")
    assert companies["expected"].to_list() == companies["result"].to_list()


def test_company_fuzzy_match_from_config():
    # Load data
    companies = load_match_data()
    config = cr.read_config(path + "config/cleaning/clean_company_name.ini")
    fns = cr.parse_functions(config)
    ref_name = cf.eval_functions_list(companies["reference_name"], fns)
    new_name = cf.eval_functions_list(companies["new_name"], fns)

    # Append and check scores
    companies["scores"] = fm.fuzzy_match_pairwise(ref_name, new_name)
    companies["result"] = np.where(companies["scores"] >= 80, "match", "new")
    assert companies["expected"].to_list() == companies["result"].to_list()


def test_company_fuzzy_match_nested_config():
    # Load data
    companies = load_match_data()
    inipath = path + "config/processing/fuzzy_match_company_test.ini"
    config = cr.read_config(inipath)

    # Process functions
    match_fns = cr.parse_functions(config)
    clean_fns = dio._cleaning_from_ini(inipath)
    assert match_fns is not None
    assert clean_fns is not None
    ref_name = cf.eval_functions_list(companies["reference_name"], clean_fns)
    new_name = cf.eval_functions_list(companies["new_name"], clean_fns)

    # Append and check scores
    companies["scores"] = fm.fuzzy_match_pairwise(ref_name, new_name)
    companies["result"] = np.where(companies["scores"] >= 80, "match", "new")
    assert companies["expected"].to_list() == companies["result"].to_list()


def test_company_fuzzy_match_e2e():
    # Params
    datapath = path + "data/fuzzy_match_companies.csv"
    inipath = path + "config/processing/fuzzy_match_company_test.ini"

    # Load data and config
    companies = dio.load_file(datapath)
    config = cr.read_config(inipath)
    ex = dio.load_files_from_ini(inipath)
    assert ex.equals(pd.read_csv(datapath)["expected"])

    # Check params
    match_threshold = int(config["parameters"]["match_threshold"])
    assert match_threshold == 80
    filesuffix = config["info"]["name"]
    assert filesuffix == "_fuzzy_match_company_test"

    # Process functions
    match_fns = cr.parse_functions(config)
    clean_fns = dio._cleaning_from_ini(inipath)
    assert match_fns is not None
    assert clean_fns is not None
    ref_name = cf.eval_functions_list(companies["reference_name"], clean_fns)
    new_name = cf.eval_functions_list(companies["new_name"], clean_fns)

    # Append and check scores
    companies["scores"] = fm.fuzzy_match_pairwise(ref_name, new_name)
    companies["result"] = np.where(
        fm.score_threshold(companies["scores"], match_threshold), "match", "new"
    )
    assert ex.to_list() == companies["result"].to_list()

    # Write data to csv
    dio._write_file(companies, filepath=datapath + filesuffix + "_test.csv", type="csv")
    saved_companies = pd.read_csv(datapath + filesuffix + "_test.csv")
    assert saved_companies["scores"].equals(companies["scores"])
