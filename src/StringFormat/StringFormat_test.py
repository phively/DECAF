import StringFormat
import unittest


def test_strip_non_numeric():
    assert StringFormat.strip_non_numeric("a123b") == "123"
    assert StringFormat.strip_non_numeric("a 123b") == "123"
    assert StringFormat.strip_non_numeric("a1@23b") == "123"
