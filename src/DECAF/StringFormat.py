import re
import unicodedata


# Safe string handling
def _safe_string(input):
    if input is None:
        input = ""
    elif type(input) == float or type(input) == int:
        input = str(input)
    return input


# Convert to lowercase
def to_lower(string_in):
    out = _safe_string(string_in).lower()
    return out


# Strip leading/trailing whitespace, including newline and similar
def trim_whitespace(string_in):
    out = _safe_string(string_in).strip()
    return out


# Strip any non-digits
def strip_non_numeric(string_in):
    out = re.sub("[^0-9]", "", _safe_string(string_in))
    return out


# Strip non-ASCII characters
def strip_non_ascii(string_in):
    out = (
        unicodedata.normalize("NFKD", _safe_string(string_in))
        .encode("ASCII", "ignore")
        .decode()
    )
    return out


# Strip punctuation-like characters
def strip_punctuation(string_in):
    out = re.sub(r"[^\w\s]", "", _safe_string(string_in))
    return out
