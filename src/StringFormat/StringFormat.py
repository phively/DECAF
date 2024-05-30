import re

def strip_non_numeric(stringIn):
    return re.sub("[^0-9]", "", stringIn)