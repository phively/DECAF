import ConfigReader as cr


def _load_file():
    return


def _write_file():
    return


# Load file(s) from ini specification
def load_files_from_ini(ini_path):
    cp = cr.read_config(ini_path)
    # Extract necessary fields
    functions = cr.parse_functions(cp)
    file1 = cr["control"]["file1"]
    col1 = cr["control"]["column1"]
    file2 = cr["control"]["file2"]
    col2 = cr["control"]["column2"]
    # 1 file, 0 col
    # 1 file, 1 col
    # 1 file, 2 col
    # 2 file, 0 col = INVALID
    # 2 file, 1 col = INVALID
    # 2 file, 2 col
    return
