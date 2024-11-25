from DECAF import ComposeFunction as cf
from DECAF import ConfigReader as cr
from DECAF import DatafileIO as dio
from DECAF import FuzzyMatch as fm


def fuzzy_match_companies(
    input_file,
    col1,
    col2,
    output_file=None,
    ini_file="DECAF/config/processing/fuzzy_match_company.ini",
):
    """Fuzzy match companies according to settings in provided config file."""

    # Setup - read
    config = cr.read_config(ini_file)
    all_fns = dio.read_functions_from_ini(ini_file)
    # Setup - ini params
    # fns_proc = all_fns["functions"]
    fns_clean = all_fns["cleaning"]
    threshold_high = int(config["parameters"]["threshold_high"])
    threshold_low = int(config["parameters"]["threshold_low"])
    file_suffix = config["info"]["name"]

    # Load & process data
    data = dio.load_file(input_file)
    data["clean1"] = cf.eval_functions_list(data[col1], fns_clean)
    data["clean2"] = cf.eval_functions_list(data[col2], fns_clean)

    # Fuzzy match
    data["scores"] = fm.fuzzy_match_pairwise(data["clean1"], data["clean2"])
    data["match"] = fm.score_threshold(data["scores"], threshold_high, threshold_low)

    # Write file
    if output_file is not None:
        file_suffix = output_file
    dio._write_file(data, filepath=input_file + file_suffix + ".csv", type="csv")
