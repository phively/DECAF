import ConfigReader

path = "src/tests/config/"


# Shared code to set up test configs
def read_test_configs():
    hw = ConfigReader.read_config(path + "processing/hello_world.ini")
    pt = ConfigReader.read_config(path + "processing/pythagorean_theorem.ini")
    return hw, pt


# Find and output config file values
def test_read_config():
    hw, pt = read_test_configs()
    assert hw.sections() == ["info", "control"]
    assert list(hw["info"]) == ["output_type"]
    assert hw["info"]["output_type"] == "str"
    assert pt.sections() == ["info", "control"]
    assert list(pt["control"]) == ["functions"]
    assert pt["control"]["functions"] == "tests.TestFuncs.tuplesquare, sum, math.sqrt"


# Turn comma-delimited functions into a list
def test_parse_functions():
    hw, pt = read_test_configs()
    assert ConfigReader.parse_functions(hw) == ["print"]
    assert ConfigReader.parse_functions(pt) == [
        "tests.TestFuncs.tuplesquare",
        "sum",
        "math.sqrt",
    ]
    assert ConfigReader.parse_cleaning(hw) == ["dummy_function_1", "dummy_function_2"]
    assert ConfigReader.parse_cleaning(pt) is None


# Ensure type checks work
def test_validate_types():
    hw, pt = read_test_configs()
    zz = ConfigReader.read_config(path + "null.ini")
    # Helper function
    assert ConfigReader._validate_type(hw, "output_type", "Hello World!")
    assert ConfigReader._validate_type(pt, "input_type", (3.0, 4.0))
    # Inputs
    assert ConfigReader.validate_input_type(pt, (3.0, 4.0))
    assert ConfigReader.validate_input_type(hw, None)
    assert ConfigReader.validate_input_type(zz, None)
    # Outputs
    assert ConfigReader.validate_output_type(hw, "Hello World!")
    assert ConfigReader.validate_output_type(pt, 5.0)
    assert ConfigReader.validate_output_type(zz, None)
