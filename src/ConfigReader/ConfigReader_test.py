import ConfigReader

path = "src/ConfigReader/"
hw = ConfigReader.read_config(path + "config_sample/hello_world.ini")
pt = ConfigReader.read_config(path + "config_sample/pythagorean_theorem.ini")


def test_read_config():
    assert hw.sections() == ["info", "control"]
    assert list(hw["info"]) == ["output_type"]
    assert hw["info"]["output_type"] == "string"
    assert pt.sections() == ["info", "control"]
    assert list(pt["control"]) == ["functions"]
    assert pt["control"]["functions"] == "tuplesquare, sum, math.sqrt"
