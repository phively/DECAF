import re


def strip_non_numeric(string_in):
    return re.sub("[^0-9]", "", string_in)


def trim_whitespace(string_in):
    return string_in.strip()
