import re
import unicodedata


# Convert to lowercase
def to_lower(string_in):
    return string_in.lower()


# Strip leading/trailing whitespace, including newline and similar
def trim_whitespace(string_in):
    return string_in.strip()


# Strip any non-digits
def strip_non_numeric(string_in):
    return re.sub("[^0-9]", "", string_in)


# Strip non-ASCII characters
def strip_non_ascii(string_in):
    return unicodedata.normalize("NFKD", string_in).encode("ASCII", "ignore").decode()


# Strip punctuation-like characters
def strip_punctuation(string_in):
    return re.sub(r"[^\w\s]", "", string_in)
