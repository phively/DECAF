import ComposeFunction as cf

helloworld = ["print"]
pythagorean = ["tests.TestFuncs/tuplesquare", "sum", "math.sqrt"]


def test_parse_funcstring_hello_world():
    # Construct print from builtins
    hwfs = cf.parse_funcstring("print")
    assert hwfs == ["builtins", "print"]
    hwm = cf.import_modules_list(hwfs[0])
    assert hwm[0].print == print
    # Test constructed function usage
    assert cf.get_function(hwm[0], "print") == print
    assert cf.get_function(hwm[0], "print")("Hello World!") == print("Hello World!")
    # Test eval of constructed function
    assert cf.eval_functions("Hello World!", cf.get_function(hwm[0], "print")) == print(
        "Hello World!"
    )


def test_parse_funcstring_pythagorean():
    # Parse functions list
    return


def test_import_and_parse():
    return
