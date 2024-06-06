import functools


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
    except:
        obj, name = ["builtins", funcstring]
    return [obj, name]


# Import a list of modules


# Return a function from a string (getattr)
