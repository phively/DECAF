from DECAF import ComposeFunction as cf
from tests.TestFuncs import tuplesquare
from tests.TestFuncs import tuplesqrt
import pandas as pd
import math
import builtins


def test_compose_functions():
    assert cf._compose_functions(sum) == sum
    assert cf._compose_functions(math.pow) == math.pow
    assert cf._compose_functions(math.sqrt) == math.sqrt


def test_eval_functions():
    pytuple = (3, 4)
    # 3 + 4
    assert cf.eval_functions(pytuple, sum) == 7
    # (3^2, 4^2)
    assert cf.eval_functions(pytuple, tuplesquare) == (9.0, 16.0)
    # 3^2 + 4^2
    assert cf.eval_functions(pytuple, tuplesquare, sum) == 25.0
    # sqrt(3^2 + 4^2)
    assert cf.eval_functions(pytuple, tuplesquare, sum, math.sqrt) == 5.0
    # List operator
    assert cf.eval_functions(pytuple, *[tuplesquare, sum, math.sqrt]) == 5.0


def test_parse_funcstring():
    # Basic object.function
    assert cf._parse_funcstring("ab.cd") == ["ab", "cd"]
    assert cf._parse_funcstring("math.mod") == ["math", "mod"]
    # Extract function from longer.object
    assert cf._parse_funcstring("tests.TestFuncs.tuplesquare") == [
        "tests.TestFuncs",
        "tuplesquare",
    ]
    # Access a built-in function
    assert cf._parse_funcstring("print") == ["builtins", "print"]


def test_parse_functions():
    # String
    assert cf._parse_functions("print") == [["builtins"], ["print"]]
    assert cf._parse_functions("math.sqrt") == [["math"], ["sqrt"]]
    # Single function
    assert cf._parse_functions(["ab.cd"]) == [["ab"], ["cd"]]
    # Multiple functions
    assert cf._parse_functions(["ab.cd", "ef.gh", "ij.kl.mn"]) == [
        ["ab", "ef", "ij.kl"],
        ["cd", "gh", "mn"],
    ]


def test_import_modules():
    # Single import as list
    m = cf._import_modules_list(["re"])
    assert m[0].sub("a", "", "abc") == "bc"
    # Single import as string
    n = cf._import_modules_list("re")
    assert n[0].sub("a", "", "abc") == "bc"
    # Import to globals
    cf.add_to_global_imports(m[0])
    # Custom import
    ci = cf._import_modules_list("tests.TestFuncs")
    tup = (1, 2, 3)
    assert ci[0].tuplecube(tup) == (1, 8, 27)
    # Multi import
    mi = cf._import_modules_list(["math", "re"])
    assert mi[0].sqrt(16.0) == 4.0
    assert mi[1].sub("a", "", "abc") == "bc"


def test_get_function():
    # Basic function equivalence
    assert cf._get_function(math, "sqrt") == math.sqrt
    assert cf._get_function(builtins, "print") == print
    # Function operations
    assert cf._get_function(math, "sqrt")(16.0) == 4.0
    assert cf._get_function(builtins, "print")("Hello World!") == print("Hello World!")
    # Module not found
    assert cf._get_function(math, "FakeFuncCausesErr") is None


def test_get_functions():
    # Test single functions
    assert cf._get_functions(math, "sqrt")[0] == math.sqrt
    assert cf._get_functions([math], ["sqrt"])[0] == math.sqrt
    # Test multiple functions
    mf = cf._get_functions([math, builtins], ["sqrt", "print"])
    assert mf[0] == math.sqrt
    assert mf[1] == builtins.print
    # Test evaluation
    assert mf[0](9.0) == math.sqrt(9.0)


def test_eval_show_work():
    mydata = [1.0, 2.0, 3.0, 4.0, 5.0]
    ts = tuplesquare(mydata)
    nums = pd.DataFrame({"n": mydata})
    # Test a single function
    result = cf.eval_functions_show_work(
        nums, "n", ["TestFuncs.tuplesquare"], ["square"]
    )
    assert (result["square"].tolist()) == list(ts)
    # Test multiple functions
    tsr = tuplesqrt(ts)
    result2 = cf.eval_functions_show_work(
        nums,
        "n",
        ["TestFuncs.tuplesquare", "TestFuncs.tuplesqrt"],
        ["square2", "sqrt2"],
    )
    assert (result2["square2"].tolist()) == list(ts)
    assert (result2["sqrt2"].tolist()) == list(tsr)
    # Test prebuilt functions
    fns = cf.construct_functions_list(["TestFuncs.tuplesquare", "TestFuncs.tuplesqrt"])
    result = cf.eval_functions_show_work(nums, "n", fns, ["square3", "sqrt3"])
    assert (result2["square3"].tolist()) == list(ts)
    assert (result2["sqrt3"].tolist()) == list(tsr)


def test_compose_functions_with_args():
    # round(x, 2)
    round2d = cf._compose_functions(cf._bundle_args(round, 2))
    # round(5.333, 2)
    assert cf.eval_functions(5.3333, round2d) == 5.33
    # round(sqrt(5), 2)
    assert cf.eval_functions(5, math.sqrt, round2d) == round(math.sqrt(5), 2)
    # List operator
    assert cf.eval_functions(7, *[math.sqrt, round2d]) == round(math.sqrt(7), 2)
    # Package function
    choose5 = cf._bundle_args(math.comb, 5)
    # 10 choose 5
    assert cf.eval_functions(10, choose5) == 252


def test_edit_funcstring_with_args():
    # Test builtins
    f = cf.construct_functions_list("round")
    round2d = cf._bundle_args(f[0], 2)
    assert cf.eval_functions(5.333, round2d) == 5.33
    round2d_v2 = cf._add_args_single_fn(f, "round", 2)
    assert cf.eval_functions(5.333, round2d_v2) == 5.33
    # Test imports
    f = cf.construct_functions_list("math.comb")
    choose5 = cf._add_args_single_fn(f, "math.comb", 5)
    assert cf.eval_functions(10, choose5) == 252
    # Test chain of functions
    f = cf.construct_functions_list(["math.sqrt", "round"])
    sqrtround2 = cf._add_args_single_fn(f, "round", 2)
    assert cf.eval_functions(5.0, sqrtround2) == 2.24
    sqrtround0 = cf._add_args_single_fn(f, "round", 0)
    assert cf.eval_functions(5.0, sqrtround0) == 2.0


def test_edit_multiple_fns_with_args():
    # Single fn to add args
    f = cf.construct_functions_list(["math.sqrt", "round"])
    sqrtround2d = cf.add_args_to_functions_list(f, ["round", 2])
    assert cf.eval_functions(5, sqrtround2d) == 2.24
    # Multiple fns to add args
    f = cf.construct_functions_list(["math.sqrt", "round", "int", "math.comb"])
    sqrtround0dcomb5 = cf.add_args_to_functions_list(
        f, [["round", 0], ["math.comb", 5]]
    )
    assert cf.eval_functions(105, sqrtround0dcomb5) == 252
    assert cf.eval_functions(26, sqrtround0dcomb5) == 1
    # Multiple args within one fn
    f = cf.construct_functions_list(["math.sqrt", "round", "int", "pow"])
    sqrtround0pow5mod3 = cf.add_args_to_functions_list(f, [["round", 0], ["pow", 5, 3]])
    assert cf.eval_functions(101, sqrtround0pow5mod3) == 1
    assert cf.eval_functions(26.25, sqrtround0pow5mod3) == 2
