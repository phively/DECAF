import ComposeFunction
from tests.TestFuncs import tuplesquare
import math


def test_compose_functions():
    assert ComposeFunction.compose_functions(sum) == sum
    assert ComposeFunction.compose_functions(math.pow) == math.pow
    assert ComposeFunction.compose_functions(math.sqrt) == math.sqrt


def test_eval_functions():
    pytuple = (3, 4)
    # 3 + 4
    assert ComposeFunction.eval_functions(pytuple, sum) == 7
    # (3^2, 4^2)
    assert ComposeFunction.eval_functions(pytuple, tuplesquare) == (9.0, 16.0)
    # 3^2 + 4^2
    assert ComposeFunction.eval_functions(pytuple, tuplesquare, sum) == 25.0
    # sqrt(3^2 + 4^2)
    assert ComposeFunction.eval_functions(pytuple, tuplesquare, sum, math.sqrt) == 5.0


def test_parse_funcstring():
    # Basic object.function
    assert ComposeFunction.parse_funcstring("ab.cd") == ["ab", "cd"]
    assert ComposeFunction.parse_funcstring("math.mod") == ["math", "mod"]
    # Extract function from longer.object
    assert ComposeFunction.parse_funcstring("tests.TestFuncs.tuplesquare") == [
        "tests.TestFuncs",
        "tuplesquare",
    ]
    # Access a built-in function
    assert ComposeFunction.parse_funcstring("print") == ["builtins", "print"]
