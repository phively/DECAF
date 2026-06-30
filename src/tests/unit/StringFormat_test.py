from DECAF import StringFormat as sf


def test_string_errors():
    assert sf._safe_string(1.0) == "1.0"
    assert sf.to_lower(1) == "1"
    assert sf.strip_non_numeric(3.0) == "30"


def test_to_lower():
    assert sf.to_lower("THE QUICK BROWN FOX") == "the quick brown fox"
    assert sf.to_lower("12#$,.?! HELLO world") == "12#$,.?! hello world"


def test_trim_witespace():
    assert sf.trim_whitespace("Aa1!Bb.'2@Cc3#") == "Aa1!Bb.'2@Cc3#"
    assert sf.trim_whitespace(" SS ") == "SS"
    assert sf.trim_whitespace(" \t\n\rABC\t\n\r ") == "ABC"
    assert sf.trim_whitespace("  ") == ""


def test_strip_non_numeric():
    assert sf.strip_non_numeric("a123b") == "123"
    assert sf.strip_non_numeric("a 123b") == "123"
    assert sf.strip_non_numeric("a1@23b") == "123"


def test_strip_non_ascii():
    assert sf.strip_non_ascii("Aa1!Bb.'2@Cc3#") == "Aa1!Bb.'2@Cc3#"
    assert sf.strip_non_ascii("random£Θ┘ stuff▼☼") == "random stuff"
    assert sf.strip_non_ascii("ÀËìÔù") == "AEiOu"


def test_strip_punctuation():
    assert sf.strip_punctuation("Hello World!") == "Hello World"
    assert sf.strip_punctuation(" ?!., ") == "  "
