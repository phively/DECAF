# DECAF
## Data Extraction and Cleaning Automated Framework - in Python!

DECAF provides an extensible framework for performing common data cleaning tasks with modular functions.

## Installation

~~~
# Install from dist (recommended)
python -m pip install FILEPATH\decaf-VERSIONNUMBER.tar.gz

# Compile source
python -m build
~~~

## Module structure

* DECAF: master module, used to specify data files and config inis to use for cleaning
* DatafileIO: reads config inis and reads and writes data

Other modules should not have dependencies on each other.

## Planned features

* String parsing libraries covering common data types: phone number, email, address...
* Exact and fuzzy match options
* RegEx compatibility, possibly some kind of assistant
* Easy creation of compound operations using config files

## To investigate

- [ ] name_matching - company name fuzzy match; see [DeNederlandscheBank/name_matching](https://github.com/DeNederlandscheBank/name_matching/tree/main)
- [x] cleanco - removes common company name suffixes like inc, ltd, etc.