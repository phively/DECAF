from configparser import ConfigParser


# Import config file
def read_config(config_file):
    """Initializes a ConfigParser reading from the provided config_file path."""
    cp = ConfigParser()
    cp.read(config_file)
    return cp


# Parse [functions] value into list
def parse_functions(cp):
    """Parse ConfigParser functions string."""
    # Read value and strip whitespace
    fns = cp["control"]["functions"].replace(" ", "")
    return fns.split(",")


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
