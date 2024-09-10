import functools
from importlib import import_module


# Recursively compose 1 or more functions
def _compose_functions(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


# Evaluate a composition of single-argument functions
def eval_functions(input, *functions):
    """Evaluate a composition of single-argument functions (NOT function name strings)."""
    functions = _compose_functions(*functions)
    return functions(input)


# Parse an "object.function" string into two strings
def _parse_funcstring(funcstring):
    # Try splitting on rightmost . to pull function name
    # If exception then assume builtin object
    try:
        obj, name = funcstring.rsplit(".", 1)
    except ValueError:
        obj, name = ["builtins", funcstring]
    return [obj, name]


# Parse a list of strings into a list of [modules, functions]
def _parse_functions(funclist):
    mods = list()
    fns = list()
    if funclist != list(funclist):
        funclist = [funclist]
    for fs in funclist:
        mod_fn = _parse_funcstring(fs)
        mods.append(mod_fn[0])
        fns.append(mod_fn[1])
    return [mods, fns]


# Return a list of modules
def _import_modules_list(imports):
    # Convert string to list
    if imports != list(imports):
        imports = [imports]
    modules = list()
    for i in imports:
        modules.append(import_module(i))
    return modules


# Manually add module to global imports
def add_to_global_imports(module):
    """Manually adds a module into to the global environment."""
    globals()[module.__name__] = module


# Return a function from a string (getattr)
def _get_function(module, funcname):
    try:
        return getattr(module, funcname)
    except ModuleNotFoundError:
        return None


# Return a list of executable functions
def _get_functions(modules, funcnames):
    out = list()
    if funcnames != list(funcnames):
        modules = [modules]
        funcnames = [funcnames]
    for m, f in zip(modules, funcnames):
        out.append(_get_function(m, f))
    return out


# Take a list of [mod.funs,] and return a list of callable functions
def construct_functions_list(stringlist):
    """Converts a list of strings representing 'module.function' names into functions."""
    # Parse stringlist
    modslist, funcslist = _parse_functions(stringlist)
    # Construct imports list
    mods = _import_modules_list(modslist)
    # Construct functions
    return _get_functions(mods, funcslist)


# Evaluate functions from list of [mod.funs,]
def eval_functions_list(input, stringlist):
    """With input, evaluate a list of strings representing 'module.function' names in order."""
    # Construct functions
    funcs = construct_functions_list(stringlist)
    try:
        return eval_functions(input, *funcs)
    except TypeError:
        out = list()
        for i in input:
            out.append(eval_functions(i, *funcs))
        return out
