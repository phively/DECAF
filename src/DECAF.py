import ComposeFunction as cf
import ConfigReader as cr
import DatafileIO as dio
import FuzzyMatch as fm
import numpy as np


def fuzzy_match_companies(input_file, col1, col2, output_file=None):
    """Fuzzy match companies according to settings in provided config file."""

    # Parameters
    ini_file = "src/config/processing/fuzzy_match_company.ini"

    # Setup - read
    config = cr.read_config(ini_file)
    all_fns = dio.read_functions_from_ini(ini_file)
    # Setup - ini params
    fns_proc = all_fns["functions"]
    fns_clean = all_fns["cleaning"]
    threshold_high = config["parameters"]["threshold_high"]
    threshold_low = config["paraneters"]["threshold_low"]
    file_suffix = config["info"]["name"]

    # Load & process data
    data = dio.load_file(input_file)
    data["clean1"] = cf.eval_functions_list(data[col1], fns_clean)
    data["clean2"] = cf.eval_functions_list(data[col2], fns_clean)

    # Fuzzy match
    data["scores"] = fm.fuzzy_match_pairwise(data["clean1"], data["clean2"])
    data["result"] = np.where(
        fm.score_threshold(
            data["scores"], threshold_high, threshold_low, "match", "nonmatch"
        )
    )

    # Write file
    dio._write_file(data, filepath=input_file + file_suffix + ".csv", type="csv")
