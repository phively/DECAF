import StringFormat


def test_to_lower():
    assert StringFormat.to_lower("THE QUICK BROWN FOX") == "the quick brown fox"
    assert StringFormat.to_lower("12#$,.?! HELLO world") == "12#$,.?! hello world"


def test_trim_witespace():
    assert StringFormat.trim_whitespace("Aa1!Bb.'2@Cc3#") == "Aa1!Bb.'2@Cc3#"
    assert StringFormat.trim_whitespace(" SS ") == "SS"
    assert StringFormat.trim_whitespace(" \t\n\rABC\t\n\r ") == "ABC"
    assert StringFormat.trim_whitespace("  ") == ""


def test_strip_non_numeric():
    assert StringFormat.strip_non_numeric("a123b") == "123"
    assert StringFormat.strip_non_numeric("a 123b") == "123"
    assert StringFormat.strip_non_numeric("a1@23b") == "123"


def test_strip_non_ascii():
    assert StringFormat.strip_non_ascii("Aa1!Bb.'2@Cc3#") == "Aa1!Bb.'2@Cc3#"
    assert StringFormat.strip_non_ascii("random£Θ┘ stuff▼☼") == "random stuff"
    assert StringFormat.strip_non_ascii("ÀËìÔù") == "AEiOu"


def test_strip_punctuation():
    assert StringFormat.strip_punctuation("Hello World!") == "Hello World"
    assert StringFormat.strip_punctuation(" ?!., ") == "  "
