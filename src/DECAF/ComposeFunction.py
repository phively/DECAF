import functools
from importlib import import_module


# Recursively compose 1 or more functions
def _compose_functions(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


# Helper to bundle multi-argument functions
def _bundle_args(func, *args, **kwargs):
    """Combine a function and its *args into one object to pass through eval_functions."""
    return lambda x: functools.partial(func, x)(*args, **kwargs)


# Ensure input is a list/tuple
def _tolist(input):
    """Convert input to a list, if not already a list/tuple."""
    if isinstance(input, (list, tuple)):
        return list(input)
    return [input]


# Evaluate a composition of single-argument functions
def eval_functions(input, *functions):
    """Evaluate a composition of single-argument functions (NOT function name strings).
    For multiple arguments, use _bundle_args first."""
    # Correct for lists versus single arguments
    fns = list()
    for fn in functions:
        if isinstance(fn, (list, tuple)):
            fns.extend(fn)
        else:
            fns.append(fn)
    # Compute results
    functions = _compose_functions(*fns)
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
    funclist = _tolist(funclist)
    for fs in funclist:
        mod_fn = _parse_funcstring(fs)
        mods.append(mod_fn[0])
        fns.append(mod_fn[1])
    return [mods, fns]


# Return a list of modules
def _import_modules_list(imports):
    # Convert string to list
    imports = _tolist(imports)
    modules = list()
    for i in imports:
        # If module not found, try DECAF.module
        try:
            modules.append(import_module(i))
        except ModuleNotFoundError:
            try:
                modules.append(import_module("DECAF." + i))
            except ModuleNotFoundError:
                return None
    return modules


# Manually add module to global imports
def add_to_global_imports(module):
    """Manually adds a module into to the global environment."""
    globals()[module.__name__] = module


# Return a function from a string (getattr)
def _get_function(module, funcname):
    try:
        return getattr(module, funcname)
    except AttributeError:
        return None


# Return a list of executable functions
def _get_functions(modules, funcnames):
    out = list()
    modules = _tolist(modules)
    funcnames = _tolist(funcnames)
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


# Helper to add *args to a functions list
def _add_args_single_fn(fns_list, fn_to_edit, *args):
    """Searches fns_list for the specified function and bundles it with the
    supplied *args."""
    output = list()
    # Delimited module.function name
    fn_mod, fn_fn = _parse_funcstring(fn_to_edit)
    fn_check = fn_mod + "." + fn_fn
    # Main loop: search fns_list for specific fn_to_edit to add *args
    for fn in fns_list:
        curr_name = fn.__module__ + "." + fn.__name__
        if curr_name == fn_check:
            fn = _bundle_args(fn, *args)
        output.append(fn)
    return output


# Helper to add [args] list to corresponding [fn] names
def add_args_to_functions_list(fns_list, fns_to_edit):
    """
    Searches fns_list for each of fns_to_edit and bundle with embedded args.

    Single function to edit:
    ["fn_name", arg1, arg2, ...]

    Multiple functions to edit:
    [
        [fn_name_1, arg1, arg2, ...],
        [fn_name_2, arg1, arg2, ...]
    ]
    """
    # Input/output cleaning
    fns_to_edit = _tolist(fns_to_edit)
    # Check if list is properly nested
    if isinstance(fns_to_edit[0], str):
        fns_to_edit = [fns_to_edit]
    # Iterate through fns_to_edit
    output = fns_list
    for fns in fns_to_edit:
        fn_name, *args = fns
        output = _add_args_single_fn(output, fn_name, *args)
    return output


# Evaluate functions from list of [mod.funs,]
def eval_functions_list(input, stringlist):
    """On input, evaluate an ordered list of strings representing 'module.function'
    names."""
    # Construct functions
    funcs = construct_functions_list(stringlist)
    try:
        return eval_functions(input, *funcs)
    except TypeError:
        out = list()
        for i in input:
            out.append(eval_functions(i, *funcs))
        return out
    # Catch list as input
    except AttributeError:
        return [eval_functions(i, *funcs) for i in input]


# Sequentially evaluate functions on a dataframe column, saving each intermediate step
def eval_functions_show_work(df, first_col, func_list, col_names):
    """On input, evaluate an ordered list of functions, or strings representing
    'module.function' names, and save each as an intermediate step using the provided
    list of column names.
    """
    # Error check
    assert len(func_list) == len(
        col_names
    ), "Mismatch: functions and new_col_names must be equal length"
    # Setup
    if isinstance(func_list[0], str):
        funcs = construct_functions_list(func_list)
    else:
        funcs = func_list
    curr_col = first_col  # next working column
    # Iterate through functions and column names
    for f, cn in zip(funcs, col_names):
        df[cn] = eval_functions(df[curr_col], f)
        curr_col = cn
    return df
