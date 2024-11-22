from configparser import ConfigParser
from pathlib import Path


# Check if file exists
def _file_exists(filepath):
    file = Path(filepath)
    return file.is_file()


# Generic relative to absolute path builder
def _build_path(filepath):
    if _file_exists(filepath):
        abs_path = Path(filepath).resolve().as_posix()
        return str(abs_path)
    # Try removing 4 characters, assumed "src/"
    trunc_filepath = filepath[4:]
    abs_path = Path(trunc_filepath).resolve().as_posix()
    return str(abs_path)


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
    try:
        return _build_path(clean[0])
    except TypeError:
        return clean


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
