import ComposeFunction
import math


def tuplesquare(xs):
    out = ()
    # Append each x^2 to out
    for x in xs:
        out += (math.pow(x, 2),)
    return out


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