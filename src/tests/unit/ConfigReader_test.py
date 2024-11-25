from DECAF import ConfigReader as cr
from TestFuncs import set_test_path

path = set_test_path()
config_path = path + "config/"


# Shared code to set up test configs
def read_test_configs():
    hw = cr.read_config(config_path + "processing/hello_world.ini")
    pt = cr.read_config(config_path + "processing/pythagorean_theorem.ini")
    return hw, pt


# Check filepath validation and construction
def test_filepaths():
    # Check if file exists
    hw_path = "processing/hello_world.ini"
    assert cr._file_exists(config_path + hw_path)
    assert not cr._file_exists(hw_path)
    # Check absolute paths
    abs_path = cr._build_path(config_path + hw_path)
    assert cr._file_exists(abs_path)
    # Check relative paths
    hw_rel_path = "cleaning/../" + hw_path
    rel_path = cr._build_path(config_path + hw_rel_path)
    assert cr._file_exists(rel_path)
    # Check removing src/
    hw_src_path = "src/" + config_path + hw_path
    src_path = cr._build_path(hw_src_path)
    assert cr._file_exists(src_path)
    # Check parent directory path
    rel_cleaning_ref = "DECAF/config/processing/fuzzy_match_company.ini"
    rel_cleaning_path = cr._build_path(rel_cleaning_ref)
    assert cr._file_exists(rel_cleaning_path)
    # Check error condition
    err_path = "DoesNotExist"
    err_output = cr._build_path(err_path)
    assert err_output == "WARNING: not found: " + err_path


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
    assert cr.parse_functions(hw) == ["print"]
    assert cr.parse_functions(pt) == [
        "tests.TestFuncs.tuplesquare",
        "sum",
        "math.sqrt",
    ]
    assert cr.parse_cleaning(hw) == ["dummy_function_1", "dummy_function_2"]
    assert cr.parse_cleaning(pt) is None
    # Check error handling
    zz = cr.read_config(config_path + "null.ini")
    assert cr.parse_cleaning(zz) is None


# Ensure type checks work
def test_validate_types():
    hw, pt = read_test_configs()
    zz = cr.read_config(config_path + "null.ini")
    # Helper function
    assert cr._validate_type(hw, "output_type", "Hello World!")
    assert cr._validate_type(pt, "input_type", (3.0, 4.0))
    # Inputs
    assert cr.validate_input_type(pt, (3.0, 4.0))
    assert cr.validate_input_type(hw, None)
    assert cr.validate_input_type(zz, None)
    # Outputs
    assert cr.validate_output_type(hw, "Hello World!")
    assert cr.validate_output_type(pt, 5.0)
    assert cr.validate_output_type(zz, None)
