import re


# Strip any non-digits
def strip_non_numeric(string_in):
    return re.sub("[^0-9]", "", string_in)


# Strip leading/trailing whitespace, including newline and similar
def trim_whitespace(string_in):
    return string_in.strip()
