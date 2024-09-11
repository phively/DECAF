import DatafileIO as dio
import ConfigReader as cr
import pandas as pd

config_path = "src/tests/config/"


# Return full path to test ini and test data file
def _get_paths(ini):
    ini_path = config_path + ini
    cp = cr.read_config(ini_path)
    data_path = cp["control"]["file1"]
    return ini_path, data_path


def test_load_files_from_ini():
    ini_path, data_path = _get_paths("load_pythagorean_triples_all.ini")
    assert dio.load_files_from_ini(ini_path).equals(pd.read_csv(data_path))
    # 1 file 1 col
    ini_path, data_path = _get_paths("load_pythagorean_triples_cols_c.ini")

    # 1 file 2 col
    ini_path, data_path = _get_paths("load_pythagorean_triples_cols_ab.ini")

    # 2 file 2 col
    ini_path, data_path = _get_paths("load_fuzzy_match_companies.ini")
