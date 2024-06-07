import functools
from importlib import import_module


# Recursively compose 1 or more functions
def compose_functions(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


# Evaluate a composition of single-argument functions
def eval_functions(input, *functions):
    functions = compose_functions(*functions)
    return functions(input)


# Parse an "object.function" string into two strings
def parse_funcstring(funcstring):
    # Try splitting on rightmost . to pull function name
    # If exception then assume builtin object
    try:
        obj, name = funcstring.rsplit(".", 1)
    except ValueError:
        obj, name = ["builtins", funcstring]
    return [obj, name]


# Return a list of modules
def import_modules_list(imports):
    # Convert string to list
    if imports != list(imports):
        imports = [imports]
    modules = list()
    for i in imports:
        modules.append(import_module(i))
    return modules


# Manually add module to global imports
def add_to_global_imports(module):
    globals()[module.__name__] = module


# Return a function from a string (getattr)
def get_function(module, funcname):
    try:
        return getattr(module, funcname)
    except ModuleNotFoundError:
        return None
