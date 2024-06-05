import math


def tuplesquare(xs):
    out = ()
    # Append each x^2 to out
    for x in xs:
        out += (math.pow(x, 2),)
    return out
