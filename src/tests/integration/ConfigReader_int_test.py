from DECAF import ConfigReader as cr
from DECAF import ComposeFunction as cf
import pandas as pd
from TestFuncs import set_test_path

path = set_test_path()


def test_import_parse_eval_helloworld():
    hwdat = pd.read_csv(path + "data/hello_world.txt", header=None)
    # Load config file
    hw = cr.read_config(path + "config/processing/hello_world.ini")
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
    pt = cr.read_config(path + "config/processing/pythagorean_theorem.ini")
    assert pt.sections() == ["info", "control"]
    # Parse and eval function
    funcs = cr.parse_functions(pt)
    assert cf.eval_functions_list(ab, funcs) == c
