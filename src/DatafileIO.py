import ConfigReader as cr
import ComposeFunction as cf
import pandas as pd


def load_file(filepath):
    """Load data files into a pandas dataframe."""
    filepath = cr._build_path(filepath)
    try:
        return pd.read_csv(filepath)
    except ValueError:
        return pd.read_excel(filepath)


def _load_files(fp1, cn1="", fp2="", cn2=""):
    # Counts for switch statement
    nfiles = int(fp1 != "") + int(fp2 != "")
    ncols = int(cn1 != "") + int(cn2 != "")
    # Build absolute paths
    fp1 = cr._build_path(fp1)
    fp2 = cr._build_path(fp2)
    # 1 file, 0-3 col
    if nfiles == 1:
        if ncols == 0:
            return load_file(fp1)
        elif ncols == 1:
            return load_file(fp1)[cn1]
        elif ncols == 2:
            return load_file(fp1)[[cn1, cn2]]
    elif nfiles == 2:
        # 2 file, 2 col
        try:
            return load_file(fp1)[cn1], pd.read_csv(fp2)[cn2]
        # 2 file, 1 or 2 col: INVALID
        except ValueError:
            return


def _write_file(dataframe, filepath, type="xlsx"):
    if type in ("xls", "xlsx"):
        dataframe.to_excel(filepath, index=False)
    if type == "csv":
        dataframe.to_csv(filepath, index=False)
    return


# Load file(s) from ini specification
def load_files_from_ini(ini_path):
    """Load data file and columns specified in .ini as a dataframe."""
    ini_path = cr._build_path(ini_path)
    cp = cr.read_config(ini_path)
    # Extract necessary fields
    fp1 = cp["control"]["file1"]
    cn1 = cp["control"]["column1"]
    fp2 = cp["control"]["file2"]
    cn2 = cp["control"]["column2"]
    return _load_files(fp1, cn1, fp2, cn2)


def dataloader(ini_path):
    """Process ini, loading files with specified function."""
    ini_path = cr._build_path(ini_path)
    cp = cr.read_config(ini_path)
    fns = cr.parse_functions(cp)
    return cf.eval_functions_list(ini_path, fns)


# Process ini files and extract relevant functions
def _fns_from_ini(ini_path):
    ini_path = cr._build_path(ini_path)
    fns = ["ConfigReader.read_config", "ConfigReader.parse_functions"]
    return cf.eval_functions_list(ini_path, fns)


def _cleaning_from_ini(ini_path):
    ini_path = cr._build_path(ini_path)
    path_fns = [
        "ConfigReader.read_config",
        "ConfigReader.parse_cleaning",
    ]
    clean_path = cf.eval_functions_list(ini_path, path_fns)
    fns = [
        "ConfigReader.read_config",
        "ConfigReader.parse_functions",
    ]
    return cf.eval_functions_list(clean_path, fns)


def read_functions_from_ini(ini_path):
    fns = _fns_from_ini(ini_path)
    cln = _cleaning_from_ini(ini_path)
    return {"functions": fns, "cleaning": cln}
