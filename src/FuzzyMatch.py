from name_matching.name_matcher import NameMatcher as company_name_matcher


# Initialize name matcher
def initialize_company_fuzzy_matcher():
    cnm = company_name_matcher(
        top_n=10,
        lowercase=True,
        punctuations=True,
        remove_ascii=True,
        legal_suffixes=False,
        common_words=False,
        verbose=True,
    )
    return cnm


# Pairwise fuzzy match
def fuzzy_match_company(new, reference, matcher):
    return
