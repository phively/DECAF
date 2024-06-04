import ConfigReader


def read_test_configs(path="src/ConfigReader/"):
    hw = ConfigReader.read_config(path + "config_sample/hello_world.ini")
    pt = ConfigReader.read_config(path + "config_sample/pythagorean_theorem.ini")
    return hw, pt


def test_read_config():
    hw, pt = read_test_configs()
    assert hw.sections() == ["info", "control"]
    assert list(hw["info"]) == ["output_type"]
    assert hw["info"]["output_type"] == "string"
    assert pt.sections() == ["info", "control"]
    assert list(pt["control"]) == ["functions"]
    assert pt["control"]["functions"] == "tuplesquare, sum, math.sqrt"


def test_parse_functions():
    hw, pt = read_test_configs()
    assert ConfigReader.parse_functions(hw) == ["print"]
    assert ConfigReader.parse_functions(pt) == ["tuplesquare", "sum", "math.sqrt"]
