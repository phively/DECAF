import ComposeFunction as cf
import math
from tests.TestFuncs import tuplesquare

helloworld = ["print"]
pythagorean = ["tests.TestFuncs.tuplesquare", "sum", "math.sqrt"]


def test_parse_funcstring_hello_world():
    # Construct print from builtins
    hwfs = cf._parse_funcstring("print")
    assert hwfs == ["builtins", "print"]
    hwm = cf._import_modules_list(hwfs[0])
    assert hwm[0].print == print
    # Test constructed function usage
    assert cf._get_function(hwm[0], "print") == print
    assert cf._get_function(hwm[0], "print")("Hello World!") == print("Hello World!")
    # Test eval of constructed function
    assert cf.eval_functions(
        "Hello World!", cf._get_function(hwm[0], "print")
    ) == print("Hello World!")


def test_parse_eval_functions_pythagorean():
    pytuple = (3, 4)
    # Parse functions list
    pylist = cf._parse_functions(pythagorean)
    assert pylist[0] == ["tests.TestFuncs", "builtins", "math"]
    assert pylist[1] == ["tuplesquare", "sum", "sqrt"]
    # Construct imports list
    pymods = cf._import_modules_list(pylist[0])
    assert pymods[0].tuplesquare(pytuple) == tuplesquare(pytuple)
    assert pymods[1].sum(pytuple) == sum(pytuple)
    assert pymods[2].sqrt(25.0) == 5.0
    # Construct functions
    pymodfuns = cf._get_functions(pymods, pylist[1])
    assert pymodfuns[0](pytuple) == tuplesquare(pytuple)
    assert pymodfuns[1](pytuple) == sum(pytuple)
    assert pymodfuns[2](25.0) == math.sqrt(25.0)
    # Batch eval
    assert cf.eval_functions(pytuple, pymodfuns[0], pymodfuns[1], pymodfuns[2]) == 5.0
    assert cf.eval_functions(pytuple, *pymodfuns) == 5.0


def test_import_and_parse():
    return
