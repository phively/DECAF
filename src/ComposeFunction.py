import functools


def compose_functions(*functions):
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def eval_functions(input, *functions):
    functions = compose_functions(*functions)
    return functions(input)
