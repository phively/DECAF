import DatafileIO as dio
import pandas as pd

config_path = "src/tests/"


# Return full path to test ini and test data file
def test_load_files():
    data_path = config_path + "data/pythagorean_triples.csv"
    # 1 file 0 col
    assert dio._load_files(data_path, "", "", "").equals(pd.read_csv(data_path))
    # 1 file 1 col
    assert dio._load_files(data_path, "c", "", "").equals(pd.read_csv(data_path)["c"])
    # 1 file 2 col
    assert dio._load_files(data_path, "a", "", "b").equals(
        pd.read_csv(data_path)[["a", "b"]]
    )
    # 2 file 2 col
    data_path = config_path + "data/fuzzy_match_companies.csv"
    rn, nn = dio._load_files(
        fp1=data_path, cn1="reference_name", fp2=data_path, cn2="new_name"
    )
    assert rn.equals(pd.read_csv(data_path)["reference_name"])
    assert nn.equals(pd.read_csv(data_path)["new_name"])
    # csv and xlsx
    my_csv = dio._load_files(data_path)
    my_xls = dio._load_files(config_path + "data/fuzzy_match_companies.xlsx")
    assert my_csv.equals(my_xls)


# Read functions from a different ini specified by current one
def test_read_cleaning_from_ini():
    # Exact path provided
    pfmc = dio._read_cleaning_from_ini(
        config_path + "config/processing/fuzzy_match_company.ini"
    )
    assert pfmc == [
        "StringFormat.to_lower",
        "StringFormat.trim_whitespace",
        "StringFormat.strip_non_ascii",
        "StringFormat.strip_punctuation",
        "FuzzyMatch.remove_company_suffixes",
    ]


# Write xlsx files
def test_write_file():
    # Setup
    path = "src/tests/data/DatafileIO_write_test.xlsx"
    df1 = pd.DataFrame({"letters": ["ABC", "DEF"], "numbers": [123, 456]})
    df2 = pd.DataFrame(None)
    # Write and read a populated datafile
    dio._write_file(df1, path)
    assert dio.load_file(path).equals(df1)
    # Write and read an empty datafile
    dio._write_file(df2, path)
    assert dio.load_file(path).equals(df2)
