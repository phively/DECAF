from DECAF import ComposeFunction
from TestFuncs import tuplesquare
import math
import builtins


def test_compose_functions():
    assert ComposeFunction._compose_functions(sum) == sum
    assert ComposeFunction._compose_functions(math.pow) == math.pow
    assert ComposeFunction._compose_functions(math.sqrt) == math.sqrt


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
    # List operator
    assert (
        ComposeFunction.eval_functions(pytuple, *[tuplesquare, sum, math.sqrt]) == 5.0
    )


def test_parse_funcstring():
    # Basic object.function
    assert ComposeFunction._parse_funcstring("ab.cd") == ["ab", "cd"]
    assert ComposeFunction._parse_funcstring("math.mod") == ["math", "mod"]
    # Extract function from longer.object
    assert ComposeFunction._parse_funcstring("tests.TestFuncs.tuplesquare") == [
        "tests.TestFuncs",
        "tuplesquare",
    ]
    # Access a built-in function
    assert ComposeFunction._parse_funcstring("print") == ["builtins", "print"]


def test_parse_functions():
    # String
    assert ComposeFunction._parse_functions("print") == [["builtins"], ["print"]]
    assert ComposeFunction._parse_functions("math.sqrt") == [["math"], ["sqrt"]]
    # Single function
    assert ComposeFunction._parse_functions(["ab.cd"]) == [["ab"], ["cd"]]
    # Multiple functions
    assert ComposeFunction._parse_functions(["ab.cd", "ef.gh", "ij.kl.mn"]) == [
        ["ab", "ef", "ij.kl"],
        ["cd", "gh", "mn"],
    ]


def test_import_modules():
    # Single import as list
    m = ComposeFunction._import_modules_list(["re"])
    assert m[0].sub("a", "", "abc") == "bc"
    # Single import as string
    n = ComposeFunction._import_modules_list("re")
    assert n[0].sub("a", "", "abc") == "bc"
    # Import to globals
    ComposeFunction.add_to_global_imports(m[0])
    # Custom import
    ci = ComposeFunction._import_modules_list("tests.TestFuncs")
    tup = (1, 2, 3)
    assert ci[0].tuplecube(tup) == (1, 8, 27)
    # Multi import
    mi = ComposeFunction._import_modules_list(["math", "re"])
    assert mi[0].sqrt(16.0) == 4.0
    assert mi[1].sub("a", "", "abc") == "bc"


def test_get_function():
    # Basic function equivalence
    assert ComposeFunction._get_function(math, "sqrt") == math.sqrt
    assert ComposeFunction._get_function(builtins, "print") == print
    # Function operations
    assert ComposeFunction._get_function(math, "sqrt")(16.0) == 4.0
    assert ComposeFunction._get_function(builtins, "print")("Hello World!") == print(
        "Hello World!"
    )
    # Module not found
    assert ComposeFunction._get_function(math, "FakeFuncCausesErr") is None


def test_get_functions():
    # Test single functions
    assert ComposeFunction._get_functions(math, "sqrt")[0] == math.sqrt
    assert ComposeFunction._get_functions([math], ["sqrt"])[0] == math.sqrt
    # Test multiple functions
    mf = ComposeFunction._get_functions([math, builtins], ["sqrt", "print"])
    assert mf[0] == math.sqrt
    assert mf[1] == builtins.print
    # Test evaluation
    assert mf[0](9.0) == math.sqrt(9.0)
