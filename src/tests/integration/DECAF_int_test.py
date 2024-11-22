from DECAF import DECAF
from DECAF import DatafileIO as dio
import numpy as np
from TestFuncs import set_test_path

path = set_test_path()


def test_company_fuzzy_match():
    # Params
    filepath = path + "data/fuzzy_match_companies.xlsx"
    inipath = path + "config/processing/fuzzy_match_company.ini"
    outname = "_OUT"
    col1 = "reference_name"
    col2 = "new_name"

    # Run script
    DECAF.fuzzy_match_companies(
        filepath,
        col1,
        col2,
        output_file=outname,
        ini_file=inipath,
    )

    # Check output
    truth = dio.load_file(filepath)
    truth = np.where(
        np.isnan(truth["thresh_expected"]), None, truth["thresh_expected"].astype(bool)
    )

    saved = dio.load_file(filepath + outname + ".csv")
    saved = np.where(saved["match"].isna(), None, saved["match"].astype(bool))

    assert saved.tolist() == truth.tolist()


def test_company_fuzzy_match_e2e():
    # Params
    filepath = path + "data/fuzzy_match_companies.xlsx"
    outname = "_OUT"
    col1 = "reference_name"
    col2 = "new_name"

    # Run script
    DECAF.fuzzy_match_companies(
        input_file=filepath,
        col1=col1,
        col2=col2,
        output_file=outname,
    )

    assert True
