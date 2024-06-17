from configparser import ConfigParser


# Import config file
def read_config(config_file):
    cp = ConfigParser()
    cp.read(config_file)
    return cp


# Parse [functions] value into list
def parse_functions(cp):
    # Read value and strip whitespace
    fns = cp["control"]["functions"].replace(" ", "")
    return fns.split(",")


# Validate input type
def validate_input_type(cp, data):
    try:
        intype = cp["info"]["input_type"]
    except KeyError:
        return data is None
    return type(data).__name__ == intype


# Validate output type
def validate_output_type(cp, data):
    try:
        outtype = cp["info"]["output_type"]
    except KeyError:
        return data is None
    return type(data).__name__ == outtype
