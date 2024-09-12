import DatafileIO as dio
import pandas as pd

config_path = "src/tests/"


# Return full path to test ini and test data file
def test_load_files():
    data_path = config_path + "data/pythagorean_triples.csv"
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
