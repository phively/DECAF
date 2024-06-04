from configparser import ConfigParser


# Import config file
def read_config(config_file):
    cp = ConfigParser()
    cp.read(config_file)
    return cp
