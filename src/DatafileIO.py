import ConfigReader as cr
import pandas as pd


def _load_files(fp1, cn1="", fp2="", cn2=""):
    # Switching
    nfiles = int(fp1 != "") + int(fp2 != "")
    ncols = int(cn1 != "") + int(cn2 != "")
    # 1 file, 0-3 col
    if nfiles == 1:
        if ncols == 0:
            return pd.read_csv(fp1)
        elif ncols == 1:
            return pd.read_csv(fp1)[cn1]
        elif ncols == 2:
            return pd.read_csv(fp1)[[cn1, cn2]]
    elif nfiles == 2:
        # 2 file, 2 col
        try:
            return pd.read_csv(fp1)[cn1], pd.read_csv(fp2)[cn2]
        # 2 file, 1 or 2 col: INVALID
        except ValueError:
            return


def _write_file(filepath):
    return


# Load file(s) from ini specification
def load_files_from_ini(ini_path):
    cp = cr.read_config(ini_path)
    # Extract necessary fields
    fp1 = cp["control"]["file1"]
    cn1 = cp["control"]["column1"]
    fp2 = cp["control"]["file2"]
    cn2 = cp["control"]["column2"]
    return _load_files(fp1, cn1, fp2, cn2)
