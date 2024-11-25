from DECAF import ConfigReader as _cr_self
from configparser import ConfigParser
from pathlib import Path


# Check if file exists
def _file_exists(filepath):
    file = Path(filepath)
    return file.is_file()


# Reencode filepath to string
def _path_string(filepath):
    return str(Path(filepath).resolve().as_posix())


# Generic relative to absolute path builder
def _build_path(filepath):
    # If path works as-is, return
    if _file_exists(filepath):
        outpath = _path_string(filepath)
        return outpath
    # Try looking from parent directory of loaded ConfigReader.py
    parent_path = _path_string(Path(_cr_self.__file__).parents[1])
    child_path = parent_path + "/" + filepath
    if _file_exists(child_path):
        outpath = _path_string(child_path)
        return outpath
    # Try removing first 4 characters, assumed "src/"
    trunc_filepath = filepath[4:]
    if _file_exists(trunc_filepath):
        outpath = _path_string(trunc_filepath)
        return outpath
    # Error condition: not found
    outpath = "WARNING: not found: " + filepath
    return outpath


# Import config file
def read_config(config_file):
    """Initializes a ConfigParser reading from the provided config_file path."""
    cp = ConfigParser(inline_comment_prefixes=";")
    path = _build_path(config_file)
    cp.read(path)
    return cp


def _parse_to_list(cp, section, key):
    # Read value and strip whitespace
    try:
        fns = cp[section][key].replace(" ", "")
        return fns.split(",")
    except KeyError:
        return None


# Parse [functions] value into list
def parse_functions(cp):
    """Parse ConfigParser functions string."""
    return _parse_to_list(cp, "control", "functions")


# Parse [cleaning] value into list
def parse_cleaning(cp):
    """Parse ConfigParser cleaning string.
    try:
        return _build_path(clean)
    except TypeError:
        return clean"""
    clean = _parse_to_list(cp, "control", "cleaning")
    # If None or list then return
    if clean is None or len(clean) > 1:
        return clean
    # If clean is filepath, return as filepath
    fp = _build_path(clean[0])
    if _file_exists(fp):
        return fp


# Validate type
def _validate_type(cp, mykey, data):
    try:
        val = cp["info"][mykey]
    except KeyError:
        return data is None
    return type(data).__name__ == val


# Validate input type
def validate_input_type(cp, data):
    return _validate_type(cp, "input_type", data)


# Validate output type
def validate_output_type(cp, data):
    return _validate_type(cp, "output_type", data)
