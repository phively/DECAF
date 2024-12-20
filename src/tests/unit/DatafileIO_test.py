from DECAF import DatafileIO as dio
import pandas as pd
from TestFuncs import set_test_path

path = set_test_path()


# Return full path to test ini and test data file
def test_load_files():
    data_path = path + "data/pythagorean_triples.csv"
    # 1 file 0 col
    assert dio._load_files(data_path, "", "", "").equals(pd.read_csv(data_path))
    # 1 file 1 col
    assert dio._load_files(data_path, "c", "", "").equals(pd.read_csv(data_path)["c"])
    # 1 file 2 col
    assert dio._load_files(data_path, "a", "", "b").equals(
        pd.read_csv(data_path)[["a", "b"]]
    )
    # Key Error returns None
    error = dio._load_files(data_path, "a", data_path, "x")
    assert error is None
    # 2 file 2 col
    data_path = path + "data/fuzzy_match_companies.csv"
    rn, nn = dio._load_files(
        fp1=data_path, cn1="reference_name", fp2=data_path, cn2="new_name"
    )
    assert rn.equals(pd.read_csv(data_path)["reference_name"])
    assert nn.equals(pd.read_csv(data_path)["new_name"])
    # csv and xlsx
    my_csv = dio._load_files(data_path)
    my_xls = dio._load_files(path + "data/fuzzy_match_companies.xlsx")
    assert my_csv["reference_name"].equals(my_xls["reference_name"])
    assert my_csv["new_name"].equals(my_xls["new_name"])


# Read functions from a different ini specified by current one
def test_read_functions_from_ini():
    # Exact path provided
    inipath = path + "config/processing/fuzzy_match_company_test.ini"
    # Processing functions
    fmc = dio._fns_from_ini(inipath)
    fns_target = ["FuzzyMatch.fuzzy_match_pairwise", "FuzzyMatch.score_threshold"]
    assert fmc == fns_target
    # Cleaning functions
    fmc = dio._cleaning_from_ini(inipath)
    cleaning_target = [
        "StringFormat.to_lower",
        "StringFormat.trim_whitespace",
        "StringFormat.strip_non_ascii",
        "StringFormat.strip_punctuation",
        "FuzzyMatch.remove_company_suffixes",
    ]
    assert fmc == cleaning_target
    # Unified processing
    fmc = dio.read_functions_from_ini(inipath)
    assert fmc["functions"] == fns_target
    assert fmc["cleaning"] == cleaning_target


# Write xlsx or csv files
def test_write_file():
    # Setup
    filepath = path + "data/DatafileIO_write_test"
    xlsx = ".xlsx"
    csv = ".csv"
    df1 = pd.DataFrame({"letters": ["ABC", "DEF"], "numbers": [123, 456]})
    df2 = pd.DataFrame(None)
    # Write and read a populated datafile
    dio._write_file(df1, filepath + xlsx, "xlsx")
    assert dio.load_file(filepath + xlsx).equals(df1)
    # Test csv
    dio._write_file(df1, filepath + csv, "csv")
    assert dio.load_file(filepath + csv).equals(df1)
    # Write and read an empty datafile
    dio._write_file(df2, filepath + xlsx)
    assert dio.load_file(filepath + xlsx).equals(df2)
