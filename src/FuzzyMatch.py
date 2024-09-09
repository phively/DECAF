from cleanco import basename
from fuzzywuzzy import fuzz


# Remove company suffixes
def remove_company_suffixes(company_name):
    return basename(company_name)


# Pairwise fuzzy match using WRatio
def fuzzy_match_pairwise(new_str, ref_str):
    if type(new_str) is str:
        return fuzz.WRatio(new_str, ref_str)
    else:
        out = list()
        for x, y in zip(new_str, ref_str):
            out.append(fuzz.WRatio(x, y))
    return out
