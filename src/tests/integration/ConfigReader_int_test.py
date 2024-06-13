import ConfigReader as cr
import ComposeFunction as cf
import pandas as pd

path = "src/tests/"


def test_import_parse_eval_helloworld():
    hwdat = pd.read_csv(path + "data/hello_world.txt", header=None)
    # Load config file
    hw = cr.read_config(path + "config/hello_world.ini")
    assert hw.sections() == ["info", "control"]
    # Parse and eval function
    funcs = cr.parse_functions(hw)
    assert cf.eval_functions_list(hwdat, funcs) == print(hwdat)


def test_import_parse_eval_pythagorean():
    pydat = pd.read_csv(path + "data/pythagorean_triples.csv")
    # Structure data
    c = pydat["c"].copy()
    ab = pydat.copy().drop("c", axis=1)
    # ab is a list of tuples, c is a list of floats
    ab = list(ab.itertuples(index=False, name=None))
    c = list(c)
    # Load config file
    pt = cr.read_config(path + "config/pythagorean_theorem.ini")
    assert pt.sections() == ["info", "control"]
    # Parse and eval function
    funcs = cr.parse_functions(pt)
    assert cf.eval_functions_list(ab, funcs) == c
