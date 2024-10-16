from configparser import ConfigParser


# Import config file
def read_config(config_file):
    """Initializes a ConfigParser reading from the provided config_file path."""
    cp = ConfigParser(inline_comment_prefixes=";")
    empty = ConfigParser()
    try:
        cp.read(config_file)
        assert cp != empty
    except AssertionError:
        # Try removing 4 characters, assumed "src/"
        cp.read(config_file[4:])
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
    """Parse ConfigParser cleaning string."""
    return _parse_to_list(cp, "control", "cleaning")


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
