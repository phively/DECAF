from DECAF import ComposeFunction as cf
import math
import pandas as pd
import tests.TestFuncs as tf

helloworld = ["print"]
pythagorean = ["tests.TestFuncs.tuplesquare", "sum", "math.sqrt"]


def test_append_decaf():
    sf = cf._import_modules_list(["StringFormat"])
    assert sf[0].to_lower("THE QUICK BROWN FOX") == "the quick brown fox"
    assert cf._import_modules_list(["FailedImport"]) is None


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
    assert pymods[0].tuplesquare(pytuple) == tf.tuplesquare(pytuple)
    assert pymods[1].sum(pytuple) == sum(pytuple)
    assert pymods[2].sqrt(25.0) == 5.0
    # Construct functions
    pymodfuns = cf._get_functions(pymods, pylist[1])
    assert pymodfuns[0](pytuple) == tf.tuplesquare(pytuple)
    assert pymodfuns[1](pytuple) == sum(pytuple)
    assert pymodfuns[2](25.0) == math.sqrt(25.0)
    # Batch eval
    assert cf.eval_functions(pytuple, pymodfuns[0], pymodfuns[1], pymodfuns[2]) == 5.0
    assert cf.eval_functions(pytuple, *pymodfuns) == 5.0


def test_funclist_to_eval_e2e():
    # Hello World! test
    hw = cf.construct_functions_list(helloworld)
    assert hw == [print]
    assert cf.eval_functions("Hello World!", *hw) == print("Hello World!")
    assert cf.eval_functions_list("Hello World!", helloworld) == print("Hello World!")
    # Pythagorean test
    pytuple = (3, 4)
    pt = cf.construct_functions_list(pythagorean)
    assert pt[1] == sum
    assert cf.eval_functions(pytuple, *pt) == 5.0
    assert cf.eval_functions_list(pytuple, pythagorean) == 5.0


def test_funclist_with_pandas():
    # Operate on a named data frame column
    # Reusable vars
    dataname = "x"
    newname = "square"
    dat = pd.DataFrame({"x": [3.0, 4.0, 5.0]})
    expected_result = [9.0, 16.0, 25.0]
    # Test direct _bundle_args
    fn = cf._bundle_args(tf.col_square, dataname, newname)
    res = cf.eval_functions(dat, fn)
    assert list(res[newname]) == expected_result
    # Test add_args_to_functions_list
    fnlist = cf.construct_functions_list("tests.TestFuncs.col_square")
    fnlist = cf.add_args_to_functions_list(
        fnlist, ["tests.TestFuncs.col_square", dataname, newname]
    )
    results = cf.eval_functions(dat, fnlist)
    assert list(results[newname]) == expected_result


def test_show_work_with_pandas():
    # Operate with multiple functions on a new dataframe column
    dataname = "x"
    newname = "sqrt"
    dat = pd.DataFrame({"x": [3.0, 4.0, 5.0]})
    expected_result = [1.73, 2.0, 2.24]
    # explicit round(sqrt(x))
    fnlist = cf.construct_functions_list(["tests.TestFuncs.col_sqrt", "round"])
    fnlist = cf.add_args_to_functions_list(
        fnlist, [["tests.TestFuncs.col_sqrt", dataname, newname], ["round", 2]]
    )
    results = cf.eval_functions(dat, fnlist)
    assert list(results[newname]) == expected_result
    # show work for function chain
    first_col = "sqrt"
    new_cols = ["round1digit", "square", "roundfinal"]
    fnlist = cf.construct_functions_list(
        ["round", "tests.TestFuncs.tuplesquare", "round"]
    )
    fnlist = cf.add_args_to_functions_list(fnlist, ["round", 1])
    results2 = cf.eval_functions_show_work(dat, first_col, fnlist, col_names=new_cols)
    # Check each intermediate step
    assert list(results2[new_cols[0]]) == [1.7, 2.0, 2.2]
    # Shenanigans to get around floating point inequality
    assert all(
        math.isclose(x, y) for x, y in zip(results2[new_cols[1]], [2.89, 4.0, 4.84])
    )
    assert list(results2[new_cols[2]]) == [2.9, 4.0, 4.8]
