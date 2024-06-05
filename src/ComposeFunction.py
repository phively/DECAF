import functools


# Recursively compose 1 or more functions
def compose_functions(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


# Evaluate a composition of single-argument functions
def eval_functions(input, *functions):
    functions = compose_functions(*functions)
    return functions(input)
