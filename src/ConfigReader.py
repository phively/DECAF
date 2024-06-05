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
