import StringFormat


def test_strip_non_numeric():
    assert StringFormat.strip_non_numeric("a123b") == "123"
    assert StringFormat.strip_non_numeric("a 123b") == "123"
    assert StringFormat.strip_non_numeric("a1@23b") == "123"


def test_trim_witespace():
    assert StringFormat.trim_whitespace("Aa1!Bb.'2@Cc3#") == "Aa1!Bb.'2@Cc3#"
    assert StringFormat.trim_whitespace(" SS ") == "SS"
    assert StringFormat.trim_whitespace(" \t\n\rABC\t\n\r ") == "ABC"
    assert StringFormat.trim_whitespace("  ") == ""
