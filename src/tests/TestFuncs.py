import math


def tuplepow(xs, pow):
    out = ()
    # Append each x^2 to out
    for x in xs:
        out += (math.pow(x, pow),)
    return out


def tuplesquare(xs):
    return tuplepow(xs, 2)


def tuplecube(xs):
    return tuplepow(xs, 3)
